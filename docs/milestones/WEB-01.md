# WEB-01 — Foundation

Dependencies: repository startup review and the owner's revised plan. No earlier Web gate.
Status/approval: [roadmap](../roadmap.md). Evidence: [handoff](../handoff.md).

## Permitted changes and sources

Create Web instructions, all seven milestone descriptions, design/content/media/testing/deployment/
provenance guides, an ADR, shared-document applicability clarification and the handoff. Establish
standard-library offline checks and a dependency-free browser runner against existing pages. Do not
replace the homepage or change public copy/layout yet. Sources: [PROJECT](../../../PROJECT.md),
[requirements](../../../docs/product/requirements.md), existing `web/site/`, the owner reference,
[design](../design.md), [content](../content.md) and [testing](../testing.md).

## Acceptance

- All seven descriptions exist before test implementation; each defines scope, dependencies,
  acceptance, exact commands, manual checks and blockers.
- Stack, routes, approval rules, asset rights, truthful placeholders, privacy boundaries and export
  strategy are unambiguous. Root summaries point to their canonical Web owners.
- Python HTML/URL checks run offline without a browser. Test the checker with good and broken
  fixtures. Preserve existing working routes/links and contact disclosures.
- Browser runner checks actual existing pages and isolated fixtures, distinguishes pass/fail/timeout/
  skipped, and makes deferred WEB-04 behavior explicit. Record actual execution or its blocker.
- Record current defects as issues assigned to later milestones; do not assert that a redirect,
  wrong disclaimer or unverifiable claim must continue to exist.
- Public source remains unchanged. No native behavior/requirement ID changes.

## Exact commands (repository root)

```sh
python3 -m unittest discover -s web/tests -p 'test_*.py'
python3 web/tests/audit.py
python3 scripts/check-doc-links.py
python3 ios/tools/ios_handoff/verify_handoff.py --require-images
python3 -m http.server 8000 --bind 127.0.0.1 --directory web
```

The audit is intentionally a target-quality report: existing defects give exit 1, separately from
the passing foundation regression suite. It is not a release pass. Open `/site/` and
`/tests/browser.html`; record browser/version, counts and failures. The runner's infrastructure
self-check is included and must not be counted as product interaction coverage.

## Manual gate and blockers

Review the complete docs and the visible runner report; inspect current About/Privacy navigation
and email destination. Confirm future gates remain unstarted. Owner approves this foundation and
baseline evidence, including recorded limits, before WEB-02. Browser unavailability blocks browser
evidence (record it honestly); unverified rights/hosting/Play do not block documentation work.
