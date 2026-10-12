"""Offline HTML/URL checks shared by the baseline tests and target-quality audit."""

from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

WEB = Path(__file__).resolve().parents[1]
SITE = WEB / "site"
REPO = WEB.parent
CONTACT = "mailto:b.lp.self@gmail.com"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def find(self, tag):
        return [node for node in self.walk() if node.tag == tag]

    def walk(self):
        for child in self.children:
            if isinstance(child, Node):
                yield child
                yield from child.walk()

    @property
    def text(self):
        def parts(node):
            if node.tag in {"script", "style"}:
                return
            for child in node.children:
                if isinstance(child, str):
                    yield child
                else:
                    yield from parts(child)
        return " ".join(" ".join(parts(self)).split())


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)

    def find(self, tag):
        return self.root.find(tag)

    @property
    def ids(self):
        return [node.attrs["id"] for node in self.root.walk() if "id" in node.attrs]


def read_document(path):
    return Document(path.read_text(encoding="utf-8"))


def required_disclaimer():
    """Read PROD-01 from its canonical owner instead of maintaining a second literal."""
    text = (REPO / "docs/product/requirements.md").read_text(encoding="utf-8")
    line = next(line for line in text.splitlines() if line.startswith("**PROD-01 "))
    return line.split("“", 1)[1].split("”", 1)[0]


def local_target(root, page, url):
    """Return (local path, decoded fragment), or None for approved external schemes."""
    parsed = urlsplit(url)
    if parsed.scheme in {"http", "https", "mailto", "tel"} or (
        not parsed.scheme and parsed.netloc
    ):
        return None
    if parsed.scheme:
        raise ValueError(f"unsupported URL scheme: {parsed.scheme}")
    root = root.resolve()
    path = unquote(parsed.path)
    if "\\" in path:
        raise ValueError("backslash in local URL")
    target = (root / path.lstrip("/") if path.startswith("/") else
              page.parent / path if path else page).resolve()
    if not target.is_relative_to(root):
        raise ValueError("local URL escapes site root")
    if target.is_dir():
        target /= "index.html"
    return target, unquote(parsed.fragment)


def references(document):
    for node in document.root.walk():
        for attr in ("href", "src", "poster"):
            if attr in node.attrs:
                yield node.attrs[attr]
        # Local responsive assets only; data URLs are deliberately unsupported.
        if "srcset" in node.attrs:
            for candidate in node.attrs["srcset"].split(","):
                if candidate.strip():
                    yield candidate.strip().split()[0]


def reference_issues(root, page, document):
    issues = []
    if document.find("base"):
        issues.append("base element is unsupported; use document-relative links")
    for url in references(document):
        try:
            result = local_target(root, page, url)
            if result is None:
                continue
            target, fragment = result
            if not target.is_file():
                issues.append(f"missing local target: {url}")
            elif fragment and target.suffix.lower() == ".html":
                if fragment not in read_document(target).ids:
                    issues.append(f"missing fragment: {url}")
        except ValueError as error:
            issues.append(f"{url}: {error}")
    return issues


def structure_issues(document, landmarks=True):
    issues = []
    for name, count in Counter(document.ids).items():
        if not name or count > 1:
            issues.append(f"empty or duplicate id: {name!r}")
    html = document.find("html")
    if len(html) != 1 or not html[0].attrs.get("lang"):
        issues.append("one html element with language is required")
    titles = document.find("title")
    if len(titles) != 1 or not titles[0].text:
        issues.append("one nonempty title is required")
    if landmarks:
        for tag in ("header", "main", "footer", "h1"):
            if len(document.find(tag)) != 1:
                issues.append(f"exactly one {tag} is required")
        if not document.find("nav"):
            issues.append("navigation landmark is required")
        headings = [int(node.tag[1]) for node in document.root.walk()
                    if node.tag in {"h1", "h2", "h3", "h4", "h5", "h6"}]
        if any(b > a + 1 for a, b in zip(headings, headings[1:])):
            issues.append("heading level skipped")
    return issues


def metadata_issues(document, canonical):
    issues = []
    for name in ("viewport", "description"):
        matches = [n for n in document.find("meta") if n.attrs.get("name") == name]
        if len(matches) != 1 or not matches[0].attrs.get("content", "").strip():
            issues.append(f"one nonempty {name} metadata entry is required")
    urls = [n.attrs.get("href") for n in document.find("link")
            if "canonical" in n.attrs.get("rel", "").split()]
    if urls != [canonical]:
        issues.append(f"canonical must be {canonical}")
    return issues
