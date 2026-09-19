# AI Video Generator — Detailed Instructions and Check-Off Worksheet

## Purpose

The AI Video Generator creates only the approved shot or transformation defined by the Creative Brief. It does not invent the campaign, rewrite the story, choose a different subject, or decide whether a result is acceptable.

The generator must protect credits by proving one uncertain shot at a time before producing a final render.

---

# 1. Job authorization

**Week/theme:**  
**Post position:**  
**Post title:**  
**Shot number:**  
**Brief revision:**  
**Generator/operator:**  
**Date:**  

## Authorization status

- [ ] Brief Validator passed.
- [ ] Creative Grader passed or owner approved an exception.
- [ ] Production Grader approved this shot.
- [ ] Existing Library media was searched first.
- [ ] Deterministic editing was considered first.
- [ ] Generation is necessary for this shot.
- [ ] Proof generation is authorized.
- [ ] Final generation is authorized.
- [ ] Owner approval is required before proceeding.

**Generation status:**

- [ ] NOT_READY
- [ ] SOURCE_FIRST
- [ ] EDIT_FIRST
- [ ] PROOF_AUTHORIZED
- [ ] PROOF_FAILED
- [ ] OWNER_REVIEW_REQUIRED
- [ ] FINAL_GENERATION_AUTHORIZED
- [ ] APPROVED
- [ ] FINAL_FAILED_USE_FALLBACK

**Estimated credit cost:**  
**Maximum attempts allowed:**  
**Attempts already used:**  
**Fallback:**  

---

# 2. One-shot rule

The generator must describe one observable job for this shot.

**The one thing this shot must visibly accomplish:**

> 

**What the shot must not attempt to accomplish:**

> 

Do not combine unrelated risks such as:

- New character identity.
- Complex hand movement.
- Exact product packaging.
- Small text.
- Lip synchronization.
- Multiple transformations.
- Complex camera movement.
- Precise scientific action.

If more than one major risk exists, split the work into separate proofs.

---

# 3. Source and fallback decision

## Existing media check

- [ ] Approved Library media satisfies the requirement.
- [ ] Approved Library media partially satisfies the requirement.
- [ ] Muse found no suitable Library media.
- [ ] Content Scout found no suitable temporary candidate.
- [ ] Deterministic editing cannot produce the required result.
- [ ] Generation is the least expensive acceptable method.

**Why existing media/editing is insufficient:**

__________________________________________________

## Fallback hierarchy

- [ ] Approved Library asset.
- [ ] Approved Content Scout asset.
- [ ] Deterministic edit using approved assets.
- [ ] Animated still or controlled motion.
- [ ] Low-cost generated proof.
- [ ] Final generated shot.
- [ ] Rewrite the shot.

**Fallback if this attempt fails:**

__________________________________________________

---

# 4. Shot contract

## Duration and format

**Proof duration:** ______ seconds  
**Final duration:** ______ seconds  
**Aspect ratio:**  
**Resolution:**  
**Frame rate:**  
**Orientation:** [ ] Vertical [ ] Square [ ] Horizontal  
**Platform:** [ ] TikTok [ ] Instagram [ ] Both  

## Required subject

> 

## Required action

Describe what must visibly happen, using observable verbs.

> 

## Starting state

> 

## Ending state

> 

## Action timing

- Action begins by: ______ seconds.
- Main action is clearly visible by: ______ seconds.
- Action ends by: ______ seconds.
- Final usable frame occurs at: ______ seconds.

## Camera

**Camera position:**  
**Framing:**  
**Camera movement:**  
**Motion direction:**  
**Lens/depth-of-field intention:**  
**Stability:** [ ] Locked [ ] Smooth motion [ ] Handheld [ ] Other  

## Visual style

**Palette:**  
**Lighting direction:**  
**Shadow quality:**  
**Texture:**  
**Background:**  
**Mood evidence:**  

## Continuity

**Continuity from previous shot:**

> 

**Continuity into next shot:**

> 

**Objects that must remain unchanged:**

> 

**Position that must remain unchanged:**

> 

---

# 5. Prompt worksheet

## Positive prompt

Write only requirements that can be judged in the generated pixels.

> 

## Negative prompt

List unwanted subjects, actions, styles, defects, and continuity failures.

> 

## Reference inputs

- [ ] Approved image reference.
- [ ] Approved video reference.
- [ ] Color reference.
- [ ] Composition reference.
- [ ] Character/subject reference.
- [ ] Product reference.
- [ ] No reference used.

**Reference IDs and purpose:**

__________________________________________________

## Prompt check-off

- [ ] Duration is stated.
- [ ] Aspect ratio is stated.
- [ ] Subject is stated.
- [ ] Action is stated.
- [ ] Starting state is stated.
- [ ] Ending state is stated.
- [ ] Action timing is stated.
- [ ] Camera is stated.
- [ ] Lighting is stated.
- [ ] Palette is stated.
- [ ] Continuity is stated.
- [ ] Prohibited elements are stated.
- [ ] Prompt does not request important text inside generated footage.
- [ ] Prompt does not request an unverified brand or product package.
- [ ] Prompt does not use vague direction as the only instruction.

---

# 6. Proof-generation procedure

The proof is a test, not the final video.

- [ ] Generate the shortest useful duration.
- [ ] Use the lowest acceptable proof resolution.
- [ ] Exclude final captions and music unless audio is the uncertainty being tested.
- [ ] Test the main action first.
- [ ] Test crop safety.
- [ ] Test continuity.
- [ ] Save the proof with a unique version ID.
- [ ] Record model, settings, prompt, seed, and reference inputs.
- [ ] Review the complete proof, not just one frame.

## Proof questions

- Does the correct subject appear?
- Does the required action actually happen?
- Is the action visible early enough?
- Is the motion physically readable?
- Does the camera behave as requested?
- Is the crop safe?
- Does the palette match?
- Does the lighting match?
- Are there unwanted objects?
- Are hands, faces, objects, and edges intact?
- Does the ending frame support the edit?
- Can the shot connect to the neighboring shot?

**Proof result:**

- [ ] PASS.
- [ ] PASS WITH WARNINGS.
- [ ] FAIL — revise one variable.
- [ ] FAIL — use fallback.
- [ ] OWNER REVIEW REQUIRED.

**Proof evidence and timestamps:**

__________________________________________________

---

# 7. Failure log

After every failed generation, record the specific failure. Never write only “make it better.”

| Attempt | Failure type | Timestamp | What failed | One variable to change | Next action |
|---:|---|---|---|---|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |

Failure categories:

- [ ] Wrong subject.
- [ ] Missing action.
- [ ] Action not visible.
- [ ] Action occurs too late.
- [ ] Wrong camera movement.
- [ ] Bad crop.
- [ ] Deformed hands.
- [ ] Deformed face.
- [ ] Broken object.
- [ ] Broken product identity.
- [ ] Broken text.
- [ ] Unwanted object.
- [ ] Wrong color.
- [ ] Wrong lighting.
- [ ] Wrong mood.
- [ ] Poor continuity.
- [ ] Too much motion.
- [ ] Not enough motion.
- [ ] Audio failure.
- [ ] Rights/provenance concern.

**Retry rule:** After two failures of the same type, stop random retries and use the fallback or return the shot for rewrite.

---

# 8. Final-generation checklist

Final generation may begin only when:

- [ ] Proof passed.
- [ ] Required action is visible.
- [ ] Start state is correct.
- [ ] End state is correct.
- [ ] Camera movement is acceptable.
- [ ] Crop is safe.
- [ ] Palette and lighting match.
- [ ] Continuity is acceptable.
- [ ] No prohibited objects or people appear.
- [ ] Faces, hands, products, and text are acceptable.
- [ ] Final duration is authorized.
- [ ] Final credit estimate is recorded.
- [ ] Retry limit is recorded.
- [ ] Owner or authorized reviewer approved the proof.

**Final-generation authorization:** ____________________  
**Date:** ____________________

---

# 9. Final shot review

- [ ] Correct source/model/settings are recorded.
- [ ] Final media opens correctly.
- [ ] Required subject is visible.
- [ ] Required action occurs.
- [ ] Action occurs at the required time.
- [ ] Start and end states are usable.
- [ ] Camera follows the brief.
- [ ] Color and lighting follow the weekly bible.
- [ ] Crop works for all approved platforms.
- [ ] No unwanted text appears.
- [ ] No unwanted logos appear.
- [ ] No unwanted people or objects appear.
- [ ] No major artifacts appear.
- [ ] Audio is synchronized if applicable.
- [ ] The shot can be edited at the assigned timeline position.
- [ ] Provenance and generation settings are stored.
- [ ] Grader review is complete.
- [ ] Owner approval is complete where required.

**Final shot status:**

- [ ] APPROVED.
- [ ] APPROVED WITH WARNINGS.
- [ ] RETURN TO GENERATOR.
- [ ] USE FALLBACK.
- [ ] REWRITE BRIEF.

**Operator notes:**

__________________________________________________
