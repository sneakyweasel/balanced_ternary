"""Descriptor for the frozen-engine BB-5 generalized Collatz map campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="bb5_map",
    title="Frozen Engine campaign: BB-5 generalized Collatz map",
    status="EXPLORATORY",
    statement=(
        "Can frozen Research Engine v2 independently reconstruct the residue-"
        "controlled affine language of the BB-5 generalized Collatz map from "
        "the exact partial transition, then derive any exact constraint beyond "
        "rediscovery of the definition? This is not a BB-5 or Collatz proof."
    ),
    bt_relevance=(
        "The campaign is an engine test on an ordinary integer partial map. "
        "Balanced ternary is not required."
    ),
    docs=("docs/problems/bb5_map.md",),
    lean=("formal/Problems/Engine/BB5Map.lean",),
)
