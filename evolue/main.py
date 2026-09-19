"""FastAPI application factory and lifespan.

Runs migrations on startup (best-effort: no-op if the SQL driver/Azure isn't
configured yet). Web routers get registered here; the clean-architecture
boundaries are exercises via application services, not direct router->SQL.
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .config import settings


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

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return (
            "<h1>Évolué Media Team</h1>"
            "<p>Fresh build 2026-09-19 · running.</p>"
        )

    return app


app = create_app()
