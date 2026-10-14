# Website export and publication

The monorepo remains the source of truth. The owner selected one-way Git subtree synchronization
of all committed `web/` files to the public `lpoli/gohealax-web` repository on 2026-10-14.
`ssd` and `mycc` retain their existing URLs and full-monorepo workflow. Source synchronization and
live deployment are separate operations. No Git hooks or force pushes are used.

## Separate public repository

The public source mirror contains `site/`, `docs/`, `tests/`, `scripts/`, `tools/`, `asset-sources/`,
`image-ref/`, README and the other tracked Web files, including their Web-only history. Native
components and monorepo root files are excluded. Ignored exports, caches and profiles are excluded.
Documentation and references are public source, but are never part of the hosted website.

From the monorepo root, after validating and committing the intended changes:

```sh
# Add once; inspect an existing remote before reusing its name.
git remote add webgithub git@github.com:lpoli/gohealax-web.git
git ls-remote webgithub
git subtree split --prefix=web
# Compare the printed split revision's root tree with HEAD:web before pushing.
git rev-parse HEAD:web
git rev-parse <split-revision>^{tree}
git subtree push --prefix=web webgithub main
```

The two tree hashes must match. Inspect the split root and confirm only Web files are present.
Before the first push, inspect the destination history: if it has conflicting initial commits,
stop and reconcile them with the owner. Never overwrite that history. Subsequent pushes are normal
fast-forward updates. Develop in the monorepo; direct GitHub edits cause divergence and must be
reconciled before the next synchronization. Existing private remotes and branch tracking stay unchanged.
See [Git subtree documentation](https://github.com/git/git/blob/master/contrib/subtree/git-subtree.adoc).

## Manual GitHub Actions publication

The source workflow is [pages.yml](../.github/workflows/pages.yml); subtree export places it at
`.github/workflows/pages.yml` in the mirror. Configure Settings → Pages → Source to **GitHub Actions**.
Source pushes never trigger publication. Actions → Publish approved website → Run workflow on
`main` requires `manifest_sha256`, the exact owner-approved manifest SHA-256. The workflow is
restricted to `lpoli/gohealax-web` and `main`, runs offline tests/audit/export validation, exports,
then [verifies approval](../scripts/verify-approved-release.py) before uploading `.release/site/`
only. A mismatching hash or altered site fails before deployment. The manifest is retained as a
separate Actions artifact; the run summary records source revision and approved hash.

From the standalone mirror root:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tests/audit.py
python3 scripts/prepare-release.py --check
python3 scripts/prepare-release.py
python3 scripts/verify-approved-release.py --manifest-sha256 9a2b92b3757712d130d1f2205c41bce36fa6a7c0e296628b253dc3730fd21aef
```

The derived [PROD-01 fixture](../tests/fixtures/prod-01-disclaimer.txt) makes validation independent
of the private monorepo. Monorepo validation additionally compares it to canonical PROD-01 and
fails if stale. Regenerate the fixture from the canonical quoted disclaimer when that requirement
changes; never silently change the requirement in the public mirror.

Only the 24-file approved site artifact is hosted at the domain root. The workflow uses the
`github-pages` environment and deployment-scoped `pages: write`/`id-token: write` permissions.
Official [custom workflow guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
was rechecked on 2026-10-14. Package approval is not live-site approval.

## Export boundary (WEB-06)

Use `web/scripts/prepare-release.py` with no dependencies. `--check` validates without writing
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

Implemented commands (repository root):

```sh
python3 web/scripts/prepare-release.py --check
python3 web/scripts/prepare-release.py
python3 -m http.server 8001 --bind 127.0.0.1 --directory web/.release/site
```

Inspect every exported page at origin root, including `/404.html`. Also test a server returning the
404 document for an unknown nested path; a generic Python 404 response alone does not test our 404.
WEB-05 supplies `python3 web/tools/preview.py --root --port 8766` for source inspection.
Export inspection uses `python3 web/tools/preview.py --exported --port 8001`.
This serves the exported document root and actual custom nested 404, on loopback only. Approve the exact
manifest hash and monorepo revision before publishing. Export approval is not permission to change DNS.

## Domain and HTTPS (WEB-07)

Prepare and validate the new repository/workflow before transferring `gohealax.com` from
`lpoli/gohealax`. Confirm authenticated administrative access and account-level domain verification.
Retain GitHub's verification TXT and all unrelated/email records. Save old/new Pages settings and
DNS evidence before mutation. Source `CNAME` is retained in the approved artifact, but GitHub Actions
uses the repository Pages custom-domain setting; `CNAME` alone does not configure the domain.

1. Recheck authoritative NS, apex A/AAAA/CAA/MX/TXT, `www` CNAME and the account challenge TXT.
   Existing intended A records are `185.199.108.153`, `185.199.109.153`, `185.199.110.153`,
   `185.199.111.153`; `www` points to `lpoli.github.io`. With the same owner, no routing change is
   expected. Preserve verification TXT, SPF and mail records; inspect differences before changing DNS.
2. Configure the new repository for Actions and validate its release before transferring the domain.
   Remove the old repository Pages custom-domain setting, then immediately set `gohealax.com` in
   the new repository. With branch publication on the old repository, also remove its root CNAME
   so a later build cannot reclaim the domain. Do not change the approved new artifact's CNAME.
3. Trigger the new workflow on the synchronized `main` with the approved manifest hash. Record
   run/deployment ID, time and public split revision. Wait for successful deployment and certificate
   readiness, enable Enforce HTTPS and check apex HTTPS plus `www` canonical redirect.
4. Compare all live assets/pages with the approved manifest. Check About, Privacy, Disclaimer,
   robots/sitemap, CSS/JS/images and the custom 404 on an unknown nested URL (HTTP 404 with the
   approved 404 document). Check contact/download state and initial network behavior. Record
   owner desktop/mobile, keyboard and console inspection and explicit live-site approval.

Reference: [GitHub domain guidance](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
(rechecked 2026-10-14). Final acceptance remains in [WEB-07](milestones/WEB-07.md).

## Release evidence and rollback

Record monorepo revision, subtree/public revision, manifest hash, Actions run/deployment ID/time,
Pages settings, before/after DNS, verification TXT confirmation, TLS/redirect and route/asset results
in [handoff](handoff.md). WEB-07 becomes Complete only after explicit owner live-site approval.

Content rollback: retain every approved package and manifest in the monorepo artifact area.
Restore the previous approved site bytes to `web/site/`, validate and commit a normal rollback,
synchronize the subtree and manually deploy with that previous approved manifest hash. This does
not rewrite history and the hash gate proves the restored artifact. Do not deploy an older public
revision without confirming it contains the reviewed workflow and standalone validation fixture.
The local `--restore` commands below verify retained package integrity independently.

Domain rollback is separate: remove the new Pages custom domain, restore the old repository's
recorded Pages source/domain (and root CNAME for branch publication), verify the old deployment/TLS,
and restore only DNS records actually changed. Preserve TXT/mail. The historical old tree includes
owner-rejected documents; do not restore those documents into public HEAD during rollback.

## Exact export allowlist and replacement

The exporter owns a literal 24-path `ALLOWLIST` in
[prepare-release.py](../scripts/prepare-release.py): five HTML pages (`index.html`, `About.html`,
`privacy-policy.html`, `medical-disclaimer.html`, `404.html`), `site.css`, `site.js`, `media.js`,
`robots.txt`, `sitemap.xml`, `CNAME`, `.nojekyll`; the project logo, four icon/social assets, three hero WebPs, and
four reviewed PNGs under `assets/screenshots/`. Only `assets/` and `assets/screenshots/` directories
are permitted. Any addition requires an explicit code/provenance review. No separate attribution
notice is currently required: the Pexels credit/licence links already appear in exported HTML;
original artwork/font rasterization and screenshots are recorded in [provenance](provenance.md).

Validation checks exact domain markers, page quality, HTML links/fragments/srcsets, media data URLs,
and literal JS module imports. CSS url/import requests are forbidden by the existing quality gate.
Source and staged copies are validated and their manifests compared before replacement. This is a
packager for the reviewed source, not a general JavaScript parser or hostile-concurrent-writer guard.

Site and manifest are staged together under a fresh `web/.artifacts/release-*` directory. The old
`web/.release/` is renamed there to `previous`, then the staged package is renamed into place.
Caught replacement failures restore the prior package. Successful replacement removes stale files.
Do not export concurrently or serve during replacement: the two renames have a brief missing-path
window. Power/process interruption between them can leave `previous` in the transaction directory;
retain it and recover with `--restore` after inspecting its manifest. This is exception-safe replacement,
not a claim of crash-atomic publication. `.release/` is disposable package output, not snapshot storage.

## Retain and restore a reviewed package

The owner-approved WEB-06 package (2026-10-13) is retained at
`web/.artifacts/releases/9a2b92b3757712d130d1f2205c41bce36fa6a7c0e296628b253dc3730fd21aef/`.
It contains exactly `site/` and `manifest.json`. For a later candidate, save once to a new hash-named
directory before approving or publishing; never overwrite an approved snapshot. Keep review evidence
and the committed monorepo revision separately from the deterministic manifest.

```sh
# Local content rollback: validates snapshot bytes against its manifest, then replaces output.
python3 web/scripts/prepare-release.py --restore web/.artifacts/releases/9a2b92b3757712d130d1f2205c41bce36fa6a7c0e296628b253dc3730fd21aef --check
python3 web/scripts/prepare-release.py --restore web/.artifacts/releases/9a2b92b3757712d130d1f2205c41bce36fa6a7c0e296628b253dc3730fd21aef
sha256sum web/.release/manifest.json
python3 web/tools/preview.py --exported --port 8001
```

`--restore` only accepts paths inside repository-local `web/.artifacts/`, rejects symlink paths,
and requires the saved manifest to match the validated site exactly. Restore also permits the
previously retained 23-file packages without the new project logo; normal source export requires all
24 files. All references must still resolve. `--check` also works with
`--restore` and writes no package or temporary files. Local regression tests restore a previous
package after a changed candidate and assert every original byte and manifest returns.

## WEB-07 existing-site review and rollback

The historical `lpoli/gohealax` tree was recorded at
`1ff05316cf3b15233104ecdf1f337c4b85601239`, containing CNAME, index.html, LICENSE and
`docs/privacy-policy.md`. The owner approved deleting the accidental Apache-2.0 licence and obsolete
Markdown privacy document on 2026-10-14. No new open-source licence is requested. Recheck old main
before deleting exactly these two files in a normal commit/push; preserve the homepage until the
new deployment is prepared. Stop and refresh the backup if old main changed.

The exact historical backup remains at `web/.artifacts/web-07/previous-public-repository.tar.gz`,
SHA-256 `ef62571c4821986ff1fcf24fd44f461eb3309c946c943070e929f20072cf3681`.
It is recovery evidence, not a package to republish unchanged. For an old-host rollback restore the
historical homepage and required CNAME in a new commit while retaining the licence/privacy deletions.
Never force-push. Current execution evidence and any access blockers belong in the handoff.
