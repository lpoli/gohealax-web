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
interaction cases; WEB-05 metadata, image dimensions, sitemap and complete route coverage. The WEB-05 audit now passes and is enforced by `test_quality.py`, including adversarial
metadata, image, missing-file, network-resource, sitemap and 404 fixtures. WEB-06 adds exporter tests (including symlinks, reproducibility and stale files).

## Browser runner

The runner loads real pages in same-origin isolated iframes and uses isolated fixtures to validate
its reporting/timeouts. Every result is PASS, FAIL, TIMEOUT or SKIP with a reason. Its summary states
whether the run is a baseline with deferred coverage; a skipped interaction test never counts as a
pass. Failed requests/imports, thrown assertions and timed-out loads must remain failures. The runner
has a visible static loading message and a watchdog for bootstrap failure.

WEB-02 real-page checks include landing/About/Privacy navigation/contact, rendered width at
320, 375, 768, 1024 and 1440px, stylesheet application and HTTP loading, with scripts disabled.
The homepage redirect is now forbidden in both the offline gate and browser runner. WEB-04 checks
import the production `site.js`/`media.js` functions into fixtures, with controlled
player adapters. The runner now has no deferred interaction groups. It checks all four pages at the
scripts-disabled widths above and applies the production enhancement to real mobile markup. Cover menu state, Escape/focus, link activation, duplicate initialization, resize,
invalid/disabled/media activation and playback failures. Maintain modules and their tests together; do
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

## Fresh browser fixtures

Real-page fixtures fetch their HTML with `cache: no-store`, then use a script-disabled `srcdoc`
frame with the original page URL as its base. Stylesheets retain their real HTTP URLs with a fresh
`_webcheck` query value per fixture. This prevents an ordinary browser profile from mixing fresh
HTML assertions with older cached frame HTML/CSS. Relative images/links still resolve from the real
page route. HTTP errors remain failures. The browser regression verifies repeated stylesheet URL
freshness, current HTML, original relative asset resolution and missing-page failure.

After changing the runner itself, hard-refresh `/tests/browser.html` once (Ctrl+Shift+R on Linux
Chrome) to load the updated test modules. Current automated coverage is 47 cases; user rerun evidence
is separate from the agent's result in the handoff.

## Reliable local preview and phone inspection

Run from the repository root:

```sh
python3 web/tools/preview.py
```

Open `http://127.0.0.1:8765/site/`; automated tests are at
`http://127.0.0.1:8765/tests/browser.html`. The source directory is resolved from the script rather
than the shell's current directory. Preview responses use `Cache-Control: no-store, max-age=0` and
ignore conditional cache validators, including for CSS. Port 8765 gives the preview a new origin
from the old port-8000 server. This avoids old preview caching; it is development-only tooling,
not a production hosting change. Stop with Ctrl+C.

For a real phone, connect it and the computer to the same Wi-Fi, then run:

```sh
python3 web/tools/preview.py --lan
```

Find the computer's Wi-Fi IPv4 address in its network settings (`hostname -I` also lists candidate
addresses; select the Wi-Fi address rather than a Docker/VPN address). On the phone open
`http://<computer-Wi-Fi-IP>:8765/`, for example `http://192.168.1.20:8765/`. Use the computer's
address, not the phone's localhost. LAN mode serves only `web/site/` at `/`; it does not serve tests,
docs or owner reference material. Test portrait/landscape, Menu and every legal-page link, readable
text, image fit and horizontal scrolling. If unreachable, check the Wi-Fi permits device-to-device
traffic and the computer firewall allows this port. Stop the server with Ctrl+C when finished.

For a desktop approximation, open Chrome DevTools (F12), toggle its device toolbar, choose
Responsive, test 320/375/425/768 widths and rotate. Firefox Responsive Design Mode uses Ctrl+Shift+M.
Use [Chrome's device-mode guide](https://developer.chrome.com/docs/devtools/device-mode) for details;
emulation is not a substitute for a real phone test.

An owner report on 2026-10-13 says the old HTTP preview rendered incorrectly while opening
`index.html` directly rendered correctly. The precise server command/URL and HTTP error have not yet
been supplied. Stale CSS or an incorrect served path are possibilities, not an established cause.
If the uncached preview still differs, inspect Network for `site.css` (HTTP 200, `text/css`) and
missing assets, and record the exact command/URL. Direct file opening is useful for static layout
but does not verify ES modules and interaction behavior; final checks use HTTP.

## Guest browser and sandbox policy

Owner requirement, 2026-10-13: automated/headless Chrome always uses `--guest` and a new, unique
profile directory under `web/.artifacts/` for each launch. Never attach to an existing personal
Chrome or use normal tabs, cookies, history or logins. A dedicated profile was used in prior runs,
but some runs reused that automation profile and did not specify Guest mode; archived commands are
historical evidence and must not be reused unchanged. Future invocations must follow this policy.

Chromium [defines the Guest switch](https://chromium.googlesource.com/chromium/src/+/HEAD/chrome/common/chrome_switches.h)
and [documents its sandbox](https://www.chromium.org/developers/design-documents/sandbox/).
Keep the browser's sandbox enabled; never pass `--no-sandbox`, `--disable-setuid-sandbox` or equivalent
flags. Profile isolation, Guest mode and the execution environment's sandbox are separate boundaries.
If the environment blocks a browser, report the failure and obtain any required tool escalation
approval without disabling Chromium's sandbox. Store its temp/config/cache/report/crash output inside
the unique repository-local run directory, and close only the process started for that run.

Example launch pattern, from the repository root (future browser verification, not run in this update):

```sh
mkdir -p web/.artifacts
web_qa_run=$(mktemp -d "$PWD/web/.artifacts/guest-run-XXXXXX")
mkdir -p "$web_qa_run/tmp" "$web_qa_run/config" "$web_qa_run/cache" "$web_qa_run/crashes"
env TMPDIR="$web_qa_run/tmp" XDG_CONFIG_HOME="$web_qa_run/config" XDG_CACHE_HOME="$web_qa_run/cache" \
  google-chrome --guest --headless --disable-gpu --disable-dev-shm-usage \
  --disable-breakpad --disable-crash-reporter --disable-background-networking \
  --disable-component-update --no-first-run --no-default-browser-check \
  --user-data-dir="$web_qa_run/profile" --disk-cache-dir="$web_qa_run/cache" \
  --crash-dumps-dir="$web_qa_run/crashes" --virtual-time-budget=30000 \
  --dump-dom http://127.0.0.1:8765/tests/browser.html \
  > "$web_qa_run/report.html" 2> "$web_qa_run/browser.log"
```


## WEB-05 origin-root and nested 404 preview

```sh
python3 web/tools/preview.py --root --port 8766
```

Inspect `http://127.0.0.1:8766/`, all four indexable routes, `/404.html` and
`http://127.0.0.1:8766/unknown/nested/page`. Missing paths return the actual site 404 HTML with
HTTP 404, root-relative assets/navigation and noindex; successful assets keep HTTP 200. LAN mode
also uses this fallback. The standard library handler is used otherwise, with unchanged uncached
responses. Stop with Ctrl+C. `--root` and `--lan` are mutually exclusive. The browser runner remains
at port 8765 in default preview mode. No cross-origin request is added to the runner; separate
origin-root inspection verifies the fallback server. Repeat against the WEB-06 export later.

On this host Chrome's Unix socket path limit requires short temporary paths: use a fresh
`web/.artifacts/gXXXX` run directory and short `t`, `p`, `c`, `k`, `d` subdirectories instead of the
long example above. Set `XDG_DATA_HOME` inside the run directory too, or use the actual Chrome binary
(`/opt/google/chrome/chrome`) to avoid wrapper-created files outside the workspace. Guest headless
`--dump-dom` yielded no report here. The verified run uses the new browser's `DevToolsActivePort`
and its own blank Guest tab (`/json/list`); Guest rejected `/json/new` with HTTP 500. Enable `Emulation.setFocusEmulationEnabled` for focused-style inspection in the headless tab.
Never connect to another instance. Keep the browser sandbox enabled and close only the browser started for the run.

WEB-05 adds 200% root-font reflow, skip-link focusability and actual image decoding checks on the
four real content pages. This automated enlargement does not replace manual browser text-only or
400% zoom, screen-reader or real-mobile checks. Lighthouse is owner-run through the DevTools method
above; record version, Mobile/Desktop results and save both reports. Current evidence is in the
[handoff](handoff.md#web-05-quality-and-review).


## WEB-06 package checks

The offline suite adds exporter allowlist/exclusion, links/escapes, symlinks, staging/replacement
failure, stale removal, byte equality, deterministic manifest and saved-package rollback checks.
Temporary fixture trees are created exclusively under `web/.artifacts/` and removed after tests.

```sh
python3 web/scripts/prepare-release.py --check
python3 web/scripts/prepare-release.py
sha256sum web/.release/manifest.json
python3 web/tools/preview.py --port 8000
# Separate terminal: root export preview with actual nested fallback
python3 web/tools/preview.py --exported --port 8001
```

Open `http://127.0.0.1:8000/tests/browser.html` for the shared suite and inspect all exported pages
at port 8001, including `/404.html` and `/unknown/nested/page`. The suite exercises source pages;
byte equality tests tie those results to the export. Exported root rendering is checked separately.
`--exported`, `--root` and `--lan` are mutually exclusive. Export preview fails clearly if the package
is missing. Saved package restore commands and future publication/rollback are in
[deployment](deployment.md#retain-and-restore-a-reviewed-package). Nothing here publishes or changes DNS.

## Standalone source mirror and deployment approval

In `lpoli/gohealax-web`, run the same suite/audit/export commands without the `web/` prefix.
The root documentation link checker belongs to the monorepo; Web documents link back to private
canonical contracts that are intentionally absent from the public mirror. The derived PROD-01
fixture is compared to canonical requirements whenever they are present in monorepo validation.
Tests prove standalone fallback, stale-fixture failure, malformed/wrong approval hashes, and altered
export bytes. The manual [Pages workflow](../.github/workflows/pages.yml) runs those gates and
verifies the approved manifest before uploading only `.release/site/`. See [deployment](deployment.md).
