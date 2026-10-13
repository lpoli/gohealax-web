# Web working instructions

Follow the repository bootstrap and [README](README.md). Before changes, read the
[roadmap](docs/roadmap.md), selected milestone, [handoff](docs/handoff.md), and relevant guides.

- `site/` is the complete deployable source: vanilla HTML, CSS and JavaScript, no dependencies or
  build step. Tests and documentation live outside it.
- Follow the seven owner approval gates. “Start Next task” selects the lowest incomplete milestone
  whose predecessor is approved. Pending approval is never implicit approval.
- Keep essential content and links in HTML, including when JavaScript fails. Preserve exact route
  case. Follow the design, content, privacy and media contracts in the guides.
- Never copy reference imagery or simulated app screens into the site. Record asset provenance and
  rights before publication. Do not modify or stage owner reference files incidentally.
- Run the offline suite and documentation link checker. Browser evidence is separate; record browser,
  version, environment and result, distinguishing agent-run from user-run checks and unrun checks.
- Owner browser-isolation rule (2026-10-13): every automated/headless Chrome launch uses
  `--guest` plus a freshly created `--user-data-dir` under `web/.artifacts/`. Never use the owner's
  normal profile, reuse an earlier automation profile, or attach to an existing personal browser.
  Keep Chromium's sandbox enabled: never use `--no-sandbox`, `--disable-setuid-sandbox` or equivalent
  bypasses. Respect the tool execution sandbox too; any needed escalation must obtain explicit tool
  approval and explain its scope. Guest/profile isolation does not replace process sandboxing.
- Keep temporary files, browser profiles, reports and export output inside this working directory.
  `web/.artifacts/` and `web/.release/` are ignored. This task-specific rule takes precedence over
  the repository's general advice to put build output elsewhere. Avoid native builds for Web-only work.
- Update the Web handoff and root task summary. Status belongs only in the Web roadmap; milestone
  files own acceptance details. Stop for owner inspection after each milestone. Do not publish or
  change DNS before WEB-07 and explicit delegation; owner publication is the default.
