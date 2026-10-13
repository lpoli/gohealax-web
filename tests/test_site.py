"""Current working guarantees. Defects belong in the audit, never in expected failures."""

import unittest

from site_checks import CONTACT, SITE, read_document, reference_issues, structure_issues


class ExistingSiteTests(unittest.TestCase):
    def test_compatible_routes_exist(self):
        for route in ("index.html", "About.html", "privacy-policy.html"):
            with self.subTest(route=route):
                self.assertTrue((SITE / route).is_file())

    def test_all_html_references_resolve(self):
        for page in SITE.rglob("*.html"):
            with self.subTest(page=page.name):
                self.assertEqual([], reference_issues(SITE, page, read_document(page)))

    def test_all_pages_have_basic_structure_and_unique_ids(self):
        for page in SITE.rglob("*.html"):
            with self.subTest(page=page.name):
                self.assertEqual([], structure_issues(read_document(page), landmarks=False))

    def test_content_pages_have_landmarks_and_heading_hierarchy(self):
        for route in ("About.html", "privacy-policy.html"):
            with self.subTest(route=route):
                self.assertEqual([], structure_issues(read_document(SITE / route)))

    def test_navigation_destinations_are_consistent(self):
        destinations = []
        for route in ("index.html", "About.html", "privacy-policy.html"):
            nav = read_document(SITE / route).find("nav")[0]
            destinations.append({n.attrs.get("href") for n in nav.find("a")})
        self.assertTrue(all(links == destinations[0] for links in destinations))
        self.assertTrue({"About.html", "privacy-policy.html"} <= destinations[0])

    def test_contact_is_available_in_html(self):
        for route in ("About.html", "privacy-policy.html"):
            with self.subTest(route=route):
                links = read_document(SITE / route).find("a")
                self.assertTrue(any(n.attrs.get("href") == CONTACT and
                                    n.text == "b.lp.self@gmail.com" for n in links))

    def test_android_privacy_disclosures_remain_present(self):
        text = read_document(SITE / "privacy-policy.html").root.text
        # These are existing factual guarantees, not assertions about uncertain website hosting.
        for disclosure in ("private on-device storage", "no user accounts, analytics",
                           "document picker", "foreground notification", "lock-screen settings",
                           "uninstall", "disables automatic Android cloud backup",
                           "device-to-device transfer", "readable, unencrypted",
                           "survive uninstall", "only after confirmation",
                           "Backups exclude permissions, active timers, loaded setup and unsaved drafts"):
            with self.subTest(disclosure=disclosure):
                self.assertIn(disclosure, text)


if __name__ == "__main__":
    unittest.main()
