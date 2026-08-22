"""Exact affine form of a finite accelerated Collatz valuation itinerary.

If the first ``m`` valuations of odd ``n`` are ``ks = (k_0, ..., k_{m-1})``,
then **PROVED**

    T^m(n) = (3^m n + C(ks)) / 2^K

with ``K = sum ks`` and

    C_empty = 0,
    C_{append k} = 3 C + 2^K_old.

Unrolling gives the closed form

    C(ks) = sum_{j=0}^{m-1}  3^{m-1-j}  2^{K_j},
    K_j = k_0 + ... + k_{j-1}   (K_0 = 0).

``C`` is a positive integer for ``m >= 1`` (each summand is positive).
The denominator is an exact power of two; the formula does **not** divide
a residue modulo ``2^P``.

Partial states: ``n_i = T^i(n) = (3^i n + C(ks[:i])) / 2^{K_i}``.

This module does not claim that an itinerary is realised by a positive
integer; that is ``collatz.min_realizer``. It does not claim a Lyapunov
function: ``2^K`` vs ``3^m`` is the homogeneous estimate only.
"""

from __future__ import annotations

from dataclasses import dataclass

from research.collatz.automata.valuation_shift import GrowthBudget, growth_budget
from research.collatz.cylinders import parse_ks
from research.collatz.valuation import v2


def affine_constant(ks: tuple[int, ...]) -> int:
    """``C(ks)`` by the append recurrence. ``C(()) = 0``."""
    ks = parse_ks(ks)
    c = 0
    k_sum = 0
    for _k in ks:
        c = 3 * c + (1 << k_sum)
        k_sum += _k
    return c


def affine_constant_closed_form(ks: tuple[int, ...]) -> int:
    """``C(ks) = sum_j 3^{m-1-j} 2^{K_j}``. Empty sum is 0."""
    ks = parse_ks(ks)
    c = 0
    k_sum = 0
    m = len(ks)
    for j, _k in enumerate(ks):
        c += pow(3, m - 1 - j) << k_sum
        k_sum += _k
    return c


def partial_sums_K(ks: tuple[int, ...]) -> tuple[int, ...]:
    """``(K_0, ..., K_m)`` with ``K_0 = 0`` and ``K_{j+1} = K_j + k_j``."""
    ks = parse_ks(ks)
    out = [0]
    s = 0
    for k in ks:
        s += k
        out.append(s)
    return tuple(out)


def partial_constants(ks: tuple[int, ...]) -> tuple[int, ...]:
    """``(C(ks[:0]), C(ks[:1]), ..., C(ks[:m]))``."""
    ks = parse_ks(ks)
    out = [0]
    c = 0
    k_sum = 0
    for k in ks:
        c = 3 * c + (1 << k_sum)
        k_sum += k
        out.append(c)
    return tuple(out)


def positivity_threshold(ks: tuple[int, ...]) -> int:
    """Smallest integer ``n`` with ``3^i n + C_i > 0`` for every prefix ``i``.

    **PROVED:** ``C_i >= 0``, so ``-C_i / 3^i <= 0``. For the positive-odd
    Collatz setting the threshold is ``1``. ``T`` sends positive odds to
    positive odds, so every genuine positive trajectory already satisfies
    ``n_i > 0``. The threshold distinguishes that Archimedean fact from
    2-adic cylinder membership, which does not mention sign.
    """
    ks = parse_ks(ks)
    constants = partial_constants(ks)
    # n > -C_i / 3^i for all i. Maximum of those lower bounds, then +1
    # if we require integer n_i > 0. All bounds are <= 0, so the integer
    # threshold among positive odds is 1.
    _ = constants
    return 1


def affine_image(n: int, ks: tuple[int, ...]) -> int:
    """``(3^m n + C) / 2^K`` as an exact integer, or raise if not divisible."""
    ks = parse_ks(ks)
    m = len(ks)
    k_sum = sum(ks)
    num = pow(3, m) * n + affine_constant(ks)
    den = 1 << k_sum
    if num % den != 0:
        raise ValueError(
            f"affine numerator {num} is not divisible by 2^{k_sum} for n={n}, ks={ks}"
        )
    return num // den


@dataclass(frozen=True)
class ValuationItinerary:
    """Exact affine data of one finite valuation word.

    ``numerator_multiplier = 3^m``, ``denominator = 2^K``, ``C`` as above.
    """

    valuations: tuple[int, ...]
    m: int
    K: int
    C: int
    numerator_multiplier: int
    denominator: int

    @classmethod
    def from_ks(cls, ks: tuple[int, ...] | str | list[int]) -> "ValuationItinerary":
        ks = parse_ks(ks)
        k_sum = sum(ks)
        c = affine_constant(ks)
        closed = affine_constant_closed_form(ks)
        if c != closed:
            raise ArithmeticError(
                f"C recurrence {c} != closed form {closed} for ks={ks}"
            )
        return cls(
            valuations=ks,
            m=len(ks),
            K=k_sum,
            C=c,
            numerator_multiplier=pow(3, len(ks)),
            denominator=1 << k_sum,
        )

    def budget(self) -> GrowthBudget:
        return growth_budget(self.valuations)

    def extend(self, k: int) -> "ValuationItinerary":
        if isinstance(k, bool) or not isinstance(k, int) or k < 1:
            raise ValueError(f"k must be an integer >= 1, got {k!r}")
        c_new = 3 * self.C + self.denominator
        k_new = self.K + k
        return ValuationItinerary(
            valuations=self.valuations + (k,),
            m=self.m + 1,
            K=k_new,
            C=c_new,
            numerator_multiplier=self.numerator_multiplier * 3,
            denominator=1 << k_new,
        )

    def prefix(self, length: int) -> "ValuationItinerary":
        if isinstance(length, bool) or not isinstance(length, int):
            raise TypeError("length must be int")
        if length < 0 or length > self.m:
            raise ValueError(f"length {length} out of range 0..{self.m}")
        return ValuationItinerary.from_ks(self.valuations[:length])

    def apply(self, n: int) -> int:
        """Exact ``T^m(n)`` from the affine formula."""
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError(f"n must be int, got {type(n).__name__}")
        num = self.numerator_multiplier * n + self.C
        if num % self.denominator != 0:
            raise ValueError(
                f"n={n} is not in the affine lattice of {self.valuations}: "
                f"{num} not divisible by {self.denominator}"
            )
        return num // self.denominator

    def partial_state(self, n: int, i: int) -> int:
        """``T^i(n)`` by the prefix affine formula."""
        return self.prefix(i).apply(n)

    def all_partial_states(self, n: int) -> tuple[int, ...]:
        constants = partial_constants(self.valuations)
        k_partial = partial_sums_K(self.valuations)
        out: list[int] = []
        for i in range(self.m + 1):
            num = pow(3, i) * n + constants[i]
            den = 1 << k_partial[i]
            if num % den != 0:
                raise ValueError(
                    f"partial i={i} numerator {num} not divisible by 2^{k_partial[i]}"
                )
            out.append(num // den)
        return tuple(out)

    def positivity_threshold(self) -> int:
        return positivity_threshold(self.valuations)

    def c_over_three_m_unreduced(self) -> tuple[int, int]:
        """Exact rational ``C / 3^m`` as ``(C, 3^m)``."""
        return self.C, self.numerator_multiplier

    def c_over_two_K_unreduced(self) -> tuple[int, int]:
        """Exact rational ``C / 2^K`` as ``(C, 2^K)``."""
        return self.C, self.denominator

    def c_over_homogeneous_gap(self) -> tuple[int, int] | None:
        """``C / (2^K - 3^m)`` as an integer ratio, or ``None`` if gap is 0.

        Equality ``2^K = 3^m`` is impossible for ``m > 0`` (irrationality of
        ``log2 3``). For ``m = 0`` the gap is ``1 - 1 = 0``.
        """
        gap = self.denominator - self.numerator_multiplier
        if gap == 0:
            return None
        return self.C, gap

    def as_dict(self) -> dict[str, object]:
        bgt = self.budget()
        gap = self.c_over_homogeneous_gap()
        return {
            "valuations": list(self.valuations),
            "m": self.m,
            "K": self.K,
            "C": self.C,
            "numerator_multiplier": self.numerator_multiplier,
            "denominator": self.denominator,
            "budget_kind": bgt.kind,
            "two_power": bgt.two_power,
            "three_power": bgt.three_power,
            "C_over_3^m": [self.C, self.numerator_multiplier],
            "C_over_2^K": [self.C, self.denominator],
            "C_over_2^K_minus_3^m": None if gap is None else [gap[0], gap[1]],
            "positivity_threshold": self.positivity_threshold(),
            "status": "EXACT",
        }

    def format(self) -> str:
        bgt = self.budget()
        lines = [
            f"Valuation itinerary  ks={self.valuations}  [EXACT]",
            f"m={self.m}  K={self.K}  C={self.C}",
            f"T^m(n) = ({self.numerator_multiplier} n + {self.C}) / {self.denominator}",
            f"budget 2^K={bgt.two_power} vs 3^m={bgt.three_power}  {bgt.kind}  "
            f"(homogeneous estimate, not a Lyapunov function)",
            f"positivity_threshold={self.positivity_threshold()}  "
            f"[PROVED: C>=0 so positive odds already have n_i>0]",
            "",
        ]
        return "\n".join(lines)


def verify_affine_against_T(n: int, ks: tuple[int, ...]) -> bool:
    """True iff ``T^m(n)`` from iterating ``T`` equals the affine formula.

    Requires odd ``n`` that realises ``ks``. Uses ``collatz_step`` on
    positive ``n``; the affine formula itself is sign-agnostic.
    """
    from research.collatz.cylinders import belongs_to_cylinder

    ks = parse_ks(ks)
    if not belongs_to_cylinder(n, ks):
        return False
    it = ValuationItinerary.from_ks(ks)
    x = n
    for _ in ks:
        y = 3 * x + 1
        k = v2(y)
        if k is None:
            return False
        x = y >> k
    return it.apply(n) == x
