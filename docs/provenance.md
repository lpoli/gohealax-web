# Website asset provenance

WEB-01 added no public assets. WEB-02 selections and pending approvals are recorded below. Record every photo, poster, icon,
screenshot, video and social image here before publication. Required licence notices belong inside
`site/`; this working register and reference files do not.

| Candidate | Source / current evidence | Rights and review | Public use |
|---|---|---|---|
| Layout reference | Owner-supplied `web/image-ref/web-design-layout.png`, inspected 2026-10-12 | Layout reference only; redistribution rights unknown | Excluded; never extract imagery or app screens |
| Existing branding | [Branding register](../../design/branding/README.md) | Author/distribution rights unrecorded | Launch blocked until confirmation; do not mark approved |
| Native screenshots | [Screen register](../../design/screens/README.md), `design/screens/manifest.json` | Must inspect revision, synthetic data and obsolete paid/locked UI | No screenshot selected yet |
| Hero photo | Mikhail Nilov / Pexels 7500034; details below | Pexels licence reviewed; owner approval pending | Local layout candidate |
| Demo poster | Not selected | Review due WEB-04 if needed | No public asset |

For every selected asset record:

- Deployable path, original source URL/file, creator and acquisition date.
- Exact licence/version and licence URL or written permission; required attribution and where it
  appears in the exported site. “Found online” is not a licence.
- Original and delivered SHA-256, dimensions, derivatives/crops/compression and who made them.
- Owner approval, date and scope of publication rights; any unresolved restrictions.
- For screenshots: exact Android commit/version, capture source, synthetic fixture identity and
  provenance, visual review date, caption and confirmation of no personal data or paid/locked UI.
- For video: source/revision, speech review, captions/transcript paths or provider evidence and
  accessibility reviewer/date. See [media.md](media.md).

Keep an original asset when its licence permits, outside the deployable source if it is only a
working reference. Do not publish a licence notice that falsely claims ownership. Missing branding
rights remain a release blocker even if local mockups use the existing artwork. New original artwork
must also have its authorship and publication permission recorded.

## WEB-02 selected assets (2026-10-12)

### Hero photo

- Creator: Mikhail Nilov. Source: [Pexels photo 7500034](https://www.pexels.com/photo/photo-of-a-woman-stretching-on-a-yoga-mat-7500034/).
  Acquired 2026-10-12 from `https://images.pexels.com/photos/7500034/pexels-photo-7500034.jpeg`.
- Licence: [Pexels License](https://www.pexels.com/license/), unnumbered web licence,
  reviewed 2026-10-12. Permits free website use and modification; attribution optional.
  Restrictions include no implied endorsement, offensive depiction, stock redistribution or use
  as a trademark. This is illustrative exercise imagery, not a patient, contributor or endorsement.
- Original retained in `web/asset-sources/pexels-7500034.jpg` (outside deployable source), 4000×6000.
  SHA-256: `990186f448b93e93d3a497853f6b4b648c0912def721a9d72c58d38b310bb1bf`.
- Agent-produced derivatives: Pillow LANCZOS resize, WebP quality 82, no retouching. CSS crops the
  displayed image using `object-fit: cover` and `object-position: 50% 85%`; the files retain the
  full frame. Responsive dimensions and hashes:

| Deployable path | Dimensions | SHA-256 |
|---|---|---|
| `site/assets/hero-480.webp` | 480×720 | `a6a35a613d5c115b721deb5182449c9cb074df4afca3f9e9e3213e7138ac25ac` |
| `site/assets/hero-800.webp` | 800×1200 | `cb4d79e98cc376b5e6deda65db7c8ae1bcca88c66debcb0db6804a7f4143f4b2` |
| `site/assets/hero-1200.webp` | 1200×1800 | `649bcf818f67916e6c8e5db6dcfe060fc60167f988a2d94c70802f6b004c862d` |

Credit and licence links appear in the landing footer; a hero caption disclaims endorsement.
Owner layout/imagery approval: **pending**, no date or publication approval inferred.

### Original branding and decoration

`site/index.html` and `site/site.css` contain a new text wordmark, CSS circle with a system-font
lowercase “g”, and two original SVG wave paths. Created by the coding agent in this repository on
2026-10-12; no existing branding, reference pixels or third-party icon paths copied. System fonts
only; no font files distributed. These inline/CSS assets have no separate bitmap dimensions or
file hashes. Owner acceptance and publication permission for this new artwork remain **pending**.
No native screenshot or demo poster selected. Existing branding rights remain unresolved if that
artwork is chosen later; it is not used in this landing page.
