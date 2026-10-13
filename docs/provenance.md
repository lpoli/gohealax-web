# Website asset provenance

WEB-01 added no public assets. WEB-02 selections and pending approvals are recorded below. Record every photo, poster, icon,
screenshot, video and social image here before publication. Required licence notices belong inside
`site/`; this working register and reference files do not.

| Candidate | Source / current evidence | Rights and review | Public use |
|---|---|---|---|
| Layout reference | Owner-supplied `web/image-ref/web-design-layout.png`, inspected 2026-10-12 | Layout reference only; redistribution rights unknown | Excluded; never extract imagery or app screens |
| Existing branding | [Branding register](../../design/branding/README.md) | Author/distribution rights unrecorded | Launch blocked until confirmation; do not mark approved |
| Native screenshots | [Screen register](../../design/screens/README.md), `design/screens/manifest.json` | Must inspect revision, synthetic data and obsolete paid/locked UI | No screenshot selected yet |
| Hero photo | Mikhail Nilov / Pexels 7500034; details below | Pexels licence reviewed; owner approved 2026-10-12 | Local layout asset |
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
Owner layout/imagery approval: **approved 2026-10-12**, by explicit WEB-02 approval.
This is local deliverable acceptance; publication remains gated on WEB-07.

### Original branding and decoration

`site/index.html` and `site/site.css` contain a new text wordmark, CSS circle with a system-font
lowercase “g”, and two original SVG wave paths. Created by the coding agent in this repository on
2026-10-12; no existing branding, reference pixels or third-party icon paths copied. System fonts
only; no font files distributed. These inline/CSS assets have no separate bitmap dimensions or
file hashes. Owner acceptance of the local artwork: **approved 2026-10-12**, with WEB-02.
External publication remains gated on WEB-07.
No native screenshot or demo poster selected. Existing branding rights remain unresolved if that
artwork is chosen later; it is not used in this landing page.

## WEB-03 screenshot review (2026-10-12)

The owner supplied five app screenshots in `web/image-ref/screenshots/` for website use. The agent
visually inspected all five at full supplied resolution. No identifying personal data, obsolete
purchases or feature locks are visible. `running-timer-2.png` actually shows the Ready/Idle state;
it remains an unused original to avoid duplicating the timer view. No owner originals were changed.

Four selected PNGs are copied byte-for-byte into `site/assets/screenshots/`. No generated UI,
compositing, retouching, cropping, resizing or compression was applied. Each has dimensions 359×801;
CSS scales proportionally without cropping. They use lazy loading, useful alt text and the caption
“Example exercise data, not an exercise prescription.” The landing feature section owns the gallery;
About links to it. The exact paths, original/delivered hashes, timestamps and review evidence are in
`web/asset-sources/screenshots.json` (outside the deployable source).

Capture/build evidence:

- Owner-reported revision: current commit `6c08b133dd2079f7899c7ac8b6946a7656aa503d`;
  Web development does not alter Android. Latest app change in that tree:
  `3f1f0f7f5002ded98bfd7415771f93ace521c49a` (FREE-2). Repository-declared version 1.2/code 3;
  installed APK identity was not independently inspected.
- Owner confirmed exercises/activity came from the generated inspection fixture,
  `android/gohealax-inspection-backup.json`. Current repository SHA-256:
  `5757fe13f279e42926e548a819a85cb696ca7450377084cc93b88add9421a610`.
  This is owner-supplied synthetic data, not a supplied exercise prescription.
- PNG metadata identifies `gnome-screenshot`, with capture times on 2026-10-12 between
  20:53:52 and 20:55:19, timezone +05:45. These are owner-supplied screen/window captures,
  not claimed to be raw Android `screencap` output. The visible thin window edges are preserved.
- Android 17 is the owner's tentative OS recollection, not independently verified; it is not the
  app version. No new native capture or device test was run by the agent.
- Local website use is authorized by the owner's submission in this task. Final gallery acceptance
  was granted with explicit WEB-03 approval on 2026-10-13; external publication remains gated on WEB-07. No blanket ownership
  or publication-rights claim is inferred for native branding.

| Delivered filename | Original = delivered SHA-256 |
|---|---|
| `running-timer-1.png` | `08b13126fa85af644ecd7da0f25d239bbce567a55f71079c6cc5e77d3fa87719` |
| `preset.png` | `3f3298c9b50ffe705c801e210f3b0f9dd9d244ff8e1be3665cf1b1667b54afcd` |
| `todays-exercises.png` | `7f92c89cac8cb064173a793c3589c1ed6797ea996efcac32e6a734d95f66acbe` |
| `statistics.png` | `52b9ad307423722325aeeb8f75d8007e2fb6b7c64a2cbc11cad356cc45826dba` |

Agent inspection of the rendered gallery: Chrome 154.0.8037.92 on Linux at 375×1400 and 1440×1400;
stacked mobile and four-column desktop layouts, uncropped images and readable captions. All four
images decoded at both widths with no horizontal overflow. Evidence is in the Web handoff.

Older candidate review retained: `design/screens/presets-populated.png` was inspected but not
selected because revision `599b377d0128fd15f233228ca54a184649a439ad` predates the free transition.
`android/docs/play-listing/screenshots/presets.png` was inspected but not selected because its
older layout lacks exact capture/fixture provenance. Simulated layout-reference app screens and
locked/purchase screens remain excluded.

## WEB-04 demo assets

The disabled demo uses the existing byte-identical `running-timer-1.png` from the WEB-03 register
as its local poster, with an example-data caption. No video, captions, remote thumbnail or new
bitmap is supplied or enabled. Media review attributes remain absent; future activation requires
revision-specific video/caption/transcript rights and accessibility evidence here.

## WEB-05 original quality assets (2026-10-13)

Created by the coding agent in this repository for local website use. No native branding, reference
pixels, photos or third-party icon paths used. The favicon is an original geometric circle/stem mark
on teal; the PNG fallback and touch icon draw the same geometry with Pillow 12.2.0. The 1200×630
social card uses original teal/mint geometry and factual GoHealaX copy. Text rasterized from the
host's DejaVu Sans; licence evidence inspected in `/usr/share/doc/fonts-dejavu-core/copyright`
(Bitstream Vera licence; DejaVu changes public domain). No font software is distributed or requested.
Sources are simple SVG geometry and Pillow drawing, with no external image source/licence requirement.
Generated on 2026-10-13; output dimensions/hashes below. Owner acceptance was recorded with WEB-05
on 2026-10-13; external publication remains gated on WEB-07. No inference about native branding
rights is made. No attribution is required for the original geometry; font files are not shipped.

| Deployable asset | Dimensions | SHA-256 |
|---|---|---|
| `site/assets/favicon.svg` | 64×64 viewBox | `fbb78387a2173375d9dc1ffdb2289ab3a07fd6ec87c6cb37173462f6154f54d8` |
| `site/assets/favicon.png` | 32×32 | `18f48b7d3046e04012fdea0b9034a5b6fa37d84a06ec5a625ab05dd56063a33d` |
| `site/assets/apple-touch-icon.png` | 180×180 | `d8d4e3d6773b195127893028d9e4529dd0f118ba32cfe73b136962d1644c341f` |
| `site/assets/social.png` | 1200×630 | `08a8e944fc0b5fb1bf4fe68d341ea700d1ae5998f33f28551f4c00554c2303d5` |

The social image uses intended absolute production URLs in metadata; this does not establish
hosting or launch. Existing hero and screenshot bytes and provenance remain unchanged.
