"""Descriptor for the balanced-ternary weight-dynamics control experiment."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="balanced_ternary_weight_dynamics",
    title="Balanced-ternary weight dynamics",
    status="ARCHIVED",
    statement=(
        "The integer map T(n)=W(n)=∑ d_i² strictly decreases |n| for |n|≥3 "
        "and every orbit is finite. v2 diagnoses the same finite-contracting "
        "digit-fold regime as s(n), with recurrent set {0,1,2} rather than "
        "{-1,0,1}. The |n|≥2 contraction of s(n) fails at T(2)=2."
    ),
    bt_relevance=(
        "W is the recursive fold of already-certified local digits: "
        "W(n)=lsd(n)²+W(D(n))."
    ),
    docs=("docs/problems/balanced_ternary_weight_dynamics.md",),
    lean=("formal/Problems/BalancedTernary/WeightDynamics.lean",),
)
