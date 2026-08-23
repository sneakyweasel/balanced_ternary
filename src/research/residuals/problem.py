"""Descriptor for cubic residual Newton-stratum research."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="residuals",
    title="Cubic residual Newton stratum",
    status="STRUCTURAL",
    statement=(
        "At horizon k and deficit r with r+1 ≤ k, count same-depth Newton "
        "classes C_{k,k-1-r} by the easy/core split and the unexhausted "
        "zero-fibre formula. M_k(x^3) is the N3-gated union of those "
        "images. No single closed term for M_k is claimed."
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
