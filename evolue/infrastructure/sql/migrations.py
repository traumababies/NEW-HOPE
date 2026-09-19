"""Database migrations (direct SQL, no ORM).

Each migration is a plain SQL file under this folder with a numeric prefix.
A tiny runner tracks applied migrations in a `schema_migrations` table.
"""

from __future__ import annotations

from .db import execute, fetch_all


def run_migrations() -> None:
    execute(
        "IF OBJECT_ID('schema_migrations') IS NULL "
        "CREATE TABLE schema_migrations (filename NVARCHAR(255) PRIMARY KEY, applied_at DATETIME2 DEFAULT SYSDATETIME())"
    )
    applied = {row["filename"] for row in fetch_all("SELECT filename FROM schema_migrations")}
    # Ordered by filename so prefixes 001, 002, ... run in order.
    for filename in sorted(_MIGRATIONS):
        if filename in applied:
            continue
        _MIGRATIONS[filename]()
        execute("INSERT INTO schema_migrations (filename) VALUES (?)", (filename,))


_MIGRATIONS: dict[str, callable] = {
    "001_asset_index.sql": lambda: execute(
        """
        CREATE TABLE asset_index (
            id              BIGINT IDENTITY(1,1) PRIMARY KEY,
            -- Core identifier until Studio COMMIT, then UUID-bearing (spec G.8.a.i)
            core_identifier NVARCHAR(500) NOT NULL,          -- YYYY_W##_IPTC-Subject-Codes-Sequence
            uuid7           NVARCHAR(64) NULL,               -- injected by UPDATE at Studio COMMIT
            creation_year   INT NULL,
            week_number     INT NULL,
            iptc_code       NVARCHAR(3) NULL,
            theme           NVARCHAR(500) NULL,
            sequence_no     INT NULL,
            host            NVARCHAR(20) NULL,               -- ig / tt / ig-tt
            file_extension  NVARCHAR(20) NULL,
            -- State machine (spec G.8.a.iii)
            current_state   NVARCHAR(40) NOT NULL DEFAULT 'STEP_0_ORIGINAL',
            active_blob_path NVARCHAR(1000) NULL,
            asset_version   NVARCHAR(20) NULL DEFAULT 'v1-0',
            -- Dublin Core
            dc_title        NVARCHAR(500) NULL,
            dc_creator      NVARCHAR(200) NULL,
            dc_subject      NVARCHAR(3) NULL,
            dc_description  NVARCHAR(MAX) NULL,
            dc_publisher    NVARCHAR(200) NULL,
            dc_contributor  NVARCHAR(500) NULL,
            dc_date         NVARCHAR(20) NULL,
            dc_type         NVARCHAR(20) NULL,
            dc_format       NVARCHAR(50) NULL,
            dc_identifier   NVARCHAR(500) NULL,
            dc_source       NVARCHAR(500) NULL,
            dc_language     NVARCHAR(10) NULL DEFAULT 'eng',
            dc_relations    NVARCHAR(500) NULL,
            dc_coverage     NVARCHAR(50) NULL DEFAULT 'Global',
            dc_rights       NVARCHAR(1000) NULL,
            -- DM Tookit
            date_created    DATETIME2 DEFAULT SYSDATETIME(),
            last_modified   DATETIME2 DEFAULT SYSDATETIME(),
            INDEX ix_asset_core (core_identifier),
            INDEX ix_asset_state (current_state),
            INDEX ix_asset_week (id, week_number)
        )
        """
    ),
}
