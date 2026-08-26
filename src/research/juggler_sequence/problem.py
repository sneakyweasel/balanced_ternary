"""Descriptor for the frozen-engine floor-power wildcard campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="juggler_sequence",
    title="Frozen Engine campaign: even/odd floor-power map",
    status="EXPLORATORY",
    statement=(
        "On the stored even/odd floor-power map, does frozen v2.3 diagnose a "
        "regime distinct from residue-affine control and from divisor-sum "
        "iteration, without a new radical attack and without claiming that "
        "every positive seed reaches 1?"
    ),
    bt_relevance="Not required. Ordinary positive integers.",
    docs=("docs/problems/juggler_sequence.md",),
    lean=("formal/Problems/Engine/FloorPower.lean",),
)
