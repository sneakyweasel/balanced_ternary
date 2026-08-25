"""Descriptor for the vector-affine latent-control engine experiment."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="vector_affine",
    title="Generic vector-affine latent control for Research Engine v2",
    status="EXPLORATORY",
    statement=(
        "Can v2 discover, certify, compose, and obstruct hidden "
        "y = A_u x + b_u dynamics on Z^d (d≥2), and does that language "
        "transfer to Euclidean remainder dynamics and an unrelated "
        "2-D lattice map?"
    ),
    bt_relevance="None required. Digit-fold cores are comparison only.",
    docs=("docs/problems/vector_affine.md",),
    lean=("formal/Problems/Engine/VectorAffine.lean",),
)
