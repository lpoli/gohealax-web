"""WEB-05 release-quality rules, shared by audit and mandatory regression tests."""
import struct
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit

from site_checks import (SITE, local_target, metadata_issues, read_document, references,
                         reference_issues, required_disclaimer, structure_issues)

CANONICALS = {name: 'https://gohealax.com/' + ('' if name == 'index.html' else name)
              for name in ('index.html', 'About.html', 'privacy-policy.html', 'medical-disclaimer.html')}


def image_dimensions(path):
    data = path.read_bytes()
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return struct.unpack('>II', data[16:24])
    if data[:4] == b'RIFF' and data[8:16] == b'WEBPVP8 ':
        width, height = struct.unpack('<HH', data[26:30])
        return width & 16383, height & 16383
    raise ValueError(f'unsupported image format: {path.name}')


def quality_issues(root=SITE):
    findings, titles, descriptions = [], [], []
    def add(route, issues):
        findings.extend(f'{route}: {issue}' for issue in issues)
    for route in [*CANONICALS, '404.html']:
        page = root / route
        if not page.is_file():
            add(route, ['required page missing']); continue
        doc = read_document(page)
        issues = structure_issues(doc) + reference_issues(root, page, doc)
        if route in CANONICALS:
            issues += metadata_issues(doc, CANONICALS[route])
            titles.extend(n.text for n in doc.find('title'))
            descriptions.extend(n.attrs.get('content') for n in doc.find('meta') if n.attrs.get('name') == 'description')
            props = {n.attrs.get('property'): n.attrs.get('content') for n in doc.find('meta')}
            expected = {'og:type': 'website', 'og:url': CANONICALS[route],
                        'og:image': 'https://gohealax.com/assets/social.png',
                        'og:image:width': '1200', 'og:image:height': '630'}
            for key, value in expected.items():
                if props.get(key) != value: issues.append(f'{key} must be {value}')
            for key in ('og:title', 'og:description', 'og:image:alt'):
                if not props.get(key): issues.append(f'{key} missing')
            if not doc.find('title') or props.get('og:title') != doc.find('title')[0].text:
                issues.append('social title differs from page title')
            if route != 'index.html' and required_disclaimer() not in doc.root.text:
                issues.append('exact PROD-01 disclaimer missing')
        else:
            if not any(n.attrs.get('name') == 'robots' and 'noindex' in n.attrs.get('content', '').split(',') for n in doc.find('meta')):
                issues.append('404 must be noindex')
            if any(n.attrs.get('rel') == 'canonical' for n in doc.find('link')):
                issues.append('404 must have no canonical')
            for url in references(doc):
                if not urlsplit(url).scheme and not url.startswith(('/', '#')):
                    issues.append(f'404 requires root-relative URLs: {url}')
        if not any(n.attrs.get('rel') == 'icon' for n in doc.find('link')):
            issues.append('favicon missing')
        if not any('skip-link' in n.attrs.get('class', '').split() and n.attrs.get('href') == '#main' for n in doc.find('a')) or 'main' not in doc.ids:
            issues.append('working skip link required')
        if any(n.attrs.get('http-equiv', '').lower() == 'refresh' for n in doc.find('meta')):
            issues.append('homepage redirect forbidden')
        for node in doc.root.walk():
            urls = []
            for attr in ('src', 'poster', 'srcset'):
                if attr in node.attrs:
                    urls.extend(item.strip().split()[0] for item in node.attrs[attr].split(',') if item.strip())
            if node.tag == 'link' and set(node.attrs.get('rel', '').split()) & {'stylesheet', 'icon', 'preload', 'preconnect', 'dns-prefetch', 'apple-touch-icon'}:
                urls.append(node.attrs.get('href', ''))
            if any(urlsplit(url).scheme or urlsplit(url).netloc for url in urls):
                issues.append('initial third-party resource forbidden')
        for image in doc.find('img'):
            attrs = image.attrs
            if 'alt' not in attrs: issues.append('image alt attribute missing')
            try:
                declared = tuple(int(attrs[key]) for key in ('width', 'height'))
                target = local_target(root, page, attrs.get('src', ''))
                if target is None or declared != image_dimensions(target[0]):
                    issues.append('image dimensions differ from asset')
            except (ValueError, KeyError, OSError, struct.error):
                issues.append('valid image dimensions required')
            hero = 'hero-' in attrs.get('src', '')
            logo = 'brand-logo' in attrs.get('class', '').split()
            if attrs.get('loading') != ('eager' if hero or logo else 'lazy'):
                issues.append('hero/header logo must be eager and below-fold images lazy')
            if hero and (not attrs.get('srcset') or not attrs.get('sizes') or attrs.get('fetchpriority') != 'high'):
                issues.append('responsive high-priority hero required')
        add(route, issues)
    if len(set(titles)) != len(titles): add('metadata', ['titles must be unique'])
    if len(set(descriptions)) != len(descriptions): add('metadata', ['descriptions must be unique'])
    try:
        tree = ET.parse(root / 'sitemap.xml')
        urls = [n.text for n in tree.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        if sorted(urls) != sorted(CANONICALS.values()): add('sitemap.xml', ['must list exactly the four canonicals'])
    except (OSError, ET.ParseError): add('sitemap.xml', ['valid sitemap required'])
    try:
        if (root / 'robots.txt').read_text() != 'User-agent: *\nAllow: /\n\nSitemap: https://gohealax.com/sitemap.xml\n':
            add('robots.txt', ['expected crawl rules and absolute sitemap required'])
    except OSError: add('robots.txt', ['required quality file missing'])
    try:
        if image_dimensions(root / 'assets/social.png') != (1200, 630): add('social.png', ['must be 1200 by 630'])
    except (OSError, ValueError, struct.error): add('social.png', ['valid social image required'])
    css = (root / 'site.css').read_text() if (root / 'site.css').is_file() else ''
    if '@import' in css or 'url(' in css: add('site.css', ['review CSS resource requests before permitting url/import'])
    return findings
