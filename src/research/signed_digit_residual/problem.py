"""Descriptor for signed-digit residual phase transitions."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="signed_digit_residual",
    title="Signed-digit residual phase transitions",
    status="STRUCTURAL",
    statement=(
        "For F_{λ,U}(s,u)=λ·D(s+u) with finite raw alphabet U, the "
        "origin-reachable residual of the family U_m={-m,...,m} and "
        "λ∈{1,2,3} is finite if and only if λ≤2 or m≤1. r-way trit "
        "addition has exact residual size M(r)=2⌊r/2⌋+1."
    ),
    bt_relevance=(
        "The step is the existing quotient D=(n-lsd(n))/3. Doubled-trit "
        "normalization and D(x+y) streaming are special alphabets of the "
        "same residual map. The adapter does not introduce a second digit "
        "model."
    ),
    docs=("docs/problems/signed_digit_residual.md",),
    lean=("formal/Problems/BalancedTernary/SignedDigitResidual.lean",),
)
