from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="sparse_polynomials",
    title="Mahler and factor experiments for P_n",
    status="EXPLORATORY",
    statement=(
        "Numerical Mahler measure and small cyclotomic factor scans of the "
        "signed ternary polynomial P_n. The polynomial representation itself "
        "remains in the core."
    ),
    bt_relevance="P_n is the generating polynomial of the balanced digits of n.",
    docs=(
        "docs/problems/sparse_polynomials.md",
        "docs/balanced_ternary_polynomials.md",
    ),
)
