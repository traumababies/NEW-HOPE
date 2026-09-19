"""State-machine domain — the closed-loop pipeline (The Library.txt G.8.a.iii).

States:
  STEP_0_ORIGINAL       file enters (pipeline scratchpad / original)
  STEP_1_COMPLETE       an editing/generation step finished
  STEP_2_PENDING        awaiting review / approval
  PIPELINE_COMPLETE_APPROVED  loop closed (approved -> Bunbuns permanent)

The listener rule (G.8.b.i): a later room only pulls rows whose CurrentState
equals the previous step's completion.
"""
from __future__ import annotations

STEP_0_ORIGINAL = "STEP_0_ORIGINAL"
STEP_1_COMPLETE = "STEP_1_COMPLETE"
STEP_2_PENDING = "STEP_2_PENDING"
PIPELINE_COMPLETE_APPROVED = "PIPELINE_COMPLETE_APPROVED"

ALLOWED_TRANSITIONS: dict[str, tuple[str, ...]] = {
    STEP_0_ORIGINAL: (STEP_1_COMPLETE, STEP_2_PENDING),
    STEP_1_COMPLETE: (STEP_2_PENDING, STEP_0_ORIGINAL),
    STEP_2_PENDING: (PIPELINE_COMPLETE_APPROVED, STEP_1_COMPLETE),
    PIPELINE_COMPLETE_APPROVED: (),
}


def can_transition(from_state: str, to_state: str) -> bool:
    return to_state in ALLOWED_TRANSITIONS.get(from_state, ())


def transition(from_state: str, to_state: str) -> str:
    if not can_transition(from_state, to_state):
        raise ValueError(f"Illegal state transition: {from_state} -> {to_state}")
    return to_state
