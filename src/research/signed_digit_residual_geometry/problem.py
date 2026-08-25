"""Descriptor for signed-digit residual geometry."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="signed_digit_residual_geometry",
    title="Signed-digit residual geometry",
    status="STRUCTURAL",
    statement=(
        "Inside the finite phase of F_{λ,U}(s,u)=λ·D(s+u), the origin-"
        "reachable set of the symmetric family U_m is the full interval "
        "[-⌊m/2⌋,⌊m/2⌋] at λ=1 and the even lattice 2ℤ∩[-2(m-1)_+,2(m-1)_+] "
        "at λ=2. Lattice-in-box fails for one-sided U, e.g. U={2}."
    ),
    bt_relevance=(
        "The step is the existing quotient D. Reachability is the orbit of "
        "0 under λ·D(s+u). No second digit model."
    ),
    docs=("docs/problems/signed_digit_residual_geometry.md",),
    lean=("formal/Problems/BalancedTernary/SignedDigitResidualGeometry.lean",),
)
