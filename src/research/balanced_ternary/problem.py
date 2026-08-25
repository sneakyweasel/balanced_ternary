"""Descriptor for doubled-trit finite-state dynamics."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="balanced_ternary_finite_state_dynamics",
    title="Balanced-ternary finite-state dynamics",
    status="STRUCTURAL",
    statement=(
        "Doubled-trit normalization has residual closure {-1,0,1}. "
        "The expanding map T(n)=3n-lsd(n) has infinite integer orbits "
        "and a 3-state LSD observational quotient r |-> -r."
    ),
    bt_relevance=(
        "T is the existing section I_{-lsd(n)}(n). Lab D remains "
        "(n-lsd(n))/3. The adapter does not introduce a second digit model."
    ),
    docs=("docs/problems/balanced_ternary_finite_state_dynamics.md",),
    lean=(
        "formal/Problems/BalancedTernary/FiniteStateDynamics.lean",
        "formal/Problems/BalancedTernary/ExpandingD.lean",
    ),
)
