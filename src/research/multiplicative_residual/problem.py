"""Descriptor for multiplicative residual universality."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="multiplicative_residual",
    title="Multiplicative residual universality",
    status="STRUCTURAL",
    statement=(
        "If F(s,c)=λ·D(s+h(c)) with output lsd(s+h(c)), residual dynamics "
        "factor through the raw contribution h. Product of two or three "
        "trits has h-image {-1,0,1} and the same origin-reachable residual "
        "as F_{λ,U_1}. The doubled product 2 d1 d2 follows U={-2,0,2}."
    ),
    bt_relevance=(
        "h is ordinary trit multiplication, the local factor already in "
        "lsd(xy)=lsd(x)lsd(y). The step reuses existing D/lsd and "
        "signed_step. No second product model."
    ),
    docs=("docs/problems/multiplicative_residual.md",),
    lean=("formal/Problems/BalancedTernary/MultiplicativeResidual.lean",),
)
