"""Direct Azure SQL access (pyodbc), strictly no SQLAlchemy.

All access goes through parameterized queries and small repository objects.
A connection string is built from config; in local/dev testing a caller may
supply any pyodbc-compatible DSN (e.g. a local SQL Server) but the production
boundary is Azure SQL (free-the-information-101010 / sanctuary-888).
"""
from __future__ import annotations

import os
import pyodbc

from evolue.config import settings


def build_connection_string() -> str:
    if settings.sql_conn_str:
        return settings.sql_conn_str
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
