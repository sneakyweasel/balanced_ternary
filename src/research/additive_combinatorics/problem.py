from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="additive_combinatorics",
    title="Digit-restricted balanced-ternary sumsets",
    status="EXPLORATORY",
    statement=(
        "Describe sumsets and difference sets of the digit-restricted families "
        "A_k, B_k, C_k and the associated additive energy."
    ),
    bt_relevance="The sets are defined by restricted balanced-ternary digits.",
    docs=(
        "docs/problems/additive_combinatorics.md",
        "docs/balanced_ternary_additive_combinatorics.md",
    ),
)
