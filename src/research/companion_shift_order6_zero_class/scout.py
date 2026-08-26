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
        "The order-6 companion window was already reconstructed; vanishing remains open.",
        "KNOWN",
    ),
    (
        "Unconditional first-coordinate vanishing is decided through order 4.",
        "THEOREM",
    ),
    (
        "A 25^6 census cube is skipped by the frozen cell budget.",
        "KNOWN",
    ),
)


MAP = ScoutEntry(
    target="companion_shift_order6_zero_class",
    problem_definition=(
        "On the declared order-6 companion window, can matrix-word or lattice-gcd "
        "structure recover a congruence constraint on vanishing indices without interpolants?"
    ),
    known_theorems=(
        "Order <= 4 vanishing is decidable. The companion representation fits. "
        "No zero on the stored finite prefix. u_11 < 0."
    ),
    known_barriers=(
        "Companion rediscovery is not a class constraint. Finite prefix gaps are "
        "not modular exclusion. Non-existence of a zero is forbidden. Interpolants "
        "are forbidden."
    ),
    open_questions=(
        "A lattice/gcd congruence on vanishing indices; not a decision procedure "
        "and not non-existence."
    ),
    literature=(
        "bacik-et-al-2026-skolem-positivity-survey",
        "kenison-et-al-2025-order-4-skolem",
        "lipton-et-al-2022-skolem-conjecture",
    ),
    classifications=(
        ("The companion window is KNOWN laboratory infrastructure.", "KNOWN"),
        ("Order <= 4 vanishing is decidable.", "THEOREM"),
        ("A vanishing-index class constraint, if any, is the question.", "UNKNOWN"),
    ),
)


def scout_for(name: str) -> ScoutEntry:
    del name
    return MAP
