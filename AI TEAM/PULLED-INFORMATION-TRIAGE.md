# Triage: "Information to Pull to NEW HOPE folder"

Updated: 2026-09-11. One pass, verdicts recorded, no rabbit holes.

## What this folder is

A complete older checkout of the Évolué project the owner pulled in for
reference. Its `app/` tree is **byte-identical to the current `app/`**
(hash-verified on templates; file-list diff shows zero code files unique to
either side except the new `app/week_archive.py`, `app/ui/Studio.dc.html`,
and `app/static/studio.js`, which exist only in the current tree). So the
duplicate `app/` must NOT be built from — but everything *around* it is
valuable.

## Verdicts

### GOLD — keep, mine, and re-run

- **`Tests/` (18 test files + conftest)** — the executable specification.
  Verified passing against the *current* app:
  - `test_week_archive.py` — 1 passed (validated the reconstructed
    `app/week_archive.py`; it also caught my missing keyword defaults).
  - `test_standards_labels.py` — 1 passed. Demands the Reviews template name
    **Dublin Core, ISO 8601, Schema.org, "Open Graph / Meta"** (and never
    "Facebook Open Graph / Meta"), "Combined / shared values",
    owner-editable, and the immutable-filename creation-date rule. All
    present in the current `LibraryReviews.dc.html`.
  - `test_review_metadata.py` + `test_review_requirements.py` — 4 passed
    together. They pin `build_review_metadata`'s schema_org/open_graph
    projections (VideoObject, width/height/duration/encodingFormat,
    og:video, copyrightNotice default-empty).
  - Running them against the current tree: copy the test (and `conftest.py`)
    to the repo root first — run from inside the folder, `import app`
    resolves to the folder's own `app/` and shadows the real one.
- **`CLAUDE.md`** — expensive-to-rediscover traps. The ones that matter for
  the rebuild: migrations must be idempotent (`ADD COLUMN IF NOT EXISTS`, one
  transaction); `get_db()` never commits (a bare `flush()` is rolled back);
  filenames are the immutable ISO 8601 creation date, date-first, never
  `YYYY-DD-MM`; all 15 Dublin Core elements live on `media_assets`; env vars
  must be `AZURE_`-prefixed and misnames die silently (`extra="ignore"`).
- **`AIs for Media Library.md`** — the assistant safety/ownership policy the
  manifest's chatboxes and guardrails implement. Owner is the sole
  destructive authority; assistants propose, never commit.
- **`requirements.txt`** — the dependency list that was missing from the
  current tree. Use as a reference when pinning (it includes deploy-only
  extras: gunicorn, alembic, opencv, rembg, hachoir, mutagen).
- **`Scripts/`** — `fetch_models.py`, `pre-commit-check.ps1`,
  `install_media_generators.ps1`, `start_media_generators.ps1`,
  `create_data_room.py`. Ops tooling worth porting deliberately.
- **`Worker/`** — `face_loop.py`, `publishing_loop.py`, `publishing_cron.py`:
  the background workers the app's `publishing_worker_secret` and face-scan
  queue are built around.
- **`DataAnalystExpert/musicgen_server.py`** — the local MusicGen REST server
  that `settings.music_generator_endpoint` points at (the 4 GB-VRAM adapter).

### PROTECTED — never commit, never merge, never "clean up"

- **`Models/*.onnx`** (`face_recognition_sface`, `face_detection_yunet`) —
  the private face-recognition models. Manifest rule: private to the owner
  and explicitly authorized friends, never public. `.gitignore` already
  blocks `*.onnx`.
- **`env`, `env.bak-before-vision-split`** — real environment files with
  credentials. Never copy their contents into the current `.env` blindly;
  never commit. CLAUDE.md's two-worktree trap applies: the directory you
  launch from decides which database you touch.

### NOISE — ignore or delete later

`_pycache_` (86 files), `.pytest_cache`, `.azure`, `Node Modules`,
`DataAnalystExpert/*.log`, `package-lock.json`/`package.json` (Node-era
leftovers), stale root `.sqlite3` databases (CLAUDE.md confirms they lack
`review_status` and are unused).

### DUPLICATE — do not build from

The entire `app/` subtree (117 files) — identical to the current tree.

## How to run the old suite against the current app

```
Copy-Item "Information to Pull to NEW HOPE folder\Tests\conftest.py" conftest.py
Copy-Item "Information to Pull to NEW HOPE folder\Tests\test_<name>.py" .   # root
python -m pytest test_<name>.py -q -p no:cacheprovider
Remove-Item conftest.py, test_<name>.py
```

`test_integration.py` was skipped this pass; run it the same way when a full
parity sweep is wanted.

## Standing rule

Tests are the contract. Every manifest step that gets rebuilt should keep
these tests passing — they encode the DAM standards (ISO 8601, Dublin Core,
Schema.org, Open Graph/Meta) at a level prose never will.
