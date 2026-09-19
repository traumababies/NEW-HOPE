"""Prompt loader — loads .md role instructions, hashes them, assembles prompts.

Per EMBEDDING-MARKDOWN-INSTRUCTIONS-INTO-AIS.md:
- Allowlisted filenames only (never load arbitrary paths)
- UTF-8 read, strip, SHA-256 hash for version tracking
- Role-specific prompt assembly with delimiter-separated sections
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_AI_TEAM_DIR = _REPO_ROOT / "AI TEAM"
_AI_EMBED_DIR = _AI_TEAM_DIR / "AI Embed Directions"

ROLE_INSTRUCTION_FILES: dict[str, tuple[str, str]] = {
    "creative_director": ("Creative Brief Grading Charts", "CREATIVE-DIRECTOR-DETAILED-INSTRUCTIONS.md"),
    "current_events": ("Social Media Marketing", "CURRENT-EVENTS-AND-FACT-CHECK-WORKFLOW.md"),
    "fact_checker": ("Social Media Marketing", "CURRENT-EVENTS-AND-FACT-CHECK-WORKFLOW.md"),
    "muse": ("", "MUSE-DETAILED-OPERATING-INSTRUCTIONS.md"),
    "brief_validator": ("Creative Brief Grading Charts", "BRIEF-VALIDATOR-REVIEW-SHEET.md"),
    "creative_grader": ("Creative Brief Grading Charts", "CREATIVE-GRADER-REVIEW-SHEET.md"),
    "production_grader": ("Creative Brief Grading Charts", "PRODUCTION-GRADER-REVIEW-SHEET.md"),
    "cataloger": ("Cataloging Detailed Instructions", "CATALOGER-DETAILED-OPERATING-INSTRUCTIONS.md"),
    "copywriter": ("Social Media Marketing", "COPYWRITER-DETAILED-OPERATING-INSTRUCTIONS.md"),
    "copy_grader": ("Social Media Marketing", "COPY-GRADING-RUBRIC.md"),
    "video_generator": ("Social Media Marketing", "AI-VIDEO-GENERATOR-DETAILED-INSTRUCTIONS-WORKSHEET.md"),
    "video_grader": ("Social Media Marketing", "AI-VIDEO-GENERATION-GRADER-REVIEW-SHEET.md"),
    "video_proof_reviewer": ("Social Media Marketing", "AI-VIDEO-PROOF-AND-CREDIT-REVIEW-SHEET.md"),
}

ROLE_SUPPLEMENTARY: dict[str, list[tuple[str, str]]] = {
    "creative_director": [
        ("Creative Brief Grading Charts", "WEEKLY-CREATIVE-BRIEF-TEMPLATE.md"),
        ("Creative Brief Grading Charts", "WORKED-EXAMPLE-WEEKLY-CREATIVE-BRIEF.md"),
    ],
    "muse": [("", "OPERATING-CONTEXT.md")],
    "cataloger": [
        ("Cataloging Detailed Instructions/CATALOGING", "SCHEMA-ORG-JSON-LD-CATALOG-STANDARD.md"),
    ],
}


@dataclass(frozen=True)
class LoadedInstruction:
    filename: str
    text: str
    sha256: str


def _resolve_path(dir_hint: str, filename: str) -> Path:
    if dir_hint:
        candidate = _AI_EMBED_DIR / dir_hint / filename
        if candidate.exists():
            return candidate
    candidate = _AI_TEAM_DIR / filename
    if candidate.exists():
        return candidate
    candidate = _AI_EMBED_DIR / filename
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"Instruction file not found: {dir_hint}/{filename}")


def load_instruction(filename: str, *, dir_hint: str = "") -> LoadedInstruction:
    path = _resolve_path(dir_hint, filename)
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"Instruction file is empty: {path}")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return LoadedInstruction(filename=filename, text=text, sha256=digest)


def load_role_instructions(role: str) -> list[LoadedInstruction]:
    if role not in ROLE_INSTRUCTION_FILES:
        raise ValueError(f"Unknown role '{role}'. Known: {sorted(ROLE_INSTRUCTION_FILES)}")
    dir_hint, filename = ROLE_INSTRUCTION_FILES[role]
    results = [load_instruction(filename, dir_hint=dir_hint)]
    for sup_dir, sup_file in ROLE_SUPPLEMENTARY.get(role, []):
        results.append(load_instruction(sup_file, dir_hint=sup_dir))
    return results


def build_role_prompt(
    *,
    role: str,
    instructions: list[LoadedInstruction],
    context: str,
    task: str,
    output_schema: str = "",
) -> str:
    """Assemble a complete prompt for an AI role.

    Layout per embedding doc §16:
      SYSTEM ROLE → GOVERNING INSTRUCTIONS → CURRENT CONTEXT → TASK → OUTPUT CONTRACT
    """
    instr_blocks: list[str] = []
    for inst in instructions:
        instr_blocks.append(
            f'<role_instructions file="{inst.filename}" sha256="{inst.sha256[:16]}">\n'
            f"{inst.text}\n</role_instructions>"
        )
    instructions_block = "\n\n".join(instr_blocks)
    role_display = role.replace("_", " ").title()

    parts = [
        f"SYSTEM ROLE:\nYou are the {role_display} assistant.",
        f"\nGOVERNING INSTRUCTIONS:\n{instructions_block}",
        f"\nCURRENT CONTEXT:\n<context>\n{context}\n</context>",
        f"\nTASK:\n{task}",
    ]
    if output_schema:
        parts.append(f"\nOUTPUT CONTRACT:\n<output_contract>\n{output_schema}\n</output_contract>")
    return "\n\n".join(parts)


def operating_context_text() -> str:
    """Load the shared OPERATING-CONTEXT.md for seeding any role."""
    path = _AI_TEAM_DIR / "OPERATING-CONTEXT.md"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


