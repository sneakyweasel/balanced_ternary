"""Descriptor for the frozen-engine factor-concatenation wildcard campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="home_prime_49",
    title="Frozen Engine campaign: factor-concatenation map",
    status="EXPLORATORY",
    statement=(
        "On the stored factorization-concatenation map, does frozen v2.3 diagnose "
        "a regime that recurs the non-affine arithmetic cluster, without a new "
        "concatenation attack and without claiming that seed 49 reaches a prime?"
    ),
    bt_relevance="Not required. Ordinary positive integers and decimal concatenation.",
    docs=("docs/problems/home_prime_49.md",),
    lean=("formal/Problems/Engine/FactorConcat.lean",),
)
