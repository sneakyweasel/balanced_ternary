"""Second-pass audit of the explicit constants in ``docs/theory/juggler_oeoee_production.md`` §11.

The note reduces the ``OEOEE`` count on the exact fibre ``J(m')`` to fifteen sign sums and bounds
them with a five-item toolkit (Vaaler, Kusmin--Landau, a second-derivative test, block counting,
pairing), arriving at the envelope ``|16|O(m')| - Y| <= 100 Y m'^{-4/9} (1 + log m')^2``.  Its
status line asked for an audit pass before the exponent ``lambda**`` is promoted.  This module is
that pass: every intermediate inequality is evaluated on exact data (``measured``), and the whole
envelope is re-assembled independently with every factor kept explicit (``assemble``), including
three corrections to the note --

* (T3) the additive constant in the second-derivative test is 2, not 1 (the two discarded
  near-integer intervals of a piece each cost one extra lattice point);
* (T4) the block-counting constant ``4(V+1)`` needs the blocks to have nearly equal length
  (here ``[(1 - 8/(9m')) delta, delta]``), not merely length ``<= delta``; with that hypothesis
  it holds because, ``f'`` being monotone, an endpoint is the minimum of ``||f'||`` over at most
  one block for every annulus ``j >= 1``;
* the ``Lambda_3``-alone pairing bound ``0.89 m'^{14/9}`` omits the ``V Delta / 2`` term of (T5):
  consecutive level sets of ``floor(w^{3/4})`` differ in length by one, so ``Delta ~ omega``,
  and the honest bound is ``(2/3) m'^{17/9} + (8/9) m'^{14/9}``; the data exceed the stated
  constant at ``m' = 200`` and sit below the corrected one everywhere.

None of the corrections touches the exponent ``-4/9`` (``= P^{-1/8}``) or the leading constant:
the assembled bound stays below the note's envelope for every ``m' >= 4`` (it is vacuous below).
"""

from __future__ import annotations

import math
from math import isqrt, log, pi, sqrt
from typing import Any

import numpy as np


def icbrt_ceil(a: int) -> int:
    """Least integer ``c`` with ``c^3 >= a``."""

    c = int(round(a ** (1 / 3))) + 2
    while (c - 1) ** 3 >= a:
        c -= 1
    while c**3 < a:
        c += 1
    return c


def kusmin_landau(delta: float) -> float:
    return 2 / (pi * delta)


def second_derivative_test(lam: float, alpha: float, M: float) -> float:
    """(T3) with the corrected additive constant: ``(alpha lam M + 1)(2.26 lam^{-1/2} + 2)``."""

    return (alpha * lam * M + 1) * (2.26 / sqrt(lam) + 2)


def assemble(mp: int, S: int | None = None, R: int | None = None) -> dict[str, Any]:
    """Independent assembly of the fifteen-term bound at source ``m'``, every factor explicit."""

    m1 = mp + 1
    L = (8 / 3) * m1 ** (5 / 3) + 1
    Ylow = (16 / 9) * mp ** (23 / 9) - 1
    Yup = (16 / 9) * m1 ** (23 / 9) + 1
    omax = (2 / 3) * m1 ** (8 / 9) + 1.5
    phimax, phimin = (2 / 3) * m1 ** (8 / 9), (2 / 3) * mp ** (8 / 9)
    pw = 2 * phimax - phimin
    eta = 1.5 * L
    if R is None:
        R = max(1, int(0.224 * mp ** (4 / 9)))

    def sum_abs_S(q: int) -> float:
        delta = q * mp ** (-8 / 9)
        V = (8 * q / 3) * m1 ** (7 / 9)
        return 4 * (V + 1) * omax + (8 / (pi * delta)) * (V + 1) * (1 + max(0.0, log(1 / (2 * delta))))

    EB = Yup / (R + 1) + sum(2 * (min(1.0, 2 / q) + 1 / (R + 1)) * sum_abs_S(q) for q in range(1, R + 1))
    if S is None:
        S = max(1, int(0.318 * mp ** (4 / 9)))
    U = S
    if U > (2 / 3) * mp ** (2 / 3):
        raise ValueError("Vaaler truncation too large for the Kusmin--Landau twist bound")
    alpha = (m1 / mp) ** (4 / 3)
    lam = lambda s: (3 * s / 8) * m1 ** (-4 / 3)
    cs = {s: min(1.0, 2 / abs(s)) + 1 / (S + 1) for s in range(-S, S + 1) if s}
    cs[0] = 1 / (S + 1)
    cu = {u: min(1.0, 2 / abs(u)) + 1 / (U + 1) for u in range(-U, U + 1) if u}
    cu[0] = 1 / (U + 1)
    EA: dict[tuple[int, int, int], float] = {}
    for b in (0, 1):
        A0 = sum(c * second_derivative_test(lam(abs(s)), alpha, L) for s, c in cs.items() if s) + cs[0] * (L if b == 0 else 1.0)
        EA[(b, 1, 0)] = pw * A0 + eta
        alpha1 = alpha * (1 + (U / 4) * mp ** (-2))
        A1 = 0.0
        for s, c in cs.items():
            for u, d in cu.items():
                if s:
                    X = second_derivative_test(lam(abs(s)), alpha1, L)
                elif u:
                    X = kusmin_landau((3 * abs(u) / 8) * m1 ** (-2 / 3)) if b == 0 else 2.55
                else:
                    X = L if b == 0 else 1.0
                A1 += c * d * X
        EA[(b, 1, 1)] = pw * A1 + eta
    V = 2 * mp + 3
    G = ((4 / 3) * m1 ** (2 / 3) + 1) * omax
    Delta = 2 * omax + 1
    EL3 = V * Delta / 2 + G
    EL13 = pw * (sum(2.55 * d for u, d in cu.items() if u) + cu[0]) + eta
    EL1 = pw + eta
    total = 8 * EB + sum(EA.values()) + EL3 + EL13 + EL1
    envelope = 100 * mp ** (-4 / 9) * (1 + log(mp)) ** 2
    return {
        "mp": mp, "R": R, "S": S, "total": total, "half_B_each": EB, "half_A": EA,
        "lambda3_alone": EL3, "lambda1_lambda3": EL13, "lambda1_alone": EL1,
        "theta_bound": total / Ylow, "note_envelope": envelope, "ratio_to_note_envelope": total / Ylow / envelope,
    }


def measured(mp: int, Q: int = 12) -> dict[str, Any]:
    """Every intermediate quantity of §11 on exact data at source ``m'``."""

    Wlo, Whi = icbrt_ceil(mp**8), icbrt_ceil((mp + 1) ** 8)
    lo, hi = icbrt_ceil(Wlo**4), icbrt_ceil(Whi**4)
    Sc = 10**10
    ixp, fxs, wl = [], [], []
    n = lo if lo & 1 else lo + 1
    while n < hi:
        n3 = n * n * n
        ix = isqrt(n3)
        ixp.append(ix & 1)
        fxs.append((isqrt(n3 * Sc * Sc) - ix * Sc) / Sc)
        wl.append(isqrt(ix))
        n += 2
    ixp_a = np.array(ixp, dtype=np.int64)
    fx = np.array(fxs)
    wv = np.array(wl, dtype=np.int64)
    Y = len(wv)
    L = Whi - Wlo
    idx = wv - Wlo
    omega = np.bincount(idx, minlength=L).astype(float)
    wa = np.arange(Wlo, Whi)
    psi1 = 1 - 2 * ixp_a
    T = np.bincount(idx, weights=psi1, minlength=L)
    L1 = np.where(wa & 1, -1.0, 1.0)
    L2 = np.array([(-1) ** (isqrt(int(x) ** 3) & 1) for x in wa], dtype=float)
    v = np.array([isqrt(isqrt(int(x) ** 3)) for x in wa])
    L3 = np.where(v & 1, -1.0, 1.0)
    O = float(((1 + psi1) * (1 - L1[idx]) * (1 + L2[idx]) * (1 + L3[idx])).sum() / 16)
    per_q = []
    for q in range(1, Q + 1):
        ph = ((q * ixp_a) % 2) / 2.0 + q * fx / 2.0
        z = np.exp(2j * pi * ph)
        Sq = np.bincount(idx, weights=z.real, minlength=L) + 1j * np.bincount(idx, weights=z.imag, minlength=L)
        absS = np.abs(Sq)
        delta = q * mp ** (-8 / 9)
        Vq = (8 * q / 3) * (mp + 1) ** (7 / 9)
        a0 = (3 * q / 2) * wa.astype(float) ** (2 / 3)
        a1 = (3 * q / 2) * (wa.astype(float) + 1) ** (2 / 3)
        d0, d1 = np.abs(a0 - np.round(a0)), np.abs(a1 - np.round(a1))
        minnorm = np.where(np.floor(a1) > np.floor(a0), 0.0, np.minimum(d0, d1))
        j = np.floor(minnorm / delta).astype(int)
        counts = np.bincount(j)
        kl_worst = 0.0
        for jj in range(1, int(j.max()) + 1):
            sel = j == jj
            if sel.any():
                kl_worst = max(kl_worst, float((absS[sel] * (pi * jj * delta) / 2).max()))
        per_q.append({
            "q": q, "sum_abs_S": float(absS.sum()),
            "note_bound": (64 / 9) * q * mp ** (5 / 3) + 6.79 * mp ** (5 / 3) * (1 + (8 / 9) * log(mp)),
            "annulus_max_over_4V1": float(counts.max() / (4 * (Vq + 1))),
            "kusmin_landau_worst_ratio": kl_worst,
            "block_length_over_delta_min": float((a1 - a0).min() / delta),
            "block_length_over_delta_max": float((a1 - a0).max() / delta),
        })
    vs = np.unique(v)
    g = np.array([omega[v == vv].sum() for vv in vs])
    t5_exact = len(vs) * float(np.max(np.abs(np.diff(g)))) / 2 + float(g.max())
    lam3_sum = abs(float((omega * L3).sum()))
    halfA = {(b, c, d): float((omega * L1**b * L2**c * L3**d).sum()) for b in (0, 1) for c in (0, 1) for d in (0, 1) if (b, c, d) != (0, 0, 0)}
    halfB = {(b, c, d): float((T * L1**b * L2**c * L3**d).sum()) for b in (0, 1) for c in (0, 1) for d in (0, 1)}
    return {
        "mp": mp, "L": L, "Y": Y, "share": O / Y, "deviation": abs(16 * O - Y),
        "sizes_ok": bool((8 / 3) * mp ** (5 / 3) - 1 <= L <= (8 / 3) * (mp + 1) ** (5 / 3) + 1 and Y >= (16 / 9) * mp ** (23 / 9) - 1),
        "omega_deviation_max": float(np.max(np.abs(omega - (2 / 3) * wa.astype(float) ** (1 / 3)))),
        "sum_abs_T": float(np.abs(T).sum()), "per_q": per_q,
        "lambda3_alone_sum": lam3_sum, "lambda3_note_bound": 0.89 * mp ** (14 / 9),
        "lambda3_T5_exact": t5_exact, "lambda3_corrected_bound": (2 / 3) * mp ** (17 / 9) + (8 / 9) * mp ** (14 / 9),
        "half_A_sums": halfA, "half_B_sums": halfB,
    }


def t3_worst_ratio(mp: int, s_max: int = 6, u_max: int = 6) -> float:
    """Worst ``|sum e(g)| / (T3 bound)`` over the Half-A modes at source ``m'``."""

    Wlo, Whi = icbrt_ceil(mp**8), icbrt_ceil((mp + 1) ** 8)
    w = list(range(Wlo, Whi))
    L = len(w)
    Sc = 10**8
    fr = np.array([(isqrt(x * x * x * Sc * Sc) % (2 * Sc)) / Sc for x in w])
    fr34 = np.array([(isqrt(isqrt(x * x * x * Sc**4)) % (2 * Sc)) / Sc for x in w])
    par = np.array([x % 2 for x in w], dtype=float)
    worst = 0.0
    for s in range(1, s_max + 1):
        for u in range(0, u_max + 1):
            for b in (0, 1):
                ph = (s * fr / 2 + u * fr34 / 2 + b * par / 2) % 1.0
                tot = abs(np.exp(2j * pi * ph).sum())
                lam = (3 * s / 8) * (mp + 1) ** (-4 / 3)
                alpha = ((mp + 1) / mp) ** (4 / 3) * (1 + (u / (4 * s)) * Wlo ** (-3 / 4))
                worst = max(worst, tot / second_derivative_test(lam, alpha, L))
    return worst


def audit(sources: tuple[int, ...] = (60, 120, 200)) -> dict[str, Any]:
    grid = list(range(2, 40)) + [60, 100, 200, 500, 1000, 10**4, 10**6, 10**8]
    ratios = {mp: assemble(mp)["ratio_to_note_envelope"] for mp in grid}
    least_ok = min(mp for mp in grid if all(ratios[m] < 1 for m in grid if m >= mp))
    return {
        "envelope_ratio_by_source": ratios, "envelope_holds_from": least_ok,
        "least_constant_from_2": max(100 * r for r in ratios.values()),
        "measured": {mp: measured(mp) for mp in sources},
        "assembled": {mp: assemble(mp) for mp in sources},
    }
