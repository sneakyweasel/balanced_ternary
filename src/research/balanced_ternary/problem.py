"""Descriptor for doubled-trit finite-state dynamics."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="balanced_ternary_finite_state_dynamics",
    title="Balanced-ternary finite-state dynamics",
    status="STRUCTURAL",
    statement=(
        "Doubled-trit normalization has residual closure {-1,0,1}. "
        "The expanding map T(n)=3n-lsd(n) has infinite integer orbits, "
        "a 3-state LSD quotient, a 9-state J2 quotient, and a 27-state "
        "J3 quotient that factors through J2 by the shift (-a,a,b). "
        "The unary/Add boundary has residual D(lsd x + lsd y) with "
        "exact trit closure {-1,0,1}."
    ),
    bt_relevance=(
        "T is the existing section I_{-lsd(n)}(n). Lab D remains "
        "(n-lsd(n))/3. The adapter does not introduce a second digit model."
    ),
    docs=(
        "docs/problems/balanced_ternary_finite_state_dynamics.md",
        "docs/problems/d_add_residual.md",
    ),
    lean=(
        "formal/Problems/BalancedTernary/FiniteStateDynamics.lean",
        "formal/Problems/BalancedTernary/ExpandingD.lean",
        "formal/Problems/BalancedTernary/DAddResidual.lean",
    ),
)
