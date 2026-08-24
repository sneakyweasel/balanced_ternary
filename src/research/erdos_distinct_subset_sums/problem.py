"""Descriptor for the Erdős distinct-subset-sums Phase-0 gate."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="erdos_distinct_subset_sums",
    title="Erdős distinct subset sums via balanced-signed relations",
    status="EXPLORATORY",
    statement=(
        "If A = {a_1, ..., a_n} subset {1, ..., N} has all 2^n subset sums "
        "distinct, Erdős conjectured N ≫ 2^n. Phase 0 asks whether canonical "
        "balanced-ternary normalization or v_3 of signed sums constrains "
        "sum-distinct sets beyond the elementary kernel R(A) = {0}, which "
        "Dubroff–Fox–Xu already use as coefficients in {-1,0,+1}^n."
    ),
    bt_relevance=(
        "Two subset sums agree iff a nontrivial ε in {-1,0,+1}^n has "
        "sum ε_i a_i = 0. The coefficient alphabet is the balanced-ternary "
        "digit alphabet. Canonical encode(s) of a signed sum is a complete "
        "invariant of the integer s, not a new constraint on A."
    ),
    docs=("docs/problems/erdos_distinct_subset_sums.md",),
)
