"""Descriptor for the frozen-engine linear-constraint-loop campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="linear_constraint_loops",
    title="Frozen Engine campaign: one-variable linear-constraint loops",
    status="EXPLORATORY",
    statement=(
        "Can frozen Research Engine v2 independently reconstruct useful "
        "arithmetic structure from exact one-variable linear-constraint "
        "loops, then certify termination or cycle constraints short of "
        "the open generalized-Collatz barrier?"
    ),
    bt_relevance=(
        "The campaign is an engine test on ordinary integer loops. "
        "Balanced ternary is not required."
    ),
    docs=("docs/problems/linear_constraint_loops.md",),
    lean=("formal/Problems/Engine/LinearConstraintLoops.lean",),
)
