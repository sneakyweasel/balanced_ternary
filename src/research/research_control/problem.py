"""Descriptor for Research Engine v2.4 research-control layer."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="research_engine_v24",
    title="Research Engine v2.4 research-control layer",
    status="EXPLORATORY",
    statement=(
        "Can frozen Research Engine v2.3 be wrapped in a control layer that "
        "preserves an immutable baseline, classifies CLOSE without implying "
        "resolution, emits exactly three non-executable next-attack proposals, "
        "and replays selected v2.2 targets in isolation?"
    ),
    bt_relevance=(
        "The control layer is engine infrastructure. Balanced ternary is not "
        "required. No new executable attack is added."
    ),
    docs=("docs/problems/research_engine_v24.md",),
)
