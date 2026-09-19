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
            core_identifier NVARCHAR(500) NOT NULL,
            uuid7           NVARCHAR(64) NULL,
            creation_year   INT NULL,
            week_number     INT NULL,
            iptc_code       NVARCHAR(3) NULL,
            theme           NVARCHAR(500) NULL,
            sequence_no     INT NULL,
            host            NVARCHAR(20) NULL,
            file_extension  NVARCHAR(20) NULL,
            current_state   NVARCHAR(40) NOT NULL DEFAULT 'STEP_0_ORIGINAL',
            active_blob_path NVARCHAR(1000) NULL,
            asset_version   NVARCHAR(20) NULL DEFAULT 'v1-0',
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
            date_created    DATETIME2 DEFAULT SYSDATETIME(),
            last_modified   DATETIME2 DEFAULT SYSDATETIME(),
            INDEX ix_asset_core (core_identifier),
            INDEX ix_asset_state (current_state),
            INDEX ix_asset_week (week_number)
        )
        """
    ),
    "002_catalog_queue.sql": lambda: execute(
        """
        CREATE TABLE catalog_queue (
            id          BIGINT IDENTITY(1,1) PRIMARY KEY,
            asset_id    BIGINT NOT NULL,
            iptc_code   NVARCHAR(3) NOT NULL,
            status      NVARCHAR(20) NOT NULL DEFAULT 'pending',  -- pending | reviewed
            reviewed_by NVARCHAR(200) NULL,
            reviewed_at DATETIME2 NULL,
            created_at  DATETIME2 DEFAULT SYSDATETIME()
        )
        """
    ),
    "003_jan_requests.sql": lambda: execute(
        """
        CREATE TABLE jan_requests (
            id          BIGINT IDENTITY(1,1) PRIMARY KEY,
            phase       NVARCHAR(40) NOT NULL,           -- creative_brief | muse | scout | catalog | media_editor | copywriter
            entity_type NVARCHAR(40) NULL,               -- week | post | asset | proposal
            entity_id   NVARCHAR(64) NULL,
            requested_by NVARCHAR(200) NULL,
            status      NVARCHAR(20) NOT NULL DEFAULT 'pending',  -- pending | approved | rejected | replaced | overridden
            decision_note NVARCHAR(MAX) NULL,
            requested_at DATETIME2 DEFAULT SYSDATETIME(),
            decided_at   DATETIME2 NULL
        )
        """
    ),
}
