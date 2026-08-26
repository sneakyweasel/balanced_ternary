"""Descriptor for the frozen-engine reverse-plus-add wildcard campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="reverse_and_add_base3",
    title="Frozen Engine campaign: balanced-ternary reverse-plus-add",
    status="EXPLORATORY",
    statement=(
        "On the stored balanced-ternary reverse-plus-add map, does frozen v2.3 "
        "diagnose a regime distinct from digit-fold saturation and from "
        "factorization or floor-power iteration, without a new reverse-add "
        "attack and without claiming that every seed reaches a reverse-fixed point?"
    ),
    bt_relevance="Uses the existing core digit reverse; the map is not a solving coordinate.",
    docs=("docs/problems/reverse_and_add_base3.md",),
    lean=("formal/Problems/Engine/ReverseAdd.lean",),
)
