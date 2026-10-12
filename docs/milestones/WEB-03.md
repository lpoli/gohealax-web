# WEB-03 — Content

Dependencies: explicit WEB-02 approval in [roadmap](../roadmap.md).
Status/approval: roadmap; evidence: [handoff](../handoff.md).

## Permitted changes and sources

Finish feature explanations and standalone About, contributor/contact placeholders, truthful download
availability and reviewed screenshot presentation. Sources: [content](../content.md),
[provenance](../provenance.md), [requirements](../../../docs/product/requirements.md),
[ADR-0007](../../../docs/decisions/0007-android-is-completely-free.md), and
[screen register](../../../design/screens/README.md). Do not implement WEB-04 interactions or publish.

## Acceptance

- Explain Prepare/Hold/Relax, repetitions, sets, Count Pace, presets, daily planning, schedules,
  history and recorded activity accurately. All current Android features are free; iOS Coming Soon.
- Unverified Play availability says “Android download link coming soon”; no actionable unavailable
  store badge. Remove the old unverifiable availability/pilot claims.
- Team placeholder and contact email are honest. Contributor and social editing comments exist in
  source. No social links until verified destinations exist.
- Screenshots have recorded revision, synthetic-data source, visual inspection and example captions.
  Reject personal data, obsolete purchases/locks and simulated reference screens.
- Add content checks for these completed requirements; navigation consistency and route tests pass.

## Exact commands (repository root)

```sh
python3 -m unittest discover -s web/tests -p 'test_*.py'
python3 web/tests/audit.py
python3 scripts/check-doc-links.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory web
```

Open `/site/`, `/site/About.html` and `/tests/browser.html`. Record residual legal/quality findings
for WEB-04/05; no in-scope defects may be hidden. Use WEB-01's iOS verifier if shared requirements change.

## Manual gate and blockers

Read all copy against the current Android implementation/requirements. Inspect screenshots at mobile
and desktop sizes, example captions and email links; check no-JS content. Owner approves wording,
screenshots and editable locations. Missing contributors/social/video/Play permits placeholders.
Missing current, reviewed screenshots blocks screenshot acceptance, not unrelated copy work.
