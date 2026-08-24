"""Descriptor for the accelerated Collatz research module."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="collatz",
    title="Accelerated odd-only Collatz through exponent codes",
    status="STRUCTURAL",
    statement=(
        "Study the accelerated map T(n)=(3n+1)/2^{v2(3n+1)} on positive odd "
        "integers via valuation codes, 2-adic cylinders, lift digits, affine "
        "centers, and balanced-ternary observables. This module does not "
        "claim a proof or disproof of the Collatz conjecture."
    ),
    bt_relevance=(
        "Balanced ternary represents the canonical realizer R and supplies "
        "word maps (W) and digit features as observables, not as an "
        "independent coordinate that solves the dynamics."
    ),
    docs=(
        "docs/problems/collatz.md",
        "docs/collatz_mathematics.md",
        "docs/collatz_research_questions.md",
    ),
    lean=("formal/Problems/Collatz/",),
    conjectures=("Nk_state_count", "low_Km_m_infinite_lifts", "noncontraction_R_to_infinity"),
)
