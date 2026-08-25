"""Scout dossier. Never imported by spec or adapter."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoutEntry:
    target: str
    problem_definition: str
    order: str
    recurrence_coefficients: str
    initial_values: str
    characteristic_polynomial: str
    known_equivalent_formulations: str
    known_positivity: str
    known_nonnegativity: str
    known_eventual_positivity: str
    known_counterexamples: str
    known_asymptotic: str
    known_spectral: str
    known_modular: str
    known_padic: str
    known_conditional: str
    known_decidability_boundary: str
    current_unresolved_status: str
    literature: tuple[str, ...]
    classifications: tuple[tuple[str, str], ...]


BASELINE = (
    (
        "The Positivity Problem asks whether every term of an integer LRS is nonnegative.",
        "THEOREM",
    ),
    (
        "Positivity is decidable for integer LRS of order at most 5.",
        "THEOREM",
    ),
    (
        "Positivity is decidable for simple integer LRS of order at most 9.",
        "THEOREM",
    ),
    (
        "Decidability of Positivity for general integer LRS of order 6 would have Diophantine-approximation consequences.",
        "CONDITIONAL",
    ),
    (
        "The 2026 survey exhibits an explicit simple order-10 integer LRS whose Positivity status is unresolved.",
        "COMPUTATIONAL",
    ),
)


MAP = ScoutEntry(
    target="companion_obs_order10",
    problem_definition=(
        "Are all terms of the order-10 simple integer LRS (16) of "
        "Bacik–Karimov–Luca–Nieuwveld–Ouaknine–Purser–Worrell 2026, "
        "Section 8.4, nonnegative?"
    ),
    order="10",
    recurrence_coefficients=(
        "u_{n+10} = -u_{n+9} - 378 u_{n+8} + 749576 u_{n+7} - 2333386 u_{n+6} "
        "+ 55996590 u_{n+5} - 205750047100 u_{n+4} + 856834394000 u_{n+3} "
        "+ 13815580471875 u_{n+2} + 20682499470546875 u_{n+1} "
        "- 41423825675781250 u_n"
    ),
    initial_values=(
        "35, 574, 34592, 8999992, 115734548, 5682747424, 1837938758372, "
        "13061285121472, 397924220049188, 290333397927490624"
    ),
    characteristic_polynomial=(
        "(x-2)(x-65)(x^2+66x+4225)(x^2-126x+4225)(x^2+78x+4225)(x^2+50x+4225). "
        "Roots: 2, 65, and the eight non-real Gaussian integers of modulus 65 "
        "arising as pairwise products of {-4±7i, 8±i}."
    ),
    known_equivalent_formulations=(
        "u_n = w_n^2 - 2^n, where w_n = λ1^n + conj(λ1)^n + 2 λ2^n + 2 conj(λ2)^n, "
        "λ1 = (1+2i)(2+3i) = -4+7i, λ2 = (1+2i)(2-3i) = 8+i. Companion-matrix form "
        "x |-> M x in Z^10 with observation e1^T x."
    ),
    known_positivity="No unconditional certificate that u_n >= 0 for every n >= 0 is known.",
    known_nonnegativity=(
        "Direct computation: u_n >= 0 for 0 <= n <= 10^6. Independently, the "
        "initial window and the recurrence coefficients match the closed form."
    ),
    known_eventual_positivity=(
        "Ultimately positive by the ineffective growth theorem: |w_n| > 2^{n/2} "
        "for all sufficiently large n, hence u_n > 0 eventually. No onset index "
        "is known."
    ),
    known_counterexamples="No negative term is known. Skolem for this sequence is settled: no zeros.",
    known_asymptotic=(
        "Nine dominant roots of modulus 65 and one non-dominant root 2. "
        "Growth is of order 65^n. Sign of the dominant combination is not "
        "controlled by an effective Baker bound because of the asymmetric "
        "coefficients 1,1,2,2 on w."
    ),
    known_spectral=(
        "Simple, non-degenerate. Dominant roots are the pairwise products of "
        "the four Gaussian integers of modulus sqrt(65) that also drive survey "
        "sequence (13)."
    ),
    known_modular=(
        "Modular certificates are of no use for Positivity (survey Section 4.5). "
        "A residue constraint is not a sign theorem."
    ),
    known_padic="p-adic interpolants do not yield a Positivity certificate for this instance.",
    known_conditional=(
        "A Positivity oracle for simple order-10 LRS would decide Skolem at "
        "order 5 (Theorem 52). No number-theoretic conjecture currently decides "
        "sequence (16)."
    ),
    known_decidability_boundary=(
        "Simple Positivity is decidable through order 9 (Baker). The techniques "
        "break at order 10. General Positivity is decidable through order 5, "
        "with Diophantine hardness at order 6."
    ),
    current_unresolved_status=(
        "Positivity of sequence (16) is open. No semialgebraic invariant "
        "certifying u_n >= 0 exists (algorithm of [9] returns negative). "
        "The gap between the computed prefix 10^6 and the ineffective onset "
        "is the open question."
    ),
    literature=(
        "bacik-et-al-2026-skolem-positivity-survey",
        "ouaknine-worrell-2014-positivity-low-order",
        "ouaknine-worrell-2014-simple-positivity",
    ),
    classifications=(
        ("Positivity decidable for integer LRS of order <= 5.", "THEOREM"),
        ("Positivity decidable for simple integer LRS of order <= 9.", "THEOREM"),
        ("Ultimate Positivity of simple LRS of all orders is decidable but non-constructive.", "THEOREM"),
        ("Sequence (16) is simple of order exactly 10 and non-degenerate.", "THEOREM"),
        ("Sequence (16) is ultimately positive.", "THEOREM"),
        ("u_n >= 0 for n <= 10^6.", "COMPUTATIONAL"),
        ("Sequence (16) has no zeros (Skolem settled).", "COMPUTATIONAL"),
        ("No semialgebraic invariant certifies u_n >= 0.", "THEOREM"),
        ("Whether u_n >= 0 for every n >= 0 is open.", "UNKNOWN"),
        ("Onset of the growth theorem is ineffective.", "THEOREM"),
        ("Decidability of simple Positivity at order 10 would decide Skolem at order 5.", "THEOREM"),
        ("Modular methods do not yield Positivity certificates.", "THEOREM"),
    ),
)


SCOUTS = {MAP.target: MAP}


def scout_for(name: str) -> ScoutEntry:
    return SCOUTS.get(name, MAP)
