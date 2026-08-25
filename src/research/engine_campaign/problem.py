"""Descriptor for the Research Engine v2 real-problem campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="engine_campaign",
    title="Research Engine v2 first real-problem campaign",
    status="EXPLORATORY",
    statement=(
        "Can the same v2 diagnosis loop recover exact structure across "
        "parameterized mx+r maps, accelerated 5x+1, Euclidean remainder "
        "dynamics, and a ResearchLoop-selected fourth target?"
    ),
    bt_relevance=(
        "The campaign is an engine test. Balanced ternary is not required. "
        "The saturated digit-fold family remains a comparison cluster."
    ),
    docs=("docs/problems/engine_campaign.md",),
    lean=("formal/Problems/Engine/MxPlusR.lean",),
)
