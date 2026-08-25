"""Scout dossier. Never imported by spec or adapter."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoutEntry:
    target: str
    problem_definition: str
    state_space: str
    transition_relation: str
    domain: str
    known_zeros: str
    known_zero_free: str
    known_computational: str
    known_conjectures: str
    literature: tuple[str, ...]
    saturation: str
    open_questions: str
    classifications: tuple[tuple[str, str], ...]


BASELINE = (
    (
        "The Skolem Problem asks whether an integer LRS ever vanishes.",
        "THEOREM",
    ),
    (
        "Skolem–Mahler–Lech: zeros of a non-degenerate LRS are a finite "
        "set union finitely many arithmetic progressions.",
        "THEOREM",
    ),
    (
        "Unconditional decidability is known through order 4.",
        "THEOREM",
    ),
    (
        "General Skolem decidability remains open from order 5 onward.",
        "OPEN",
    ),
    (
        "The 2026 survey exhibits an explicit order-6 integer LRS whose "
        "Skolem status is unresolved.",
        "COMPUTATIONAL",
    ),
)


MAP = ScoutEntry(
    target="companion_shift_order6",
    problem_definition=(
        "Does the order-6 integer LRS of Bacik–Karimov–Luca–Nieuwveld–"
        "Ouaknine–Purser–Worrell 2026, Section 8.3, ever vanish?"
    ),
    state_space="Z^6 companion windows (u_n,...,u_{n+5})",
    transition_relation="x |-> M x for the companion matrix of the recurrence",
    domain="n >= 0",
    known_zeros=(
        "No integer zero is known. Any integer zero is congruent to 4 mod 16 "
        "and, by a 17-adic analysis, larger than 10^1000 if it exists. At most "
        "one natural-number zero is possible."
    ),
    known_zero_free=(
        "u_n != 0 for all n <= 10^1000 (17-adic interpolants). No modular "
        "certificate exists: the sequence has zeros modulo every m >= 2 "
        "(Proposition 53). No semialgebraic invariant exists. The instance "
        "lies outside the MSTV class."
    ),
    known_computational=(
        "Closed form u_n = 2(-4+7i)^n + 2(-4-7i)^n + 4(8+i)^n + 4(8-i)^n + n. "
        "Initial window 12, 49, 374, 6003, 21520, 150773. First negative term "
        "u_11. Characteristic polynomial (x-1)^2 (x^2+8x+65)(x^2-16x+65)."
    ),
    known_conjectures=(
        "Conditional general decidability under ELGP / p-adic Schanuel, and "
        "a 2026 Cramér-type heuristic ruling out large zeros. Neither is an "
        "unconditional procedure for this instance."
    ),
    literature=(
        "bacik-et-al-2026-skolem-positivity-survey",
        "lipton-et-al-2022-skolem-conjecture",
        "luca-ouaknine-worrell-2026-conjectural-decidability",
        "kenison-et-al-2025-order-4-skolem",
    ),
    saturation=(
        "Order <= 4 is classical. This order-6 example is the survey's "
        "explicit unresolved Skolem instance. Do not import roots, p-adic "
        "interpolants, or Proposition 53 into the adapter."
    ),
    open_questions="Does the sequence (13) of the 2026 survey vanish for some n in N?",
    classifications=(
        ("Skolem decidable for integer LRS of order <= 4.", "THEOREM"),
        ("Skolem open for general order >= 5.", "OPEN"),
        ("Survey sequence (13) has no modular or semialgebraic certificate.", "THEOREM"),
        ("u_n != 0 for n <= 10^1000.", "COMPUTATIONAL"),
        ("Whether any integer zero exists is open.", "OPEN"),
        ("Zeros modulo every m >= 2 (ghost zeros).", "THEOREM"),
    ),
)


SCOUTS = {MAP.target: MAP}


def scout_for(name: str) -> ScoutEntry:
    return SCOUTS.get(name, MAP)
