"""JAN (Jean Approval Needed) — the owner-gate.

Per The Library.txt (E.1): content needing Jean's approval is alerted to Jean,
visible on the AI TEAM Panel as PENDING, blocks downstream phases with an
explanation, and can only be unblocked by Jean's approval or her unique
override password. The Cataloger can never approve his own work.
"""
from __future__ import annotations

import secrets

from ..infrastructure.sql.db import execute, fetch_all


class JanGate:
    """Raised when a phase is blocked awaiting owner approval."""

    def __init__(self, phase: str, entity_type: str = "", entity_id: str = ""):
        self.phase = phase
        self.entity_type = entity_type
        self.entity_id = entity_id

    def __str__(self) -> str:
        return f"Phase '{self.phase}' is pending Jean's approval (JAN)."


def request_jan(*, phase: str, entity_type: str, entity_id: str, requested_by: str) -> int:
    execute(
        "INSERT INTO jan_requests (phase, entity_type, entity_id, requested_by, status) "
        "VALUES (?,?,?,?,?)",
        (phase, entity_type, entity_id, requested_by, "pending"),
    )
    rows = fetch_all(
        "SELECT id FROM jan_requests WHERE phase=? AND entity_type=? AND entity_id=? "
        "AND status='pending' ORDER BY id DESC",
        (phase, entity_type, entity_id),
    )
    return rows[0]["id"]


def resolve_jan(
    *,
    jan_id: int,
    decision: str,
    owner_password: str,
    admin_email: str,
    override_password: str = "",
    note: str = "",
) -> bool:
    """Owner resolves a JAN. Requires owner password (or unique override)."""
    if decision not in {"approve", "reject", "replace", "override"}:
        raise ValueError("decision must be approve/reject/replace/override")
    if not owner_password:
        raise ValueError("Owner password required.")
    row = fetch_all("SELECT * FROM jan_requests WHERE id=?", (jan_id,))
    if not row:
        raise ValueError("JAN request not found.")
    current = row[0]
    if current["status"] != "pending":
        raise ValueError("JAN request already decided.")
    if decision == "override":
        if not override_password or override_password != secrets.compare_digest(
            override_password, overrides().get(current["phase"], "")
        ):
            raise ValueError("Override password rejected.")
    execute(
        "UPDATE jan_requests SET status=?, decision_note=?, decided_at=SYSDATETIME() WHERE id=?",
        (decision, note, jan_id),
    )
    # Reject/Replace on a proposal also marks the pending proposal as needing redo.
    if decision in {"reject", "replace"} and current.get("entity_type"):
        _propagate_redo(current)
    return True


def pending_for(phase: str) -> list[dict]:
    return fetch_all(
        "SELECT * FROM jan_requests WHERE phase=? AND status='pending' ORDER BY id", (phase,)
    )


def overrides() -> dict[str, str]:
    """Per-phase override passwords. Seeded from env; owners change via settings."""
    from evolue.config import settings

    return {
        "creative_brief": settings.jan_override_creative_brief or "",
        "muse": settings.jan_override_muse or "",
        "scout": settings.jan_override_scout or "",
        "catalog": settings.jan_override_catalog or "",
        "media_editor": settings.jan_override_media_editor or "",
        "copywriter": settings.jan_override_copywriter or "",
    }


def _propagate_redo(current: dict) -> None:
    """A reject/replace on an entity marks the target for redo (2-max, owner override)."""
    entity_type = current.get("entity_type")
    if entity_type == "proposal":
        execute(
            "UPDATE proposals SET status='needs_redo' WHERE id=CAST(? AS INT)",
            (current.get("entity_id"),),
        )

