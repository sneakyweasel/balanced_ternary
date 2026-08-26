"""Descriptor for Research Engine v2.3 research strategy (Phases 1–4)."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="research_strategy",
    title="Research Engine v2.3 research strategy",
    status="EXPLORATORY",
    statement=(
        "Can frozen Research Engine v2.2 turn attack artifacts into ranked "
        "hypotheses and opt-in chains, certify inductive/ranking structure, "
        "separate affine laws from truncated domains, and keep EXISTS_PATH "
        "distinct from ALL_PATHS on legal_controls-as-relation — without adding "
        "flood attacks, overlapping-domain census, or a nondeterministic SLC solver?"
    ),
    bt_relevance=(
        "The strategy, reasoning, law, and quantifier layers are engine "
        "infrastructure. Balanced ternary is not required. No new flood-order "
        "attack is added."
    ),
    docs=("docs/problems/research_strategy.md",),
)
