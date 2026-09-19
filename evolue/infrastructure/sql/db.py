"""Direct Azure SQL access (pyodbc), strictly no SQLAlchemy.

All access goes through parameterized queries and small repository objects.
A connection string is built from config; in local/dev testing a caller may
supply any pyodbc-compatible DSN (e.g. a local SQL Server) but the production
boundary is Azure SQL (free-the-information-101010 / sanctuary-888).
"""
from __future__ import annotations

import os
import re
import urllib.parse

import pyodbc

from evolue.config import settings


_URL_RE = re.compile(
    r"^[a-z0-9+]+://([^:]+):([^@]+)@([^/:]+)(?::(\d+))?/([^?]+)(?:\?.*)?$"
)


def connection_string_from_url(url: str) -> str:
    """Translate our DATABASE_URL (mssql+pyodbc://user:pwd@host:1433/db?...) into
    an ODBC connection string. Never logs the password."""
    m = _URL_RE.match(url)
    if not m:
        raise ValueError("DATABASE_URL is not in mssql+pyodbc://user:pass@host:1433/db form")
    user_enc, pwd_enc, host, port, db = m.groups()[0], m.groups()[1], m.groups()[2], m.groups()[3] or "1433", m.groups()[4]
    user = urllib.parse.unquote(user_enc)
    pwd = urllib.parse.unquote(pwd_enc)
    return (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={host},{port};"
        f"DATABASE={db};"
        f"UID={user};"
        f"PWD={pwd};"
        "Encrypt=yes;TrustServerCertificate=no;"
    )


def build_connection_string() -> str:
    if settings.sql_conn_str:
        return settings.sql_conn_str
    if settings.database_url:
        return connection_string_from_url(settings.database_url)
    return (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={settings.sql_server};"
        f"DATABASE={settings.sql_database};"
        f"UID={settings.sql_username};"
        f"PWD={settings.sql_password};"
        "Encrypt=yes;TrustServerCertificate=no;"
    )


def connect() -> pyodbc.Connection:
    return pyodbc.connect(build_connection_string(), timeout=10)


def execute(sql: str, params: tuple = ()) -> None:
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
    finally:
        conn.close()


def fetch_all(sql: str, params: tuple = ()) -> list[dict]:
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        columns = [c[0] for c in cur.description or ()]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
    finally:
        conn.close()
