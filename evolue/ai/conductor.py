"""The Conductor — AI agent orchestrator.

Watches the pipeline state and auto-triggers the next step.
Handles retry loops (max 2), JAN gates, and feedback injection.

Before each AI call, injects training knowledge from the decision ledger.
After each decision, records to the ledger for future learning.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone

from .decision_ledger import DecisionRecord, record_decision, get_taste_tags
from .training_knowledge import load_knowledge_for_prompt, distill_knowledge
from .runners import run_role
from .prompt_loader import operating_context_text

log = logging.getLogger(__name__)
MAX_REDO = 2


@dataclass
class PipelineEvent:
    step: str
    action: str
    entity_id: str
    result: str
    provider_used: str = ""
    timestamp: str = ""
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()


@dataclass
class ConductorState:
    week_id: str
    events: list[PipelineEvent] = field(default_factory=list)
    redo_counts: dict[str, int] = field(default_factory=dict)
    blocked_at: list[str] = field(default_factory=list)

    def log_event(self, step, action, entity_id, result, provider=""):
        self.events.append(PipelineEvent(step, action, entity_id, result, provider))

    def get_redo_count(self, entity_id):
        return self.redo_counts.get(entity_id, 0)

    def increment_redo(self, entity_id):
        self.redo_counts[entity_id] = self.get_redo_count(entity_id) + 1
        return self.redo_counts[entity_id]


def build_context(week_id: str, extra: str = "") -> str:
    """Build context for an AI role, injecting training knowledge."""
    parts = [operating_context_text()]
    knowledge = load_knowledge_for_prompt()
    if knowledge:
        parts.append(knowledge)
    tags = get_taste_tags()
    if tags:
        parts.append(f"TASTE TAGS (from past rejections): {', '.join(tags)}")
    if extra:
        parts.append(extra)
    return "\n\n".join(parts)


def conductor_run_brief(week, context_extra=""):
    """Conductor runs the full Creative Brief pipeline with retry loops.

    CD → Current Events → Fact Check → Validator → Creative Grader → Production Grader
    If graders reject: re-run CD with feedback (max 2 times).
    Every decision recorded to the ledger for training.
    """
    state = ConductorState(week_id=f"{week.year}_W{week.week_number:02d}")
    ctx = build_context(state.week_id, context_extra)

    # Step 2: Creative Director
    state.log_event("CD", "start", state.week_id, "running")
    cd_result = run_role("creative_director",
        f"Create the weekly Creative Brief for Week {week.week_number}, {week.year}.\n"
        f"Theme: {week.theme}\nUse all 9 IPTC subjects: CUL ART CIN CHM HLT PRD FIN LIF HUM.\n"
        f"Host: Instagram and TikTok. 3 posts/day: Mon(1-3), Wed(4-6), Fri(7-9).\n"
        f"Identify one hero post. All 9 must be distinct.", ctx)
    brief = cd_result["result"]
    state.log_event("CD", "complete", state.week_id, f"theme={brief.get('weekly_theme','')}", cd_result["provider_used"])

    # Step 2b: Current Events
    ce_result = run_role("current_events",
        f"Find timely claims. Theme: {brief.get('weekly_theme','')}\nMax 3 per subject. source_url REQUIRED.", ctx)
    state.log_event("CE", "complete", state.week_id, f"claims={len(ce_result['result'].get('claims',[]))}", ce_result["provider_used"])

    # Step 2c: Fact Check
    fc_result = run_role("fact_checker",
        f"Verify claims:\n{json.dumps(ce_result['result'], indent=2)[:4000]}\n"
        f"Cannot verify? Say 'cannot_verify'. Do not guess.", ctx)
    state.log_event("FC", "complete", state.week_id, "done", fc_result["provider_used"])

    # Step 3b: Validator
    val_result = run_role("brief_validator",
        f"Validate:\n{json.dumps(brief, indent=2)[:8000]}", ctx)
    val = val_result["result"]
    state.log_event("BV", "complete", state.week_id, f"verdict={val.get('verdict','?')}", val_result["provider_used"])

    # Step 3c: Creative Grader
    cg_result = run_role("creative_grader",
        f"Grade (9 sections, 0-5 each, /100):\n{json.dumps(brief, indent=2)[:8000]}", ctx)
    cg = cg_result["result"]
    state.log_event("CG", "complete", state.week_id, f"score={cg.get('total_score','?')}/100", cg_result["provider_used"])

    # Step 3d: Production Grader
    pg_result = run_role("production_grader",
        f"Grade feasibility (7 sections, /75):\n{json.dumps(brief, indent=2)[:8000]}", ctx)
    pg = pg_result["result"]
    state.log_event("PG", "complete", state.week_id, f"score={pg.get('total_score','?')}/75", pg_result["provider_used"])

    # Redo loop: if graders reject, re-run CD with feedback
    if val.get("verdict") == "blocked" or cg.get("total_score", 0) < 70:
        redo_key = f"brief_{state.week_id}"
        count = state.increment_redo(redo_key)
        if count <= MAX_REDO:
            record_decision(DecisionRecord(
                id=f"{state.week_id}_brief_reject_{count}",
                week_id=state.week_id, post_position=0, phase="creative_brief",
                entity_type="brief", entity_id=state.week_id, decision="reject",
                reason=f"Val={val.get('verdict','')}, CG={cg.get('total_score',0)}/100, PG={pg.get('total_score',0)}/75",
                decided_by="ai_team", taste_tags=["needs_revision"],
                grader_scores={"validator": val.get("structural_score",0), "creative": cg.get("total_score",0), "production": pg.get("total_score",0)},
                revision_count=count,
            ))
            # Re-run CD with grader feedback
            feedback = ctx + f"\n\nGRADER FEEDBACK (revision {count}):\n"
            feedback += f"Validator: {val.get('critical_errors',[])}\n"
            feedback += f"Creative: {cg.get('required_revisions',[])}\n"
            feedback += f"Production: {pg.get('required_corrections',[])}\nRevise addressing ALL feedback."
            cd_result2 = run_role("creative_director",
                f"REVISE brief for Week {week.week_number}. Theme: {week.theme}\n"
                f"Previous:\n{json.dumps(brief, indent=2)[:4000]}", feedback)
            brief = cd_result2["result"]
            state.log_event("CD", "revised", state.week_id, f"rev_{count}", cd_result2["provider_used"])

    # Record final decision
    record_decision(DecisionRecord(
        id=f"{state.week_id}_brief_final", week_id=state.week_id, post_position=0,
        phase="creative_brief", entity_type="brief", entity_id=state.week_id,
        decision="approve" if val.get("verdict") != "blocked" else "reject",
        reason=f"Val={val.get('verdict','')}, CG={cg.get('total_score',0)}/100, PG={pg.get('total_score',0)}/75",
        decided_by="ai_team",
        grader_scores={"validator": val.get("structural_score",0), "creative": cg.get("total_score",0), "production": pg.get("total_score",0)},
    ))

    distill_knowledge()  # Refresh training knowledge

    return {
        "brief": brief, "current_events": ce_result["result"], "fact_check": fc_result["result"],
        "validator": val, "creative_grader": cg, "production_grader": pg,
        "events": [{"step": e.step, "action": e.action, "result": e.result,
                     "provider": e.provider_used, "time": e.timestamp} for e in state.events],
        "redo_count": state.redo_counts.get(f"brief_{state.week_id}", 0),
    }


def conductor_run_copywriter(post_position, media_asset, brief_output):
    """Conductor runs Copywriter → Copy Grader with retry loop."""
    state = ConductorState(week_id=brief_output.get("weekly_theme", ""))
    ctx = build_context(state.week_id)

    posts = brief_output.get("post_briefs", [])
    post_data = posts[post_position - 1] if post_position <= len(posts) else {}

    # Copywriter
    cw_result = run_role("copywriter",
        f"Write captions and hashtags for post {post_position}.\n"
        f"TikTok: caption + CTA + 5 hashtags | Instagram: caption + CTA + 5 hashtags\n"
        f"Also: alt text, attribution, disclosure.\n\n"
        f"Brief:\n{json.dumps(post_data, indent=2)[:2000]}\n\n"
        f"Media:\n{json.dumps(media_asset, indent=2)[:2000]}", ctx)
    copy = cw_result["result"]

    # Copy Grader
    cgr_result = run_role("copy_grader",
        f"Grade (8 categories, 0-5 each, /100):\n{json.dumps(copy, indent=2)[:4000]}", ctx)
    grade = cgr_result["result"]

    # Redo loop
    if grade.get("total_score", 0) < 70:
        redo_key = f"copy_{post_position}"
        count = state.increment_redo(redo_key)
        if count <= MAX_REDO:
            record_decision(DecisionRecord(
                id=f"copy_p{post_position}_reject_{count}",
                week_id=state.week_id, post_position=post_position, phase="copywriter",
                entity_type="copy", entity_id=f"post_{post_position}", decision="reject",
                reason=f"Score: {grade.get('total_score',0)}/100. {grade.get('required_corrections',[])}",
                decided_by="ai_team", taste_tags=["copy_needs_revision"], revision_count=count,
            ))
            feedback = ctx + f"\n\nCOPY GRADER FEEDBACK:\n{grade.get('required_corrections',[])}\nRevise."
            cw_result2 = run_role("copywriter",
                f"REVISE copy for post {post_position}.\nPrevious:\n{json.dumps(copy, indent=2)[:2000]}", feedback)
            copy = cw_result2["result"]

    # Record
    record_decision(DecisionRecord(
        id=f"copy_p{post_position}_final", week_id=state.week_id, post_position=post_position,
        phase="copywriter", entity_type="copy", entity_id=f"post_{post_position}",
        decision="approve" if grade.get("total_score", 0) >= 70 else "reject",
        reason=f"Score: {grade.get('total_score',0)}/100",
        decided_by="ai_team", grader_scores={"copy_grade": grade.get("total_score",0)},
    ))
    distill_knowledge()

    return {
        "copy": copy, "grader": grade,
        "events": [{"step": e.step, "action": e.action, "result": e.result,
                     "provider": e.provider_used} for e in state.events],
        "redo_count": state.redo_counts.get(f"copy_{post_position}", 0),
    }