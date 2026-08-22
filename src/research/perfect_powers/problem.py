from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="perfect_powers",
    title="Sparse balanced-ternary perfect powers",
    status="EXPLORATORY",
    statement=(
        "Locate squares and cubes whose canonical balanced-ternary weight "
        "is small, and record the exact W_1 square classification."
    ),
    bt_relevance="Sparsity is measured by balanced-ternary Hamming weight.",
    docs=("docs/problems/perfect_powers.md",),
)
