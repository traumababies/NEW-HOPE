"""Decision Ledger — the memory of every approve/reject/replace with WHY.

This is the foundation of the Learning Center. Every decision creates a record
that feeds back into the AI team's prompts so they improve over time.

The training loop:
  Post lifecycle → Decision record → Taste tags → Training knowledge
    → Feed back into CD/Muse/Copywriter prompts
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
LEDGER_FILE = DATA_DIR / "decision_ledger.json"
TASTE_FILE = DATA_DIR / "taste.md"
KNOWLEDGE_FILE = DATA_DIR / "training_knowledge.json"


@dataclass
class DecisionRecord:
    """One approve/reject/replace decision with full context."""
    id: str
    week_id: str                  # YYYY_W##
    post_position: int            # 1-9
    phase: str                    # creative_brief | muse | studio | catalog | media_editor | copywriter | publishing
    entity_type: str              # brief | asset | copy | media
    entity_id: str                # core identifier or brief_id
    decision: str                 # approve | reject | replace | override
    reason: str                   # WHY — specific, not vague
    decided_by: str               # jean | ai_team
    taste_tags: list[str] = field(default_factory=list)  # extracted patterns
    grader_scores: dict = field(default_factory=dict)
    original_context: str = ""    # what was submitted
    replacement_context: str = "" # what replaced it (if replace)
    revision_count: int = 0
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()


def _load_ledger() -> list[dict]:
    if LEDGER_FILE.exists():
        try:
            return json.loads(LEDGER_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return []


def _save_ledger(records: list[dict]) -> None:
    LEDGER_FILE.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")


def record_decision(rec: DecisionRecord) -> None:
    """Append a decision to the ledger."""
    records = _load_ledger()
    records.append({
        "id": rec.id,
        "week_id": rec.week_id,
        "post_position": rec.post_position,
        "phase": rec.phase,
        "entity_type": rec.entity_type,
        "entity_id": rec.entity_id,
        "decision": rec.decision,
        "reason": rec.reason,
        "decided_by": rec.decided_by,
        "taste_tags": rec.taste_tags,
        "grader_scores": rec.grader_scores,
        "original_context": rec.original_context[:500],
        "replacement_context": rec.replacement_context[:500],
        "revision_count": rec.revision_count,
        "timestamp": rec.timestamp,
    })
    _save_ledger(records)

    # Also write taste tags to taste.md
    if rec.taste_tags and rec.decision in ("reject", "replace"):
        _append_taste_tags(rec.taste_tags, rec.reason, rec.week_id)


def _append_taste_tags(tags: list[str], reason: str, week_id: str) -> None:
    """Append tagged rejection reasons to taste.md."""
    line = f"- [{week_id}] {', '.join(tags)}: {reason}\n"
    with open(TASTE_FILE, "a", encoding="utf-8") as f:
        f.write(line)


def get_taste_tags() -> list[str]:
    """Read all taste tags from taste.md."""
    if not TASTE_FILE.exists():
        return []
    tags = set()
    for line in TASTE_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- ["):
            # Extract tags between ] and :
            try:
                tag_part = line.split("]")[1].split(":")[0].strip()
                for tag in tag_part.split(","):
                    tag = tag.strip()
                    if tag:
                        tags.add(tag)
            except (IndexError, ValueError):
                pass
    return sorted(tags)


def get_recent_decisions(n: int = 20) -> list[dict]:
    """Get the most recent N decisions."""
    return _load_ledger()[-n:]


def get_decisions_for_week(week_id: str) -> list[dict]:
    """Get all decisions for a specific week."""
    return [r for r in _load_ledger() if r.get("week_id") == week_id]


def get_rejection_reasons(entity_type: str = "", limit: int = 10) -> list[dict]:
    """Get recent rejection reasons for training."""
    records = [r for r in _load_ledger() if r.get("decision") in ("reject", "replace")]
    if entity_type:
        records = [r for r in records if r.get("entity_type") == entity_type]
    return records[-limit:]