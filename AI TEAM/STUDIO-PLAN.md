# Studio Page — One-Page Build Plan

Updated: 2026-09-12 · Owner-approved structure from the structural review.
The Studio is a **gating workbench**: gathered images/videos land here, the owner
keeps 0–9 per batch, everything else never touches the Library.

## 1. Data model (new `studio_candidates` table — no new cataloging engine)

| column | purpose |
|---|---|
| id, created_at | identity |
| batch_id (str) | drop-session grouping ("b20260912-0833") |
| media_kind | image / video / audio (auto-detected) |
| storage_key, checksum, width, height, duration_s | full file stays in storage (disk/Azure), never in the DB |
| poster_key, strip_key | poster JPEG + 3-frame strip (worker-generated, ~320px) |
| status | `new` → `chosen` → `discarded` → `trashed` |
| tile_number | 1–9 (owner-assigned post slot; NULL = unassigned) |
| proposed_filename | ISO 8601 name, composed at drop, live-updates when tile assigned, final at commit |
| note | one optional owner note |

**Naming timing (owner decision, 2026-09-12): name as early as possible.**
Drop form carries Week No. + Theme (pre-filled from the calendar's current week), so the
ISO name exists the moment a file lands — with the tile slot blank. Assigning tile 1–9
during choosing fills the sequence in live; commit uses the name as-is (no naming step
at the end); dismissal kills the name with the row. Date-first ISO part is immutable
after commit, per CLAUDE.md — early composition means it is born correct, never renamed.

Checksum-deduped on insert (reuse `create_media_asset` dedupe rules) — re-drops cost nothing.
Dismissed rows are **never** Library rows; they die in `studio_candidates` and only the
files go to Trash on commit.

## 2. Endpoints (all under `/studio`, owner-auth)

- `POST /studio/drop` — multi-file upload (multipart, per-file progress, ≤3 parallel, warn >150 MB)
- `GET  /studio/candidates?batch=&status=&page=` — proof-grid rows (metadata + poster URLs only)
- `POST /studio/decide` — batch {candidate_ids → tile_number | dismiss | restore}
- `POST /studio/thumbnails/run` — (worker) generate missing posters/strips, ffmpeg one-at-a-time
- `POST /studio/commit` — chosen → real Library assets via `create_media_asset` → Library Review
  (cataloger queue), filenames = ISO `YYYY-MM-DD_W##_THEME_SEQ##_VERTICAL.ext`, platform `IG-TT`
- `POST /studio/empty-discards` — discard tray → Trash (files deleted, rows → `trashed`)
- `GET  /studio/batches` — batch list with counts (new/chosen/discarded)

## 2b. Container & commit flow (owner decision, 2026-09-13 — Azure: godzilla1126)

Two blob containers: **bunbuns** = cataloged Library assets. **ephemera** = ALL scout
searches + Studio candidates (true to its name — holds things while you decide).

- Drop/search → candidates land in **ephemera** with a light provisional name:
  `YYYY_W##_IPTC-subject-codes_SEQUENCE` (sequence is the load-bearing part —
  everything else is identical for the week).
- **Commit to selections** is the moment full metadata happens:
  - Chosen originals get full metadata + their own **UUID**, land in **bunbuns**,
    and queue with the **Cataloger**.
  - Derivatives queue with the **Media Editor** — they do NOT populate or
    categorize until the Media Editor finishes, the owner approves, and SAVE is
    pressed (that is why the filename format/example lives on the Media Editor
    page). On save they receive full metadata + UUID, linked to the original.
- Unpicked ephemera candidates expire naturally — ephemera never feeds the
  Library directly.
- Azure **Cosmos DB** is a good fit for the scout-candidate docs (write-heavy
  JSON, TTL for ephemera); the read-only Azure SQL in .env is the reporting
  mirror. Wire Cosmos as the ephemera store when the Studio build starts.

## 3. Screen spec (matches the évolué design language)

- **Drop zone** — top strip: drag-drop + file picker, per-file progress bars, dedupe notices ("already staged — reused").
- **Proof grid (left)** — 100 tiles/page (paginated), tiles are `<img>` posters only — **no `<video>` tags in the grid**. Tile shows: poster + 3-frame strip, media-type chip, tile-number badge, status border (UNSEEN grey / CHOSEN green / DISMISSED rose).
- **Loupe (right, fixed size)** — selected tile large: video plays muted+loop with scrubber (one decoder at a time), image zooms. Keep buttons: `1–9` assign, `0` dismiss, `Z` undo, `Space` play, `E` enlarge.
- **Header commit bar (always visible)** — "7 chosen · 2 discarded · 18 left" + `Send chosen to Library Review` + `Empty Discards`.
- **Discard tray** — bottom strip of last N dismissed with `↩ Restore` per tile; `Empty Discards` commits to Trash in one batch. Undo = `Z` pops the last one back.
- **Keyboard map** — `←/→/↑/↓` navigate · `Space` play · `E` enlarge · `1–9` tile · `0` dismiss · `Z` undo · `Enter` commit chosen · `Shift+1..0` batch-assign.

## 4. Naming + handoff (reuses everything that already exists)

- `proposed_filename` composes at drop (Week + Theme from the pre-filled drop form;
  tile slot blank) and live-updates the instant a tile 1–9 is assigned — no naming
  step exists in the flow. Commit uses the name as-is into `create_media_asset`
  (dedupe, kind detect, storage) → straight into the existing **Library Review**
  queue → cataloger. Trash path = existing trash, no Library rows ever.
- Drop form fields: Week No. (pre-filled from calendar), Theme (pre-filled),
  optional note. That is all the owner types — ever.

## 5. Performance guards (mostly-video reality, 4 GB PC)

1. Grid = posters only; video decode only in the loupe, one file at a time.
2. Posters/strips generated by background worker (existing `worker/` pattern), never in-request.
3. Paginate grid (100/page); virtual-scroll later if needed.
4. Uploads ≤3 parallel with per-file progress; chunked is a v2 need, plain multipart first.
5. Videos >150 MB: warn, still allow. No video bytes in SQLite — storage keys only.

## 6. Build order

1. Table + drop endpoint + dedupe (staging works)
2. Worker poster/strip generation
3. Proof grid + loupe + keyboard decisions + discard tray
4. Commit → Library Review with ISO names; empty-discards → Trash
5. Polish: batch counters, dedupe toasts, design pass to match the évolué look
