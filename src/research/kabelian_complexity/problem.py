"""Descriptor for the k-abelian residual-signature Phase-0 gate."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="kabelian_complexity",
    title="k-abelian complexity residual signatures of automatic sequences",
    status="ARCHIVED",
    statement=(
        "The k-abelian class of a factor is exactly the Karhumäki–Saarela–"
        "Zamboni triple (prefix of length k-1, suffix of length k-1, length-k "
        "Parikh vector). Raw signatures are unbounded. A finite n-independent "
        "class residual therefore cannot be the mechanism of b-regular "
        "complexity whenever ρ_k^{ab} is unbounded. The classical mechanism "
        "is k-block coding plus abelian complexity, already in the 2015–2025 "
        "literature. The general regularity conjecture remains open and is "
        "not attacked here."
    ),
    bt_relevance=(
        "Base-3 automatic sequences such as the Cantor sequence are a natural "
        "test for the laboratory, but Phase 0 uses ordinary unsigned digits. "
        "A balanced-trit address of the same sequence is a coordinate change "
        "and was not opened."
    ),
    docs=("docs/problems/kabelian_complexity.md",),
    conjectures=("kabelian_regularity_automatic",),
)
