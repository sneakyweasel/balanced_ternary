"""Descriptor for matrix-word recursive invariant experiment."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="matrix_word_invariant",
    title="Matrix-word recursive invariants for vector class obstructions",
    status="EXPLORATORY",
    statement=(
        "Can v2 discover a recursive arithmetic invariant of matrix-word "
        "composition that proves (M(u)-I)x = -c(u) has no integer solution "
        "for an infinite control class when magnitude domination is "
        "inapplicable?"
    ),
    bt_relevance="None required.",
    docs=("docs/problems/matrix_word_invariant.md",),
    lean=("formal/Problems/Engine/MatrixWord.lean",),
)
