"""First intermediate cubic layer: depth deficit ``r = 1`` (``m = k-2``).

At ``m = k-2`` the Newton coordinates simplify, for ``k ≥ 4``, to

    N3 ≡ 0,
    N2 ≡ 2 · 3^{k-1} p,
    N1 ≡ 3 p^2 + 3^{k-1} p,
    N0  = D^{k-2}(p^3)          (mod 3^k).

``N2`` sees only ``p mod 3``.  ``N1`` and ``N0`` then refine.  The
horizon lift ``Φ_{k-1} → Φ_k`` on this depth is a refinement of the
previous deepest layer; unit sign pairs always split.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from bt.calculus.cubic import F_k
from bt.calculus.cubic_deepest import deepest_class_count, fibre_kind
from bt.calculus.cubic_fibres import (
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


def layer_depth(k: int, deficit: int = 1) -> int:
    """``m = k-1-r``.  This module treats only ``r = 1``."""
    k = _require_nat(k, "k")
    deficit = _require_nat(deficit, "deficit")
    if deficit != 1:
        raise ValueError("only depth-deficit 1 (m=k-2) is implemented")
    if k < 2:
        raise ValueError("k must be at least 2 for m=k-2")
    return k - 2


def inter_n2(p: int, k: int) -> int:
    """``N2 ≡ 2 · 3^{k-1} p (mod 3^k)`` for ``k ≥ 3``."""
    k = _require_nat(k, "k")
    mod = 3**k if k else 1
    return (2 * 3 ** (k - 1) * p) % mod


def inter_n1(p: int, k: int) -> int:
    """``N1 ≡ 3 p^2 + 3^{k-1} p (mod 3^k)`` for ``k ≥ 4``."""
    k = _require_nat(k, "k")
    mod = 3**k if k else 1
    return (3 * p * p + 3 ** (k - 1) * p) % mod


def inter_n0(p: int, k: int) -> int:
    """``N0 = D^{k-2}(p^3) (mod 3^k)``."""
    k = _require_nat(k, "k")
    if k < 2:
        return 0
    return iter_dz(p**3, k - 2) % (3**k)


def inter_n2_agree(p: int, q: int, k: int) -> bool:
    """``p ≡ q (mod 3)``."""
    return same_depth_n2(k - 2, p, q, k)


def inter_n1_agree(p: int, q: int, k: int) -> bool:
    """``3^{k-1} | (p-q)(p+q+3^{k-2})``."""
    return same_depth_n1(k - 2, p, q, k)


def inter_n0_agree(p: int, q: int, k: int) -> bool:
    return same_depth_n0(k - 2, p, q, k)


def inter_equiv(p: int, q: int, k: int) -> bool:
    """Exact same-depth fibre criterion at ``m = k-2``."""
    return same_depth_equiv(k - 2, p, q, k)


def n2_image(k: int) -> set[int]:
    """Exact ``N2`` residues (not the ``k≥3`` abbreviation)."""
    m = layer_depth(k)
    mod = 3**k
    return {(2 * 3 ** (m + 1) * (p + 3**m)) % mod for p in prefixes_at(m)}


def n21_image(k: int) -> set[tuple[int, int]]:
    """Exact ``(N1, N2)`` residues."""
    m = layer_depth(k)
    mod = 3**k
    out = set()
    for p in prefixes_at(m):
        n1 = (3 ** (2 * m) + 3 ** (m + 1) * p + 3 * p * p) % mod
        n2 = (2 * 3 ** (m + 1) * (p + 3**m)) % mod
        out.add((n1, n2))
    return out


def inter_image(k: int) -> dict[tuple[int, int, int, int], list[int]]:
    m = layer_depth(k)
    buckets: dict[tuple[int, int, int, int], list[int]] = defaultdict(list)
    for p in prefixes_at(m):
        buckets[F_k(m, p, k)].append(p)
    return buckets


def inter_class_count(k: int) -> int:
    """``C_{k,k-2}``."""
    return len(inter_image(k))


def one_layer_surplus(k: int) -> int:
    """``Δ_k = C_{k,k-2} - C_{k-1,k-2}``."""
    k = _require_nat(k, "k")
    if k < 3:
        return 0
    return inter_class_count(k) - deepest_class_count(k - 1)


def horizon_splits(k: int) -> list[tuple[list[int], list[list[int]]]]:
    """Previous-deepest classes that split under horizon lift ``k-1 → k``."""
    k = _require_nat(k, "k")
    m = layer_depth(k)
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


def zero_exp_inter(k: int) -> int:
    """``ceil((2k-2)/3)`` for the ``m=k-2`` zero fibre."""
    k = _require_nat(k, "k")
    if k == 0:
        return 0
    return (2 * k) // 3


def inter_zero_fibre(k: int) -> list[int]:
    """Prefixes at ``m=k-2`` with ``3^{ceil((2k-2)/3)} | p``."""
    m = layer_depth(k)
    r = zero_exp_inter(k)
    step = 3**r
    return [p for p in prefixes_at(m) if p % step == 0]


def inter_fibre_of(p: int, k: int) -> list[int]:
    k = _require_nat(k, "k")
    m = layer_depth(k)
    if abs(p) > balanced_bound(m):
        raise ValueError(f"p={p} is not a packed prefix of width {m}")
    target = F_k(m, p, k)
    return [q for q in prefixes_at(m) if F_k(m, q, k) == target]


def layer_report(k: int, deficit: int = 1) -> dict[str, object]:
    """CLI payload for ``cubic-layer``."""
    m = layer_depth(k, deficit)
    image = inter_image(k)
    C = len(image)
    raw = 3**m
    n2 = len(n2_image(k))
    n21 = len(n21_image(k))
    hist = dict(sorted(Counter(len(v) for v in image.values()).items()))
    kinds = Counter(fibre_kind(sorted(ps), m) for ps in image.values())
    fibres = [sorted(ps) for ps in image.values() if len(ps) > 1]
    examples = sorted(fibres, key=lambda xs: (len(xs), xs[0]))[:12]
    prev = deepest_class_count(k - 1) if k >= 3 else C
    return {
        "k": k,
        "m": m,
        "deficit": 1,
        "raw": raw,
        "N2": n2,
        "N21": n21,
        "C": C,
        "C_prev_deepest": prev,
        "Delta": C - prev,
        "histogram": hist,
        "kinds": dict(kinds),
        "n_fibres": len(fibres),
        "examples": examples,
    }
