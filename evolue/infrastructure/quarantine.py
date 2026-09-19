"""Ephemera quarantine — STEPS 7/8.

Scout candidates land in the Ephemera container (provisional names), are held
for Studio review, and NEVER touch the Library. Unselected candidates are
deleted when Jean COMMITs (S9); selected ones promote to Bunbuns via
copy-first and the Ephemera copy is deleted.

Only metadata (and an optional poster) is written here — the heavy original is
never downloaded into app storage at search time. Downloads happen only on an
owner Accept (Studio), per the owner rule.
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

from .storage import BlobRef, delete_blob, ensure_container, mirage_url, put_blob
from evolue.config import settings
from evolue.domain.naming import scout_assignment_name


def quarantine_candidates(*, platform: str, subject_code: str, year: int, week_number: int, candidates: list[dict]) -> list[dict]:
    """Persist candidate metadata into the ephemera container and return records.

    Each record gets a provisional key derived from the scout naming law
    (YYYY_W##_IPTC-Subject-Code_SEQUENCE). Heavy files are NOT downloaded; only
    a tiny poster (if the source provides a thumbnail URL) is stored so the
    Studio grid has a mirage to show.
    """
    ensure_container(settings.container_ephemera)
    records = []
    for i, cand in enumerate(candidates, start=1):
        base = scout_assignment_name(year, week_number, subject_code, i)
        poster_url = cand.get("poster_url") or cand.get("preview_url") or ""
        poster_key = ""
        if poster_url:
            try:
                poster_key = f"scout-candidates/{base}.poster.jpg"
                # Fetch the small poster only (not the full file).
                import requests

                r = requests.get(poster_url, timeout=15)
                if r.status_code == 200 and len(r.content) > 0:
                    put_blob(BlobRef(settings.container_ephemera, poster_key), r.content, content_type="image/jpeg")
            except Exception:
                poster_key = ""
        records.append({
            "platform": platform,
            "subject_code": subject_code,
            "sequence": i,
            "assignment_name": base,
            "provider": cand.get("provider", ""),
            "media": cand.get("media", ""),
            "dc_contributor": cand.get("dc_contributor", ""),
            "dc_source": cand.get("dc_source", ""),
            "dc_rights": cand.get("dc_rights", ""),
            "dc_type": cand.get("dc_type", ""),
            "dc_format": cand.get("dc_format", ""),
            "download_url": cand.get("download_url", ""),
            "title": cand.get("title", ""),
            "page": cand.get("page", ""),
            "poster_key": poster_key,
            "status": "in_ephemera",
            "quarantined_at": datetime.now(timezone.utc).isoformat(),
        })
    return records


def delete_ephemera(key: str) -> None:
    delete_blob(BlobRef(settings.container_ephemera, key))
