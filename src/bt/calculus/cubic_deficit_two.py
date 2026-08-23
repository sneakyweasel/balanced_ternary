"""Cubic residual layer at depth deficit ``r = 2`` (``m = k-3``).

For ``k ≥ 5`` the Newton coordinates simplify to

    N3 ≡ 0,
    N2 ≡ 2 · 3^{k-2} p,
    N1 ≡ 3 p^2 + 3^{k-2} p     (k ≥ 6),
    N0  = D^{k-3}(p^3)          (mod 3^k).

``N2`` sees exactly ``p mod 9``.  This is the ``r = 2`` case of the
depth-deficit visibility law ``N2`` iff ``p ≡ q (mod 3^r)``.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from bt.calculus.cubic import F_k
from bt.calculus.cubic_deepest import fibre_kind
from bt.calculus.cubic_fibres import (
    C_km,
    balanced_bound,
    prefixes_at,
    same_depth_equiv,
    same_depth_n0,
    same_depth_n1,
    same_depth_n2,
)
from bt.calculus.quadratic import iter_dz


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def deficit_two_depth(k: int) -> int:
    """``m = k-3``."""
    k = _require_nat(k, "k")
    if k < 3:
        raise ValueError("k must be at least 3 for m=k-3")
    return k - 3


def def2_n2(p: int, k: int) -> int:
    """``N2 ≡ 2 · 3^{k-2} p (mod 3^k)`` for ``k ≥ 5``."""
    k = _require_nat(k, "k")
    mod = 3**k if k else 1
    return (2 * 3 ** (k - 2) * p) % mod


def def2_n1(p: int, k: int) -> int:
    """``N1 ≡ 3 p^2 + 3^{k-2} p (mod 3^k)`` for ``k ≥ 6``."""
    k = _require_nat(k, "k")
    mod = 3**k if k else 1
    return (3 * p * p + 3 ** (k - 2) * p) % mod


def def2_n0(p: int, k: int) -> int:
    """``N0 = D^{k-3}(p^3) (mod 3^k)``."""
    k = _require_nat(k, "k")
    if k < 3:
        return 0
    return iter_dz(p**3, k - 3) % (3**k)


def def2_n2_agree(p: int, q: int, k: int) -> bool:
    """``p ≡ q (mod 9)``."""
    return same_depth_n2(k - 3, p, q, k)


def def2_n1_agree(p: int, q: int, k: int) -> bool:
    """``3^{k-1} | (p-q)(p+q+3^{k-3})``."""
    return same_depth_n1(k - 3, p, q, k)


def def2_n0_agree(p: int, q: int, k: int) -> bool:
    return same_depth_n0(k - 3, p, q, k)


def def2_equiv(p: int, q: int, k: int) -> bool:
    """Exact same-depth fibre criterion at ``m = k-3``."""
    return same_depth_equiv(k - 3, p, q, k)


def n2_image(k: int) -> set[int]:
    """Exact ``N2`` residues."""
    m = deficit_two_depth(k)
    mod = 3**k
    return {(2 * 3 ** (m + 1) * (p + 3**m)) % mod for p in prefixes_at(m)}


def n21_image(k: int) -> set[tuple[int, int]]:
    """Exact ``(N1, N2)`` residues."""
    m = deficit_two_depth(k)
    mod = 3**k
    out = set()
    for p in prefixes_at(m):
        n1 = (3 ** (2 * m) + 3 ** (m + 1) * p + 3 * p * p) % mod
        n2 = (2 * 3 ** (m + 1) * (p + 3**m)) % mod
        out.add((n1, n2))
    return out


def def2_image(k: int) -> dict[tuple[int, int, int, int], list[int]]:
    m = deficit_two_depth(k)
    buckets: dict[tuple[int, int, int, int], list[int]] = defaultdict(list)
    for p in prefixes_at(m):
        buckets[F_k(m, p, k)].append(p)
    return buckets


def def2_class_count(k: int) -> int:
    """``C_{k,k-3}``."""
    return len(def2_image(k))


def horizon_surplus(k: int) -> int:
    """``Δ_k^{(r=2)} = C_{k,k-3} - C_{k-1,k-3}``."""
    k = _require_nat(k, "k")
    if k < 4:
        return 0
    return def2_class_count(k) - C_km(k - 1, k - 3)


def horizon_splits(k: int) -> list[tuple[list[int], list[list[int]]]]:
    """Classes at horizon ``k-1`` that split under ``Φ_{k-1} → Φ_k``."""
    k = _require_nat(k, "k")
    m = deficit_two_depth(k)
    coarse: dict[tuple[int, int, int, int], list[int]] = defaultdict(list)
    for p in prefixes_at(m):
        coarse[F_k(m, p, k - 1)].append(p)
    out = []
    for ps in coarse.values():
        fine: dict[tuple[int, int, int, int], list[int]] = defaultdict(list)
        for p in ps:
            fine[F_k(m, p, k)].append(p)
        if len(fine) > 1:
            out.append((sorted(ps), [sorted(v) for v in fine.values()]))
    return out


def def2_fibre_of(p: int, k: int) -> list[int]:
    k = _require_nat(k, "k")
    m = deficit_two_depth(k)
    if abs(p) > balanced_bound(m):
        raise ValueError(f"p={p} is not a packed prefix of width {m}")
    target = F_k(m, p, k)
    return [q for q in prefixes_at(m) if F_k(m, q, k) == target]


def def2_report(k: int) -> dict[str, object]:
    """CLI payload for ``cubic-layer --depth-deficit 2``."""
    m = deficit_two_depth(k)
    image = def2_image(k)
    C = len(image)
    raw = 3**m
    n2 = len(n2_image(k))
    n21 = len(n21_image(k))
    hist = dict(sorted(Counter(len(v) for v in image.values()).items()))
    kinds = Counter(fibre_kind(sorted(ps), m) for ps in image.values())
    fibres = [sorted(ps) for ps in image.values() if len(ps) > 1]
    examples = sorted(fibres, key=lambda xs: (len(xs), xs[0]))[:12]
    prev = C_km(k - 1, k - 3) if k >= 4 else C
    return {
        "k": k,
        "m": m,
        "deficit": 2,
        "raw": raw,
        "N2": n2,
        "N21": n21,
        "C": C,
        "C_prev": prev,
        "Delta": C - prev,
        "Delta1": n21 - n2,
        "Delta0": C - n21,
        "histogram": hist,
        "kinds": dict(kinds),
        "n_fibres": len(fibres),
        "examples": examples,
        "max_fibre": max((len(v) for v in image.values()), default=1),
        "singletons": hist.get(1, 0),
    }
