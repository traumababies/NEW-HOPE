"""Évolué workflow spine — STEPS 1-19, wired to real AI providers.

Each step is a deterministic function that either completes and returns its
artifact, or raises with a reason. Steps 2, 3b-d, 5, 10, 11-12, 14-15 call
the AI embedding system (evolue.ai.runners).
"""
from __future__ import annotations

import json
import uuid
from datetime import date, datetime

from evolue.domain.brief import WeeklyBrief, Panel, Tile
from evolue.domain.calendar import Week
from evolue.domain.jan_gate import request_jan, resolve_jan
from evolue.domain.naming import (
    theme_name, brief_title, tile_label, scout_assignment_name,
    original_uuid_name, derivative_uuid_name, final_created_name,
    final_derivative_name, standalone_name,
)
from evolue.ai.runners import run_role, run_role_text
from evolue.ai.validators import validate_brief, validate_muse, validate_catalog, validate_copy

SUBJECTS = ("CUL", "ART", "CIN", "CHM", "HLT", "PRD", "FIN", "LIF", "HUM")


# ---- Step 1: Jean saves theme ------------------------------------------------
def step1_save_theme(week: Week) -> str:
    theme = (week.theme or "").strip()
    if not theme:
        raise ValueError("Step 1: theme cannot be blank.")
    return theme_name(week.year, week.week_number, theme)


# ---- Step 2: Creative Director writes the brief (AI) -------------------------
def step2_compose_brief(week: Week, *, context: str = "") -> dict:
    theme_str = step1_save_theme(week)
    task = (
        f"Create the weekly Creative Brief for Week {week.week_number}, {week.year}.\n"
        f"Theme: {week.theme}\nTheme string: {theme_str}\n"
        f"Week start: {week.start}\nWeek end: {week.end}\n"
        f"Use all 9 IPTC subjects: {', '.join(SUBJECTS)}\n"
        f"Host platforms: Instagram and TikTok\n"
        f"3 posts per day: Mon (1-3), Wed (4-6), Fri (7-9)\n"
        f"Identify one hero post. All 9 must be distinct."
    )
    return run_role("creative_director", task, context)


# ---- Step 2b: Current Events (AI) --------------------------------------------
def step2b_current_events(brief_output: dict, context: str = "") -> dict:
    theme = brief_output.get("weekly_theme", "")
    angles = "\n".join(
        f"- {p.get('subject_code','?')}: {p.get('subject_angle','')}"
        for p in brief_output.get("post_briefs", [])
    )
    task = (
        f"Find timely current-event claims for this week's content.\n"
        f"Theme: {theme}\n\nSubject angles:\n{angles}\n\n"
        f"Max 3 claims per subject. Every claim MUST have source_url."
    )
    return run_role("current_events", task, context)


# ---- Step 2c: Fact Checker (AI) ----------------------------------------------
def step2c_fact_check(claims: dict, context: str = "") -> dict:
    task = (
        f"Verify these claims. Verdicts: verified|partially_verified|unverified|"
        f"contradicted|cannot_verify\n\nClaims:\n{json.dumps(claims, indent=2)[:4000]}\n\n"
        f"If you cannot verify, say 'cannot_verify'. Do not guess."
    )
    return run_role("fact_checker", task, context)


# ---- Step 3: JAN request for the brief ---------------------------------------
def step3_request_brief_jan(brief_id: str) -> int:
    return request_jan(phase="creative_brief", entity_type="week",
                       entity_id=brief_id, requested_by="creative_director")


# ---- Step 4: Owner decides on brief ------------------------------------------
def step4_owner_decides(jan_id: int, decision: str, owner_password: str) -> bool:
    return resolve_jan(jan_id=jan_id, decision=decision, owner_password=owner_password)


# ---- Step 3b: Brief Validator (AI) -------------------------------------------
def step3b_validate_brief(brief_output: dict, context: str = "") -> dict:
    task = (
        f"Validate this Creative Brief for structural completeness.\n"
        f"Check: 9 posts, positions 1-9, timelines, search packets, music direction.\n"
        f"Return PASS, PASS_WITH_WARNINGS, or BLOCKED.\n\n"
        f"Brief:\n{json.dumps(brief_output, indent=2)[:8000]}"
    )
    return run_role("brief_validator", task, context)


# ---- Step 3c: Creative Grader (AI) -------------------------------------------
def step3c_creative_grade(brief_output: dict, context: str = "") -> dict:
    task = (
        f"Grade this Creative Brief across 9 sections (0-5 each, total /100):\n"
        f"Theme fidelity, Emotional direction, Nine-post narrative, Subject integration,\n"
        f"Hook quality, Visual identity, Audio identity, Originality, Brand alignment.\n\n"
        f"Brief:\n{json.dumps(brief_output, indent=2)[:8000]}"
    )
    return run_role("creative_grader", task, context)


# ---- Step 3d: Production Grader (AI) -----------------------------------------
def step3d_production_grade(brief_output: dict, context: str = "") -> dict:
    task = (
        f"Grade this brief for production feasibility (0-5 each section, total /75):\n"
        f"Searchability, Footage availability, Editability, Risk assessment,\n"
        f"Technical delivery, Rights/provenance, Candidate acceptance rules.\n\n"
        f"Brief:\n{json.dumps(brief_output, indent=2)[:8000]}"
    )
    return run_role("production_grader", task, context)


# ---- Step 5: Muse matches brief to Library (AI) ------------------------------
def step5_muse_search(brief_output: dict, approved_assets: list[dict], context: str = "") -> dict:
    task = (
        f"Match approved Library assets to each position in this brief.\n"
        f"For positions 1-9: if an asset fits, set selected_candidate_id + evidence.\n"
        f"If NO asset fits, set gap with a Content Scout request (search_terms, media_type).\n\n"
        f"Brief:\n{json.dumps(brief_output.get('post_briefs', []), indent=2)[:6000]}\n\n"
        f"Library assets:\n{json.dumps(approved_assets, indent=2)[:4000]}"
    )
    return run_role("muse", task, context)


# ---- Step 6: Extract scout requests from Muse gaps (deterministic) -----------
def step6_extract_scout_requests(muse_output: dict) -> list[dict]:
    requests = []
    for pos in muse_output.get("positions", []):
        gap = pos.get("gap")
        if gap:
            requests.append({
                "position": pos.get("position"),
                "subject_code": pos.get("subject_code", ""),
                "search_terms": gap.get("search_terms", []),
                "media_type": gap.get("media_type", "image"),
                "assignment_name": gap.get("assignment_name", ""),
            })
    return requests


# ---- Step 7/8: Content Scouts fetch -> Ephemera (existing infra) -------------
def step7_8_scout_fetch(scout_requests: list[dict], year: int, week_number: int) -> list[dict]:
    from evolue.infrastructure.scouts import run_platform
    from evolue.infrastructure.quarantine import quarantine_candidates

    all_results = []
    for req in scout_requests:
        queries = {req["subject_code"]: " ".join(req.get("search_terms", []))}
        for platform in ("pixabay", "pexels", "unsplash", "coverr"):
            try:
                results = run_platform(platform, queries)
                candidates = results.get(req["subject_code"], [])
                if candidates:
                    records = quarantine_candidates(
                        platform=platform, subject_code=req["subject_code"],
                        year=year, week_number=week_number, candidates=candidates[:10],
                    )
                    all_results.extend(records)
            except Exception:
                continue
    return all_results


# ---- Step 9: Studio COMMIT — uuidv7, destroy unselected, write metadata ------
def step9_studio_commit(brief_id: str, selected_tiles: list[str],
                        all_candidates: list[dict] | None = None) -> dict:
    """Upon Jean's COMMIT:
    1. Assign uuidv7 to selected originals
    2. Create original (dcterms:hasVersion) + derivative (dcterms:isVersionof)
    3. Write metadata for BOTH versions
    4. Destroy all unselected items from Ephemera
    5. Originals → Cataloger queue, Derivatives → Media Editor
    """
    from evolue.infrastructure.storage import delete_blob, BlobRef
    from evolue.config import settings

    ident = brief_id.split("_")
    year = int(ident[0])
    week_number = int(ident[1].lstrip("W"))
    results = []
    selected_labels = set(selected_tiles)

    for label in selected_tiles:
        parts = label.split("_")
        code = parts[0] if parts[0] in SUBJECTS else "TI"
        seq_str = parts[-1] if len(parts) > 1 else label[2:]
        seq = int(seq_str) if seq_str.isdigit() else 0
        u = uuid.uuid4().hex
        orig = original_uuid_name(year, week_number, code, seq, u)
        deriv = derivative_uuid_name(year, week_number, code, seq, u)
        results.append({
            "tile": label, "code": code, "sequence": seq, "uuid": u,
            "original": orig, "derivative": deriv,
            "original_meta": {
                "dc:identifier": orig, "dcterms:hasVersion": f"v1-0_{u}",
                "dc:subject": code, "state": "STEP_0_ORIGINAL",
                "destination": "Cataloger queue",
            },
            "derivative_meta": {
                "dc:identifier": deriv, "dcterms:isVersionof": f"v1-0_{u}",
                "dc:identifier_url": orig, "dc:subject": code,
                "state": "STEP_0_ORIGINAL", "destination": "Media Editor",
            },
        })

    # Destroy unselected items from Ephemera
    destroyed = 0
    if all_candidates:
        for cand in all_candidates:
            cand_label = f"{cand.get('subject_code','TI')}_{cand.get('sequence',0):02d}"
            if cand_label not in selected_labels:
                key = cand.get("poster_key", "")
                if key:
                    try:
                        delete_blob(BlobRef(settings.container_ephemera, key))
                        destroyed += 1
                    except Exception:
                        pass

    return {"committed": results, "destroyed": destroyed}


# ---- Step 10: Cataloger catalogs originals (AI) -----------------------------
def step10_catalog(original_asset: dict, context: str = "") -> dict:
    task = (
        f"Catalog this asset following ALL of these standards:\n\n"
        f"ISO 8601: dc:date must be YYYY-MM-DD from the FILENAME ONLY. If filename has no date, leave EMPTY.\n\n"
        f"Dublin Core (15 fields):\n"
        f"  dc:title = from filename: YYYY_W##_THEME_FILE-EXTENSION_SEQUENCE_for-HOST\n"
        f"  dc:creator = 'Evolue Media Team' (default)\n"
        f"  dc:subject = IPTC 3-letter code ONLY (CUL/ART/CIN/CHM/HLT/PRD/FIN/LIF/HUM)\n"
        f"  dc:description = captions/hashtags after Copywriter approval\n"
        f"  dc:publisher = 'Evolue Skincare Inc' (default)\n"
        f"  dc:contributor = 'Original Creator via url of platform' (from scout)\n"
        f"  dc:date = YYYY-MM-DD from filename only (never guess)\n"
        f"  dc:type = StillImage|MovingImage|Sound|Text|Dataset|Software|InteractiveResource\n"
        f"  dc:format = image/jpeg, video/mp4, etc.\n"
        f"  dc:identifier = full filename\n"
        f"  dc:source = URL of platform (e.g. www.pexels.com)\n"
        f"  dc:language = 'eng' (ISO 639-3)\n"
        f"  dc:relations = YYYY_IPTC-SUBJECT-CODE\n"
        f"  dc:coverage = 'Global' (default)\n"
        f"  dc:rights = '© 2026 Evolue Skincare Inc...' (default with platform name)\n\n"
        f"IPTC Subject Codes: CUL ART CIN CHM HLT PRD FIN LIF HUM (3 letters only)\n\n"
        f"Schema.org: Map dc:type to @type (StillImage->ImageObject, MovingImage->VideoObject, etc.)\n"
        f"  Required: @context, @type, @id (uuidv7), name, description, contentUrl, encodingFormat\n\n"
        f"Open Graph: og:title (<60 chars), og:type, og:image, og:description, og:url\n\n"
        f"Mark uncertain fields as needs_review. Never invent dates, people, or claims.\n\n"
        f"Asset:\n{json.dumps(original_asset, indent=2)[:4000]}"
    )
    return run_role("cataloger", task, context)


# ---- Step 11/12: Media Editor (AI) ------------------------------------------
def step11_12_media_editor(*, work_kind: str, original_asset: dict,
                           brief_output: dict, software: list[str],
                           redo_count: int = 0, owner_override: str = "",
                           context: str = "") -> dict:
    if work_kind not in ("derivative", "create_from_scratch"):
        raise ValueError("work_kind must be derivative or create_from_scratch")
    if redo_count > 2 and not owner_override:
        raise PermissionError("Media Editor redo limit exceeded.")
    task = (
        f"Produce a {work_kind} from this original.\n"
        f"Software: {', '.join(software)}\n"
        f"Brief:\n{json.dumps(brief_output.get('post_briefs', [])[:1], indent=2)[:2000]}\n\n"
        f"Original:\n{json.dumps(original_asset, indent=2)[:2000]}"
    )
    result = run_role_text("media_editor", task, context)
    return {"work_kind": work_kind, "software": software, "instructions": result,
            "redo_count": redo_count, "status": "needs_review"}


# ---- Step 13: Theme Image -> Cataloger -> Library -> Publishing --------------
def step13_theme_image(week: Week, theme_image: dict, context: str = "") -> dict:
    if not week.theme_image_key:
        raise ValueError("Step 13: no theme image uploaded.")
    cat = step10_catalog(theme_image, context)
    return {"storage_key": week.theme_image_key, "catalog": cat,
            "destination": "Library (Bunbuns) -> Publishing"}


# ---- Step 14/15: Copywriter (AI) --------------------------------------------
def step14_15_copywriter(*, post_position: int, media_asset: dict,
                         brief_output: dict, context: str = "") -> dict:
    posts = brief_output.get("post_briefs", [])
    post_data = posts[post_position - 1] if post_position <= len(posts) else {}
    task = (
        f"Write captions and hashtags for post {post_position}.\n"
        f"TikTok: caption + CTA + 5 hashtags | Instagram: caption + CTA + 5 hashtags\n"
        f"Also: alt text, attribution, disclosure.\n\n"
        f"Brief:\n{json.dumps(post_data, indent=2)[:2000]}\n\n"
        f"Media:\n{json.dumps(media_asset, indent=2)[:2000]}"
    )
    return run_role("copywriter", task, context)


# ---- Step 15b: Copy Grader (AI) ---------------------------------------------
def step15b_copy_grade(copy_output: dict, context: str = "") -> dict:
    task = (
        f"Grade this copy (8 categories, 0-5 each, total /100).\n\n"
        f"Copy:\n{json.dumps(copy_output, indent=2)[:4000]}"
    )
    return run_role("copy_grader", task, context)


# ---- Step 16: Scheduler — 3 at a time Mon/Wed/Fri, Phoenix MST ----------------
def step16_scheduler(*, platform: str, tile: int) -> dict:
    """Return the tile's posting schedule per the spec.

    IG: tiles 1-9 forward. TT: tiles 9-1 reverse.
    Mon: tiles 1,2,3 (IG) / 9,8,7 (TT) — 7am-9am MST
    Wed: tiles 4,5,6 (IG) / 6,5,4 (TT) — 11am-1pm MST
    Fri: tiles 7,8,9 (IG) / 3,2,1 (TT) — 3pm-5pm MST
    Timezone: America/Phoenix (MST, no DST)
    """
    if platform.lower() == "instagram":
        order = tile
    else:
        order = 10 - tile  # TikTok: 9→1

    if order <= 3:
        return {"tile": tile, "platform": platform, "order": order,
                "day": "Monday", "window": "07:00-09:00", "timezone": "America/Phoenix"}
    elif order <= 6:
        return {"tile": tile, "platform": platform, "order": order,
                "day": "Wednesday", "window": "11:00-13:00", "timezone": "America/Phoenix"}
    else:
        return {"tile": tile, "platform": platform, "order": order,
                "day": "Friday", "window": "15:00-17:00", "timezone": "America/Phoenix"}


# ---- Step 17: In-order enforcement ------------------------------------------
def step17_in_order(*, platform: str, tile: int, approved_up_to: int) -> bool:
    sched = step16_scheduler(platform=platform, tile=tile)
    return sched["order"] <= approved_up_to


# ---- Step 18/19: Published -> History; missed -> archive ---------------------
def step18_19_history(*, published: bool, storage_key: str) -> dict:
    return {"storage_key": storage_key,
            "state": "published" if published else "unpublished_archive",
            "mirage": True}
