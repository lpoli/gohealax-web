"""The audit is a mandatory gate, with adversarial fixtures proving its failures."""
from pathlib import Path
import shutil
import re
from tempfile import TemporaryDirectory
import unittest

from quality_checks import quality_issues
from site_checks import SITE, WEB


class QualityTests(unittest.TestCase):
    def test_complete_static_audit_passes(self):
        self.assertEqual([], quality_issues())

    def test_quality_regressions_are_reported(self):
        mutations = {
            'About.html': [('https://gohealax.com/About.html', 'https://gohealax.com/about.html', 'canonical must'),
                           ('href="#main"', 'href="#missing"', 'working skip link')],
            '404.html': [('content="noindex"', 'content="index"', 'noindex'),
                         ('href="/site.css"', 'href="site.css"', 'root-relative')],
            'index.html': [('width="800"', 'width="1"', 'dimensions differ'),
                           ('loading="lazy"', 'loading="eager"', 'below-fold'),
                           ('src="assets/hero-800.webp"', 'src="https://example.invalid/hero.webp"', 'third-party'),
                           ('srcset=', 'data-unused=', 'responsive'),
                           ('<title>GoHealaX — Make time for your routine</title>', '<title>About GoHealaX — Your exercise routine</title>', 'titles must be unique')],
            'sitemap.xml': [('https://gohealax.com/About.html', 'https://gohealax.com/404.html', 'four canonicals')],
            'robots.txt': [('Allow: /', 'Disallow: /', 'crawl rules')],
        }
        (WEB / '.artifacts').mkdir(exist_ok=True)
        with TemporaryDirectory(dir=WEB / '.artifacts', prefix='quality-') as directory:
            root = Path(directory) / 'site'
            shutil.copytree(SITE, root)
            for route, changes in mutations.items():
                page = root / route
                original = page.read_text()
                for before, after, expected in changes:
                    with self.subTest(route=route, expected=expected):
                        self.assertIn(before, original)
                        page.write_text(original.replace(before, after))
                        self.assertTrue(any(expected in issue for issue in quality_issues(root)))
                        page.write_text(original)
            for route in ('404.html', 'robots.txt', 'sitemap.xml', 'assets/social.png'):
                page = root / route
                data = page.read_bytes(); page.unlink()
                self.assertTrue(quality_issues(root))
                page.write_bytes(data)


class ContrastTests(unittest.TestCase):
    def test_small_footer_copy_meets_aa_contrast(self):
        css = (SITE / 'site.css').read_text()
        rule = re.search(r'\.landing-footer\s*\{([^}]+)\}', css)[1]
        colors = dict(re.findall(r'(?:^|;)\s*(color|background):\s*(#[0-9a-f]{6})', rule))
        def luminance(value):
            channels = [int(value[i:i+2], 16) / 255 for i in (1, 3, 5)]
            linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in channels]
            return sum(v * weight for v, weight in zip(linear, [.2126, .7152, .0722]))
        low, high = sorted(luminance(colors[key]) for key in ('color', 'background'))
        self.assertGreaterEqual((high + .05) / (low + .05), 4.5)
