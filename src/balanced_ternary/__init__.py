"""Public API for balanced ternary representation, arithmetic, and invariants."""

from balanced_ternary.arithmetic import factorize, format_factorization, is_prime
from balanced_ternary.features import (
    ZeroGapStatistics,
    RunStatistics,
    negative_digit_count,
    position_class_sums,
    positive_digit_count,
    run_statistics,
    signed_digit_sum,
    weight,
    zero_count,
    zero_gap_statistics,
)
from balanced_ternary.invariants import (
    automaton_residue,
    lsd_nonzero_index,
    v3,
    verify_invariants,
)
from balanced_ternary.representation import (
    BalancedTernary,
    decode,
    digits,
    encode,
    is_canonical,
    normalize,
)

__all__ = [
    "BalancedTernary",
    "RunStatistics",
    "ZeroGapStatistics",
    "automaton_residue",
    "decode",
    "digits",
    "encode",
    "factorize",
    "format_factorization",
    "is_canonical",
    "is_prime",
    "lsd_nonzero_index",
    "negative_digit_count",
    "normalize",
    "position_class_sums",
    "positive_digit_count",
    "run_statistics",
    "signed_digit_sum",
    "v3",
    "verify_invariants",
    "weight",
    "zero_count",
    "zero_gap_statistics",
]
