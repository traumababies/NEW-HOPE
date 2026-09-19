"""The nine immutable editorial subjects (IPTC codes only — no numbers).

Source: owner's `The Library.txt` (B.8 / C.2). These are the fixed 1:1 mapping
for the nine posts each week.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Subject:
    code: str       # IPTC 3-letter code
    title: str
    purpose: str


SUBJECTS: tuple[Subject, ...] = (
    Subject("CUL", "Historical Beauty Rituals & Culture", "Culture, customs, and heritage traditions"),
    Subject("ART", "Museum Art About Beauty", "Libraries & Museums / Fine Art Exhibitions"),
    Subject("CIN", "Hollywood & Editorial Philosophy", "Cinema / Film Industry"),
    Subject("CHM", "Organic/Raw vs Synthetic Ingredients", "Chemicals / Organic Compounds"),
    Subject("HLT", "Wellness and Healthy Habits", "Health / Welfare (health and safety)"),
    Subject("PRD", "Évolué Product Shot", "Consumer Products"),
    Subject("FIN", "Évolué History", "Business Brands"),
    Subject("LIF", "Holidays", "Festive Events, Holidays, Seasonal Observances"),
    Subject("HUM", "Texture / Sensory", "Human Interest & Novelty / Visual Art & Design"),
)

SUBJECT_CODES: frozenset[str] = frozenset(s.code for s in SUBJECTS)


def subject_by_code(code: str) -> Subject | None:
    for subject in SUBJECTS:
        if subject.code == code:
            return subject
    return None
