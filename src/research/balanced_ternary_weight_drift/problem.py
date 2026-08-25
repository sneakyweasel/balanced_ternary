"""Descriptor for the balanced-ternary weight-drift experiment."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="balanced_ternary_weight_drift",
    title="Balanced-ternary weight-drift dynamics",
    status="ARCHIVED",
    statement=(
        "The integer map T(n)=n+W(n) strictly increases off 0, preserves the "
        "nonpositive ray, and sends every nonpositive seed to 0. Positive "
        "orbits are infinite. v2 reports inconclusive residual closure on the "
        "positive seed 4, unlike the finite-contracting digit-fold regime."
    ),
    bt_relevance=(
        "The increment is the already-certified local fold W(n)=lsd(n)²+W(D(n)); "
        "the state is not replaced by that statistic."
    ),
    docs=("docs/problems/balanced_ternary_weight_drift.md",),
    lean=("formal/Problems/BalancedTernary/WeightDrift.lean",),
)
