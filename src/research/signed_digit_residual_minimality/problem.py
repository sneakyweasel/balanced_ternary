"""Descriptor for signed-digit residual minimality."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="signed_digit_residual_minimality",
    title="Signed-digit residual minimality",
    status="STRUCTURAL",
    statement=(
        "If λ is not divisible by 3 and U is nonempty, distinct integer "
        "residuals of F_{λ,U}(s,u)=λ·D(s+u) with output lsd(s+u) are "
        "separated by a constant word of length v_3(s-t)+1. Hence M=|R| "
        "on every origin-reachable finite machine in this regime. At λ=3, "
        "translation by 3 is a global behavioral symmetry, but it is not "
        "origin-reachable when max|u|≤1."
    ),
    bt_relevance=(
        "The output is existing lsd; the 3-adic drop is the unique trit "
        "residue. No second digit model."
    ),
    docs=("docs/problems/signed_digit_residual_minimality.md",),
    lean=("formal/Problems/BalancedTernary/SignedDigitResidualMinimality.lean",),
)
