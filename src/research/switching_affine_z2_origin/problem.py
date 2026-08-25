"""Descriptor for the frozen-engine two-path Z^2 campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="switching_affine_z2_origin",
    title="Frozen Engine campaign: switching affine Z^2 origin",
    status="EXPLORATORY",
    statement=(
        "What exact origin-reachability, avoidance, or class obstruction can "
        "frozen Research Engine v2 derive from the stored two-path integer loop "
        "on Z^2, without new attacks?"
    ),
    bt_relevance="Not required. The campaign is an engine test on a 2-D switching affine map.",
    docs=("docs/problems/switching_affine_z2_origin.md",),
    lean=("formal/Problems/Engine/TwoPathZ2.lean",),
)
