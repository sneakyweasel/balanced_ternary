"""Valuation cylinders for finite Collatz valuation prefixes.

For a word ``ks = (k_0, ..., k_{m-1})`` with each ``k_i >= 1``,

    C_ks = { n odd : v2(3 T^i(n) + 1) = k_i for 0 <= i < m }.

**PROVED:** at leftover precision ``Q = 1``, there is a unique residue class
modulo ``2^{1+K}`` (``K = sum k_i``). Its density among the ``2^K`` odd
residues is exactly ``2^{-K}``. Every finite word over ``{1,2,...}`` is
admissible at this *minimum* precision. Layer C ``FORBIDDEN`` labels are
relative to a *fixed* starting ``P`` that may be smaller than ``1+K``.

Construction: work backwards from the unique odd residue ``1 (mod 2)`` by
inverting ``T`` with exponent ``k``:

    n ≡ (2^k r - 1)  3^{-1}  (mod 2^{P+k}).

Never divide a residue modulo ``2^P`` by ``2^k``. The inverse formula
multiplies by ``2^k`` first, then subtracts 1 and multiplies by the
modular inverse of 3.

With leftover ``Q > 1`` there are ``2^{Q-1}`` classes modulo ``2^{Q+K}``.
"""

from __future__ import annotations

from dataclasses import dataclass

from collatz.automata.valuation_shift import (
    GrowthBudget,
    PrecisionState,
    follow_path,
    growth_budget,
)
from collatz.valuation import v2


def parse_ks(ks: object) -> tuple[int, ...]:
    """Accept a tuple/list of ints, or a comma-separated string ``'1,2,1'``."""
    if isinstance(ks, str):
        parts = [p.strip() for p in ks.split(",") if p.strip() != ""]
        if not parts:
            return ()
        try:
            values = tuple(int(p) for p in parts)
        except ValueError as exc:
            raise ValueError(f"ks must be comma-separated integers, got {ks!r}") from exc
        ks = values
    if not isinstance(ks, (tuple, list)):
        raise TypeError(f"ks must be a sequence of ints, got {type(ks).__name__}")
    out: list[int] = []
    for k in ks:
        if isinstance(k, bool) or not isinstance(k, int) or k < 1:
            raise ValueError(f"each k must be an integer >= 1, got {k!r}")
        out.append(k)
    return tuple(out)


def total_valuation(ks: tuple[int, ...]) -> int:
    return sum(ks)


def precision_cost(ks: tuple[int, ...], leftover_q: int = 1) -> int:
    """Initial 2-adic precision needed to finish with leftover ``Q``.

    ``P = Q + sum k_i``. Each exact-k step consumes ``k`` bits.
    """
    if isinstance(leftover_q, bool) or not isinstance(leftover_q, int) or leftover_q < 1:
        raise ValueError(f"leftover_q must be an integer >= 1, got {leftover_q!r}")
    return leftover_q + total_valuation(ks)


def min_precision(ks: tuple[int, ...], leftover_q: int = 1) -> int:
    return precision_cost(ks, leftover_q=leftover_q)


def _require_leftover(leftover_q: int) -> int:
    if isinstance(leftover_q, bool) or not isinstance(leftover_q, int) or leftover_q < 1:
        raise ValueError(f"leftover_q must be an integer >= 1, got {leftover_q!r}")
    return leftover_q


def inverse_collatz_residue(residue: int, precision: int, k: int) -> PrecisionState:
    """Unique preimage residue of ``T`` with exact exponent ``k``.

    If ``T(n) ≡ r (mod 2^P)``, then

        3n + 1 ≡ r * 2^k  (mod 2^{P+k}),
        n ≡ (r * 2^k - 1) * 3^{-1}  (mod 2^{P+k}).
    """
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError(f"k must be an integer >= 1, got {k!r}")
    if isinstance(precision, bool) or not isinstance(precision, int) or precision < 1:
        raise ValueError(f"precision must be an integer >= 1, got {precision!r}")
    new_p = precision + k
    modulus = 1 << new_p
    r = residue % (1 << precision)
    inv3 = pow(3, -1, modulus)
    n = ((r << k) - 1) * inv3 % modulus
    return PrecisionState(residue=n, precision=new_p)


def cylinder_residues(
    ks: tuple[int, ...], leftover_q: int = 1
) -> tuple[int, ...]:
    """Odd residues modulo ``2^{Q+K}`` that realise ``ks``. Sorted."""
    leftover_q = _require_leftover(leftover_q)
    ks = parse_ks(ks)
    starts = [
        PrecisionState(r, leftover_q)
        for r in range(1, 1 << leftover_q, 2)
    ]
    for k in reversed(ks):
        starts = [inverse_collatz_residue(st.residue, st.precision, k) for st in starts]
    residues = sorted({st.residue % (1 << st.precision) for st in starts})
    return tuple(residues)


def successive_valuations(n: int, length: int) -> tuple[int, ...]:
    """``(v2(3 T^i(n)+1) for i < length)`` for any nonzero odd ``n``."""
    if isinstance(n, bool) or not isinstance(n, int) or n % 2 == 0:
        raise ValueError(f"n must be a nonzero odd int, got {n!r}")
    if n == 0:
        raise ValueError("n must be nonzero")
    if isinstance(length, bool) or not isinstance(length, int) or length < 0:
        raise ValueError(f"length must be an integer >= 0, got {length!r}")
    out: list[int] = []
    x = n
    for _ in range(length):
        y = 3 * x + 1
        k = v2(y)
        if k is None:
            raise ArithmeticError("3n+1 was 0")
        out.append(k)
        x = y >> k
    return tuple(out)


def belongs_to_cylinder(n: int, ks: tuple[int, ...]) -> bool:
    """True iff odd ``n`` realises the valuation prefix ``ks``."""
    ks = parse_ks(ks)
    if isinstance(n, bool) or not isinstance(n, int) or n % 2 == 0 or n == 0:
        return False
    return successive_valuations(n, len(ks)) == ks


@dataclass(frozen=True)
class ValuationCylinder:
    ks: tuple[int, ...]
    leftover_q: int
    precision: int
    residues: tuple[int, ...]
    class_count: int
    odd_residue_count: int
    density_numerator: int
    density_denominator: int
    matches_haar: bool
    admissible: bool
    budget: GrowthBudget

    def contains_residue(self, n: int) -> bool:
        if isinstance(n, bool) or not isinstance(n, int):
            return False
        return (n % (1 << self.precision)) in self.residues

    def as_dict(self) -> dict[str, object]:
        return {
            "ks": list(self.ks),
            "leftover_q": self.leftover_q,
            "precision": self.precision,
            "residues": list(self.residues),
            "class_count": self.class_count,
            "odd_residue_count": self.odd_residue_count,
            "density_numerator": self.density_numerator,
            "density_denominator": self.density_denominator,
            "matches_haar": self.matches_haar,
            "admissible": self.admissible,
            "budget": self.budget.as_dict(),
        }

    def format(self) -> str:
        dens = (
            f"{self.density_numerator}/{self.density_denominator}"
            if self.density_denominator
            else "undefined"
        )
        haar = "2^{-K}" if self.leftover_q == 1 else f"2^{{Q-1-K}} with Q={self.leftover_q}"
        lines = [
            f"Valuation cylinder  ks={self.ks}  leftover_Q={self.leftover_q}",
            f"K=sum k={sum(self.ks)}  P=Q+K={self.precision}  "
            f"modulus=2^{self.precision}={1 << self.precision}",
            f"residue classes: {self.class_count}  "
            f"odd residues at this P: {self.odd_residue_count}",
            f"density among odd residues: {dens}  "
            f"matches Haar {haar}: {str(self.matches_haar).lower()}",
            f"admissible: {str(self.admissible).lower()}  "
            f"budget: 2^K={self.budget.two_power} vs 3^m={self.budget.three_power}  "
            f"{self.budget.kind}",
            f"residues: {self.residues if len(self.residues) <= 16 else list(self.residues[:16]) + ['...']}",
            "",
            "Density 2^{-K} among odds is PROVED for leftover Q=1. "
            "Growth budget is the homogeneous estimate, not a Lyapunov function.",
            "",
        ]
        return "\n".join(lines)


def valuation_cylinder(
    ks: tuple[int, ...] | str | list[int], leftover_q: int = 1
) -> ValuationCylinder:
    leftover_q = _require_leftover(leftover_q)
    ks = parse_ks(ks)
    p = precision_cost(ks, leftover_q=leftover_q)
    residues = cylinder_residues(ks, leftover_q=leftover_q)
    odd_count = 1 << (p - 1)
    n_cls = len(residues)
    k_sum = total_valuation(ks)
    expected = 1 << (leftover_q - 1)  # 2^{Q-1} classes; unique when Q=1
    return ValuationCylinder(
        ks=ks,
        leftover_q=leftover_q,
        precision=p,
        residues=residues,
        class_count=n_cls,
        odd_residue_count=odd_count,
        density_numerator=n_cls,
        density_denominator=odd_count,
        matches_haar=n_cls == expected,
        admissible=n_cls > 0,
        budget=growth_budget(ks) if ks else growth_budget(()),
    )


def verify_cylinder_against_follow_path(
    ks: tuple[int, ...], leftover_q: int = 1
) -> bool:
    """Cross-check the inverse construction against ``follow_path``."""
    cyl = valuation_cylinder(ks, leftover_q=leftover_q)
    p = cyl.precision
    matched: list[int] = []
    for r in range(1, 1 << p, 2):
        _, status = follow_path(PrecisionState(r, p), ks)
        if status == "ok":
            matched.append(r)
    return tuple(matched) == cyl.residues
