"""Descriptor for the frozen-engine order-6 vanishing-class campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="companion_shift_order6_zero_class",
    title="Frozen Engine campaign: order-6 vanishing class constraint",
    status="EXPLORATORY",
    statement=(
        "On the declared order-6 companion window, can frozen v2.3 recover a "
        "lattice/gcd or matrix-word congruence constraint on vanishing indices, "
        "without new attacks, without interpolants, and without claiming that "
        "a zero does not exist?"
    ),
    bt_relevance="Not required. Ordinary integer companion windows.",
    docs=("docs/problems/companion_shift_order6_zero_class.md",),
    lean=("formal/Problems/Engine/CompanionShift.lean",),
)
