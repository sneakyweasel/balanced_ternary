"""Exact dual coding of finite Collatz valuation itineraries.

For a prefix ``p`` of length ``m`` with total valuation ``K``, affine
constant ``C``, canonical realizer ``R``, and endpoint

    x = T^m(R) = (3^m R + C) / 2^K,

the direct residue formula is

    R = ((2^K - C) * (3^m)^(-1)) mod 2^(K+1).

For an extension by valuation ``k``, put ``q = (3x+1)/2``.  The lift
digit is the unique representative in ``[0, 2^k)`` satisfying

    t = (3^(m+1))^(-1) * (2^(k-1) - q)  (mod 2^k).

Then

    R' = R + t 2^(K+1),
    x' = (q + 3^(m+1)t) / 2^(k-1).

These identities are **PROVED** by the exact cylinder congruence.  They
do not replay the complete trajectory and never divide a residue modulo
a power of two.
"""

from __future__ import annotations

from dataclasses import dataclass

from balanced_ternary.representation import decode, encode
from research.collatz.automata.valuation_shift import growth_budget
from research.collatz.cylinders import parse_ks
from research.collatz.features import BalancedTernaryFeatures, extract_features
from research.collatz.itinerary import affine_constant


def _require_k(k: int) -> int:
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError(f"k must be an integer >= 1, got {k!r}")
    return k


def canonical_realizer_formula(
    valuations: tuple[int, ...] | str | list[int],
) -> int:
    """Compute ``R`` directly from ``(m,K,C)``. **PROVED**."""
    ks = parse_ks(valuations)
    m = len(ks)
    K = sum(ks)
    modulus = 1 << (K + 1)
    c = affine_constant(ks)
    inv_three_m = pow(pow(3, m, modulus), -1, modulus)
    r = (((1 << K) - c) * inv_three_m) % modulus
    if r == 0 or r % 2 == 0:
        raise ArithmeticError("direct realizer formula did not produce an odd residue")
    return r


def canonical_endpoint_formula(
    valuations: tuple[int, ...] | str | list[int],
    R: int | None = None,
) -> int:
    """Return ``x=T^m(R)`` from affine data, using exact integer division."""
    ks = parse_ks(valuations)
    r = canonical_realizer_formula(ks) if R is None else R
    numerator = pow(3, len(ks)) * r + affine_constant(ks)
    denominator = 1 << sum(ks)
    if numerator % denominator:
        raise ArithmeticError("canonical endpoint numerator is not exactly divisible")
    x = numerator // denominator
    if x <= 0 or x % 2 == 0:
        raise ArithmeticError("canonical endpoint is not a positive odd integer")
    return x


def lift_digit_from_state(m: int, x: int, k: int) -> int:
    """Exact lift digit from the minimal state ``(m,x)`` and next ``k``."""
    if isinstance(m, bool) or not isinstance(m, int) or m < 0:
        raise ValueError(f"m must be an integer >= 0, got {m!r}")
    if isinstance(x, bool) or not isinstance(x, int) or x <= 0 or x % 2 == 0:
        raise ValueError(f"x must be a positive odd integer, got {x!r}")
    k = _require_k(k)
    q = (3 * x + 1) // 2
    modulus = 1 << k
    three = pow(3, m + 1, modulus)
    inverse = pow(three, -1, modulus)
    return ((1 << (k - 1)) - q) * inverse % modulus


def lift_digit_formula(
    parent: tuple[int, ...] | str | list[int],
    k: int,
) -> int:
    """Exact ``t(parent,k)`` without constructing the child cylinder."""
    parent = parse_ks(parent)
    x = canonical_endpoint_formula(parent)
    return lift_digit_from_state(len(parent), x, k)


def endpoint_successor(m: int, x: int, k: int, lift_digit: int) -> int:
    """Exact canonical endpoint after one paired ``(k,t)`` transition."""
    k = _require_k(k)
    if (
        isinstance(lift_digit, bool)
        or not isinstance(lift_digit, int)
        or not 0 <= lift_digit < (1 << k)
    ):
        raise ValueError(f"lift_digit must lie in [0, 2^{k}), got {lift_digit!r}")
    q = (3 * x + 1) // 2
    numerator = q + pow(3, m + 1) * lift_digit
    denominator = 1 << (k - 1)
    if numerator % denominator:
        raise ValueError("the paired (k,lift_digit) transition is not integral")
    child = numerator // denominator
    if child <= 0 or child % 2 == 0:
        raise ValueError("the paired (k,lift_digit) transition is not exact-k")
    return child


def reconstruct_realizer(
    valuations: tuple[int, ...] | str | list[int],
    digits: tuple[int, ...] | list[int],
) -> int:
    """Mixed-radix reconstruction ``1 + sum t_j 2^(K_j+1)``."""
    ks = parse_ks(valuations)
    ts = tuple(digits)
    if len(ts) != len(ks):
        raise ValueError("valuations and lift digits must have equal length")
    r = 1
    K = 0
    for k, t in zip(ks, ts):
        if isinstance(t, bool) or not isinstance(t, int) or not 0 <= t < (1 << k):
            raise ValueError(f"lift digit {t!r} must lie in [0, 2^{k})")
        r += t << (K + 1)
        K += k
    return r


def decode_lift_digits(
    valuations: tuple[int, ...] | str | list[int],
    R: int,
) -> tuple[int, ...]:
    """Unique mixed-radix digits of odd ``R`` for fixed valuations."""
    ks = parse_ks(valuations)
    modulus = 1 << (sum(ks) + 1)
    if isinstance(R, bool) or not isinstance(R, int) or R <= 0 or R % 2 == 0:
        raise ValueError(f"R must be a positive odd integer, got {R!r}")
    if R >= modulus:
        raise ValueError(f"R must be below the canonical modulus {modulus}")
    payload = (R - 1) // 2
    K = 0
    out: list[int] = []
    for k in ks:
        out.append((payload >> K) % (1 << k))
        K += k
    return tuple(out)


@dataclass(frozen=True)
class DualCodeStep:
    index: int
    valuation: int
    K_before: int
    K_after: int
    lift_digit: int
    R_before: int
    R_after: int
    endpoint_before: int
    endpoint_after: int

    @property
    def zero_lift(self) -> bool:
        return self.lift_digit == 0

    @property
    def edge_class(self) -> str:
        return "ZERO_LIFT" if self.zero_lift else "POSITIVE_LIFT"

    @property
    def budget_delta(self) -> str:
        return growth_budget((self.valuation,)).kind


@dataclass(frozen=True)
class CollatzDualCode:
    """First-class exact valuation/lift/balanced-ternary coding."""

    valuations: tuple[int, ...]
    cumulative_K: tuple[int, ...]
    lift_digits: tuple[int, ...]
    realizers: tuple[int, ...]
    endpoints: tuple[int, ...]
    steps: tuple[DualCodeStep, ...]
    m: int
    K: int
    C: int
    modulus: int
    R: int
    balanced_ternary_R: str
    features: BalancedTernaryFeatures

    @classmethod
    def from_valuations(
        cls, valuations: tuple[int, ...] | str | list[int]
    ) -> "CollatzDualCode":
        ks = parse_ks(valuations)
        K = 0
        r = 1
        x = 1
        cumulative = [0]
        digits: list[int] = []
        realizers = [r]
        endpoints = [x]
        steps: list[DualCodeStep] = []
        for m, k in enumerate(ks):
            t = lift_digit_from_state(m, x, k)
            child_r = r + (t << (K + 1))
            child_x = endpoint_successor(m, x, k, t)
            steps.append(
                DualCodeStep(
                    index=m,
                    valuation=k,
                    K_before=K,
                    K_after=K + k,
                    lift_digit=t,
                    R_before=r,
                    R_after=child_r,
                    endpoint_before=x,
                    endpoint_after=child_x,
                )
            )
            K += k
            r = child_r
            x = child_x
            cumulative.append(K)
            digits.append(t)
            realizers.append(r)
            endpoints.append(x)
        direct = canonical_realizer_formula(ks)
        if r != direct:
            raise ArithmeticError(f"dual recurrence R={r} != direct R={direct}")
        if reconstruct_realizer(ks, digits) != r:
            raise ArithmeticError("mixed-radix reconstruction failed")
        if decode_lift_digits(ks, r) != tuple(digits):
            raise ArithmeticError("mixed-radix digit uniqueness failed")
        word = encode(r)
        if decode(word) != r:
            raise ArithmeticError("balanced-ternary round trip failed")
        return cls(
            valuations=ks,
            cumulative_K=tuple(cumulative),
            lift_digits=tuple(digits),
            realizers=tuple(realizers),
            endpoints=tuple(endpoints),
            steps=tuple(steps),
            m=len(ks),
            K=K,
            C=affine_constant(ks),
            modulus=1 << (K + 1),
            R=r,
            balanced_ternary_R=word.word(),
            features=extract_features(word),
        )

    def reconstruct_R(self) -> int:
        return reconstruct_realizer(self.valuations, self.lift_digits)

    def validates(self) -> bool:
        return (
            self.reconstruct_R() == self.R
            and decode_lift_digits(self.valuations, self.R) == self.lift_digits
            and canonical_realizer_formula(self.valuations) == self.R
            and canonical_endpoint_formula(self.valuations, self.R)
            == self.endpoints[-1]
        )

    def as_dict(self) -> dict[str, object]:
        budget = growth_budget(self.valuations)
        return {
            "itinerary": list(self.valuations),
            "m": self.m,
            "K": self.K,
            "cumulative_K": list(self.cumulative_K),
            "C": self.C,
            "lift_digits": list(self.lift_digits),
            "residue": self.R,
            "modulus": self.modulus,
            "R": self.R,
            "R_prefixes": list(self.realizers),
            "canonical_endpoints": list(self.endpoints),
            "BT(R)": self.balanced_ternary_R,
            "features": self.features.as_dict(),
            "two_power": budget.two_power,
            "three_power": budget.three_power,
            "budget_comparison": budget.kind,
            "zero_lift_flag": bool(self.lift_digits and self.lift_digits[-1] == 0),
            "status": "EXACT",
        }


def valid_pair_word(
    valuations: tuple[int, ...] | str | list[int],
    digits: tuple[int, ...] | list[int],
) -> bool:
    """Whether ``(valuations,digits)`` is the exact dual coding."""
    ks = parse_ks(valuations)
    ts = tuple(digits)
    if len(ks) != len(ts):
        return False
    try:
        return CollatzDualCode.from_valuations(ks).lift_digits == ts
    except (TypeError, ValueError):
        return False


def verify_dual_exhaustive(max_length: int, k_max: int) -> int:
    """Stream every word through the exact dual recurrences.

    Returns the number of prefixes checked, including the empty prefix.
    Raises immediately on any failed identity and stores no rows.
    """
    if max_length < 0 or k_max < 1:
        raise ValueError("max_length must be >= 0 and k_max >= 1")
    checked = 0

    def visit(
        prefix: tuple[int, ...],
        m: int,
        K: int,
        C: int,
        R: int,
        x: int,
    ) -> None:
        nonlocal checked
        checked += 1
        modulus = 1 << (K + 1)
        direct = (((1 << K) - C) * pow(pow(3, m, modulus), -1, modulus)) % modulus
        if direct != R:
            raise ArithmeticError(f"direct R mismatch at {prefix}")
        if (pow(3, m) * R + C) // (1 << K) != x:
            raise ArithmeticError(f"endpoint mismatch at {prefix}")
        if m == max_length:
            return
        for k in range(1, k_max + 1):
            t = lift_digit_from_state(m, x, k)
            if not 0 <= t < (1 << k):
                raise ArithmeticError(f"lift bound failed at {prefix + (k,)}")
            child_R = R + (t << (K + 1))
            child_x = endpoint_successor(m, x, k, t)
            child_C = 3 * C + (1 << K)
            visit(prefix + (k,), m + 1, K + k, child_C, child_R, child_x)

    visit((), 0, 0, 0, 1, 1)
    return checked
