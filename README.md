# Évolué — AI Media Team (rebuild)

**Build date:** 2026-09-19 · **Owner:** Jean · **Architecture:** FastAPI + Jinja2, direct Azure SQL, Azure Blob (no SQLAlchemy)

## Structure

| Path | Purpose |
|---|---|
| `evolue/` | Application package (layered) |
| `evolue/domain/` | Workflow, planning, library/catalog, media lineage, proposals, publishing, history rules |
| `evolue/application/` | Transactional commands + orchestration |
| `evolue/infrastructure/` | SQL repos+migrations, storage adapters (SAS mirages, copy-first promotion), durable jobs |
| `evolue/web/routers/` | auth, calendar, weeks, posts, studio, media_editor, library, reviews, approvals, publishing, history, assistants |
| `evolue/ui/` | Shared templates/components |

## Owner rules (binding)

- 9 immutable IPTC subjects: `CUL ART CIN CHM HLT PRD FIN LIF HUM` (no numbers)
- Naming: `YYYY_W##_IPTC-Subject-Code_SEQUENCE` → derivative suffix `_dcterms:isVersionof_uuidv7().ext`; original `_dcterms:hasVersion_uuid`
- Containers: `Bunbuns` permanent · `Ephemera` scout quarantine · `Scrappa` pipeline scratchpad (distinct)
- State machine: `STEP_0_ORIGINAL → STEP_1_COMPLETE → STEP_2_PENDING → PIPELINE_COMPLETE_APPROVED`
- JAN gates bind everything; owner password required; override password exists
- Muse searches approved library only, reports gaps; scouts 9/subject into Ephemera; Studio COMMIT assigns uuidv7() and destroys unselected
- AI team: CD, Brief Validator, Creative Grader, Production Grader, Current Events, Fact Check, Muse, Content Scouts, Cataloger, Media Editor, Copywriter, Copy Grader, Scheduler
- `mirages`: short-lived SAS URLs for streaming heavy files

## Contracts

- Creative Brief FORM: 10 panels (1 theme image + 9 posts), 3×3, 9:16, titled `YYYY_W##_THEME_HOST`, tiles `IPTC-Subject-Code_Sequence##`, A/R/R per panel and per tile
- Grader sheets: Brief Validator PASS/WITH-WARNINGS/BLOCKED + structural /100; Creative Grader 9 sections /100; Production Grader 7 sections /75
