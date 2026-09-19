"""Naming law — THE single authority for every Évolué filename.

Applies The Library.txt F.1–F.7 and G.8.a.ii:

    theme (calendar/week):  YYYY_W##_THEME
    brief title:            YYYY_W##_THEME_HOST
    tile label:             IPTC-Subject-Code_Sequence##        (top-right corner)
    scout assignment:       YYYY_W##_IPTC-Subject-Code_SEQUENCE
    original (via uuid):    YYYY_W##_IPTC-Subject-Code_SEQUENCE_dcterms:hasVersion_Version_uuid
    derivative (via uuid):  YYYY_W##_IPTC-Subject-Code_SEQUENCE_dcterms:isVersionof_Version_uuid
    final created            YYYY_W##_IPTC-Subject-Code_THEME_Sequence_HOST.ext
    final derivative         YYYY_W##_IPTC-Subject-Code_THEME_Sequence_HOST_dc:identifier_dcterms:isVersionof_uuidv7().ext
    standalone (Jean):      YYYY_IPTC-Subject-Code.File-Format
"""
from __future__ import annotations

__all__ = [
    "theme_name",
    "brief_title",
    "tile_label",
    "scout_assignment_name",
    "original_uuid_name",
    "derivative_uuid_name",
    "final_created_name",
    "final_derivative_name",
    "standalone_name",
]

SEQUENCE_SEPARATOR = "_"


def _z2(value: int) -> str:
    return f"{value:02d}"


def theme_name(year: int, week_number: int, theme: str) -> str:
    """YYYY_W##_THEME (F.1)."""
    return f"{year}_W{_z2(week_number)}_{theme}"


def brief_title(year: int, week_number: int, theme_host: str) -> str:
    """YYYY_W##_THEME_HOST (F.2 / D.4.i)."""
    return f"{year}_W{_z2(week_number)}_{theme_host}"


def tile_label(iptc_code: str, sequence: int) -> str:
    """IPTC-Subject-Code_Sequence## (F.3 / top-right corner).

    Theme-image tiles have no subject code and use TI01..TI09 instead (A.10.iii).
    """
    code = (iptc_code or "TI").strip().upper()
    return f"{code}_{_z2(sequence)}" if code != "TI" else f"TI{_z2(sequence)}"


def scout_assignment_name(year: int, week_number: int, iptc_code: str, sequence: int) -> str:
    """YYYY_W##_IPTC-Subject-Code_SEQUENCE (F.4 / Scout)."""
    return f"{year}_W{_z2(week_number)}_{iptc_code}_{_z2(sequence)}"


def original_uuid_name(
    year: int, week_number: int, iptc_code: str, sequence: int, uuid7: str
) -> str:
    """YYYY_W##_IPTC-Subject-Code_SEQUENCE_dcterms:hasVersion_Version_uuid (F.6)."""
    return f"{year}_W{_z2(week_number)}_{iptc_code}_{_z2(sequence)}_dcterms:hasVersion_v1-0_{uuid7}"


def derivative_uuid_name(
    year: int, week_number: int, iptc_code: str, sequence: int, uuid7: str, version: str = "v1-0"
) -> str:
    """YYYY_W##_IPTC-Subject-Code_SEQUENCE_dcterms:isVersionof_Version_uuid (F.6)."""
    return f"{year}_W{_z2(week_number)}_{iptc_code}_{_z2(sequence)}_dcterms:isVersionof_{version}_{uuid7}"


def final_created_name(
    year: int, week_number: int, iptc_code: str, theme: str, sequence: int, host: str, ext: str
) -> str:
    """YYYY_W##_IPTC-Subject-Code_THEME_Sequence_HOST.ext (F.7)."""
    return f"{year}_W{_z2(week_number)}_{iptc_code}_{theme}_{sequence}_{host}.{ext.lstrip('.')}"


def final_derivative_name(
    year: int, week_number: int, iptc_code: str, theme: str, sequence: int, host: str, ext: str, uuid7: str
) -> str:
    """YYYY_W##_IPTC-Subject-Code_THEME_Sequence_HOST_dc:identifier_dcterms:isVersionof_uuidv7().ext (step 12)."""
    return (
        f"{year}_W{_z2(week_number)}_{iptc_code}_{theme}_{sequence}_{host}"
        f"_dc:identifier_dcterms:isVersionof_{uuid7}.{ext.lstrip('.')}"
    )


def standalone_name(year: int, iptc_code: str, fmt: str) -> str:
    """YYYY_IPTC-Subject-Code.File-Format (Jean's Creations)."""
    return f"{year}_{iptc_code}.{fmt.lstrip('.')}"
