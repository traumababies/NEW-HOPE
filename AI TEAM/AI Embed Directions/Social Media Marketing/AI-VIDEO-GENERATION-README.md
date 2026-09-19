# AI Video Generation README

## Purpose

AI video generation is a high-risk production step. It should be used only after the system has proved that existing Library media and deterministic editing cannot satisfy the approved Creative Brief.

The AI Video Generator creates a specific approved shot. It does not invent the campaign, rewrite the weekly theme, choose a different subject, decide whether the result is acceptable, or authorize its own final generation.

The workflow is designed to protect credits by testing one uncertain shot at a time before producing a final render.

---

# Quick-start workflow

```text
Creative Brief
    ↓
Brief Validator
    ↓
Creative Grader
    ↓
Production Grader
    ↓
Muse Library search
    ↓
Content Scout search
    ↓
Deterministic edit attempt
    ↓
Short generated proof
    ↓
Proof review
    ↓
Owner or authorized approval
    ↓
Final generated shot
    ↓
Media Editor assembly
    ↓
Final video review
```

Do not skip directly from a theme to full-video generation.

---

# Files used for this workflow

- `AI-VIDEO-GENERATOR-DETAILED-INSTRUCTIONS-WORKSHEET.md`  
  Instructions and check-off worksheet for the generator or operator.

- `AI-VIDEO-GENERATION-GRADER-REVIEW-SHEET.md`  
  Independent quality review of a generated proof or final shot.

- `AI-VIDEO-PROOF-AND-CREDIT-REVIEW-SHEET.md`  
  Authorization sheet used before spending final-generation credits.

- `CREATIVE-DIRECTOR-DETAILED-INSTRUCTIONS.md`  
  Defines the creative and production requirements that the generated shot must satisfy.

- `PRODUCTION-GRADER-REVIEW-SHEET.md`  
  Determines whether generation is technically feasible and worth the risk.

---

# 1. Classify the shot before generating

Every shot must be assigned a production tier.

## Tier 1 — Existing approved media

Use existing Library media when it satisfies the requirement.

Examples:

- An approved autumn leaf close-up.
- An approved laboratory clip.
- An approved product image.
- An owner-approved business scene.

No generative credits should be used.

## Tier 2 — Deterministic editing

Use ordinary editing tools when they can create the result:

- Cropping.
- Reframing.
- Speed changes.
- Zooms or pans across still images.
- Color correction.
- Text overlays.
- Simple transitions.
- Layering.
- Masking.
- Reordering.
- Sound design.

Do not generate video merely because an edit would be less exciting.

## Tier 3 — Low-risk generation

Generate a short isolated shot for:

- Abstract backgrounds.
- Light, smoke, leaves, water, or particles.
- Simple object movement.
- Atmospheric transitions.
- Texture or environmental motion.

## Tier 4 — High-risk generation

Treat these as expensive and require proof review:

- Human hands.
- Faces.
- Multiple people.
- Exact text.
- Product packaging.
- Scientific procedures.
- Complex cause-and-effect actions.
- Precise object continuity.
- Lip synchronization.
- Branded environments.
- Multiple actions in one shot.

---

# 2. The one-shot rule

Each generation request must have one observable job.

Weak request:

> Make a beautiful cinematic autumn chemistry video.

Strong request:

> Generate a three-second vertical macro shot of a clear glass vessel. A visible amber liquid stream enters from the upper-right and mixes with the liquid already in the vessel. Keep the vessel centered, use warm copper light, and make the action readable by 0.7 seconds. No people, labels, logos, flames, smoke, or extra vessels.

The generator should not combine multiple major risks in one request, such as:

- New character identity.
- Complex hands.
- Exact packaging.
- Small text.
- Lip synchronization.
- Multiple transformations.
- Complex camera movement.
- Precise scientific behavior.

Split those into separate proofs.

---

# 3. What every shot contract must contain

Before generation, document:

- Week and post position.
- Brief revision.
- Shot number.
- One observable objective.
- Proof duration.
- Final duration.
- Aspect ratio.
- Resolution.
- Frame rate.
- Platform.
- Required subject.
- Required action.
- Starting state.
- Ending state.
- Exact action timing.
- Camera position and framing.
- Camera movement.
- Motion direction.
- Lighting.
- Palette.
- Texture.
- Continuity from the previous shot.
- Continuity into the next shot.
- Negative requirements.
- Acceptance criteria.
- Rejection criteria.
- Fallback.
- Maximum attempts.
- Estimated credit cost.

If any material field is missing, generation should be blocked or returned for clarification.

---

# 4. Prompt-writing rules

## Positive prompt

Write requirements that can be judged in the generated pixels:

- Subject.
- Observable action.
- Starting and ending states.
- Camera.
- Timing.
- Lighting.
- Color.
- Texture.
- Composition.
- Continuity.

## Negative prompt

List unwanted:

- Subjects.
- Objects.
- Actions.
- Colors.
- Camera behavior.
- Text.
- Logos.
- Faces or people.
- Artifacts.
- Continuity failures.

## Do not rely on vague language

These may describe intent, but they are not sufficient instructions:

- Cinematic.
- Beautiful.
- Emotional.
- Powerful.
- Inspiring.
- Premium.
- Authentic.
- Magical.

Translate them into observable evidence: camera, light, movement, texture, timing, sound, and visible action.

## Avoid generated text and packaging

AI video often produces unreliable:

- Small text.
- Labels.
- Logos.
- Product names.
- Scientific notation.
- Packaging details.

Generate a clean visual shot and add important text or approved product imagery deterministically in Media Editor.

---

# 5. Proof-first generation

A proof is a test, not the final video.

For a risky shot:

1. Generate the shortest useful duration.
2. Use the lowest acceptable proof resolution.
3. Exclude final captions and music unless audio is the uncertainty.
4. Test the main action first.
5. Test crop safety.
6. Test continuity.
7. Save the proof with a unique version ID.
8. Record model, settings, prompt, seed, and references.
9. Review the entire proof.
10. Approve final generation only if the proof passes.

The proof must answer:

- Is the subject correct?
- Does the required action happen?
- Is the action readable early enough?
- Is the camera correct?
- Is the crop safe?
- Do the palette and lighting match?
- Are unwanted objects absent?
- Are faces, hands, objects, and edges intact?
- Can the ending connect to the next shot?

---

# 6. Retry policy

Never retry indefinitely.

Before generating, record:

- Maximum proof attempts.
- Maximum final attempts.
- Maximum credit budget.
- Which failures justify another attempt.
- When the shot must be replaced.
- When the Creative Director must rewrite the brief.

Recommended default:

```text
Proof attempts: 3
Final attempts: 2
Maximum total attempts: 5
```

After two failures of the same type:

- Stop random retries.
- Record the failure.
- Change one specific variable or use the fallback.
- Return the shot to the Creative Director if the requirement is unrealistic.

Do not write “make it better.” Write the exact failure and exact correction.

Example:

```text
Failure:
The liquid was present, but it never visibly entered the vessel.

Correction:
The stream must begin outside the vessel at 0.0 seconds, cross into frame by 0.3 seconds, and visibly contact the liquid surface by 0.7 seconds. Keep the stream continuous until 2.4 seconds.
```

---

# 7. Final-generation gate

Final generation is blocked until all applicable conditions are checked:

- [ ] Brief Validator passed.
- [ ] Creative Grader passed or owner approved an exception.
- [ ] Production Grader approved the shot.
- [ ] Existing Library media was searched.
- [ ] Content Scout was used when required.
- [ ] Deterministic editing was considered.
- [ ] A fallback exists.
- [ ] Proof passed.
- [ ] Acceptance criteria are satisfied.
- [ ] No critical defect remains.
- [ ] Estimated credit cost is recorded.
- [ ] Retry limit is recorded.
- [ ] Owner or authorized reviewer approved the proof.
- [ ] Generation settings and provenance will be retained.

Recommended status values:

- `NOT_READY`
- `SOURCE_FIRST`
- `EDIT_FIRST`
- `PROOF_AUTHORIZED`
- `PROOF_FAILED`
- `OWNER_REVIEW_REQUIRED`
- `FINAL_GENERATION_AUTHORIZED`
- `FINAL_FAILED_USE_FALLBACK`
- `APPROVED`

---

# 8. Generated-shot acceptance test

A shot passes only when:

- [ ] Correct subject is visible.
- [ ] Required action occurs.
- [ ] Action occurs at the required time.
- [ ] Start state is correct.
- [ ] End state is usable.
- [ ] Camera movement matches the brief.
- [ ] Palette matches the weekly creative bible.
- [ ] Lighting matches the weekly creative bible.
- [ ] Crop is safe for TikTok and Instagram.
- [ ] No unwanted people appear.
- [ ] No unwanted objects appear.
- [ ] No unwanted logos or text appear.
- [ ] Faces, hands, and objects are acceptable.
- [ ] The shot can be edited into the assigned timeline.
- [ ] The shot connects to neighboring shots.
- [ ] Provenance is recorded.
- [ ] Grader review is complete.
- [ ] Owner approval is complete where required.

---

# 9. Credit-protection rules

- Never generate a full video to test one uncertain shot.
- Never generate before considering Library media.
- Never generate before considering deterministic editing.
- Never generate important text inside the video when it can be overlaid later.
- Never generate a product package as a substitute for the approved product asset.
- Never retry without recording the prior failure.
- Never change many variables at once when diagnosing a failure.
- Never allow a high semantic or aesthetic score to override a failed required-action check.
- Never use a beautiful but irrelevant clip merely because it looks good.
- Never spend final credits without a passed proof.
- Stop when the brief is impossible and use a documented fallback.

---

# 10. Review files

Use these files in order:

1. `AI-VIDEO-GENERATOR-DETAILED-INSTRUCTIONS-WORKSHEET.md`
2. `AI-VIDEO-PROOF-AND-CREDIT-REVIEW-SHEET.md`
3. `AI-VIDEO-GENERATION-GRADER-REVIEW-SHEET.md`

The generator fills out the first worksheet. The proof and credit reviewer authorizes or blocks final generation. The independent grader evaluates the actual proof or final shot.

---

# 11. Final principle

The AI should generate the pixels. It should not decide:

- The campaign concept.
- The story.
- The timing.
- The acceptance standard.
- The fallback.
- The budget.
- The owner approval.

One observable job per shot, one short proof before final generation, one recorded failure reason per retry, and one explicit acceptance test are the foundation of credit-efficient AI video production.
