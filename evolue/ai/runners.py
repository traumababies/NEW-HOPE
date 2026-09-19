"""Runners — end-to-end role execution.

Flow: load instructions → build prompt → call provider → parse JSON →
validate with Pydantic → validate with deterministic code → return typed result.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from .prompt_loader import (
    LoadedInstruction,
    build_role_prompt,
    load_role_instructions,
    operating_context_text,
)
from .providers import chat_with_fallback, get_provider
from .roles import RoleConfig, get_role_config
from .validators import (
    validate_brief,
    validate_catalog,
    validate_copy,
    validate_muse,
)

log = logging.getLogger(__name__)


# Map role names to their Pydantic output models
_MODEL_MAP: dict[str, type] = {}


def _register_models():
    from . import models
    _MODEL_MAP.update({
        "creative_director": models.CreativeBriefOutput,
        "current_events": models.CurrentEventsOutput,
        "fact_checker": models.FactCheckOutput,
        "muse": models.MuseProposal,
        "brief_validator": models.BriefValidationResult,
        "creative_grader": models.CreativeGradeResult,
        "production_grader": models.ProductionGradeResult,
        "cataloger": models.CatalogRecord,
        "copywriter": models.CopySubmission,
        "copy_grader": models.CopyGradeResult,
        "video_generator": models.VideoShotContract,
        "video_proof_reviewer": models.VideoProofResult,
    })


_register_models()

# Map roles to their deterministic validators
_VALIDATOR_MAP = {
    "creative_director": validate_brief,
    "muse": validate_muse,
    "cataloger": validate_catalog,
    "copywriter": validate_copy,
}


def run_role(role, task, context="", *, extra_context="", max_retries=2):
    """Run an AI role end-to-end. Returns dict with result, validation_errors, etc."""
    config = get_role_config(role)
    instructions = load_role_instructions(role)
    full_context = context or operating_context_text()
    if extra_context:
        full_context += f"\n\n{extra_context}"

    model_cls = _MODEL_MAP.get(role)
    schema_hint = ""
    if model_cls:
        schema_hint = f"Return valid JSON matching this Pydantic schema:\n{json.dumps(model_cls.model_json_schema(), indent=2)}"

    prompt = build_role_prompt(role=role, instructions=instructions,
                               context=full_context, task=task, output_schema=schema_hint)
    messages = [{"role": "user", "content": prompt}]

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            provider_name, response_text = chat_with_fallback(
                messages,
                providers=[config.primary_provider] + config.fallback_providers,
                model_overrides={config.primary_provider: config.primary_model},
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            )
            if config.output_type == "json" and model_cls:
                cleaned = response_text.strip()
                if cleaned.startswith("```"):
                    lines = cleaned.split("\n")
                    lines = [l for l in lines if not l.strip().startswith("```")]
                    cleaned = "\n".join(lines)
                parsed = json.loads(cleaned)
                result = model_cls.model_validate(parsed)
            else:
                result = response_text

            det_errors = []
            if role in _VALIDATOR_MAP and model_cls:
                det_errors = _VALIDATOR_MAP[role](result)

            return {
                "role": role,
                "result": result.model_dump() if hasattr(result, "model_dump") else result,
                "validation_errors": det_errors,
                "provider_used": provider_name,
                "instruction_sha256": [i.sha256 for i in instructions],
                "attempt": attempt + 1,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as exc:
            log.warning("Role %s attempt %d failed: %s", role, attempt + 1, exc)
            last_error = exc

    raise RuntimeError(f"Role '{role}' failed after {max_retries + 1} attempts: {last_error}")


def run_role_text(role, task, context=""):
    """Run a role expecting plain text output (no JSON validation)."""
    config = get_role_config(role)
    instructions = load_role_instructions(role)
    full_context = context or operating_context_text()
    prompt = build_role_prompt(role=role, instructions=instructions,
                               context=full_context, task=task)
    messages = [{"role": "user", "content": prompt}]
    _, text = chat_with_fallback(
        messages,
        providers=[config.primary_provider] + config.fallback_providers,
        model_overrides={config.primary_provider: config.primary_model},
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    return text
