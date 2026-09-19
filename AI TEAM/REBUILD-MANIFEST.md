we# Évolué Direct Workflow Rebuild

This file is the durable, local source of truth for the rebuild in `C:\Users\Bunbunz\Documents\New Hope` and private repository `bunbunz/new-hope`.

THE GOAL

The social media calendar that goes from weeks (on calendar page) to week (week page) to post (post page). 1 theme image that cuts into 9 tiles that are thumbnails for the 9 posts that share the theme. They post 3 at a time 3 times a week. 3 on Monday, 3 on Wednesday, and 3 on Friday. They post to instagram and tiktok and they have to post with differen thumbnails and sizes that match the order and size of instagram and tiktok. On calendar page I can write them themes 2 years ahead and approve the posts so they automatically go out. So on Calendar I write the theme. Then on Week Page the creative director writes the creative brief (the two assistants that use Groq's compound and compoud-mini AI make sure the themes are current and fact checks). Then the muse sees what we have in the library that the cataloger already got approved (he has to catalog using DAM standards with ISO 8601, Dublin Core, Schema.org and the Open Graphs/META standards). All content has to have my final approval. So after muse picks out the content based on what the library has approved, the Content Scouts use their 4 API keys to go grab images and videos that have same theme of the week at PIXELS, PIXABY, COVEERS, and UNDERsomething. They bring 9 images or videos PER post that I can pick from. They download it to the STUDIO page for me to approve or reject (goes to trash) I only choose 1 and that's the only one that goes into the library. Rest are deleted right away and never touch the library. We have a Blob (godzilla1126) and 2 containers. The STUDIO Page will use the container name Ephemera to store the 10 images/videos that I will pick from. As oon as I choose, the chosen ones go to the other container named Bunbuns. The Azure SQL name is free-the-information-101010 and the SQL database name is sanctuary-888. I have all the keys. As soon as the content is chosen, it gets qued to the cataloger to catalogue. So after I choose, it is Media Editor's job to transformed them to posts using image, video, and/or audio generators. After he's done, The COPYWRITER can write the captions and 5 hashtags per post with the help of the 2 AIs who make sure things are current and verify facts again. All assistants have a button that I can click to APPROVE their work, REJECT (Assistants have to REDO), or REPLACE button (which means I will take it from there and do it myself). They all have 2 redos, after, they cannot. Anyway, after the work is approved, they stay approved in their week/post pages until a week before and they go to the Approvals Page, then the week of their post, they go to the PUBLISHING Page where the scheduler makes sure that the order, thurmnails, and sizes match instagram or tiktok standards. From the Publishing Page, I have the option to go to Tiktok and/or Instagram and ManualPublish the posts. Because 9 images make an image, if one is late, all other posts have to wait if they are behind the late one. When the week is over, the posts that don't get published move on to History and HistoryDetails Pages to be recorded to teach future AIs and humans on - so the original raw image/video, final image/video, and all the WRITTEN edits go to history/historydetals page. Let's discuss the website design - The Top Menu is this order and they all have to look uniform with same font, size, spacing, color, etc. on all the pages. Order of Menu is: Calendar (with Week and Post underneath), Media Editor (with Studio underneath), Library (with Reviews underneath), Approvals, Publishing (with Manual Publishing underneath), History (with History Details underneath), then a LOG OUT. The brand colors are bright cool white background with Cool Medium Grey text. Cool Light Grey to color in big boxes to contrast with white, and rarely use Cool Dark grey, never on headlines or titles. Black is never allowed anywhere. The accent colors are light pink, light green, and light yellowish orange as you can see in the Approvals Page. Calendar, Post, Media Editor, Studio, Library, and Reviews pages all have chatbox with on top right, please make sure to look at the HTMLs in the APP/UI folder. Godzilla is always around with a button on bottom right. The chatbox has an Activities svg icon  where when I click it the Assistants Panel popup comes up showing what is pending for each of the AI assistants. When I click the button on the left it starts the assistants on their pending work. There is a toggle on the far right of each assistant that lets me turn them off and do the work myself. There is also a chatbox at the bottom that lets me talk to them. Our goal is recreate this (I spent A LOT of time perfecting it), and clean it up so the backend is much more efficient and direct without the mess. While I finish up gathering the rest of the files, please think of the most efficient way this whole process can be done. If you think we need another step somewhere or we should delete a step, please tell me. The goal is for everything to be communicated the fastest and most direct way possible so the information isn't bouncing all over the files before it gets to where it needs to go.

## Ten-step governing plan

1. Define one direct workflow and shared records so Calendar → Week → Post → Library/Muse → Scouts/Studio → Cataloger → Media Editor → Copywriter → Approvals → Publishing → History passes each item forward once.
2. Recreate the unified shell and perfected design: identical ordered navigation, cool-white/grey palette, restrained pink/green/yellow-orange accents, chatboxes, Activities panel, assistant controls, and Godzilla.
3. Build Calendar planning up to two years ahead: one weekly theme image, nine linked post-cover tiles, owner approval, and three posts each Monday, Wednesday, and Friday.
4. Build Week/Post planning: Creative Director brief, Groq Compound and Compound Mini currency/fact checks, and nine posts sharing the approved weekly theme.
5. Build the Library pipeline: Cataloger metadata under ISO 8601, Dublin Core, Schema.org, Open Graph, and META standards; owner review controls Muse eligibility.
6. Build Muse → Scouts → Studio sourcing: Muse searches approved Library content and gives Scouts precise gaps; four providers return nine total candidates per post into `Ephemera`; Studio is viewing/selection only; one selected item moves to `Bunbuns` and Library, and the rest are deleted after safe promotion.
7. Build creative production without removing existing tools: preserve Creator's Studio for quick stickers/emojis/words; preserve separate Post image/video/audio editors; preserve ACE Studio and ComfyUI inside Media Editor; create platform derivatives while retaining nine-tile order.
8. Build Copywriter and universal decisions: captions plus exactly five hashtags per platform; APPROVE, REJECT/REDO, or REPLACE; maximum two redos; REPLACE permanently transfers that stage to the owner.
9. Build Approvals and Publishing: stage work one week ahead; enforce platform order, dimensions, thumbnails, Monday/Wednesday/Friday groups, automatic/manual publishing, and predecessor blocking.
10. Build History and validate end to end: record all written edits, reasons, approvals, rejections, redos, replacements, and publishing outcomes; retain raw original and final media only; then connect Azure and external providers safely.

## Step 1 — Workflow contract

### Canonical flow

Owner theme → Creative Director brief → owner decision → Muse approved-Library search → Scout request → `Ephemera` candidates → Studio owner selection → `Bunbuns` promotion → Cataloger metadata → owner metadata approval → creative production → Copywriter package → owner final approval → Approvals → Publishing/Manual Publishing → History.

### Weekly structure

- One week owns one approved theme, creative brief, theme image, and exactly nine ordered posts.
- The theme image is cut into nine stable cover tiles that reconstruct the weekly image only in the correct order.
- Each post may also own selected source media, final media, caption, exactly five hashtags, and Instagram/TikTok derivatives.
- Positions 1–3 publish Monday, 4–6 Wednesday, and 7–9 Friday. Later dependent positions cannot pass a blocked or late predecessor.

### Direct handoffs

1. Only the owner creates or changes themes and gives final approval.
2. Creative Director submits a proposal. APPROVE advances; REJECT requests one of at most two redos; REPLACE permanently transfers the stage to the owner.
3. Muse searches only owner-approved, cataloged Library media.
4. Muse creates precise Scout requests for unresolved needs; Scouts do not reinterpret the theme independently.
5. Scouts gather nine total temporary candidates per post across four providers into `Ephemera`.
6. Studio is viewing/selection only. APPROVE chooses one; REJECT follows the redo flow; REPLACE lets the owner upload or select media.
7. Owner uploads immediately queue Cataloger. Owner-approved selections cancel stale Muse/Scout work.
8. Promotion is copy-first: selected media is durably copied to `Bunbuns`; only then are unselected temporary candidates deleted. They never enter Library.
9. New media must be cataloged and metadata owner-approved before creative production begins.
10. Every page reads shared canonical IDs and projections rather than maintaining duplicate pipeline records.

## History and training record

- Record every written edit/change and every APPROVE, REJECT, REDO, and REPLACE with actor, time, stage, before/after values, selected reasons, free-written reason, and affected record IDs.
- History is append-only. Corrections append events rather than rewriting earlier records.
- Retain immutable raw-original media and approved final media only. Temporary/intermediate bytes expire, but recipes, instructions, parameters, outcomes, and reasons remain.
- Approval fingerprints exact final media, cover, audio, caption, hashtags, and platform settings. Later edits revoke current approval without deleting its history.

## Mandatory preservation rules

- Preserve Creator's Studio for quick stickers, emojis, and words.
- Preserve the Post page’s separate image, video, and audio editors.
- Preserve ACE Studio and ComfyUI inside Media Editor.
- Do not delete, redesign, replace, or modify creative software without explicit owner approval.
- Do not classify a control as dead because wiring is missing. Ask the owner before removal; default to making it work.
- New Studio is viewing and selection only; leave its visual design for Claude design.
- Preserve private face recognition/search for the owner and explicitly authorized friends. It is never public.
- Do not use SQLAlchemy. Use direct, parameterized Azure SQL access with explicit repositories, transactions, migrations, and typed command/row models.

## Azure boundaries

- Azure SQL server/database: `free-the-information-101010` / `sanctuary-888`.
- Azure Blob account: `godzilla1126`.
- Containers: `Ephemera` and `Bunbuns` (actual service identifiers must be verified before integration).
- Credentials are supplied later and never committed.

## UI contract

- Bright cool-white background.
- Cool-medium-grey text.
- Cool-light-grey large panels.
- Cool-dark-grey only rarely and never for titles/headings.
- No black.
- Light pink, light green, and light yellow-orange accents.
- Navigation: Calendar (Week, Post) → Media Editor (Studio) → Library (Reviews) → Approvals → Publishing (Manual Publishing) → History (History Details) → Log Out.
- Assistant chatboxes: Calendar, Week, Post, Studio, Media Editor, Library, Library Reviews, and History Details.
- Activities SVG opens pending work with start controls and assistant toggles. Godzilla remains at bottom right.

## Clean architecture

- FastAPI/Jinja with a small application factory and thin routers.
- `domain/`: workflow, planning, library/catalog, media lineage, proposals/decisions, publishing, and history rules.
- `application/`: transactional commands and orchestration.
- `infrastructure/sql/`: direct Azure SQL repositories and migrations; no SQLAlchemy.
- `infrastructure/storage/`: Azure Blob adapters, copy-first promotion, authenticated delivery, and durable deletion intents.
- `infrastructure/jobs/`: durable idempotent assistant, cataloging, generation, deletion, and publishing jobs.
- `web/routers/`: auth, calendar, weeks, posts, studio, media editor, library, reviews, approvals, publishing, history, assistants, and media delivery.
- Shared templates/components and centralized brand tokens; remove duplication only after behavior parity is verified.

## Source and safety

- Build directly in `C:\Users\Bunbunz\Documents\New Hope` from the `bunbunz/new-hope` tree.
- Treat the owner-supplied `app` folder as messy reference material to understand and rewrite, not as code to copy blindly.
- Never search for or use old files, prior worktrees, backups, archives, transcripts, deleted material, or other Downloads content. Ask the owner if something is missing.
- Do not delete supplied reference files during planning. Build and verify replacements first.
- Never commit credentials, environments, databases, media, caches, models, logs, or generated output.
- Confirm the fourth Scout provider name before integration; do not guess.
