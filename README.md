# GoHealaX website

Responsive informational website, developed in the monorepo and eventually published separately
through GitHub Pages. Plain HTML, CSS and JavaScript; no framework, package manager or build step.
Decision: [ADR-0008](../docs/decisions/0008-static-informational-website.md).

Start with [Web instructions](AGENTS.md), [roadmap](docs/roadmap.md) and [handoff](docs/handoff.md).
The roadmap owns the seven approval gates. WEB-02 replaces the homepage redirect with an owner-approved responsive landing page. WEB-03
product/About copy and screenshot gallery were approved on 2026-10-13. WEB-04 navigation, media
support and legal pages and WEB-05 quality were approved on 2026-10-13. WEB-06 export preparation is next. Later
increments follow the roadmap gates.

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
| [Deployment](docs/deployment.md) | Planned deterministic export, publication, DNS/HTTPS and rollback |
| `tests/` | Standard-library static checks and dependency-free browser runner |
| `image-ref/` | Owner reference material, never deployable |

## Local verification

From the repository root:

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

The repository does not verify current hosting or Play availability. Keep the exact case-sensitive
`About.html` and `privacy-policy.html` routes. App privacy disclosures must remain aligned with
[privacy principles](../docs/security/privacy.md) and Android's policy; website-only disclosures are
separate. No deployment, DNS or external publication is part of WEB-01.
