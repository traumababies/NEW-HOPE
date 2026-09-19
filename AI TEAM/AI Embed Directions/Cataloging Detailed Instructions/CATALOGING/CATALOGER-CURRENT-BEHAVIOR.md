# What the Cataloger Does Today — Current Behavior (for your directions)

Written 2026-09-12 from the live code. This is a read-out, not a proposal —
work your DAM standards into it wherever you want the behavior to change.

## 1. The pipeline order (app/cli.py — the backfill)

```
import-library → catalog-pending → scan-faces → cluster-subjects
```
- `import-library` — brings files in, detects kind, extracts checksum + capture
  date (`filename_creation_date()` first, embedded metadata as fallback).
- `catalog-pending` — the Cataloger (below). Resumable; runs as worker too.
- `scan-faces` — YuNet detection → SFace embeddings (your private models).
- `cluster-subjects` — groups detections into subject groups (people/pets).

## 2. The catalog run itself (app/cataloger.py)

Stage 1 — VISION (perception only): the vision model looks at the photo or
sampled video frames and describes ONLY what is visible. No names, brands,
dates, prices. If words appear in the image they are quoted exactly.

Stage 2 — WRITER (text only): a second model call writes the strict-JSON record
from the Stage 1 description. No image is sent. Then two guards stamp over it:
- `_stamp_filename_date`: the FILENAME is the only creation date allowed. If the
  filename has no ISO date, every date field is written EMPTY — never guessed.
- The 15 Dublin Core elements land on `media_assets`; the Schema.org and
  Open-Graph/Meta projections are built from them (`build_review_metadata`),
  pinned by Tests (test_standards_labels, test_review_metadata).

Label rules your tests enforce: "Dublin Core, ISO 8601, Schema.org, Open Graph /
Meta" (never "Facebook Open Graph"), "Combined / shared values", owner-editable,
immutable-filename creation-date rule, `date_created_raw` naive on purpose.

## 3. Who writes it — provider fallback chain (app/catalog_providers.py)

Order from config `catalog_provider_order` (default groq → gemini →
openrouter → ollama). Vision-capable variants are chosen automatically when an
image is attached (groq_vision_model / ollama_vision_model). First provider to
return valid JSON wins; all failures are collected into one error. Your keys
for Groq/Gemini/OpenRouter/Ollama are all present in .env.

## 4. The subject system today (app/subject_rotation.py) — 12, not your 7

A deterministic wheel, NOT engagement-driven: 12 fixed editorial subjects
(historical ritual, museum art, brutalist architecture, raw macro, crystals,
flowers, landscapes, old hollywood, icon quotes, product anchor, vintage
cinema, founder diary). Position 5 is ALWAYS the product anchor; the other 8
rotate through the remaining 11, advancing one step per week. The Muse's scout
guidance and the Week-page tile labels come from `planning_guidance(week)`.

**This is the piece to replace with your 7 (or 9) IPTC subjects** — the wheel
is load-bearing: Muse retrieval (below) matches Library content against it.

## 5. How the Muse finds content (app/muse_retrieval.py)

Given a week's subjects, the Muse searches the cataloged Library for assets
matching each subject, proposes them position-by-position, and
`muse_assignment.apply_approved_muse_selection()` applies your approved picks
in visual-position order — refusing partial, duplicate, unknown, trashed, or
non-image/video selections. Asset rows are never mutated by the Muse.

## 6. Metadata governance (app/metadata_registry.py)

Ten declared families, each with one authoritative owner:
asset · bytes · dublin_core · catalog_evidence · faces · subjects · folders ·
scout · posts · audit. New features are supposed to attach metadata to the
right family instead of inventing columns — useful guardrail when you write
the three/four content-class directions.

## 7. Owner gates (hard rules the code enforces)

- Filename = immutable creation date (ISO 8601 date-first only; `2020-30-08`
  deliberately yields NO date rather than a wrong one).
- `get_db()` never commits — a bare `flush()` rolls back; cataloger results
  stay "suggested" until owner review marks them catalogued.
- Owner is the sole destructive authority; assistants propose, never commit.

## 8. Open spots for your directions to fill

1. The 12-subject wheel → your 7/9 IPTC subjects (Muse + scouts + Week labels
   all read from it — one swap changes every consumer).
2. Content-class dispatch: Original Raw vs Derivative vs Owner Archive vs New
   Original — the cataloger currently treats everything identically.
3. Derivative lineage in the record (dc:relation / derived_from chain) — not
   yet written into the Dublin Core block.
4. Stock-license blocks (Pexels/Pixabay/Unsplash/Coverr attribution) — scout
   captures creator+license, cataloger does not yet project them into
   dc:rights/dc:contributor automatically.
