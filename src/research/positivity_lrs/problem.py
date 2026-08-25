"""Descriptor for the frozen-engine companion-window / Positivity campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="positivity_lrs",
    title="Frozen Engine campaign: open order-10 LRS Positivity instance",
    status="EXPLORATORY",
    statement=(
        "What can frozen Research Engine v2, augmented only by v2.2 research "
        "memory, discover about first-coordinate nonnegativity for an exact "
        "companion-matrix iteration in Z^10, including the unresolved order-10 "
        "integer LRS of the 2026 Skolem/Positivity survey, without new attacks? "
        "This is not a Positivity decision procedure."
    ),
    bt_relevance=(
        "The campaign is an engine test on integer linear recurrences. "
        "Balanced ternary is not required."
    ),
    docs=("docs/problems/positivity_lrs.md",),
    lean=("formal/Problems/Engine/CompanionObservation.lean",),
)
