"""Exact affine geometry of one fixed positive odd Collatz trajectory.

For a genuine orbit ``n_{m+1} = T(n_m)`` the start is fixed: the cylinder
representative of every actual prefix is the integer ``n`` itself, not a
varying finite-code ``R_m`` (except as the unique residue of ``n`` modulo
``2^{K_m+1}``).

All stored arithmetic is ``int`` or ``Fraction``. Floating drift estimates
are not part of the core state.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from research.collatz.affine_center import AffineRegime
from research.collatz.affine_gap import affine_gap, affine_gap_from_orbit, next_affine_gap
from research.collatz.core import collatz_step, collatz_valuation, require_positive_odd
from research.collatz.cylinders import parse_ks
from research.collatz.dual_code import canonical_realizer_formula
from research.collatz.endpoint_3adic import KramerEndpoint
from research.collatz.itinerary import (
    ValuationItinerary,
    affine_constant,
    affine_constant_closed_form,
    partial_sums_K,
)


def exact_regime(two_power: int, three_power: int) -> AffineRegime | None:
    """Compare ``2^K`` and ``3^m`` exactly. ``None`` only for ``m = K = 0``."""
    gap = two_power - three_power
    if gap == 0:
        return None
    return AffineRegime.CONTRACTING if gap > 0 else AffineRegime.EXPANDING


def exact_partition(two_power: int, three_power: int, critical_gap: int) -> str:
    """Classify a prefix by the exact absolute gap ``|2^K - 3^m|``."""
    if (
        isinstance(critical_gap, bool)
        or not isinstance(critical_gap, int)
        or critical_gap < 0
    ):
        raise ValueError("critical_gap must be an integer >= 0")
    gap = two_power - three_power
    if gap == 0:
        return "empty"
    if abs(gap) <= critical_gap:
        return "critical-near"
    return "contracting" if gap > 0 else "expanding"


def normalized_C(C: int, m: int) -> Fraction:
    """``A_m = C_m / 3^m`` as an exact rational."""
    if isinstance(m, bool) or not isinstance(m, int) or m < 0:
        raise ValueError("m must be an integer >= 0")
    if isinstance(C, bool) or not isinstance(C, int):
        raise TypeError("C must be int")
    return Fraction(C, 3**m)


def normalized_C_series(partial_K: tuple[int, ...]) -> Fraction:
    """``A_m = sum_{j=0}^{m-1} 2^{K_j} / 3^{j+1}``.

    ``partial_K`` is ``(K_0, ..., K_m)`` with ``K_0 = 0``.
    """
    if not partial_K:
        raise ValueError("partial_K must contain K_0 = 0")
    if partial_K[0] != 0:
        raise ValueError("K_0 must be 0")
    total = Fraction(0)
    for j, Kj in enumerate(partial_K[:-1]):
        total += Fraction(1 << Kj, 3 ** (j + 1))
    return total


def required_start_residue(valuations: tuple[int, ...] | str | list[int]) -> int:
    """Unique cylinder residue ``R`` modulo ``2^{K+1}`` of a valuation word."""
    return canonical_realizer_formula(valuations)


def required_start_residue_mod_power(
    valuations: tuple[int, ...] | str | list[int],
) -> tuple[int, int]:
    """``(R, 2^{K+1})`` for the cylinder of ``valuations``."""
    ks = parse_ks(valuations)
    modulus = 1 << (sum(ks) + 1)
    return canonical_realizer_formula(ks), modulus


def next_C(C: int, two_power: int) -> int:
    """``C' = 3C + 2^K``."""
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (C, two_power)):
        raise TypeError("C recurrence arguments must be int")
    return 3 * C + two_power


def next_normalized_C(A: Fraction, two_power: int, m: int) -> Fraction:
    """``A' = A + 2^K / 3^{m+1}``."""
    if not isinstance(A, Fraction):
        raise TypeError("A must be a Fraction")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (two_power, m)):
        raise TypeError("normalized-C recurrence arguments must be int")
    if m < 0:
        raise ValueError("m must be an integer >= 0")
    return A + Fraction(two_power, 3 ** (m + 1))


def next_affine_center(
    C: int,
    two_power: int,
    three_power: int,
    k: int,
) -> Fraction | None:
    """Exact successor center, or ``None`` if the next gap vanishes."""
    if any(
        isinstance(value, bool) or not isinstance(value, int)
        for value in (C, two_power, three_power, k)
    ):
        raise TypeError("center recurrence arguments must be int")
    if k < 1:
        raise ValueError("k must be an integer >= 1")
    C_next = next_C(C, two_power)
    gap_next = (two_power << k) - 3 * three_power
    if gap_next == 0:
        return None
    return Fraction(C_next, gap_next)


def normalized_C_finite_bounds(partial_K: tuple[int, ...]) -> dict[str, Fraction]:
    """Exact finite-m bounds that do not assume an average slope.

    Each term satisfies ``1/3^{j+1} <= 2^{K_j}/3^{j+1} <= 2^{K_{m-1}}/3^{j+1}``
    because ``0 <= K_j <= K_{m-1}``.
    """
    if not partial_K or partial_K[0] != 0:
        raise ValueError("partial_K must start with K_0 = 0")
    m = len(partial_K) - 1
    if m == 0:
        zero = Fraction(0)
        return {
            "A": zero,
            "lower_K_j_ge_0": zero,
            "upper_K_j_le_K_last": zero,
        }
    K_last = partial_K[-2]
    lower = Fraction(0)
    upper = Fraction(0)
    for j in range(m):
        lower += Fraction(1, 3 ** (j + 1))
        upper += Fraction(1 << K_last, 3 ** (j + 1))
    return {
        "A": normalized_C_series(partial_K),
        "lower_K_j_ge_0": lower,
        "upper_K_j_le_K_last": upper,
    }


@dataclass(frozen=True)
class InfiniteTrajectoryAffineState:
    """Exact affine snapshot of ``T^m(n)`` for one fixed positive odd ``n``."""

    n: int
    m: int
    K: int
    C: int
    x: int
    valuations: tuple[int, ...]
    two_power: int
    three_power: int
    lambda_m: Fraction
    A: Fraction
    B: Fraction
    affine_center: Fraction | None
    displacement: Fraction | None
    n_star_raw: tuple[int, int] | None
    n_star_reduced: tuple[int, int] | None
    G: int
    regime: str
    start_residue: int
    start_modulus: int
    M: int | None

    @property
    def gap(self) -> int:
        return self.two_power - self.three_power

    @classmethod
    def prefix(cls, n: int, m: int) -> "InfiniteTrajectoryAffineState":
        """State after exactly ``m`` accelerated steps of ``n``."""
        n = require_positive_odd(n)
        if isinstance(m, bool) or not isinstance(m, int) or m < 0:
            raise ValueError("m must be an integer >= 0")
        ks: list[int] = []
        x = n
        for _ in range(m):
            ks.append(collatz_valuation(x))
            x = collatz_step(x)
        return cls.from_valuations(n, tuple(ks), x)

    @classmethod
    def from_valuations(
        cls,
        n: int,
        valuations: tuple[int, ...],
        x: int | None = None,
    ) -> "InfiniteTrajectoryAffineState":
        n = require_positive_odd(n)
        ks = parse_ks(valuations)
        itinerary = ValuationItinerary.from_ks(ks)
        if affine_constant(ks) != affine_constant_closed_form(ks):
            raise ArithmeticError("C recurrence disagrees with the closed form")
        computed_x = itinerary.apply(n)
        if x is None:
            x = computed_x
        elif x != computed_x:
            raise ArithmeticError("supplied x disagrees with the affine formula")
        two_power = itinerary.denominator
        three_power = itinerary.numerator_multiplier
        A = normalized_C(itinerary.C, itinerary.m)
        series = normalized_C_series(partial_sums_K(ks))
        if A != series:
            raise ArithmeticError("normalized C disagrees with the valuation series")
        B = n + A
        expected_B = Fraction(two_power * x, three_power)
        if B != expected_B:
            raise ArithmeticError("B = n + A disagrees with (2^K/3^m) x")
        lambda_m = Fraction(three_power, two_power)
        gap = two_power - three_power
        if itinerary.m == 0:
            center = None
            displacement = None
            n_star_raw = None
            n_star_reduced = None
            regime = "empty"
            M = None
        else:
            if gap == 0:
                raise ArithmeticError("2^K = 3^m is impossible for m >= 1")
            center = Fraction(itinerary.C, gap)
            displacement = n - center
            n_star_raw = (itinerary.C, gap)
            n_star_reduced = (center.numerator, center.denominator)
            regime = exact_regime(two_power, three_power).value  # type: ignore[union-attr]
            M = KramerEndpoint.from_valuations(ks).M
        G = affine_gap(n, two_power, three_power, itinerary.C)
        if G != affine_gap_from_orbit(n, x, two_power):
            raise ArithmeticError("G disagrees with 2^K (n - x)")
        residue, modulus = required_start_residue_mod_power(ks)
        if n % modulus != residue % modulus:
            raise ArithmeticError("fixed n is not in its own valuation cylinder")
        state = cls(
            n=n,
            m=itinerary.m,
            K=itinerary.K,
            C=itinerary.C,
            x=x,
            valuations=ks,
            two_power=two_power,
            three_power=three_power,
            lambda_m=lambda_m,
            A=A,
            B=B,
            affine_center=center,
            displacement=displacement,
            n_star_raw=n_star_raw,
            n_star_reduced=n_star_reduced,
            G=G,
            regime=regime,
            start_residue=residue,
            start_modulus=modulus,
            M=M,
        )
        if not state.validates():
            raise ArithmeticError("fixed-integer affine state failed validation")
        return state

    def form_A(self) -> Fraction:
        """``x = lambda n + C / 2^K``."""
        return self.lambda_m * self.n + Fraction(self.C, self.two_power)

    def form_B_centered(self) -> Fraction | None:
        """``x - n_* = lambda (n - n_*)``."""
        if self.affine_center is None:
            return None
        return self.lambda_m * (self.n - self.affine_center)

    def form_C_over_three(self) -> Fraction:
        """``C / 3^m = lambda^{-1} x - n``."""
        return self.x / self.lambda_m - self.n

    def form_C_over_two(self) -> Fraction:
        """``C / 2^K = x - lambda n``."""
        return Fraction(self.x) - self.lambda_m * self.n

    def form_center(self) -> Fraction | None:
        return self.affine_center

    def form_displacement_unreduced(self) -> tuple[int, int] | None:
        """Numerator ``2^K n - 3^m n - C`` over ``2^K - 3^m``."""
        if self.m == 0:
            return None
        return (self.two_power * self.n - self.three_power * self.n - self.C, self.gap)

    def n_star_le_n(self) -> bool | None:
        if self.affine_center is None:
            return None
        return self.affine_center <= self.n

    def positivity_bound(self) -> bool:
        """``B >= 2^K / 3^m``, i.e. ``x >= 1``. Tautological for actual orbits."""
        return self.B >= Fraction(self.two_power, self.three_power)

    def validates(self) -> bool:
        if self.x != Fraction(self.three_power * self.n + self.C, self.two_power):
            return False
        if self.form_A() != self.x:
            return False
        if self.A != self.form_C_over_three() or self.A != Fraction(self.C, self.three_power):
            return False
        if self.form_C_over_two() != Fraction(self.C, self.two_power):
            return False
        if self.B != self.n + self.A:
            return False
        if self.G != self.two_power * (self.n - self.x):
            return False
        if self.m >= 1:
            if self.affine_center is None or self.gap == 0:
                return False
            if self.form_B_centered() != self.x - self.affine_center:
                return False
            if Fraction(*self.form_displacement_unreduced()) != self.displacement:
                return False
            if (self.affine_center <= self.n) != (self.G * self.gap >= 0):
                return False
            if self.M is not None and self.M > self.x:
                return False
        return True

    def as_dict(self) -> dict[str, object]:
        return {
            "n": self.n,
            "m": self.m,
            "K": self.K,
            "C": self.C,
            "x": self.x,
            "valuations": list(self.valuations),
            "two_power": self.two_power,
            "three_power": self.three_power,
            "lambda_num": self.lambda_m.numerator,
            "lambda_den": self.lambda_m.denominator,
            "A_num": self.A.numerator,
            "A_den": self.A.denominator,
            "B_num": self.B.numerator,
            "B_den": self.B.denominator,
            "n_star": None if self.n_star_reduced is None else list(self.n_star_reduced),
            "n_star_raw": None if self.n_star_raw is None else list(self.n_star_raw),
            "displacement": (
                None
                if self.displacement is None
                else [self.displacement.numerator, self.displacement.denominator]
            ),
            "G": self.G,
            "regime": self.regime,
            "start_residue": self.start_residue,
            "start_modulus": self.start_modulus,
            "M": self.M,
            "n_star_le_n": self.n_star_le_n(),
        }


def iterate_states(n: int, max_steps: int) -> tuple[InfiniteTrajectoryAffineState, ...]:
    """States for prefixes ``0 .. min(max_steps, steps until 1)``."""
    n = require_positive_odd(n)
    if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps < 0:
        raise ValueError("max_steps must be an integer >= 0")
    states = [InfiniteTrajectoryAffineState.from_valuations(n, ())]
    ks: list[int] = []
    x = n
    steps = 0
    while steps < max_steps:
        ks.append(collatz_valuation(x))
        x = collatz_step(x)
        states.append(InfiniteTrajectoryAffineState.from_valuations(n, tuple(ks), x))
        steps += 1
        if x == 1:
            break
    return tuple(states)


def next_state(
    state: InfiniteTrajectoryAffineState,
) -> InfiniteTrajectoryAffineState:
    """Advance one accelerated step, checking the exact recurrences."""
    if state.x == 1 and state.m > 0:
        k = collatz_valuation(1)
    else:
        k = collatz_valuation(state.x)
    predicted_G = next_affine_gap(state.G, state.n, state.two_power, k)
    predicted_C = next_C(state.C, state.two_power)
    predicted_A = next_normalized_C(state.A, state.two_power, state.m)
    predicted_center = next_affine_center(
        state.C, state.two_power, state.three_power, k
    )
    child = InfiniteTrajectoryAffineState.from_valuations(
        state.n,
        state.valuations + (k,),
    )
    if child.G != predicted_G:
        raise ArithmeticError("G recurrence disagrees with the next state")
    if child.C != predicted_C:
        raise ArithmeticError("C recurrence disagrees with the next state")
    if child.A != predicted_A:
        raise ArithmeticError("A recurrence disagrees with the next state")
    if child.affine_center != predicted_center:
        raise ArithmeticError("n_* recurrence disagrees with the next state")
    return child
