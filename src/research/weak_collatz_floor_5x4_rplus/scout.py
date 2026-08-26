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
        "One-variable integer SLCs are tightly connected to generalized Collatz maps.",
        "THEOREM",
    ),
    (
        "The 4/3 strip R+ was already reconstructed; this is a different (m,d) instance.",
        "KNOWN",
    ),
    (
        "Reachability for modulus d>2 remains open in the literature.",
        "CONJECTURE",
    ),
)


MAP = ScoutEntry(
    target="weak_collatz_floor_5x4_rplus",
    problem_definition=(
        "On the integer strip 5x-4 <= 4x' <= 5x-1 with x >= 2, does an exact "
        "class or branch obstruction constrain losing the successor?"
    ),
    known_theorems=(
        "A cyclic trace of a one-variable integer SLC implies a cyclic trace of "
        "length at most two (Carelli). Weak maps with modulus 2 are decided."
    ),
    known_barriers=(
        "Recovering residue-affine branches is the 4/3 campaign language, not a "
        "new theorem. Finite seed growth is not a map theorem on Z. A universal "
        "halt claim is forbidden."
    ),
    open_questions=(
        "Class obstruction to losing the successor; not termination of floor(5x/4) "
        "and not the Reachability Conjecture."
    ),
    literature=(
        "carelli-2026-loop-termination",
        "matthews-watts-1984-generalization-hasse",
        "ben-amram-genaim-ouaknine-worrell-2025-termination-survey",
    ),
    classifications=(
        ("The inequality graph is a one-variable SLC.", "THEOREM"),
        ("The 4/3 R+ reconstruction is KNOWN.", "KNOWN"),
        ("A 5/4-specific obstruction, if any, is the question.", "UNKNOWN"),
    ),
)


def scout_for(name: str) -> ScoutEntry:
    del name
    return MAP
