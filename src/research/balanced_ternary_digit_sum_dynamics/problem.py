"""Descriptor for the balanced-ternary digit-sum dynamics benchmark."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="balanced_ternary_digit_sum_dynamics",
    title="Balanced-ternary digit-sum dynamics",
    status="ARCHIVED",
    statement=(
        "The integer map T(n)=s(n), the signed sum of canonical balanced-ternary "
        "digits, strictly decreases |n| for |n|≥2 and every orbit is finite. "
        "v2 diagnoses per-seed exact closure, a non-leaking interval sample, "
        "and identity-observation Mealy size equal to the reachable orbit. "
        "The regime is the known balanced-ternary digital root."
    ),
    bt_relevance=(
        "T is the recursive fold of already-certified local digits "
        "lsd and D: s(n)=lsd(n)+s(D(n))."
    ),
    docs=("docs/problems/balanced_ternary_digit_sum_dynamics.md",),
    lean=("formal/Problems/BalancedTernary/DigitSumDynamics.lean",),
)
