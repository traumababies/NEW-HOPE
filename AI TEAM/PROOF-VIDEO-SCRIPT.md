# PROOF VIDEO — 2-minute one-take script (Founder's Hub submission)

## What this video actually is (plain English)

Program reviewers watch hundreds of applications. The video is **not a movie** — it is
a screen recording of the real app doing real work, while you explain it in one take.
No editing, no music, no animations. Honest beats polished: they are judging whether
the product is real and whether the founder knows it. Under 2:10 total.

## How to record (Windows, free)

- **OBS Studio** (free, best): Add Display Capture + Audio Input Capture sources, hit
  "Start Recording". Or **Xbox Game Bar**: press `Win+G`, click the record button.
- Record at your screen's normal size, close extra tabs, silence notifications
  (`Win+Focus assist` or just quit chat apps).
- Talk like you're showing a friend. If you stumble, just keep going — one take, done.

## The shot list (timestamps are targets, not laws)

**0:00–0:10 — The problem (title card or voice-over over the app)**
"Beauty brands pay agencies thousands for wallpaper content — pretty girls, coffee,
products with no story. I built the machine that makes content mean something, and it
runs on Azure."

**0:10–0:30 — Calendar / Week view**
Show the weekly theme and the 9-tile week. One sentence: "Every week has one theme;
nine posts form a single story, not nine random posts."

**0:30–0:55 — Studio (the gating workbench)**
Drop a file. Show the dedupe notice. Choose one candidate, dismiss the rest, commit.
"Nothing reaches the library unless I choose it. Discards are deleted — they never
touch the archive."

**0:55–1:15 — Library / Cataloger**
Open the committed asset's metadata: Dublin Core fields, ISO date, provenance.
"Every asset gets museum-grade metadata automatically. This is a catalog, not a
camera roll."

**1:15–1:35 — Copywriter + Approvals**
Show the drafted TikTok/Instagram caption, then press approve.
"Assistants can draft and suggest — nothing publishes without my approval."

**1:35–1:55 — Publishing (the payoff)**
Show the live post on TikTok or Instagram. "Three posts a week, every week, and the
machine did the showing up."

**1:55–2:10 — Azure proof (10–15 seconds, the part reviewers want)**
Azure portal: the two blob containers (**Ephemera** = staging, **Bunbuns** = permanent
archive), Key Vault holding the tokens. "Media never gets public links — TikTok
fetches it through short-lived signed URLs."

## Pre-flight checklist

- [ ] App running on the **deployed URL** if the deploy is done; local `127.0.0.1:8011` is an acceptable fallback — re-film later if needed
- [ ] Sample content ready: 1 image + 1 video for the Studio drop
- [ ] A real weekly theme active in the calendar
- [ ] One post queued for approval so the Approvals → Publish click is real
- [ ] Azure portal tab open and logged in (containers + Key Vault visible)
- [ ] Fresh session, no test junk visible on screen

## One rule

Show the *flow*, not the features. Drop → choose → cataloged → approved → live, with
Azure visible at the end. That single arc answers every question they will ask.
