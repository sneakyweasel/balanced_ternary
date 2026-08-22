"""Copy this package to add a new research problem without editing bt.*."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="template",
    title="New open problem",
    status="EXPLORATORY",
    statement="Replace with the exact statement.",
    bt_relevance="Why balanced ternary is a relevant representation.",
    docs=("docs/problems/TEMPLATE.md",),
)
