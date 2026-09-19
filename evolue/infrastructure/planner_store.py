"""Planner store (calendar + weeks).

Dev/local store is a JSON file under `data/` (git-ignored). The SQL adapter is
the production boundary; this exists so the app is usable before Azure SQL is
whitelisted, and mirrors the same CRUD surface.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from ..domain.calendar import Week

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
CALENDAR_FILE = DATA_DIR / "calendar.json"


def _load() -> dict:
    if not CALENDAR_FILE.exists():
        return {"weeks": {}, "updated_at": ""}
    try:
        return json.loads(CALENDAR_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"weeks": {}, "updated_at": ""}


def _save(data: dict) -> None:
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    CALENDAR_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _key(year: int, week_number: int) -> str:
    return f"{year}-W{week_number:02d}"


def to_state(week: Week) -> dict:
    return {
        "year": week.year,
        "week_number": week.week_number,
        "theme": week.theme,
        "theme_image_key": week.theme_image_key,
        "approved_tiles": sorted(week.approved_tiles),
        "theme_image_approved": week.theme_image_approved,
        "status": week.status,
        "start": week.start.isoformat(),
        "end": week.end.isoformat(),
    }


def from_state(row: dict) -> Week:
    return Week(
        year=int(row["year"]),
        week_number=int(row["week_number"]),
        theme=row.get("theme", ""),
        theme_image_key=row.get("theme_image_key", ""),
        approved_tiles=set(row.get("approved_tiles", [])),
        theme_image_approved=bool(row.get("theme_image_approved", False)),
        status=row.get("status", "planning"),
    )


def save_week(week: Week) -> None:
    data = _load()
    data["weeks"][_key(week.year, week.week_number)] = to_state(week)
    _save(data)


def get_week(year: int, week_number: int) -> Week | None:
    data = _load()
    row = data["weeks"].get(_key(year, week_number))
    return from_state(row) if row else None


def list_weeks() -> list[Week]:
    data = _load()
    return [from_state(row) for row in data["weeks"].values()]
