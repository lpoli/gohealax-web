# GoHealaX web (gohealax.com)

## Current state

`site/` holds the current static gohealax.com pages. They were moved here from the Android project
root (`android/`), where they had lived since the "rebrand Healx as GoHealaX" commit (`80b80c7`):

| File | Purpose |
|---|---|
| `site/index.html` | Redirects to `About.html` (canonical `https://gohealax.com/About.html`) |
| `site/About.html` | Product introduction, no-ads statement and feedback contact |
| `site/privacy-policy.html` | Public privacy policy, also the Play Console privacy-policy URL (`https://gohealax.com/privacy-policy.html`) |
| `site/site.css` | Shared styling |

The pages are plain HTML and CSS with no build step. To preview them, open `site/About.html` in a
browser or run `python3 -m http.server -d web/site`.

The repository does not record how or where gohealax.com is deployed. The Android pre-release
checklist (`android/docs/run-and-deploy.md`) still lists "Public HTTPS privacy-policy URL published" as
unchecked. Whoever deploys the site should document the process here.

## Rules

- The public privacy policy must match the in-app privacy text and
  [docs/security/privacy.md](../docs/security/privacy.md). When the app's data handling changes,
  update `site/privacy-policy.html`, `android/docs/privacy-policy.md` and the in-app copy together.
- A fuller gohealax.com frontend is planned (see [ROADMAP.md](../ROADMAP.md)) but not designed. Record
  its stack choice as an ADR in `docs/decisions/` before adding a framework or build tooling.
