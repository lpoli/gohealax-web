# Website handoff

Updated: 2026-10-13. Milestone status and approval authority: [roadmap](roadmap.md).
WEB-02 startup: clean `web-development` branch at `2a360fa`. WEB-01 history below retains its
original evidence. WEB-02 was committed as `6c08b13`. WEB-03 began from that clean revision on
`web-development`; it was committed as `5b1de39`. Approval documentation is uncommitted.
Nothing pushed by the agent.

## Current increment

WEB-01 established the documentation and verification baseline and was explicitly approved by the
owner on 2026-10-12. All seven milestone descriptions were created before checker/runner
implementation. WEB-02 replaces the index redirect with the responsive landing composition. Owner layout/imagery
approval was granted explicitly on 2026-10-12. WEB-03 content and screenshot presentation were explicitly approved on 2026-10-13.
WEB-04 is eligible to start; it has not started. See the evidence below.

## WEB-03 startup and verification

Owner approval, 2026-10-12 (user-reported): “Approve WEB-02 and start WEB-03”. This approves
WEB-02's current layout and imagery and authorizes WEB-03. It does not establish individual manual
browser/assistive results or authorize publication. WEB-02's pending-review wording below describes
its original handoff; the roadmap and this approval record supersede it.

Implemented: complete landing feature explanations and standalone About; phase skipping, pace
units/example, repetition/set/session structure, seconds-based set rest, presets, Today targets,
weekday/one-time schedules while open, History and recorded Statistics/adherence. Removed the old
unverified Google Play availability and pilot-release claims. Free Android and iOS Coming Soon,
contributor placeholders, source editing comments and readable email remain explicit. Landing,
About and Privacy now share HTML navigation destinations, with legal-page brand links returning
home. Privacy disclosures were not edited. No production JavaScript, publishing or DNS changes.

Copy was checked against the shared TMR/DATA/HIST/STAT requirements, ADR-0007 and current Android
`docs/product-spec.md`, `CountPace.kt` and `TimerSessionSequence.kt`. No shared/native behavior changed.

Agent-run, Linux, 2026-10-12:

| Check | Result |
|---|---|
| `python3 -m unittest discover -s web/tests -p 'test_*.py'` | PASS: 26 tests; new content tests first failed against old copy, then passed |
| `python3 web/tests/audit.py` | Exit 1: 8 residual WEB-04/05 findings (same legal/metadata/route scope as WEB-02); screenshot rights/currentness is a separate review blocker |
| `python3 scripts/check-doc-links.py` | PASS: recorded after handoff edits |
| `git diff --check` | PASS: recorded after handoff edits |
| Chrome 154.0.8037.92 headless `/tests/browser.html` | 24 PASS / 0 FAIL / 0 TIMEOUT / 4 explicit WEB-04 SKIP |

Browser timestamp: `2026-10-12T14:39:29.292Z`. Includes added product-copy/availability checks,
three-page navigation consistency, loaded styling and scripts-disabled widths 320/375/768/1024/1440.
Chrome crashed with exit 133 inside the sandbox; tool-approved execution outside it passed. Exact
server command is below; browser invocation:

```sh
env TMPDIR=/home/lpoli/workspace/gohealax/web/.artifacts/tmp XDG_CONFIG_HOME=/home/lpoli/workspace/gohealax/web/.artifacts/config XDG_CACHE_HOME=/home/lpoli/workspace/gohealax/web/.artifacts/cache google-chrome --headless --disable-gpu --disable-dev-shm-usage --disable-breakpad --disable-crash-reporter --disable-background-networking --disable-component-update --no-first-run --no-default-browser-check --user-data-dir=/home/lpoli/workspace/gohealax/web/.artifacts/chrome-web03 --disk-cache-dir=/home/lpoli/workspace/gohealax/web/.artifacts/cache-web03 --crash-dumps-dir=/home/lpoli/workspace/gohealax/web/.artifacts/crashes --virtual-time-budget=30000 --dump-dom http://127.0.0.1:8000/tests/browser.html > web/.artifacts/browser-chrome-web03.html 2> web/.artifacts/browser-chrome-web03.log
```

HTML/JSON reports, logs and profiles stay under ignored `web/.artifacts/`. The runner tab requested
`/favicon.ico` (404, WEB-05); this was not a clean DevTools network review. Preview server stopped at
handoff. No native builds/device tests or shared requirement edits; iOS verification not needed.

## WEB-03 owner revisions and screenshot completion

Owner requested exercise/routine tracking wording and the exact feature sentence “User can totally
focus on exercise rather than mental counting.” Both are now in homepage/About HTML. The removed
pilot-release wording remains absent. The owner's “actual release” correction is recorded in the
content guide; Google Play availability remains unverified and the download placeholder is retained.

The owner supplied five screenshots and confirmed current-commit Android code with exercises/activity
from the generated inspection fixture. Four were selected for the landing gallery: running Hold
phase, Presets, Today's Exercises and Statistics. The second timer image is Ready/Idle and was not
selected. All originals are preserved; deliverable PNGs are byte-identical copies. Capture metadata,
owner-reported revision, repository version, fixture identity/hash and visual inspection are recorded
in [provenance](provenance.md#web-03-screenshot-review-2026-10-12) and the asset register. Android 17
is a tentative owner OS recollection, not an independently verified fact.

Latest agent-run checks, Linux/Chrome 154.0.8037.92, 2026-10-12:

| Check | Result |
|---|---|
| `python3 -m unittest discover -s web/tests -p 'test_*.py'` | PASS: 28 tests, including requested wording, screenshot hashes/original equality, PNG dimensions, alt text/lazy loading and example captions |
| `python3 web/tests/audit.py` | Exit 1: 8 residual WEB-04/05 legal/metadata/route findings |
| `python3 scripts/check-doc-links.py` | PASS: 90 Markdown files |
| `git diff --check` | PASS |
| Browser runner after wording/gallery changes | 24 PASS / 0 FAIL / 0 TIMEOUT / 4 explicit WEB-04 SKIP; timestamp `2026-10-12T15:42:10.902Z` |
| Isolated headless gallery check | PASS at 375×1400 and 1440×1400: all four images decoded, no horizontal overflow; screenshots visually inspected |

Browser runner command matches the earlier WEB-03 invocation, with profile/cache/report suffix
`web03-images`. Reports are `web/.artifacts/browser-chrome-web03-images.html` and `.json`.
Command-line gallery captures twice produced blank PNGs and were rejected as visual evidence.
The final gallery check ran `node web/.artifacts/inspect-gallery.mjs` after user-requested security
review and explicit tool approval. The reviewed script launches its own headless Chrome with a new
profile and random local debugging port; it does not attach to personal Chrome or use personal tabs,
history, cookies or logins. It creates its own tab, disables page scripts, blocks page requests
outside local `/site/`, validates debugging URLs, refuses output overwrites, uses bounded timeouts
and closes its own browser. The browser process is closed; the profile is retained only in ignored
artifacts. This script is temporary QA tooling, not a website dependency or deployable asset.

Final visual artifacts: `web/.artifacts/gallery-check-6N6Jev/gallery-reviewed-mobile.png` and
`gallery-reviewed-desktop.png`, with corresponding JSON reports. Gallery originals, full-resolution
review, layout inspection and example captions are complete. Normal browser tabs were not involved.

**At the implementation handoff:** owner review of final wording, gallery and editable source
locations was pending. The approval below resolves that milestone gate;
WEB-04 has not started. Firefox, real mobile, manual keyboard/assistive, zoom/orientation, DevTools
Network/console and Lighthouse checks remain not run. No native build/device test, publication or DNS
change occurred. Preview server stopped at handoff.

## WEB-03 owner approval

Owner approval, 2026-10-13 (user-reported): “I approve WEB-03.” This explicitly approves the
implemented content and screenshot gallery at `5b1de39`. The roadmap records WEB-03 as Complete;
WEB-04 is now eligible. No WEB-04 implementation or publication was performed in this approval update.

The approval does not establish results for unrun manual/browser checks. The owner separately
requested [Web todos](todos.md) after development: Schedules/History screenshots and a manual review
of all webpage wording. These deferred tasks remain open; existing WEB-04/05/07 gates still apply.

Approval update validation: `python3 scripts/check-doc-links.py` and `git diff --check` passed.
Website source is unchanged, so browser/native tests were not rerun.

## WEB-02 verification and review

Implemented 2026-10-12: landing sections in the required order (including Team/Contact), plain HTML
navigation/anchors, 72rem container, 48rem/64rem breakpoints, scoped landing CSS, original CSS/text
branding and SVG waves, licensed self-hosted responsive hero photo with credit, and honest demo,
contributor and download placeholders. About/Privacy HTML and route case are unchanged. No production
JavaScript, app screenshots, export, publishing or DNS changes. Asset sources, hashes, licence,
derivatives and pending approvals are in [provenance](provenance.md#web-02-selected-assets-2026-10-12).

Agent-run, Linux, 2026-10-12:

| Check | Result |
|---|---|
| `python3 -m unittest discover -s web/tests -p 'test_*.py'` | PASS: 23 tests; includes mandatory landing regression checks |
| `python3 web/tests/audit.py` | Exit 1: 8 remaining findings; no landing findings |
| `python3 scripts/check-doc-links.py` | PASS: 90 Markdown files |
| `git diff --check` | PASS |
| Chrome 154.0.8037.92 headless `/tests/browser.html` | 22 PASS / 0 FAIL / 0 TIMEOUT / 4 explicit WEB-04 SKIP |
| Agent screenshot inspection | Landing at 375×1200 and 1440×1200: readable, photo subject visible, stacked/split composition |

Final runner timestamp: `2026-10-12T13:57:10.586Z`. Checks include HTML/contact/fragment destinations,
stylesheet loading, visible no-JS navigation and no horizontal overflow at 320, 375, 768, 1024 and
1440px on all three real pages. Four deferred interaction groups are not passes. Sandbox denied the
server socket and crashed Chrome; tool-approved execution outside the sandbox succeeded. An old
baseline profile initially used stale CSS and produced three image-overflow failures; fresh profiles
resolved these without source changes. Use a fresh profile/cache for reproducible evidence.

Server command is the same as WEB-01 below. Final browser invocation:

```sh
env TMPDIR=/home/lpoli/workspace/gohealax/web/.artifacts/tmp XDG_CONFIG_HOME=/home/lpoli/workspace/gohealax/web/.artifacts/config XDG_CACHE_HOME=/home/lpoli/workspace/gohealax/web/.artifacts/cache google-chrome --headless --disable-gpu --disable-dev-shm-usage --disable-breakpad --disable-crash-reporter --disable-background-networking --disable-component-update --no-first-run --no-default-browser-check --user-data-dir=/home/lpoli/workspace/gohealax/web/.artifacts/chrome-web02-final --disk-cache-dir=/home/lpoli/workspace/gohealax/web/.artifacts/cache-web02-final --crash-dumps-dir=/home/lpoli/workspace/gohealax/web/.artifacts/crashes --virtual-time-budget=30000 --dump-dom http://127.0.0.1:8000/tests/browser.html > web/.artifacts/browser-chrome-web02.html 2> web/.artifacts/browser-chrome-web02.log
```

Ignored artifacts: HTML/JSON runner report, log, `landing-375.png`, `landing-1440.png`, profiles and
caches under `web/.artifacts/`. Owned preview server stopped at handoff. All task writes stayed in
this repository. No shared requirements changed; iOS verifier/native builds were not needed or run.

The browser requested `/favicon.ico`, which returned 404; favicon work belongs to WEB-05.
This run is not a clean DevTools network/console review.

Remaining audit findings: About/Privacy canonical URLs (WEB-05), exact disclaimers on both pages
and missing medical disclaimer page (WEB-04), 404/sitemap/robots (WEB-05). Content truth, metadata
beyond the current checker, accessibility and release checks still require their planned reviews.

**Owner review required:** layout/reference comparison and photo/new branding acceptance; portrait/
landscape, 200% text and 400% desktop zoom, keyboard/assistive checks, Firefox and real mobile browser.
These manual checks, DevTools Network/console review and Lighthouse are **not run**. Chrome's automated
width tests and screenshot inspection do not establish those results. Missing Play/video/team details
use the permitted placeholders. Photo/new-artwork publication approval remains pending.

## Baseline findings (not permanent expected behavior)

| Finding | Resolution gate |
|---|---|
| Homepage redirect/content/viewport/landmarks | Resolved and enforced in WEB-02 |
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

The approval is recorded in the roadmap. WEB-02 was subsequently implemented and committed as `6c08b13`, then explicitly approved on
2026-10-12 as recorded above. WEB-03 was committed as `5b1de39` and explicitly approved on 2026-10-13.
WEB-04 is the next eligible increment. The seven-milestone gate remains in force.

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
