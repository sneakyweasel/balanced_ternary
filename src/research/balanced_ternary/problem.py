"""Descriptor for doubled-trit finite-state dynamics."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="balanced_ternary_finite_state_dynamics",
    title="Balanced-ternary finite-state dynamics",
    status="STRUCTURAL",
    statement=(
        "The LSD carry of normalizing the doubled trit stream 2 d_i, "
        "d_i in {-1,0,1}, has exact residual closure {-1,0,1}. The "
        "mechanism is radix-3 division plus bounded forcing. Gain λ=3 "
        "on the same remainder map is unbounded along the all-+1 word."
    ),
    bt_relevance=(
        "The adapter reuses BoundedNormalizeTransducer(2) and "
        "balanced_divmod; it does not introduce a second digit model."
    ),
    docs=("docs/problems/balanced_ternary_finite_state_dynamics.md",),
    lean=("formal/Problems/BalancedTernary/FiniteStateDynamics.lean",),
)
