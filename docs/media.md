# Optional media contract

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

## Implementation and editing

`site/media.js` exports `mediaConfiguration`, `initMedia` and the native `createPlayer` adapter.
Initialization reuses one promise per element and checks local asset existence with same-origin HEAD
requests only for a complete reviewed candidate. Disabled/invalid candidates create no control or
player; the current disabled demo performs no probes. HEAD checks establish file availability, not
media quality or rights. Player creation and video body/YouTube requests require explicit Play.

Failures and a 12-second player timeout expose Retry, retain the description and remove the failed
player. Local video retains an explicit direct-file link; YouTube retains an explicit watch link. Late callbacks cannot revive a failed
attempt. YouTube iframe load clears the loading timer but explicitly does not claim playback success;
the description and fallback remain visible for a blocked embed. Native video and caption errors
use the same fallback. Current native caption labels are English; review an English WebVTT file or
extend the language contract before configuring other languages.

To enable a future demo, review the exact assets and record rights/accessibility evidence in
[provenance](provenance.md), update the HTML attributes and placeholder copy in `site/index.html`,
then review [Privacy](../site/privacy-policy.html) and run the browser/manual gates. No reviewed
video or captions are supplied now. The local poster reuses the WEB-03 running-timer screenshot;
no new asset or permission claim is introduced.
