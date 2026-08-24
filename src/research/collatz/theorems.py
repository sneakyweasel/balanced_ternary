"""Layer A: exact balanced ternary form of ``3n+1``.

**PROVED** for every integer ``n != 0``:

    BT(3n+1) = BT(n)  followed by a trailing ``+``.

Proof: multiplication by 3 appends a trailing ``0`` (new LSD is ``0``).
Adding ``+1`` to LSD ``0`` yields ``+`` and produces no carry, so the digits
of ``n`` are unchanged and a new least-significant digit ``+1`` is attached.

Exception: ``n = 0``. Then ``3*0+1 = 1`` and ``BT(1) = +``, not ``0+``.
Collatz states are positive odd, so the exception does not arise.

The adder in ``bt.arithmetic`` remains an independent check, not the
definition of this identity.

Closed-form feature map ``n -> 3n+1`` (PROVED, extra LSD ``a_0 = +1`` and
index shift ``a'_{i+1} = a_i``):

- length +1
- weight +1 (parity flips)
- signed digit sum +1
- positive count +1; negative and zero counts unchanged
- position-class sums, period t:
      S_0(y) = 1 + S_{t-1}(n)
      S_j(y) = S_{j-1}(n)   for j = 1, ..., t-1
"""

from __future__ import annotations

from bt.representation import (
    BalancedTernary,
    WordLike,
    decode,
    encode,
    normalize,
)
from bt.arithmetic import three_n_plus_one_word
from research.collatz.features import BalancedTernaryFeatures, extract_features


def append_plus(word: WordLike) -> BalancedTernary:
    """Concatenate a trailing ``+`` (new LSD ``+1``).

    Raises ``ValueError`` on the zero word: that is the unique exception
    to ``BT(3n+1) = BT(n)+``.
    """
    canonical = normalize(word)
    if canonical.word() == "0":
        raise ValueError(
            "append_plus is undefined for 0: BT(1) = '+' not '0+'"
        )
    return BalancedTernary(canonical.digits_msd + (1,))


def three_n_plus_one_from_word(word: WordLike) -> BalancedTernary:
    """``BT(3n+1)`` by the append-plus theorem. ``n = 0`` uses ``encode(1)``."""
    canonical = normalize(word)
    if canonical.word() == "0":
        return encode(1)
    return append_plus(canonical)


def shift_position_class_sums(
    sums: tuple[int, ...], new_lsd: int = 1
) -> tuple[int, ...]:
    """Position-class sums after prepending LSD ``new_lsd`` (index shift by 1)."""
    t = len(sums)
    if t < 1:
        raise ValueError("position-class tuple must be non-empty")
    s0 = new_lsd + sums[t - 1]
    rest = tuple(sums[j - 1] for j in range(1, t))
    return (s0,) + rest


def predicted_features_after_append_plus(word: WordLike) -> BalancedTernaryFeatures:
    """Closed-form features of ``BT(n)+`` for ``n != 0``."""
    src = extract_features(word)
    new_word = append_plus(word)
    runs = extract_features(new_word)
    predicted = BalancedTernaryFeatures(
        length=src.length + 1,
        weight=src.weight + 1,
        weight_parity=(src.weight + 1) % 2,
        signed_digit_sum=src.signed_digit_sum + 1,
        positive_digit_count=src.positive_digit_count + 1,
        negative_digit_count=src.negative_digit_count,
        zero_count=src.zero_count,
        number_of_runs=runs.number_of_runs,
        max_run_length=runs.max_run_length,
        max_zero_run=runs.max_zero_run,
        zero_run_lengths=runs.zero_run_lengths,
        nonzero_run_lengths=runs.nonzero_run_lengths,
        gaps_between_nonzero=runs.gaps_between_nonzero,
        position_class_sums_period_2=shift_position_class_sums(
            src.position_class_sums_period_2
        ),
        position_class_sums_period_3=shift_position_class_sums(
            src.position_class_sums_period_3
        ),
    )
    return predicted


def append_plus_matches_integer(n: int) -> bool:
    """``append_plus(BT(n)) == encode(3n+1)`` for ``n != 0``."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n == 0:
        return False
    word = encode(n)
    got = append_plus(word)
    return got == encode(3 * n + 1) and decode(got) == 3 * n + 1


def append_plus_agrees_with_adder(n: int) -> bool:
    """Append-plus agrees with shift-then-add-one for ``n != 0``."""
    if n == 0:
        return False
    word = encode(n)
    return append_plus(word) == three_n_plus_one_word(word)
