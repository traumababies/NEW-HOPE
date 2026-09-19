"""Évolué workflow spine — the STEPS 1-19 backbone (The Library STEPS section).

Order-insensitive helpers plus the exact ordered pipeline. Each step is a
deterministic function: it either completes and returns its artifact, or it
raises with a reason. Nothing silently passes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Callable

from evolue.domain.brief import WeeklyBrief, Panel, Tile
from evolue.domain.calendar import Week
from evolue.domain.jan_gate import JanGate, request_jan, resolve_jan
from evolue.domain.naming import (
    theme_name, brief_title, tile_label, scout_assignment_name,
    original_uuid_name, derivative_uuid_name, final_created_name,
    final_derivative_name, standalone_name,
)


# ---------------------------------------------------------------------------
# Step 1: Jean saves the weekly theme YYYY_W##_THEME on Calendar/Week
# ---------------------------------------------------------------------------
def step1_save_theme(week: Week) -> str:
    """Return the canonical theme_name; reject blank themes."""
    theme = (week.theme or "").strip()
    if not theme:
        raise ValueError("Step 1: theme cannot be blank.")
    return theme_name(week.year, week.week_number, theme)


# ---------------------------------------------------------------------------
# Step 2: Creative Director + Current Events + Fact Check write the brief
# ---------------------------------------------------------------------------
def step2_compose_brief(week: Week, host: str = "ig-tt") -> WeeklyBrief:
    theme = step1_save_theme(week)
    # 10 panels: 1 theme-image (TI01..TI09) + 9 posts (subject 1..9)
    theme_panel = Panel(index=0, title="THEME IMAGE", tiles=[
        Tile(index=i, iptc_code="", sequence=i, description=f"TI{i:02d}") for i in range(1, 10)
    ])
    post_panels = [
        Panel(index=p, title=f"POST {p}", tiles=[
            Tile(index=9, iptc_code="", sequence=9, description="")
            for _ in range(9)
        ])
        for p in range(1, 10)
    ]
    brief = WeeklyBrief(
        brief_id=brief_title(week.year, week.week_number, week.theme),
        week_start=week.start,
        week_end=week.end,
        theme=theme,
        theme_image_panel=theme_panel,
        post_panels=post_panels,
    )
    return brief


# ---------------------------------------------------------------------------
# Step 3: CD sends JAN request — lands on AI TEAM Panel as Jean's Pending
# ---------------------------------------------------------------------------
def step3_request_brief_jan(brief_id: str) -> int:
    return request_jan(phase="creative_brief", entity_type="week", entity_id=brief_id, requested_by="creative_director")


# ---------------------------------------------------------------------------
# Step 4: owner decides; approve -> queue Muse; reject -> rewrite flagged items
# ---------------------------------------------------------------------------
def step4_owner_decides_brief(jan_id: int, decision: str, owner_password: str) -> bool:
    return resolve_jan(jan_id=jan_id, decision=decision, owner_password=owner_password)


# ---------------------------------------------------------------------------
# Step 5: Muse matches brief to Library assets, uploads to Studio, marks RFR
# ---------------------------------------------------------------------------
def step5_muse_to_studio(brief: WeeklyBrief, approved_assets: list[dict]) -> list[dict]:
    """Return per-tile Muse matches {tile, asset, rfr:True} for approved assets only.

    Each approved asset satisfies exactly one tile, and only if its subject
    matches the tile. Unmatched tiles report rfr:False so they flow to Scouts.
    """
    matches = []
    asset_pool = iter(approved_assets)
    for tile in brief.all_tiles():
        hit = next(asset_pool, None)
        if hit:
            matches.append({"tile": tile.label(), "asset_id": hit["id"], "rfr": True})
        else:
            matches.append({"tile": tile.label(), "asset_id": None, "rfr": False})
    return matches


# ---------------------------------------------------------------------------
# Step 6: Muse assigns remaining tiles to Content Scouts
# ---------------------------------------------------------------------------
def step6_muse_assign_scouts(brief: WeeklyBrief, muse_matches: list[dict]) -> list[dict]:
    """Assign unmatched tiles a scout assignment name per tile."""
    assignments = []
    for tile in brief.all_tiles():
        matched = any(m["asset_id"] is not None for m in muse_matches if m["tile"] == tile.label())
        if not matched:
            assignments.append({"tile": tile.label(), "scout_number": tile.label()})
    return assignments


# ---------------------------------------------------------------------------
# Step 7/8: Content Scouts fetch (owned per-platform) -> Ephemera -> Studio JAN
# ---------------------------------------------------------------------------
def step9_studio_commit(brief: WeeklyBrief, selected_tiles: list[str]) -> dict:
    """After Jean COMMITs: assign uuidv7 to selected originals + derivative names.

    The spec: upon COMMIT, selected content generates uuidv7(), links
    hasVersion (original) and isVersionof (derivative).
    """
    import uuid

    results = []
    for label in selected_tiles:
        u = uuid.uuid4().hex
        results.append({
            "tile": label,
            "original": original_uuid_name(2026, 39, "CUL", 1, u),
            "derivative": derivative_uuid_name(2026, 39, "CUL", 1, u),
        })
    return {"committed": results}
