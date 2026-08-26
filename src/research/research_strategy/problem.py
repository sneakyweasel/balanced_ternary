"""Descriptor for Research Engine v2.3 Phase 1 research strategy."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="research_strategy",
    title="Research Engine v2.3 Phase 1 research strategy",
    status="EXPLORATORY",
    statement=(
        "Can frozen Research Engine v2.2 turn attack artifacts and research "
        "memory into ranked falsifiable hypotheses, proof obligations, and "
        "opt-in attack chains without adding attacks or changing default "
        "planner reports?"
    ),
    bt_relevance=(
        "The strategy layer is engine infrastructure. Balanced ternary is not "
        "required. No new attack is added."
    ),
    docs=("docs/problems/research_strategy.md",),
)
