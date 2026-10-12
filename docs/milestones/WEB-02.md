# WEB-02 — Layout

Dependencies: explicit WEB-01 approval in [roadmap](../roadmap.md).
Status/approval: roadmap; evidence: [handoff](../handoff.md).

## Permitted changes and sources

Replace `index.html` redirect with the complete landing composition; add scoped CSS, licensed hero
imagery, original branding, anchors, download-panel layout and wave footer. Include coherent initial
copy and visible plain navigation. Sources: [design](../design.md), [content](../content.md),
[provenance](../provenance.md), [requirements](../../../docs/product/requirements.md) and the owner
reference. No playback/disclosure JS, release export or deployment in this increment.

## Acceptance

- All sections appear in the agreed order, including Team and Contact. No reference presentation
  heading, recovery promises, fake app screens or copied reference imagery.
- Layout uses 72rem max, 48rem/64rem breakpoints, readable legal pages and wrapping text. Navigation
  and download availability are usable without JavaScript. Android/iOS placeholders are honest.
- Hero is self-hosted with recorded source, licence, attribution, changes and approval state. Any
  unconfirmed publication rights are visible release blockers, not silently cleared.
- Replace homepage redirect audit findings with enforced landing checks; section links resolve.
  About/Privacy route case and content remain intact.

## Exact commands (repository root)

```sh
python3 -m unittest discover -s web/tests -p 'test_*.py'
python3 web/tests/audit.py
python3 scripts/check-doc-links.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory web
```

Open `/site/` and `/tests/browser.html`. Document remaining audit findings by later milestone;
new or in-scope failures prevent approval. Run the iOS verifier command in WEB-01 if shared
requirements change.

## Manual gate and blockers

Compare composition with the reference at 320, 375, 768, 1024 and 1440px; check portrait/landscape,
200% text and 400% desktop zoom, wrapping, anchor targets and no-JS navigation. Inspect legal pages
for CSS regressions. Owner approves layout/imagery and known remaining content work. Lack of an
acceptable licensed photo blocks the final layout gate; no verified Play URL permits placeholder.
