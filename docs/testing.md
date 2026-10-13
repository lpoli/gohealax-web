# Website verification

Run from the repository root. The Python suite uses only the standard library; it neither contacts
the network nor starts/depends on a browser. Parser assertions use `html.parser` and `urllib.parse`,
not broad HTML regex matching. Test fixtures use repository-local temporary directories.

```sh
python3 -m unittest discover -s web/tests -p 'test_*.py'
python3 web/tests/audit.py
python3 scripts/check-doc-links.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory web
```

Preview `http://127.0.0.1:8000/site/`; browser runner:
`http://127.0.0.1:8000/tests/browser.html`. Use HTTP, not file URLs, for modules and same-origin frames.
After shared requirement edits also run:

```sh
python3 ios/tools/ios_handoff/verify_handoff.py --require-images
```

## Baseline and coverage growth

WEB-01 checks existing local HTML links/fragments, IDs, linked assets, title/language, About/Privacy
landmarks/headings/navigation/contact, and critical Android disclosures. Unit fixtures prove the
checker catches broken links, fragments, duplicates, invalid routes and metadata. The separate
`audit.py` reports target-quality gaps with exit 1. These are findings to fix, not expected failures
to preserve. Never assert a defect must exist and never make it disappear by blanket skipping a page.

Promote resolved audit rules into mandatory tests in the milestone that fixes them. WEB-02 enforces
landing section order, no redirect, visible HTML links, honest availability and local responsive hero
assets; WEB-03 now enforces product explanations, availability, contributor/social editing locations and
three-page navigation consistency. Screenshot asset hashes, equality to owner originals, PNG dimensions, alt text, lazy loading and
example captions are enforced. Owner-reported build/fixture evidence lives in the provenance register; WEB-04 disclaimer and
interaction cases; WEB-05 metadata, image dimensions, sitemap and complete route coverage. By WEB-05
the audit must pass. WEB-06 adds exporter tests (including symlinks, reproducibility and stale files).

## Browser runner

The runner loads real pages in same-origin isolated iframes and uses isolated fixtures to validate
its reporting/timeouts. Every result is PASS, FAIL, TIMEOUT or SKIP with a reason. Its summary states
whether the run is a baseline with deferred coverage; a skipped interaction test never counts as a
pass. Failed requests/imports, thrown assertions and timed-out loads must remain failures. The runner
has a visible static loading message and a watchdog for bootstrap failure.

WEB-02 real-page checks include landing/About/Privacy navigation/contact, rendered width at
320, 375, 768, 1024 and 1440px, stylesheet application and HTTP loading, with scripts disabled.
The homepage redirect is now forbidden in both the offline gate and browser runner. WEB-04 must
import the production `site.js`/`media.js` functions into fixtures, with controlled
player adapters. Cover menu state, Escape/focus, link activation, duplicate initialization, resize,
invalid/disabled/media activation and playback failures. Add modules and their tests together; do
not create a test-only imitation of the production controller. The baseline runner self-check is
infrastructure coverage, not proof of future product behavior.

Tests never contact YouTube. Separately use browser DevTools Network: disable cache, clear requests,
reload each real page, and verify all initial requests are same-origin (including fonts, poster and
connection hints). Save the result even when playback is disabled. Controlled-adapter tests alone
cannot establish the production network boundary.

## Manual gates

Record browser/version, OS/device, viewport, date, checker, command/URL and outcome for:

- Chrome and Firefox plus an owner-run real mobile browser; portrait and landscape.
- Widths 320, 375, 768, 1024, 1440px; 200% text enlargement and 400% desktop zoom.
- Keyboard traversal/activation/Escape/focus and screen-reader smoke check; contrast and focus.
- Disabled/failed JavaScript, reduced motion, failed media, no console errors or missing requests.
- Mobile/desktop Lighthouse in WEB-05, with report/version and material findings resolved. A score
  does not replace manual accessibility checks.
- Export origin-root and nested-path 404 behavior in WEB-06, repeated on the live site in WEB-07.

Use DevTools → Lighthouse → Navigation → Mobile, then Desktop; save reports inside
`web/.artifacts/`. Browser screenshots, temporary profiles and reports stay there as well. Do not
run native builds/device tests for Web-only changes. Any owner-reported evidence is explicitly
labelled **user-run**, and unrun work is **not run**, never inferred from source inspection.
