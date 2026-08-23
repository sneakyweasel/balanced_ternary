"""Descriptor for cubic residual Newton-stratum research."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="residuals",
    title="Cubic residual Newton stratum",
    status="STRUCTURAL",
    statement=(
        "At horizon k and deficit r with r+1 ≤ k, classify same-depth fibres "
        "of F_k at m = k-1-r by N2 visibility, N1 valuation, and the "
        "mismatched N0 quotient Q_{t,K,W}. This module does not claim a "
        "closed formula for M_k(x^3)."
    ),
    bt_relevance=(
        "Residuals are the section-calculus Mealy machine of bt.calculus. "
        "Packed prefixes are balanced-ternary words of length m."
    ),
    docs=(
        "docs/problems/residuals.md",
        "docs/theory/cubic_newton_stratum.md",
    ),
    lean=("formal/BTCalculus/NewtonStratum.lean",),
)
