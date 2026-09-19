# AI Model Recommendations for the Creative Brief Pipeline

## Purpose

This document defines the recommended model assignments for the Creative Director, Brief Validator, Creative Grader, Production Grader, Muse, Content Scout, and related quality-control steps.

The goal is not to use the largest model for every task. The goal is to use the right model for each task while protecting media-generation credits and requiring human approval before irreversible or expensive work.

---

# 1. Recommended model assignments

The current Microsoft Foundry project has these deployed models:

- `gpt-5.6-luna`
- `gpt-5.6-sol`
- `gpt-4.1`
- `text-embedding-3-small`

## Creative Director — `gpt-5.6-luna`

Use `gpt-5.6-luna` for the highest-reasoning planning work:

- Interpret the owner's theme and broad subjects.
- Create the weekly creative bible.
- Build the nine-post narrative.
- Assign the hero post and supporting posts.
- Write second-by-second timelines.
- Define visual continuity.
- Define music, lyric, vocal, and instrumental direction.
- Create Content Scout search packets.
- Create Media Editor execution instructions.
- Identify uncertainty and owner-review questions.
- Revise briefs after validator and grader feedback.

The Creative Director must return structured data, not only ordinary prose.

Recommended output requirements:

- Exactly nine post objects.
- One object for each position 1 through 9.
- Explicit total duration for every post.
- Timeline beginning at `0.0` seconds.
- Timeline ending at the declared duration.
- No timeline gaps or overlaps.
- Observable actions for every interval.
- Search queries and negative terms for every required shot.
- Acceptance and rejection criteria.
- Fallback plans.
- Production risk for every post.
- Confidence and uncertainty fields.
- No implicit generation authorization.

## Creative Grader — `gpt-5.6-sol`

Use `gpt-5.6-sol` as an independent creative reviewer with a separate role and prompt.

It should evaluate:

- Theme fidelity.
- Emotional progression.
- Nine-post narrative flow.
- Subject integration.
- Hook quality.
- Visual identity.
- Music and audio continuity.
- Originality.
- Brand and taste alignment.
- Distinctness of all nine posts.

The Creative Grader must not automatically rewrite, approve, or authorize the brief. It must return a score, evidence, failing fields, critical failures, and required revisions.

## Production Grader — `gpt-4.1`

Use `gpt-4.1` for rubric-driven feasibility review:

- Searchability.
- Availability of likely footage.
- Timing realism.
- Editability.
- Crop safety.
- Platform requirements.
- Candidate acceptance and rejection criteria.
- Rights and provenance questions.
- Generation-risk identification.
- Credit-waste risk.
- Fallback quality.

The Production Grader may identify that a license, fact, or source needs verification. It must not claim that the item is legally cleared or factually verified without evidence.

## Retrieval and matching — `text-embedding-3-small`

Use `text-embedding-3-small` for semantic retrieval and matching:

- Match brief shot requirements to approved library assets.
- Find media with similar subjects, colors, moods, textures, and camera language.
- Retrieve previous owner decisions from `taste.md`.
- Find similar successful and failed briefs.
- Identify repeated concepts across weeks.
- Match Content Scout candidates against exact shot requirements.
- Retrieve prior rejection reasons and avoid repeating them.

Embeddings should rank and retrieve candidates. They should not make final owner approval decisions.

---

# 2. Recommended workflow

```text
Owner theme and broad subjects
        |
        v
gpt-5.6-luna
Creative Director structured brief
        |
        v
Deterministic Brief Validator
        |
        v
gpt-5.6-sol
Independent Creative Grader
        |
        v
gpt-4.1
Production Grader
        |
        v
Owner review and authorization
        |
        v
text-embedding-3-small + Muse
Library retrieval and matching
        |
        v
Content Scout searches unresolved requirements
        |
        v
Studio candidate review
        |
        v
Media Editor low-cost proof
        |
        v
Owner approval
        |
        v
Final media generation
```

---

# 3. Model separation rules

## Do not use one model for every role

The Creative Director must not be the only judge of her own brief. Self-review tends to produce generous scores and overlook missing production details.

Use separate role prompts and preferably separate deployments:

- Director creates.
- Validator checks structure using application code.
- Creative Grader judges artistic quality.
- Production Grader judges feasibility and risk.
- Owner makes final decisions.

## Do not let graders silently rewrite

Each grader must return:

- Numeric score.
- Category scores.
- Evidence from the brief.
- Critical failures.
- Warnings.
- Exact fields requiring revision.
- Status: `PASS`, `WARN`, `REVISION_REQUIRED`, or `BLOCKED`.

A grader may suggest a correction, but the Creative Director must create a new brief revision and submit it again.

## Critical failures override numeric scores

A brief must be blocked regardless of its score if:

- The nine-post structure is incomplete.
- Timeline intervals have gaps or overlaps.
- Required shots are not searchable.
- Required actions are not observable.
- A major factual claim is unsupported.
- Rights or licensing are unclear for required media.
- A high-risk shot has no fallback.
- The brief requests impossible or contradictory production steps.
- The owner has not approved an unresolved material risk.

---

# 4. Suggested model behavior by task

## Creative Director settings

Use structured output and a low-to-moderate temperature.

Require these output groups:

1. Weekly creative bible.
2. Nine-post narrative map.
3. Individual post briefs.
4. Second-by-second timelines.
5. Content Scout search packets.
6. Media Editor instructions.
7. Acceptance and rejection criteria.
8. Fallback plans.
9. Fact-check queue.
10. Rights and provenance queue.
11. Risk register.
12. Owner review questions.
13. Self-check result.

The model must explicitly say when it is uncertain.

## Creative Grader settings

Use a strict rubric and require evidence.

Recommended categories:

- Theme fidelity — 15 points.
- Emotional direction — 10 points.
- Nine-post narrative flow — 15 points.
- Subject integration — 10 points.
- Hook and retention design — 10 points.
- Visual identity — 10 points.
- Audio and music identity — 10 points.
- Originality — 10 points.
- Brand and taste alignment — 10 points.

Suggested status thresholds:

- `90–100`: Excellent.
- `80–89`: Strong.
- `70–79`: Revision required.
- Below `70`: Reject.

A critical failure blocks the brief even if the total score is high.

## Production Grader settings

Require the grader to inspect each required shot separately.

Recommended categories:

- Searchability — 15 points.
- Footage availability — 10 points.
- Editability — 15 points.
- Technical delivery — 15 points.
- Rights and provenance — 10 points.
- Candidate acceptance rules — 10 points.

Suggested status values:

- `READY_FOR_CONTENT_SCOUT`.
- `READY_FOR_LOW_COST_PROOF_ONLY`.
- `OWNER_REVIEW_REQUIRED`.
- `BLOCKED`.
- `CREATIVE_DIRECTOR_REVISION_REQUIRED`.

The Production Grader should estimate risk per post:

- Low.
- Medium.
- High.
- Critical.

---

# 5. Deterministic checks that must not be delegated to AI

Use regular application code for these checks:

- Exactly nine posts exist.
- Positions are unique and complete.
- Timeline starts at `0.0`.
- Timeline intervals are ordered.
- No gaps exist.
- No overlaps exist.
- End time equals declared duration.
- Required fields are present.
- Durations are valid numbers.
- Platform dimensions are valid.
- Required scores are present.
- Critical-failure flags are respected.
- Approval gates block unauthorized production.
- Revision numbers increase correctly.
- Owner approval is attached to the correct brief revision.

AI is useful for judgment and interpretation. Application code is better for exact structural rules.

---

# 6. How to test whether the models are good enough

Create an evaluation set of approximately 20 themes. Include:

- Simple themes.
- Broad themes.
- Themes with unrelated-looking subjects.
- Themes with limited available media.
- Themes requiring factual review.
- Themes with difficult visual actions.
- Themes requiring people, faces, hands, or text.
- Themes with high generation risk.
- Themes that conflict with prior taste decisions.
- Themes that require fallback planning.

For each test case, record whether the system correctly identifies:

- Missing information.
- Timeline gaps.
- Timeline overlaps.
- Unsearchable shots.
- Weak theme connections.
- Repetitive posts.
- Weak hooks.
- Unsupported claims.
- Rights risks.
- Platform crop risks.
- High credit exposure.
- Missing fallback plans.

## Minimum success standard

Do not judge success only by how polished the brief sounds. The system should reliably produce:

- Few or no structural validation failures.
- Concrete search queries.
- Observable shot requirements.
- Accurate risk identification.
- Useful fallback plans.
- Specific grader criticism.
- Meaningful score differences between strong and weak briefs.

If every brief receives approximately the same score, the grader is too lenient or the rubric is not being enforced.

---

# 7. Recommended first deployment

Start with this configuration:

| Role | Model | Approval authority |
|---|---|---|
| Creative Director | `gpt-5.6-luna` | None; proposal only |
| Brief Validator | Application code | None; structural gate |
| Creative Grader | `gpt-5.6-sol` | None; recommendation only |
| Production Grader | `gpt-4.1` | None; production recommendation only |
| Muse/retrieval | `text-embedding-3-small` plus application ranking | None; candidate recommendation only |
| Owner | Human | Final approval |

Do not add another model provider until testing shows a specific deficiency that the existing setup cannot solve.

---

# 8. Credit-protection policy

- Never spend final-generation credits on an unvalidated brief.
- Never generate all nine posts to test one uncertain shot.
- Test high-risk shots separately.
- Use approved library media before external or generated media.
- Use deterministic editing before generative editing when possible.
- Use low-cost proofs before final renders.
- Record estimated credit use before generation.
- Record maximum expected redo count.
- Stop and return the brief when no candidate satisfies the acceptance criteria.
- Require owner authorization before moving from proof to final generation.

The purpose of the graders is not simply to produce scores. It is to prevent the system from spending resources on a brief that is unclear, unsearchable, impossible, or likely to be rejected.

---

# 9. Final recommendation

The currently deployed models are sufficient for the first reliable version:

- Use `gpt-5.6-luna` as the Creative Director.
- Use `gpt-5.6-sol` as the independent Creative Grader.
- Use `gpt-4.1` as the Production Grader and fact-check triage assistant.
- Use `text-embedding-3-small` for library, taste, and candidate retrieval.
- Use deterministic application code for exact validation and approval gates.
- Keep the owner as the final approval authority.

The quality will come from the combination of model roles, structured output, hard validation, independent grading, production-risk review, and feedback from actual rejected candidates—not from adding more models alone.
