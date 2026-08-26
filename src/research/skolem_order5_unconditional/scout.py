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
        "Unconditional first-coordinate vanishing is decided through order 4.",
        "THEOREM",
    ),
    (
        "Order 5 is decidable only conditionally; this campaign forbids that procedure.",
        "KNOWN",
    ),
    (
        "A 25^5 census cube is skipped by the frozen cell budget, as at dimension 6.",
        "KNOWN",
    ),
)


MAP = ScoutEntry(
    target="skolem_order5_unconditional",
    problem_definition=(
        "On a declared order-5 companion window, can frozen v2.3 do more than "
        "exhaust a finite prefix without interpolants?"
    ),
    known_theorems=(
        "Order <= 4 vanishing is decidable. The companion representation fits. "
        "Lipton et al. 2022 Example 2.4 has a unique zero at index 2, certified "
        "in the literature by a modulus larger than the frozen 2..32 probe."
    ),
    known_barriers=(
        "A finite zero is not an unconditional order-5 decision procedure. "
        "Census skip at d=5 is the same computational cluster as d=6. "
        "Interpolants and named modular uniqueness certificates are forbidden."
    ),
    open_questions=(
        "Unconditional vanishing for general order-5 LRS; not this campaign's yield."
    ),
    literature=(
        "lipton-et-al-2022-skolem-conjecture",
        "kenison-et-al-2025-order-4-skolem",
        "bacik-et-al-2026-skolem-positivity-survey",
    ),
    classifications=(
        ("Order <= 4 vanishing is decidable.", "THEOREM"),
        ("This explicit order-5 window has a literature zero at index 2.", "KNOWN"),
        ("Unconditional order-5 decidability remains open.", "OPEN"),
        ("25^5 census skip is the same barrier as 25^6.", "KNOWN"),
    ),
)


def scout_for(name: str) -> ScoutEntry:
    del name
    return MAP
