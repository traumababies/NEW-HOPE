"""Content Scout provider runners — STEPS 7/8.

Each scout is a dedicated agent for ONE platform, per The Library.txt B.8:
  - Pixabay  : per_page=200, page 1 only
  - Pexels   : per_page=80,  page 1 only
  - Unsplash : per_page=30, hard 12s delay between the 9 subjects,
               page 2 ONLY if page 1 < 3 relevant matches
  - Coverr   : page_size=20, hard 12s delay between the 9 subjects, page 1 only

Results are provisional metadata (dc:contributor / dc:source / dc:rights /
dc:type / dc:format) + a download URL. They are NOT written anywhere that is
the Library — they'll be quarantined to Ephemera by the caller.
"""
from __future__ import annotations

import time

import requests

from evolue.config import settings

SUBJECT_CODES = ("CUL", "ART", "CIN", "CHM", "HLT", "PRD", "FIN", "LIF", "HUM")


class ScoutError(RuntimeError):
    pass


def _get_json(url: str, *, headers: dict | None = None, params: dict | None = None, timeout: int = 30) -> dict:
    try:
        resp = requests.get(url, headers=headers or {}, params=params or {}, timeout=timeout)
        resp.raise_for_status()
        body = resp.json()
    except (requests.RequestException, ValueError) as exc:
        raise ScoutError(f"{type(exc).__name__}: {exc}") from exc
    if not isinstance(body, dict):
        raise ScoutError("Provider returned non-object JSON.")
    return body


# --- Pixabay ---
def search_pixabay(query: str, *, media: str = "image") -> list[dict]:
    if not settings.pixabay_api_key:
        return []
    base = "https://pixabay.com/api/videos/" if media == "video" else "https://pixabay.com/api/"
    body = _get_json(
        base,
        params={
            "key": settings.pixabay_api_key,
            "q": query,
            "per_page": settings.scout_pixabay_per_page,
            "safesearch": "true",
        },
    )
    out = []
    for it in body.get("hits", []):
        url = ""
        if media == "video":
            url = (it.get("videos") or {}).get("large", {}).get("url", "")
        else:
            url = it.get("largeImageURL", "")
        out.append({
            "provider": "pixabay",
            "media": media,
            "query": query,
            "dc_contributor": it.get("user", ""),
            "dc_source": "pixabay.com",
            "dc_rights": "Pixabay license",
            "dc_type": "MovingImage" if media == "video" else "StillImage",
            "dc_format": "video/mp4" if media == "video" else "image/jpeg",
            "download_url": url,
            "title": it.get("tags", ""),
            "page": it.get("pageURL", ""),
        })
    return out


# --- Pexels ---
def search_pexels(query: str, *, media: str = "image") -> list[dict]:
    if not settings.pexels_api_key:
        return []
    url = "https://api.pexels.com/videos/search" if media == "video" else "https://api.pexels.com/v1/search"
    body = _get_json(
        url,
        headers={"Authorization": settings.pexels_api_key},
        params={"query": query, "per_page": settings.scout_pexels_per_page},
    )
    items = body.get("videos", []) if media == "video" else body.get("photos", [])
    out = []
    for it in items:
        if media == "video":
            files = sorted(it.get("video_files", []), key=lambda f: f.get("width", 0) or 0)
            url = (files[0] if files else {}).get("link", "")
        else:
            url = (it.get("src") or {}).get("original", "")
        out.append({
            "provider": "pexels",
            "media": media,
            "query": query,
            "dc_contributor": it.get("photographer") or (it.get("user") or {}).get("name", ""),
            "dc_source": "pexels.com",
            "dc_rights": "Pexels license",
            "dc_type": "MovingImage" if media == "video" else "StillImage",
            "dc_format": "video/mp4" if media == "video" else "image/jpeg",
            "download_url": url,
            "title": it.get("alt") or it.get("url", ""),
            "page": it.get("url", ""),
        })
    return out


# --- Unsplash (images only) ---
def search_unsplash(query: str) -> list[dict]:
    if not settings.unsplash_access_key:
        return []
    body = _get_json(
        "https://api.unsplash.com/search/photos",
        headers={"Authorization": f"Client-ID {settings.unsplash_access_key}"},
        params={"query": query, "per_page": settings.scout_unsplash_per_page, "orientation": "portrait"},
    )
    out = []
    for it in body.get("results", []):
        out.append({
            "provider": "unsplash",
            "media": "image",
            "query": query,
            "dc_contributor": (it.get("user") or {}).get("name", ""),
            "dc_source": "unsplash.com",
            "dc_rights": "Unsplash license",
            "dc_type": "StillImage",
            "dc_format": "image/jpeg",
            "download_url": (it.get("urls") or {}).get("raw", ""),
            "title": it.get("alt_description") or it.get("description") or "",
            "page": (it.get("links") or {}).get("html", ""),
        })
    return out


# --- Coverr (videos only) ---
def search_coverr(query: str) -> list[dict]:
    if not settings.coverr_api_key:
        return []
    body = _get_json(
        "https://api.coverr.co/videos",
        headers={"Authorization": f"Bearer {settings.coverr_api_key}"},
        params={"query": query, "page_size": settings.scout_coverr_page_size},
    )
    out = []
    for it in body.get("hits", []):
        out.append({
            "provider": "coverr",
            "media": "video",
            "query": query,
            "dc_contributor": it.get("contributor_name") or "Coverr",
            "dc_source": "coverr.co",
            "dc_rights": "Coverr license",
            "dc_type": "MovingImage",
            "dc_format": "video/mp4",
            "download_url": it.get("download_url") or it.get("url", ""),
            "title": it.get("title", ""),
            "page": it.get("url", ""),
        })
    return out


# --- Orchestration: one scout per platform, all 9 subjects, sleeps between ---
def run_platform(platform: str, queries: dict[str, str], *, sleep_between: float = 0.0) -> dict[str, list[dict]]:
    """Run one platform across the subjects. queries: {subject_code: query}."""
    results: dict[str, list[dict]] = {}
    for idx, (code, query) in enumerate(queries.items()):
        if idx:
            time.sleep(sleep_between)
        if platform == "pixabay":
            results[code] = search_pixabay(query, media="image") + search_pixabay(query, media="video")
        elif platform == "pexels":
            results[code] = search_pexels(query, media="image") + search_pexels(query, media="video")
        elif platform == "unsplash":
            results[code] = search_unsplash(query)
        elif platform == "coverr":
            results[code] = search_coverr(query)
        else:
            raise ScoutError(f"unknown platform: {platform}")
    return results

