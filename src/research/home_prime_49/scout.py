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
        "Packet seed 49 grows under factor concatenation until the factorization budget.",
        "COMPUTATIONAL",
    ),
    (
        "The map is not residue-affine; concatenation of prime factors is not a linear control.",
        "KNOWN",
    ),
    (
        "Whether seed 49 reaches a prime is literature-open and not this campaign's yield.",
        "OPEN",
    ),
)


MAP = ScoutEntry(
    target="home_prime_49",
    problem_definition=(
        "On the stored factorization-concatenation map, does frozen v2.3 diagnose "
        "a regime that recurs the non-affine arithmetic cluster, distinct from "
        "divisor-sum truncation and from reverse-add or floor-power closures, "
        "without a dedicated attack and without claiming that seed 49 reaches a prime?"
    ),
    known_theorems=(
        "T(p)=p for a prime p inside the budget. Seed 4 reaches the prime 211. "
        "Seed 10 reaches the prime 773. Seed 49 maps to 77 then grows past the "
        "factorization cap. The successor is not sigma(n)-n and not a floor power."
    ),
    known_barriers=(
        "A budget truncation is not a Z-theorem. Factor concatenation is outside "
        "the frozen affine census. Do not add a concatenation attack. Do not "
        "import published unfinished-seed folklore."
    ),
    open_questions="Whether seed 49 eventually reaches a prime.",
    literature=("oeis-A037274",),
    classifications=(
        ("T(p)=p for primes inside the budget.", "KNOWN"),
        ("Seed 4 reaches 211.", "KNOWN"),
        ("No residue-affine cover is expected.", "KNOWN"),
        ("Seed 49 reaching a prime is literature-open.", "OPEN"),
    ),
)


def scout_for(name: str) -> ScoutEntry:
    del name
    return MAP
