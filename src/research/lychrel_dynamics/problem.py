"""Thin laboratory descriptor for Lychrel / Reverse-and-Add dynamics."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="lychrel_dynamics",
    title="Lychrel / Reverse-and-Add dynamics",
    status="EXPLORATORY",
    statement=(
        "For integer bases b>=2, does repeated Reverse-and-Add "
        "R_b(n)=n+rev_b(n) always reach a base-b palindrome, or does there "
        "exist n>0 whose trajectory never does? Canonical instance b=10; "
        "secondary instance b=3; balanced-ternary digits are an exploratory "
        "representation branch. This is problem registration only."
    ),
    bt_relevance=(
        "Optional signed/balanced ternary is an exploratory representation "
        "question, not a claim that balanced ternary solves Lychrel. Distinct "
        "from the closed reverse_and_add_base3 campaign on n+W(n)."
    ),
    docs=("docs/problems/lychrel_dynamics.md",),
)
