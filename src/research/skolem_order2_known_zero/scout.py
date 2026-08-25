"""Scout dossier. Never imported by spec or adapter."""

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
        "Unconditional Skolem decidability is known through order 4.",
        "THEOREM",
    ),
    (
        "An explicit order-2 companion window with a first-coordinate zero "
        "is a competence check, not an open instance.",
        "KNOWN",
    ),
    (
        "General Skolem decidability remains open from order 5 onward.",
        "OPEN",
    ),
)


MAP = ScoutEntry(
    target="companion_shift_order2",
    problem_definition=(
        "On the declared order-2 companion window, does the first coordinate "
        "vanish, and does frozen v2 recover the companion matrix?"
    ),
    known_theorems=(
        "Order <= 4 Skolem is decidable (Kenison–Nieuwveld–Ouaknine–Worrell). "
        "This window is a known finite zero, not an open instance."
    ),
    known_barriers=(
        "The open cluster is infinite-time vanishing in higher order. "
        "This calibration must not be billed as that cluster."
    ),
    open_questions="None for this calibration window.",
    literature=(
        "kenison-et-al-2025-order-4-skolem",
        "bacik-et-al-2026-skolem-positivity-survey",
    ),
    classifications=(
        ("Order <= 4 Skolem is decidable.", "THEOREM"),
        ("This explicit order-2 window has a certified small zero.", "KNOWN"),
        ("Order-6 vanishing remains a separate GLOBAL_REASONING cluster.", "OPEN"),
    ),
)


def scout_for(name: str) -> ScoutEntry:
    del name
    return MAP
