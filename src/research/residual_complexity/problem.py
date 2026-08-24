"""Descriptor for the unrestricted residual-complexity triage branch."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="residual_complexity",
    title="Two-parameter unrestricted residual complexity C_F(m,r)",
    status="STRUCTURAL",
    statement=(
        "For F in Z[x], write C_F(m,r) for the number of distinct "
        "remaining-horizon-r right-language types among unrestricted "
        "residuals of F after input depth m. The identity is constantly 1 "
        "and the x^2 band r>=m-1 is exact. The interior 0<r<m-1 is the "
        "image size of p |-> (p mod 3^r, DZ^m(p^2) mod 3^r); the zero "
        "fibre is quadratic residues at m=2r and full for m>=3r, while "
        "a closed m_0(r) for every fibre is not claimed."
    ),
    bt_relevance=(
        "Types are the existing residual Mealy right languages of "
        "bt.calculus, distinguished by finite-horizon equivalence ≡_r, "
        "not a safety product and not a manufactured remaining-horizon "
        "clock."
    ),
    docs=("docs/problems/residual_complexity.md",),
)
