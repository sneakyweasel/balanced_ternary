"""Descriptor for the frozen-engine encoded word-rewrite wildcard campaign."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="cyclic_tag_bit",
    title="Frozen Engine campaign: encoded binary-word rewrite",
    status="EXPLORATORY",
    statement=(
        "On the stored 0|->0, 1|->11 rewrite with halt on empty, does frozen v2.3 "
        "diagnose a representation mismatch for an integer encoding of words, "
        "without a new rewrite attack and without a universality claim?"
    ),
    bt_relevance="Not required. Binary words encoded as integers.",
    docs=("docs/problems/cyclic_tag_bit.md",),
    lean=("formal/Problems/Engine/CyclicTag.lean",),
)
