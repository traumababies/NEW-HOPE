# Current Events and Fact-Check Workflow

## Purpose

Current Events and Fact Check are separate assistants with separate responsibilities.

- **Current Events** discovers timely, relevant developments that may strengthen the approved weekly content plan.
- **Fact Check** verifies whether proposed claims are supported, current, accurately worded, and safe to use.
- **Creative Director** integrates only approved claims into the Creative Brief.
- **Copywriter** expresses approved claims but may not introduce new factual claims.
- **Owner** approves the final brief and any material risk.

The central rule is:

> **Current Events proposes. Fact Check verifies. Creative Director integrates. Copywriter expresses. Owner approves.**

Neither Current Events nor Fact Check should independently rewrite the Creative Brief or authorize publication.

---

# 1. Where these assistants fit

```text
Owner theme and subjects
        ↓
Creative Director creates nine ideas
        ↓
Current Events finds timely angles
        ↓
Fact Checker verifies claims
        ↓
Creative Director integrates approved claims
        ↓
Creative Grader reviews the brief
        ↓
Owner approves the brief
        ↓
Muse and downstream production begin
```

Claims that fail Fact Check must not silently return to the Creative Brief.

---

# 2. Do not force current events into every post

Every post should receive a content classification:

- `evergreen`
- `current_context`
- `current_claim`
- `trend_reference`
- `owner_original`

Use Current Events only when freshness adds genuine value.

Do not force a current event into an educational, product, or creative post merely to make it appear timely. Forced relevance weakens the content and increases factual risk.

Recommended limits:

- Maximum three research claims per subject.
- Usually use no more than one approved current claim per post.
- Do not automatically create 27 claims for a nine-post week.
- Every claim used in the brief must have a source and verification record.

---

# 3. Current Events contract

## Inputs

Current Events receives:

- Weekly theme.
- Nine subject list.
- Creative Director's subject angles.
- Freshness window.
- Current date and timezone.
- Geographic scope.
- Audience.
- Maximum claims per subject.
- Allowed source types.
- Excluded topics.
- Product or brand context when relevant.

## Output

Current Events returns structured claim candidates:

```json
[
  {
    "claim_id": "",
    "subject_code": "",
    "claim": "",
    "why_relevant": "",
    "source_url": "",
    "source_name": "",
    "source_type": "",
    "source_tier": "",
    "source_published_at": "",
    "event_date": "",
    "as_of_date": "",
    "valid_from": "",
    "review_by": "",
    "expires_on": "",
    "geographic_scope": "",
    "claim_type": "",
    "evidence_excerpt": "",
    "confidence": 0.0,
    "developing_story": false,
    "risks": [],
    "suggested_wording": ""
  }
]
```

## Required fields

Every proposed claim must include:

- Claim ID.
- Subject code.
- Exact claim.
- Why it fits the theme and subject.
- Source URL.
- Source name.
- Source type.
- Source tier.
- Source publication date.
- Event date, if different.
- As-of date.
- Freshness window.
- Geographic scope.
- Evidence excerpt.
- Confidence.
- Expiration or review date.
- Potential risks.
- Suggested wording.

No URL means the claim is not eligible for Fact Check.

---

# 4. Freshness windows

The assistant must declare the freshness window before researching.

| Content type | Suggested window |
|---|---|
| Breaking event | Last 24–72 hours |
| Current week | Last 7 days |
| Recent development | Last 30 days |
| Seasonal context | Current season/year |
| Evergreen fact | No current-events window, but factual verification may still be required |
| Historical fact | Stable source and clear historical date context |
| Product information | Current approved product record and review date |

Every research package must state:

```text
Research window:
Current/as-of date:
Timezone:
Geographic scope:
Search completed at:
```

Do not present an old article as a current development without explicitly labeling it.

---

# 5. Source hierarchy

## Preferred primary sources

- Government agencies.
- Universities and research institutions.
- Official company or organization sources.
- Primary datasets.
- Court, regulatory, or public records.
- Original scientific papers.
- Official statements from the relevant authority.

## Acceptable secondary sources

- Established journalism with named sources.
- Reputable wire services.
- Professional associations.
- Industry publications with transparent sourcing.

## Discovery-only sources

These may identify leads but should not be final evidence for important claims:

- Social posts.
- Influencers.
- Aggregator pages.
- Unsourced blogs.
- Search snippets.
- AI-generated summaries.
- Anonymous posts.

Every claim should include source quality and whether the source is primary or secondary.

---

# 6. Fact Checker contract

## Inputs

Fact Checker receives:

- Current Events claims payload.
- Approved theme.
- Subject context.
- Research window.
- Current/as-of date.
- Geographic scope.
- Source requirements.
- Relevant owner or product context.

## Output

```json
[
  {
    "claim_id": "",
    "claim": "",
    "verdict": "verified",
    "evidence_urls": [],
    "evidence_excerpts": [],
    "confidence": 0.0,
    "source_quality": "",
    "scope_check": "",
    "date_check": "",
    "context_check": "",
    "contradictory_sources": [],
    "note": "",
    "valid_until": "",
    "recommended_wording": ""
  }
]
```

## Allowed verdicts

- `verified`
- `partially_verified`
- `unverified`
- `contradicted`
- `out_of_date`
- `misleading_context`
- `not_applicable`
- `cannot_verify`

The Fact Checker must be conservative and must be allowed to say `cannot_verify`.

> `cannot_verify` means the claim is not approved for factual publication.

---

# 7. Fact-check procedure

For every claim:

1. Read the exact wording proposed by Current Events.
2. Open and inspect the source URL.
3. Locate the relevant evidence passage.
4. Compare the claim with the source exactly.
5. Check whether the source is primary or secondary.
6. Check publication date.
7. Check event date.
8. Check geographic scope.
9. Check whether the claim is still current.
10. Check whether important context is missing.
11. Search for credible contradictory evidence when the claim is material.
12. Determine whether the wording exaggerates certainty.
13. Record the verdict and confidence.
14. Record expiration or refresh date.
15. Provide safe wording only when the evidence supports it.

The Fact Checker must not:

- Invent or recall sources.
- Treat a URL alone as proof.
- Approve a claim because it sounds plausible.
- Replace missing evidence with confidence.
- Turn partial evidence into a broad claim.
- Hide contradictory sources.
- Rewrite the Creative Brief.
- Add creative content of its own.
- Approve publication.

---

# 8. Claim ledger

Every researched claim must be stored in a durable claim ledger.

```text
Claim ID:
Subject code:
Weekly theme:
Post position:
Exact claim:
Proposed wording:
Source URL:
Source name:
Source type:
Source tier:
Source publication date:
Event date:
As-of date:
Research window:
Geographic scope:
Evidence excerpt:
Fact Checker verdict:
Confidence:
Contradictory sources:
Valid from:
Review by:
Expires on:
Used in post:
Owner review status:
```

Do not store only a URL. Store the exact evidence excerpt reviewed and the exact wording approved.

---

# 9. Claim classification

Separate factual claims from creative language.

## Verified fact

A statement supported by evidence and approved by Fact Check.

## Creative interpretation

A clearly framed artistic or editorial interpretation that does not pretend to be an objective fact.

## Owner opinion

The owner's perspective, clearly expressed as opinion or brand position.

## Unverified claim

A proposed statement that cannot currently be supported. Do not publish it as fact.

Use labels when necessary:

```text
Verified fact:
The source states ...

Creative interpretation:
This post frames the idea as ...

Owner perspective:
Our view is ...

Unverified:
Do not publish as factual.
```

A poetic metaphor should not accidentally become a scientific, business, historical, cultural, financial, or product claim.

---

# 10. Expiration and refresh rules

Current claims become stale. Each approved claim should have:

- `valid_from`
- `review_by`
- `expires_on`
- `requires_refresh`

Recommended behavior:

- Breaking event: refresh immediately before publication.
- Current statistic: refresh at publication time.
- Seasonal trend: refresh weekly.
- Historical fact: normally no expiration, but retain source context.
- Product information: refresh when formula, price, policy, or availability changes.
- Developing story: refresh before every publication.

If `expires_on` passes, the claim must return to Fact Check before use.

---

# 11. Recommended gates

## Gate 1 — Research relevance

Current Events must confirm:

- [ ] Claim relates to the weekly theme.
- [ ] Claim relates to the assigned subject.
- [ ] Source fits the allowed source policy.
- [ ] Source is within the freshness window.
- [ ] Claim provides audience value.
- [ ] Claim does not force current context into an unrelated post.
- [ ] Claim has a source URL.
- [ ] Claim has an evidence excerpt.

## Gate 2 — Fact verification

Fact Checker must confirm:

- [ ] Source URL exists.
- [ ] Source is accessible.
- [ ] Evidence supports the exact wording.
- [ ] Dates are correct.
- [ ] Scope is correct.
- [ ] Important context is not omitted.
- [ ] Contradictory evidence was considered where material.
- [ ] Confidence is recorded.
- [ ] Expiration is recorded.
- [ ] Safe wording is supplied or claim is rejected.

## Gate 3 — Creative integration

Creative Director may use a factual claim only when it is:

- `verified`, or
- explicitly framed as owner opinion or creative interpretation rather than fact.

The Creative Director must not use:

- `unverified`
- `contradicted`
- `out_of_date`
- `misleading_context`
- `cannot_verify`

## Gate 4 — Copywriting

Copywriter may express approved claims but may not introduce new factual claims.

If Copywriter adds a new claim:

1. Add it to the claim ledger.
2. Send it to Fact Check.
3. Block publishing until it is resolved.

## Gate 5 — Publication

Before publishing:

- [ ] Claim is not expired.
- [ ] Source still supports the wording.
- [ ] Caption wording matches the verified wording.
- [ ] No new unsupported factual claim was added.
- [ ] Attribution is included when required.
- [ ] Commercial or affiliate disclosure is correct when applicable.
- [ ] Owner approval is attached to the current brief revision.

---

# 12. Handling failed claims

## Contradicted

- Remove the claim from the Brief.
- Preserve the rejected claim and evidence in History.
- Record why it was contradicted.
- Do not silently replace it with a similar claim.
- Return the gap to Creative Director if the post needs a new angle.

## Unverified or cannot verify

- Do not publish it as fact.
- Keep it out of the Brief's factual claim set.
- Record the missing evidence.
- Do not blindly retry the same research.
- Permit re-check only when new evidence or a changed scope is supplied.

## Partially verified

- Narrow the wording to the supported portion, or reject it.
- Send the narrowed wording through Fact Check again.
- Do not preserve unsupported implications.

## Out of date

- Mark the claim expired.
- Refresh it within the correct window.
- Do not present it as current.

## Misleading context

- Explain what context is missing.
- Rewrite only after the relevant context is included.
- Re-run Fact Check on the revised claim.

---

# 13. Current Events review worksheet

**Week/theme:**  
**Subject code:**  
**Researcher:**  
**As-of date:**  
**Timezone:**  
**Geographic scope:**  
**Freshness window:**  

## Claim candidate

**Claim ID:**  
**Exact claim:**

> 

**Why it fits the theme and subject:**

> 

**Suggested wording:**

> 

**Claim type:** [ ] Current event [ ] Statistic [ ] Trend [ ] Policy [ ] Research [ ] Other  
**Developing story:** [ ] Yes [ ] No  

## Source review

**Source URL:**  
**Source name:**  
**Source type:**  
**Source tier:**  
**Publication date:**  
**Event date:**  

**Evidence excerpt:**

> 

- [ ] URL is present.
- [ ] Source is accessible.
- [ ] Source is within the declared window.
- [ ] Source is appropriate for the claim.
- [ ] Geographic scope is clear.
- [ ] Contradictory sources were considered when necessary.
- [ ] Expiration date is assigned.

**Current Events status:**

- [ ] Ready for Fact Check.
- [ ] Needs better source.
- [ ] Not relevant.
- [ ] Do not use.

---

# 14. Fact Check review worksheet

**Claim ID:**  
**Fact Checker:**  
**Date checked:**  

**Claim reviewed:**

> 

**Source URL:**  
**Evidence excerpt:**

> 

## Verification checklist

- [ ] Exact wording matches the evidence.
- [ ] Source quality is acceptable.
- [ ] Source date is checked.
- [ ] Event date is checked.
- [ ] Geographic scope is checked.
- [ ] Important context is included.
- [ ] Contradictory evidence was considered.
- [ ] Claim does not exaggerate certainty.
- [ ] Product, scientific, health, financial, or legal implications were checked where relevant.
- [ ] Confidence is recorded.
- [ ] Expiration or review date is recorded.

**Verdict:**

- [ ] VERIFIED.
- [ ] PARTIALLY VERIFIED.
- [ ] UNVERIFIED.
- [ ] CONTRADICTED.
- [ ] OUT OF DATE.
- [ ] MISLEADING CONTEXT.
- [ ] CANNOT VERIFY.

**Safe wording, if any:**

> 

**Reason:**

> 

**Evidence URLs:**

- 

**Contradictory sources:**

- 

**Valid until:**  
**Refresh required:** [ ] Yes [ ] No  

---

# 15. Publication claim check

Complete immediately before publication.

**Post:**  
**Brief revision:**  
**Copy revision:**  
**Publication date/time:**  

- [ ] Every factual claim in the caption is in the claim ledger.
- [ ] Every claim has a passing verdict.
- [ ] No claim is expired.
- [ ] Caption wording matches approved wording.
- [ ] Copywriter did not add an unverified claim.
- [ ] Current-event attribution is included where needed.
- [ ] Affiliate/sponsorship disclosure is included where needed.
- [ ] Owner approval is attached to this revision.

**Publication status:**

- [ ] CLEARED.
- [ ] HOLD FOR REFRESH.
- [ ] HOLD FOR FACT CHECK.
- [ ] BLOCKED.

---

# 16. Required application behavior

The application should enforce these rules:

- Current Events cannot write directly into the Creative Brief.
- Fact Check verdicts must be stored with evidence and timestamps.
- Contradicted claims are removed from usable claim sets.
- Unverified claims are excluded from factual content.
- Expired claims cannot pass the publication gate.
- Copywriter-added factual claims reopen Fact Check.
- Owner approval is tied to a specific brief and copy revision.
- Every decision is written to History and available for future learning.
- Grader scores do not override critical claim failures.

---

# 17. Final standard

The workflow succeeds when it can answer:

- What is the claim?
- Why does it belong in this week's theme?
- What source supports it?
- What exact evidence was reviewed?
- How current is it?
- What geography and scope apply?
- Is it verified, partially verified, unverified, contradicted, stale, or misleading?
- When must it be refreshed?
- What wording is safe?
- Did the Creative Director use it correctly?
- Did the Copywriter introduce any new claim?
- Did the owner approve the final revision?

If those questions cannot be answered, the claim is not ready for publication.

**Current Events status:** READY FOR FACT CHECK  
**Fact Check status:** READY FOR CREATIVE INTEGRATION  
**Publication status:** OWNER APPROVAL REQUIRED
