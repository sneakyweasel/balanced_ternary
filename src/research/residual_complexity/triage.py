"""Exact Phase-0 census of unrestricted residual complexity C_F(m,r).

C_F(m,r) counts ≡_r right-language types among all residual polynomials
of F after exactly m input trits. There is no safety/live filter and no
remaining-horizon clock: two residuals are identified only when they
emit the same output word on every input of length r.

Finite-horizon types are Newton residues Φ_r (equivalently, for degree
≤ 2, coefficient triples mod 3^r). Sample signatures and clocked
unfoldings are a different predicate.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product

from bt.calculus.myhill_nerode import levelled_mealy_count, reachable_layers
from bt.calculus.poly_congruence import phi_k
from bt.calculus.quadratic import invariant_mod, quadratic_residual_formula
from bt.calculus.residual import TRITS, delta, rho
from bt.calculus.section import IntPoly, parse_poly

MAX_DEPTH = 7
X = parse_poly("x")
X2 = parse_poly("x^2")

# Unrestricted C_{x^2}(m,r) for m,r ≤ 7. COMPUTATIONALLY VERIFIED.
X2_CENSUS: tuple[tuple[int, ...], ...] = (
    (1, 1, 1, 1, 1, 1, 1, 1),
    (1, 3, 3, 3, 3, 3, 3, 3),
    (1, 6, 9, 9, 9, 9, 9, 9),
    (1, 9, 24, 27, 27, 27, 27, 27),
    (1, 9, 50, 78, 81, 81, 81, 81),
    (1, 9, 77, 212, 240, 243, 243, 243),
    (1, 9, 81, 463, 694, 726, 729, 729),
    (1, 9, 81, 711, 1885, 2156, 2184, 2187),
)

# Live safety types for Y={0,+}^ω at horizon 7. Contrast only; not C_F.
SAFETY_HORIZON7: tuple[int, ...] = (1, 3, 7, 16, 33, 66, 131, 260)


def _require_nat(n: int, name: str = "n") -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a nonnegative int")
    return n


def type_key(g: IntPoly, r: int) -> tuple[int, ...]:
    """Canonical ≡_r invariant: Newton residues modulo 3^r."""

    return phi_k(g, _require_nat(r, "r"))


@lru_cache(maxsize=None)
def mealy_signature(coeffs: tuple[int, ...], r: int) -> object:
    """Exact remaining-horizon Mealy right-language signature."""

    r = _require_nat(r, "r")
    if r == 0:
        return ()
    g = IntPoly(coeffs)
    return tuple((rho(g, a), mealy_signature(delta(g, a).coeffs, r - 1)) for a in TRITS)


def residuals_at(f: IntPoly, m: int) -> list[IntPoly]:
    """Distinct residual polynomials after exactly ``m`` input letters."""

    return reachable_layers(f, _require_nat(m, "m"))[_require_nat(m, "m")]


def census_count(f: IntPoly, m: int, r: int) -> int:
    """``C_F(m,r)``: number of ≡_r types among unrestricted depth-``m`` residuals."""

    return len({type_key(g, r) for g in residuals_at(f, m)})


def census_table(f: IntPoly, max_depth: int = MAX_DEPTH) -> tuple[tuple[int, ...], ...]:
    """Rows are depths ``m=0..max_depth``; columns are horizons ``r=0..max_depth``."""

    max_depth = _require_nat(max_depth, "max_depth")
    layers = reachable_layers(f, max_depth)
    rows = []
    for m in range(max_depth + 1):
        rows.append(tuple(len({type_key(g, r) for g in layers[m]}) for r in range(max_depth + 1)))
    return tuple(rows)


def census_count_mealy(f: IntPoly, m: int, r: int) -> int:
    """``C_F(m,r)`` by remaining-horizon Mealy signatures (cross-check)."""

    return len({mealy_signature(g.coeffs, r) for g in residuals_at(f, m)})


def census_count_quad(f: IntPoly, m: int, r: int) -> int:
    """Degree-≤2 coefficient form of ``C_F(m,r)``."""

    return len({invariant_mod(g, r) for g in residuals_at(f, m)})


def x2_proved_count(m: int, r: int) -> int | None:
    """Closed value of ``C_{x^2}(m,r)`` on the proved band, else ``None``.

    The band is ``r = 0``, ``r ≥ m``, and the superdiagonal ``r = m-1``
    for ``m ≥ 2``. Interior cells ``0 < r < m-1`` are not claimed.
    """

    m = _require_nat(m, "m")
    r = _require_nat(r, "r")
    if r == 0:
        return 1
    if r >= m:
        return 3**m
    if r == m - 1:
        return 3**m - 3
    return None


def type_cap(m: int, r: int) -> int:
    """``min(3^m, 3^{2r})`` with the convention ``3^{0}=1`` at ``r=0``."""

    m = _require_nat(m, "m")
    r = _require_nat(r, "r")
    return min(3**m, 3 ** (2 * r) if r else 1)


def half_repunit(r: int) -> int:
    """``(3^r-1)/2 = pack((+)^r)``."""

    r = _require_nat(r, "r")
    return (3**r - 1) // 2


def squared_half_repunit_digits(r: int) -> tuple[int, ...]:
    """Balanced digits of ``((3^r-1)/2)^2``.

    If ``r=2k`` the word is ``(+-)^k (--+)^k`` in the sense
    ``(+,-)^k ⌢ (-,+)^k``. If ``r=2k+1`` it is
    ``(+,-)^k ⌢ (+,0) ⌢ (-,+)^k``. Digit ``r`` is never ``+1``.
    """

    r = _require_nat(r, "r")
    if r == 0:
        return ()
    if r % 2 == 0:
        k = r // 2
        return (1, -1) * k + (-1, 1) * k
    k = (r - 1) // 2
    return (1, -1) * k + (1, 0) + (-1, 1) * k


def superdiagonal_pairs(m: int) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """The three colliding pairs at depth ``m`` and horizon ``m-1``.

    For each ``σ ∈ {-1,0,+1}``, the two length-``m`` extensions of
    ``σ^{m-1}`` by a trit other than ``σ`` are ≡_{m-1}-equivalent.
    """

    m = _require_nat(m, "m")
    if m < 2:
        raise ValueError("superdiagonal pairs start at m=2")
    r = m - 1
    pairs = []
    for sigma in TRITS:
        base = (sigma,) * r
        others = tuple(eps for eps in TRITS if eps != sigma)
        pairs.append((base + (others[0],), base + (others[1],)))
    return tuple(pairs)


def prefixes(m: int) -> tuple[tuple[int, ...], ...]:
    m = _require_nat(m, "m")
    if m == 0:
        return ((),)
    return tuple(product(TRITS, repeat=m))


def colliding_pairs_at(m: int, r: int) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """All unordered prefix pairs at depth ``m`` that are ≡_r-equivalent."""

    m = _require_nat(m, "m")
    r = _require_nat(r, "r")
    buckets: dict[object, list[tuple[int, ...]]] = {}
    for word in prefixes(m):
        key = invariant_mod(quadratic_residual_formula(word), r)
        buckets.setdefault(key, []).append(word)
    out: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for group in buckets.values():
        for i, left in enumerate(group):
            for right in group[i + 1 :]:
                out.append((left, right))
    return out


def linear_is_constant_one(max_depth: int = MAX_DEPTH) -> dict[str, object]:
    table = census_table(X, max_depth)
    types = {count for row in table for count in row}
    clock = tuple(levelled_mealy_count(X, k) for k in range(max_depth + 1))
    return {
        "table": table,
        "unique_counts": sorted(types),
        "single_type": types == {1},
        "clock": clock,
        "clock_grows": clock == tuple(range(max_depth + 1)),
    }


def simple_formula_failures(table: tuple[tuple[int, ...], ...]) -> dict[str, object]:
    """Refute 3^{min(m,r)} and the coefficient cap as exact two-parameter laws."""

    max_depth = len(table) - 1
    min_exp = []
    cap = []
    for m in range(max_depth + 1):
        min_row = []
        cap_row = []
        for r in range(max_depth + 1):
            min_row.append(table[m][r] != 3 ** min(m, r))
            cap_row.append(table[m][r] != type_cap(m, r))
        min_exp.append(tuple(min_row))
        cap.append(tuple(cap_row))
    return {
        "not_three_min": any(any(row) for row in min_exp),
        "not_coefficient_cap": any(any(row) for row in cap),
        "witness_three_min": (2, 1, table[2][1], 3),
        "witness_cap": (2, 1, table[2][1], 9),
    }


def triage_report(max_depth: int = MAX_DEPTH) -> dict[str, object]:
    max_depth = _require_nat(max_depth, "max_depth")
    linear = linear_is_constant_one(max_depth)
    table = census_table(X2, max_depth)
    band_ok = True
    interior = 0
    for m in range(max_depth + 1):
        for r in range(max_depth + 1):
            proved = x2_proved_count(m, r)
            if proved is None:
                interior += 1
            elif proved != table[m][r]:
                band_ok = False
    failures = simple_formula_failures(table)
    safety_col = SAFETY_HORIZON7[: max_depth + 1]
    unrestricted_h7 = tuple(table[m][max_depth] for m in range(max_depth + 1))
    return {
        "polynomials": ["x", "x^2"],
        "max_depth": max_depth,
        "linear": linear,
        "x2_census": table,
        "band_formula_holds": band_ok,
        "interior_cells": interior,
        "formula_failures": failures,
        "safety_horizon7": list(safety_col),
        "unrestricted_last_column": list(unrestricted_h7),
        "differs_from_safety": list(safety_col) != list(unrestricted_h7)
        if max_depth == MAX_DEPTH
        else True,
        "not_a_clock": linear["single_type"] and linear["clock_grows"],
        "ahmed_savchuk_unrestricted_infinite": True,
    }
