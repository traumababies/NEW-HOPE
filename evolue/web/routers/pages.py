"""Pages router — Calendar, Week, Creative Brief, Approvals, Post,
Media Editor, Publishing, History, Learning Center, Library, Brand Settings.
"""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from evolue.domain.calendar import Week
from evolue.domain.subjects import SUBJECTS
from evolue.infrastructure import planner_store
from evolue.infrastructure.sql.db import fetch_all
from evolue.main import templates
from evolue.web.routers.auth import login_redirect

router = APIRouter(tags=["pages"])


def _auth(request: Request):
    if login_redirect(request):
        return RedirectResponse("/login", status_code=303)
    return None


@router.get("/brief/{year}/{week_number}", response_class=HTMLResponse)
def brief_page(request: Request, year: int, week_number: int):
    redir = _auth(request)
    if redir:
        return redir
    week = planner_store.get_week(year, week_number) or Week(year=year, week_number=week_number)
    return templates.TemplateResponse("creative_brief.html", {
        "request": request, "week": week, "active_nav": "brief",
    })


@router.get("/approvals", response_class=HTMLResponse)
def approvals_page(request: Request):
    redir = _auth(request)
    if redir:
        return redir
    try:
        pending = fetch_all("SELECT * FROM jan_requests WHERE status='pending' ORDER BY id")
    except Exception:
        pending = []
    return templates.TemplateResponse("approvals.html", {
        "request": request, "pending": pending, "active_nav": "approvals",
    })


@router.post("/approvals/{jan_id}/decide")
def approve_or_reject(request: Request, jan_id: int, decision: str = Form(...), note: str = Form("")):
    redir = _auth(request)
    if redir:
        return redir
    from evolue.config import settings
    from evolue.domain.jan_gate import resolve_jan
    try:
        resolve_jan(jan_id=jan_id, decision=decision, owner_password=settings.owner_password, note=note)
    except Exception:
        pass
    return RedirectResponse("/approvals", status_code=303)


@router.get("/post/{year}/{week_number}/{position}", response_class=HTMLResponse)
def post_page(request: Request, year: int, week_number: int, position: int):
    redir = _auth(request)
    if redir: return redir
    return templates.TemplateResponse("post.html", {
        "request": request, "year": year, "week_number": week_number,
        "position": position, "subject_code": "", "title": "", "active_nav": "brief",
    })


@router.get("/media-editor", response_class=HTMLResponse)
def media_editor_page(request: Request):
    redir = _auth(request)
    if redir: return redir
    return templates.TemplateResponse("media_editor.html", {"request": request, "active_nav": "media_editor"})


@router.get("/publishing", response_class=HTMLResponse)
def publishing_page(request: Request):
    redir = _auth(request)
    if redir: return redir
    return templates.TemplateResponse("publishing.html", {"request": request, "active_nav": "publishing"})


@router.get("/history", response_class=HTMLResponse)
def history_page(request: Request):
    redir = _auth(request)
    if redir: return redir
    return templates.TemplateResponse("history.html", {
        "request": request, "published": [], "archived": [], "active_nav": "history",
    })


@router.get("/learning", response_class=HTMLResponse)
def learning_page(request: Request):
    redir = _auth(request)
    if redir: return redir
    return templates.TemplateResponse("learning.html", {
        "request": request, "taste_tags": [], "knowledge": [], "active_nav": "learning",
    })


@router.get("/library", response_class=HTMLResponse)
def library_page(request: Request):
    redir = _auth(request)
    if redir: return redir
    return templates.TemplateResponse("library.html", {
        "request": request, "subjects": SUBJECTS, "active_nav": "library",
    })


@router.get("/settings/brand", response_class=HTMLResponse)
def brand_settings_page(request: Request):
    redir = _auth(request)
    if redir: return redir
    return templates.TemplateResponse("brand_settings.html", {
        "request": request, "brand": {}, "active_nav": "settings",
    })


@router.post("/settings/brand")
def save_brand_settings(request: Request, brand_voice: str = Form(""), tone_notes: str = Form(""),
                        prohibited: str = Form(""), taste_prefs: str = Form(""),
                        taste_exclusions: str = Form("")):
    redir = _auth(request)
    if redir: return redir


@router.get("/studio", response_class=HTMLResponse)
@router.get("/studio/{year}/{week_number}", response_class=HTMLResponse)
def studio_page(request: Request, year: int = 0, week_number: int = 0):
    redir = _auth(request)
    if redir: return redir
    candidates = []
    if year and week_number:
        try:
            candidates = fetch_all(
                "SELECT * FROM ephemera_candidates WHERE year=? AND week_number=? ORDER BY subject_code, sequence",
                (year, week_number),
            )
        except Exception:
            candidates = []
    return templates.TemplateResponse("studio.html", {
        "request": request, "candidates": candidates,
        "year": year or 2026, "week_number": week_number or 0, "theme": "",
        "active_nav": "studio",
    })
    return RedirectResponse("/settings/brand", status_code=303)