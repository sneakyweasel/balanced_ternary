"""Baranwal order-(m) Gamma-system: place values and valuation.

Definition transcribed from Baranwal, thesis §5.3, pp. 49–50.
This is not a general numeration framework.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class OstrowskiSystem:
    """Order-m system given by eventually periodic partial quotients.

    ``periods[k-1]`` is the repeating tail of ``α_k = [0; d_{k,1}, …]``.
    ``preperiods[k-1]`` is the non-repeating prefix of those partial
    quotients, possibly empty. Indices ``k`` and ``i`` are 1-based, as
    in the thesis.
    """

    preperiods: tuple[tuple[int, ...], ...]
    periods: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        if len(self.preperiods) != len(self.periods):
            raise ValueError("preperiods and periods must have length m")
        if not self.periods:
            raise ValueError("order m must be at least 1")
        for k, (pre, per) in enumerate(zip(self.preperiods, self.periods), start=1):
            if not per:
                raise ValueError(f"α_{k} period must be nonempty")
            if any(d < 1 for d in pre + per):
                raise ValueError(f"α_{k} partial quotients must be positive")

    @property
    def order(self) -> int:
        return len(self.periods)

    def d(self, k: int, i: int) -> int:
        """Partial quotient ``d_{k,i}`` (both indices 1-based)."""
        if not (1 <= k <= self.order):
            raise ValueError(f"k={k} out of range for order {self.order}")
        if i < 1:
            raise ValueError(f"i={i} must be >= 1")
        pre = self.preperiods[k - 1]
        per = self.periods[k - 1]
        if i <= len(pre):
            return pre[i - 1]
        return per[(i - 1 - len(pre)) % len(per)]

    def place_value(self, i: int) -> int:
        """``q_i``: 0 if ``i<0``, 1 if ``i=0``, else the §5.3 recurrence."""
        if i < 0:
            return 0
        return self.place_values(i + 1)[i]

    def place_values(self, n: int) -> tuple[int, ...]:
        """``(q_0, …, q_{n-1})`` computed iteratively."""
        if n < 0:
            raise ValueError("n must be nonnegative")
        m = self.order
        qs: list[int] = []
        for i in range(n):
            if i == 0:
                qs.append(1)
                continue
            total = 0
            for k in range(1, m + 1):
                j = i - k
                qj = 0 if j < 0 else qs[j]
                total += self.d(k, i) * qj
            qs.append(total)
        return tuple(qs)

    def val(self, digits: Sequence[int]) -> int:
        """``sum a_i q_i`` with ``digits[i] = a_i`` (LSD first)."""
        qs = self.place_values(len(digits))
        return sum(a * q for a, q in zip(digits, qs))

    def pad(self, digits: Sequence[int], length: int) -> tuple[int, ...]:
        """Pad MSD (the high end) with zeros to ``length``."""
        if length < len(digits):
            raise ValueError("cannot pad to a shorter length")
        extra = length - len(digits)
        return tuple(digits) + (0,) * extra


def ostrowski_order2(
    preperiod: tuple[int, ...],
    period: tuple[int, ...],
) -> OstrowskiSystem:
    """Classical Ostrowski as order-2: ``Γ = (α, φ-1)``, ``φ-1 = [0; 1̄]``."""
    return OstrowskiSystem(
        preperiods=(preperiod, ()),
        periods=(period, (1,)),
    )


def fibonacci_system() -> OstrowskiSystem:
    """Zeckendorf / Fibonacci: ``α = [0; 2, 1̄]``."""
    return ostrowski_order2((2,), (1,))


def pell_system() -> OstrowskiSystem:
    """Pell: ``α = [0; 2̄]``."""
    return ostrowski_order2((), (2,))


def phase0_order3() -> OstrowskiSystem:
    """Phase-0 genuine order-3: ``Γ = ([0; 2̄], [0; 1̄], [0; 1̄])``."""
    return OstrowskiSystem(
        preperiods=((), (), ()),
        periods=((2,), (1,), (1,)),
    )


def nonpisot_order3() -> OstrowskiSystem:
    """Spectral comparison: ``Γ = ([0; 2̄], [0; 1̄], [0; 3̄])``.

    Same ``d_1=2``, ``d_2=1`` as ``phase0_order3``, so the memoryless
    digit alphabets agree. Only ``d_3`` changes (1 to 3). Characteristic
    polynomial ``x^3-2x^2-x-3`` is an irreducible Perron non-Pisot cubic.
    """
    return OstrowskiSystem(
        preperiods=((), (), ()),
        periods=((2,), (1,), (3,)),
    )


def characteristic_poly_coeffs(system: OstrowskiSystem) -> tuple[int, ...] | None:
    """Constant-coefficient characteristic polynomial, or None if not constant.

    Returns ``(c_m, …, c_0)`` for ``x^m - d_1 x^{m-1} - ⋯ - d_m``,
    using the first column of partial quotients when every ``α_k`` is
    purely periodic of length 1.
    """
    if any(system.preperiods[k] or len(system.periods[k]) != 1 for k in range(system.order)):
        return None
    m = system.order
    return (1, *( -system.d(k, 1) for k in range(1, m + 1)))
