"""Deterministic validators — enforce rules that code must own, not the AI.

Per the embedding doc §3: "The Markdown tells the AI what to do. Code makes it
happen." These validators run on every AI output before it's accepted.
"""
from __future__ import annotations

from .models import (
    BriefValidationResult,
    CatalogRecord,
    CopySubmission,
    CreativeBriefOutput,
    CreativeGradeResult,
    MuseProposal,
    ProductionGradeResult,
)

VALID_IPTC = {"CUL", "ART", "CIN", "CHM", "HLT", "PRD", "FIN", "LIF", "HUM"}


def validate_brief(brief: CreativeBriefOutput) -> list[str]:
    """Validate a Creative Brief. Returns list of errors (empty = valid)."""
    errors: list[str] = []

    if not brief.weekly_theme.strip():
        errors.append("weekly_theme is required")

    if len(brief.post_briefs) != 9:
        errors.append(f"Exactly 9 post_briefs required, got {len(brief.post_briefs)}")

    positions = [p.position for p in brief.post_briefs]
    if sorted(positions) != list(range(1, 10)):
        errors.append(f"Positions must be 1-9 exactly once, got {sorted(positions)}")

    for post in brief.post_briefs:
        if not post.working_title.strip():
            errors.append(f"Post {post.position}: working_title is required")
        if post.duration_seconds <= 0:
            errors.append(f"Post {post.position}: duration_seconds must be > 0")
        if post.subject_code and post.subject_code not in VALID_IPTC:
            errors.append(f"Post {post.position}: invalid IPTC code '{post.subject_code}'")

    # Timeline validation
    for post in brief.post_briefs:
        if post.timeline:
            intervals = sorted(post.timeline, key=lambda t: t.start_seconds)
            if intervals[0].start_seconds != 0.0:
                errors.append(f"Post {post.position}: timeline must start at 0.0")
            for i in range(1, len(intervals)):
                if intervals[i].start_seconds < intervals[i - 1].end_seconds:
                    errors.append(f"Post {post.position}: timeline overlap at {intervals[i].start_seconds}")

    return errors


def validate_muse(proposal: MuseProposal) -> list[str]:
    """Validate a Muse proposal. Returns list of errors."""
    errors: list[str] = []

    if len(proposal.positions) != 9:
        errors.append(f"Exactly 9 positions required, got {len(proposal.positions)}")

    positions = [p.position for p in proposal.positions]
    if len(set(positions)) != 9:
        errors.append(f"Positions must be unique, got {positions}")

    for pos in proposal.positions:
        has_pick = pos.selected_candidate_id is not None
        has_gap = pos.gap is not None
        if not has_pick and not has_gap:
            errors.append(f"Position {pos.position}: must have either a library pick or a gap")
        if has_pick and has_gap:
            errors.append(f"Position {pos.position}: cannot have both a pick AND a gap")
        if not pos.evidence.strip() and has_pick:
            errors.append(f"Position {pos.position}: evidence is required for selected candidate")

    return errors


def validate_catalog(record: CatalogRecord) -> list[str]:
    """Validate a Catalog Record per spec: ISO 8601, Dublin Core 15 fields,
    IPTC Subject Codes, Schema.org JSON, Open Graph."""
    errors: list[str] = []
    dc = record.dublin_core

    # dc:type required — map from file extension
    if not dc.dc_type:
        errors.append("dc_type is required (StillImage, MovingImage, Sound, Text, Dataset, Software, InteractiveResource)")
    if not dc.dc_format:
        errors.append("dc_format is required (image/jpeg, video/mp4, etc.)")

    # dc:subject must be a valid IPTC code (3 letters)
    if not dc.dc_subject:
        errors.append("dc_subject (IPTC code) is required")
    elif dc.dc_subject not in VALID_IPTC:
        # Extract just the code if it contains extra text
        code = dc.dc_subject.strip()[:3].upper()
        if code not in VALID_IPTC:
            errors.append(f"Invalid IPTC subject code: '{dc.dc_subject}' (expected one of {sorted(VALID_IPTC)})")

    # dc:date must be ISO 8601 (YYYY-MM-DD) from FILENAME only
    if dc.dc_date:
        import re
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", dc.dc_date):
            errors.append(f"dc_date must be ISO 8601 YYYY-MM-DD, got '{dc.dc_date}'")

    # dc:language must be ISO 639-3 (default: eng)
    if dc.dc_language and dc.dc_language != "eng":
        import re
        if not re.match(r"^[a-z]{3}$", dc.dc_language):
            errors.append(f"dc_language must be ISO 639-3 (3-letter), got '{dc.dc_language}'")

    # dc:creator default
    if dc.dc_creator and dc.dc_creator != "Evolue Media Team":
        pass  # Allow custom creators but flag for review

    # dc:publisher default
    if dc.dc_publisher and dc.dc_publisher != "Evolue Skincare Inc":
        pass  # Allow custom publishers but flag for review

    # dc:rights default check
    if dc.dc_rights and "Evolue Skincare Inc" not in dc.dc_rights:
        errors.append("dc_rights must reference 'Evolue Skincare Inc'")

    # Schema.org type must match dc:type
    if record.schema_org_type:
        type_map = {
            "StillImage": "ImageObject", "MovingImage": "VideoObject",
            "Sound": "AudioObject", "Text": "DigitalDocument",
            "Dataset": "Dataset", "Software": "SoftwareApplication",
            "InteractiveResource": "MediaObject",
        }
        expected = type_map.get(dc.dc_type, "")
        if expected and record.schema_org_type != expected:
            errors.append(f"schema_org_type '{record.schema_org_type}' doesn't match dc:type '{dc.dc_type}' (expected '{expected}')")

    # OG fields check — og:title must exist if asset is publishable
    if record.og_title and not record.og_title.strip():
        errors.append("og_title cannot be empty if set")

    return errors


def validate_copy(copy: CopySubmission) -> list[str]:
    """Validate a Copy Submission. Returns list of errors."""
    errors: list[str] = []

    if not copy.tiktok_caption.strip():
        errors.append("tiktok_caption is required")
    if not copy.instagram_caption.strip():
        errors.append("instagram_caption is required")

    # Accept hashtags with or without # prefix — normalize for counting
    tt_tags = [h for h in copy.tiktok_hashtags if h.tag.strip()]
    ig_tags = [h for h in copy.instagram_hashtags if h.tag.strip()]
    if len(tt_tags) != 5:
        errors.append(f"TikTok requires exactly 5 hashtags, got {len(tt_tags)}")
    if len(ig_tags) != 5:
        errors.append(f"Instagram requires exactly 5 hashtags, got {len(ig_tags)}")

    # Ensure hashtags start with #
    for h in copy.tiktok_hashtags + copy.instagram_hashtags:
        if h.tag.strip() and not h.tag.strip().startswith("#"):
            errors.append(f"Hashtag '{h.tag}' must start with #")

    if not copy.alt_text.strip():
        errors.append("alt_text is required for accessibility")

    return errors


def validate_grader_scores(result, max_score: int) -> list[str]:
    """Validate grader score is within range."""
    errors: list[str] = []
    if result.total_score < 0 or result.total_score > max_score:
        errors.append(f"Score {result.total_score} out of range 0-{max_score}")
    return errors
