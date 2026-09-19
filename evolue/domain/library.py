"""Library domain — the 9 immutable subject folders and asset identity.

Per The Library.txt (A.1.a + C.2): nine fixed subjects, each with a backup
folder for Raw Originals, a folder for Derivative Work not yet posted, and a
folder of formerly-posted work. Nothing broader than this renders at the top
level of the Library page.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SubjectFolder:
    code: str
    title: str
    raw_original_backup: str
    derivative_pending: str
    formerly_posted: str


def build_folders() -> tuple[SubjectFolder, ...]:
    from .subjects import SUBJECTS

    return tuple(
        SubjectFolder(
            code=s.code,
            title=s.title,
            raw_original_backup=f"{s.code} · {s.title} / Raw Originals (no UUID)",
            derivative_pending=f"{s.code} · {s.title} / Derivative Work (not yet posted)",
            formerly_posted=f"{s.code} · {s.title} / Formerly Posted (with dates)",
        )
        for s in SUBJECTS
    )


@dataclass
class AssetRow:
    """One row in asset_index (the atomic decomposition of the filename law)."""

    core_identifier: str
    uuid: str | None = None
    state: str = "STEP_0_ORIGINAL"
    asset_version: str = "v1-0"
    active_blob_path: str | None = None
    dc_fields: dict = field(default_factory=dict)

    def composite_name(self, *, theme: str, sequence: int, host: str, ext: str) -> str:
        """The owner's full filename law, applied in ONE place."""
        return f"{self.core_identifier}_{theme}_SEQ{sequence}_{host}.{ext}"
