"""Descriptor for the frozen-engine 7x+1 class-obstruction campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="mx_plus_r_7x1_class_obstruction",
    title="Frozen Engine campaign: 7x+1 class obstruction",
    status="EXPLORATORY",
    statement=(
        "Does the exact residue/valuation control of T(x)=(7x+1)/2^{v_2(7x+1)} "
        "induce a nontrivial class obstruction relevant to reaching 1, without "
        "new attacks and without rediscovering the generic mx+r family as yield?"
    ),
    bt_relevance="Not required. Ordinary integer arithmetic on odd positives.",
    docs=("docs/problems/mx_plus_r_7x1_class_obstruction.md",),
    lean=("formal/Problems/Engine/MxPlusR.lean",),
)
