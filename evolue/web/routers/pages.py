"""Pages router — serves the .dc.html templates."""
from __future__ import annotations
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from evolue.domain.calendar import Week
from evolue.infrastructure import planner_store
from evolue.main import templates
from evolue.web.routers.auth import login_redirect

router = APIRouter(tags=["pages"])
BRAND = {"company_name": "\u00c9volu\u00e9", "logo_url": "/static/brand/logo.svg"}


def _auth(request):
    if login_redirect(request):
        return RedirectResponse("/login", status_code=303)
    return None


def _ctx(request, **kw):
    base = {"request": request, "brand": BRAND}
    base.update(kw)
    return base


@router.get("/calendar", response_class=HTMLResponse)
def calendar_page(request: Request, offset: int = 0):
    r = _auth(request)
    if r: return r
    from datetime import date
    from evolue.domain.calendar import week_window
    anchor = date.today()
    store = {f"{w.year}-W{w.week_number:02d}": w for w in planner_store.list_weeks()}
    weeks = []
    for w in week_window(anchor, count=9):
        saved = store.get(f"{w.year}-W{w.week_number:02d}")
        weeks.append(saved if saved else w)
    return templates.TemplateResponse("Calendar.dc.html", _ctx(request, active_page="calendar", weeks=weeks))


@router.get("/week", response_class=HTMLResponse)
def week_page(request: Request):
    r = _auth(request)
    if r: return r
    from datetime import date
    today = date.today()
    week = planner_store.get_week(today.year, today.isocalendar().week) or Week(year=today.year, week_number=today.isocalendar().week)
    return templates.TemplateResponse("Week.dc.html", _ctx(request, active_page="week", week=week))


@router.get("/post", response_class=HTMLResponse)
def post_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("Post.dc.html", _ctx(request, active_page="post"))


@router.get("/media-editor", response_class=HTMLResponse)
def media_editor_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("MediaEditor.dc.html", _ctx(request, active_page="media_editor"))


@router.get("/studio", response_class=HTMLResponse)
def studio_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("Studio.dc.html", _ctx(request, active_page="studio", state={}))


@router.get("/library", response_class=HTMLResponse)
def library_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("Library.dc.html", _ctx(request, active_page="library"))


@router.get("/library/reviews", response_class=HTMLResponse)
def library_reviews_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("LibraryReviews.dc.html", _ctx(request, active_page="reviews"))


@router.get("/approvals", response_class=HTMLResponse)
def approvals_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("Approvals.dc.html", _ctx(request, active_page="approvals"))


@router.get("/publishing", response_class=HTMLResponse)
def publishing_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("Publishing.dc.html", _ctx(request, active_page="publishing"))


@router.get("/history", response_class=HTMLResponse)
def history_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("History.dc.html", _ctx(request, active_page="history"))


@router.get("/history/{post_id}", response_class=HTMLResponse)
def history_detail_page(request: Request, post_id: str):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("HistoryDetail.dc.html", _ctx(request, active_page="history", post_id=post_id))


@router.get("/settings/brand", response_class=HTMLResponse)
def brand_settings_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("BrandSettings.dc.html", _ctx(request, active_page="brand_settings"))


@router.get("/subjects", response_class=HTMLResponse)
def subjects_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("Subjects.dc.html", _ctx(request, active_page="subjects"))


@router.get("/shared-room", response_class=HTMLResponse)
def shared_room_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("SharedRoom.dc.html", _ctx(request, active_page="shared_room"))


@router.get("/shared-library", response_class=HTMLResponse)
def shared_library_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("SharedLibrary.dc.html", _ctx(request, active_page="shared_library"))
