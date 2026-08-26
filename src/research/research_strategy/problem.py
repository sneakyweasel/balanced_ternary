"""Descriptor for Research Engine v2.3 research strategy (Phases 1–3)."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="research_strategy",
    title="Research Engine v2.3 research strategy",
    status="EXPLORATORY",
    statement=(
        "Can frozen Research Engine v2.2 turn attack artifacts into ranked "
        "hypotheses and opt-in chains, certify inductive/ranking structure, "
        "and separate affine laws from truncated domains without adding flood "
        "attacks or completing the parked involution census?"
    ),
    bt_relevance=(
        "The strategy, reasoning, and law layers are engine infrastructure. "
        "Balanced ternary is not required. No new flood-order attack is added."
    ),
    docs=("docs/problems/research_strategy.md",),
)
