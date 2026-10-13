# Website export and publication

This is a plan, not evidence of live hosting. Current authoritative DNS, hosting provider, public
repository owner/name, access and domain authority are unverified. WEB-01 does not publish anything.
The owner publishes in WEB-07 unless they explicitly delegate the action.

## Export boundary (WEB-06)

Implement `web/scripts/prepare-release.py` with no dependencies. `--check` validates without writing
or replacing an existing package. Default output is fixed at ignored `web/.release/site/`; the
sorted path/byte-size/SHA-256 manifest is `web/.release/manifest.json`, outside the public directory.
No timestamps or machine-specific paths in that manifest. Retain the approved package and manifest
for rollback, inside the repository's ignored artifact area.

Validate the whole source before replacing an earlier package. Reject symlinks (including directory
links), unexpected files, broken references and paths escaping `site/`. Explicitly allow deployable
HTML pages, CSS/JS, reviewed assets, required licence notices, `robots.txt`, `sitemap.xml`, `CNAME` and
`.nojekyll`. Document the precise allowlist with the implementation. Copy bytes unchanged. Exclude
tests, documentation, source reference images, native code, Git metadata and private configuration.
Stage a complete validated export before replacing the old one; failures preserve the prior package.
Repeated inputs produce identical site bytes and manifest, with no stale files. Test all of these.

Planned commands, implemented in WEB-06 (not available in WEB-01):

```sh
python3 web/scripts/prepare-release.py --check
python3 web/scripts/prepare-release.py
python3 -m http.server 8001 --bind 127.0.0.1 --directory web/.release/site
```

Inspect every exported page at origin root, including `/404.html`. Also test a server returning the
404 document for an unknown nested path; a generic Python 404 response alone does not test our 404.
WEB-05 supplies `python3 web/tools/preview.py --root --port 8766` for source inspection.
WEB-06 must extend this preview to the export and record the exact command. Approve the exact
manifest hash and monorepo revision before publishing. Export approval is not permission to change DNS.

## Separate public repository

Publish only `web/.release/site/` contents to the dedicated public repository's `main` branch, root
folder. Never publish this monorepo. Configure Pages to deploy from that branch and `/ (root)`.
An empty `.nojekyll` prevents Jekyll processing. `CNAME` contains only `gohealax.com` plus a newline.
The public repository identity and exact owner-run copy/commit/push commands must be recorded in
WEB-06 once known; do not invent a remote or push to the monorepo's private remotes.

GitHub supports branch/root publication; see its
[publishing-source guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
(reviewed 2026-10-12; recheck before launch).

## Domain and HTTPS (owner, WEB-07)

1. Record the current authoritative DNS answers and hosting, including apex, `www`, NS, MX and TXT
   records. Confirm control of the dedicated repository, domain and all publication rights.
2. Verify the domain at account level with GitHub's supplied TXT record. This is distinct from the
   repository custom-domain setting. Preserve verification and all unrelated/email records.
3. Set the repository custom domain to `gohealax.com` before changing DNS routing. Recheck current
   official values at launch. The planned apex A records are `185.199.108.153`, `185.199.109.153`,
   `185.199.110.153`, `185.199.111.153`; `www` is a CNAME to `<owner>.github.io`. Do not set a
   wildcard. Resolve conflicting obsolete routing records only with the recorded owner-approved plan.
4. Wait for DNS/certificate readiness, enable HTTPS, and verify HTTPS plus `www` redirect to the
   intended canonical apex. Do not claim success while certificate provisioning is pending.
5. Verify all public routes and anchors, case-sensitive About, assets, no initial third-party
   requests, robots/sitemap, unknown nested URL behavior, contact and actual store link state.

Reference: [GitHub custom-domain guidance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).
The values above are planning inputs, not authorization or evidence of DNS changes.

## Release evidence and rollback

Record owner approval of the exact package/manifest hash, monorepo revision, publication repository
and commit, deployment identifier/time, domain verification, before/after DNS, HTTPS and redirect
results, route/asset checks and explicit live-site approval. WEB-07 is not Complete before that final
approval. Store sanitized evidence in the Web handoff; keep credentials and private DNS tokens out.

Content rollback: republish the previous approved package without rebuilding it; record the new
publication commit and repeat live checks. DNS rollback is separate: restore the recorded prior
routing under owner authority, preserve email/TXT records, and verify the previous host and TLS.
Test the content rollback procedure locally in WEB-06 before launch.
