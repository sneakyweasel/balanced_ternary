"""Phase-0 visibility gate for same-depth fibres of x^4.

Closed form, Newton residues, and deficit-0/1 checks. Not a counting
line and not a cubic-layer clone. All census code stays out of ``bt.*``.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product

from bt.calculus.cubic import prefixes_at
from bt.calculus.poly_congruence import newton_coeffs, phi_k
from bt.calculus.quadratic import iter_dz, pack_word
from bt.calculus.residual import TRITS, residual_along
from bt.calculus.section import IntPoly
from bt.metrics import v3

X4 = IntPoly((0, 0, 0, 0, 1))
MAX_K = 7
DEFICITS = (0, 1)


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def quartic_coeffs(m: int, p: int) -> tuple[int, int, int, int, int]:
    """Monomial ``(A, B, C, D, E)`` of ``D^m((p + 3^m x)^4)``.

    ``A x^4 + B x^3 + C x^2 + D x + E`` with
    ``A = 3^{3m}``, ``B = 4 p 3^{2m}``, ``C = 6 p^2 3^m``,
    ``D = 4 p^3``, ``E = D^m(p^4)``.
    """

    m = _require_nat(m, "m")
    return (
        3 ** (3 * m),
        4 * p * 3 ** (2 * m),
        6 * p * p * 3**m,
        4 * p * p * p,
        iter_dz(p**4, m),
    )


def quartic_residual(m: int, p: int) -> IntPoly:
    A, B, C, D, E = quartic_coeffs(m, p)
    return IntPoly((E, D, C, B, A))


def quartic_residual_formula(word: tuple[int, ...]) -> IntPoly:
    return quartic_residual(len(word), pack_word(word))


def newton_of_residual(m: int, p: int) -> tuple[int, ...]:
    return newton_coeffs(quartic_residual(m, p))


def F_k(m: int, p: int, k: int) -> tuple[int, ...]:
    return phi_k(quartic_residual(m, p), k)


def n0_scaled_fourth(u: int, m: int, r: int) -> int:
    """Two-regime leftover of ``D^m((3^r u)^4)``."""

    m = _require_nat(m, "m")
    r = _require_nat(r, "r")
    if m <= 4 * r:
        return (3 ** (4 * r - m)) * (u**4)
    return iter_dz(u**4, m - 4 * r)


def leftover_matches(p: int, m: int, r: int) -> bool:
    if r and p % (3**r):
        return False
    u = p // (3**r) if r else p
    return iter_dz(p**4, m) == n0_scaled_fourth(u, m, r)


def _visible_iff(values: dict[int, int], key_of, r: int, k: int) -> bool:
    """``value(p) ≡ value(q) (mod 3^k)`` iff ``key(p) = key(q)``."""

    mod = 3**k if k else 1
    n_to_key: dict[int, set[object]] = defaultdict(set)
    key_to_n: dict[object, set[int]] = defaultdict(set)
    for p, val in values.items():
        key = key_of(p)
        residue = val % mod
        n_to_key[residue].add(key)
        key_to_n[key].add(residue)
    return all(len(s) == 1 for s in n_to_key.values()) and all(
        len(s) == 1 for s in key_to_n.values()
    )


def _visible_iff_residue(values: dict[int, int], r: int, k: int) -> bool:
    """``value(p) ≡ value(q) (mod 3^k)`` iff ``p ≡ q (mod 3^r)``."""

    res_mod = 3**r if r else 1
    return _visible_iff(values, lambda p: p % res_mod, r, k)


def _group_by(values: dict[int, int], k: int) -> dict[int, list[int]]:
    mod = 3**k if k else 1
    groups: dict[int, list[int]] = defaultdict(list)
    for p, val in values.items():
        groups[val % mod].append(p)
    return dict(groups)


def layer_report(k: int, r: int) -> dict[str, object]:
    k = _require_nat(k, "k")
    r = _require_nat(r, "r")
    if r + 1 > k:
        raise ValueError("need r+1 <= k")
    m = k - 1 - r
    prefixes = list(prefixes_at(m))
    newtons = {p: newton_of_residual(m, p) for p in prefixes}
    phis = {p: F_k(m, p, k) for p in prefixes}
    vis = []
    sees_square = []
    constant = []
    for j in range(5):
        coord = {p: newtons[p][j] if j < len(newtons[p]) else 0 for p in prefixes}
        vis.append(_visible_iff_residue(coord, r, k))
        res_mod = 3**r if r else 1
        sees_square.append(_visible_iff(coord, lambda p, rm=res_mod: (p * p) % rm, r, k))
        constant.append(len({v % (3**k if k else 1) for v in coord.values()}) <= 1)
    visible_js = [j for j, ok in enumerate(vis) if ok]
    after: dict[str, object] = {}
    if visible_js:
        j0 = visible_js[0]
        coord = {p: newtons[p][j0] if j0 < len(newtons[p]) else 0 for p in prefixes}
        groups = _group_by(coord, k)
        fibres = [sorted(g) for g in groups.values() if len(g) > 1]
        low_val_split = True
        core_in_pow = True
        for fibre in fibres:
            for p in fibre:
                if v3(p) is not None and v3(p) < r and any(q != p for q in fibre):
                    low_val_split = False
                if r and p % (3**r):
                    core_in_pow = False
        after = {
            "visible_index": j0,
            "nontrivial_fibres": len(fibres),
            "low_val_injective": low_val_split,
            "nontrivial_in_3rZ": core_in_pow or not fibres,
            "sample_fibre": fibres[0][:8] if fibres else [],
        }
    leftover_ok = all(leftover_matches(p, m, r) for p in prefixes if r == 0 or p % (3**r) == 0)
    real_groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for p, phi in phis.items():
        real_groups[phi].append(p)
    return {
        "k": k,
        "r": r,
        "m": m,
        "prefix_count": len(prefixes),
        "visibility": vis,
        "visible_indices": visible_js,
        "sees_square": sees_square,
        "constant": constant,
        "after_visibility": after,
        "leftover_two_regime": leftover_ok,
        "same_depth_classes": len(real_groups),
        "nontrivial_phi_fibres": sum(1 for g in real_groups.values() if len(g) > 1),
    }


def visibility_scan(max_k: int = MAX_K) -> list[dict[str, object]]:
    max_k = _require_nat(max_k, "max_k")
    rows = []
    for k in range(2, max_k + 1):
        for r in DEFICITS:
            if r + 1 <= k:
                rows.append(layer_report(k, r))
    return rows


def linear_coeff_valuation(m: int, p: int) -> int | None:
    """``v_3`` of the linear-in-``p`` monomial coefficient ``4 p 3^{2m}``.

    For ``3`` not dividing ``p`` this is ``2m``. Degree 3 had valuation
    ``m``; the extra factor of ``3^m`` is why ``N_3`` vanishes at
    deficits ``0`` and ``1``.
    """

    m = _require_nat(m, "m")
    coeff = 4 * p * 3 ** (2 * m)
    return v3(coeff)


def n2_square_residue(p: int, k: int) -> int:
    """Exact ``N_2`` at deficit ``1``: ``4 p^2 3^{k-1}`` modulo ``3^k``."""

    k = _require_nat(k, "k")
    if k < 2:
        raise ValueError("need k >= 2")
    mod = 3**k
    return (4 * p * p * 3 ** (k - 1)) % mod


def degree_increment_pattern(rows: list[dict[str, object]]) -> bool:
    """True when visibility is exactly the cubic pattern with N2↦N3."""

    r1 = [row for row in rows if row["r"] == 1 and row["k"] >= 4]
    if not r1:
        return False
    return all(row["visible_indices"] == [3] for row in r1)


def phase0_verdict(rows: list[dict[str, object]]) -> str:
    """``CLOSE``: no residue visibility at ``r=1`` once ``|P_m|>3``."""

    r1 = [row for row in rows if row["r"] == 1 and row["k"] >= 4]
    if not r1:
        return "PARK"
    if any(row["visible_indices"] for row in r1):
        if degree_increment_pattern(rows):
            return "CLOSE"
        return "PROMOTE"
    return "CLOSE"


def triage_report(max_k: int = 5) -> dict[str, object]:
    max_k = _require_nat(max_k, "max_k")
    formula_ok = True
    for m in range(4):
        for word in product(TRITS, repeat=m):
            if quartic_residual_formula(word) != residual_along(X4, word):
                formula_ok = False
                break
        if not formula_ok:
            break
    rows = visibility_scan(max_k)
    leftover = all(row["leftover_two_regime"] for row in rows)
    increment = degree_increment_pattern(rows)
    r1_stable = [row for row in rows if row["r"] == 1 and row["k"] >= 4]
    return {
        "max_k": max_k,
        "formula_matches_residual_along": formula_ok,
        "leftover_two_regime": leftover,
        "degree_increment_n3": increment,
        "r1_has_visibility": any(row["visible_indices"] for row in r1_stable),
        "n2_sees_square": all(row["sees_square"][2] for row in r1_stable),
        "verdict": phase0_verdict(rows),
        "rows": rows,
    }
