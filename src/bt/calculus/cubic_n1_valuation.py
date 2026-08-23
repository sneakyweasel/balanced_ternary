"""N1 refinement after the general N2 depth-deficit filter.

At deficit ``r`` with ``m = k-1-r``, ``N2`` equality is ``p ≡ q (mod 3^r)``.
After that filter, ``N1`` equality is

    3^{k-1-r} | δ (p + q + 3^m),    p - q = 3^r δ.

On the balanced prefix interval, every prefix with ``v3(p) < r`` is then
separated from every other prefix.  Nontrivial ``N2+N1`` fibres can survive
only inside ``3^r Z``.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from bt.calculus.cubic_fibres import balanced_bound, prefixes_at, same_depth_n1, same_depth_n2
from bt.metrics import v3


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def deficit_depth(k: int, r: int) -> int:
    """``m = k-1-r``."""
    k = _require_nat(k, "k")
    r = _require_nat(r, "r")
    if r + 1 > k:
        raise ValueError("need r+1 ≤ k so that m = k-1-r ≥ 0")
    return k - 1 - r


def n1_after_n2(p: int, q: int, k: int, r: int) -> bool:
    """``3^{k-1-r} | δ(p+q+3^m)`` given ``p-q = 3^r δ``; equivalent to ``N1``."""
    m = deficit_depth(k, r)
    return same_depth_n1(m, p, q, k)


def n21_agree(p: int, q: int, k: int, r: int) -> bool:
    m = deficit_depth(k, r)
    return same_depth_n2(m, p, q, k) and same_depth_n1(m, p, q, k)


def n2_image(k: int, r: int) -> set[int]:
    m = deficit_depth(k, r)
    return {p % (3**r) for p in prefixes_at(m)}


def n21_image(k: int, r: int) -> dict[tuple[int, int], list[int]]:
    """Buckets of prefixes by ``(p mod 3^r, N1 residue class key)``."""
    m = deficit_depth(k, r)
    mod = 3**k if k else 1
    buckets: dict[tuple[int, int], list[int]] = defaultdict(list)
    for p in prefixes_at(m):
        n1 = (3 ** (2 * m) + 3 ** (m + 1) * p + 3 * p * p) % mod
        n2key = p % (3**r) if r else 0
        buckets[(n2key, n1)].append(p)
    return buckets


def n21_class_count(k: int, r: int) -> int:
    return len(n21_image(k, r))


def n21_fibre_of(p: int, k: int, r: int) -> list[int]:
    m = deficit_depth(k, r)
    if abs(p) > balanced_bound(m):
        raise ValueError(f"p={p} is not a packed prefix of width {m}")
    return [q for q in prefixes_at(m) if n21_agree(p, q, k, r)]


def surviving_locus_ok(k: int, r: int) -> bool:
    """Every nontrivial ``N2+N1`` fibre lies in ``3^r Z``."""
    step = 3**r
    for ps in n21_image(k, r).values():
        if len(ps) <= 1:
            continue
        if any(p % step != 0 for p in ps):
            return False
    return True


def stratum_histogram(k: int, r: int) -> dict[str, int]:
    """How many prefixes, and how many nontrivial fibres, per valuation."""
    m = deficit_depth(k, r)
    prefixes = list(prefixes_at(m))
    by_v: Counter[str] = Counter()
    for p in prefixes:
        vp = v3(p)
        key = "inf" if vp is None else str(vp)
        by_v[key] += 1
    fibres = n21_image(k, r)
    fibre_v: Counter[str] = Counter()
    for ps in fibres.values():
        if len(ps) <= 1:
            continue
        vals = [v3(x) for x in ps]
        finite = [v for v in vals if v is not None]
        key = "inf" if not finite else str(min(finite))
        fibre_v[key] += 1
    return {
        "n_prefixes": len(prefixes),
        "n_units": sum(1 for p in prefixes if p % 3 != 0),
        "n_div_r": sum(1 for p in prefixes if p % (3**r) == 0),
        "n21": len(fibres),
        "n21_nontrivial": sum(1 for ps in fibres.values() if len(ps) > 1),
        "stratum_sizes": dict(sorted(by_v.items(), key=lambda kv: (kv[0] == "inf", int(kv[0]) if kv[0] != "inf" else 0))),
        "nontrivial_by_min_v": dict(fibre_v),
    }


def n1_strata_report(k: int, r: int) -> dict[str, object]:
    m = deficit_depth(k, r)
    image = n21_image(k, r)
    n2 = len(n2_image(k, r))
    n21 = len(image)
    units = [p for p in prefixes_at(m) if p % 3 != 0]
    unit_classes = {
        (p % (3**r) if r else 0,
         (3 ** (2 * m) + 3 ** (m + 1) * p + 3 * p * p) % (3**k if k else 1))
        for p in units
    }
    nontrivial = [sorted(ps) for ps in image.values() if len(ps) > 1]
    hist = dict(sorted(Counter(len(v) for v in image.values()).items()))
    info = stratum_histogram(k, r)
    return {
        "k": k,
        "r": r,
        "m": m,
        "raw": 3**m,
        "N2": n2,
        "N21": n21,
        "unit_prefixes": len(units),
        "unit_classes": len(unit_classes),
        "n_div_r": info["n_div_r"],
        "n21_nontrivial": len(nontrivial),
        "histogram": hist,
        "surviving_in_3r": surviving_locus_ok(k, r),
        "examples": nontrivial[:8],
        "max_fibre": max((len(v) for v in image.values()), default=1),
        "min_nontrivial": min((len(v) for v in nontrivial), default=0),
        "stratum_sizes": info["stratum_sizes"],
        "nontrivial_by_min_v": info["nontrivial_by_min_v"],
    }


def low_val_collisions(k: int, r: int) -> list[tuple[int, int]]:
    """Pairs with ``v3(p) < r``, ``p ≢ q``, that still agree on ``N2+N1``."""
    m = deficit_depth(k, r)
    hits: list[tuple[int, int]] = []
    ps = list(prefixes_at(m))
    for i, p in enumerate(ps):
        vp = v3(p)
        if vp is None or vp >= r:
            continue
        for q in ps[i + 1 :]:
            if n21_agree(p, q, k, r):
                hits.append((p, q))
    return hits


def n1_high_val_reduces(k: int, r: int, u: int, v: int) -> bool:
    """Whether scaled ``N1`` at deficit ``r`` matches deepest ``N1`` at ``k-2r``.

    Valid only for ``k ≥ 2r+2``.  Returns the two sides of the reduction.
    """
    if k < 2 * r + 2:
        raise ValueError("need k ≥ 2r+2 for the scaled N1 reduction")
    left = n1_after_n2(3**r * u, 3**r * v, k, r)
    right = same_depth_n1(k - 1 - 2 * r, u, v, k - 2 * r)
    return left == right
