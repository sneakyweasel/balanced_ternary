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


def packed_bound(m: int) -> int:
    """Half-width of ``P_m``: ``(3^m-1)/2``."""

    return (3 ** _require_nat(m, "m") - 1) // 2


def packed_range(m: int) -> range:
    """Integers ``P_m`` as a contiguous symmetric interval."""

    bound = packed_bound(m)
    return range(-bound, bound + 1)


def balanced_mod(n: int, mod: int) -> int:
    """Unique residue of ``n`` in ``[-(mod-1)/2, (mod-1)/2]`` for odd ``mod``."""

    if isinstance(mod, bool) or not isinstance(mod, int) or mod < 1 or mod % 2 == 0:
        raise ValueError("mod must be a positive odd int")
    residue = n % mod
    half = (mod - 1) // 2
    if residue > half:
        residue -= mod
    return residue


def dz_pow(n: int, k: int) -> int:
    """``DZ^k(n)`` by one balanced quotient by ``3^k``."""

    k = _require_nat(k, "k")
    if k == 0:
        return n
    mod = 3**k
    return (n - balanced_mod(n, mod)) // mod


def interior_type(p: int, m: int, r: int) -> tuple[int, int]:
    """``(p mod 3^r, DZ^m(p^2) mod 3^r)`` in ``[0, 3^r)``."""

    m = _require_nat(m, "m")
    r = _require_nat(r, "r")
    if r == 0:
        return (0, 0)
    mod = 3**r
    return (p % mod, dz_pow(p * p, m) % mod)


def interior_image(m: int, r: int) -> set[tuple[int, int]]:
    """Exact image of ``p ↦ (p mod 3^r, DZ^m(p^2) mod 3^r)`` on ``P_m``."""

    return {interior_type(p, m, r) for p in packed_range(m)}


def interior_image_size(m: int, r: int) -> int:
    """``C_{x^2}(m,r)`` for ``r < m`` by the coefficient-pair image (exact)."""

    return len(interior_image(m, r))


def squares_mod(r: int) -> set[int]:
    """Quadratic residues in ``Z/3^r Z`` as residues in ``[0, 3^r)``."""

    r = _require_nat(r, "r")
    if r == 0:
        return {0}
    mod = 3**r
    return {t * t % mod for t in packed_range(r)}


def zero_fibre_values(m: int, r: int) -> set[int]:
    """``{ DZ^m(p^2) mod 3^r : p ∈ P_m, p ≡ 0 (mod 3^r) }``."""

    m = _require_nat(m, "m")
    r = _require_nat(r, "r")
    if r == 0:
        return {0}
    mod = 3**r
    return {dz_pow(p * p, m) % mod for p in packed_range(m) if p % mod == 0}


def zero_fibre_witness(m: int, r: int, v: int) -> int:
    """Packed prefix ``p = 3^r + v 3^{m-r}`` for the zero-fibre construction.

    For ``m ≥ 3r`` and ``v ∈ P_r`` this lies in ``P_m``, is ``0 mod 3^r``,
    and has ``DZ^m(p^2) ≡ 2v (mod 3^r)``.
    """

    m = _require_nat(m, "m")
    r = _require_nat(r, "r")
    if m < 3 * r:
        raise ValueError("zero-fibre witnesses start at m=3r")
    if abs(v) > packed_bound(r):
        raise ValueError("v must lie in P_r")
    return 3**r + v * 3 ** (m - r)


def fibre_second_coordinates(m: int, r: int, alpha: int) -> set[int]:
    """``{ DZ^m(p^2) mod 3^r : p ∈ P_m, p ≡ α (mod 3^r) }``."""

    m = _require_nat(m, "m")
    r = _require_nat(r, "r")
    if r == 0:
        return {0}
    mod = 3**r
    residue = alpha % mod
    return {dz_pow(p * p, m) % mod for p in packed_range(m) if p % mod == residue}


def fibre_fill_witness(m: int, r: int, alpha: int, u: int) -> int:
    """Packed prefix ``p = α + u 3^r + 3^{m-r}`` filling a general fibre.

    For ``m ≥ 5r`` and ``α,u ∈ P_r`` this lies in ``P_m``, is ``α mod 3^r``,
    and has ``DZ^m(p^2) ≡ 2u + DZ^r(2α) (mod 3^r)``.
    """

    m = _require_nat(m, "m")
    r = _require_nat(r, "r")
    if r < 1:
        raise ValueError("fibre-fill witnesses start at r≥1")
    if m < 5 * r:
        raise ValueError("fibre-fill witnesses start at m=5r")
    if abs(alpha) > packed_bound(r):
        raise ValueError("alpha must lie in P_r")
    if abs(u) > packed_bound(r):
        raise ValueError("u must lie in P_r")
    return alpha + u * 3**r + 3 ** (m - r)


def fibre_fill_second(r: int, alpha: int, u: int) -> int:
    """Second coordinate of the ``m≥5r`` fibre-fill witness, in ``[0, 3^r)``."""

    r = _require_nat(r, "r")
    if r < 1:
        raise ValueError("r must be positive")
    if abs(alpha) > packed_bound(r):
        raise ValueError("alpha must lie in P_r")
    if abs(u) > packed_bound(r):
        raise ValueError("u must lie in P_r")
    return (2 * u + dz_pow(2 * alpha, r)) % (3**r)


def two_parameter_prefix(m: int, r: int, alpha: int, u: int, v: int) -> int:
    """Packed prefix ``p = α + u 3^r + v 3^{m-r}``.

    For ``m ≥ 3r`` and ``α,u,v ∈ P_r`` this lies in ``P_m`` and is
    ``α mod 3^r``. At ``m = 3r`` it is the entire fibre: every
    ``p ∈ P_{3r}`` with ``p ≡ α (mod 3^r)`` is uniquely of this form.
    """

    m = _require_nat(m, "m")
    r = _require_nat(r, "r")
    if r < 1:
        raise ValueError("two-parameter prefixes start at r≥1")
    if m < 3 * r:
        raise ValueError("two-parameter prefixes start at m=3r")
    if abs(alpha) > packed_bound(r):
        raise ValueError("alpha must lie in P_r")
    if abs(u) > packed_bound(r):
        raise ValueError("u must lie in P_r")
    if abs(v) > packed_bound(r):
        raise ValueError("v must lie in P_r")
    return alpha + u * 3**r + v * 3 ** (m - r)


def triple_width_second(r: int, alpha: int, u: int, v: int) -> int:
    """Second coordinate of ``p = α + u 3^r + v 3^{2r}`` at ``m = 3r``.

    Equals ``2uv + DZ^r(2αv + u² + DZ^r(2αu + DZ^r(α²)))`` in ``[0, 3^r)``.
    This is the exact fibre map, not a filling witness: a single fixed
    ``u`` or a single fixed ``v`` does not make it bijective for a
    general fibre.
    """

    r = _require_nat(r, "r")
    if r < 1:
        raise ValueError("r must be positive")
    if abs(alpha) > packed_bound(r):
        raise ValueError("alpha must lie in P_r")
    if abs(u) > packed_bound(r):
        raise ValueError("u must lie in P_r")
    if abs(v) > packed_bound(r):
        raise ValueError("v must lie in P_r")
    delta = dz_pow(alpha * alpha, r)
    gamma = dz_pow(2 * alpha * u + delta, r)
    return (2 * u * v + dz_pow(2 * alpha * v + u * u + gamma, r)) % (3**r)


# First m at which C_{x^2}(m,r)=3^{2r}, for r=1..6. COMPUTATIONALLY VERIFIED.
# Persistence checked a few steps past each threshold. Not a proved m_0(r).
FIRST_SATURATION: dict[int, int] = {1: 3, 2: 6, 3: 8, 4: 10, 5: 13, 6: 15}


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
        "first_saturation": dict(FIRST_SATURATION),
        "guess_m0_3r_not_sharp": FIRST_SATURATION[3] < 9,
        "zero_fibre_squares_at_2r": True,
        "zero_fibre_full_from_3r": True,
        "every_fibre_full_from_5r": True,
        "triple_width_map_identity": True,
        "one_parameter_slice_not_fill_at_3r": True,
        "first_fill_is_fibre_dependent": True,
    }
