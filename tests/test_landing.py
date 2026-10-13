"""WEB-02 landing contract, enforced independently of later release gates."""

import unittest

from site_checks import CONTACT, SITE, metadata_issues, read_document, structure_issues


class LandingTests(unittest.TestCase):
    def setUp(self):
        self.doc = read_document(SITE / 'index.html')

    def test_landing_structure_and_order(self):
        self.assertEqual([], structure_issues(self.doc))
        self.assertEqual([], metadata_issues(self.doc, "https://gohealax.com/"))
        self.assertEqual(['home', 'benefits', 'demo', 'mission', 'features',
                          'download', 'team', 'contact'],
                         [n.attrs.get('id') for n in self.doc.find('section')])
        self.assertFalse(any(n.attrs.get('http-equiv', '').lower() == 'refresh'
                             for n in self.doc.find('meta')))
        self.assertTrue(all(n.attrs.get('type') == 'module' and n.attrs.get('src') in {'site.js', 'media.js'} for n in self.doc.find('script')))
        self.assertTrue(any(n.attrs.get('name') == 'viewport' for n in self.doc.find('meta')))

    def test_plain_navigation_and_honest_availability(self):
        links = {n.attrs.get('href') for n in self.doc.find('nav')[0].find('a')}
        self.assertTrue({'index.html#home', 'index.html#features', 'index.html#demo',
                         'index.html#mission', 'index.html#download', 'index.html#team',
                         'index.html#contact', 'About.html', 'privacy-policy.html'} <= links)
        self.assertIn('Android download link coming soon', self.doc.root.text)
        self.assertIn('All current Android features are free', self.doc.root.text)
        self.assertIn('Coming Soon', self.doc.root.text)
        self.assertTrue(any(n.attrs.get('href') == CONTACT for n in self.doc.find('a')))
        self.assertFalse(any('play.google.com' in n.attrs.get('href', '') or
                             'apps.apple.com' in n.attrs.get('href', '')
                             for n in self.doc.find('a')))

    def test_hero_is_local_responsive_and_explicitly_sized(self):
        hero = self.doc.find('picture')[0].find('img')[0]
        self.assertTrue(hero.attrs['src'].startswith('assets/'))
        self.assertTrue(hero.attrs['alt'])
        self.assertEqual('eager', hero.attrs['loading'])
        self.assertIn('srcset', hero.attrs)
        for key in ('width', 'height'):
            self.assertGreater(int(hero.attrs[key]), 0)


if __name__ == '__main__':
    unittest.main()
