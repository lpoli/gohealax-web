# Website export and publication

This is a local release procedure, not evidence of live hosting. The owner identified the dedicated
publication repository as `lpoli/gohealax` on 2026-10-13. WEB-07 preflight independently confirms a
public repository and existing GitHub Pages hosting. The owner confirms repository/domain control
and website asset distribution rights. Current recursive DNS and HTTPS evidence is recorded in
[handoff](handoff.md#web-07-launch-preflight); direct authoritative DNS, authenticated Pages settings
and account-level verification still need confirmation. Existing routing already matches GitHub Pages.
The owner publishes in WEB-07 unless they explicitly delegate the action.

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

## Separate public repository

Publish only `web/.release/site/` contents to the dedicated public repository's `main` branch, root
folder. Never publish this monorepo. Configure Pages to deploy from that branch and `/ (root)`.
An empty `.nojekyll` prevents Jekyll processing. `CNAME` contains only `gohealax.com` plus a newline.
The owner supplied `lpoli/gohealax`; use the concrete commands below only after the remaining
launch prerequisites and package approval. Never push to the monorepo's private remotes.

GitHub supports branch/root publication; see its
[publishing-source guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
(rechecked 2026-10-13; recheck before launch).

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

## Owner publication commands for WEB-07

These are future owner-run commands, not executed publication. Before using them: confirm this is
an independent public repository, inspect its existing files/history and Pages configuration, confirm
access/domain/rights, record DNS and existing hosting, commit the monorepo implementation, and approve
this exact package hash and committed revision. If the remote is missing or private, stop and resolve
that explicitly. The following clone must be new and clean; do not reuse an arbitrary checkout.
All local writes remain within this working directory.

```sh
git clone --branch main https://github.com/lpoli/gohealax.git web/.artifacts/public-gohealax
git -C web/.artifacts/public-gohealax remote -v
git -C web/.artifacts/public-gohealax status --short
# Review every proposed deletion and replacement first; .git alone is preserved.
rsync -a --dry-run --delete --exclude='/.git/' web/.artifacts/releases/9a2b92b3757712d130d1f2205c41bce36fa6a7c0e296628b253dc3730fd21aef/site/ web/.artifacts/public-gohealax/
rsync -a --delete --exclude='/.git/' web/.artifacts/releases/9a2b92b3757712d130d1f2205c41bce36fa6a7c0e296628b253dc3730fd21aef/site/ web/.artifacts/public-gohealax/
git -C web/.artifacts/public-gohealax add --all
git -C web/.artifacts/public-gohealax diff --cached --stat
git -C web/.artifacts/public-gohealax diff --cached --check
git -C web/.artifacts/public-gohealax commit -m "Publish approved GoHealaX website package 9a2b92b3"
git -C web/.artifacts/public-gohealax push origin main
```

If the repository is empty and has no `main`, the clone command needs owner setup first; do not
invent a branch/history. `rsync --delete` intentionally makes the public working tree exactly the
approved site; review the dry run before execution. The manifest, snapshots and documentation are
never copied. For content rollback, substitute the previous approved hash-named snapshot in those
same copy/commit/push commands, then repeat live checks. Never force-push or rebuild the old package.

In repository Settings → Pages select **Deploy from a branch**, `main`, `/ (root)`.
Verify the domain at account level; set repository custom domain to `gohealax.com` before DNS routing,
then follow the DNS/HTTPS steps above. CNAME bytes alone do not establish domain configuration.
Current official Pages guidance was rechecked on 2026-10-13; A values above still match. Recheck
again when launching. No live DNS/HTTPS/deployment state was inferred from these instructions.

The earlier WEB-06 candidate (`16535334…87c4`) is retained locally for rollback, but superseded
for owner review by the project-logo candidate above.

## WEB-07 existing-site review and rollback

The approved source is now committed at `5ba3f2b79b59f62b4dbd0f9f0318f746a59ff0e4`.
Preflight on 2026-10-13 found the existing public `main` commit
`1ff05316cf3b15233104ecdf1f337c4b85601239`. Its four files are `CNAME`, `index.html`, `LICENSE`
and `docs/privacy-policy.md`. The exact-package copy above proposes 22 additions, replacement of
the homepage/CNAME, and removal of the existing licence and Markdown privacy document. On
2026-10-14 the owner approved both removals: Apache-2.0 was added unintentionally; the owner
states the project is proprietary. Do not add an open-source licence or republish the obsolete
privacy document. The approved package remains unchanged. This does not delegate an agent push. The proposed changes are saved in `web/.artifacts/web-07/publication-diff.json`.

Before copying, confirm public `main` still matches that recorded commit; if it moved, stop and
refresh the backup/diff. A read-only archive of the prior public tree is retained at
`web/.artifacts/web-07/previous-public-repository.tar.gz`, SHA-256
`ef62571c4821986ff1fcf24fd44f461eb3309c946c943070e929f20072cf3681`.
All four archive files were inspected; the archived homepage exactly matches the current live
homepage. No checkout/push or rollback was performed.

For an owner-run rollback after publication, use the clean public checkout with no unrelated
changes, review restoring the recorded prior tree, then create a new commit and push normally:

```sh
git -C web/.artifacts/public-gohealax restore --source=1ff05316cf3b15233104ecdf1f337c4b85601239 --staged --worktree -- .
git -C web/.artifacts/public-gohealax rm --ignore-unmatch LICENSE docs/privacy-policy.md
git -C web/.artifacts/public-gohealax diff --cached --stat
git -C web/.artifacts/public-gohealax diff --cached --check
git -C web/.artifacts/public-gohealax commit -m "Restore pre-WEB-07 public website"
git -C web/.artifacts/public-gohealax push origin main
```

This restores the prior homepage/CNAME while retaining the owner-requested licence/privacy
removals. The archive is an exact historical backup, not a package to republish unchanged. No
history rewrite or rebuild is involved. Repeat HTTPS/homepage/redirect checks; the old
site does not provide the new WEB-07 routes. Execution remains unrun. DNS restoration is separate:
retain the preflight A/CNAME/NS/MX/TXT evidence, confirm it directly against authoritative servers
and the Namecheap account, and restore only records actually changed under owner authority.
No DNS change is proposed for the currently working apex/www routing. Account-verification TXT
records must be retained, alongside SPF/mail records.
