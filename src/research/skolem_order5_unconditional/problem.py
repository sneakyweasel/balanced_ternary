"""Descriptor for the frozen-engine order-5 companion campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="skolem_order5_unconditional",
    title="Frozen Engine campaign: order-5 companion vanishing",
    status="EXPLORATORY",
    statement=(
        "On a declared order-5 companion window, can frozen v2.3 do more than "
        "exhaust a finite prefix, without interpolants, without un-skipping "
        "matrix-word, and without claiming an unconditional order-5 decision "
        "procedure?"
    ),
    bt_relevance="Not required. Ordinary integer companion windows.",
    docs=("docs/problems/skolem_order5_unconditional.md",),
    lean=("formal/Problems/Engine/CompanionShift.lean",),
)
