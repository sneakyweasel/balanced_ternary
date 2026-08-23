"""Descriptor for cubic residual Newton-stratum research."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="residuals",
    title="Cubic residual Newton stratum",
    status="STRUCTURAL",
    statement=(
        "Dedicated x^3 counting is closed at Outcome C: after the exact "
        "Newton-stratum reductions, M_k(x^3) is the N3-gated deep-image "
        "union. No substantially simpler closed arithmetic formula exists "
        "inside this framework. No single closed term for M_k is claimed."
    ),
    bt_relevance=(
        "Residuals are the section-calculus Mealy machine of bt.calculus. "
        "Packed prefixes are balanced-ternary words of length m."
    ),
    docs=(
        "docs/problems/residuals.md",
        "docs/theory/cubic_newton_stratum.md",
    ),
    lean=(
        "formal/BTCalculus/NewtonStratum.lean",
        "formal/BTCalculus/XCubeStateComplexity.lean",
    ),
)
