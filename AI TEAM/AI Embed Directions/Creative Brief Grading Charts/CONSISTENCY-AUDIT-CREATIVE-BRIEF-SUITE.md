# Consistency Audit — Creative Brief Suite

**Audited:** 2026-09-17
**Scope:** WEEKLY-CREATIVE-BRIEF-TEMPLATE · CREATIVE-DIRECTOR-DETAILED-
INSTRUCTIONS · BRIEF-VALIDATOR-REVIEW-SHEET · CREATIVE-GRADER-REVIEW-SHEET ·
PRODUCTION-GRADER-REVIEW-SHEET · FINAL-BRIEF-AUTHORIZATION-SHEET ·
COPYWRITER-DETAILED-OPERATING-INSTRUCTIONS · COPY-REVIEW-SHEET ·
COPY-GRADER-REVIEW-SHEET · COPY-GRADING-RUBRIC · GRADER-RETURN-PACKET-COMPLETE ·
WORKED-EXAMPLE-WEEKLY-CREATIVE-BRIEF · app/ai_prompt_loader.py
**Method:** cross-file term scans + arithmetic verification of score weights.

---

# 1. Verified consistent ✅

1. **Score scales add up.**
   - Creative Grader `/100` = 15+10+15+10+10+10+10+10+10 (nine sections, 0–5).
   - Production Grader `/75` = 15+10+15+15+10+10 (six scored sections; §4 risk
     register gates but scores 0 by design).
   - Copy Grader `/100` = 20+15+15+15+10+10+10+5 (eight categories).
   - Brief Validator `/100` structural (checklist, no weighted sections).
2. **Verdict bands match the template's grader handoff (J).** PASS / PASS WITH
   WARNINGS / BLOCKED; EXCELLENT / STRONG / REVISION REQUIRED / REJECTED;
   READY (CONTENT SCOUT / LOW-COST PROOF) / OWNER REVIEW / BLOCKED — the same
   terms appear in both the sheets and the template.
3. **Authorization threshold is single-sourced.** FINAL-BRIEF-AUTHORIZATION
   "Creative score is at least 80" == STRONG band (80–89) == template K
   "Creative score meets the required threshold".
4. **Auto-fail rules are identical** between COPY-GRADER-REVIEW-SHEET and
   COPY-GRADING-RUBRIC (9 rules: invented fact, unsupported claim, hidden
   disclosure, privacy, clickbait, unverified endorsement, inaccurate
   ingredients, rights misstatement, serious error).
5. **Monday/Wednesday/Friday structure aligned** across template D1/D2
   (publishing-day column) and Validator §2 ("Monday, Wednesday, and Friday
   groupings are defined").
6. **Redo guard is one number everywhere**: max 2, owner override beyond —
   in the sheets, the return packet, and the Creator instructions.
7. **No "score out of 5" contradictions remain.** The app's assistant
   one-liners that said "out of 5" were aligned to the sheets on 2026-09-17;
   a repo-wide scan of the sheets/template now finds none.
8. **Loader mapping matches EMBEDDING spec §1** for the nine wired roles
   (Creative Director, Validator, Creative/Production/Copy Grader, Current
   Events, Fact Check, Cataloger, Copywriter). Roles without files are
   explicitly reported, not silent.
9. **Tile/filename grammar consistent** with The Library E.5: assignment
   label `YYYY_W##_IPTC-Subject-Code_Sequence` vs canonical filename
   date-first — used identically in template, sheets, and worked example.

---

# 2. Findings and recommendations ⚠️

1. **[GAP] Subject-spread rule has no template field.** The Library E.4 (no
   single IPTC subject beyond 5 of 9 posts; target 3–5) is law, but
   WEEKLY-CREATIVE-BRIEF-TEMPLATE has no subject-spread check. The worked
   example demonstrates it inside D2 as a note.
   **Recommendation:** add a "Subject-spread check" block to template D2/D3 on
   its next revision. *Not edited now — in-place edits are paused per owner
   directive; this is queued.*
2. **[GAP] Four roles still run on short prompts only.** Muse, Content
   Scouts, Media Editor, Scheduler have no instruction file; the loader
   reports `(no role instruction file written yet)` and these roles fall back
   to their embedded one-liner prompts.
   **Recommendation:** author MUSE-DETAILED-OPERATING-INSTRUCTIONS.md next,
   then the Media Editor file (from The Library §11–12).
3. **[MINOR] Casing drift on two verdict phrases.** Production sheet says
   "READY FOR LOW-COST PROOF ONLY"; template J says "Low-cost proof only".
   Same meaning. Optionally normalize on next revision.
4. **[MINOR] Production §4 intentionally carries no points** (risk register
   gates the verdict but is not scored). Confirmed as designed; documenting so
   nobody "fixes" it later.
5. **[INFO] Validator /100 has no published section weights** — it is a
   deterministic completeness/timing gate. Fine as designed; keep weights out
   of prompts (three-layer rule).

---

# 3. Stack note (owner-confirmed)

**Azure SQL is the production database (reached via SQLAlchemy + pyodbc
today); Azure Cosmos is the additional store (used by metadata_registry.py).**
SQLite remains the safe local sandbox default. SQLAlchemy removal, if pursued,
is a separate migration phase touching many app files and is not part of this
suite's wiring.

---

**Audit closed by:** ____________________  **Date:** ____________________
**Owner verdict on findings:** [ ] Address GAP 1 on next template revision
[ ] Author Muse file next  [ ] Accept minor items as-is
