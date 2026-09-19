"""Library repository — direct SQL, no ORM.

Wraps asset_index plus the review/catalog queues. All queries parameterized.
"""
from __future__ import annotations

from ..infrastructure.sql.db import execute, fetch_all


class LibraryRepo:
    def create_catalog_entry(
        self,
        *,
        core_identifier: str,
        creation_year: int,
        week_number: int,
        iptc_code: str,
        theme: str,
        sequence_no: int,
        host: str,
        file_extension: str,
        dc_fields: dict | None = None,
    ) -> dict:
        fields = dc_fields or {}
        sql = """
            INSERT INTO asset_index (
                core_identifier, creation_year, week_number, iptc_code, theme,
                sequence_no, host, file_extension, current_state, asset_version,
                dc_title, dc_creator, dc_subject, dc_description, dc_publisher,
                dc_contributor, dc_date, dc_type, dc_format, dc_identifier,
                dc_source, dc_language, dc_relations, dc_coverage, dc_rights
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        execute(
            sql,
            (
                core_identifier,
                creation_year,
                week_number,
                iptc_code,
                theme,
                sequence_no,
                host,
                file_extension,
                "STEP_0_ORIGINAL",
                "v1-0",
                fields.get("dc_title", ""),
                fields.get("dc_creator", "Evolue Media Team"),
                fields.get("dc_subject", iptc_code),
                fields.get("dc_description", ""),
                fields.get("dc_publisher", "Evolue Skincare Inc"),
                fields.get("dc_contributor", ""),
                fields.get("dc_date", ""),
                fields.get("dc_type", ""),
                fields.get("dc_format", ""),
                fields.get("dc_identifier", ""),
                fields.get("dc_source", ""),
                fields.get("dc_language", "eng"),
                fields.get("dc_relations", ""),
                fields.get("dc_coverage", "Global"),
                fields.get(
                    "dc_rights",
                    "© 2026 Evolue Skincare Inc. All rights reserved for new creative additions. "
                    "Pre-existing image elements are utilized under the standard content license "
                    "provided by dc:resource.",
                ),
            ),
        )
        row = self.by_core_identifier(core_identifier)
        return row

    def by_core_identifier(self, core_identifier: str) -> dict | None:
        rows = fetch_all(
            "SELECT * FROM asset_index WHERE core_identifier = ?", (core_identifier,)
        )
        return rows[0] if rows else None

    def update_state(self, core_identifier: str, state: str, blob_path: str | None = None) -> None:
        execute(
            "UPDATE asset_index SET current_state = ?, active_blob_path = COALESCE(?, active_blob_path), last_modified = SYSDATETIME() WHERE core_identifier = ?",
            (state, blob_path, core_identifier),
        )

    def set_uuid_v7(self, core_identifier: str, uuid7: str) -> None:
        execute(
            "UPDATE asset_index SET uuid7 = ?, current_state = 'PIPELINE_COMPLETE_APPROVED', last_modified = SYSDATETIME() WHERE core_identifier = ?",
            (uuid7, core_identifier),
        )

    def queue_catalog(self, asset_id: int, iptc_code: str) -> None:
        execute(
            "INSERT INTO catalog_queue (asset_id, iptc_code, status) VALUES (?, ?, ?)",
            (asset_id, iptc_code, "pending"),
        )
