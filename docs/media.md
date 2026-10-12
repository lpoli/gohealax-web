# Optional media contract (implementation in WEB-04)

Keep navigation in `site.js` and playback in a separate `media.js` ES module. No player is created
before a visitor explicitly activates Play. Initialization must be idempotent. Essential demo
description, local poster and fallback remain in HTML. Default mode is disabled with the text
“Demo coming soon” and no actionable play control.

The demo element owns configuration through these attributes; do not maintain a second JS settings
object in the production source:

| Attribute | Meaning |
|---|---|
| `data-media-provider` | `disabled` (default), `youtube`, or `self-hosted` |
| `data-media-id` | YouTube video identifier, only accepted in YouTube mode |
| `data-media-src` | Document-relative same-origin video path, only for self-hosted mode |
| `data-media-poster` | Document-relative local poster image; never a remote thumbnail |
| `data-media-description-id` | ID of an existing visible transcript or equivalent description |
| `data-media-accessibility-reviewed` | Literal `true` only after review of this exact media revision |
| `data-media-has-speech` | Explicit `true` or `false` after review |
| `data-media-captions-src` | Local WebVTT captions for spoken self-hosted content |
| `data-media-captions-reviewed` | `true` after captions are verified; mandatory for spoken YouTube content |

Validate configuration before enabling a control: reject unknown modes, malformed IDs, remote or
missing local sources, absent descriptions, missing review or required captions. HTML review markers
record a human decision, not proof from an automated test. Add evidence in provenance for the exact
video/captions/transcript revision. Invalid/incomplete configuration preserves the disabled placeholder.

For YouTube, construct a privacy-enhanced `https://www.youtube-nocookie.com/embed/` player only after
activation, with a descriptive iframe title. Never fetch a remote thumbnail, iframe, script,
preconnect or DNS hint on initial load. For local video use native controls, no autoplay before
activation, appropriate captions and no initial video download. Keep visible fallback copy and an
accessible retry or explicit direct-media link on failure; iframe load alone does not prove successful
YouTube playback. A blocked player must not erase the transcript/fallback.

Tests inject controlled player adapters into the production module so they never contact YouTube.
Cover missing/invalid configuration, all providers, duplicate initialization/activation, no player
before click, captions, blocked playback, error and timeout fallback. Real-page Network inspection is
a separate gate; adapter tests do not prove it. Record approved changes to these attributes here when
implementation reveals a necessary refinement.
