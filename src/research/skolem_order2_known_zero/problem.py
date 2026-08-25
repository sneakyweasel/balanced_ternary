"""Descriptor for the frozen-engine order-2 companion competence check."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="skolem_order2_known_zero",
    title="Frozen Engine campaign: order-2 companion known zero",
    status="EXPLORATORY",
    statement=(
        "Does frozen Research Engine v2 certify the declared order-2 "
        "first-coordinate zero and recover the 2-D companion, without a "
        "new attack? This is a competence check, not a Skolem decision."
    ),
    bt_relevance="Not required. The campaign is an engine competence check.",
    docs=("docs/problems/skolem_order2_known_zero.md",),
    lean=("formal/Problems/Engine/CompanionShift.lean",),
)
