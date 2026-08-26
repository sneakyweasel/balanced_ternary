"""Scout dossier. Never imported by spec, adapter, or planner."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoutEntry:
    target: str
    problem_definition: str
    known_theorems: str
    known_barriers: str
    open_questions: str
    literature: tuple[str, ...]
    classifications: tuple[tuple[str, str], ...]


BASELINE = (
    (
        "The accelerated odd map T(x)=(7x+1)/2^{v_2(7x+1)} is well-defined.",
        "THEOREM",
    ),
    (
        "Family reconstruction 2^k y = 7x+1 is KNOWN infrastructure, not the target.",
        "KNOWN",
    ),
    (
        "Most 5x+1 / 7x+1 relatives are believed divergent (Crandall).",
        "CONJECTURE",
    ),
)


MAP = ScoutEntry(
    target="mx_plus_r_7x1_class_obstruction",
    problem_definition=(
        "On the normalized odd map T(x)=(7x+1)/2^{v_2(7x+1)}, does an exact "
        "class obstruction constrain which odd states can reach 1?"
    ),
    known_theorems=(
        "The accelerated odd map is well-defined. Length-one cycles of 2^k y = mx+r "
        "require (2^k-m) | r. For (m,r)=(7,1) this forces the fixed point 1."
    ),
    known_barriers=(
        "Family rediscovery is not a new theorem. Finite non-visit of 1 is not "
        "divergence. A residue image restriction is not automatically a basin exclusion."
    ),
    open_questions="Class obstruction to reaching 1; not convergence of 7x+1.",
    literature=("crandall-1978-3x+1", "chamberland-2003-3x+1-survey"),
    classifications=(
        ("Accelerated 7x+1 is well-defined.", "THEOREM"),
        ("Family 2^k y = 7x+1 is KNOWN.", "KNOWN"),
        ("A 7-specific class constraint, if any, is the question.", "UNKNOWN"),
    ),
)


def scout_for(name: str) -> ScoutEntry:
    del name
    return MAP
