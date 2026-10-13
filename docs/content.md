# Website content contract

Authority: [product requirements](../../docs/product/requirements.md),
[Android free decision](../../docs/decisions/0007-android-is-completely-free.md), and
[privacy principles](../../docs/security/privacy.md). Describe current Android behavior. The
website does not implement a native timer or imply clinical outcomes.

## Page copy and editing locations

| Area | Required message | Editing location after implementation |
|---|---|---|
| Hero/benefits | Time and track user-chosen exercises and routines | `site/index.html`, `#home` and benefits section |
| Demo | “Demo coming soon” until accessible media is approved | `site/index.html#demo`; configuration in [media.md](media.md) |
| Mission | GoHealaX means “Go heal and relax”; support following a routine, no recovery promise | `site/index.html#mission`, `site/About.html` |
| Features | Prepare, Hold, Relax; repetitions, sets, Count Pace, presets, daily planning, schedules, history and recorded activity; focus on exercise rather than mental counting | `site/index.html#features`, `site/About.html` |
| Download | “All current Android features are free”; “Android download link coming soon”; iOS “Coming Soon” | `site/index.html#download` and hero availability copy |
| Team | Honest contributor placeholder; no invented names, credentials or endorsements | `site/index.html#team`, with a source comment marking contributor edits |
| Contact | `mailto:b.lp.self@gmail.com` with readable email address | `site/index.html#contact`, About and Privacy |
| Social | Omit links until real destinations are supplied and verified | Footer source comment marking future social edits |

Count Pace is seconds per count; counts equal seconds only at pace 1.0. Schedules add items to daily
planning; do not promise closed-app reminders. History and statistics show recorded activity, not
recovery measurements. Users create their own exercises; no catalogue, supplied exercise plan or
medical advice. Captions on synthetic screenshots say “Example exercise data, not an exercise
prescription.” Do not show obsolete purchase controls or locked-feature screens.

Owner wording decision (2026-10-12): the product is an actual release, not a pilot. Do not use
“pilot release” in public copy. State that GoHealaX tracks exercises/routines and include:
“User can totally focus on exercise rather than mental counting.” This describes the purpose of
timer cues; it does not claim a clinical outcome.

The actual Google Play listing has not been verified. Until it is, do not claim availability, invent
a store URL or make a store badge/action appear enabled. A navigation link may go to the download
section. iOS availability is Coming Soon; do not decide its unresolved pricing policy here.

## Legal copy

About, Privacy and Medical Disclaimer include this exact PROD-01 text (ordinary HTML
paragraphs, readable without scripting):

> GoHealaX does not diagnose, treat, cure, or prevent any condition. Configurable timings are tools,
> not universally optimal treatment. Consult a qualified healthcare professional about your exercise
> programme.

Preserve the current Android disclosures when revising Privacy: private on-device exercise settings,
plans, schedules, history, completed-duration events, adherence and preferences; no accounts, ads,
analytics or automatic exercise-data transfer; no purchases/store connection for current Android
features; user-selected document providers; foreground notifications and lock-screen settings;
retention/deletion; disabled Android automatic cloud backup and device transfer; readable unencrypted
JSON exports that can outlive uninstall; confirmed replacement on restore; excluded permissions,
active timers, loaded setup and drafts; and contact information. Compare against
[current Privacy](../site/privacy-policy.html) and [Android policy](../../android/docs/privacy-policy.md).
Website-only changes do not change native data handling.

Separate app privacy from website hosting and optional media. There are no developer-added analytics,
forms, cookies/persistence or service worker. Email uses the visitor's provider. State the actual
hosting operator and applicable policy only after verification. The existing sentence naming GitHub
Pages is not evidence of a deployment. Explain any enabled player, the explicit activation boundary,
and its third-party requests; privacy-enhanced YouTube does not mean no data exchange. The default
disabled demo sends no media requests. Re-review disclosures if that configuration changes.

Missing contributor, social, Play and video details permit these honest placeholders. Unconfirmed
publication rights, repository access and DNS authority block launch, not local development.
