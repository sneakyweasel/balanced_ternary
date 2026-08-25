"""Descriptor for the frozen-engine aliquot-dynamics campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="aliquot_dynamics",
    title="Frozen Engine campaign: aliquot dynamics",
    status="EXPLORATORY",
    statement=(
        "What can frozen Research Engine v2 discover about the map "
        "A(n)=sigma(n)-n, including the open seed 276, when its existing "
        "affine-control machinery is given a genuinely arithmetic non-affine "
        "transition? This is not a Catalan–Dickson proof."
    ),
    bt_relevance=(
        "The campaign is an engine test on ordinary integer arithmetic. "
        "Balanced ternary is not required."
    ),
    docs=("docs/problems/aliquot_dynamics.md",),
    lean=("formal/Problems/Engine/AliquotDynamics.lean",),
)
