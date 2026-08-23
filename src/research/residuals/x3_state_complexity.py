"""Exact image counts for the residual machine of ``x^3``.

Master identity:

    M_k(x^3) = |⋃_{m < k} Im F_k(m, ·)|.

Same-depth classes at deficit ``r = k-1-m`` split into the injective
``v_3(p) < r`` region and the ``3^r``-divisible core ``p = 3^r u``,
``u ∈ P_W``, ``W = k-1-2r``.  The core image is counted directly as
``{(N1, N0)}`` (equivalently the ``Q``-image in the exhausted regime,
together with ``N1``).  This module does not classify ``Q``-fibres.
"""

from __future__ import annotations

from collections import defaultdict

from bt.calculus.cubic import F_k, prefixes_at, raw_count_x3
from bt.metrics import v3
from research.residuals.cubic_fibres import zero_spine_depths
from research.residuals.cubic_n0_reduction import n0_mod, n0_regime
from research.residuals.cubic_n1_valuation import deficit_depth
from research.residuals.mismatched_cubic import q_split_high


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def layer_depth(k: int, r: int) -> int:
    """``m = k-1-r``."""
    return deficit_depth(k, r)


def core_width(k: int, r: int) -> int:
    """``W = m-r = k-1-2r``, or ``-1`` if the core is empty."""
    m = layer_depth(k, r)
    return m - r


def easy_count(m: int, r: int) -> int:
    """``#{p ∈ P_m : v_3(p) < r}``.

    First nonzero balanced digit before position ``r``: ``3^m - 3^{m-r}``
    when ``0 ≤ r ≤ m``, the full ``3^m`` when ``r > m``, and ``0`` at
    ``r = 0``.
    """
    m = _require_nat(m, "m")
    r = _require_nat(r, "r")
    if r == 0:
        return 0
    if r > m:
        return 3**m
    return 3**m - 3 ** (m - r)


def core_domain_size(k: int, r: int) -> int:
    """``|P_W| = 3^W`` if ``W ≥ 0``, else ``0`` (only the empty core)."""
    W = core_width(k, r)
    if W < 0:
        return 0
    return 3**W


def in_core_domain(u: int, k: int, r: int) -> bool:
    """``3^r u ∈ P_m`` iff ``u ∈ P_W`` (empty core forces ``u = 0``)."""
    W = core_width(k, r)
    if W < 0:
        return u == 0
    return abs(u) <= (3**W - 1) // 2


def core_u_range(k: int, r: int) -> range:
    W = core_width(k, r)
    if W < 0:
        return range(0, 1)
    return prefixes_at(W)


def core_phi(u: int, k: int, r: int) -> tuple[int, int, int, int]:
    m = layer_depth(k, r)
    return F_k(m, (3**r) * u, k)


def core_n1(u: int, k: int, r: int) -> int:
    """``N1 ≡ 3^{2r+1} u^2 (mod 3^k)`` once ``k ≥ 2r+2``; exact otherwise."""
    return core_phi(u, k, r)[1]


def core_n0(u: int, k: int, r: int) -> int:
    return n0_mod(u, k, r)


def g_poly(t: int, a: int, b: int) -> int:
    """Two-scale polynomial ``G_a(b) = D^t((a + 3^t b)^3)``."""
    return q_split_high(t, a, b)


def core_image(k: int, r: int) -> set[tuple[int, int, int, int]]:
    """Observable Newton classes on the ``3^r``-divisible core."""
    return {core_phi(u, k, r) for u in core_u_range(k, r)}


def q_core_image(k: int, r: int) -> set[int]:
    """``N0``-only image on the core (the ``Q``-image when exhausted)."""
    return {core_n0(u, k, r) for u in core_u_range(k, r)}


def C_km_count(k: int, m: int) -> int:
    """Exact ``C_{k,m} = easy + |core image|`` (or ``3^m`` if ``r > m``)."""
    k = _require_nat(k, "k")
    m = _require_nat(m, "m")
    if m >= k:
        return 0
    r = k - 1 - m
    if r > m:
        return 3**m
    return easy_count(m, r) + len(core_image(k, r))


def unexhausted_zero_exp(k: int, r: int) -> int:
    """Valuation threshold on ``u`` for the core zero class, unexhausted."""
    k = _require_nat(k, "k")
    r = _require_nat(r, "r")
    return (2 * k - 4 * r - 1 + 2) // 3


def unexhausted_zero_size(k: int, r: int) -> int:
    """``|{u ∈ P_W : 3^s | u}|`` with ``s = ceil((2k-4r-1)/3)``."""
    W = core_width(k, r)
    if W < 0:
        return 0
    s = unexhausted_zero_exp(k, r)
    if s <= 0:
        return 3**W
    if s > W:
        return 1
    return 3 ** (W - s)


def C_unexhausted_formula(k: int, r: int) -> int:
    """``C_{k,k-1-r} = 3^m - Z + 1`` on the unexhausted locus.

    The only core collisions are the zero fibre: after ``N1`` one has
    ``u^2 ≡ v^2 (mod 3^W)`` on ``P_W``, hence ``u = ±v``, and a surviving
    sign pair forces ``N0 = 0``, which already forces ``N1 = 0``.
    """
    m = layer_depth(k, r)
    return 3**m - unexhausted_zero_size(k, r) + 1


def C_layer(k: int, r: int) -> int:
    """``C_{k,k-1-r}`` by the easy/core split, using the closed unexhausted formula."""
    k = _require_nat(k, "k")
    r = _require_nat(r, "r")
    m = layer_depth(k, r)
    if r > m:
        return 3**m
    if k < 4 * r + 1:
        return C_unexhausted_formula(k, r)
    return easy_count(m, r) + len(core_image(k, r))


def unit_prefixes(W: int) -> list[int]:
    return [u for u in prefixes_at(W) if u % 3 != 0]


def split_low_high(u: int, t: int) -> tuple[int, int]:
    """``u = a + 3^t b`` with ``a = bal_t(u)``."""
    t = _require_nat(t, "t")
    if t == 0:
        return 0, u
    from bt.calculus.jets import integer_jet
    from bt.calculus.quadratic import pack_word

    a = pack_word(integer_jet(u, t))
    return a, (u - a) // (3**t)


def unit_q_image(k: int, r: int) -> set[int]:
    """``Q``-image (or scaled-cube image) on unit ``u ∈ P_W``."""
    out = set()
    for u in core_u_range(k, r):
        if u % 3 == 0:
            continue
        out.add(core_n0(u, k, r))
    return out


def valuation_q_images(k: int, r: int) -> dict[int | None, int]:
    """``N0``-image size by ``v_3(u)`` (``None`` is ``u = 0``)."""
    buckets: dict[int | None, set[int]] = defaultdict(set)
    for u in core_u_range(k, r):
        key = None if u == 0 else v3(u)
        buckets[key].add(core_n0(u, k, r))
    return {key: len(vals) for key, vals in sorted(buckets.items(), key=lambda kv: (-1 if kv[0] is None else kv[0]))}


def unit_g_injective_mod(t: int, K: int, a: int, b: int, c: int) -> bool:
    """Unit-stratum law: ``G_a(b) ≡ G_a(c) (mod 3^K)`` iff ``3^{K-1} | (b-c)``."""
    if a % 3 == 0:
        raise ValueError("unit stratum requires 3 ∤ a")
    if t < 1 or K < 1:
        raise ValueError("need t ≥ 1 and K ≥ 1")
    left = (g_poly(t, a, b) - g_poly(t, a, c)) % (3**K)
    right = (b - c) % (3 ** (K - 1))
    return (left == 0) == (right == 0)


def deep_start(k: int) -> int:
    """Smallest ``m`` with ``N3 ≡ 0 (mod 3^k)``: ``ceil((k-1)/2) = ⌊k/2⌋``."""
    k = _require_nat(k, "k")
    return k // 2


def shallow_state_sum(k: int) -> int:
    """``∑_{2m+1 < k} 3^m = (3^{m0} - 1)/2`` with ``m0 = ceil((k-1)/2)``."""
    k = _require_nat(k, "k")
    m0 = deep_start(k)
    if m0 <= 0:
        return 0
    return (3**m0 - 1) // 2


def layer_phis(k: int, m: int) -> set[tuple[int, int, int, int]]:
    return {F_k(m, p, k) for p in prefixes_at(m)}


def M_k_count(k: int) -> int:
    """``M_k`` from the N3 split: shallow sum plus the deep-image union."""
    k = _require_nat(k, "k")
    if k == 0:
        return 0
    deep: set[tuple[int, int, int, int]] = set()
    for m in range(deep_start(k), k):
        deep |= layer_phis(k, m)
    return shallow_state_sum(k) + len(deep)


def same_depth_total(k: int) -> int:
    return sum(C_layer(k, k - 1 - m) for m in range(k))


def zero_spine_overcount(k: int) -> int:
    """``|spine| - 1`` if the spine is nonempty, else ``0``."""
    spine = zero_spine_depths(k)
    return max(len(spine) - 1, 0)


def cross_depth_pairs(k: int) -> list[tuple[int, int, int, int]]:
    """``(m, n, |Im_m ∩ Im_n|, nonzero)`` among deep depths."""
    k = _require_nat(k, "k")
    start = deep_start(k)
    images = [layer_phis(k, m) if m >= start else set() for m in range(k)]
    zero = F_k(max(start, 0), 0, k) if k else (0, 0, 0, 0)
    out = []
    for m in range(start, k):
        for n in range(m + 1, k):
            inter = images[m] & images[n]
            if not inter:
                continue
            nonzero = sum(1 for phi in inter if phi != zero)
            out.append((m, n, len(inter), nonzero))
    return out


def cross_depth_overlap(k: int) -> int:
    """``∑_m C_{k,m} - M_k``."""
    return same_depth_total(k) - M_k_count(k)


def layer_count_report(k: int, r: int) -> dict[str, object]:
    """CLI payload for ``x3-layer-count``."""
    k = _require_nat(k, "k")
    r = _require_nat(r, "r")
    m = layer_depth(k, r)
    raw = 3**m
    easy = easy_count(m, r)
    core_n = core_domain_size(k, r)
    regime = n0_regime(k, r)
    if r > m:
        C = raw
        q_im = 0
        core_im = 0
        source = "shallow-n2"
    elif k < 4 * r + 1:
        C = C_unexhausted_formula(k, r)
        core_im = C - easy
        q_im = len(q_core_image(k, r))
        source = "unexhausted-formula"
    else:
        core = core_image(k, r)
        core_im = len(core)
        q_im = len({phi[0] for phi in core})
        C = easy + core_im
        source = "core-image"
    return {
        "k": k,
        "r": r,
        "m": m,
        "W": max(core_width(k, r), 0) if r <= m else 0,
        "regime": regime,
        "C": C,
        "raw": raw,
        "injective": easy,
        "core_domain": core_n,
        "core_image": core_im,
        "q_image": q_im,
        "overlap": raw - C,
        "source": source,
        "valuation_q": valuation_q_images(k, r) if r <= m else {},
    }


def states_report(k: int) -> dict[str, object]:
    """CLI payload for ``x3-states``."""
    k = _require_nat(k, "k")
    R = raw_count_x3(k)
    layers = [layer_count_report(k, k - 1 - m) for m in range(k)]
    Cs = [row["C"] for row in layers]
    sum_C = sum(Cs)
    M = M_k_count(k)
    q_contrib = [row["q_image"] for row in layers]
    return {
        "k": k,
        "R": R,
        "same_depth_totals": Cs,
        "sum_C": sum_C,
        "q_image_contributions": q_contrib,
        "cross_depth_overlap": sum_C - M,
        "zero_spine": zero_spine_depths(k),
        "zero_spine_overcount": zero_spine_overcount(k),
        "cross_depth_pairs": cross_depth_pairs(k),
        "M": M,
        "compression": (R - M),
        "ratio": (M / R) if R else None,
        "source": "shallow-sum + deep-image union",
    }


def verification_row(k: int, *, c_source: str, m_source: str) -> dict[str, object]:
    R = raw_count_x3(k)
    Cs = [C_layer(k, k - 1 - m) for m in range(k)]
    M = M_k_count(k)
    return {
        "k": k,
        "R": R,
        "M": M,
        "R_minus_M": R - M,
        "ratio": (M / R) if R else None,
        "C": Cs,
        "sum_C": sum(Cs),
        "c_source": c_source,
        "m_source": m_source,
    }
