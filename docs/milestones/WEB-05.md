# WEB-05 — Quality

Dependencies: explicit WEB-04 approval in [roadmap](../roadmap.md).
Status/approval: roadmap; evidence: [handoff](../handoff.md).

## Permitted changes and sources

Finish responsive assets, accessibility, metadata, favicons/social image, sitemap, robots and 404.
Sources: [design](../design.md), [testing](../testing.md), [content](../content.md) and
[provenance](../provenance.md). No export/publication yet.

## Acceptance

- Image dimensions, responsive hero sources, eager hero and lazy below-fold loading; no missing
  assets or initial third-party requests. Record rights for favicon/social derivatives too.
- Readable focus/contrast, keyboard access, reduced motion, browser resizing and text zoom.
- Each indexable page has unique title/description and the specified absolute canonical; homepage
  canonical ends `/`. Sitemap lists exactly these pages; 404 is excluded and noindex.
- 404 root-relative assets/navigation work under unknown nested URLs at origin root. Add a local
  fallback preview fixture/server and document its exact command.
- Static target audit is now a required passing gate with all findings enforced in regression tests.
  Browser interaction suite has no unexplained skips, failures or timeouts.
- Record mobile and desktop Lighthouse versions/results and resolve material findings. Scores do
  not replace accessibility inspection.

## Exact commands (repository root)

```sh
python3 -m unittest discover -s web/tests -p 'test_*.py'
python3 web/tests/audit.py
python3 scripts/check-doc-links.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory web
python3 -m http.server 8001 --bind 127.0.0.1 --directory web/site
```

At port 8000 open `/tests/browser.html`; at 8001 inspect all root routes. Run Lighthouse via Chrome
DevTools → Lighthouse → Navigation, once Mobile and once Desktop, exporting reports inside
`web/.artifacts/`. Add the nested-404 server command when implemented; Python's stock 404 is insufficient.

## Manual gate and blockers

Chrome, Firefox, real mobile; 320–1440px, both orientations, 200% text, 400% desktop zoom; keyboard and
screen reader; reduced motion, contrast/focus, console and missing requests. Owner approves quality
evidence. Unrun real-device/assistive checks remain pending and must be resolved for this gate.
