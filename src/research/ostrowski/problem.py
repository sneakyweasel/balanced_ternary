"""Descriptor for the order-(m) Ostrowski-adder Phase-0 gate."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="ostrowski_order_m_adder",
    title="Generalized Ostrowski order-(m) adder",
    status="EXPLORATORY",
    statement=(
        "Baranwal’s thesis §5.3 proposes an adder for an order-m "
        "Gamma-numeration system with m-dimensional states. Phase 0 "
        "asks whether the unread-tail residual of a genuine order-3 "
        "Gamma lives in a finite box, analogously to Theorem 2.2. "
        "The quadratic Ostrowski adder is already known and is only "
        "a regression."
    ),
    bt_relevance=(
        "The rewrite-calculus theorem add_not_DLocal isolates the LSD "
        "carry as the missing state for D(x+y). The Ostrowski question "
        "is whether a higher-dimensional unread-tail residual plays "
        "the same role. The systems are not identified."
    ),
    docs=("docs/problems/ostrowski_order_m_adder.md",),
)
