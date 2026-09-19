# AI TEAM SPECS — contracts · loops · state · wrong-layer · starvation · gates

Version: 1 · Created: 2026-09-14 · Owner-approved design target
Reader: any human or model resuming this team. Read `OPERATING-CONTEXT.md` and
`taste.md` alongside this file. Bump the version at the top whenever a contract changes.

## The six patterns (applied to every member)
1. **CONTRACT** — exact input → output schema; required fields; validation runs at every boundary.
2. **LOOP** — how the member iterates on feedback and where the feedback sinks (redo-with-reason, max 2 redos).
3. **STATE** — what it reads and writes (queues, tables, files). Files/DB are the memory, never chat logs.
4. **WRONG LAYER** — the tasks that must NOT be asked of it (they belong to deterministic code or another role).
5. **STARVATION GUARD** — the minimum context it must always be seeded with so it never works blind.
6. **LETTING IT FLY** — the human gates: where the owner must approve, and where safe autonomy is allowed.

Shared laws: version every artifact · contracts validate loudly · deterministic spine owns cadence/laws ·
every decision writes a sink (history / taste.md / training_knowledge) · a rejected redo must visibly change.

Status legend: ✅ built · 🟡 partial/wiring needed · 🟢 to build.

---

## 1 · Creative Director (🟡 prompt+profile exist; brief panel exists)
**CONTRACT**
- In: theme (from calendar), year plan, brand voice 1-liner, last 2-4 weeks of decisions, the 9-subject list.
- Out (JSON): theme rationale; 9 subject briefs, each = `subject_code, one_line_angle, search_terms[], tone_note, reference_description`. Every subject required - no fewer than 9.
**LOOP** — owner reviews the brief; changes are re-fed once (max 2 redo); the approved brief is version-stamped and becomes THE artifact.
**STATE** — reads: `calendar_weeks`, `operating context`, `taste.md` recent tags, last weeks' approvals. Writes: the weekly brief (the shared object).
**WRONG LAYER** — never edits library, never picks assets, never writes final captions, never decides posting times.
**STARVATION GUARD** — always seed: current week + year direction + last 4 weeks of approve/reject "why" + brand voice line + taste tags.
**LETTING IT FLY** — drafts autonomously; the brief is OWNER-GATED before any downstream role consumes it.

## 2 · Current Events (compound) (🟡 needs wiring into the brief step)
**CONTRACT**
- In: the brief's theme + subject angles; a scope cap ("exactly 3 claims per subject max, window = this week").
- Out (JSON): `[{subject_code, claim, source_url, source_name, confidence(0-1), as_of_date}]`. Source URL REQUIRED on every claim.
**LOOP** — Fact Checker consumes its output; claims that fail fact-check return to it as "re-check" - never silently re-emitted.
**STATE** — reads: brief. Writes: its claims payload (fed to Fact Checker; logged to history).
**WRONG LAYER** — must not assert without a URL; must not write the brief itself; must not decide relevance alone.
**STARVATION GUARD** — fresh window declaration ("this week, not evergreen"), theme and subjects always passed in.
**LETTING IT FLY** — drafts claims autonomously; only verified+rated claims reach the brief (gated by Fact Checker, seen by owner in the brief).

## 3 · Fact Checker (compound-mini) (🟡 wiring needed)
**CONTRACT**
- In: Current Events claims payload + the theme for context.
- Out (JSON): `[{claim, verdict: verified|unverified|contradicted, evidence_urls[], confidence, note}]`. Reservation REQUIRED when unverifiable - it must be able to say "cannot verify."
**LOOP** — any "contradicted" claim is removed from the brief with the reason logged; unverified = dropped, never reshuffled.
**STATE** — reads: claims payload, brief. Writes: verdicts into history/training logs; contributes no content of its own.
**WRONG LAYER** — must not invent or "recall" sources; must not act as the Creative Director; must not auto-approve claims.
**STARVATION GUARD** — always seeded with "you may say I cannot verify - do not guess" and the current window.
**LETTING IT FLY** — verdicts are autonomous but conservative; its "cannot verify" is permanent until new evidence is supplied, not retried blindly.

## 4 · Muse (✅ exists)
**CONTRACT**
- In: brief (9 subjects) + approved Library only (the 9 IPTC folders).
- Out (JSON): per subject `{subject_code, library_pick_asset_id, gap: {needs_scout: bool, search_terms[], media_type}, caption_suggestion, confidence}`. If empty, gap REQUIRED, never a fabricated pick.
**LOOP** — owner-approved picks become examples; Muse re-runs each week with approval history to converge on taste.
**STATE** — reads: `media_assets` (approved only), approval snapshots, subject folders. Writes: its per-week suggestion manifest.
**WRONG LAYER** — never promotes anything into the Library; never marks eligibility; never bypasses Studio.
**STARVATION GUARD** — always seed: "approved assets only; report gaps; never invent a match."
**LETTING IT FLY** — suggests autonomously; every pick is owner-confirmed in Studio before anything moves.
