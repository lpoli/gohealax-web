# WEB-07 — Launch

Dependencies: explicit WEB-06 approval of a specific package hash in [roadmap](../roadmap.md),
confirmed publication rights, repository access and domain authority.
Status/approval: roadmap; evidence: [handoff](../handoff.md).

## Permitted changes and sources

The owner delegated the source-mirror/Actions migration on 2026-10-14. Synchronize committed
`web/` with Git subtree to `lpoli/gohealax-web`; manually deploy the approved site artifact and
transfer the Pages domain after preparing the new deployment. Sources: [deployment](../deployment.md),
approved manifest, [provenance](../provenance.md), and rechecked official GitHub guidance. Any source
change requires retesting/export and renewed package approval before publication.

## Acceptance

- The public source mirror matches the committed `web/` tree and excludes other components.
  The hosted artifact contains only approved export bytes. Record package hash, monorepo revision,
  subtree/publication revision, Actions run/deployment identifier and timestamp.
- Record authoritative before/after DNS, account TXT verification separately from repository domain
  settings, HTTPS and `www` redirect. Preserve mail and unrelated DNS records.
- Verify landing, exact-case About, Privacy, Disclaimer, 404 including an unknown nested URL,
  assets, robots/sitemap, contact, download state and initial network behavior on the live domain.
- Document previous package/content rollback and DNS restoration separately.
- Owner explicitly approves the live site before WEB-07 becomes Complete.

## Exact verification commands (repository root; network access required)

```sh
python3 -m unittest discover -s web/tests -p 'test_*.py'
python3 web/scripts/prepare-release.py --check
python3 scripts/check-doc-links.py
sha256sum web/.release/manifest.json
dig gohealax.com NS
dig gohealax.com A
dig gohealax.com MX
dig gohealax.com TXT
dig www.gohealax.com CNAME
curl -I https://gohealax.com/
curl -I https://gohealax.com/About.html
curl -I https://gohealax.com/privacy-policy.html
curl -I https://gohealax.com/medical-disclaimer.html
curl -I https://gohealax.com/404.html
curl -I https://gohealax.com/unknown/nested/path
curl -IL https://www.gohealax.com/
```

Also query the authoritative nameserver identified by NS, using `dig @<authoritative-nameserver>`
with the same names/types; replace the placeholder and record the exact commands in launch evidence.
Publication commands are finalized with the real public repository in WEB-06, not guessed here.

## Manual gate and blockers

Owner checks live desktop/mobile, keyboard, contact/download, console/network and source bytes
against the approved manifest. Confirm unknown paths return our usable 404 with an appropriate HTTP
status and that redirect/TLS work. Missing rights, authority/access, failed DNS/certificate checks,
unapproved package or missing explicit live-site approval prevent completion. Do not label a launch
verified from DNS alone or a successful upload alone.
