# Website roadmap

The owner supplied the revised seven-milestone plan on 2026-10-12. This file alone owns Web milestone
status. Acceptance details live in the linked milestone files; evidence and blockers live in
[handoff.md](handoff.md). The informational website is governed by
[ADR-0008](../../docs/decisions/0008-static-informational-website.md).

| Milestone | Deliverable | Status | Owner approval |
|---|---|---|---|
| [WEB-01](milestones/WEB-01.md) | Foundation, complete milestone documentation and baseline checks | Complete | Approved 2026-10-12; see [handoff](handoff.md#owner-review-and-next-action) |
| [WEB-02](milestones/WEB-02.md) | Responsive landing-page layout and licensed imagery | Complete | Approved 2026-10-12; see [handoff](handoff.md#web-03-startup-and-verification). Unrun manual checks remain recorded |
| [WEB-03](milestones/WEB-03.md) | Product content, About and reviewed screenshots | Awaiting approval | Pending: owner wording/gallery/editing-location review; see [handoff](handoff.md#web-03-startup-and-verification) |
| [WEB-04](milestones/WEB-04.md) | Disclosure navigation, optional media and legal pages | Not started | Pending |
| [WEB-05](milestones/WEB-05.md) | Accessibility, performance, metadata and 404 | Not started | Pending |
| [WEB-06](milestones/WEB-06.md) | Deterministic export and release preparation | Not started | Pending |
| [WEB-07](milestones/WEB-07.md) | Owner publication and verified launch | Not started | Pending |

## Gate rules

`Not started → In progress → Awaiting approval → Complete`. Blockers are recorded separately and
do not introduce another status. A milestone reaches Awaiting approval after its implementation and
available verification have been recorded, including any verification limitations. Only explicit owner
approval of the concrete deliverable can make it Complete. Record the approval date and evidence in
this table and the handoff. Failed acceptance items must be resolved or explicitly decided by the
owner; successful automated checks alone cannot approve a milestone.

“Start Next task” selects the lowest incomplete milestone whose predecessor is approved. If it is
Awaiting approval, present its review evidence and wait; do not silently mark it Complete or start
its successor. The first implementation session ends after WEB-01. Later sessions follow the same
one-milestone gate unless the owner explicitly changes the scope.

## Document ownership

- [Web todos](todos.md): deferred owner-requested follow-ups after Web development.
- [Design](design.md): page sequence, layout, responsive behavior and navigation.
- [Content](content.md): product copy, availability, contact and legal disclosures.
- [Media](media.md): optional-player configuration and accessibility contract.
- [Provenance](provenance.md): photo, branding and screenshot review records.
- [Testing](testing.md): executable gates, coverage growth and manual evidence.
- [Deployment](deployment.md): export boundary, publication, DNS, HTTPS and rollback.
- Root [roadmap](../../ROADMAP.md) and [tasks](../../tasks/active.md) summarize and link here.
