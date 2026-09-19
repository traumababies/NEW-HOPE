"""Owner authentication.

Jean logs in with the email/password from .env (OWNER_EMAIL / OWNER_PASSWORD).
Sessions are signed cookies via the session secret. No DB required; the owner
gate is the app's admin boundary (The Library.txt A.16).
"""
from __future__ import annotations

import hmac
import secrets
import time
from dataclasses import dataclass, field

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from evolue.config import settings

router = APIRouter(tags=["auth"])

SESSION_HOURS = 24 * 7


def login_redirect(request: Request) -> str | None:
    """Return a redirect to /login if the session is absent/invalid."""
    token = request.cookies.get("evolue_session")
    if token and _verify_token(token):
        return None
    return "/login"


def _sign(payload: str) -> str:
    return hmac.new(settings.session_secret.encode(), payload.encode(), "sha256").hexdigest()


def _verify_token(token: str) -> bool:
    try:
        payload, sig = token.rsplit(".", 1)
    except ValueError:
        return False
    if not hmac.compare_digest(sig, _sign(payload)):
        return False
    parts = payload.split(":", 2)
    if len(parts) != 3:
        return False
    email, issued, expiry = parts
    if int(expiry) < time.time():
        return False
    return email == settings.admin_email


def make_session_token(email: str) -> str:
    now = int(time.time())
    payload = f"{email}:{now}:{now + SESSION_HOURS * 3600}"
    return f"{payload}.{_sign(payload)}"


def require_owner(request: Request):
    """FastAPI dependency: returns True or raises redirect to login."""
    from fastapi.responses import RedirectResponse

    if _verify_token(request.cookies.get("evolue_session", "")):
        return True
    return RedirectResponse("/login", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    from evolue.main import templates
    brand = {"company_name": "Évolué", "logo_url": "/static/brand/logo.svg"}
    return templates.TemplateResponse("Login.dc.html", {
        "request": request, "brand": brand, "msg": "",
    })


@router.post("/login")
def login_post(
    email: str = Form(...),
    password: str = Form(...),
):
    if settings.admin_email and settings.owner_password:
        ok_email = email.strip().lower() == settings.admin_email.lower()
        ok_pass = hmac.compare_digest(password, settings.owner_password)
        if ok_email and ok_pass:
            response = RedirectResponse("/", status_code=303)
            response.set_cookie(
                "evolue_session",
                make_session_token(settings.admin_email),
                httponly=True,
                samesite="lax",
                max_age=SESSION_HOURS * 3600,
            )
            return response
    return RedirectResponse("/login?error=1", status_code=303)


@router.post("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("evolue_session")
    return response
