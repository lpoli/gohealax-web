# WEB-04 — Interaction and legal

Dependencies: explicit WEB-03 approval in [roadmap](../roadmap.md).
Status/approval: roadmap; evidence: [handoff](../handoff.md).

## Permitted changes and sources

Implement `site.js`, separate `media.js`, medical disclaimer, exact disclaimer in About/Privacy,
and separate website privacy disclosures. Sources: [design](../design.md), [media](../media.md),
[content](../content.md), [privacy principles](../../../docs/security/privacy.md), PROD-01/02/03 in
[requirements](../../../docs/product/requirements.md), existing Privacy and the WAI source in design.
Do not enable unreviewed media or invent hosting evidence.

## Acceptance

- Mobile disclosure has native links/button, correct ARIA, Escape/focus return, unprevented link
  activation and safe resizing. Visible HTML navigation survives failed/disabled JS. Initialization
  twice does not duplicate listeners or effects.
- Disabled/invalid media stays a local poster and readable placeholder, with no active play control.
  Valid YouTube/self-hosted configurations follow the attribute contract and accessibility review.
  Player creation occurs only on explicit activation; captions/transcript and failure fallback work.
- Browser tests execute actual production modules on isolated fixtures using controlled adapters;
  no test contacts YouTube. Replace deferred interaction skips with real assertions covering state,
  Escape, focus, resize, duplicates, invalid media, activation, error and timeout behavior.
- Exact PROD-01 appears on all three legal/About pages; preserve Android disclosures and clearly
  separate hosting/media. Record unresolved actual-hosting verification honestly.

## Exact commands (repository root)

```sh
python3 -m unittest discover -s web/tests -p 'test_*.py'
python3 web/tests/audit.py
python3 scripts/check-doc-links.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory web
```

Open `/tests/browser.html` and all `/site/` pages. Run WEB-01's iOS verifier if shared requirements
change. Record remaining WEB-05 metadata findings separately, with no interaction skips excused.

## Manual gate and blockers

Keyboard Tab/Shift+Tab, Enter/Space, Escape, resize while focused; screen-reader smoke test; disabled
and failed JS; blocked player and missing video/captions; Network panel reload showing no initial
third-party requests. Test Chrome, Firefox and owner-run real mobile browser. Owner approves keyboard,
failure and legal behavior. Missing accessible video keeps demo disabled and does not block the site.
