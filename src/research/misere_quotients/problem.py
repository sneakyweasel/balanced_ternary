"""Descriptor for the misere-quotient finite-context gate."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="misere_quotients",
    title="Finite-context signatures and misere quotients",
    status="ARCHIVED",
    statement=(
        "Finite-context signatures, distinguishing contexts, and candidate "
        "monoid audits reproduce the classical Plambeck–Siegel "
        "indistinguishability congruence on octal 0.123 and the published "
        "single-heap outcomes of Q_33(0.07). They do not supply a new "
        "quotient construction, finite-context completeness theorem, or "
        "reduction of the Q_34 question."
    ),
    bt_relevance=(
        "Balanced-ternary arithmetic is not a representation of misere "
        "positions. Only the laboratory methodology transfers: finite "
        "signatures, shortest witnesses, and behavioural quotienting. "
        "In misere theory those objects are already the definition of "
        "the indistinguishability congruence."
    ),
    docs=("docs/problems/misere_quotients.md",),
)
