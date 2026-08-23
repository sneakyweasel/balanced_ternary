"""Candidate invariants for the mismatched-width cubic quotient.

This module implements the Milestone 27 decision: residue / valuation /
discarded-digit candidates versus the exact two-scale expansion
``Q(a + 3^t b) = D^t(a^3) + 3 a^2 b + 3^{t+1} a b^2 + 3^{2t} b^3``.
"""

from __future__ import annotations

from collections import defaultdict

from bt.metrics import v3
from research.residuals.cubic_fibres import prefixes_at
from research.residuals.mismatched_cubic import (
    bal_digits,
    q_eq,
    q_image,
    q_mod,
    q_split_high,
    require_width,
)


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def split_two_scale(t: int, u: int) -> tuple[int, int]:
    """``u = a + 3^t b`` with ``a = bal_t(u)``."""
    t = _require_nat(t, "t")
    a = bal_digits(u, t)
    if t == 0:
        return 0, u
    return a, (u - a) // (3**t)


def q_expansion(t: int, a: int, b: int) -> int:
    """Integer two-scale expansion, identical to ``q_split_high``."""
    return q_split_high(t, a, b)


def surviving_exponents(t: int, K: int) -> dict[str, int | None]:
    """Valuation of each expansion term; ``None`` means the term is identically 0."""
    t = _require_nat(t, "t")
    K = _require_nat(K, "K")
    return {
        "low_Dt_a3": 0,
        "linear_3a2b": 1 if K > 1 else None,
        "quad_3^{t+1}ab2": (t + 1) if t + 1 < K else None,
        "cubic_3^{2t}b3": (2 * t) if 2 * t < K else None,
    }


def information_exponents(t: int, K: int) -> tuple[int, int]:
    """Sufficient ``(α, β)`` so that ``a mod 3^α`` and ``b mod 3^β`` determine ``Q``.

    The low part ``a`` is already a ``t``-digit balanced word, so ``α = t``.
    The linear carry ``3 a^2 b`` needs ``b`` modulo ``3^{K-1}`` on units.
    """
    t = _require_nat(t, "t")
    K = _require_nat(K, "K")
    alpha = t
    beta = 0 if K == 0 else max(0, K - 1)
    if t + 1 < K:
        beta = max(beta, K - (t + 1))
    if 2 * t < K:
        beta = max(beta, max(0, K - 2 * t))
    return alpha, beta


def B_t(t: int, u: int) -> int:
    return bal_digits(u**3, _require_nat(t, "t"))


def psi1(u: int, s: int) -> tuple[int, ...]:
    s = _require_nat(s, "s")
    return (u % (3**s if s else 1),)


def psi2(u: int, s: int) -> tuple[object, ...]:
    vu = v3(u)
    return ("inf" if vu is None else vu, *psi1(u, s))


def psi3(u: int, s: int) -> tuple[object, ...]:
    if u > 0:
        sgn = 1
    elif u < 0:
        sgn = -1
    else:
        sgn = 0
    return (*psi2(u, s), sgn)


def psi4(u: int, s: int, t: int, ell: int) -> tuple[object, ...]:
    ell = _require_nat(ell, "ell")
    return (*psi2(u, s), B_t(t, u) % (3**ell if ell else 1))


def psi5(u: int, t: int, alpha: int, beta: int) -> tuple[object, ...]:
    a, b = split_two_scale(t, u)
    vu = v3(u)
    am = 3 ** _require_nat(alpha, "alpha") if alpha else 1
    bm = 3 ** _require_nat(beta, "beta") if beta else 1
    return ("inf" if vu is None else vu, a % am, b % bm)


CANDIDATES = ("psi1", "psi2", "psi3", "psi4", "psi5")


def psi_of(
    name: str,
    u: int,
    t: int,
    s: int,
    ell: int | None = None,
    alpha: int | None = None,
    beta: int | None = None,
) -> tuple[object, ...]:
    if name == "psi1":
        return psi1(u, s)
    if name == "psi2":
        return psi2(u, s)
    if name == "psi3":
        return psi3(u, s)
    if name == "psi4":
        return psi4(u, s, t, t if ell is None else ell)
    if name == "psi5":
        if alpha is None:
            aa, bb = information_exponents(t, s)
        else:
            aa, bb = alpha, (0 if beta is None else beta)
        return psi5(u, t, aa, bb)
    raise ValueError(f"unknown candidate {name}")


def score_candidate(
    name: str,
    t: int,
    K: int,
    W: int,
    s: int,
    *,
    ell: int | None = None,
    alpha: int | None = None,
    beta: int | None = None,
    domain: list[int] | None = None,
) -> dict[str, object]:
    t = _require_nat(t, "t")
    K = _require_nat(K, "K")
    W = _require_nat(W, "W")
    points = domain if domain is not None else prefixes_at(W)
    by_psi: dict[tuple[object, ...], list[int]] = defaultdict(list)
    by_q: dict[int, list[int]] = defaultdict(list)
    qmap: dict[int, int] = {}
    for u in points:
        qv = q_mod(t, K, u)
        qmap[u] = qv
        key = psi_of(name, u, t, s, ell=ell, alpha=alpha, beta=beta)
        by_psi[key].append(u)
        by_q[qv].append(u)
    merges = 0
    merge_ex = None
    for members in by_psi.values():
        qs = {qmap[u] for u in members}
        if len(qs) > 1:
            merges += 1
            if merge_ex is None:
                merge_ex = (members[0], next(x for x in members[1:] if qmap[x] != qmap[members[0]]))
    splits = 0
    split_ex = None
    for members in by_q.values():
        keys = {psi_of(name, u, t, s, ell=ell, alpha=alpha, beta=beta) for u in members}
        if len(keys) > 1:
            splits += 1
            if split_ex is None:
                split_ex = (members[0], next(x for x in members[1:] if psi_of(name, x, t, s, ell=ell, alpha=alpha, beta=beta) != psi_of(name, members[0], t, s, ell=ell, alpha=alpha, beta=beta)))
    return {
        "candidate": name,
        "t": t,
        "K": K,
        "W": W,
        "s": s,
        "raw": len(points),
        "q_classes": len(by_q),
        "psi_classes": len(by_psi),
        "false_merges": merges,
        "false_splits": splits,
        "merge_example": merge_ex,
        "split_example": split_ex,
        "exact": merges == 0 and splits == 0,
    }


def one_family(t: int, W: int) -> list[int]:
    """Units ``1 + 3^t b`` that still lie in ``P_W``."""
    t = _require_nat(t, "t")
    W = _require_nat(W, "W")
    bound = (3**W - 1) // 2
    out: list[int] = []
    if t == 0:
        return [u for u in prefixes_at(W) if u % 3 == 1]
    step = 3**t
    b = 0
    while True:
        u = 1 + step * b
        if abs(u) > bound:
            break
        out.append(u)
        b += 1
    b = -1
    while True:
        u = 1 + step * b
        if abs(u) > bound:
            break
        out.append(u)
        b -= 1
    return sorted(out)


def one_family_obstruction(t: int, K: int, W: int) -> dict[str, object]:
    """Same ``(v3, u mod 3^t, B_t)``, many ``Q``-classes when ``t ≥ 1``."""
    t = _require_nat(t, "t")
    K = _require_nat(K, "K")
    W = _require_nat(W, "W")
    fam = one_family(t, W)
    qs = {q_mod(t, K, u) for u in fam}
    bals = {B_t(t, u) for u in fam}
    residues = {u % (3**t if t else 1) for u in fam}
    return {
        "t": t,
        "K": K,
        "W": W,
        "family_size": len(fam),
        "q_classes": len(qs),
        "shared_residue_mod_3^t": len(residues) == 1,
        "shared_B_t": len(bals) == 1,
        "lower_bound_trits": _log3_ceil(len(qs)),
        "family": fam[:12],
    }


def _log3_ceil(n: int) -> int:
    if n <= 1:
        return 0
    e = 0
    p = 1
    while p < n:
        p *= 3
        e += 1
    return e


def invariant_report(t: int, K: int, W: int) -> dict[str, object]:
    t = _require_nat(t, "t")
    K = _require_nat(K, "K")
    W = _require_nat(W, "W")
    alpha, beta = information_exponents(t, K)
    image = q_image(t, K, W)
    scores = []
    for name, s in (
        ("psi1", min(W, t) if t else 0),
        ("psi2", min(W, t) if t else 0),
        ("psi3", min(W, t) if t else 0),
        ("psi4", min(W, t) if t else 0),
        ("psi5", K),
    ):
        if name == "psi5":
            scores.append(score_candidate(name, t, K, W, K, alpha=alpha, beta=min(beta, max(W - t, 0))))
        else:
            scores.append(score_candidate(name, t, K, W, s, ell=t))
    # full-width residue is tautological on P_W
    scores.append(score_candidate("psi1", t, K, W, W))
    obst = one_family_obstruction(t, K, W) if t >= 1 else None
    return {
        "t": t,
        "K": K,
        "W": W,
        "raw": 3**W,
        "q_classes": len(image),
        "alpha_beta": (alpha, beta),
        "surviving": surviving_exponents(t, K),
        "candidates": scores,
        "one_family": obst,
        "high_val_zero": f"Q=0 when 3s-t ≥ K",
        "verdict": (
            "Outcome C: residue/valuation/B_t invariants require growing width; "
            "the extra 2r high trits remain visible through 3a^2 b"
        ),
    }


def invariant_compare(t: int, K: int, W: int, u: int, v: int) -> dict[str, object]:
    require_width(W, u)
    require_width(W, v)
    t = _require_nat(t, "t")
    K = _require_nat(K, "K")
    au, bu = split_two_scale(t, u)
    av, bv = split_two_scale(t, v)
    s = t
    same_q = q_eq(t, K, u, v)
    keys = {
        name: (
            psi_of(name, u, t, s, ell=t),
            psi_of(name, v, t, s, ell=t),
        )
        for name in ("psi1", "psi2", "psi3", "psi4")
    }
    keys["psi5"] = (psi5(u, t, t, max(W - t, 0)), psi5(v, t, t, max(W - t, 0)))
    missing = []
    if same_q:
        for name, (pu, pv) in keys.items():
            if pu != pv:
                missing.append(f"{name} splits a true Q-fibre")
    else:
        for name, (pu, pv) in keys.items():
            if pu == pv:
                missing.append(f"{name} merges distinct Q-classes")
    if not same_q and keys["psi4"][0] == keys["psi4"][1]:
        missing.append("discarded B_t and low residue agree; high-trit carry 3a^2 b differs")
    return {
        "t": t,
        "K": K,
        "W": W,
        "u": u,
        "v": v,
        "v3_u": v3(u),
        "v3_v": v3(v),
        "a_u": au,
        "b_u": bu,
        "a_v": av,
        "b_v": bv,
        "B_t_u": B_t(t, u),
        "B_t_v": B_t(t, v),
        "Q_u": q_mod(t, K, u),
        "Q_v": q_mod(t, K, v),
        "same_Q": same_q,
        "expansion_u": q_expansion(t, au, bu),
        "expansion_v": q_expansion(t, av, bv),
        "psi": {name: {"u": pu, "v": pv, "same": pu == pv} for name, (pu, pv) in keys.items()},
        "missing": missing,
    }
