"""Descriptor for Research Engine v2.2 research memory."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="engine_memory",
    title="Research Engine v2.2 research memory",
    status="EXPLORATORY",
    statement=(
        "Can frozen Research Engine v2 turn accumulated successes, failures, "
        "counterexamples, and prior-art findings into persistent research "
        "knowledge that improves target selection without contaminating blind "
        "mathematical discovery?"
    ),
    bt_relevance=(
        "The memory layer is engine infrastructure. Balanced ternary is not "
        "required. No new attack is added."
    ),
    docs=("docs/problems/engine_memory.md",),
)
