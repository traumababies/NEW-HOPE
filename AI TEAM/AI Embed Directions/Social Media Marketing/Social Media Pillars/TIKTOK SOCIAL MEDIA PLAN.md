# ÉVOLUÉ — TIKTOK SOCIAL MEDIA PLAN

Companion to `SOCIAL MEDIA ALGORITHM PILLARS.md` (the 4-pillar framework — read that first).
This is the TikTok execution plan: how the pillars, the weekly theme, and the app's
pipeline (Calendar → Studio → Library → Copywriter → Approvals → Publishing) come out
the other end as TikTok posts.

## 1. Cadence

- **3 posts per week**: Monday, Wednesday, Friday — hours set in `app\config.py`
  (`monday_publish_hour` 8, `wednesday_publish_hour` 12, `friday_publish_hour` 16,
  America/Phoenix). Same schedule as Instagram; one approved post publishes to both.
- Every post belongs to the **active weekly theme**. TikTok and Instagram carry the
  same story — platform rules change the delivery, never the message.

## 2. The 4 pillars on TikTok

| Pillar | TikTok job | Format |
|---|---|---|
| Authority & Education | teach fast: one ingredient/history fact per video, 15–30s | talking/overlay video |
| Brand Identity & Storytelling | the évolué soul — vintage-film philosophy, product lore | cinematic monochrome video |
| Entertainment & Culture | trend + seasonal hooks (holidays, pop culture) for reach | trending-audio video |
| Aesthetic & Sensory Experience | ASMR texture (Resurfacing Grains: oat flour + creme de la creme milk powder) | close-up macro video, minimal voice |

A healthy week touches at least 2 pillars; the algorithm needs repetition to bucket
the profile, not variety for its own sake.

## 3. Platform rules (mirror of the Copywriter's prompt in `app\ai_assistants.py`)

- **Hook in the first 1–3 seconds** — motion or a bold claim before anything else.
- **Conversational, authentic tone** — never polished-corporate. Humor, relatability,
  emotional honesty.
- **Short captions** unless running a story thread or sarcastic hook.
- **Ask questions / invite debate** — comments are the growth signal on TikTok.
- **Hashtags: trending + niche mix** — the algorithm rewards diversity; ~5–8 on
  TikTok (vs 10–30 on Instagram).
- No virality promises — engagement logic only.

## 4. How content physically gets there (app flow)

1. Studio commits the chosen original — filename ISO
   `YYYY-MM-DD_W##_CODE_THEME_SEQ##_VERTICAL.ext`, platform `IG-TT`, vertical video.
2. Cataloger gives it full metadata (Dublin Core / Schema.org / Open Graph) in
   **bunbuns**; Copywriter drafts the TikTok caption + hashtag group.
3. Owner approves in **Approvals** — nothing publishes without final approval.
4. Publishing worker posts via the TikTok Content Posting API
   (`app\publishing_adapters.py`: `publish_tiktok` — image or video; media handed to
   TikTok through a ~15-minute signed blob URL from bunbuns, never a public link).
5. Tokens: `tiktok_client_key/secret` + access/refresh tokens in Key Vault
   (`app\platform_tokens.py` refreshes automatically).

## 5. Week-shape example (fill per weekly theme)

- **Mon (Authority):** "Why oat flour was in 1920s cold creams" — 20s, caption asks
  "would you trust a 100-year-old ingredient?"
- **Wed (Sensory):** grains-in-palm ASMR macro, 12s, near-zero caption.
- **Fri (Story/Culture):** vintage-film-styled product shot with weekly-theme audio,
  hook line from the Creative Director brief.

The 9-tile profile-grid rule applies to the Instagram grid; TikTok has no grid —
there the week wins on **consistency and theme repetition**, so keep covers and
opening frames visually identical across the week.
