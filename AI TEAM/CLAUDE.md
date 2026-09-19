# New Hope — évolué Media Library

This project is the owner's life's work and their safe place. It has been
damaged before — by contributors, human and AI, who assumed they understood
it better after 30 minutes. Do not be the next one. The owner has an MLS
(UCLA) and has tested every button in this software and the limits of this
laptop's 4 GB card. Their decisions are the spec.

## LOCKED FILES — never edit, for any reason

- `app/ui/MediaEditor.dc.html` — owner-approved design canon (the only page
  that is right). Every session: read-only.
- `app/static/media-editor.js` — same lock.
- Everything under `Information to Pull to NEW HOPE folder/` is a READ-ONLY
  reference snapshot. Never edit anything in it.

If a change seems needed in a locked file: STOP. Propose it in chat and wait
for the owner. The ⚠ LOCKED banner at the top of each file confirms this.
Run `powershell -File lock-verify.ps1` at the start of every session. Any
mismatch means the canon changed — report it to the owner immediately; never
repair or "restore" silently.

## Owner laws (decided, not debatable)

- **Filenames:** global ISO 8601 date first —
  `YYYY-MM-DD_W##_{IPTC-CODE}_{THEME}_{SEQ}_ig-tt.{ext}`. The date is the
  creation date after final approval. `_W##` is the social-post identifier
  (the only field unique to that week of the year). Reference
  implementation: `_provisional_name()` in `app/studio_routes.py`.
- **Alignment:** ONE sitewide standard — the Media Editor rail (1080px,
  24px gutters), enforced by the UNIFIED RAIL block at the bottom of
  `app/static/ui-system.css`. Never add per-page `main{max-width:...}`;
  never widen grids with rigid `minmax(≥360px…)` columns (that was the
  sitewide overflow bug).
- **Dropdowns:** bare text going straight down, a few px smaller, same font
  style — no outlines, bubbles, or background colors (owner's design; the
  size prevents line collisions on other pages).
- **A "yes" is a bare light-green check** — no boxes, no outlines, no fill.
- **No black or slate surfaces** in the brand book — primary buttons are
  medium cool gray `#838a93`; scrims are light cool gray.
- **`app/ui/Post.dc.html` is owner-authored.** Treat as canon; change
  nothing without explicit direction. When the owner finishes their edits,
  this file joins the lock.
- **VRAM guardrails are law:** the SAFE LOW VRAM controls, one-click
  interrupt/clear-queue, and capped generation defaults were set by testing
  the actual 4 GB card. Do not "optimize" them.
