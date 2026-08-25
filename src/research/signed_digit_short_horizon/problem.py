"""Descriptor for signed-digit short-horizon controls."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="signed_digit_short_horizon",
    title="Signed-digit short-horizon controls",
    status="STRUCTURAL",
    statement=(
        "If 3 does not divide λ, then at a remaining-horizon control state "
        "q_L the product states (s,q_L) and (t,q_L) are observationally "
        "equivalent if and only if 3^L divides s-t. Horizon 0 is deadlock. "
        "The smallest genuine residual merge is (0,q_1)~(3,q_1)."
    ),
    bt_relevance=(
        "The residual step is existing D. Finite horizon only decides "
        "whether the 3-adic observation depth is accessible."
    ),
    docs=("docs/problems/signed_digit_short_horizon.md",),
    lean=("formal/Problems/BalancedTernary/SignedDigitShortHorizon.lean",),
)
