"""Candidate Reverse-and-Add attack families. Not executable."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CandidateAttackFamily:
    """Named attack family for later selection. Never a flood-order attack."""

    family_id: str
    title: str
    question: str
    existing_machinery: str
    executable: bool = False

    def __post_init__(self) -> None:
        if self.executable:
            raise ValueError(f"{self.family_id} must not be marked executable")


DIGIT_TRANSDUCER = CandidateAttackFamily(
    family_id="digit_transducer",
    title="Digit transducer",
    question=(
        "What local information (digit pair and carry, or an equivalent) is "
        "required to process one Reverse-and-Add step, and does a bounded "
        "carry alphabet suffice?"
    ),
    existing_machinery=(
        "bt.transducers; engine reverse-add carry Phases 4-5 as comparison "
        "on the distinct map n+W(n), not as this unsigned R_b"
    ),
)

RESIDUAL_STATE_ANALYSIS = CandidateAttackFamily(
    family_id="residual_state_analysis",
    title="Residual-state analysis",
    question=(
        "Does a residual of a partially processed digit string determine "
        "future Reverse-and-Add evolution, so that distinct prefixes can "
        "collapse to identical residual behaviour?"
    ),
    existing_machinery=(
        "research_engine residual / Mealy quotient "
        "(research_engine.behavior.quotient); do not introduce a parallel "
        "abstraction unless that one is inapplicable"
    ),
)

PALINDROME_SEPARATION = CandidateAttackFamily(
    family_id="palindrome_separation",
    title="Palindrome-separation analysis",
    question=(
        "For residuals q1, q2, does there exist a continuation w such that "
        "PalReach(q1,w) != PalReach(q2,w)? Use the smallest exact definition "
        "supported later; this formula is not assumed final."
    ),
    existing_machinery=(
        "research_engine.attacks.separation pair-state BFS; palindrome "
        "reachability is a target condition, not a proved invariant"
    ),
)

FORBIDDEN_PATTERN_SEARCH = CandidateAttackFamily(
    family_id="forbidden_pattern_search",
    title="Forbidden-pattern search",
    question=(
        "Which finite digit or carry patterns cannot occur on a trajectory "
        "from a valid positive integer? Distinguish syntactic, locally "
        "transition-valid, globally realizable, and origin-live words."
    ),
    existing_machinery=(
        "Ostrowski/engine origin-live and forbidden-word terminology; do not "
        "invent a parallel vocabulary"
    ),
)

POTENTIAL_ENERGY = CandidateAttackFamily(
    family_id="potential_energy",
    title="Potential / energy functions",
    question=(
        "Are there exact or eventually contracting quantities in digit length, "
        "leading/trailing structure, carry profile, digit sum, weighted digit "
        "sum, symmetric digit differences, or residual automaton state? Do "
        "not assume monotone decrease. Heuristics are not proved invariants."
    ),
    existing_machinery=(
        "engine functional/ranking probes as negative templates; Phase-0/1 "
        "ranking is not an attack family for this map"
    ),
)

CANDIDATE_ATTACK_FAMILIES: tuple[CandidateAttackFamily, ...] = (
    DIGIT_TRANSDUCER,
    RESIDUAL_STATE_ANALYSIS,
    PALINDROME_SEPARATION,
    FORBIDDEN_PATTERN_SEARCH,
    POTENTIAL_ENERGY,
)

CANDIDATE_ATTACK_FAMILY_IDS: tuple[str, ...] = tuple(
    item.family_id for item in CANDIDATE_ATTACK_FAMILIES
)
