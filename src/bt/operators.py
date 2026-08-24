"""First-class balanced-ternary operators.

Integer-level maps and word-level maps are distinct callables. Passing a
word to :meth:`BTOperator.apply` or an integer to :meth:`BTOperator.apply_word`
is a type error at the call site: the two methods do not share a signature.

Canonical conventions (MSD display, LSD mathematics) are those of
:mod:`bt.representation`. Collatz is not used here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from bt.metrics import (
    negative_digit_count,
    position_class_sums,
    positive_digit_count,
    signed_digit_sum,
    v3,
    weight,
    zero_count,
)
from bt.sequences import bt_reverse, bt_reverse_tail, bt_reverse_zeros
from bt.support import gap_sequence, support
from bt.representation import (
    BalancedTernary,
    WordLike,
    decode,
    digits,
    encode,
    from_digits_lsd,
    normalize,
)


class OperatorDomainError(ValueError):
    """The integer or word is outside the operator's domain."""


class Level(str, Enum):
    """Which kind of object an operator transforms."""

    INTEGER = "integer"
    WORD = "word"


def _require_int(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"{name} must be int, got {type(n).__name__}")
    return n


def lsd_digit(n: int) -> int:
    """Least-significant balanced digit ``a_0 in {-1, 0, +1}``.

    This is ``n`` reduced into ``{-1, 0, +1}`` modulo 3, not ``n % 3`` in
    ``{0, 1, 2}``.
    """
    n = _require_int(n)
    r = n % 3
    return -1 if r == 2 else r


def balanced_quotient(n: int) -> int:
    """``(n - a_0) / 3``. Not ordinary floor division by 3.

    Counterexamples to ``D(n) = n // 3``: ``D(2) = 1`` while ``2 // 3 = 0``;
    ``D(-1) = 0`` while ``(-1) // 3 = -1``.
    """
    n = _require_int(n)
    return (n - lsd_digit(n)) // 3


def digit_derivative(n: int) -> int:
    """Integer-level ``D``: drop the least-significant balanced digit."""
    return balanced_quotient(n)


def multiply_by_3(n: int) -> int:
    return 3 * _require_int(n)


def multiply_by_3_pow(n: int, k: int) -> int:
    k = _require_int(k, "k")
    if k < 0:
        raise ValueError(f"k must be >= 0, got {k}")
    return _require_int(n) * (3**k)


def shift_left(word: WordLike, k: int = 1) -> BalancedTernary:
    """Append ``k`` trailing zeros (new LSDs). Canonical ``0`` stays ``0``."""
    k = _require_int(k, "k")
    if k < 0:
        raise ValueError(f"k must be >= 0, got {k}")
    canonical = normalize(word)
    if canonical.word() == "0" or k == 0:
        return canonical
    return from_digits_lsd((0,) * k + digits(canonical))


def drop_lsd_word(word: WordLike) -> BalancedTernary:
    """Word-level ``D``: drop ``a_0``. The zero word stays ``0``."""
    lsd = digits(normalize(word))
    if len(lsd) == 1:
        return BalancedTernary((0,))
    return from_digits_lsd(lsd[1:])


def negate_word(word: WordLike) -> BalancedTernary:
    return -normalize(word)


def reverse_word(word: WordLike) -> BalancedTernary:
    """Canonical reverse (OEIS A134028 word form)."""
    canonical = normalize(word)
    if canonical.word() == "0":
        return canonical
    return BalancedTernary(tuple(reversed(canonical.digits_msd)))


def reverse_zeros_word(word: WordLike) -> BalancedTernary:
    """Reverse leaving trailing zeros (A160652 word form)."""
    n = decode(word)
    return encode(bt_reverse_zeros(n))


def reverse_tail_word(word: WordLike) -> BalancedTernary:
    """Reverse every digit except the MSD (A351702 word form)."""
    n = decode(word)
    return encode(bt_reverse_tail(n))


def prepend_lsd_word(word: WordLike, digit: int) -> BalancedTernary:
    """Digit integral of one step: new LSD ``digit in {-1,0,+1}``."""
    if digit not in (-1, 0, 1):
        raise ValueError(f"digit must be in {{-1,0,+1}}, got {digit!r}")
    canonical = normalize(word)
    if canonical.word() == "0":
        return from_digits_lsd((digit,))
    return from_digits_lsd((digit,) + digits(canonical))


def three_kernel(n: int) -> int:
    """Strip all factors of 3: ``n / 3^{v_3(n)}`` (``0`` stays ``0``)."""
    n = _require_int(n)
    if n == 0:
        return 0
    val = v3(n)
    assert val is not None
    return n // (3**val)


def shift_feature_effects(n: int) -> dict[str, int | tuple[int, ...]]:
    """Exact feature change under ``S(n) = 3n``."""
    n = _require_int(n)
    src = encode(n)
    dst = encode(3 * n)
    return {
        "length_src": len(src),
        "length_dst": len(dst),
        "weight_src": weight(src),
        "weight_dst": weight(dst),
        "signed_sum_src": signed_digit_sum(src),
        "signed_sum_dst": signed_digit_sum(dst),
        "positive_src": positive_digit_count(src),
        "positive_dst": positive_digit_count(dst),
        "negative_src": negative_digit_count(src),
        "negative_dst": negative_digit_count(dst),
        "zeros_src": zero_count(src),
        "zeros_dst": zero_count(dst),
        "position_class_2_src": position_class_sums(src, 2),
        "position_class_2_dst": position_class_sums(dst, 2),
        "position_class_3_src": position_class_sums(src, 3),
        "position_class_3_dst": position_class_sums(dst, 3),
    }


@dataclass(frozen=True)
class OperatorMetadata:
    name: str
    symbol: str
    integer_domain: str
    word_domain: str
    partial: bool
    involution_on_stated_domain: bool
    finite_state: bool | None
    transducer_type: str
    reading_direction: str
    state_count: int | None
    proof_status: str
    notes: str

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "symbol": self.symbol,
            "integer_domain": self.integer_domain,
            "word_domain": self.word_domain,
            "partial": self.partial,
            "involution_on_stated_domain": self.involution_on_stated_domain,
            "finite_state": self.finite_state,
            "transducer_type": self.transducer_type,
            "reading_direction": self.reading_direction,
            "state_count": self.state_count,
            "proof_status": self.proof_status,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class BTOperator:
    """A paired integer-level and word-level balanced-ternary operator.

    ``apply`` is only defined on ``int``. ``apply_word`` is only defined on
    words. There is no overload that accepts both.
    """

    name: str
    symbol: str
    integer_domain: str
    word_domain: str
    _apply_int: Callable[[int], int]
    _apply_word: Callable[[WordLike], BalancedTernary]
    _in_integer_domain: Callable[[int], bool]
    _in_word_domain: Callable[[WordLike], bool]
    _inverse_int: Callable[[int], int | None]
    metadata_record: OperatorMetadata

    def apply(self, n: int) -> int:
        """Integer-level map. ``n`` must be ``int``, not a word."""
        n = _require_int(n)
        if not self._in_integer_domain(n):
            raise OperatorDomainError(
                f"{self.symbol} is undefined at integer {n} (domain {self.integer_domain})"
            )
        return self._apply_int(n)

    def apply_word(self, word: WordLike) -> BalancedTernary:
        """Word-level map. Does not accept a bare integer."""
        if isinstance(word, bool) or isinstance(word, int):
            raise TypeError(
                f"{self.symbol}.apply_word expects a balanced-ternary word, "
                f"got {type(word).__name__}; use apply(n) for integers"
            )
        if not self._in_word_domain(word):
            raise OperatorDomainError(
                f"{self.symbol} is undefined on word {normalize(word).word()!r} "
                f"(domain {self.word_domain})"
            )
        return self._apply_word(word)

    def inverse_if_defined(self, n: int) -> int | None:
        n = _require_int(n)
        return self._inverse_int(n)

    def metadata(self) -> OperatorMetadata:
        return self.metadata_record

    def in_domain(self, n: int) -> bool:
        return self._in_integer_domain(_require_int(n))

    def consistent_on(self, n: int) -> bool:
        """``decode(apply_word(BT(n))) == apply(n)`` when both are defined."""
        n = _require_int(n)
        if not self._in_integer_domain(n):
            return False
        return decode(self.apply_word(encode(n))) == self.apply(n)


def _always_int(_n: int) -> bool:
    return True


def _always_word(_w: WordLike) -> bool:
    return True


def _even_int(n: int) -> bool:
    return n % 2 == 0


def _even_word(word: WordLike) -> bool:
    return decode(word) % 2 == 0


def _div3_int(n: int) -> bool:
    return n % 3 == 0


def _div3_word(word: WordLike) -> bool:
    return digits(normalize(word))[0] == 0


def _no_inverse(_n: int) -> int | None:
    return None


SHIFT = BTOperator(
    name="ternary_shift",
    symbol="S",
    integer_domain="Z",
    word_domain="canonical_words",
    _apply_int=multiply_by_3,
    _apply_word=lambda w: shift_left(w, 1),
    _in_integer_domain=_always_int,
    _in_word_domain=_always_word,
    _inverse_int=lambda n: n // 3 if n % 3 == 0 else None,
    metadata_record=OperatorMetadata(
        name="ternary_shift",
        symbol="S",
        integer_domain="Z",
        word_domain="canonical_words",
        partial=False,
        involution_on_stated_domain=False,
        finite_state=True,
        transducer_type="letter-to-letter morphism (append LSD 0)",
        reading_direction="either (length-preserving after padding)",
        state_count=1,
        proof_status="EXACT — HUMAN PROOF",
        notes="S(n)=3n. BT(3n)=BT(n) followed by 0, except BT(0)=0.",
    ),
)

NEGATION = BTOperator(
    name="digit_negation",
    symbol="N",
    integer_domain="Z",
    word_domain="canonical_words",
    _apply_int=lambda n: -n,
    _apply_word=negate_word,
    _in_integer_domain=_always_int,
    _in_word_domain=_always_word,
    _inverse_int=lambda n: -n,
    metadata_record=OperatorMetadata(
        name="digit_negation",
        symbol="N",
        integer_domain="Z",
        word_domain="canonical_words",
        partial=False,
        involution_on_stated_domain=True,
        finite_state=True,
        transducer_type="letter-to-letter (sign flip)",
        reading_direction="either",
        state_count=1,
        proof_status="EXACT — HUMAN PROOF",
        notes="N(n)=-n is digitwise negation. N∘N = id.",
    ),
)

DERIVATIVE = BTOperator(
    name="digit_derivative",
    symbol="D",
    integer_domain="Z",
    word_domain="canonical_words",
    _apply_int=digit_derivative,
    _apply_word=drop_lsd_word,
    _in_integer_domain=_always_int,
    _in_word_domain=_always_word,
    _inverse_int=_no_inverse,
    metadata_record=OperatorMetadata(
        name="digit_derivative",
        symbol="D",
        integer_domain="Z",
        word_domain="canonical_words",
        partial=False,
        involution_on_stated_domain=False,
        finite_state=True,
        transducer_type="LSD-first: drop first letter, copy the rest",
        reading_direction="LSD-first sequential",
        state_count=1,
        proof_status="EXACT — HUMAN PROOF",
        notes="n = a0 + 3 D(n). Not floor-division by 3. Left inverse of S.",
    ),
)

REVERSAL = BTOperator(
    name="bt_reverse",
    symbol="W",
    integer_domain="Z",
    word_domain="canonical_words",
    _apply_int=bt_reverse,
    _apply_word=reverse_word,
    _in_integer_domain=_always_int,
    _in_word_domain=_always_word,
    _inverse_int=lambda n: bt_reverse(n) if n == 0 or n % 3 != 0 else None,
    metadata_record=OperatorMetadata(
        name="bt_reverse",
        symbol="W",
        integer_domain="Z",
        word_domain="canonical_words",
        partial=False,
        involution_on_stated_domain=False,
        finite_state=False,
        transducer_type="not one-way sequential (global reverse + canonicalize)",
        reading_direction="requires both ends",
        state_count=None,
        proof_status="EXACT — HUMAN PROOF",
        notes="OEIS A134028. W(W(n))=n iff n=0 or 3 does not divide n. W(3)=1≠3.",
    ),
)

REVERSAL_ZEROS = BTOperator(
    name="bt_reverse_zeros",
    symbol="Wz",
    integer_domain="Z",
    word_domain="canonical_words",
    _apply_int=bt_reverse_zeros,
    _apply_word=reverse_zeros_word,
    _in_integer_domain=_always_int,
    _in_word_domain=_always_word,
    _inverse_int=bt_reverse_zeros,
    metadata_record=OperatorMetadata(
        name="bt_reverse_zeros",
        symbol="Wz",
        integer_domain="Z",
        word_domain="canonical_words",
        partial=False,
        involution_on_stated_domain=True,
        finite_state=False,
        transducer_type="reverse leaving trailing zeros",
        reading_direction="requires both ends",
        state_count=None,
        proof_status="EXACT — HUMAN PROOF",
        notes="OEIS A160652. Wz(n)=W(n) 3^{v3(n)}. Involutive on Z.",
    ),
)

REVERSAL_TAIL = BTOperator(
    name="bt_reverse_tail",
    symbol="Wt",
    integer_domain="Z",
    word_domain="canonical_words",
    _apply_int=bt_reverse_tail,
    _apply_word=reverse_tail_word,
    _in_integer_domain=_always_int,
    _in_word_domain=_always_word,
    _inverse_int=bt_reverse_tail,
    metadata_record=OperatorMetadata(
        name="bt_reverse_tail",
        symbol="Wt",
        integer_domain="Z",
        word_domain="canonical_words",
        partial=False,
        involution_on_stated_domain=True,
        finite_state=False,
        transducer_type="reverse all but MSD",
        reading_direction="requires both ends",
        state_count=None,
        proof_status="EXACT — HUMAN PROOF",
        notes="OEIS A351702. Involutive on each length block.",
    ),
)


def _apply_m2_int(n: int) -> int:
    return 2 * n


def _apply_m2_word(word: WordLike) -> BalancedTernary:
    from bt.transducers.doubling import apply_double

    return apply_double(word)


def _apply_h2_int(n: int) -> int:
    if n % 2 != 0:
        raise OperatorDomainError(f"H2 is defined only on even integers, got {n}")
    return n // 2


def _apply_h2_word(word: WordLike) -> BalancedTernary:
    from bt.transducers.divide_by_two import apply_even

    return apply_even(word)


DOUBLE = BTOperator(
    name="multiply_by_two",
    symbol="M2",
    integer_domain="Z",
    word_domain="canonical_words",
    _apply_int=_apply_m2_int,
    _apply_word=_apply_m2_word,
    _in_integer_domain=_always_int,
    _in_word_domain=_always_word,
    _inverse_int=lambda n: n // 2 if n % 2 == 0 else None,
    metadata_record=OperatorMetadata(
        name="multiply_by_two",
        symbol="M2",
        integer_domain="Z",
        word_domain="canonical_words",
        partial=False,
        involution_on_stated_domain=False,
        finite_state=True,
        transducer_type="LSD Mealy, carry in {-1,0,+1}",
        reading_direction="LSD-first",
        state_count=3,
        proof_status="EXACT — HUMAN PROOF",
        notes="Existing DoublingTransducer. Sequential inverse of H2 on 2Z.",
    ),
)

HALVE = BTOperator(
    name="divide_by_two_even",
    symbol="H2",
    integer_domain="2Z",
    word_domain="even_integers",
    _apply_int=_apply_h2_int,
    _apply_word=_apply_h2_word,
    _in_integer_domain=_even_int,
    _in_word_domain=_even_word,
    _inverse_int=lambda n: 2 * n,
    metadata_record=OperatorMetadata(
        name="divide_by_two_even",
        symbol="H2",
        integer_domain="2Z",
        word_domain="even_integers",
        partial=True,
        involution_on_stated_domain=False,
        finite_state=True,
        transducer_type="LSD Mealy on even integers; leftover carry on odds",
        reading_direction="LSD-first",
        state_count=3,
        proof_status="EXACT — HUMAN PROOF",
        notes="Existing DivideByTwoTransducer. Partial: undefined on odds.",
    ),
)

DIVIDE_BY_THREE = BTOperator(
    name="divide_by_three_when_divisible",
    symbol="H3",
    integer_domain="3Z",
    word_domain="words_with_a0_zero",
    _apply_int=lambda n: n // 3,
    _apply_word=drop_lsd_word,
    _in_integer_domain=_div3_int,
    _in_word_domain=_div3_word,
    _inverse_int=lambda n: 3 * n,
    metadata_record=OperatorMetadata(
        name="divide_by_three_when_divisible",
        symbol="H3",
        integer_domain="3Z",
        word_domain="words_with_a0_zero",
        partial=True,
        involution_on_stated_domain=False,
        finite_state=True,
        transducer_type="D restricted to a0=0",
        reading_direction="LSD-first",
        state_count=1,
        proof_status="EXACT — HUMAN PROOF",
        notes="On 3Z, H3 = D. Inverse of S.",
    ),
)

KERNEL3 = BTOperator(
    name="three_kernel",
    symbol="K3",
    integer_domain="Z",
    word_domain="canonical_words",
    _apply_int=three_kernel,
    _apply_word=lambda w: encode(three_kernel(decode(w))),
    _in_integer_domain=_always_int,
    _in_word_domain=_always_word,
    _inverse_int=_no_inverse,
    metadata_record=OperatorMetadata(
        name="three_kernel",
        symbol="K3",
        integer_domain="Z",
        word_domain="canonical_words",
        partial=False,
        involution_on_stated_domain=False,
        finite_state=True,
        transducer_type="LSD-first: skip trailing zeros, then copy",
        reading_direction="LSD-first sequential",
        state_count=2,
        proof_status="EXACT — HUMAN PROOF",
        notes="n / 3^{v3(n)}. Trailing zeros are locally visible, unlike v2.",
    ),
)


def _integral_operator(digit: int, symbol: str) -> BTOperator:
    def app_int(n: int) -> int:
        return 3 * n + digit

    def app_word(word: WordLike) -> BalancedTernary:
        return prepend_lsd_word(word, digit)

    def inv(n: int) -> int | None:
        if lsd_digit(n) != digit:
            return None
        return digit_derivative(n)

    return BTOperator(
        name=f"digit_integral_{digit:+d}".replace("+", "p").replace("-", "m"),
        symbol=symbol,
        integer_domain="Z",
        word_domain="canonical_words",
        _apply_int=app_int,
        _apply_word=app_word,
        _in_integer_domain=_always_int,
        _in_word_domain=_always_word,
        _inverse_int=inv,
        metadata_record=OperatorMetadata(
            name=f"digit_integral_lsd_{digit}",
            symbol=symbol,
            integer_domain="Z",
            word_domain="canonical_words",
            partial=False,
            involution_on_stated_domain=False,
            finite_state=True,
            transducer_type="prepend LSD digit",
            reading_direction="LSD-first",
            state_count=1,
            proof_status="EXACT — HUMAN PROOF",
            notes=f"I_{digit}(n)=3n+({digit}). D ∘ I_{digit} = id. I_0 = S.",
        ),
    )


INTEGRAL_MINUS = _integral_operator(-1, "Im")
INTEGRAL_ZERO = SHIFT
INTEGRAL_PLUS = _integral_operator(1, "Ip")

OPERATORS: dict[str, BTOperator] = {
    "S": SHIFT,
    "N": NEGATION,
    "D": DERIVATIVE,
    "W": REVERSAL,
    "Wz": REVERSAL_ZEROS,
    "Wt": REVERSAL_TAIL,
    "M2": DOUBLE,
    "H2": HALVE,
    "H3": DIVIDE_BY_THREE,
    "K3": KERNEL3,
    "Im": INTEGRAL_MINUS,
    "I0": SHIFT,
    "Ip": INTEGRAL_PLUS,
}

# Default generators for algebra (I_0 is S).
ALGEBRA_GENERATORS: tuple[str, ...] = ("S", "N", "D", "W", "Wz", "Wt", "M2", "H2")


def get_operator(symbol: str) -> BTOperator:
    try:
        return OPERATORS[symbol]
    except KeyError as exc:
        known = ", ".join(sorted(OPERATORS))
        raise KeyError(f"unknown operator {symbol!r}; known: {known}") from exc


def d_orbit(n: int) -> tuple[int, ...]:
    """``(n, D(n), D^2(n), ..., 0)``. Length is ``L_3(n)+1`` for ``n != 0``."""
    n = _require_int(n)
    orbit = [n]
    seen = {n}
    while n != 0:
        n = digit_derivative(n)
        if n in seen:
            raise RuntimeError(f"D-orbit failed to reach 0: {orbit}")
        seen.add(n)
        orbit.append(n)
    return tuple(orbit)


def recovered_digits(n: int) -> tuple[int, ...]:
    """LSD-first digits recovered as successive LSDs along the D-orbit."""
    n = _require_int(n)
    if n == 0:
        return (0,)
    out: list[int] = []
    while n != 0:
        out.append(lsd_digit(n))
        n = digit_derivative(n)
    return tuple(out)


def d_steps_to_zero(n: int) -> int:
    """Stopping time of D. Equals canonical length ``L_3(n)`` for ``n != 0``."""
    n = _require_int(n)
    if n == 0:
        return 0
    steps = 0
    while n != 0:
        n = digit_derivative(n)
        steps += 1
        if steps > 10_000:
            raise RuntimeError("D-orbit exceeded 10000 steps")
    return steps


def iterate_operator(symbol: str, n: int, steps: int) -> tuple[int, ...]:
    """Forward orbit ``n, F(n), ..., F^{steps}(n)`` while defined."""
    op = get_operator(symbol)
    n = _require_int(n)
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise ValueError(f"steps must be a nonnegative int, got {steps!r}")
    orbit = [n]
    for _ in range(steps):
        if not op.in_domain(n):
            break
        n = op.apply(n)
        orbit.append(n)
    return tuple(orbit)


def fixed_points(symbol: str, limit: int) -> tuple[int, ...]:
    """``F(n)=n`` on ``[-limit, limit] ∩ domain``."""
    op = get_operator(symbol)
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
        raise ValueError(f"limit must be a nonnegative int, got {limit!r}")
    hits = []
    for n in range(-limit, limit + 1):
        if op.in_domain(n) and op.apply(n) == n:
            hits.append(n)
    return tuple(hits)
