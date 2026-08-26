"""Descriptor for the frozen-engine 5x-4 strip campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="weak_collatz_floor_5x4_rplus",
    title="Frozen Engine campaign: 5x-4 one-variable strip",
    status="EXPLORATORY",
    statement=(
        "On the hint-free strip 5x-4 <= 4x' <= 5x-1 with x >= 2, does frozen "
        "v2.3 recover a class or branch obstruction relevant to losing the "
        "successor, without new attacks and without rediscovering the 4/3 SLC "
        "language as the yield?"
    ),
    bt_relevance="Not required. Ordinary integer arithmetic.",
    docs=("docs/problems/weak_collatz_floor_5x4_rplus.md",),
    lean=("formal/Problems/Engine/LinearConstraintLoops.lean",),
)
