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
        "The three residue-affine formulas are the problem definition.",
        "KNOWN",
    ),
    (
        "Once 0 (mod 3) is hit the orbit stays there and expands.",
        "THEOREM",
    ),
    (
        "Avoiding orbits enter the cycles at -1 or {-2,-4} is literature-open.",
        "CONJECTURE",
    ),
)


MAP = ScoutEntry(
    target="matthews_prize_mod3_avoider",
    problem_definition=(
        "On T(x)=2x when 3|x, T(x)=(7x+2)/3 when x ≡ 1 (mod 3), "
        "T(x)=(x-2)/3 when x ≡ 2 (mod 3), does an exact class obstruction "
        "force ±1 (mod 3) avoiders into the known cycles?"
    ),
    known_theorems=(
        "0 (mod 3) is invariant and expanding. Length-one cycle at -1. "
        "Length-two cycle {-2,-4}."
    ),
    known_barriers=(
        "Branch reconstruction is the problem definition, not a new theorem. "
        "Finite seed visits of cycles are not a map theorem on Z. Totality "
        "and prize claims are forbidden."
    ),
    open_questions=(
        "Class obstruction forcing avoiders into the known cycles; not "
        "convergence of every orbit."
    ),
    literature=("matthews-watts-1984-generalization-hasse",),
    classifications=(
        ("The three formulas are the problem definition.", "KNOWN"),
        ("0 (mod 3) is invariant.", "THEOREM"),
        ("An avoider-class obstruction, if any, is the question.", "UNKNOWN"),
    ),
)


def scout_for(name: str) -> ScoutEntry:
    del name
    return MAP
