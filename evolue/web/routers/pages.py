"""Pages router — serves .dc.html templates with proper view models."""
from __future__ import annotations
from datetime import date, timedelta
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from evolue.infrastructure import planner_store
from evolue.main import templates
from evolue.ui.view_models import BRAND, CalendarWeek, StudioState, build_calendar_context, build_studio_context
from evolue.web.routers.auth import login_redirect

router = APIRouter(tags=["pages"])


def _auth(request):
    if login_redirect(request):
        return RedirectResponse("/login", status_code=303)
    return None


@router.get("/calendar", response_class=HTMLResponse)
def calendar_page(request: Request, offset: int = 0):
    r = _auth(request)
    if r: return r
    today = date.today()
    store = {f"{w.year}-W{w.week_number:02d}": w for w in planner_store.list_weeks()}
    weeks = []
    for i in range(9):
        d = today + timedelta(weeks=i + offset)
        iso_d = d.isocalendar()
        key = f"{iso_d.year}-W{iso_d.week:02d}"
        saved = store.get(key)
        week_start = d - timedelta(days=d.weekday())
        weeks.append(CalendarWeek(
            id=key, week_number=iso_d.week, year=iso_d.year,
            theme=saved.theme if saved else "",
            week_start=week_start, week_end=week_start + timedelta(days=6),
            planning_week_number=iso_d.week,
        ))
    return templates.TemplateResponse("Calendar.dc.html", build_calendar_context(weeks, request))


@router.get("/studio", response_class=HTMLResponse)
def studio_page(request: Request, week: int = 0):
    r = _auth(request)
    if r: return r
    today = date.today()
    week_no = week or today.isocalendar().week
    saved = planner_store.get_week(today.year, week_no)
    return templates.TemplateResponse("Studio.dc.html",
        build_studio_context(request, week_no=week_no, theme=saved.theme if saved else "", year=today.year))


@router.get("/week", response_class=HTMLResponse)
def week_page(request: Request):
    r = _auth(request)
    if r: return r
    from evolue.domain.calendar import Week
    today = date.today()
    week = planner_store.get_week(today.year, today.isocalendar().week) or Week(year=today.year, week_number=today.isocalendar().week)
    return templates.TemplateResponse("Week.dc.html", {"request": request, "brand": BRAND, "week": week})


@router.get("/post", response_class=HTMLResponse)
def post_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("Post.dc.html", {"request": request, "brand": BRAND})


@router.get("/media-editor", response_class=HTMLResponse)
def media_editor_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("MediaEditor.dc.html", {"request": request, "brand": BRAND})


@router.get("/library", response_class=HTMLResponse)
def library_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("Library.dc.html", {"request": request, "brand": BRAND})


@router.get("/library/reviews", response_class=HTMLResponse)
def library_reviews_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("LibraryReviews.dc.html", {"request": request, "brand": BRAND})


@router.get("/approvals", response_class=HTMLResponse)
def approvals_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("Approvals.dc.html", {"request": request, "brand": BRAND})


@router.get("/publishing", response_class=HTMLResponse)
def publishing_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("Publishing.dc.html", {"request": request, "brand": BRAND})


@router.get("/history", response_class=HTMLResponse)
def history_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("History.dc.html", {"request": request, "brand": BRAND})


@router.get("/history/{post_id}", response_class=HTMLResponse)
def history_detail_page(request: Request, post_id: str):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("HistoryDetail.dc.html", {"request": request, "brand": BRAND, "post_id": post_id})


@router.get("/settings/brand", response_class=HTMLResponse)
def brand_settings_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("BrandSettings.dc.html", {"request": request, "brand": BRAND})


@router.get("/subjects", response_class=HTMLResponse)
def subjects_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("Subjects.dc.html", {"request": request, "brand": BRAND})


@router.get("/shared-room", response_class=HTMLResponse)
def shared_room_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("SharedRoom.dc.html", {"request": request, "brand": BRAND})


@router.get("/shared-library", response_class=HTMLResponse)
def shared_library_page(request: Request):
    r = _auth(request)
    if r: return r
    return templates.TemplateResponse("SharedLibrary.dc.html", {"request": request, "brand": BRAND})
