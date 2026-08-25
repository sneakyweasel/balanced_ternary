"""Descriptor for the frozen-engine companion-window / Skolem campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="skolem_lrs",
    title="Frozen Engine campaign: open order-6 Skolem instance",
    status="EXPLORATORY",
    statement=(
        "What can frozen Research Engine v2 discover about first-coordinate "
        "vanishing for an exact companion-matrix iteration in Z^6, including "
        "the unresolved order-6 integer LRS of the 2026 Skolem survey, "
        "without new attacks? This is not a Skolem decision procedure."
    ),
    bt_relevance=(
        "The campaign is an engine test on integer linear recurrences. "
        "Balanced ternary is not required."
    ),
    docs=("docs/problems/skolem_lrs.md",),
    lean=("formal/Problems/Engine/CompanionShift.lean",),
)
