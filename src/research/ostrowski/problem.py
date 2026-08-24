"""Descriptor for the order-(m) Ostrowski-adder Phase-0 gate."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="ostrowski_order_m_adder",
    title="Generalized Ostrowski order-(m) adder",
    status="STRUCTURAL",
    statement=(
        "For the genuine order-3 Gamma=([0;2-bar],[0;1-bar],[0;1-bar]), "
        "the live unread-tail residuals form an explicit 55-element "
        "forward-invariant set B_MIN. The comparison Gamma=([0;2-bar],"
        "[0;1-bar],[0;3-bar]) is an irreducible Perron non-Pisot cubic "
        "with the same digit alphabets; its live union grows in every "
        "scan window, but unbounded live paths are not proved. Reverse "
        "contraction of A^{-1} is certified in a Q-norm and makes the "
        "basin of the origin finite (9164 states); that basin is not "
        "the adder live set. The non-Pisot accepting boundary is "
        "K_0 = {s3=0} and the E_n-slabs K_n, with an explicit unbounded "
        "family on F. That does not decide whether the live set from "
        "the origin is finite. Pisot existence of some adder is known."
    ),
    bt_relevance=(
        "The rewrite-calculus theorem add_not_DLocal isolates the LSD "
        "carry as the missing state for D(x+y). The Ostrowski question "
        "is whether a higher-dimensional unread-tail residual plays "
        "the same role. The systems are not identified."
    ),
    docs=("docs/problems/ostrowski_order_m_adder.md",),
)
