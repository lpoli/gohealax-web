# Website design contract

## Structure and reference

The owner-supplied `web/image-ref/web-design-layout.png` is a composition reference only, inspected
2026-10-12. It is not a licensed source of photos, branding or app screens and is never exported.
Its presentation heading (“3. Clean & Professional”) is not site content.

Landing order: navigation → photographic hero → benefits → demo → mission → features → download →
Team → Contact → wave footer. Team and Contact are additions to the reference. Use calm teal/green,
light mint surfaces, readable dark text, generous spacing and restrained rounded controls. Replace
recovery promises with factual exercise-support language from [content.md](content.md).

Use a 72rem content maximum, readable legal columns (about 65ch), and breakpoints at 48rem and 64rem.
Use system fonts, relative text sizes and content-driven section heights. Respect browser text sizing
and zoom. Stack at narrow widths; test 320–1440px and portrait/landscape. Decorative waves are local
CSS or original SVG with no accessible name. Never use fixed section heights that clip enlarged text.

## File and route contract

`web/site/` is the entire public source. Keep shared header/footer markup directly in the small set
of pages and test destination consistency. No runtime includes or templates. CSS sections: tokens,
base styles, layout, components, responsive overrides. Scope landing styles under a landing-specific
class so legal-page layout remains readable.

| URL | Role | Canonical |
|---|---|---|
| `/` | Landing page; replace the existing redirect in WEB-02 | `https://gohealax.com/` |
| `/About.html` | Standalone product explanation | `https://gohealax.com/About.html` |
| `/privacy-policy.html` | App policy and separate website disclosure | `https://gohealax.com/privacy-policy.html` |
| `/medical-disclaimer.html` | PROD-01 disclaimer with factual context | `https://gohealax.com/medical-disclaimer.html` |
| `/404.html` | Helpful missing-page navigation, noindex, excluded from sitemap | None |

Use document-relative links/assets on ordinary pages; cross-page section links use
`index.html#features`, `index.html#demo`, `index.html#mission`, `index.html#download`,
`index.html#team`, and `index.html#contact`. Provide `#home` for the top. Preserve the case of
`About.html`. The 404 uses root-relative links/assets, checked with the export at origin root and
with its content returned for an unknown nested URL. Each indexable page has a unique title,
description and absolute canonical. Add sitemap, robots rules and social metadata in WEB-05.

## Progressive navigation

HTML starts with visible native navigation links. WEB-02 must work without JavaScript. In WEB-04,
`site.js` exposes an idempotent initialization function; it reveals a real disclosure button and
collapses mobile navigation only after setup succeeds. Use `aria-expanded` and `aria-controls`,
native Tab order, no application-menu roles, no focus trap. Escape closes and focuses the button;
link activation closes without cancelling navigation. On resize, never hide the focused element
without moving focus to an appropriate visible control. Desktop navigation remains visible.

Basis: [WAI disclosure navigation guidance](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/),
reviewed 2026-10-12. Test our implementation and assistive-technology behavior; do not copy the example
as production code.

## Imagery

Use a self-hosted licensed hero photo, original branding and approved current screenshots. Keep
subjects and important content visible when crops change. Define responsive sources, explicit
dimensions, useful alt text (empty for decoration), eager hero loading and lazy below-fold loading.
Record originals, crop/resize changes and rights in [provenance.md](provenance.md). No remote fonts,
remote thumbnails, stock-photo hotlinks, analytics or initial third-party requests.
