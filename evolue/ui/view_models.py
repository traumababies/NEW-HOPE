"""View models — build template context for .dc.html pages.

Each page needs specific data structures. This module creates them
from the planner store and domain models.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Brand:
    company_name: str = "Évolué"
    logo_url: str = "/static/brand/logo.svg"


@dataclass
class Flash:
    level: str = ""
    message: str = ""


@dataclass
class WeekStatus:
    value: str = "planning"  # planning | skipped | approved | published


@dataclass
class PostStatus:
    value: str = "pending"  # pending | approved | rejected | redo | replace


@dataclass
class CalendarPost:
    id: str = ""
    visual_position: int = 0
    creative_status: PostStatus = field(default_factory=PostStatus)


@dataclass
class CalendarWeek:
    id: str = ""
    week_number: int = 0
    year: int = 0
    theme: str = ""
    thoughts: str = ""
    status: WeekStatus = field(default_factory=WeekStatus)
    planning_week_number: int = 0
    week_start: date = None
    week_end: date = None
    posts: list = field(default_factory=list)
    approved_count: int = 0
    published_count: int = 0

    def __post_init__(self):
        if self.week_start is None:
            self.week_start = date.today()
        if self.week_end is None:
            self.week_end = self.week_start + timedelta(days=6)


@dataclass
class WeekGroup:
    label: str = ""
    weeks: list = field(default_factory=list)


@dataclass
class Assistant:
    kind: str = ""
    name: str = ""


@dataclass
class StudioState:
    year: int = 2026
    week_no: int = 0
    theme: str = ""
    week_prev: int = 0
    week_next: int = 0


BRAND = Brand()
DEFAULT_ASSISTANTS = [
    Assistant("creative_director", "Creative Director"),
    Assistant("copywriter", "Copywriter"),
    Assistant("muse", "Muse"),
    Assistant("cataloger", "Cataloger"),
    Assistant("media_editor", "Media Editor"),
]


def build_calendar_context(weeks, request, brand=None):
    """Build context for Calendar.dc.html from a list of CalendarWeek objects."""
    if not weeks:
        today = date.today()
        iso = today.isocalendar()
        weeks = [CalendarWeek(
            id=f"{today.year}-W{iso.week:02d}",
            week_number=iso.week, year=today.year,
            week_start=today - timedelta(days=today.weekday()),
        )]

    # Group by month
    groups = []
    current_month = ""
    for w in weeks:
        month_label = w.week_start.strftime("%B %Y") if w.week_start else ""
        if month_label != current_month:
            groups.append(WeekGroup(label=month_label, weeks=[]))
            current_month = month_label
        groups[-1].weeks.append(w)

    # Window dates
    window_start = weeks[0].week_start if weeks else date.today()
    window_end = weeks[-1].week_end if weeks else date.today()
    prev_start = window_start - timedelta(weeks=9)
    next_start = window_end + timedelta(days=1)

    return {
        "request": request,
        "brand": brand or BRAND,
        "flash": None,
        "groups": groups,
        "weeks": weeks,
        "window_start": window_start,
        "window_end": window_end,
        "previous_start": prev_start,
        "next_start": next_start,
        "assistants": DEFAULT_ASSISTANTS,
    }


def build_studio_context(request, week_no=0, theme="", year=2026, brand=None):
    """Build context for Studio.dc.html."""
    return {
        "request": request,
        "brand": brand or BRAND,
        "state": StudioState(
            year=year, week_no=week_no, theme=theme,
            week_prev=max(1, week_no - 1), week_next=week_no + 1,
        ),
    }