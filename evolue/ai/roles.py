"""Role registry — maps each AI role to its provider, model, fallback chain, and output type.

Provider assignment (from the plan):
  DeepSeek:  creative_director, muse, creative_grader, cataloger, copywriter,
             video_generator, video_grader, video_proof_reviewer
  Groq:      current_events, fact_checker, brief_validator, production_grader,
             media_editor, copy_grader
  OpenRouter: fallback for all
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RoleConfig:
    role: str
    primary_provider: str
    primary_model: str
    fallback_providers: list[str] = field(default_factory=lambda: ["openrouter", "groq"])
    temperature: float = 0.7
    max_tokens: int = 8192
    output_type: str = "json"  # json | text


ROLE_REGISTRY: dict[str, RoleConfig] = {
    # ── DeepSeek-primary roles ──────────────────────────────────────────────
    "creative_director": RoleConfig(
        role="creative_director",
        primary_provider="deepseek",
        primary_model="deepseek-chat",
        temperature=0.7,
        max_tokens=16384,  # large: 9-post brief with timelines
    ),
    "muse": RoleConfig(
        role="muse",
        primary_provider="deepseek",
        primary_model="deepseek-chat",
        temperature=0.3,  # lower temp for retrieval/matching
        max_tokens=12288,
    ),
    "creative_grader": RoleConfig(
        role="creative_grader",
        primary_provider="deepseek",
        primary_model="deepseek-chat",
        temperature=0.4,
    ),
    "cataloger": RoleConfig(
        role="cataloger",
        primary_provider="deepseek",
        primary_model="deepseek-chat",
        temperature=0.2,  # very precise for metadata
    ),
    "copywriter": RoleConfig(
        role="copywriter",
        primary_provider="deepseek",
        primary_model="deepseek-chat",
        temperature=0.8,  # higher temp for creative writing
    ),
    "video_generator": RoleConfig(
        role="video_generator",
        primary_provider="deepseek",
        primary_model="deepseek-chat",
        temperature=0.5,
    ),
    "video_grader": RoleConfig(
        role="video_grader",
        primary_provider="deepseek",
        primary_model="deepseek-chat",
        temperature=0.3,
    ),
    "video_proof_reviewer": RoleConfig(
        role="video_proof_reviewer",
        primary_provider="deepseek",
        primary_model="deepseek-chat",
        temperature=0.3,
    ),
    # ── Groq-primary roles ──────────────────────────────────────────────────
    "current_events": RoleConfig(
        role="current_events",
        primary_provider="groq",
        primary_model="qwen/qwen3.8-27b",
        temperature=0.5,
    ),
    "fact_checker": RoleConfig(
        role="fact_checker",
        primary_provider="groq",
        primary_model="qwen/qwen3.8-27b",
        temperature=0.1,  # very conservative
    ),
    "brief_validator": RoleConfig(
        role="brief_validator",
        primary_provider="groq",
        primary_model="qwen/qwen3.8-27b",
        temperature=0.1,  # deterministic
    ),
    "production_grader": RoleConfig(
        role="production_grader",
        primary_provider="groq",
        primary_model="qwen/qwen3.8-27b",
        temperature=0.3,
    ),
    "media_editor": RoleConfig(
        role="media_editor",
        primary_provider="groq",
        primary_model="qwen/qwen3.8-27b",
        temperature=0.4,
    ),
    "copy_grader": RoleConfig(
        role="copy_grader",
        primary_provider="groq",
        primary_model="qwen/qwen3.8-27b",
        temperature=0.2,
    ),
}


def get_role_config(role: str) -> RoleConfig:
    if role not in ROLE_REGISTRY:
        raise ValueError(f"Unknown role '{role}'. Known: {sorted(ROLE_REGISTRY)}")
    return ROLE_REGISTRY[role]
