# Website handoff

Updated: 2026-10-12. Milestone status and approval authority: [roadmap](roadmap.md).
Working branch at startup: `update-web-requirements`; base revision: `2dbdef1`.

## Current increment

WEB-01 established the documentation and verification baseline and was explicitly approved by the
owner on 2026-10-12. All seven milestone descriptions were created before checker/runner
implementation. The next eligible increment is WEB-02; it has not started.

## Baseline findings (not permanent expected behavior)

| Finding | Resolution gate |
|---|---|
| Homepage redirects to About; lacks landing content, viewport and landmarks | WEB-02 |
| About asserts Google Play availability and an uncertain pilot release | WEB-03 |
| About lacks the exact PROD-01 disclaimer; Privacy has different wording | WEB-04 |
| Privacy asserts GitHub Pages hosting without deployment evidence | WEB-04 wording review; WEB-07 hosting verification |
| No medical disclaimer page or enhanced navigation/media modules | WEB-04 |
| About/Privacy lack canonical URLs; homepage canonical is About; no 404, sitemap, robots, favicon or social assets | WEB-05 |
| No exporter, CNAME or .nojekyll | WEB-06 |

## Verification evidence

Agent-run, Linux, 2026-10-12:

| Command / check | Result |
|---|---|
| `python3 -m unittest discover -s web/tests -p 'test_*.py'` | PASS: 20 tests, offline, standard library only |
| `python3 web/tests/audit.py` | Exit 1: 17 target-quality gaps; assigned above, not a release pass |
| `python3 scripts/check-doc-links.py` | PASS: 90 Markdown files, no broken relative links |
| `python3 ios/tools/ios_handoff/verify_handoff.py --require-images` | PASS: 10 sections, 76 requirements, fixtures/checksums and 110 image metadata records |
| `git diff --check` | PASS |
| `git diff -- web/site` | Empty: all four existing deployable files unchanged |
| Browser baseline at `/tests/browser.html` | Chrome 154.0.8037.92 headless: 12 PASS, 0 FAIL, 0 TIMEOUT, 4 SKIP |

Browser run timestamp: `2026-10-12T11:42:37.334Z`. Two passed checks cover runner infrastructure,
ten cover existing pages: retrievable homepage/link, About/Privacy navigation consistency, content
landmarks/contact/links, loaded styling, visible native navigation and no horizontal overflow at
320, 768 and 1440px. Real-page frames disable scripts. Four skipped groups explicitly cover future
production navigation state/duplicates, Escape/focus/resize, media states/activation and playback
failure. They are not product passes. The runner reports `BASELINE_WITH_SKIPS`.

Reproduce by starting this server from the repository root and visiting the runner in Chrome or Firefox:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory web
```

Exact successful agent browser invocation (directories created under ignored `web/.artifacts/`):

```sh
env TMPDIR=/home/lpoli/workspace/gohealax/web/.artifacts/tmp XDG_CONFIG_HOME=/home/lpoli/workspace/gohealax/web/.artifacts/config XDG_CACHE_HOME=/home/lpoli/workspace/gohealax/web/.artifacts/cache google-chrome --headless --disable-gpu --disable-dev-shm-usage --disable-breakpad --disable-crash-reporter --disable-background-networking --disable-component-update --no-first-run --no-default-browser-check --user-data-dir=/home/lpoli/workspace/gohealax/web/.artifacts/chrome-profile --disk-cache-dir=/home/lpoli/workspace/gohealax/web/.artifacts/cache --crash-dumps-dir=/home/lpoli/workspace/gohealax/web/.artifacts/crashes --virtual-time-budget=15000 --dump-dom http://127.0.0.1:8000/tests/browser.html > web/.artifacts/browser-chrome.html 2> web/.artifacts/browser-chrome.log
```

The sandbox initially denied the server socket and crashed Chrome (exit 133); both succeeded after
tool approval to execute outside the sandbox. Browser profile/cache/temp files and reports were
configured inside this repository. Local reports: `web/.artifacts/browser-chrome.html` and extracted
`web/.artifacts/browser-chrome.json` (ignored). The durable result summary is this handoff.
The preview server logged an incidental `/favicon.ico` 404 from the runner tab; no favicon exists
in this baseline. This is recorded for WEB-05, not treated as a clean network inspection.

**Not run by the agent:** Firefox (153.0 installed), real mobile browser, manual keyboard/screen-reader checks,
text enlargement/desktop zoom/orientation/reduced motion, DevTools Network/console review and
Lighthouse. These remain explicit later milestone gates; headless layout checks do not replace them.
The owner subsequently reported that the review looked good and approved WEB-01; browser versions,
individual test counts and specific manual checks were not supplied. This general approval does not
establish detailed Firefox/mobile/assistive evidence. No live-domain or store-availability verification,
native build or native device test was run. Official WAI/GitHub planning references were reviewed;
that is not verification of our deployment. Local preview server is stopped at session teardown.

## Owner review and next action

Owner approval, 2026-10-12 (user-reported): “looks good to me. I approve WEB-01”. This explicitly
approves the foundation documentation and recorded baseline with its limits. Detailed browser versions
and per-check manual results were not provided; later manual/release gates remain applicable.

The approval is recorded in the roadmap. WEB-02 is the next eligible milestone and remains
Not started until requested. Changes remain uncommitted on the startup branch; `2dbdef1` remains
the last committed base.

## Blockers and owner inputs

- **WEB-01 approval:** resolved by explicit owner approval on 2026-10-12.
- **Launch:** publication rights for branding are unrecorded; public repository identity/access,
  authoritative DNS/control and existing hosting are unverified. No publication or DNS change made.
- **Permitted placeholders:** Play availability, contributor names, social destinations and demo
  video are unverified/unsupplied. Use the [content](content.md) defaults.
- **Reference:** untracked `web/image-ref/web-design-layout.png` existed at startup; preserved and
  excluded from deployment. Layout inspected; no assets extracted or rights inferred.

No native implementation, requirement IDs, iOS pricing decision or app contracts changed. The shared
requirements clarify the informational site's applicability and browser text sizing only.
