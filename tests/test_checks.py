"""Prove checker behavior with small adversarial fixtures, all stored inside the repo."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from site_checks import (Document, WEB, local_target, metadata_issues, read_document,
                         reference_issues, required_disclaimer, structure_issues)


class ParserTests(unittest.TestCase):
    def test_entities_nested_text_and_void_tags(self):
        doc = Document('<p>Prepare <strong>&amp; hold</strong><br> then relax</p>'
                       '<script>not public copy</script>')
        self.assertEqual("Prepare & hold then relax", doc.root.text)
        self.assertEqual("Prepare & hold then relax", doc.find("p")[0].text)

    def test_duplicate_ids_are_detected(self):
        doc = Document('<div id="same"></div><section id="same"></section>')
        self.assertIn("empty or duplicate id: 'same'", structure_issues(doc, False))

    def test_missing_landmarks_and_skipped_headings_are_detected(self):
        problems = structure_issues(Document('<h1>Title</h1><h3>Jump</h3>'))
        self.assertIn("exactly one main is required", problems)
        self.assertIn("heading level skipped", problems)

    def test_canonical_is_exact_and_metadata_required(self):
        doc = Document('<meta name="viewport" content="width=device-width">'
                       '<meta name="description" content="Routine support">'
                       '<link rel="canonical" href="https://gohealax.com/">')
        self.assertEqual([], metadata_issues(doc, "https://gohealax.com/"))
        self.assertTrue(metadata_issues(doc, "https://gohealax.com/About.html"))
        self.assertEqual(3, len(metadata_issues(Document(""), "https://gohealax.com/")))

    def test_disclaimer_is_read_from_prod_01(self):
        text = required_disclaimer()
        self.assertTrue(text.startswith("GoHealaX does not diagnose"))
        self.assertTrue(text.endswith("exercise programme."))


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        artifacts = WEB / ".artifacts"
        artifacts.mkdir(exist_ok=True)
        self.temp = TemporaryDirectory(prefix="checker-", dir=artifacts)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.page = self.root / "index.html"
        self.page.write_text('<html lang="en"><title>Title</title><p id="local">Text</p></html>')
        (self.root / "About.html").write_text('<h1 id="a b">About &amp; contact</h1>')
        (self.root / "poster.png").write_bytes(b"fixture")

    def issues(self, source):
        return reference_issues(self.root, self.page, Document(source))

    def test_query_fragment_entity_and_root_links_resolve(self):
        self.assertEqual([], self.issues('<a href="About.html?x=1&amp;y=2#a%20b">About</a>'
                                         '<a href="/#local">Top</a><a href="#local">Here</a>'))

    def test_missing_target_case_and_fragment_fail(self):
        issues = self.issues('<a href="about.html">Wrong case</a>'
                             '<a href="About.html#missing">Wrong ID</a>')
        self.assertEqual(2, len(issues))
        self.assertIn("missing local target", issues[0])
        self.assertIn("missing fragment", issues[1])

    def test_external_destinations_are_not_fetched(self):
        self.assertEqual([], self.issues('<a href="https://example.invalid/missing">External</a>'
                                         '<a href="mailto:b.lp.self@gmail.com">Email</a>'))

    def test_encoded_traversal_and_unsafe_scheme_rejected(self):
        for url in ("../secret", "%2e%2e/secret", "javascript:alert(1)", "file:///etc/passwd"):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    local_target(self.root, self.page, url)

    def test_symlink_escape_rejected(self):
        # Link points to existing repo content outside this fixture, without touching that content.
        (self.root / "escape.html").symlink_to(WEB / "site/About.html")
        self.assertIn("escapes site root", self.issues('<a href="escape.html">Escape</a>')[0])

    def test_local_assets_and_srcset_checked(self):
        self.assertEqual([], self.issues('<img src="poster.png" srcset="poster.png 1x">'))
        self.assertEqual(2, len(self.issues('<video poster="missing.png">'
                                          '<source src="missing.mp4"></video>')))

    def test_base_rejected_to_avoid_misresolved_links(self):
        self.assertIn("base element", self.issues('<base href="https://example.invalid/">')[0])

    def test_read_document_preserves_ids(self):
        self.assertEqual(["local"], read_document(self.page).ids)


if __name__ == "__main__":
    unittest.main()
