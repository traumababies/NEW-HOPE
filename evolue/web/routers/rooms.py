"""Room routes for the media pipeline, including the standalone Reader room."""
from __future__ import annotations

from html import escape
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from evolue.web.routers.auth import login_redirect

router = APIRouter(tags=["rooms"])
READER_FILE = Path(__file__).resolve().parents[2] / "ui" / "Reader-standalone (1).html"


def _reader_document() -> str:
    if not READER_FILE.exists():
        return "<!doctype html><html><body><p>Reader room is unavailable.</p></body></html>"
    return READER_FILE.read_text(encoding="utf-8")


@router.get("/reader", response_class=HTMLResponse)
def reader_room(request: Request):
    """Open the standalone Reader as a first-class authenticated room."""
    if login_redirect(request):
        return RedirectResponse("/login", status_code=303)
    return HTMLResponse(_reader_document())


@router.get("/book-room", response_class=HTMLResponse)
def book_room(request: Request):
    """Compatibility route for the Library's book-room action."""
    if login_redirect(request):
        return RedirectResponse("/login", status_code=303)
    return HTMLResponse(_reader_document())


@router.get("/api/reader/health")
def reader_health(request: Request):
    if login_redirect(request):
        return RedirectResponse("/login", status_code=303)
    return {"room": "reader", "status": "ready", "source": READER_FILE.name}


def reader_modal_markup() -> str:
    """Reusable Library modal that opens the Reader room, not a dead placeholder."""
    return """
<dialog id="book-room-modal" class="book-room-modal" aria-labelledby="book-room-title">
  <button class="close-x" type="button" data-close-book-room aria-label="Close">×</button>
  <p class="eyebrow">Library room</p>
  <h2 id="book-room-title">Open the Reader</h2>
  <p>Read a saved book or document in the standalone Reader room without leaving Evolue.</p>
  <a class="button" href="/reader">Open the Reader <span aria-hidden="true">→</span></a>
</dialog>
<script>
(() => {
  const dialog = document.getElementById('book-room-modal');
  document.querySelectorAll('[data-open-book-room]').forEach((trigger) => {
    trigger.addEventListener('click', () => dialog?.showModal());
  });
  dialog?.querySelector('[data-close-book-room]')?.addEventListener('click', () => dialog.close());
})();
</script>
"""
