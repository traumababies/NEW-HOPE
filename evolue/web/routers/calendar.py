"""Calendar page — plan themes 52 weeks ahead (The Library.txt A.4).

Behind login. Shows up to 9 weeks at a time; arrows advance 9 weeks.
Green checkmarks (approved tiles) render per the store.
"""
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from evolue.domain.calendar import Week, week_window
from evolue.infrastructure import planner_store
from evolue.main import templates
from evolue.web.routers.auth import login_redirect

router = APIRouter(prefix="", tags=["calendar"])

WEEKS_PER_PAGE = 9


def _page_context(request: Request) -> dict:
    return {
        "request": request,
        "weeks": planner_store.list_weeks(),
    }


@router.get("/calendar", response_class=HTMLResponse)
def calendar_page(request: Request, offset: int = 0):
    if login_redirect(request):
        return RedirectResponse("/login", status_code=303)

    anchor = date.today()
    window: list[Week] = []
    store_by_key = {f"{w.year}-W{w.week_number:02d}": w for w in planner_store.list_weeks()}
    for w in week_window(anchor, count=WEEKS_PER_PAGE):
        saved = store_by_key.get(f"{w.year}-W{w.week_number:02d}")
        window.append(saved if saved else w)

    return templates.TemplateResponse("calendar.html", {
        "request": request,
        "weeks": window,
        "active_nav": "calendar",
    })


def render_calendar(weeks: list[Week]) -> str:
    cards = []
    for w in weeks:
        tiles = []
        approved = sorted(w.approved_tiles)
        for i in range(1, 10):
            cls = "tile approved" if i in approved else "tile"
            check = (
                '<span class="check"><svg viewBox="0 0 24 24" width="12" height="12" '
                'fill="none" stroke="currentColor" stroke-width="3">'
                '<path d="M5 13l4 4L19 7"/></svg></span>'
                if i in approved
                else ""
            )
            tiles.append(f'<div class="{cls}" data-t="{i}"><span class="no">{i}</span>{check}</div>')
        cards.append(
            f"""
            <div class="week-card">
              <div class="week-head"><b>WEEK {w.week_number}</b></div>
              <div class="week-title">{w.theme or '—'}</div>
              <div class="tiles">{''.join(tiles)}</div>
              <div class="week-foot">{len(approved)} of 9 tiles approved</div>
            </div>
            """
        )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Calendar · Évolué</title>
<link rel="stylesheet" href="/static/ui.css">
<link rel="stylesheet" href="/static/godzilla.css">
<style>
  :root{{--ink:#7A8084;--muted:#8B9195;--quiet:#A9AEB2;--line:#CDD1D4;--green:#dfeee2;--green-ink:#3f6b4a}}
  *{{box-sizing:border-box}}html,body{{margin:0;background:#fff;color:var(--ink);font-family:"Jost","Segoe UI",sans-serif}}
  main{{max-width:1200px;margin:auto;padding:40px 44px}}
  h1{{font-weight:200;font-size:40px;margin:0 0 6px}}
  .sub{{color:var(--muted);font-size:13px;margin-bottom:30px}}
  .week-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
  .week-card{{border:1px solid var(--line);background:#fafbfb;min-width:0}}
  .week-head{{display:flex;align-items:center;justify-content:space-between;padding:12px 14px;border-bottom:1px solid var(--line)}}
  .week-head b{{font:600 10px "Archivo",sans-serif;letter-spacing:.14em;text-transform:uppercase}}
  .week-title{{padding:12px 14px;font-size:16px;line-height:1.4;min-height:50px}}
  .tiles{{display:grid;grid-template-columns:repeat(3,1fr)}}
  .tile{{aspect-ratio:4/5;border-right:1px solid var(--line);border-bottom:1px solid var(--line);position:relative;display:flex;align-items:center;justify-content:center;font:600 8px "Archivo",sans-serif}}
  .tile:nth-child(3n){{border-right:0}}
  .tile.approved{{background:var(--green);color:var(--green-ink)}}
  .tile.approved .check{{position:absolute;top:5px;right:6px;width:16px;height:16px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center}}
  .tile .no{{position:absolute;bottom:5px;left:6px}}
  .week-foot{{padding:9px 14px;color:var(--quiet);font:500 9px "Archivo",sans-serif;letter-spacing:.12em}}
</style></head><body>
<main>
  <h1>Calendar</h1>
  <div class="sub">Plan up to 52 weeks ahead. Light-green tiles = approved and queued for publishing.</div>
  <div class="week-grid">{''.join(cards)}</div>
</main>
</body></html>"""


@router.post("/weeks/{year}/{week_number}/theme")
def save_week_theme(request: Request, year: int, week_number: int, theme: str = Form(...)):
    if login_redirect(request):
        return RedirectResponse("/login", status_code=303)
    week = planner_store.get_week(year, week_number) or Week(year=year, week_number=week_number)
    week.theme = theme.strip()
    planner_store.save_week(week)
    return RedirectResponse("/calendar", status_code=303)


@router.get("/weeks/{year}/{week_number}", response_class=HTMLResponse)
def week_detail(request: Request, year: int, week_number: int):
    if login_redirect(request):
        return RedirectResponse("/login", status_code=303)
    week = planner_store.get_week(year, week_number) or Week(year=year, week_number=week_number)
    return templates.TemplateResponse("week.html", {
        "request": request,
        "week": week,
        "active_nav": "calendar",
    })
