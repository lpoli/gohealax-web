"""WEB-03 content and screenshot guarantees; owner acceptance is recorded separately."""

import unittest
import hashlib
import json
import struct

from site_checks import CONTACT, SITE, WEB, read_document


class ContentTests(unittest.TestCase):
    def test_product_explanations_are_available_without_scripts(self):
        for route in ('index.html', 'About.html'):
            with self.subTest(route=route):
                doc = read_document(SITE / route)
                text = doc.find('main')[0].text
                for phrase in ('Prepare', 'Hold', 'Relax', 'Count Pace', 'seconds per count',
                               'zero counts', 'repetition', 'set', 'presets',
                               "Today's Exercises", 'schedules', 'while the app is open',
                               'History', 'Statistics', 'planned and completed sets',
                               'do not measure recovery', 'create your own exercises'):
                    self.assertIn(phrase, text)
                self.assertFalse(doc.find('script'))

    def test_availability_and_contact_are_honest(self):
        for route in ('index.html', 'About.html'):
            with self.subTest(route=route):
                doc = read_document(SITE / route)
                text = doc.find('main')[0].text
                for phrase in ('All current Android features are free',
                               'Android download link coming soon', 'iOS', 'Coming Soon',
                               'Contributor introductions are coming soon'):
                    self.assertIn(phrase, text)
                for obsolete in ('can be downloaded through Google Play', 'pilot release'):
                    self.assertNotIn(obsolete, text)
                self.assertTrue(any(n.attrs.get('href') == CONTACT and
                                    'b.lp.self@gmail.com' in n.text for n in doc.find('a')))
                self.assertFalse(any('play.google.com' in n.attrs.get('href', '') or
                                     'apps.apple.com' in n.attrs.get('href', '')
                                     for n in doc.find('a')))

    def test_editing_locations_are_marked_and_social_links_are_absent(self):
        for route in ('index.html', 'About.html'):
            source = (SITE / route).read_text()
            self.assertIn('<!-- Contributor edits:', source)
            self.assertIn('<!-- Social edits:', source)
            links = read_document(SITE / route).find('a')
            self.assertFalse(any(domain in n.attrs.get('href', '') for n in links
                                 for domain in ('facebook.com', 'instagram.com', 'linkedin.com',
                                                'twitter.com', 'x.com/')))

    def test_owner_wording_is_present(self):
        for route in ('index.html', 'About.html'):
            text = read_document(SITE / route).find('main')[0].text
            self.assertIn('User can totally focus on exercise rather than mental counting.', text)
            self.assertIn('Track your exercises and routine', text)
            self.assertNotIn('pilot', text.lower())

    def test_screenshot_assets_match_review_register_and_have_example_captions(self):
        register = json.loads((WEB / 'asset-sources/screenshots.json').read_text())
        entries = {e['deployable'].removeprefix('site/'): e for e in register['screenshots']}
        figures = [n for n in read_document(SITE / 'index.html').find('figure')
                   if 'app-screenshot' in n.attrs.get('class', '').split()]
        self.assertEqual(4, len(figures))
        self.assertEqual(set(entries), {n.find('img')[0].attrs['src'] for n in figures})
        for figure in figures:
            img = figure.find('img')[0]
            entry = entries[img.attrs['src']]
            data = (SITE / img.attrs['src']).read_bytes()
            self.assertEqual(b'\x89PNG\r\n\x1a\n', data[:8])
            self.assertEqual((int(img.attrs['width']), int(img.attrs['height'])),
                             struct.unpack('>II', data[16:24]))
            self.assertEqual(entry['sha256'], hashlib.sha256(data).hexdigest())
            self.assertEqual(data, (WEB / entry['source']).read_bytes())
            self.assertEqual(entry['alt'], img.attrs['alt'])
            self.assertEqual('lazy', img.attrs['loading'])
            self.assertTrue(entry['visual_review_date'])
            self.assertIn('Example exercise data, not an exercise prescription.',
                          figure.find('figcaption')[0].text)


if __name__ == '__main__':
    unittest.main()
