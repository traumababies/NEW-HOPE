"""Pydantic output contracts for every AI role.

Each model defines the structured output the AI must return.
The application validates responses against these schemas before accepting them.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


# ── Creative Director output (Steps 2-3) ────────────────────────────────────

class SearchPacket(BaseModel):
    primary_query: str = ""
    alternate_queries: list[str] = Field(default_factory=list)
    required_objects: list[str] = Field(default_factory=list)
    required_actions: list[str] = Field(default_factory=list)
    required_setting: str = ""
    required_color_lighting: str = ""
    required_framing: str = ""
    min_duration_seconds: float = 0
    orientation: str = ""  # vertical | square | horizontal
    aspect_ratio: str = ""
    licensing_requirement: str = ""
    negative_terms: list[str] = Field(default_factory=list)
    acceptable_substitutes: list[str] = Field(default_factory=list)
    unacceptable_substitutes: list[str] = Field(default_factory=list)


class TimelineInterval(BaseModel):
    start_seconds: float
    end_seconds: float
    observable_action: str
    camera: str = ""
    lighting: str = ""
    transition: str = ""
    audio: str = ""


class PostBrief(BaseModel):
    position: int = Field(ge=1, le=9)
    working_title: str
    narrative_role: str = ""
    subject_code: str = ""  # IPTC code
    subject_angle: str = ""
    theme_connection: str = ""
    is_hero: bool = False
    duration_seconds: float = 0
    hook_description: str = ""
    timeline: list[TimelineInterval] = Field(default_factory=list)
    search_packet: SearchPacket = Field(default_factory=SearchPacket)
    media_editor_instructions: str = ""
    acceptance_criteria: list[str] = Field(default_factory=list)
    rejection_criteria: list[str] = Field(default_factory=list)
    fallback_plan: str = ""
    production_risk: str = ""  # low | medium | high | critical


class WeekGroup(BaseModel):
    day: str  # monday | wednesday | friday
    positions: list[int]


class CreativeBriefOutput(BaseModel):
    weekly_theme: str
    theme_meaning: str = ""
    central_question: str = ""
    creative_bible: str = ""
    nine_post_narrative: str = ""
    hero_position: int = 0
    week_groups: list[WeekGroup] = Field(default_factory=list)
    post_briefs: list[PostBrief] = Field(default_factory=list, max_length=9, min_length=9)
    music_direction: str = ""
    visual_continuity_rules: str = ""
    platform_rules: str = ""
    fact_check_queue: list[str] = Field(default_factory=list)
    rights_review_queue: list[str] = Field(default_factory=list)
    owner_review_questions: list[str] = Field(default_factory=list)
    self_check_passed: bool = False
    status: str = "ready_for_grading"


# ── Current Events output (Step 2) ──────────────────────────────────────────

class ClaimCandidate(BaseModel):
    claim_id: str = ""
    subject_code: str
    claim: str
    why_relevant: str = ""
    source_url: str  # REQUIRED
    source_name: str = ""
    source_type: str = ""
    source_tier: str = ""
    source_published_at: str = ""
    event_date: str = ""
    as_of_date: str = ""
    geographic_scope: str = ""
    claim_type: str = ""  # evergreen | current_context | current_claim | trend_reference
    evidence_excerpt: str = ""
    confidence: float = Field(ge=0, le=1)
    developing_story: bool = False
    risks: list[str] = Field(default_factory=list)
    suggested_wording: str = ""


class CurrentEventsOutput(BaseModel):
    claims: list[ClaimCandidate] = Field(default_factory=list)
    freshness_window: str = ""
    total_claims: int = 0


# ── Fact Checker output (Step 2) ────────────────────────────────────────────

class ClaimVerdict(BaseModel):
    claim: str
    verdict: str  # verified | partially_verified | unverified | contradicted | out_of_date | misleading | cannot_verify
    evidence_urls: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    note: str = ""
    safe_wording: str = ""
    valid_until: str = ""
    refresh_required: bool = False


class FactCheckOutput(BaseModel):
    verdicts: list[ClaimVerdict] = Field(default_factory=list)
    all_verified: bool = False


# ── Muse output (Steps 5-6) ─────────────────────────────────────────────────

class ContentScoutRequest(BaseModel):
    scout_number: str = ""
    assignment_name: str = ""
    search_terms: list[str] = Field(default_factory=list)
    media_type: str = ""  # image | video
    platform_hint: str = ""
    orientation: str = ""
    aspect_ratio: str = ""
    min_duration: float = 0


class MusePosition(BaseModel):
    position: int = Field(ge=1, le=9)
    subject_code: str
    selected_candidate_id: str | None = None
    candidate_ids: list[str] = Field(default_factory=list)
    match_score: float = 0
    confidence: float = Field(ge=0, le=1)
    evidence: str = ""
    platform_fit: str = ""
    content_angle: str = ""
    theme_connection: str = ""
    duplicate_warnings: list[str] = Field(default_factory=list)
    gap: ContentScoutRequest | None = None  # populated when no library match


class MuseProposal(BaseModel):
    week_id: str
    weekly_theme: str
    brief_revision: int = 1
    positions: list[MusePosition] = Field(default_factory=list, min_length=9, max_length=9)
    theme_image_candidate: str | None = None
    theme_image_evidence: str = ""
    review_notes: str = ""
    revision: int = 1


# ── Brief Validator output (Step 3) ─────────────────────────────────────────

class BriefValidationResult(BaseModel):
    verdict: str  # pass | pass_with_warnings | blocked
    structural_score: int = Field(ge=0, le=100)
    critical_errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    required_corrections: list[str] = Field(default_factory=list)
    generation_authorization: str = "not_authorized"


# ── Creative Grader output (Step 3) ─────────────────────────────────────────

class SectionScore(BaseModel):
    section_name: str
    score: int = Field(ge=0, le=5)
    max_score: int = 5
    evidence: str = ""


class CreativeGradeResult(BaseModel):
    total_score: int = Field(ge=0, le=100)
    verdict: str  # excellent | strong | revision_required | rejected
    section_scores: list[SectionScore] = Field(default_factory=list)
    best_elements: str = ""
    weakest_elements: str = ""
    posts_requiring_revision: list[int] = Field(default_factory=list)
    required_revisions: list[str] = Field(default_factory=list)


# ── Production Grader output (Step 3) ───────────────────────────────────────

class PostRisk(BaseModel):
    position: int
    risk_level: str  # low | medium | high | critical
    main_risk: str = ""
    fallback_exists: bool = False


class ProductionGradeResult(BaseModel):
    total_score: int = Field(ge=0, le=75)
    verdict: str  # ready | proof_only | owner_review_required | blocked
    section_scores: list[SectionScore] = Field(default_factory=list)
    post_risks: list[PostRisk] = Field(default_factory=list)
    estimated_credit_risk: str = ""
    most_dangerous_assumptions: str = ""
    missing_fallbacks: str = ""
    rights_concerns: str = ""
    required_corrections: list[str] = Field(default_factory=list)


# ── Cataloger output (Step 10) ───────────────────────────────────────────────

class DublinCoreFields(BaseModel):
    dc_title: str = ""
    dc_creator: str = "Evolue Media Team"
    dc_subject: str = ""
    dc_description: str = ""
    dc_publisher: str = "Evolue Skincare Inc"
    dc_contributor: str = ""
    dc_date: str = ""  # ISO 8601, from filename only
    dc_type: str = ""  # StillImage | MovingImage | Sound | Text
    dc_format: str = ""  # image/jpeg, video/mp4, etc.
    dc_identifier: str = ""
    dc_source: str = ""
    dc_language: str = "eng"
    dc_relations: str = ""
    dc_coverage: str = "Global"
    dc_rights: str = ""


class CatalogRecord(BaseModel):
    asset_id: str = ""
    media_kind: str = ""  # image | video | audio | document
    original_filename: str = ""
    storage_key: str = ""
    file_size_bytes: int = 0
    mime_type: str = ""
    width: int = 0
    height: int = 0
    duration_seconds: float = 0
    orientation: str = ""
    checksum: str = ""
    dublin_core: DublinCoreFields = Field(default_factory=DublinCoreFields)
    schema_org_type: str = ""  # ImageObject | VideoObject | AudioObject
    schema_org_json: dict = Field(default_factory=dict)
    og_title: str = ""
    og_description: str = ""
    og_type: str = ""
    og_image_url: str = ""
    visual_description: str = ""
    derived_keywords: list[str] = Field(default_factory=list)
    iptc_subject_code: str = ""
    evidence_summary: str = ""
    confidence_values: dict = Field(default_factory=dict)
    uncertainty_notes: list[str] = Field(default_factory=list)
    fact_check_queue: list[str] = Field(default_factory=list)
    owner_review_queue: list[str] = Field(default_factory=list)
    catalog_status: str = "ready_for_review"


# ── Copywriter output (Steps 14-15) ─────────────────────────────────────────

class HashtagEntry(BaseModel):
    tag: str
    category: str = ""  # subject | niche | theme | brand | location
    reason: str = ""
    platform: str = ""  # tiktok | instagram | both


class CopySubmission(BaseModel):
    post_position: int = Field(ge=1, le=9)
    media_evidence_summary: str = ""
    tiktok_caption: str = ""
    tiktok_cta: str = ""
    tiktok_hashtags: list[HashtagEntry] = Field(default_factory=list)
    instagram_caption: str = ""
    instagram_cta: str = ""
    instagram_hashtags: list[HashtagEntry] = Field(default_factory=list)
    alt_text: str = ""
    attribution: str = ""
    disclosure: str = ""
    disclosure_type: str = ""  # none | affiliate | paid_partnership | gifted | sponsored
    fact_check_queue: list[str] = Field(default_factory=list)
    tone_assessment: str = ""
    uncertainty_notes: list[str] = Field(default_factory=list)
    status: str = "ready_for_copy_grading"


# ── Copy Grader output (Step 15) ────────────────────────────────────────────

class CopyGradeResult(BaseModel):
    total_score: int = Field(ge=0, le=100)
    status: str  # pass | pass_with_warnings | return_to_copywriter | fact_check_required | rights_review_required | blocked
    section_scores: list[SectionScore] = Field(default_factory=list)
    auto_failure_flags: list[str] = Field(default_factory=list)
    best_copy_element: str = ""
    weakest_copy_element: str = ""
    required_corrections: list[str] = Field(default_factory=list)
    critical_failure_details: str = ""


# ── Video Generator output ──────────────────────────────────────────────────

class VideoShotContract(BaseModel):
    post_position: int
    shot_number: int
    one_observable_job: str = ""
    proof_duration_seconds: float = 0
    final_duration_seconds: float = 0
    aspect_ratio: str = ""
    resolution: str = ""
    orientation: str = ""
    required_subject: str = ""
    required_action: str = ""
    starting_state: str = ""
    ending_state: str = ""
    camera_movement: str = ""
    palette: str = ""
    lighting: str = ""
    prompt: str = ""
    negative_prompt: str = ""
    acceptance_criteria: list[str] = Field(default_factory=list)
    fallback_plan: str = ""
    estimated_credit_cost: str = ""
    generation_tier: int = Field(ge=1, le=4)  # 1=existing, 2=edit, 3=low-risk, 4=high-risk


class VideoProofResult(BaseModel):
    shot_position: int
    shot_number: int
    attempt_number: int
    verdict: str  # pass | pass_with_warnings | fail
    brief_compliance_score: int = 0
    visual_quality_score: int = 0
    action_quality_score: int = 0
    platform_score: int = 0
    continuity_score: int = 0
    total_score: int = 0
    critical_failures: list[str] = Field(default_factory=list)
    evidence_timestamps: str = ""
    one_required_correction: str = ""




