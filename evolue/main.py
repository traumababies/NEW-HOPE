"""FastAPI application factory and lifespan.

Runs migrations on startup (best-effort: no-op if the SQL driver/Azure isn't
configured yet). Web routers get registered here; the clean-architecture
boundaries are exercises via application services, not direct router->SQL.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from .config import settings

STATIC_DIR = Path(__file__).resolve().parent / "static"


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Migrations run only when the SQL layer is actually configured.
        if settings.sql_server or settings.sql_conn_str:
            try:
                from .infrastructure.sql.migrations import run_migrations

                run_migrations()
            except Exception:  # pragma: no cover - boot must not crash on absent Azure
                pass
        yield

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/")
    def index():
        # Session check: naive for now — the auth router owns real enforcement.
        return RedirectResponse("/calendar", status_code=307)

    def register_router(mod_path: str):
        import importlib

        mod = importlib.import_module(mod_path)
        if hasattr(mod, "router"):
            app.include_router(mod.router)

    register_router("evolue.web.routers.auth")

    return app


app = create_app()

