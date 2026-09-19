"""AI Team router — exposes workflow STEPS 1-19 as API endpoints.

The Studio, Calendar, Library, and Publishing pages call these endpoints
to trigger AI roles (Creative Director, Muse, Cataloger, Copywriter, etc.)
and retrieve structured results.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from evolue.web.routers.auth import require_owner

router = APIRouter(prefix="/api/ai", tags=["ai-team"])


# ---- Request/Response models ------------------------------------------------

class BriefRequest(BaseModel):
    year: int
    week_number: int
    theme: str
    context: str = ""


class BriefValidateRequest(BaseModel):
    brief_output: dict
    context: str = ""


class MuseRequest(BaseModel):
    brief_output: dict
    approved_assets: list[dict] = []
    context: str = ""


class ScoutFetchRequest(BaseModel):
    scout_requests: list[dict]
    year: int
    week_number: int


class CatalogRequest(BaseModel):
    original_asset: dict
    context: str = ""


class MediaEditorRequest(BaseModel):
    work_kind: str
    original_asset: dict
    brief_output: dict
    software: list[str] = []
    redo_count: int = 0
    context: str = ""


class CopywriterRequest(BaseModel):
    post_position: int
    media_asset: dict
    brief_output: dict
    context: str = ""


# ---- Step 2: Creative Director ------------------------------------------------
@router.post("/brief/compose")
def compose_brief(req: BriefRequest, _=Depends(require_owner)):
    from evolue.domain.calendar import Week
    from evolue.application.services.workflow import step2_compose_brief
    week = Week(year=req.year, week_number=req.week_number, theme=req.theme)
    try:
        return step2_compose_brief(week, context=req.context)
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 2b: Current Events --------------------------------------------------
@router.post("/brief/current-events")
def current_events(req: BriefValidateRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step2b_current_events
    try:
        return step2b_current_events(req.brief_output, req.context)
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 2c: Fact Check ------------------------------------------------------
@router.post("/brief/fact-check")
def fact_check(req: BriefValidateRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step2c_fact_check
    try:
        return step2c_fact_check(req.brief_output, req.context)
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 3b: Brief Validator --------------------------------------------------
@router.post("/brief/validate")
def validate_brief(req: BriefValidateRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step3b_validate_brief
    try:
        return step3b_validate_brief(req.brief_output, req.context)
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 3c: Creative Grader --------------------------------------------------
@router.post("/brief/creative-grade")
def creative_grade(req: BriefValidateRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step3c_creative_grade
    try:
        return step3c_creative_grade(req.brief_output, req.context)
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 3d: Production Grader ------------------------------------------------
@router.post("/brief/production-grade")
def production_grade(req: BriefValidateRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step3d_production_grade
    try:
        return step3d_production_grade(req.brief_output, req.context)
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 5: Muse -------------------------------------------------------------
@router.post("/muse/search")
def muse_search(req: MuseRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step5_muse_search
    try:
        return step5_muse_search(req.brief_output, req.approved_assets, req.context)
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 7/8: Scout Fetch ----------------------------------------------------
@router.post("/scouts/fetch")
def scout_fetch(req: ScoutFetchRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step7_8_scout_fetch
    try:
        return {"results": step7_8_scout_fetch(req.scout_requests, req.year, req.week_number)}
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 9: Studio Commit ----------------------------------------------------
@router.post("/studio/commit")
def studio_commit(req: CommitRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step9_studio_commit
    try:
        return step9_studio_commit(req.brief_id, req.selected_tiles)
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 10: Cataloger -------------------------------------------------------
@router.post("/catalog")
def catalog(req: CatalogRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step10_catalog
    try:
        return step10_catalog(req.original_asset, req.context)
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 11/12: Media Editor --------------------------------------------------
@router.post("/media-editor")
def media_editor(req: MediaEditorRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step11_12_media_editor
    try:
        return step11_12_media_editor(
            work_kind=req.work_kind, original_asset=req.original_asset,
            brief_output=req.brief_output, software=req.software,
            redo_count=req.redo_count, context=req.context,
        )
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 14/15: Copywriter ---------------------------------------------------
@router.post("/copywriter")
def copywriter(req: CopywriterRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step14_15_copywriter
    try:
        return step14_15_copywriter(
            post_position=req.post_position, media_asset=req.media_asset,
            brief_output=req.brief_output, context=req.context,
        )
    except Exception as e:
        raise HTTPException(500, str(e))


# ---- Step 15b: Copy Grader ----------------------------------------------------
@router.post("/copy-grade")
def copy_grade(req: CopyGradeRequest, _=Depends(require_owner)):
    from evolue.application.services.workflow import step15b_copy_grade
    try:
        return step15b_copy_grade(req.copy_output, req.context)
    except Exception as e:
        raise HTTPException(500, str(e))
    from evolue.application.services.workflow import step3d_production_grade
    try:
        return step3d_production_grade(req.brief_output, req.context)
    except Exception as e:
        raise HTTPException(500, str(e))


class CopyGradeRequest(BaseModel):
    copy_output: dict
    context: str = ""


class CommitRequest(BaseModel):
    brief_id: str
    selected_tiles: list[str]
