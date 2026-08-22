from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="operator_dynamics",
    title="Compositions and orbits of balanced-ternary operators",
    status="EXPLORATORY",
    statement=(
        "Census of compositions and commutators of the core operators, plus "
        "OEIS-style sequence dossiers. Generic operator definitions remain "
        "in bt.operators."
    ),
    bt_relevance="All maps act on canonical balanced-ternary words or integers.",
    docs=(
        "docs/problems/operator_dynamics.md",
        "docs/operator_algebra.md",
    ),
)
