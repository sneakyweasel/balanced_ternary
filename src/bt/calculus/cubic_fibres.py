"""Fibres of the cubic Newton image map ``F_k``.

Same-depth collisions are decided by the three surviving Newton
coordinates after ``N3`` is cancelled. Cross-depth collisions require
both depths to be deep enough that ``N3`` vanishes, and then reduce to
the same arithmetic conditions on ``(N2, N1, N0)``.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from bt.calculus.cubic import F_k, raw_count_x3
from bt.calculus.quadratic import iter_dz
from bt.metrics import v3


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def balanced_bound(m: int) -> int:
    """Half-width of ``P_m``: ``(3^m-1)/2``."""
    m = _require_nat(m, "m")
    return (3**m - 1) // 2


def is_balanced_width(m: int, p: int) -> bool:
    """``p`` is a packed prefix of some length-``m`` trit word."""
    return abs(p) <= balanced_bound(m)


def prefixes_at(m: int) -> range:
    """Integers ``P_m`` as a contiguous symmetric interval."""
    w = balanced_bound(m)
    return range(-w, w + 1)


def n2_divisor(m: int, k: int) -> int:
    """Exponent ``s = max(k-m-1, 0)`` in the same-depth ``N2`` law."""
    m = _require_nat(m, "m")
    k = _require_nat(k, "k")
    return max(k - m - 1, 0)


def same_depth_n2(m: int, p: int, q: int, k: int) -> bool:
    """``3^{k-m-1} | (p-q)`` when ``k > m+1``; otherwise automatic."""
    s = n2_divisor(m, k)
    if s == 0:
        return True
    return (p - q) % (3**s) == 0


def same_depth_n1(m: int, p: int, q: int, k: int) -> bool:
    """``3^{k-1} | (p-q)(p+q+3^m)``."""
    k = _require_nat(k, "k")
    m = _require_nat(m, "m")
    if k == 0:
        return True
    return ((p - q) * (p + q + 3**m)) % (3 ** (k - 1)) == 0


def same_depth_n0(m: int, p: int, q: int, k: int) -> bool:
    """``3^k | D^m(p^3) - D^m(q^3)``."""
    k = _require_nat(k, "k")
    m = _require_nat(m, "m")
    if k == 0:
        return True
    return (iter_dz(p**3, m) - iter_dz(q**3, m)) % (3**k) == 0


def same_depth_equiv(m: int, p: int, q: int, k: int) -> bool:
    """Necessary and sufficient same-depth fibre criterion."""
    return same_depth_n2(m, p, q, k) and same_depth_n1(m, p, q, k) and same_depth_n0(m, p, q, k)


def n3_vanishes(m: int, k: int) -> bool:
    """``N3 = 2·3^{2m+1}`` is ``0`` modulo ``3^k``."""
    return 2 * m + 1 >= k


def n1_zero_vanishes(m: int, k: int) -> bool:
    """``N1(m, 0) = 3^{2m}`` is ``0`` modulo ``3^k``."""
    return 2 * m >= k


def cross_depth_n3(m: int, n: int, k: int) -> bool:
    """``N3`` agrees across depths iff both are deep or the depths match."""
    if m == n:
        return True
    return n3_vanishes(m, k) and n3_vanishes(n, k)


def sign_pair_n2n1(m: int, p: int, k: int) -> bool:
    """``N2`` and ``N1`` of the odd pair ``(p, -p)`` agree."""
    s = n2_divisor(m, k)
    if s == 0:
        return True
    return p % (3**s) == 0


def sign_pair_equiv(m: int, p: int, k: int) -> bool:
    """``F_k(m, p) = F_k(m, -p)`` for ``p ≠ 0``."""
    if p == 0:
        return True
    if not sign_pair_n2n1(m, p, k):
        return False
    return iter_dz(p**3, m) % (3**k if k else 1) == 0


def zero_fibre_exponent(k: int) -> int:
    """Valuation threshold for the deepest ``0``-fibre.

    At depth ``m = k-1``, ``F_k(k-1, q) = F_k(k-1, 0)`` iff
    ``3^{ceil((2k-1)/3)} | q`` (for ``q ∈ P_{k-1}``).
    """
    k = _require_nat(k, "k")
    if k == 0:
        return 0
    return (2 * k - 1 + 2) // 3


def C_km(k: int, m: int) -> int:
    """Number of distinct Newton classes at a single depth."""
    k = _require_nat(k, "k")
    m = _require_nat(m, "m")
    if m >= k:
        return 0
    return len({F_k(m, p, k) for p in prefixes_at(m)})


def per_depth_counts(k: int) -> list[int]:
    return [C_km(k, m) for m in range(k)]


def depth_image(k: int, m: int) -> dict[tuple[int, int, int, int], list[int]]:
    buckets: dict[tuple[int, int, int, int], list[int]] = defaultdict(list)
    for p in prefixes_at(m):
        buckets[F_k(m, p, k)].append(p)
    return buckets


def newton_image_params(k: int) -> dict[tuple[int, int, int, int], list[tuple[int, int]]]:
    """``Φ_k →`` list of ``(m, p)`` with ``m < k``."""
    k = _require_nat(k, "k")
    buckets: dict[tuple[int, int, int, int], list[tuple[int, int]]] = defaultdict(list)
    for m in range(k):
        for p in prefixes_at(m):
            buckets[F_k(m, p, k)].append((m, p))
    return buckets


def fibre_of(m: int, p: int, k: int) -> list[tuple[int, int]]:
    """Complete ``~_k``-class of the residual parameter ``(m, p)``."""
    target = F_k(m, p, k)
    return list(newton_image_params(k)[target])


def cross_depth_intersections(k: int) -> list[tuple[int, int, int]]:
    """``(m, n, |Im_m ∩ Im_n|)`` for ``m < n`` with nonempty overlap."""
    images = [set(depth_image(k, m)) for m in range(k)]
    out = []
    for m in range(k):
        for n in range(m + 1, k):
            inter = images[m] & images[n]
            if inter:
                out.append((m, n, len(inter)))
    return out


def fibre_size_histogram(k: int) -> dict[int, int]:
    sizes = Counter(len(v) for v in newton_image_params(k).values())
    return dict(sorted(sizes.items()))


def same_depth_fibres(k: int) -> dict[int, list[list[int]]]:
    """Colliding ``p``-lists at each depth (size at least 2)."""
    out: dict[int, list[list[int]]] = {}
    for m in range(k):
        fibs = [sorted(ps) for ps in depth_image(k, m).values() if len(ps) > 1]
        if fibs:
            out[m] = sorted(fibs, key=lambda xs: (len(xs), xs[0]))
    return out


def zero_spine_depths(k: int) -> list[int]:
    """Depths whose residual ``p = 0`` shares the zero Newton class."""
    return [m for m in range(k) if n3_vanishes(m, k) and n1_zero_vanishes(m, k)]


def fibre_report(k: int) -> dict[str, object]:
    """CLI payload for ``cubic-fibres``."""
    k = _require_nat(k, "k")
    image = newton_image_params(k)
    R = raw_count_x3(k)
    M = len(image)
    counts = per_depth_counts(k)
    hist = fibre_size_histogram(k)
    fibres = [members for members in image.values() if len(members) > 1]
    largest = max((len(f) for f in fibres), default=1)
    examples = []
    for members in sorted(fibres, key=len, reverse=True)[:8]:
        examples.append([(m, p) for m, p in members])
    return {
        "k": k,
        "R": R,
        "M": M,
        "per_depth": counts,
        "sum_C": sum(counts),
        "cross_depth": cross_depth_intersections(k),
        "largest_fibre": largest,
        "histogram": hist,
        "n_collision_classes": len(fibres),
        "zero_spine": zero_spine_depths(k),
        "examples": examples,
        "shallow_full": [3**m for m in range(k) if 2 * m + 1 <= k],
    }


def fibre_lifting_split(k: int) -> dict[str, object]:
    """How classes at horizon ``k`` refine at ``k+1`` (same prefixes ``m < k``)."""
    k = _require_nat(k, "k")
    coarse = newton_image_params(k)
    split = 0
    stay = 0
    for members in coarse.values():
        fine = {F_k(m, p, k + 1) for m, p in members if m < k}
        if len(fine) > 1:
            split += 1
        else:
            stay += 1
    return {"k": k, "classes": len(coarse), "stay": stay, "split": split}
