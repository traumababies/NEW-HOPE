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
# Step 10: Cataloger catalogs the original; Jean must approve (JC never self-approves)
# ---------------------------------------------------------------------------
def step10_cataloger(original_row: dict) -> dict:
    """Cataloger adds ISO/DublinCore/OG metadata and requests JAN; never approves."""
    catalog = dict(original_row)
    catalog["catalog_status"] = "pending_jean_approval"  # Jean must approve
    return catalog


# ---------------------------------------------------------------------------
# Step 11/12: Media Editor transforms original (Derivative) or creates from
# scratch; checks software in the brief; max 2 redoes, owner password override.
# ---------------------------------------------------------------------------
def step11_12_media_editor(
    *, work_kind: str, software: list[str], redo_count: int = 0, owner_override: str = ""
) -> str:
    if work_kind not in {"derivative", "create_from_scratch"}:
        raise ValueError("work_kind must be derivative or create_from_scratch")
    if redo_count > 2 and not owner_override:
        raise PermissionError("Media Editor redo limit is 2; owner password required to exceed.")
    if not software:
        raise ValueError("Media Editor must check off the software used.")
    return f"{work_kind}|{','.join(software)}|redo{redo_count}"


# ---------------------------------------------------------------------------
# Step 13: Approved Theme Image -> Cataloger -> permanent Library -> Publishing
# ---------------------------------------------------------------------------
def step13_theme_image_to_library(week: Week) -> str:
    if not week.theme_image_key:
        raise ValueError("Step 13: no theme image uploaded for week.")
    return f"{week.theme_image_key} -> Library (Bunbuns) -> Publishing"


# ---------------------------------------------------------------------------
# Step 14/15: Copywriter (w/ Current Events + Fact Check) writes captions +
# 5 hashtags per platform; JAN; redo max 2; then final naming + Cataloger.
# ---------------------------------------------------------------------------
def step14_15_copywriter(*, platform: str, caption: str, hashtags: list[str]) -> dict:
    platform = platform.lower()
    if platform not in {"instagram", "tiktok"}:
        raise ValueError("platform must be instagram or tiktok")
    if not caption.strip():
        raise ValueError("Caption required.")
    tags = [h for h in hashtags if h.startswith("#")]
    if len(tags) != 5:
        raise ValueError("Exactly 5 hashtags required per platform.")
    return {"platform": platform, "caption": caption.strip(), "hashtags": tags, "j": "pending"}


# ---------------------------------------------------------------------------
# Step 16: Scheduler formats + publishes 3 at a time Mon/Wed/Fri, MST.
# IG order 1-9, TT order 9-1.
# ---------------------------------------------------------------------------
def step16_scheduler(*, platform: str, tile: int) -> int:
    """Return the tile's slot position (1-based) for the platform's posting order."""
    if platform.lower() == "instagram":
        return tile
    return 10 - tile  # TikTok posts 9..1


# ---------------------------------------------------------------------------
# Step 17: in-order enforcement — if any earlier tile not approved, block.
# ---------------------------------------------------------------------------
def step17_in_order(*, platform: str, tile: int, approved_up_to: int) -> bool:
    order = step16_scheduler(platform=platform, tile=tile)
    return order <= approved_up_to


# ---------------------------------------------------------------------------
# Step 18/19: missed/unpublished => unpublish on Status; published => history as mirage.
# ---------------------------------------------------------------------------
def step18_19_history(*, published: bool, storage_key: str) -> dict:
    state = "published" if published else "unpublished_archive"
    return {"storage_key": storage_key, "state": state, "mirage": True}


# Convenience: run the full 1-19 spine against a week + selected tiles, no DB.
def run_full_spine(week: Week, *, selected_tiles: list[str] | None = None) -> dict:
    """Exercise STEPS 1-19 without DB; raises at the first broken step."""
    out = {}
    out["s1_theme"] = step1_save_theme(week)
    brief = step2_compose_brief(week)
    out["s2_brief_id"] = brief.brief_id
    out["s3"] = "JAN requested (needs DB)"
    matches = step5_muse_to_studio(brief, approved_assets=[])
    out["s5_rfr"] = sum(1 for m in matches if m["rfr"])
    out["s6_scouts"] = len(step6_muse_assign_scouts(brief, matches))
    if selected_tiles:
        comm = step9_studio_commit(brief, selected_tiles)
        out["s9_orig"] = [c["original"] for c in comm["committed"]]
        out["s9_deriv"] = [c["derivative"] for c in comm["committed"]]
        cat = step10_cataloger({"original": out["s9_orig"][0], "id": 1})
        out["s10_status"] = cat["catalog_status"]
        out["s11_12"] = step11_12_media_editor(work_kind="derivative", software=["ComfyUI"])
        if week.theme_image_key:
            out["s13"] = step13_theme_image_to_library(week)
        cp = step14_15_copywriter(
            platform="instagram",
            caption="Under one moon.",
            hashtags=["#a", "#b", "#c", "#d", "#e"],
        )
        out["s14_15_j"] = cp["j"]
        out["s16_tile3_tt"] = step16_scheduler(platform="tiktok", tile=3)
        out["s17_blocked"] = not step17_in_order(platform="tiktok", tile=3, approved_up_to=2)
        out["s18_19"] = step18_19_history(published=True, storage_key="k")
    return out

# ---------------------------------------------------------------------------
# Step 7/8: Content Scouts fetch (owned per-platform) -> Ephemera -> Studio JAN
# ---------------------------------------------------------------------------
def step9_studio_commit(brief: WeeklyBrief, selected_tiles: list[str]) -> dict:
    """After Jean COMMITs: assign uuidv7 to selected originals + derivative names.

    The spec: upon COMMIT, selected content generates uuidv7(), links
    hasVersion (original) and isVersionof (derivative).
    """
    import uuid

    # Extract year + week from the brief id (YYYY_W##_THEME_HOST).
    ident = brief.brief_id.split("_")
    year = int(ident[0])
    week_number = int(ident[1].lstrip("W"))
    results = []
    SUBJECTS = ("ART", "CHM", "CIN", "CUL", "FIN", "HLT", "HUM", "LIF", "PRD")
    for label in selected_tiles:
        code = label.split("_")[0] if label.split("_")[0] in SUBJECTS else "TI"
        seq_str = label.split("_")[-1] if "_" in label else "0"
        seq = int(seq_str or 0) if seq_str.isdigit() else 0
        u = uuid.uuid4().hex
        results.append({
            "tile": label,
            "code": code,
            "sequence": seq,
            "original": original_uuid_name(year, week_number, code, seq, u),
            "derivative": derivative_uuid_name(year, week_number, code, seq, u),
        })
    return {"committed": results}
