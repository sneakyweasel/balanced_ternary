"""Descriptor for Research Engine v2.3 research strategy (Phases 1–2)."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="research_strategy",
    title="Research Engine v2.3 research strategy",
    status="EXPLORATORY",
    statement=(
        "Can frozen Research Engine v2.2 turn attack artifacts and research "
        "memory into ranked falsifiable hypotheses and opt-in chains, and can "
        "a generic inductive/ranking layer certify T(S)⊆S or V(T(x))<V(x) "
        "without adding flood attacks or claiming a universal theorem?"
    ),
    bt_relevance=(
        "The strategy and reasoning layers are engine infrastructure. "
        "Balanced ternary is not required. No new flood-order attack is added."
    ),
    docs=("docs/problems/research_strategy.md",),
)
