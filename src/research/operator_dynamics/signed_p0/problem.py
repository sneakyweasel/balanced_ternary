"""Descriptor for the N∘I₀∘D cross-dynamics benchmark."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="operator_dynamics_benchmark",
    title="Cross-dynamics benchmark of N∘I₀∘D",
    status="ARCHIVED",
    statement=(
        "The integer map F = N∘I_0∘D has F² = P_0 and every orbit has size "
        "at most 3. The preferred family I_a∘D∘I_b collapses to I_a. v2 "
        "diagnoses finite per-orbit closure, a leaking interval envelope, "
        "and a sign Mealy quotient strictly smaller than the reachable set."
    ),
    bt_relevance=(
        "F is the existing word N I0 D evaluated on Z. Local semantics are "
        "the calculus identities D∘I_0 = id and P_0 = I_0∘D."
    ),
    docs=("docs/problems/operator_dynamics_benchmark.md",),
    lean=("formal/Problems/BalancedTernary/SignedP0.lean",),
)
