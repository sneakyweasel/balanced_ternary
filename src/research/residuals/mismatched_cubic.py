"""Mismatched-width cubic quotient ``Q_{t,K,W}(u) = D^t(u^3) mod 3^K``.

The domain is the balanced interval ``P_W``.  This is not a standard
cubic residual: the input width ``W`` may exceed the ``D``-depth ``t``,
and the modulus exponent ``K`` may exceed ``t+1``.

For the cubic residual problem in the exhausted regime one has
``t = k-1-4r``, ``K = k``, ``W = k-1-2r = t+2r``.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from research.residuals.cubic_fibres import balanced_bound, prefixes_at
from bt.calculus.jets import integer_jet
from bt.calculus.quadratic import iter_dz, pack_word
from bt.metrics import v3


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def q_params(k: int, r: int) -> tuple[int, int, int]:
    """``(t, K, W)`` of the exhausted cubic residual at deficit ``r``."""
    k = _require_nat(k, "k")
    r = _require_nat(r, "r")
    if k < 4 * r + 1:
        raise ValueError("need k ≥ 4r+1 so that t = k-1-4r ≥ 0")
    return k - 1 - 4 * r, k, k - 1 - 2 * r


def bal_digits(z: int, t: int) -> int:
    """Canonical balanced representative of ``z`` modulo ``3^t``."""
    t = _require_nat(t, "t")
    if t == 0:
        return 0
    return pack_word(integer_jet(z, t))


def q_int(t: int, u: int) -> int:
    """Integer value ``D^t(u^3)``."""
    return iter_dz(u**3, _require_nat(t, "t"))


def q_mod(t: int, K: int, u: int) -> int:
    K = _require_nat(K, "K")
    return q_int(t, u) % (3**K if K else 1)


def q_eq(t: int, K: int, u: int, v: int) -> bool:
    return q_mod(t, K, u) == q_mod(t, K, v)


def q_recon_delta(t: int, u: int, v: int) -> int:
    """``u^3 - v^3 - (bal_t(u^3) - bal_t(v^3))``."""
    t = _require_nat(t, "t")
    return (u**3 - v**3) - (bal_digits(u**3, t) - bal_digits(v**3, t))


def q_eq_iff(t: int, K: int, u: int, v: int) -> bool:
    """Exact reconstruction criterion, as a boolean."""
    K = _require_nat(K, "K")
    t = _require_nat(t, "t")
    return q_recon_delta(t, u, v) % (3 ** (t + K) if t + K else 1) == 0


def q_split_high(t: int, a: int, b: int) -> int:
    """``D^t((a + 3^t b)^3)`` via the high-trit expansion."""
    t = _require_nat(t, "t")
    return (
        q_int(t, a)
        + 3 * a * a * b
        + (3 ** (t + 1)) * a * b * b
        + (3 ** (2 * t)) * b * b * b
    )


def q_val_int(t: int, u: int) -> int:
    """Two-regime formula for ``D^t(u^3)`` from ``v3(u)``."""
    t = _require_nat(t, "t")
    if u == 0:
        return 0
    s = v3(u)
    assert s is not None
    w = u // (3**s)
    if t <= 3 * s:
        return (3 ** (3 * s - t)) * (w**3)
    return iter_dz(w**3, t - 3 * s)


def visibility_bound(t: int, K: int) -> int:
    """Sufficient unit-scale bound ``s = max(1, t+K-1)``."""
    t = _require_nat(t, "t")
    K = _require_nat(K, "K")
    return max(1, t + K - 1)


def require_width(W: int, u: int) -> None:
    if abs(u) > balanced_bound(_require_nat(W, "W")):
        raise ValueError(f"u={u} is outside P_{W}")


def q_fibre(t: int, K: int, W: int, u: int) -> list[int]:
    require_width(W, u)
    return [v for v in prefixes_at(W) if q_eq(t, K, u, v)]


def q_image(t: int, K: int, W: int) -> dict[int, list[int]]:
    buckets: dict[int, list[int]] = defaultdict(list)
    for u in prefixes_at(W):
        buckets[q_mod(t, K, u)].append(u)
    return buckets


def q_report(t: int, K: int, W: int) -> dict[str, object]:
    t = _require_nat(t, "t")
    K = _require_nat(K, "K")
    W = _require_nat(W, "W")
    image = q_image(t, K, W)
    units = [u for u in prefixes_at(W) if u % 3 != 0]
    unit_classes = {q_mod(t, K, u) for u in units}
    nontrivial = [sorted(ps) for ps in image.values() if len(ps) > 1]
    hist = dict(sorted(Counter(len(v) for v in image.values()).items()))
    by_v: Counter[str] = Counter()
    for u in prefixes_at(W):
        vu = v3(u)
        by_v["inf" if vu is None else str(vu)] += 1
    extra = W - t
    return {
        "t": t,
        "K": K,
        "W": W,
        "raw": 3**W,
        "classes": len(image),
        "unit_prefixes": len(units),
        "unit_classes": len(unit_classes),
        "nontrivial": len(nontrivial),
        "histogram": hist,
        "max_fibre": max((len(v) for v in image.values()), default=1),
        "min_nontrivial": min((len(v) for v in nontrivial), default=0),
        "width_excess": extra,
        "visibility_s": visibility_bound(t, K),
        "stratum_sizes": dict(sorted(by_v.items(), key=lambda kv: (kv[0] == "inf", int(kv[0]) if kv[0] != "inf" else 0))),
        "examples": nontrivial[:8],
    }


def q_compare(t: int, K: int, u: int, v: int) -> dict[str, object]:
    t = _require_nat(t, "t")
    K = _require_nat(K, "K")
    bu = bal_digits(u**3, t)
    bv = bal_digits(v**3, t)
    du = q_int(t, u)
    dv = q_int(t, v)
    delta = q_recon_delta(t, u, v)
    return {
        "t": t,
        "K": K,
        "u": u,
        "v": v,
        "u3": u**3,
        "v3": v**3,
        "bal_u3": bu,
        "bal_v3": bv,
        "Dt_u3": du,
        "Dt_v3": dv,
        "Q_u": q_mod(t, K, u),
        "Q_v": q_mod(t, K, v),
        "equal": q_eq(t, K, u, v),
        "recon_delta": delta,
        "recon_ok": q_eq_iff(t, K, u, v),
        "v3_u": v3(u),
        "v3_v": v3(v),
        "v3_Dt_u": v3(du),
        "cube_mod_sufficient": (u**3 - v**3) % (3 ** (t + K) if t + K else 1) == 0,
    }


def unit_extra_collisions(t: int, K: int, W: int) -> list[tuple[int, int]]:
    """Unit pairs with ``Q`` equal but not ``u ≡ v (mod 3^{t+K-1})``."""
    s = visibility_bound(t, K)
    hits: list[tuple[int, int]] = []
    units = [u for u in prefixes_at(W) if u % 3 != 0]
    for i, u in enumerate(units):
        for v in units[i + 1 :]:
            if q_eq(t, K, u, v) and (u - v) % (3**s) != 0:
                hits.append((u, v))
    return hits


def common_modulus_exp(members: list[int], cap: int = 32) -> int:
    """Largest ``e ≤ cap`` such that all members agree modulo ``3^e``."""
    if len(members) <= 1:
        return cap
    e = 0
    while e < cap:
        mod = 3 ** (e + 1)
        residue = members[0] % mod
        if any(x % mod != residue for x in members[1:]):
            return e
        e += 1
    return cap


def q_visibility(t: int, K: int, W: int, u: int) -> dict[str, object]:
    """What the fibre of ``u`` exposes about residues and discarded digits."""
    require_width(W, u)
    members = q_fibre(t, K, W, u)
    s = visibility_bound(t, K)
    bals = sorted({bal_digits(x**3, t) for x in members})
    vals = sorted({("inf" if v3(x) is None else v3(x)) for x in members}, key=lambda x: (x == "inf", x if x != "inf" else 0))
    return {
        "t": t,
        "K": K,
        "W": W,
        "u": u,
        "fibre": members,
        "fibre_size": len(members),
        "visibility_s": s,
        "agrees_mod_s": all((x - u) % (3**s) == 0 for x in members),
        "common_mod_exp": common_modulus_exp(members),
        "bal_values": bals,
        "valuations": vals,
        "width_excess": W - t,
        "cube_mod_necessary_on_fibre": len(bals) == 1,
    }


def q_prefix_state_counts(t: int, K: int, W: int) -> list[int]:
    """Exploratory MN class counts by LSD prefix length, not a theorem."""
    W = _require_nat(W, "W")
    prefixes = prefixes_at(W)
    values = {u: q_mod(t, K, u) for u in prefixes}
    counts: list[int] = []
    for j in range(W + 1):
        mod = 3**j if j else 1
        buckets: dict[int, dict[int, int]] = defaultdict(dict)
        for u in prefixes:
            buckets[u % mod][u] = values[u]
        signatures: set[tuple[tuple[int, int], ...]] = set()
        for table in buckets.values():
            high_map = tuple(sorted(((u - (u % mod)) // mod, q) for u, q in table.items()))
            signatures.add(high_map)
        counts.append(len(signatures))
    return counts
