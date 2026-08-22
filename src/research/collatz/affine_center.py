"""Exact affine-center geometry of finite Collatz exponent codes.

For a nonempty exponent code, put

    D = 2^K - 3^m,             n_star = C / D.

The affine map ``F(n) = (3^m n + C) / 2^K`` fixes ``n_star``.  At the
canonical start/end pair ``(R, X)`` this gives the exact centered scaling

    X - n_star = (3^m / 2^K) (R - n_star).

All stored arithmetic is integral or ``Fraction`` arithmetic.  Floating
approximations are deliberately absent.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction

from research.collatz.compatibility import CompatibilityState
from research.collatz.cylinders import parse_ks


class AffineRegime(str, Enum):
    CONTRACTING = "contracting"
    EXPANDING = "expanding"


def _fraction_pair(value: Fraction) -> tuple[int, int]:
    return value.numerator, value.denominator


@dataclass(frozen=True)
class AffineCenterState:
    """Exact affine fixed-center data for one nonempty exponent code."""

    valuations: tuple[int, ...]
    m: int
    K: int
    C: int
    R: int
    X: int
    M: int
    two_power: int
    three_power: int
    gap: int
    n_star: Fraction
    R_minus_n_star: Fraction
    X_minus_n_star: Fraction
    R_difference_raw: tuple[int, int]
    X_difference_raw: tuple[int, int]
    endpoint_lift_quotient: int

    @classmethod
    def from_valuations(
        cls, valuations: tuple[int, ...] | list[int] | str
    ) -> "AffineCenterState":
        ks = parse_ks(valuations)
        if not ks:
            raise ValueError("the affine center is undefined for the empty code")
        compatibility = CompatibilityState.from_valuations(ks)
        gap = compatibility.two_power - compatibility.three_power
        if gap == 0:
            raise ArithmeticError("a nonempty code cannot have 2^K = 3^m")
        n_star = Fraction(compatibility.C, gap)
        R_raw = (gap * compatibility.R - compatibility.C, gap)
        X_raw = (
            gap * compatibility.canonical_endpoint - compatibility.C,
            gap,
        )
        endpoint_delta = compatibility.canonical_endpoint - compatibility.M
        if endpoint_delta < 0 or endpoint_delta % compatibility.three_power:
            raise ArithmeticError("endpoint is not a nonnegative 3-adic lift of M")
        state = cls(
            valuations=ks,
            m=compatibility.m,
            K=compatibility.K,
            C=compatibility.C,
            R=compatibility.R,
            X=compatibility.canonical_endpoint,
            M=compatibility.M,
            two_power=compatibility.two_power,
            three_power=compatibility.three_power,
            gap=gap,
            n_star=n_star,
            R_minus_n_star=Fraction(*R_raw),
            X_minus_n_star=Fraction(*X_raw),
            R_difference_raw=R_raw,
            X_difference_raw=X_raw,
            endpoint_lift_quotient=endpoint_delta // compatibility.three_power,
        )
        if not state.validates():
            raise ArithmeticError("affine-center construction failed validation")
        return state

    @property
    def regime(self) -> AffineRegime:
        return (
            AffineRegime.CONTRACTING
            if self.gap > 0
            else AffineRegime.EXPANDING
        )

    @property
    def homogeneous_factor(self) -> Fraction:
        return Fraction(self.three_power, self.two_power)

    @property
    def R_difference_reduced(self) -> tuple[int, int]:
        return _fraction_pair(self.R_minus_n_star)

    @property
    def X_difference_reduced(self) -> tuple[int, int]:
        return _fraction_pair(self.X_minus_n_star)

    def partition(self, critical_gap: int) -> str:
        """Classify with a caller-specified exact absolute-gap threshold."""
        if (
            isinstance(critical_gap, bool)
            or not isinstance(critical_gap, int)
            or critical_gap < 0
        ):
            raise ValueError("critical_gap must be an integer >= 0")
        if abs(self.gap) <= critical_gap:
            return "critical-near"
        return self.regime.value

    def validates(self) -> bool:
        try:
            compatibility = CompatibilityState.from_valuations(self.valuations)
        except (ArithmeticError, TypeError, ValueError):
            return False
        return (
            self.m == compatibility.m
            and self.K == compatibility.K
            and self.C == compatibility.C
            and self.R == compatibility.R
            and self.X == compatibility.canonical_endpoint
            and self.M == compatibility.M
            and self.two_power == 1 << self.K
            and self.three_power == 3**self.m
            and self.gap == self.two_power - self.three_power
            and self.gap != 0
            and self.n_star == Fraction(self.C, self.gap)
            and self.R_difference_raw
            == (self.gap * self.R - self.C, self.gap)
            and self.X_difference_raw
            == (self.gap * self.X - self.C, self.gap)
            and self.R_minus_n_star == self.R - self.n_star
            and self.X_minus_n_star == self.X - self.n_star
            and self.X_minus_n_star
            == self.homogeneous_factor * self.R_minus_n_star
            and self.R_difference_raw[0] == self.two_power * (self.R - self.X)
            and self.X_difference_raw[0] == self.three_power * (self.R - self.X)
            and self.X == self.M + self.endpoint_lift_quotient * self.three_power
            and self.endpoint_lift_quotient >= 0
        )

    def exact_inequalities(self) -> dict[str, bool]:
        """Universal geometry checks, specialized to this state."""
        common = {
            "M_le_X": self.M <= self.X,
            "center_scaling": self.X_minus_n_star
            == self.homogeneous_factor * self.R_minus_n_star,
            "same_side_of_center": (
                self.R_minus_n_star * self.X_minus_n_star >= 0
            ),
        }
        if self.regime is AffineRegime.EXPANDING:
            common.update(
                {
                    "n_star_negative": self.n_star < 0,
                    "n_star_lt_M": self.n_star < self.M,
                    "n_star_lt_R": self.n_star < self.R,
                    "R_lt_X": self.R < self.X,
                    "center_distance_expands": abs(self.R_minus_n_star)
                    < abs(self.X_minus_n_star),
                }
            )
        else:
            common.update(
                {
                    "n_star_positive": self.n_star > 0,
                    "center_distance_contracts": abs(self.X_minus_n_star)
                    <= abs(self.R_minus_n_star),
                    "equal_distance_iff_fixed": (
                        abs(self.X_minus_n_star)
                        == abs(self.R_minus_n_star)
                    )
                    == (self.R == self.X),
                    "R_and_X_order_matches_center_side": (
                        (self.R < self.X and self.R < self.n_star)
                        or (self.R > self.X and self.R > self.n_star)
                        or self.R == self.X == self.n_star
                    ),
                }
            )
        return common

    def as_dict(self, critical_gap: int = 0) -> dict[str, object]:
        return {
            "valuations": list(self.valuations),
            "m": self.m,
            "K": self.K,
            "C": self.C,
            "R": self.R,
            "X": self.X,
            "M": self.M,
            "two_power": self.two_power,
            "three_power": self.three_power,
            "gap": self.gap,
            "absolute_gap": abs(self.gap),
            "regime": self.regime.value,
            "partition": self.partition(critical_gap),
            "n_star": list(_fraction_pair(self.n_star)),
            "R_minus_n_star_raw": list(self.R_difference_raw),
            "R_minus_n_star_reduced": list(self.R_difference_reduced),
            "X_minus_n_star_raw": list(self.X_difference_raw),
            "X_minus_n_star_reduced": list(self.X_difference_reduced),
            "homogeneous_factor": list(_fraction_pair(self.homogeneous_factor)),
            "endpoint_lift_quotient": self.endpoint_lift_quotient,
            "inequalities": self.exact_inequalities(),
            "status": "EXACT",
        }
