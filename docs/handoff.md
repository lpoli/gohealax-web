# Website handoff

Updated: 2026-10-13. Milestone status and approval authority: [roadmap](roadmap.md).
WEB-02 startup: clean `web-development` branch at `2a360fa`. WEB-01 history below retains its
original evidence. WEB-02 was committed as `6c08b13`. WEB-03 began from that clean revision on
`web-development`; it was committed as `5b1de39`. Approval documentation was committed as `559a0e0`.
Nothing pushed by the agent.

## Current increment

WEB-01 established the documentation and verification baseline and was explicitly approved by the
owner on 2026-10-12. All seven milestone descriptions were created before checker/runner
implementation. WEB-02 replaces the index redirect with the responsive landing composition. Owner layout/imagery
approval was granted explicitly on 2026-10-12. WEB-03 content and screenshot presentation were explicitly approved on 2026-10-13.
WEB-04 implementation evidence and explicit owner approval are recorded below. WEB-05 quality
implementation and pending manual evidence are recorded in [WEB-05 review](#web-05-quality-and-review).

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
WEB-04 was subsequently implemented as recorded below. The seven-milestone gate remains in force.

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

## WEB-04 implementation and verification

Startup: clean `web-development` at `559a0e0` (WEB-03 approval), 2026-10-13. Owner request:
“Start milestone WEB-04.” Implementation/handoff changes are uncommitted. Nothing pushed.

Implemented:

- `site/site.js`: idempotent progressive mobile disclosure on all four pages, native links and
  button, ARIA state/control association, Escape with focus return, unprevented link activation,
  and focus movement before resize hides a control. Native navigation stays visible with failed
  or disabled JavaScript. Reviewed the linked WAI guidance again; no example code copied.
- `site/media.js`: attribute-driven reviewed configuration validation, same-origin local-file
  existence probes, explicit activation, native video/English caption and privacy-enhanced YouTube
  adapters. Error/timeout cleanup, explicit Retry, direct-media/watch links, retained description
  and stale-callback protection. An iframe load reports loading only, not verified playback.
- Disabled demo retains a local poster reused from the approved WEB-03 screenshot register, with
  synthetic-data caption and readable description. No video is supplied/reviewed or enabled; no
  media probe or player request occurs for this disabled configuration.
- New exact-case `medical-disclaimer.html`; exact canonical PROD-01 paragraph on About, Privacy
  and Medical Disclaimer. Android privacy disclosures retained and checked against the Android
  policy. Separate website hosting, optional-media and email disclosures replace the unverified
  GitHub Pages assertion. Actual hosting/operator verification remains a WEB-07 input.
- Browser tests now exercise actual production modules and real mobile page markup. Deferred
  interaction groups are removed. Controlled adapters isolate playback; the native YouTube DOM
  check uses a detached iframe and makes no YouTube request. Native caption/video DOM and error
  handling are checked with playback suppressed.

Agent-run, Linux, 2026-10-13:

| Check | Result |
|---|---|
| `python3 -m unittest discover -s web/tests -p 'test_*.py'` | PASS: 33 tests. Four WEB-04 tests first failed against the existing pages; the final suite also checks local initial HTML resources |
| `python3 web/tests/audit.py` | Exit 1: six WEB-05 findings only: About/Privacy/Medical canonical URLs; 404, sitemap and robots |
| `python3 scripts/check-doc-links.py` | PASS: 91 Markdown files |
| `git diff --check` | PASS |
| Chrome 154.0.8037.92 headless `/tests/browser.html` | PASS: 41 PASS / 0 FAIL / 0 TIMEOUT / 0 SKIP |

Final browser report timestamp: `2026-10-13T02:59:10.900Z`.

Browser coverage: scripts-disabled styling/width checks at 320/375/768/1024/1440 on all four pages,
HTML navigation/link/contact checks, real mobile enhancement on all four pages, idempotent controllers,
Escape/focus/resize, invalid/review/caption/source checks, duplicate activation, blocked/error/timeout
fallbacks, stale callbacks, explicit retry, native player attributes and caption errors. Adapter
checks do not establish live playback, assistive usability or a clean production network trace.

Preview command: `python3 -m http.server 8000 --bind 127.0.0.1 --directory web`.
Exact browser command:

```sh
env TMPDIR=/home/lpoli/workspace/gohealax/web/.artifacts/tmp XDG_CONFIG_HOME=/home/lpoli/workspace/gohealax/web/.artifacts/config XDG_CACHE_HOME=/home/lpoli/workspace/gohealax/web/.artifacts/cache google-chrome --headless --disable-gpu --disable-dev-shm-usage --disable-breakpad --disable-crash-reporter --disable-background-networking --disable-component-update --no-first-run --no-default-browser-check --user-data-dir=/home/lpoli/workspace/gohealax/web/.artifacts/chrome-web04 --disk-cache-dir=/home/lpoli/workspace/gohealax/web/.artifacts/cache-web04 --crash-dumps-dir=/home/lpoli/workspace/gohealax/web/.artifacts/crashes --virtual-time-budget=30000 --dump-dom http://127.0.0.1:8000/tests/browser.html > web/.artifacts/browser-chrome-web04.html 2> web/.artifacts/browser-chrome-web04.log
```

Chrome exited 133 under the sandbox; explicitly tool-approved execution outside it succeeded.
Profile/cache/temp/log/HTML and extracted JSON report remain inside ignored `web/.artifacts/`.
The runner's incidental favicon request is still a 404 (WEB-05). Preview server stopped at handoff.
No native build/device tests or shared requirement edits; iOS verifier was not required or run.
All writes stayed inside the working directory. Owner reference files are untouched.

**Owner inspection required by `web/AGENTS.md`:** “Stop for owner inspection after each milestone.”
Review navigation, keyboard/failure behavior and the legal pages before explicitly approving WEB-04;
WEB-05 remains gated. Firefox, real mobile portrait/landscape, manual Tab/Shift+Tab/Enter/Space/Escape,
screen-reader smoke, zoom/text enlargement, disabled/failed module loading in a real tab, real
blocked/missing media/captions and a DevTools Network/console review are **not run**. Scripts-disabled
frames establish the HTML fallback; controlled fixtures establish interaction behavior, neither
substitutes for those manual checks. Missing reviewed media is the permitted disabled-demo default,
not a blocker for local site implementation. No hosting, store, DNS or publication claim is inferred.

## WEB-04 owner report and runner cache correction

User-run Chrome 154 on Linux, `http://127.0.0.1:8000/tests/browser.html`, timestamp
`2026-10-13T03:11:05.814Z`: **37 PASS / 4 FAIL / 0 TIMEOUT / 0 SKIP**. Three failures showed homepage
images at intrinsic width at 320/375/768; the fourth found no About disclosure button. These results
are preserved as failed owner evidence, not replaced by the earlier agent pass.

Inspection identified a runner cache weakness: its separate assertions fetched pages with no-store,
but its real-page iframes loaded ordinary cached URLs, including CSS. The report is consistent with
older cached landing CSS and About HTML; the owner's cache contents were not inspected directly.

Changed only test infrastructure and documentation: real-frame HTML now comes from the no-store
fetch itself, with an original-route base and fresh same-origin stylesheet URLs. Page scripts remain
disabled. A regression checks repeated CSS URL freshness, current HTML, correct relative images and
HTTP 404 failure. Website code is unchanged by this correction.

Agent-run, Linux/Chrome 154.0.8037.92, `2026-10-13T03:20:47.363Z`: **42 PASS / 0 FAIL / 0 TIMEOUT /
0 SKIP**. Reused the isolated WEB-04 profile/cache. Command matches the WEB-04 invocation above,
with preview port `8001` and report suffix `web04-cachefix`. The separate preview used
`python3 -m http.server 8001 --bind 127.0.0.1 --directory web`; the sandbox denied its socket, then
explicitly tool-approved execution succeeded. That agent-owned server was stopped without touching
the owner's port-8000 preview. Reports remain in `web/.artifacts/`. Offline suite: 33 PASS;
documentation links and `git diff --check`: PASS. No source/native change or new publication action.

Owner action: hard-refresh the browser runner once (Ctrl+Shift+R) to load its updated modules and
rerun; expect 42 checks. The subsequent owner rerun and approval below resolve this request. Other unrun manual checks
remain recorded separately.

## WEB-04 owner approval

Owner report and approval, 2026-10-13 (user-run): “Yes all the tests passes. The firefox browser also
displays the pages properly even with variable sizes. I approve these changes.”

This explicitly approves the WEB-04 implementation, including the runner cache correction. The owner
confirms all automated browser checks pass after the correction (the current runner has 42 cases;
no replacement JSON or separate counts were supplied). The owner also reports that Firefox renders
the pages correctly at variable sizes. Firefox version, exact widths and per-page results were not
supplied, so this is recorded as a general user-run layout check.

WEB-04 is Complete in the roadmap; WEB-05 is the next eligible increment and has not started.
Approval does not establish individual keyboard, screen-reader, real mobile, zoom/orientation,
DevTools Network/console or actual enabled-media checks. Their remaining limitations carry forward
into the later accessibility/release gates. The demo stays disabled; nothing was published or pushed.
Implementation and approval documentation remain uncommitted.

Approval-update validation: `python3 scripts/check-doc-links.py` and `git diff --check` passed.
Website/test implementation is unchanged in this approval update; browser/native tests were not rerun.

## Preview follow-up and browser isolation requirement

Owner report/request, 2026-10-13: the HTTP preview has an incorrect view while directly opening
`index.html` in Chrome/Firefox renders properly; future headless Chrome must always use a Guest
profile and respect sandboxing; provide a mobile inspection method.

Added `web/tools/preview.py`: source directory is independent of the working directory, responses
are uncached and conditional validators are ignored. Default loopback preview uses port 8765 and
preserves `/site/` and `/tests/` URLs. Explicit `--lan` mode serves only deployable website files at
`/` for a real phone on the same Wi-Fi. Phone steps and desktop responsive-mode instructions are in
[testing](testing.md#reliable-local-preview-and-phone-inspection). No LAN server was started by the
agent. The owner must run it for phone inspection.

Recorded the owner's Guest requirement in `web/AGENTS.md` and the testing guide: future automated
Chrome uses `--guest`, a unique fresh repository-local profile per launch, and Chromium's sandbox
stays enabled. Previous runs used separate automation profiles, not the owner's normal profile;
some reused those separate profiles and lacked Guest mode. Historical commands remain evidence,
not approved future launch templates. No browser was launched during this follow-up.

The reported HTTP rendering difference is unresolved pending the precise command/URL and testing
with the new uncached preview. The cache/path explanation is a hypothesis, not verified owner-host
state. This tooling follow-up does not change the approved website source or start WEB-05.

Agent-run validation: 35 offline tests PASS, including actual handler response bytes/headers and
current CSS MIME type with conditional requests, plus LAN-root exclusion of docs/tests/traversal.
Tests use in-memory HTTP connections without opening sockets. `python3 web/tools/preview.py --help`,
documentation links and `git diff --check` PASS. Live server/browser/phone rendering has not been
verified in this update. Changes are uncommitted; WEB-04 commit is `8f1b3be`.


## WEB-05 quality and review

Started on owner instruction “Start milestone WEB-05”, from clean `web-development` revision
`51d7b04` (preview follow-up); WEB-04 predecessor approval is recorded above. Changes are uncommitted.
No native changes, export, publication, DNS changes or push. Owner references and existing hero/
screenshot bytes are untouched.

Implemented:

- Absolute canonical URLs on all four indexable pages; unique titles/descriptions, page-specific
  Open Graph metadata and shared local social card. Original SVG/PNG favicons and touch icon;
  candidate provenance, dimensions and SHA-256 are in [provenance](provenance.md#web-05-original-quality-assets-2026-10-13).
- Sitemap containing exactly the four canonicals, crawl rules and absolute sitemap location.
  Helpful noindex 404, no canonical, with root-relative navigation and assets. The loopback
  origin-root preview returns these exact bytes and HTTP 404 for unknown nested URLs.
- Skip links on legal pages and 404, explicit visible focus styling, text wrapping without a fixed
  body minimum width, 44px navigation targets, reduced-motion and forced-colors focus support.
  Numeric inspection found the small footer copy at 4.03:1 against mint; changed it to dark green,
  now above 4.5:1, with a regression. Other sampled text/surface pairs were 4.95:1 or higher.
- Mandatory complete static audit (`quality_checks.py`) shared by `audit.py` and the regression
  suite. Adversarial fixtures check metadata, missing files, images, external resources, 404,
  sitemap and robots failures. Existing hero responsive sources/eager priority and screenshot
  explicit dimensions/lazy loading are preserved. No production dependencies or build step.
- Browser suite grows from 42 to 47 cases: skip-link focusability, actual image decoding and
  reflow at 320px with 200% root text on all four real pages; social image, sitemap and 404 HTML.
  HTTP fallback-handler tests check custom 404 bytes/status plus root asset/navigation availability.

Agent-run, Linux, 2026-10-13:

| Exact command / check | Outcome |
|---|---|
| `python3 -m unittest discover -s web/tests -p 'test_*.py'` | PASS: 39 tests |
| `python3 web/tests/audit.py` | PASS: 0 findings, exit 0 |
| `python3 scripts/check-doc-links.py` | PASS |
| `git diff --check` | PASS |
| `python3 web/tools/preview.py --port 8765` | Uncached loopback test/site preview |
| `python3 web/tools/preview.py --root --port 8766` | Origin-root source and actual nested custom 404 |
| `node web/.artifacts/web05-check.mjs` | Chrome 154.0.8037.92 Guest; final browser evidence below |

The execution sandbox refused preview sockets and crashed Chrome; each necessary rerun received
explicit tool escalation approval. Chromium's own sandbox remained enabled throughout. Every
browser launch used Guest and a fresh repository-local profile; no personal browser was attached.
Long temporary paths exceeded Chrome's Unix socket limit. Short fresh run directories resolved this.
Guest `--dump-dom` produced no report and `/json/new` returned HTTP 500; the local verification
script instead connects to the debugging port recorded by the browser it just started and uses
that instance's existing blank Guest tab. All run profiles/reports remain under `web/.artifacts/`.

Intermediate runs are preserved: 43 PASS / 4 FAIL from inactive headless focus pseudo-classes;
46 PASS / 1 FAIL from responsive image selection racing text enlargement. The runner now verifies
DOM focusability, and waits two rendering frames after changing text size before decoding images.
The origin-root inspection separately checks actual focused skip-link visibility with headless
focus emulation enabled. A later runner passed 47 checks, but its extra root focus inspection
failed before focus emulation; it is not counted as a passing full inspection.

**Outstanding at implementation handoff (subsequently resolved by owner review below):** Mobile and Desktop Lighthouse (CLI is not installed;
use Chrome DevTools Navigation and save both reports/version under `web/.artifacts/`), real-mobile
portrait/landscape, screen-reader smoke, manual Tab/Shift+Tab/Enter/Space/Escape and skip-target
behavior, text-only enlargement/400% desktop zoom, reduced-motion/forced-colors inspection, Firefox
rerun for this increment, and manual DevTools console/network inspection. The earlier owner Firefox
WEB-04 report does not verify changed WEB-05 pages. The automated 200% root-font check is not
claimed as a real browser text-only setting or manual zoom result. Material Lighthouse findings
must be resolved and remaining manual acceptance established before approval.

Owner review: run the default preview for `/site/` and `/tests/browser.html`, and the `--root`
preview for `/unknown/nested/page`. Review local artwork and the quality/accessibility evidence.
[Web instructions](../AGENTS.md) require “Stop for owner inspection after each milestone.” WEB-05
was Awaiting approval at this implementation handoff; the subsequent owner review is recorded below.


Final Guest browser result: **47 PASS / 0 FAIL / 0 TIMEOUT / 0 SKIP**, Chrome
154.0.8037.92 on Linux, `2026-10-13T06:37:09.145Z`, at
`http://127.0.0.1:8765/tests/browser.html`. Evidence: `web/.artifacts/qYyzSLa/browser.json`.
The same isolated browser then inspected all four indexable origin-root routes plus
`/unknown/nested/page`: CSS loaded, focused skip links unclipped, no horizontal overflow, no
network loading failures, and all observed page requests stayed on `http://127.0.0.1:8766/`.
Route JSON and `network.json` are in the same run directory. The custom HTTP 404 status and exact
body are verified by the offline handler test; root browser inspection establishes rendering and
asset resolution. Social image was also visually inspected locally; no clipping of the card text.
Both agent-owned preview servers were stopped after verification. Final documentation links and
whitespace validation pass. Lighthouse and manual limitations were pending at this run.

## WEB-05 owner review and approval

On 2026-10-13 the owner reported: “All is good. The lighthouse report is updated in the
web/.artifacts directory.” This accepts WEB-05 after the supplied manual verification checklist:
keyboard/skip-link navigation, narrow layouts and text/desktop zoom, Firefox and a real phone in
both orientations, reduced motion and screen-reader smoke, and the nested custom 404. These are
**user-run** results, not agent-run checks. Exact manual browser versions, phone model,
screen-reader name and individual viewport measurements were not supplied. Earlier agent-run
console/network and fallback evidence remains recorded above; current local preview inspection
is accepted, while the cause of the earlier HTTP/file discrepancy remains unknown.

The agent parsed the updated reports locally without loading the entire JSON into conversation.
Both test `http://127.0.0.1:8766/` with Lighthouse **13.4.1**, Chrome **154.0.0.0** host user-agent
on Linux. Neither has a runtime error, run warning or observed extension resource; the earlier
extension-related unused-JavaScript finding has disappeared. Lighthouse Mobile is simulation,
separate from the owner's real-phone inspection.

| User-run report | UTC fetch time | Performance / Accessibility / Best practices / SEO | FCP | LCP | TBT | CLS |
|---|---|---|---|---|---|---|
| `web/.artifacts/lighthouse-mobile.json` | 2026-10-13T07:31:32.031Z | 100 / 100 / 100 / 100 | 1.0 s | 1.4 s | 0 ms | 0 |
| `web/.artifacts/lighthouse-desktop.json` | 2026-10-13T07:32:22.783Z | 100 / 100 / 100 / 100 | 0.3 s | 0.4 s | 0 ms | 0 |

Report SHA-256, to identify the reviewed local files (artifacts remain ignored):

- Mobile: `23858894eac5f2fc926751cfb7fb0f9ef71668fba26958225c87c3959b1f66ea`.
- Desktop: `762116d697c89eb8f51058f193dc896de7e67bb52df570e94a7fbb1ba08e4ebc`.

Remaining diagnostics were reviewed as nonblocking for this local quality gate:

- Back/forward cache exclusions name the preview's intentional `Cache-Control: no-store`;
  compression is absent from this standard-library preview. These are local-server observations;
  assess actual hosting headers again at launch, rather than claiming production verification.
- Image delivery estimates 80 KiB savings on Mobile and 188 KiB on Desktop. These concern existing
  responsive hero selection and below-fold lazy screenshots. With 1.4 s Mobile LCP, zero blocking
  time and zero layout shift, these are optimization opportunities rather than observed loading
  failures. Retain the approved original screenshot bytes and responsive hero in this milestone.
- The short same-origin CSS/module dependency chain and stylesheet render-blocking diagnostic
  show no material load regression in these reports. No third-party preconnect is needed.

WEB-05 is owner-approved and Complete in the [roadmap](roadmap.md). WEB-06 is next but has not been
started. Changes remain uncommitted; nothing was exported, published or pushed.

Agent-run approval handoff validation, 2026-10-13: `python3 -m unittest discover -s web/tests
-p 'test_*.py'` PASS (39 tests); `python3 web/tests/audit.py` PASS (0 findings);
`python3 scripts/check-doc-links.py` PASS (91 Markdown files); `git diff --check` PASS.
Browser automation was not repeated for these documentation-only approval updates.


## WEB-06 release preparation

Started 2026-10-13 at the owner's request, on clean `web-development` revision
`af4d09aa59d41a5d6ea7b6b0f5eb25ec975d782a` (committed WEB-05). Implementation changes are uncommitted;
that is the base revision, not an approved launch revision. No publication, push, repository mutation
or DNS change occurred. WEB-06 status is owned by [roadmap](roadmap.md).

Implemented the standard-library exporter, literal 23-file allowlist, exact `CNAME` and empty
`.nojekyll`, validation-only `--check`, staged byte-preserving replacement, sorted deterministic
path/size/SHA-256 manifest outside the public directory, and validated repository-local saved-package
restore. Exclusions and symlink/reference safety, failed copy/replacement, changed staged bytes,
stale removal and previous-package rollback are regression tested. No deployable content, photo,
screenshot or artwork bytes changed beyond the two hosting markers. `preview.py --exported` serves
the actual package at origin root with the actual custom nested 404. The deployment guide owns the
precise allowlist, replacement/crash limits and owner publication/rollback procedure.

Candidate manifest SHA-256:
`16535334fcc817f08c5067e9df3aeb41b873cdaa784a498321089d248d0c87c4`.
Output: `web/.release/site/` and `web/.release/manifest.json`.
Retained byte-identical candidate: `web/.artifacts/releases/` followed by the full hash above.
Snapshots/reports remain ignored. The manifest contains no time, machine path, Git state or credentials.
Owner review must identify this exact hash; an eventual committed monorepo revision must also be
recorded before launch. This candidate is locally verified, not launch-ready or publication-approved.

Agent-run verification on Linux, 2026-10-13:

| Command / check | Result |
|---|---|
| `python3 -m unittest discover -s web/tests -p 'test_*.py'` | PASS: 49 tests |
| `python3 web/tests/audit.py` | PASS: zero findings |
| `python3 scripts/check-doc-links.py` | PASS: 91 Markdown files |
| `python3 web/scripts/prepare-release.py --check` | PASS: 23 files; validation only |
| `python3 web/scripts/prepare-release.py` | PASS; candidate hash above |
| `sha256sum web/.release/manifest.json` | Hash above |
| `python3 web/scripts/prepare-release.py --restore web/.artifacts/releases/16535334fcc817f08c5067e9df3aeb41b873cdaa784a498321089d248d0c87c4 --check` | PASS |
| Same restore command without `--check` | PASS; original candidate/hash retained |
| `python3 web/tools/preview.py --port 8000` | Source/browser preview |
| `python3 web/tools/preview.py --exported --port 8001` | Export root and nested custom fallback |
| `node web/.artifacts/web06-check.mjs` | Chrome 154.0.8037.92 Guest: 47 PASS / 0 FAIL / 0 TIMEOUT / 0 SKIP |
| Export root browser inspection | All four indexable pages, `/404.html`, and `/unknown/nested/page`: CSS loaded, focused skip links visible, no overflow or failed network loads; same-origin page requests only |
| `git diff --check` | PASS |

Browser evidence: `web/.artifacts/qQ1HbAz/browser.json`, route JSON and `network.json`.
The shared browser suite exercised source pages; exporter tests prove the exported files match those
bytes. The same fresh Guest browser separately inspected all exported root routes and the fallback.
Offline HTTP-handler tests assert HTTP 404 and exact fallback body, plus HTTP 200 for exported pages
and assets. Regression tests install a previous saved package after a changed candidate and verify
all prior bytes/manifest return. No real phone or assistive-tool rerun was performed in WEB-06;
website page bytes are unchanged from owner-approved WEB-05.

The execution sandbox rejected preview sockets and the initial Chrome startup timed out. Necessary
reruns received explicit tool escalation approval. Chrome retained its own sandbox, used Guest and a
fresh repository-local profile; no personal browser was attached. Reports/profiles remain in the
workspace. Both agent-owned preview servers were stopped after verification.

### Launch prerequisites and owner review

- Owner identified the dedicated public repository as **`lpoli/gohealax`** in this session. A read-only
  web fetch of its GitHub URL failed with cache miss; visibility, existence, access, existing history,
  `main` and Pages settings were not independently established. Confirm it is separate from the
  private monorepo before following the concrete owner commands in deployment.
- Authoritative existing hosting, DNS records/provider and domain-control authority are still unknown.
  No live DNS snapshot or HTTPS/redirect result is claimed. Obtain apex/`www`/NS/MX/TXT records and
  a routing rollback plan under owner authority before launch.
- Hero licence, screenshot synthetic-data review and original-artwork authorship remain documented in
  [provenance](provenance.md). Local milestone approvals are recorded; explicit public-use confirmation
  for selected screenshots/original artwork was requested but has not been supplied. Native branding
  and completion fanfare are absent from this package; their native-release blockers do not add
  assets to the website. Do not call this package launch-ready until selected-asset rights are resolved.
- Google Play availability remains unverified. The exported download state is still truthful,
  disabled pending availability. Contact remains `b.lp.self@gmail.com`; owner should verify it is
  suitable before publishing. No invented store URL was added.
- Current official GitHub branch/root and custom-domain guidance was rechecked read-only on
  2026-10-13; exact links, current planned routing and future commands are in deployment.

Inspect the manifest, all exported routes, licence/contact/download state and exclusions. Approve
or reject this exact candidate, and resolve the launch prerequisites above. Package approval does
not grant publication/DNS authority or start WEB-07 automatically.
[Web instructions](../AGENTS.md) require “Stop for owner inspection after each milestone.”
WEB-06 is therefore Awaiting approval after local implementation and available verification;
missing authority/rights remain explicit blockers to launch.


### WEB-06 owner-requested persistent navigation

On 2026-10-13 the owner requested navigation that stays visible while scrolling and looks consistent
between pages, allowing a 404 exception. The shared four-page header now uses identical branding,
link labels/order/destinations and button styling; current-page links use `aria-current="page"`.
It is sticky with an opaque background, with a persistent disclosure button on mobile. Header height
is limited to half the viewport, with internal scrolling for long menus/enlarged text. Root scroll
padding tracks actual header height after enhancement, with a CSS-only fallback, so section/skip
navigation clears the header. The 404 retains its simpler header; legal content keeps its narrow
reading column. No copy, asset or availability changes were made.

The original WEB-06 package/hash above is now historical and retained for rollback. **Current review
candidate:** `c7bd4c36ef8d471520206f74d2b8a2c868fd79eaa551c0582aa479c2cf6df562`.
It is exported at `web/.release/` and retained under `web/.artifacts/releases/` with that hash as its
directory name. Publication commands in deployment now select this candidate. Launch prerequisites
and owner approval remain pending; changes remain uncommitted on the same base revision.

Agent-run final verification: 49 offline tests PASS; audit zero findings; documentation links PASS;
`prepare-release.py --check` PASS; export has 23 files and the current manifest hash above;
`git diff --check` PASS. Chrome 154.0.8037.92, Linux, fresh Guest profile with sandbox enabled:
**55 PASS / 0 FAIL / 0 TIMEOUT / 0 SKIP**, including sticky position after scrolling, usable mobile
menus and unobscured section targets at 375px and 1440px on every indexable page. The shared
navigation check now compares ordered label/destination pairs across all four pages.
The export root and nested 404 inspection also passed. Latest browser evidence is recorded below.
Real-phone, assistive-tool and Lighthouse checks were not repeated for this requested UI revision.

Review with `python3 web/tools/preview.py --exported --port 8001`; inspect scrolling on each content
page and cross-page section links. The deployment gate still requires review of this exact refreshed
package. Both verification previews were stopped after the final checks.

Final revised-navigation browser evidence: `web/.artifacts/qi9EptJ/browser.json`, route JSON,
`network.json` and `cross-page-anchor.json`. In the exported browser, clicking Features from About
navigated to `index.html#features` with the target below the sticky header. All observed exported
page requests stayed same-origin and had no network loading failures.


### WEB-06 owner-selected project logo

On 2026-10-13 the owner verified the Android/master icon and instructed use of
`design/branding/icon-master.png` before the leading GoHealaX text, identifying it as the project
logo. The four content-page headers now display `assets/project-logo.png`, an unchanged copy of
that master, at 2.75rem square. Empty alt text avoids repeating the adjacent accessible brand name;
explicit intrinsic dimensions and eager loading reserve its layout space. The 404 exception retains
its simpler header. Asset provenance and the precise owner authorization are in
[provenance](provenance.md#web-06-owner-selected-project-logo-2026-10-13).

**Current candidate superseding both prior WEB-06 packages:**
`9a2b92b3757712d130d1f2205c41bce36fa6a7c0e296628b253dc3730fd21aef`.
The exporter now allows 24 files, including `assets/project-logo.png`. The package is exported at
`web/.release/`, retained under the full hash in `web/.artifacts/releases/`, and selected by the
future publication commands. Prior packages remain available for rollback. This is still awaiting
owner review, with no publication/push/DNS changes and no new committed revision.

Agent-run checks: 49 offline tests PASS; audit zero findings; exporter validation PASS; manifest hash
matches the current candidate; documentation links and whitespace PASS. Browser evidence is below.
Mobile/assistive-tool/Lighthouse checks were not repeated for this logo change. Website logo bytes
match the master's SHA-256 `be700fb51c492f59611666b738dcd8a66213da8360de669e2c4a3056414bb8aa`.
Both agent-owned previews were stopped after verification. The current package can be inspected with
`python3 web/tools/preview.py --exported --port 8001`.

Final logo browser evidence: `web/.artifacts/qk22yOm/browser.json`, route JSON, `network.json`
and `cross-page-anchor.json`: Chrome 154.0.8037.92 on Linux, fresh Guest with sandbox enabled,
55 PASS / 0 FAIL / 0 TIMEOUT / 0 SKIP. Header logo images decoded in real-page/200% text checks;
export root pages, nested 404 and the cross-page Features anchor inspection also passed.
Saved-package restore accepts the retained pre-logo 23-file packages as well as the new 24-file
package, checking the saved manifest and references; normal source export requires the logo.


## WEB-06 owner approval

On 2026-10-13 the owner reported: “All looks good. I approve WEB-06.” This explicitly approves
the final local package with the persistent consistent navigation and owner-selected project logo.
Approved manifest SHA-256:
`9a2b92b3757712d130d1f2205c41bce36fa6a7c0e296628b253dc3730fd21aef`.
The 24-file package at `web/.release/` matches the retained snapshot in
`web/.artifacts/releases/9a2b92b3757712d130d1f2205c41bce36fa6a7c0e296628b253dc3730fd21aef/`.
This is user-reported visual acceptance; exact browser/device details were not supplied. The
agent-run evidence remains 49 passing offline tests, zero audit findings and 55 passing isolated
Guest Chrome checks, recorded above. No browser checks were repeated for this documentation-only
approval update.

WEB-06 is Complete in the Web roadmap. WEB-07 is next and has not started. Package approval does
not grant publication or DNS authority. Repository access/visibility, authoritative existing
hosting/DNS and publication-rights evidence remain launch prerequisites recorded above. No push,
publication or DNS changes occurred. WEB-06 implementation is still uncommitted, based on
`af4d09aa59d41a5d6ea7b6b0f5eb25ec975d782a`; record the eventual commit as the approved source
revision before publication. The owner requested a commit message, not creation of a commit.

Approval handoff validation: `python3 web/scripts/prepare-release.py --check` PASS (24 files,
approved hash); `python3 scripts/check-doc-links.py` PASS (91 Markdown files);
`git diff --check` PASS. Approval documentation does not change package bytes.

## WEB-07 launch preflight

Started at the owner's request on 2026-10-13. This section supersedes WEB-06's historical
“uncommitted/unverified hosting” notes: approved source revision is now
`5ba3f2b79b59f62b4dbd0f9f0318f746a59ff0e4`. No publication, push or DNS change occurred.
Publication remains owner-run unless explicitly delegated.

### Package validation

Approved manifest SHA-256 remains
`9a2b92b3757712d130d1f2205c41bce36fa6a7c0e296628b253dc3730fd21aef`.
All 24 source/export/retained-snapshot files were compared to manifest sizes and hashes, including
exact path sets: PASS. Public source bytes are unchanged. Agent-run on Linux:

```sh
python3 -m unittest discover -s web/tests -p 'test_*.py'
python3 web/tests/audit.py
python3 web/scripts/prepare-release.py --check
python3 scripts/check-doc-links.py
sha256sum web/.release/manifest.json
git rev-parse HEAD
```

49 tests PASS; audit zero findings; source validation PASS (24 files, approved hash);
documentation links PASS. No browser/mobile/assistive checks were repeated. Final live manual
acceptance remains pending.

### Existing public state

Read-only network probes used approved execution outside the restricted network sandbox, normal
TLS verification, GET requests, 20-second timeouts and redirect following. All saved responses and
the backup are under ignored `web/.artifacts/web-07/`; no writes outside the working directory.
GitHub API confirms `lpoli/gohealax` is public, Pages is enabled, and public `main` is at
`1ff05316cf3b15233104ecdf1f337c4b85601239`. Latest listed deployment: `5607510626`, created
`2026-07-26T05:11:55Z`, with that same revision. Unauthenticated Pages-settings API returns 404;
this does not establish that Pages is absent and does not verify its source/custom-domain/HTTPS
settings or agent write access.

The prior public tree has four files; a saved archive's homepage exactly matches live bytes.
Proposed publication diff: 22 additions, two replacements (`index.html`, `CNAME`), two removals
(`LICENSE`, `docs/privacy-policy.md`). Owner approved both removals on 2026-10-14 (details below). Archive checksum and
rollback commands are in [deployment](deployment.md#web-07-existing-site-review-and-rollback).
Agent publication still requires explicit delegation; owner-run publication remains the default.

| HTTPS request | Result |
|---|---|
| `/` | 200; old homepage, byte-identical to prior public revision |
| `/About.html`, `/privacy-policy.html`, `/medical-disclaimer.html` | 404 |
| `/404.html`, `/unknown/nested/path` | 404; host default, not approved custom document |
| `/site.css`, `/site.js`, `/media.js` | 404 |
| `/robots.txt`, `/sitemap.xml` | 404 |
| `https://www.gohealax.com/` | 301 to HTTPS apex, then 200 |

Headers identify GitHub serving; apex/www TLS requests succeeded. Capture around
`2026-10-13 12:25 UTC`. These are existing-host checks, not new-package acceptance or proof of the
Enforce HTTPS setting. Contact/download/network behavior and all approved assets need live checks
after publication. No checkout/push or rollback was performed.

### DNS and owner confirmation

Google DNS-over-HTTPS queries (`https://dns.google/resolve?name=<name>&type=<type>`) captured:

- NS: `dns1.registrar-servers.com.`, `dns2.registrar-servers.com.`.
- A: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
- `www` CNAME: `lpoli.github.io.`.
- MX: priority 10 `eforward1`, `eforward2`, `eforward3`; priority 15 `eforward4`; priority 20
  `eforward5`, all under `registrar-servers.com.`.
- Apex TXT: `v=spf1 include:spf.efwd.registrar-servers.com ~all`.
- Apex AAAA/CAA: no answers (NOERROR with SOA).
- `_github-pages-challenge-lpoli.gohealax.com` TXT: NXDOMAIN. Confirm the account UI/generated
  record rather than inferring account verification state from DNS alone.

This is recursive resolver evidence, not direct authoritative verification. `dig` is unavailable;
direct authoritative queries and full Namecheap zone review were not run. On an equipped host run
the milestone queries against both listed authoritative servers, also including challenge TXT,
AAAA/CAA and www records. Preserve mail/SPF/unrelated records. Existing apex/www routing already
matches GitHub Pages; no routing change is proposed.

The owner replied “yes of course” to confirmation of repository/domain control and public website
distribution rights for the logo/screenshots. This is owner-reported control/permission, not
authenticated agent access or an authorship claim. See
[provenance](provenance.md#web-07-publication-rights-confirmation-2026-10-13).

Official [GitHub domain guidance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site),
[account verification](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
and [Namecheap setup](https://www.namecheap.com/support/knowledgebase/article.aspx/9645/2208/how-do-i-link-my-domain-to-github-pages/)
were rechecked on 2026-10-13. GitHub serves file paths; Namecheap DNS routes the hostname.
Intended publication remains `main`, root, custom domain `gohealax.com`.

### Remaining owner actions and acceptance

1. Confirm GitHub account Settings → Pages domain verification. If absent, add GitHub's supplied
   TXT in Namecheap, verify it and retain it. Confirm repository Pages source/custom domain/HTTPS
   settings, and direct authoritative DNS evidence.
2. Removal of `LICENSE` and the old Markdown privacy page is owner-approved on 2026-10-14;
   publish the approved package without either file. Do not reintroduce them during rollback.
3. Owner publishes the retained approved package or explicitly delegates. Recheck public main
   before copying, retain rollback, and record publication commit/deployment/time.
4. Compare all live package bytes to the manifest, check routes/custom nested 404/assets/metadata,
   contact/download state/TLS/redirects; owner checks desktop/mobile, keyboard, console and initial
   network behavior. Download/demo intentionally remain “coming soon”.
5. Record explicit owner live-site approval before completion. Publication, account verification,
   direct DNS evidence, post-launch checks and owner acceptance are still unfinished.


### WEB-07 owner decisions (2026-10-14)

The owner reports Apache-2.0 was added unknowingly, states the project is solely proprietary,
and requests not retaining the old privacy document. Both removals are approved. No new
open-source licence is requested. The approved 24-file package already excludes both files;
no source/export/hash change is necessary. Preserve the historical backup; rollback instructions
now retain these removals. No public repository/history change has been executed.

The owner sees `gohealax.com` under repository Pages → Custom domain and the message
“Your site is live at https://gohealax.com/”. This confirms repository domain configuration as
owner-reported evidence, consistent with prior HTTPS checks. It does not confirm account-level
verified-domain status. Check profile Settings → Pages → Verified domains separately; if absent,
use Add a domain, add GitHub's generated TXT at Namecheap and click Verify. Account verification,
publishing source/HTTPS settings and direct authoritative DNS evidence remain pending.
Official [account verification](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
and [Pages availability](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
guidance were rechecked on 2026-10-14; no live probes repeated.

Only website files are intended for publication; the private application monorepo remains excluded.
The dedicated website repository is currently public, so its files are visible. If the owner wants
that repository private too, settle GitHub plan/Pages compatibility and hosting choice before
changing visibility. No visibility change has been authorized or executed.
