# SCHEMA.ORG / JSON-LD CATALOG STANDARD

**Authority:** This file is the single authoritative definition for Schema.org output in the Evolue Media Library. It is a projection of the Dublin Core block plus catalog evidence — NEVER an independent invention.

**Canonical reference:** https://schema.org

## 1. Prime Rule

Schema.org is written as JSON-LD and is a **projection of the Dublin Core block plus catalog evidence**. If a Dublin Core field is blank, the matching Schema.org field stays blank. Schema.org never invents a fact that is not already in the record.

## 2. @type Mapping (from dc:type)

| dc:type | @type |
|---|---|
| StillImage (image/jpeg, png, webp) | ImageObject |
| MovingImage (video/mp4) | VideoObject |
| Sound (audio) | AudioObject |
| Text (docx, pdf, html, md, json) | DigitalDocument |
| Dataset (spreadsheets, databases) | Dataset |
| Software (programs, executables) | SoftwareApplication |
| InteractiveResource (web apps, VR, games) | MediaObject |

## 3. Field Tables

Every Schema.org field maps 1:1 from Dublin Core. A dash (—) means "leave blank unless evidence exists."

### Required (7)

| Schema.org | Source | Rule |
|---|---|---|
| @context | const | `https://schema.org` |
| @type | §2 map | from dc:type |
| @id | uuidv7() | the SAME UUID that links Original and Derivative |
| name | dc:title | from the filename (available after MUSE) |
| description | dc:description | captions/hashtags after COPYWRITER approval |
| contentUrl | — | SAS-token URL ONLY (see §5). Omitted if not authorized for sharing. |
| encodingFormat | dc:format | image/jpeg, video/mp4, ... |

### Structural (6)

| Field | Rule |
|---|---|
| width | pixels, ImageObject only |
| height | pixels, ImageObject only |
| duration | seconds, VideoObject/AudioObject only |
| uploadDate | ISO 8601 — from the FILENAME only. Never guessed. |
| dateCreated | ISO date from the FILENAME only (immutable-filename rule). Empty if the filename has no date. |
| thumbnailUrl | SAS-token URL of the standard thumbnail |

### Provenance (6)

| Field | Source |
|---|---|
| creator | dc:creator — "Evolue Media Team" default; a real person only with evidence |
| publisher | dc:publisher — "Evolue Skincare Inc" |
| contributor | dc:contributor — "Jane Doe via www.pexels.com/photo/12345" |
| license | dc:rights wording, including the source platform name |
| creditText | short credit line |
| copyrightNotice | dc:rights full notice |

### Lineage (3)

| Field | Rule |
|---|---|
| isBasedOn | dc:identifier URL of the ORIGINAL work — the machine-readable mirror of dcterms:isVersionof on the Derivative |
| isPartOf | the week's collection (YYYY_W##_THEME) |
| keywords | dc:subject (IPTC Subject Codes) + derived keywords |

## 4. Worked Examples

### ImageObject (Original)

```json
{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "@id": "0192a1b2-c3d4-4e5f-8a6b-7c8d9e0f1a2b",
  "name": "2026-09-17_W37_CUL_HERITAGE-RITUALS_01_ig-tt",
  "description": "Heritage beauty ritual highlight for Evolue week 37.",
  "contentUrl": "https://bunbuns.blob.core.windows.net/library/...?sig=...&se=...",
  "encodingFormat": "image/jpeg",
  "width": 1080,
  "height": 1920,
  "uploadDate": "2026-09-17",
  "dateCreated": "2026-09-17",
  "creator": { "@type": "Organization", "name": "Evolue Media Team" },
  "publisher": { "@type": "Organization", "name": "Evolue Skincare Inc" },
  "keywords": ["CUL", "01000000", "heritage", "beauty"]
}
```

### VideoObject (Derivative with lineage)

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "@id": "0192b3c4-d5e6-4f70-9a81-b2c3d4e5f607",
  "name": "2026-09-17_W37_CUL_HERITAGE-RITUALS_01_ig-tt",
  "description": "Derivative cut of the original ritual footage.",
  "contentUrl": "https://bunbuns.blob.core.windows.net/library/...?sig=...&se=...",
  "encodingFormat": "video/mp4",
  "duration": "PT12S",
  "uploadDate": "2026-09-17",
  "isBasedOn": "https://bunbuns.blob.core.windows.net/library/original...?sig=...&se=...",
  "isPartOf": "2026_W37_HERITAGE-RITUALS",
  "creator": { "@type": "Organization", "name": "Evolue Media Team" },
  "publisher": { "@type": "Organization", "name": "Evolue Skincare Inc" },
  "keywords": ["CUL", "01000000", "heritage"]
}
```

## 5. Private-Archive Rules

1. `contentUrl` / `thumbnailUrl` are **1-hour SAS token URLs only** — a raw or private URL is NEVER written here. If the asset is not authorized for sharing, `contentUrl` is omitted.
2. No private person, location, claim, or private URL is ever exposed.
3. Fields are never promoted to public schema without approval — this is a **private archive first**.

## 6. Validation Checklist

- Has all 7 required fields (or a justified omission, e.g. `contentUrl`)
- `@type` matches the dc:type map
- `@id` is the uuidv7() recorded in the catalog record
- `uploadDate`/`dateCreated` came from the filename, never guessed
- No private data present
- Valid JSON (re-check with `json.loads`)

## 7. What NOT to do

- Never invent a field the Dublin Core block does not support.
- Never convert JSON-LD to prose in the record.
- Never promote to public schema without approval.
- Never guess uploadDate or dateCreated.
