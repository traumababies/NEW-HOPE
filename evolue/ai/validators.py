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
    """Validate a Catalog Record. Returns list of errors."""
    errors: list[str] = []

    dc = record.dublin_core
    if not dc.dc_type:
        errors.append("dc_type is required (StillImage, MovingImage, Sound, Text)")
    if not dc.dc_format:
        errors.append("dc_format is required")
    if not dc.dc_subject:
        errors.append("dc_subject (IPTC code) is required")
    if dc.dc_subject and dc.dc_subject not in VALID_IPTC:
        errors.append(f"Invalid IPTC subject code: '{dc.dc_subject}'")

    # Date must come from filename, never guessed
    if dc.dc_date:
        import re
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", dc.dc_date):
            errors.append(f"dc_date must be ISO 8601 (YYYY-MM-DD), got '{dc.dc_date}'")

    return errors


def validate_copy(copy: CopySubmission) -> list[str]:
    """Validate a Copy Submission. Returns list of errors."""
    errors: list[str] = []

    if not copy.tiktok_caption.strip():
        errors.append("tiktok_caption is required")
    if not copy.instagram_caption.strip():
        errors.append("instagram_caption is required")

    tt_tags = [h for h in copy.tiktok_hashtags if h.tag.startswith("#")]
    ig_tags = [h for h in copy.instagram_hashtags if h.tag.startswith("#")]
    if len(tt_tags) != 5:
        errors.append(f"TikTok requires exactly 5 hashtags, got {len(tt_tags)}")
    if len(ig_tags) != 5:
        errors.append(f"Instagram requires exactly 5 hashtags, got {len(ig_tags)}")

    if not copy.alt_text.strip():
        errors.append("alt_text is required for accessibility")

    return errors


def validate_grader_scores(result, max_score: int) -> list[str]:
    """Validate grader score is within range."""
    errors: list[str] = []
    if result.total_score < 0 or result.total_score > max_score:
        errors.append(f"Score {result.total_score} out of range 0-{max_score}")
    return errors
