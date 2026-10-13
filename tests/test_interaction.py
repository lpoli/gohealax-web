"""WEB-04 HTML fallbacks and legal guarantees; interactions run in the browser."""
import unittest
from urllib.parse import urlsplit
from site_checks import SITE, read_document, required_disclaimer

class InteractionTests(unittest.TestCase):
    def test_exact_legal_disclaimer(self):
        for route in ('About.html', 'privacy-policy.html', 'medical-disclaimer.html'):
            doc = read_document(SITE / route)
            self.assertIn(required_disclaimer(), [n.text for n in doc.find('p')])

    def test_navigation_fallback_and_modules(self):
        for page in SITE.glob('*.html'):
            doc = read_document(page)
            nav = doc.find('nav')[0]
            self.assertNotIn('hidden', nav.attrs)
            if page.name == '404.html':
                self.assertFalse(doc.find('button') + doc.find('script'))
                self.assertTrue(all(n.attrs['href'].startswith('/') for n in nav.find('a')))
                continue
            self.assertEqual('site-navigation', nav.attrs['id'])
            button = doc.find('button')[0]
            self.assertIn('hidden', button.attrs)
            self.assertEqual('site-navigation', button.attrs['aria-controls'])
            self.assertTrue(any(n.attrs == {'type': 'module', 'src': 'site.js'} for n in doc.find('script')))
            self.assertTrue(any(n.attrs.get('href') == 'medical-disclaimer.html' for n in doc.find('a')))

    def test_disabled_demo_is_local_and_has_no_player(self):
        doc = read_document(SITE / 'index.html')
        demo = next(n for n in doc.root.walk() if 'data-media-provider' in n.attrs)
        self.assertEqual('disabled', demo.attrs['data-media-provider'])
        self.assertEqual([], demo.find('button'))
        self.assertEqual([], demo.find('iframe') + demo.find('video'))
        self.assertTrue((SITE / demo.attrs['data-media-poster']).is_file())
        self.assertIn('Demo coming soon', demo.text)

    def test_website_privacy_separates_unverified_hosting_and_media(self):
        text = read_document(SITE / 'privacy-policy.html').root.text
        for phrase in ('hosting operator has not yet been verified', 'no media requests',
                       'explicitly choose Play', 'no developer-added cookies', 'service worker'):
            self.assertIn(phrase, text)
        self.assertNotIn('site is hosted through GitHub Pages', text)

    def test_initial_html_resources_are_local(self):
        for page in SITE.glob('*.html'):
            doc = read_document(page)
            self.assertFalse(doc.find('iframe') + doc.find('video'))
            for node in doc.root.walk():
                if node.tag in {'img', 'script', 'source'} and 'src' in node.attrs:
                    self.assertFalse(urlsplit(node.attrs['src']).netloc)
                if node.tag == 'link':
                    self.assertFalse({'preconnect', 'dns-prefetch'} & set(node.attrs.get('rel', '').split()))
                    if node.attrs.get('rel') == 'stylesheet':
                        self.assertFalse(urlsplit(node.attrs['href']).netloc)
