"""Descriptor for the unrestricted residual-complexity triage branch."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="residual_complexity",
    title="Two-parameter unrestricted residual complexity C_F(m,r)",
    status="STRUCTURAL",
    statement=(
        "For F in Z[x], write C_F(m,r) for the number of distinct "
        "remaining-horizon-r right-language types among unrestricted "
        "residuals of F after input depth m. Decide whether C_F(m,r) "
        "has an exact two-parameter law for F(x)=x and F(x)=x^2, or a "
        "proved obstruction that the census is not a remaining-horizon "
        "clock and not a closed low-degree formula."
    ),
    bt_relevance=(
        "Types are the existing residual Mealy right languages of "
        "bt.calculus, distinguished by finite-horizon equivalence ≡_r, "
        "not a safety product and not a manufactured remaining-horizon "
        "clock."
    ),
    docs=("docs/problems/residual_complexity.md",),
)
