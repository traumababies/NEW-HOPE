"""Training Knowledge — distills decision records into actionable intelligence.

The feedback loop:
  1. Jean approves/rejects with reasons
  2. Decision records accumulate in the ledger
  3. Training knowledge extracts patterns (what works, what doesn't)
  4. CD/Muse/Copywriter read these patterns in their prompts
  5. AIs produce better output because they learn from past decisions
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .decision_ledger import (
    KNOWLEDGE_FILE, get_recent_decisions, get_rejection_reasons,
    get_taste_tags,
)


def distill_knowledge() -> dict:
    """Extract training knowledge from the decision ledger.

    Returns a structured dict that can be injected into AI prompts:
    - rejection_patterns: what gets rejected and why
    - approval_patterns: what gets approved and why
    - taste_tags: owner's taste vocabulary
    - recent_outcomes: last 4 weeks of decisions
    - quality_signals: what the graders consistently flag
    """
    recent = get_recent_decisions(50)
    rejections = get_rejection_reasons(limit=20)
    taste = get_taste_tags()

    # Extract rejection patterns
    rejection_patterns = []
    for r in rejections:
        pattern = {
            "phase": r.get("phase", ""),
            "reason": r.get("reason", ""),
            "tags": r.get("taste_tags", []),
            "week": r.get("week_id", ""),
        }
        rejection_patterns.append(pattern)

    # Extract approval patterns
    approvals = [r for r in recent if r.get("decision") == "approve"]
    approval_patterns = []
    for a in approvals[-10:]:
        approval_patterns.append({
            "phase": a.get("phase", ""),
            "entity_type": a.get("entity_type", ""),
            "week": a.get("week_id", ""),
        })

    # Extract quality signals from grader scores
    quality_signals = []
    for r in recent:
        scores = r.get("grader_scores", {})
        if scores:
            for section, score in scores.items():
                if isinstance(score, (int, float)) and score < 3:
                    quality_signals.append(f"Weak {section} (scored {score}/5)")

    # Build the knowledge object
    knowledge = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "taste_tags": taste,
        "rejection_patterns": rejection_patterns[-10:],
        "approval_patterns": approval_patterns,
        "quality_signals": list(set(quality_signals))[:10],
        "recent_outcomes": _summarize_recent(recent),
    }

    # Save to file
    KNOWLEDGE_FILE.write_text(
        json.dumps(knowledge, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return knowledge


def _summarize_recent(decisions: list[dict]) -> list[dict]:
    """Summarize recent decisions into a compact format for prompts."""
    summaries = []
    for d in decisions[-12:]:
        summaries.append({
            "week": d.get("week_id", ""),
            "post": d.get("post_position", 0),
            "phase": d.get("phase", ""),
            "decision": d.get("decision", ""),
            "reason": d.get("reason", "")[:100],
        })
    return summaries


def load_knowledge_for_prompt() -> str:
    """Load training knowledge as a text block for injection into AI prompts.

    This is what the CD, Muse, and Copywriter read before they start working.
    """
    if KNOWLEDGE_FILE.exists():
        try:
            knowledge = json.loads(KNOWLEDGE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            knowledge = distill_knowledge()
    else:
        knowledge = distill_knowledge()

    lines = ["TRAINING KNOWLEDGE (from past decisions):"]

    if knowledge.get("taste_tags"):
        lines.append(f"\nTaste tags (what Jean cares about): {', '.join(knowledge['taste_tags'])}")

    if knowledge.get("rejection_patterns"):
        lines.append("\nRecent rejections (avoid these patterns):")
        for p in knowledge["rejection_patterns"][:5]:
            lines.append(f"  - [{p['phase']}] {p['reason']}")
            if p.get("tags"):
                lines.append(f"    Tags: {', '.join(p['tags'])}")

    if knowledge.get("quality_signals"):
        lines.append(f"\nQuality signals: {'; '.join(knowledge['quality_signals'][:5])}")

    if knowledge.get("recent_outcomes"):
        lines.append("\nRecent outcomes:")
        for o in knowledge["recent_outcomes"][:4]:
            lines.append(f"  - {o['week']} post{o['post']}: {o['decision']} ({o['phase']}) — {o['reason']}")

    return "\n".join(lines)