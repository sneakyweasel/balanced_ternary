"""N0 scaling on the 3^r-divisible locus after the N2+N1 filter.

On ``p = 3^r u`` one has ``p^3 = 3^{3r} u^3``.  Iterating ``D(3n)=n``
gives the two-regime identity

    D^m(p^3) = 3^{3r-m} u^3     if m ≤ 3r,
    D^m(p^3) = D^{m-3r}(u^3)    if m ≥ 3r.

With ``m = k-1-r`` this is ``k ≤ 4r+1`` versus ``k ≥ 4r+1``.
The exhausted case is the same ``D``-process on ``u^3``, but it is
**not** a standard cubic residual instance: the prefix width is
``k-1-2r`` while the remaining depth is ``k-1-4r``, and the modulus
stays ``3^k``.
"""

from __future__ import annotations

from collections import defaultdict

from bt.calculus.cubic_fibres import balanced_bound, prefixes_at, same_depth_n0
from bt.calculus.cubic_n1_valuation import deficit_depth, n21_agree, n21_fibre_of
from bt.calculus.quadratic import iter_dz
from bt.metrics import v3


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def reduced_depth(k: int, r: int) -> int:
    """``t = m-3r = k-1-4r``, or 0 when the valuation is not exhausted."""
    k = _require_nat(k, "k")
    r = _require_nat(r, "r")
    m = deficit_depth(k, r)
    return max(m - 3 * r, 0)


def n0_regime(k: int, r: int) -> str:
    m = deficit_depth(k, r)
    if m < 3 * r:
        return "unexhausted"
    if m == 3 * r:
        return "boundary"
    return "exhausted"


def n0_scaled(u: int, k: int, r: int) -> int:
    """Exact integer ``D^m((3^r u)^3)`` from the two-regime formula."""
    m = deficit_depth(k, r)
    if m <= 3 * r:
        return (3 ** (3 * r - m)) * (u**3)
    return iter_dz(u**3, m - 3 * r)


def n0_original(u: int, k: int, r: int) -> int:
    """``D^m((3^r u)^3)`` by iterating ``D``."""
    m = deficit_depth(k, r)
    return iter_dz((3**r * u) ** 3, m)


def n0_candidate_deepest(u: int, k: int, r: int) -> int:
    """Naive candidate: deepest ``N0`` at the Milestone-24 ``N1`` horizon ``k-2r``."""
    if k < 2 * r + 1:
        raise ValueError("need k ≥ 2r+1 for the N1 reduced horizon")
    return iter_dz(u**3, k - 2 * r - 1)


def u_prefixes(k: int, r: int) -> range:
    """Integers ``u`` such that ``3^r u`` lies in ``P_m``."""
    m = deficit_depth(k, r)
    if m < r:
        return range(0, 1)
    return prefixes_at(m - r)


def n0_mod(u: int, k: int, r: int) -> int:
    return n0_scaled(u, k, r) % (3**k if k else 1)


def n0_agree(u: int, v: int, k: int, r: int) -> bool:
    return n0_mod(u, k, r) == n0_mod(v, k, r)


def n0_visibility_bound(t: int, k: int) -> int:
    """Sufficient integer bound: ``u ≡ v (mod 3^s)`` implies ``D^t(u^3) ≡ D^t(v^3) (mod 3^k)``.

    The algebraic argument gives ``s = max(1, t+k-1)``.
    """
    t = _require_nat(t, "t")
    k = _require_nat(k, "k")
    return max(1, t + k - 1)


def n0_visible_mod(t: int, k: int, s: int, u: int, v: int) -> bool:
    if (u - v) % (3**s) != 0:
        return True
    return (iter_dz(u**3, t) - iter_dz(v**3, t)) % (3**k if k else 1) == 0


def n0_fibre_after_n21(p: int, k: int, r: int) -> list[int]:
    """Full same-depth fibre of ``p`` (N2+N1+N0) at deficit ``r``."""
    m = deficit_depth(k, r)
    if abs(p) > balanced_bound(m):
        raise ValueError(f"p={p} is not a packed prefix of width {m}")
    return [q for q in n21_fibre_of(p, k, r) if same_depth_n0(m, p, q, k)]


def locus_prefixes(k: int, r: int) -> list[int]:
    step = 3**r
    return [p for p in prefixes_at(deficit_depth(k, r)) if p % step == 0]


def n0_classes_on_locus(k: int, r: int) -> dict[int, list[int]]:
    m = deficit_depth(k, r)
    mod = 3**k if k else 1
    buckets: dict[int, list[int]] = defaultdict(list)
    for p in locus_prefixes(k, r):
        buckets[iter_dz(p**3, m) % mod].append(p)
    return buckets


def n0_reduction_report(k: int, r: int) -> dict[str, object]:
    m = deficit_depth(k, r)
    t = reduced_depth(k, r)
    regime = n0_regime(k, r)
    us = list(u_prefixes(k, r))
    mismatches_deepest = 0
    if k >= 2 * r + 1 and us:
        for u in us:
            a = n0_mod(u, k, r)
            b = n0_candidate_deepest(u, k, r) % (3 ** (k - 2 * r) if k > 2 * r else 1)
            # Compare apples-to-oranges on purpose: same integer vs reduced modulus.
            if a % (3 ** (k - 2 * r) if k > 2 * r else 1) != b:
                mismatches_deepest += 1
    formula_ok = all(n0_original(u, k, r) == n0_scaled(u, k, r) for u in us)
    samples = []
    for u in us[:8]:
        samples.append(
            {
                "u": u,
                "p": 3**r * u,
                "N0": n0_original(u, k, r),
                "stripped": n0_scaled(u, k, r),
            }
        )
    seen: set[frozenset[int]] = set()
    n21_n0 = 0
    n21_only = 0
    for p in locus_prefixes(k, r):
        fib21 = frozenset(n21_fibre_of(p, k, r))
        if len(fib21) <= 1 or fib21 in seen:
            continue
        seen.add(fib21)
        n21_only += 1
        if len([q for q in fib21 if same_depth_n0(m, p, q, k)]) > 1:
            n21_n0 += 1
    return {
        "k": k,
        "r": r,
        "m": m,
        "t": t,
        "regime": regime,
        "unexhausted": m <= 3 * r,
        "exponent": max(3 * r - m, 0),
        "u_width": m - r if m >= r else 0,
        "u_count": len(us),
        "formula_ok": formula_ok,
        "n1_horizon": k - 2 * r if k >= 2 * r else None,
        "n1_deepest_depth": k - 2 * r - 1 if k >= 2 * r + 1 else None,
        "depth_mismatch": t != (k - 2 * r - 1 if k >= 2 * r + 1 else t),
        "visibility_s": n0_visibility_bound(t, k) if regime != "unexhausted" or t == 0 else None,
        "mismatches_vs_n1_horizon": mismatches_deepest,
        "n21_nontrivial_on_locus": n21_only,
        "n21_n0_nontrivial": n21_n0,
        "samples": samples,
    }


def phase_row(k: int, r: int, s: int) -> dict[str, object]:
    """N0 regime for a valuation ``s ≥ r`` at deficit ``r``."""
    m = deficit_depth(k, r)
    return {
        "r": r,
        "s": s,
        "m": m,
        "m_minus_3s": m - 3 * s,
        "regime": "unexhausted" if m <= 3 * s else "exhausted",
    }
