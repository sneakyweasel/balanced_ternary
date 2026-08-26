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
        "Small positive seeds reach 1 under the even/odd floor-power map.",
        "COMPUTATIONAL",
    ),
    (
        "The map is not residue-affine; odd terms use a floor of a 3/2-power.",
        "KNOWN",
    ),
    (
        "Universal reachability of 1 is literature-open and not this campaign's yield.",
        "OPEN",
    ),
)


MAP = ScoutEntry(
    target="juggler_sequence",
    problem_definition=(
        "On the stored even/odd floor-power map, does frozen v2.3 diagnose a "
        "regime distinct from residue-affine control and from divisor-sum, "
        "without a radical attack and without a halt theorem on all positive integers?"
    ),
    known_theorems=(
        "Packet seed 13 reaches 1 in four steps. 1 is a fixed point. "
        "Some odd seeds increase. The map is not the 5x/4 strip and not sigma(n)-n."
    ),
    known_barriers=(
        "A finite seed closure is not a Z-theorem. Floor powers are outside "
        "the frozen affine census. Do not add a radical attack."
    ),
    open_questions="Whether every positive integer reaches 1.",
    literature=("oeis-A007320",),
    classifications=(
        ("Seed 13 reaches 1 in four steps.", "KNOWN"),
        ("No residue-affine cover is expected.", "KNOWN"),
        ("Universal halt is literature-open.", "OPEN"),
    ),
)


def scout_for(name: str) -> ScoutEntry:
    del name
    return MAP
