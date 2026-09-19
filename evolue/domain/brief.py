"""Weekly Creative Brief — THE shared artifact (A.10, D, WEEKLY-CREATIVE-BRIEF-TEMPLATE).

The FORM per The Library.txt:
- title format: YYYY_W##_THEME_HOST
- 10 panels: 1 theme-image panel (tiles TI01..TI09) + 9 post panels (tiles 1..9)
- each panel + each tile is Approve/Reject/Replace (A/R/R) independently
- a Media-Editor section (derivative vs create-from-scratch + software choices)
- an owner comment box at every review fork
- graders (Validator / Creative / Production) attached at the end (E.2, D)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Literal

Approval = Literal["pending", "approved", "rejected", "replaced"]


@dataclass
class Tile:
    index: int
    iptc_code: str        # post tiles: IPTC subject code
    sequence: int = 0     # 1..9
    description: str = ""
    approval: Approval = "pending"
    source: str = ""      # scout | muse | generated | owner_upload

    def label(self) -> str:
        # Top-right corner format: IPTC-Subject-Code_Sequence##
        return f"{self.iptc_code}_{self.sequence:02d}"


@dataclass
class Panel:
    index: int
    title: str            # TI01..TI09 for theme image; post index for posts
    tiles: list[Tile] = field(default_factory=list)
    approval: Approval = "pending"
    description: str = ""
    comment: str = ""     # owner comment at this fork


@dataclass
class MediaEditorChoice:
    post: int
    work_kind: Literal["derivative", "create_from_scratch"] = "derivative"
    software: list[str] = field(default_factory=list)  # ComfyUI / Ace Studio / Music Gen / Hunyuan
    note: str = ""


@dataclass
class WeeklyBrief:
    brief_id: str        # format: YYYY_W##_THEME_HOST
    week_start: date
    week_end: date
    theme: str
    theme_image_panel: Panel
    post_panels: list[Panel] = field(default_factory=list)
    creative_direction: str = ""
    music_direction: str = ""
    media_editor_choices: list[MediaEditorChoice] = field(default_factory=list)
    status: str = "draft"           # draft | needs_validator | needs_graders | jans_pending | approved
    validator: dict = field(default_factory=dict)   # {verdict, structural_score, notes}
    creative_grader: dict = field(default_factory=dict)
    production_grader: dict = field(default_factory=dict)

    def title(self) -> str:
        return self.brief_id

    def all_tiles(self):
        return (t for panel in [self.theme_image_panel, *self.post_panels] for t in panel.tiles)

    def is_complete(self) -> bool:
        return all(
            len(p.tiles) == 9 and all(t.description.strip() for t in p.tiles)
            for p in [self.theme_image_panel, *self.post_panels]
        )


def compose_brief_id(year: int, week_number: int, theme_host: str) -> str:
    """YYYY_W##_THEME_HOST (The Library D.4.ii)."""
    return f"{year}_W{week_number:02d}_{theme_host}"
