"""Descriptor for the v2.2 research target board."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="target_board",
    title="Research Engine v2.2 research target board",
    status="EXPLORATORY",
    statement=(
        "Can frozen Research Engine v2.2 enter a campaign with persistent "
        "research memory, grey loot, a ranked target portfolio, and prior-art "
        "maps, without adding attacks or contaminating blind discovery?"
    ),
    bt_relevance=(
        "The board is laboratory intelligence. Balanced ternary is not required. "
        "Digit-fold saturation remains a comparison cluster. Reverse-and-add "
        "in balanced ternary is a wildcard, not a core theorem programme."
    ),
    docs=("docs/problems/research_target_board.md",),
)
