"""Calendar domain — the weekly planner.

The Library.txt A.4: Jean writes the THEME for up to 52 weeks ahead on the
calendar; light-green checkmarks mark approved tiles; arrows move 9 weeks.
Week status: planning -> theme_set -> tiles_approved -> publishing.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Week:
    week_number: int
    year: int
    theme: str = ""
    theme_image_key: str = ""            # blob key or local path
    approved_tiles: set[int] = field(default_factory=set)   # 1..9 (post tiles)
    theme_image_approved: bool = False
    status: str = "planning"             # planning | theme_set | tiles_approved | publishing | archived

    @property
    def start(self) -> date:
        # ISO week start (Monday) for (year, week_number)
        return date.fromisocalendar(self.year, self.week_number, 1)

    @property
    def end(self) -> date:
        return self.start + timedelta(days=6)


def week_window(anchor: date, count: int = 9) -> list[Week]:
    """Return `count` weeks starting at the anchor's Monday week (forward)."""
    iso = anchor.isocalendar()
    weeks = []
    for offset in range(count):
        w = Week(
            week_number=iso.week + offset,
            year=iso.year,
        )
        weeks.append(w)
    return weeks
