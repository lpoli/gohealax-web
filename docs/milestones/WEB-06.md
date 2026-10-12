# WEB-06 — Release preparation

Dependencies: explicit WEB-05 approval in [roadmap](../roadmap.md).
Status/approval: roadmap; evidence: [handoff](../handoff.md).

## Permitted changes and sources

Implement deterministic export, `CNAME`, `.nojekyll`, packaging tests and final owner publication,
DNS/HTTPS and rollback instructions. Sources: [deployment](../deployment.md),
[testing](../testing.md), [provenance](../provenance.md) and GitHub guidance linked in deployment.
Do not publish or mutate DNS. Resolve repository identity and rights before calling a package launch-ready.

## Acceptance

- `prepare-release.py --check` is validation-only, with fixed ignored output for normal export.
  Validate before replacement, reject symlinks/unexpected files/escaping or broken references,
  preserve earlier output on failure and remove stale files on success.
- Exact allowlist excludes docs/tests/reference/native/private/Git content. Copy bytes unchanged;
  sorted deterministic path/size/SHA-256 manifest lives beside, not inside, the public directory.
- Test exclusions, bad references, symlink rejection, repeated identical outputs, failed replacement
  and stale-file removal. All temporary test trees stay inside the repository.
- Preview exported root routes and actual nested 404 fallback; test rollback to a prior local package.
- Record owner/repository identity, authoritative existing hosting/DNS, rights status, and exact
  future publication commands. Approve the exact package hash and monorepo revision.

## Exact commands (repository root; implement exporter in this milestone)

```sh
python3 -m unittest discover -s web/tests -p 'test_*.py'
python3 web/tests/audit.py
python3 scripts/check-doc-links.py
python3 web/scripts/prepare-release.py --check
python3 web/scripts/prepare-release.py
sha256sum web/.release/manifest.json
python3 -m http.server 8001 --bind 127.0.0.1 --directory web/.release/site
```

Run the browser suite at port 8000 as in WEB-05. Use the nested-404 preview command supplied in WEB-05
with the export as its document root; record it in the handoff.

## Manual gate and blockers

Inspect the manifest and every exported route, licences, contact/download state and no extraneous
files. Owner approves the exact exported package. Missing rights/repository/DNS authority blocks
launch; safe local export testing can continue. Do not infer publication permission from package approval.
