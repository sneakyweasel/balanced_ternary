"""Descriptor for the Euclidean remainder campaign adapter."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="euclidean_quotient",
    title="Euclidean remainder dynamics as a v2 latent-control transfer test",
    status="EXPLORATORY",
    statement=(
        "Can Research Engine v2 discover latent quotient control and "
        "affine matrix branches from (a,b)↦(b, a mod b) without being "
        "told the quotient?"
    ),
    bt_relevance="None required. Ordinary integer arithmetic.",
    docs=("docs/problems/engine_campaign.md",),
)
