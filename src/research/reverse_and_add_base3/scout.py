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
        "Packet seed 196 is reverse-fixed and reaches 0 in eight steps.",
        "COMPUTATIONAL",
    ),
    (
        "The map is not residue-affine; digit reverse is not a linear control.",
        "KNOWN",
    ),
    (
        "Universal reverse-fixed reachability is literature-open and not this campaign's yield.",
        "OPEN",
    ),
)


MAP = ScoutEntry(
    target="reverse_and_add_base3",
    problem_definition=(
        "On the stored balanced-ternary reverse-plus-add map, does frozen v2.3 "
        "diagnose a regime distinct from digit-fold saturation and from "
        "factorization or floor-power maps, without a reverse-fixed totality "
        "theorem and without importing base-10 folklore?"
    ),
    known_theorems=(
        "Packet seed 196 equals its digit reverse, so the first image is 392. "
        "The orbit reaches 0 in eight steps. 0 is a fixed point. The map is "
        "not digit-sum, not sigma(n)-n, and not the even/odd floor-power map."
    ),
    known_barriers=(
        "A finite seed closure is not a Z-theorem. Digit reverse is outside "
        "the frozen affine census. Do not add a reverse-add attack. Do not "
        "import palindrome conjectures."
    ),
    open_questions="Whether every integer seed eventually hits a reverse-fixed point.",
    literature=("oeis-A134028",),
    classifications=(
        ("Seed 196 reaches 0 in eight steps.", "KNOWN"),
        ("No residue-affine cover is expected.", "KNOWN"),
        ("Universal reverse-fixed reachability is literature-open.", "OPEN"),
    ),
)


def scout_for(name: str) -> ScoutEntry:
    del name
    return MAP
