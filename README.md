# GoHealaX website

Responsive informational website, developed in the monorepo and synchronized with Git subtree to the
public `lpoli/gohealax-web` source mirror. Manual GitHub Actions deploys only the approved site export. Plain HTML, CSS and JavaScript; no framework, package manager or build step.
Decision: [ADR-0008](../docs/decisions/0008-static-informational-website.md).

Start with [Web instructions](AGENTS.md), [roadmap](docs/roadmap.md) and [handoff](docs/handoff.md).
The roadmap owns the seven approval gates. WEB-02 replaces the homepage redirect with an owner-approved responsive landing page. WEB-03
product/About copy and screenshot gallery were approved on 2026-10-13. WEB-04 navigation, media
support and legal pages and WEB-05 quality were approved on 2026-10-13. WEB-06 release preparation was approved on 2026-10-13; WEB-07 deployment and the final live site were approved on 2026-10-14. All seven milestones are
Complete; subsequent owner-requested work is listed in Web todos. Evidence limits remain in the handoff.

## Source and documentation

| Location | Purpose |
|---|---|
| `site/` | Complete deployable source; landing, About, Privacy, local hero assets and shared CSS |
| [Design](docs/design.md) | Routes, composition, styling and progressive navigation |
| [Content](docs/content.md) | Product truth, availability, contributor/contact editing and legal text |
| [Media](docs/media.md) | Optional accessible player configuration (WEB-04) |
| [Provenance](docs/provenance.md) | Image, branding, screenshot and media rights/review |
| [Testing](docs/testing.md) | Offline checks, browser runner and manual gates |
| [Web todos](docs/todos.md) | Owner-requested follow-ups after Web development is complete |
| [Deployment](docs/deployment.md) | Source mirror, approved-artifact publication, DNS/HTTPS and rollback |
| `tests/` | Standard-library static checks and dependency-free browser runner |
| `image-ref/` | Owner reference material, never deployable |

## Local verification

From the monorepo root (in the standalone mirror, omit the `web/` prefix; the root doc-link
checker remains monorepo-only):

```sh
python3 -m unittest discover -s web/tests -p 'test_*.py'
python3 web/tests/audit.py
python3 scripts/check-doc-links.py
python3 web/tools/preview.py
```

Open `http://127.0.0.1:8765/site/` and `http://127.0.0.1:8765/tests/browser.html`.
The preview disables caching. For a phone on the same Wi-Fi, run
`python3 web/tools/preview.py --lan` and open `http://<computer-Wi-Fi-IP>:8765/` on the phone;
LAN mode serves only website files. Details and the required Guest/sandbox policy are in
[testing](docs/testing.md#reliable-local-preview-and-phone-inspection).
The audit reports target-quality gaps independently of the current regression gate; exit 1 is an
unresolved finding, not a passing release. See the handoff for actual evidence.

Live hosting is verified in the [WEB-07 handoff](docs/handoff.md#web-07-deployed-site-verification);
Play availability remains unverified. Keep the exact case-sensitive
`About.html` and `privacy-policy.html` routes. App privacy disclosures must remain aligned with
[privacy principles](../docs/security/privacy.md) and Android's policy; website-only disclosures are
separate. No deployment, DNS or external publication is part of WEB-01.

## Public source synchronization

Keep development here; synchronize committed Web files with
`git subtree push --prefix=web webgithub main`. The Web-only remote is
`git@github.com:lpoli/gohealax-web.git`. Source includes documentation/tests/references; Pages hosts
only `.release/site/`. Deployment is manually triggered with the approved manifest hash. See
[deployment](docs/deployment.md) for preflight, standalone validation, domain transfer and rollback.
Monorepo requirement links in these documents refer to the private source of truth and are not
available in the standalone mirror; tests use a derived disclaimer fixture checked in the monorepo.
