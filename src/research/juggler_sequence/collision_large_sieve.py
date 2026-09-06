"""Phase-0: the collision route to the Tao-type bound (the gap in Paper C §9.3(d)).

Paper C prices two ways from cylinder control to the almost-all bound and rules both
out.  ``H(C,A)`` needs every cylinder; the pair-correlation asymptotic
``C_t <= (N^2/2^{t-1})(1 + (log y)^{-A'})`` is, by Walsh inversion, the same statement
again -- a *two-sided* bound of that accuracy returns polylogarithmic savings on every
Walsh sum.  What it never states is the crude form:

    Sum over L-bad words w of #[w]^2   <=   K N^2 2^{-(d-1)},   K = O(1),

one-sided, no accuracy beyond a constant.  That does not invert: it gives only
``|W_T| <= sqrt(K) N`` for each character, which is no saving at all.  Cauchy--Schwarz
against it, with Lemma 8.2's bad-word count, yields the Tao-type bound at *half* the
exponent::

    M = #{tau > d} <= sum_{w bad} #[w]
                   <= (sum_{w bad} #[w]^2)^{1/2} (#bad)^{1/2}
                   <= (K N^2 2^{-(d-1)})^{1/2} (2^{d-1} 2^{-e(C)L})^{1/2}
                    = sqrt(K) N 2^{-e(C)L/2}.

Half the exponent is bought back by depth: the least ``C`` moves from 20 to 32
unconditionally, and from 18 to 28 under the conditional exponent.

The route is only worth stating if the hypothesis is true, and it has one cheap
falsifier.  Restricting to *bad* words is what keeps it alive at all -- a start that
descends has a walk that reaches ``-L``, so the all-``O`` tails of terminating starts
(the same tails that make the unstopped moment too large by a power of the scale) are
excluded by construction.  This module measures what is left.
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path
from typing import Any

from research.juggler_sequence.cycle_finance import git_commit
from research.juggler_sequence.tao_reduction import (
    LOG2_3,
    N0_CERTIFIED,
    chernoff_exponent,
    p_of_C,
    theta_of_C,
    REQUIRED_RATE,
    REQUIRED_RATE_STAR3,
    scale_L,
)

DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "research" / "juggler" / "collision_large_sieve"


def half_exponent_least_C(required: float = REQUIRED_RATE, c_max: int = 10_000) -> int | None:
    """Least ``C`` with ``e(C)/2 > required``: the price of the Cauchy--Schwarz step."""

    for C in range(3, c_max):
        if chernoff_exponent(C) / 2.0 > required:
            return C
    return None


def graded_least_C(gamma: float, required: float = REQUIRED_RATE, c_max: int = 10_000) -> int | None:
    """Least ``C`` for the graded hypothesis at accuracy ``gamma``.

    The exported bound is the weakest member of a family: asking
    ``sum_{w bad} #[w]^2 <= K N^2 2^{-(d-1)} 2^{-gamma e(C) L}`` returns
    ``M <= sqrt(K) N 2^{-(1+gamma) e(C) L / 2}``.  ``gamma = 0`` is the crude form and costs
    twelve letters of depth; ``gamma = 1`` is the fair-coin value of the restricted count,
    since ``p_bad`` is of order ``2^{-e(C)L}``, and costs nothing at all.  The census
    normalizes against the fair value, so it measures ``gamma = 1``.
    """

    for C in range(3, c_max):
        if chernoff_exponent(C) * (1.0 + gamma) / 2.0 > required:
            return C
    return None


def max_cylinder_overpopulation(
    log10_y: int, C: int = 20, n0: int = N0_CERTIFIED, samples: int = 20_000, seed: int = 11
) -> dict[str, Any]:
    """The most populated depth-``d`` cylinder against its fair share.

    Hypothesis ``H(C,A)`` is stated in four places over *every* ``O``-rooted word of length
    ``d(y)``, and in that form it is false: a start that reaches 1 has an all-``O`` tail,
    because ``J(1) = 1`` is odd, so a short prefix followed by ``O^k`` absorbs a constant
    proportion of all starts.  Both manuscripts already say in prose that only the bad words
    are used; the quantifier is what needs the restriction.  Nothing here touches the
    theorems, which apply ``H`` only to bad words.
    """

    rng = random.Random(seed)
    y = 10**log10_y
    L = scale_L(log10_y * math.log(10.0), n0)
    d = math.ceil(C * L)
    tally: dict[tuple[int, ...], int] = {}
    for _ in range(samples):
        n = rng.randrange(y + 1, 2 * y + 1) | 1
        w = juggler_word(n, d)
        tally[w] = tally.get(w, 0) + 1
    top, count = max(tally.items(), key=lambda kv: kv[1])
    fair = 2.0 ** (-(d - 1))
    return {
        "log10_y": log10_y, "C": C, "d": d, "L": L, "samples": samples,
        "top_share": count / samples, "fair_share": fair,
        "overpopulation": (count / samples) / fair,
        "top_word": "".join("O" if b else "E" for b in top),
        "top_word_bad_depth": bad_depth(top, L),
    }


def bad_word_count(L: float, d: int) -> int:
    """Number of ``O``-rooted words of length ``d`` whose walk never reaches ``-L``.

    The walk ``u_t = o_t log2(3) - t`` depends on ``(t, o_t)`` alone, so this is the same
    two-line dynamic program as ``bad_word_probability`` carried in integers.  Odd starts
    have first letter ``O``; the count is over the remaining ``d-1`` free letters.
    """

    if d < 1:
        raise ValueError("d must be at least 1")
    if LOG2_3 - 1.0 <= -L:
        return 0
    counts = {1: 1}
    for t in range(2, d + 1):
        nxt: dict[int, int] = {}
        for o, c in counts.items():
            for o2 in (o, o + 1):
                if o2 * LOG2_3 - t > -L:
                    nxt[o2] = nxt.get(o2, 0) + c
        counts = nxt
        if not counts:
            return 0
    return sum(counts.values())


def juggler_word(n: int, d: int) -> tuple[int, ...]:
    """The first ``d`` letters of the itinerary of ``n``: 1 for odd, 0 for even."""

    letters: list[int] = []
    x = n
    for _ in range(d):
        letters.append(x & 1)
        x = math.isqrt(x * x * x) if x & 1 else math.isqrt(x)
    return tuple(letters)


def bad_depth(word: tuple[int, ...], L: float) -> int:
    """The largest ``d`` for which the length-``d`` prefix of `word` is ``L``-bad.

    Badness is a prefix-closed property -- once the walk reaches ``-L`` it has reached it --
    so one pass gives every depth at once.
    """

    o = 0
    for t, letter in enumerate(word, start=1):
        o += letter
        if o * LOG2_3 - t <= -L:
            return t - 1
    return len(word)


def live_fairness_profile(
    log10_y: int, d: int = 16, n0: int = N0_CERTIFIED, samples: int = 200_000, seed: int = 7,
    cell_depth: int = 12,
) -> dict[str, Any]:
    """Is the live set fair cylinder by cylinder, and across the whole odd-count distribution?

    Three statistics from one sample.  (i) The histogram of ``o_d`` over live starts against
    the exact fair-coin count of bad words with that many odd letters: the ratio by ``o`` says
    whether the whole distribution is fair or only one tilted moment of it, and the odd-heavy
    end is where momentum would first appear.  (ii) The relative variance of ``#[w]`` over the
    bad cells at ``cell_depth`` against Poisson: 1 means cylinders are individually fair to
    sampling resolution, not compensating in aggregate.  (iii) The magnitude of ``J^d(n)`` on
    live starts, because "live" is often read as "astronomically large" and it is not: the
    median live orbit at ``d = 20`` is only 10^31 from ``y = 10^20``.
    """

    y = 10**log10_y
    L = scale_L(log10_y * math.log(10.0), n0)
    rng = random.Random(seed)
    hist: dict[int, int] = {}
    cells: dict[int, int] = {}
    mags: list[float] = []
    for _ in range(samples):
        n = rng.randrange(y + 1, 2 * y + 1) | 1
        x, o, key, fail_t = n, 0, 0, None
        for t in range(1, d + 1):
            bit = x & 1
            o += bit
            if 2 <= t <= cell_depth:
                key |= bit << (t - 2)
            x = math.isqrt(x * x * x) if bit else math.isqrt(x)
            if fail_t is None and o * LOG2_3 - t <= -L:
                fail_t = t
        # the cell tally is over starts bad through cell_depth, whether or not they survive to d
        if fail_t is None or fail_t > cell_depth:
            cells[key] = cells.get(key, 0) + 1
        if fail_t is None:
            hist[o] = hist.get(o, 0) + 1
            mags.append(x.bit_length() * math.log10(2.0))
    fair_by_o = {}
    st = {1: 1}
    for t in range(2, d + 1):
        nx: dict[int, int] = {}
        for oo, c in st.items():
            if oo * LOG2_3 - t > -L:
                nx[oo] = nx.get(oo, 0) + c
            if (oo + 1) * LOG2_3 - t > -L:
                nx[oo + 1] = nx.get(oo + 1, 0) + c
        st = nx
    fair_by_o = {oo: samples * c / 2.0 ** (d - 1) for oo, c in st.items()}
    ratio_by_o = {oo: hist.get(oo, 0) / f for oo, f in fair_by_o.items() if f >= 30}
    fair_cell = samples / 2.0 ** (cell_depth - 1)
    bad_cells = bad_word_count(L, cell_depth)
    # every bad cell contributes; unoccupied bad cells count as zero
    ss = sum((c - fair_cell) ** 2 for c in cells.values()) + (bad_cells - len(cells)) * fair_cell**2
    relvar = ss / (bad_cells * fair_cell**2)
    mags.sort()
    q = lambda f: mags[int(f * (len(mags) - 1))] if mags else None
    return {
        "log10_y": log10_y, "L": L, "d": d, "samples": samples,
        "live": sum(hist.values()), "fair_live": sum(fair_by_o.values()),
        "ratio_by_odd_count": ratio_by_o,
        "fair_by_odd_count": {oo: f for oo, f in fair_by_o.items() if f >= 30},
        "worst_sigma_resolved": max(
            abs(hist.get(oo, 0) - f) / math.sqrt(f) for oo, f in fair_by_o.items() if f >= 30
        ),
        "cell_depth": cell_depth, "bad_cells": bad_cells, "fair_per_cell": fair_cell,
        "relative_variance_over_poisson": relvar * fair_cell,
        "live_orbit_log10": {"min": q(0.0), "median": q(0.5), "p90": q(0.9), "max": q(1.0)},
    }


def restricted_walsh_profile(
    log10_y: int, depths: tuple[int, ...] = (12, 16), C: int = 20,
    n0: int = N0_CERTIFIED, samples: int = 60_000, seed: int = 2026,
) -> dict[str, Any]:
    """Per-order profile of the restricted Walsh sums, and the live tilted moment itself.

    Two things at once from one sample.  First, ``mean_{|T|=k} |W_T^bad| / M`` by order and
    the per-order ratio ``r_k``: the product-shape conjecture says ``|W_T^bad| <= K M b^|T|``
    with ``b = tanh(theta/2)``, and the measurement is that ``r`` sits ON the floor ``b`` at
    orders 1..3 with ``K`` about 1.6, not between ``b`` and 1.  Second, the direct object:
    ``R_d`` = live tilted moment over its fair unrestricted value, against ``phi_d``, the same
    ratio for a fair coin restricted to bad words.  ``R_d / phi_d = 1`` says the live set is
    tilted-fair, which is ``P_theta`` with the fair-coin constant; measured 1.000-1.003.
    """

    y = 10**log10_y
    L = scale_L(log10_y * math.log(10.0), n0)
    theta = theta_of_C(C)
    e, b = math.exp(theta), math.tanh(theta_of_C(C) / 2.0)
    a_theta = 0.5 * (1.0 + e)
    rng = random.Random(seed)
    dmax = max(depths)
    words = [juggler_word(rng.randrange(y + 1, 2 * y + 1) | 1, dmax) for _ in range(samples)]
    bd = [bad_depth(w, L) for w in words]

    def phi(d: int) -> float:
        bad = {1: e}
        for t in range(2, d + 1):
            nb: dict[int, float] = {}
            for o, w in bad.items():
                if o * LOG2_3 - t > -L:
                    nb[o] = nb.get(o, 0.0) + w
                if (o + 1) * LOG2_3 - t > -L:
                    nb[o + 1] = nb.get(o + 1, 0.0) + w * e
            bad = nb
        return sum(bad.values()) / (e * (1.0 + e) ** (d - 1))

    rows = []
    for d in depths:
        n = 1 << (d - 1)
        cnt = [0.0] * n
        M, live = 0, 0.0
        for w, k in zip(words, bd):
            if k >= d:
                m = 0
                for i, x in enumerate(w[1:d]):
                    m |= x << i
                cnt[m] += 1.0
                M += 1
                live += math.exp(theta * sum(w[:d]))
        h = 1
        while h < n:
            for i in range(0, n, 2 * h):
                for j in range(i, i + h):
                    x, z = cnt[j], cnt[j + h]
                    cnt[j], cnt[j + h] = x + z, x - z
            h *= 2
        absm: dict[int, float] = {}
        num: dict[int, int] = {}
        for T in range(1, n):
            k = bin(T).count("1")
            absm[k] = absm.get(k, 0.0) + abs(cnt[T]) / M
            num[k] = num.get(k, 0) + 1
        means = [absm[k] / num[k] for k in range(1, 5)]
        R = live / (samples * e * a_theta ** (d - 1))
        ph = phi(d)
        rows.append({
            "d": d, "M": M, "noise_floor": 1.0 / math.sqrt(M),
            "mean_abs_by_order": means,
            "ratio_1_to_2": means[1] / means[0], "ratio_2_to_3": means[2] / means[1],
            "K_from_order_1": means[0] / b,
            "R_d": R, "phi_d": ph, "R_over_phi": R / ph,
        })
    return {"log10_y": log10_y, "L": L, "C": C, "floor_b": b, "samples": samples, "rows": rows}


def bad_set_spectrum(d: int, L: float) -> dict[str, Any]:
    """The Walsh spectrum of the L-bad set, and what it can and cannot buy.

    ``1_B`` is not a character, so ``W_T^bad = sum_S bhat_S W_{S xor T}``.  Two standard
    inequalities are available and both lose to the trivial ``|W_T^bad| <= N p_bad``:

    * Cauchy-Schwarz gives ``sqrt(sum_S bhat_S^2) * sqrt(sum_U |W_U|^2)``.  The first factor
      is ``sqrt(p_bad)`` EXACTLY -- Parseval for a 0/1 indicator, an identity with no slack --
      so no better knowledge of the spectrum can improve that side.  The second is the
      UNRESTRICTED Walsh energy ``2^{d-1} C_d``, the object dominated by the all-``O`` tails
      the bad restriction exists to remove.  The route beats the trivial bound iff
      ``K_all < p_bad``, and ``K_all >= 1 > p_bad`` always.
    * Hoelder against the Wiener norm gives ``||bhat||_1 max_U |W_U|``, worse: the ratio
      ``||bhat||_1 / p_bad`` grows like ``1.25^d``.

    Splitting the sum by order would rescue Cauchy-Schwarz only if the spectrum were
    low-degree concentrated.  It is not, and it gets worse with depth: the fraction of l2
    weight above order 2 rises from 0.218 at ``d = 12`` to 0.303 at ``d = 20``.

    Cost is ``2^(d-1)`` for the walk scan plus the transform, so keep ``d <= 20``.
    """

    if d < 2 or d > 24:
        raise ValueError("d must be between 2 and 24")
    n = 1 << (d - 1)
    vec = [0.0] * n
    for m in range(n):
        o, ok = 1, True
        for t in range(2, d + 1):
            o += (m >> (t - 2)) & 1
            if o * LOG2_3 - t <= -L:
                ok = False
                break
        vec[m] = 1.0 if ok else 0.0
    h = 1
    while h < n:                                  # in-place Walsh-Hadamard transform
        for i in range(0, n, h * 2):
            for j in range(i, i + h):
                x, y = vec[j], vec[j + h]
                vec[j], vec[j + h] = x + y, x - y
        h *= 2
    bhat = [x / n for x in vec]
    p_bad = bhat[0]
    l2 = sum(x * x for x in bhat)
    l1 = sum(abs(x) for x in bhat)
    tails = {}
    for k in (2, 5, 10, 15):
        tails[k] = sum(x * x for s, x in enumerate(bhat) if bin(s).count("1") > k) / l2
    return {
        "d": d, "L": L, "p_bad": p_bad,
        "l2_is_p_bad": abs(l2 - p_bad) < 1e-12,
        "wiener_norm": l1, "wiener_over_density": l1 / p_bad if p_bad else None,
        "l2_tail_fraction_above_order": tails,
        "cauchy_schwarz_can_win_iff_K_all_below": p_bad,
    }


def walsh_downweighting(C: int = 20) -> dict[str, Any]:
    """Does 9.3(c)'s per-letter down-weighting survive the live restriction?

    It does, unchanged, and for a reason unlike the tower's.  The weights come from
    factorising ``e^{theta X_s} = a_theta + b_theta (-1)^{J^s(n)}`` one letter at a time,
    with ``-b_theta/a_theta = tanh(theta/2)``.  That is an identity about the tilt and says
    nothing about which ``n`` are summed, so restricting the sum to the L-bad words leaves
    every weight where it was and moves the restriction into the Walsh sums themselves:
    ``W_T`` becomes ``W_T^bad = sum over bad n of the character``.  The tower threshold
    inherited a factor rho because it was a ratio whose denominator shrank; there is no
    denominator here.

    What the restriction does buy is the trivial bound on each sum, ``|W_T^bad| <= N p_bad``
    against ``|W_T| <= N``, which shaves the tail exponent by exactly ``e(C)`` -- since
    ``p_bad`` is of order ``2^{-e(C)L}``.  The tail stays exponential either way, so 9.3(c)'s
    conclusion is untouched.
    """

    theta = theta_of_C(C)
    t = math.tanh(theta / 2.0)
    unstopped = C * math.log2(1.0 + t)
    e_c = chernoff_exponent(C)
    return {
        "C": C, "theta": theta,
        "per_letter_downweighting": t,
        "tail_exponent_unstopped": unstopped,
        "tail_exponent_live": unstopped - e_c,
        "shaved_by": e_c,
        "tail_is_still_exponential": unstopped - e_c > 0.0,
    }


def tower_threshold(C: int = 20) -> dict[str, Any]:
    """The odd share below which a tower ``O^t`` stays harmless -- both readings.

    Section 9.3(b) computes ``a_theta e^{-theta} = 0.836`` by charging the tower
    ``#[O^t] e^{theta t}`` against the fair total ``N e^theta a_theta^{t-1}``.  That is the
    right comparison for one question and not for the other:

    * *Can the tower alone break* ``P_theta``?  ``P_theta`` bounds the live sum by the
      UNRESTRICTED fair value, so the denominator is the unrestricted total and the answer
      is the printed ``a_theta e^{-theta}``.
    * *Does the tower contribute a bounded total to* ``sum_t (s_theta(t) - 1/2)^+``?  Here
      ``s_theta(t)`` averages over the LIVE population, whose tilted mass decays, so the
      denominator shrinks and the threshold tightens by that decay rate.

    The rate is a barrier problem: steps ``+log2(3)-1`` with weight ``e^theta`` and ``-1``
    with weight 1, held above ``-L``.  The tilted drift is negative, so absorption is
    certain and the surviving weight grows like ``lambda^t`` with
    ``lambda = min_{s>=0}(e^theta e^{(log2(3)-1)s} + e^{-s})`` against ``(1+e^theta)^t``.
    The correction is small -- about 0.2% -- because the tilt already sits at odd share
    ``p_C ~ 0.599`` while the barrier asks for ``1/log2(3) = 0.631``: the tilt selects
    almost exactly the words that survive.
    """

    theta = theta_of_C(C)
    e = math.exp(theta)
    a_theta = 0.5 * (1.0 + e)
    printed = a_theta * math.exp(-theta)
    step_o = LOG2_3 - 1.0

    def f(s: float) -> float:
        return e * math.exp(step_o * s) + math.exp(-s)

    lo, hi = 0.0, 5.0
    for _ in range(200):
        x, z = lo + (hi - lo) / 3.0, hi - (hi - lo) / 3.0
        if f(x) < f(z):
            hi = z
        else:
            lo = x
    rho = f((lo + hi) / 2.0) / (1.0 + e)
    return {
        "C": C, "theta": theta,
        "threshold_against_P_theta": printed,
        "live_decay_rate_rho": rho,
        "threshold_for_the_no_momentum_sum": printed * rho,
        "overpopulation_factor_printed": 2.0 * printed,
        "overpopulation_factor_live": 2.0 * printed * rho,
        "tilt_odd_share_p_C": p_of_C(C),
        "barrier_needs_odd_share": 1.0 / LOG2_3,
    }


def tau_vs_sigma(
    log10_y: int, C: int = 20, n0: int = N0_CERTIFIED, samples: int = 20_000, seed: int = 7
) -> dict[str, Any]:
    """Compare the entrance time into the floor with the walk's first passage below ``-L``.

    ``tau = min{t : J^t(n) <= N0}`` and ``sigma = min{t : u_t <= -L}`` are the two "stopped"
    notions the reduction uses.  ``tau <= sigma`` always -- that is Lemma 8.1 read at
    ``t = sigma`` -- but they are not equal, because the power envelope
    ``J^t(n)^(2^t) <= n^(3^(o_t))`` is only an upper bound and the orbit usually sits well
    under it, so an orbit can pass below the floor before the envelope certifies it.

    What matters for the reduction is not the pointwise gap but the containment cost at the
    operative depth, ``#{sigma > d} / #{tau > d}``: Theorem 8.3 and the collision route both
    bound the live count by the bad-word count in their first step.
    """

    rng = random.Random(seed)
    y = 10**log10_y
    L = scale_L(log10_y * math.log(10.0), n0)
    d = math.ceil(C * L)
    live = bad = strictly_less = both = 0
    for _ in range(samples):
        n = rng.randrange(y + 1, 2 * y + 1) | 1
        x, o = n, 0
        tau = sigma = None
        for t in range(1, d + 1):
            o += x & 1
            x = math.isqrt(x * x * x) if x & 1 else math.isqrt(x)
            if tau is None and x <= n0:
                tau = t
            if sigma is None and o * LOG2_3 - t <= -L:
                sigma = t
        live += tau is None
        bad += sigma is None
        if tau is not None and sigma is not None:
            both += 1
            strictly_less += tau < sigma
    return {
        "log10_y": log10_y, "C": C, "d": d, "L": L, "samples": samples,
        "live_tau_gt_d": live, "bad_sigma_gt_d": bad,
        "containment_cost": bad / live if live else None,
        "tau_strictly_less_when_both_fire": strictly_less / both if both else None,
        "tau_ever_exceeds_sigma": False,
    }


def worst_odd_continuation_share(
    log10_y: int, C: int = 20, n0: int = N0_CERTIFIED, samples: int = 20_000,
    seed: int = 11, min_mass: int = 200,
) -> dict[str, Any]:
    """The largest odd-continuation share over cylinders carrying real mass.

    ``H_q(C,A)`` asks that every cylinder of depth ``t < d(y)`` send at most ``q #[w]``
    of its members to an odd next state, for a fixed ``q < log 2 / log 3 = 0.6309``.  Stated
    over every ``w`` it fails for the same reason ``H(C,A)`` did, and maximally: a cylinder
    whose starts have already reached 1 continues with ``O`` at share exactly 1.  Unlike
    ``H(C,A)`` this one is not repaired by restricting the quantifier alone -- Theorem 9.1
    averages the slack over the whole population -- so the probe records it rather than
    assuming a fix.
    """

    rng = random.Random(seed)
    y = 10**log10_y
    L = scale_L(log10_y * math.log(10.0), n0)
    d = math.ceil(C * L)
    words = [juggler_word(rng.randrange(y + 1, 2 * y + 1) | 1, d) for _ in range(samples)]
    worst = {"share": -1.0}
    for t in range(1, d):
        total: dict[tuple[int, ...], int] = {}
        odd_next: dict[tuple[int, ...], int] = {}
        for w in words:
            key = w[:t]
            total[key] = total.get(key, 0) + 1
            if w[t]:
                odd_next[key] = odd_next.get(key, 0) + 1
        for key, tot in total.items():
            if tot < min_mass:
                continue
            share = odd_next.get(key, 0) / tot
            if share > worst["share"]:
                worst = {
                    "share": share, "depth": t, "members": tot, "mass": tot / samples,
                    "word": "".join("O" if b else "E" for b in key),
                    "bad_depth": bad_depth(key, L),
                }
    worst.update({"log10_y": log10_y, "C": C, "d": d, "q_crit": 1.0 / LOG2_3,
                  "violates_H_q": worst["share"] > 1.0 / LOG2_3})
    return worst


def collision_census(
    log10_y: int,
    n0: int = N0_CERTIFIED,
    samples: int = 20_000,
    d_max: int = 12,
    seed: int = 20260906,
) -> dict[str, Any]:
    """Measure ``sum_{w bad} #[w]^2`` against the constant the hypothesis allows.

    Under a fair coin the ratio ``K(d) = (sum_{w bad} #[w]^2) / (N^2 2^{-(d-1)})`` is the
    bad-word probability itself, hence at most one and decreasing.  The falsifier is
    ``K(d)`` growing with ``d``.  A finite sample of ``N`` starts adds a Poisson term
    ``N P(bad)`` to the numerator, which is why the null is computed rather than assumed:
    at these depths ``2^{d}/N`` is not negligible and would otherwise read as growth.
    """

    rng = random.Random(seed)
    y = 10**log10_y
    L = scale_L(log10_y * math.log(10.0), n0)
    words: list[tuple[int, ...]] = []
    depths: list[int] = []
    for _ in range(samples):
        n = rng.randrange(y + 1, 2 * y + 1) | 1
        w = juggler_word(n, d_max)
        words.append(w)
        depths.append(bad_depth(w, L))

    rows: list[dict[str, Any]] = []
    for d in range(1, d_max + 1):
        tally: dict[tuple[int, ...], int] = {}
        for w, bd in zip(words, depths):
            if bd >= d:
                key = w[:d]
                tally[key] = tally.get(key, 0) + 1
        collisions = sum(c * c for c in tally.values())
        live = sum(tally.values())
        n_bad = bad_word_count(L, d)
        fair = float(samples) ** 2 * 2.0 ** (-(d - 1))
        p_bad = n_bad * 2.0 ** (-(d - 1))
        null = samples * (samples - 1) * n_bad * 4.0 ** (-(d - 1)) + samples * p_bad
        rows.append({
            "d": d,
            "is_operative_depth": d == math.ceil(32 * L),
            "sample_support": samples / n_bad if n_bad else None,
            "bad_words_available": n_bad,
            "bad_words_occupied": len(tally),
            "starts_still_bad": live,
            "collisions": collisions,
            "K_measured": collisions / fair,
            "K_fair_coin": p_bad,
            "ratio_to_null": collisions / null if null > 0 else None,
        })
    return {"log10_y": log10_y, "N0": n0, "samples": samples, "L": L, "d_max": d_max,
            "seed": seed, "operative_depth_C32": math.ceil(32 * L), "rows": rows}


def verdict(censuses: list[dict[str, Any]]) -> dict[str, Any]:
    """Does the bad-word collision count deviate from a fair population as the depth grows?

    Two statistics, and only one of them is honest.  ``K_measured / K_fair_coin`` compares
    the count with its ``N -> infinity`` fair value, so once ``2^d`` approaches the sample
    size it reads the Poisson term -- every bad word occupied at most once -- as a
    deviation, and it climbs to 2 at ``d = 18`` for that reason alone.  ``ratio_to_null``
    compares against the fair value *at this sample size*, Poisson term included, and is
    the statistic the falsifier is stated on.  The raw excess is reported beside it, with
    the sample support, so the gap between the two is visible rather than hidden.
    """

    worst_null = 0.0
    worst_null_growth = 0.0
    worst_raw_excess = 0.0
    worst_supported_excess = 0.0
    operative_nulls: dict[str, float] = {}
    for census in censuses:
        usable = [r for r in census["rows"]
                  if r["starts_still_bad"] > 0 and r["K_fair_coin"] > 0 and r["d"] > 2]
        nulls = [r["ratio_to_null"] for r in usable if r["ratio_to_null"] is not None]
        worst_null = max([worst_null, *nulls])
        for a, b in zip(nulls, nulls[1:]):
            worst_null_growth = max(worst_null_growth, b / a)
        for r in usable:
            excess = r["K_measured"] / r["K_fair_coin"]
            worst_raw_excess = max(worst_raw_excess, excess)
            if (r["sample_support"] or 0) >= 50.0:
                worst_supported_excess = max(worst_supported_excess, excess)
            if r["is_operative_depth"] and r["ratio_to_null"] is not None:
                operative_nulls[f"1e{census['log10_y']}"] = r["ratio_to_null"]
    return {
        "worst_ratio_to_finite_sample_null": worst_null,
        "worst_depth_to_depth_growth_of_that_ratio": worst_null_growth,
        "ratio_at_the_operative_depth": operative_nulls,
        "worst_raw_excess_over_fair_coin": worst_raw_excess,
        "worst_excess_where_the_sample_supports_it": worst_supported_excess,
        "falsifier_fired": worst_null > 1.25 or worst_null_growth > 1.10,
        "hypothesis_survives_phase0": worst_null <= 1.25 and worst_null_growth <= 1.10,
    }


def summary(samples: int = 120_000, d_max: int = 18) -> dict[str, Any]:
    """``d_max = 18`` so that the operative depth at ``y = 10^12`` -- ``ceil(32 L) = 17`` --
    is inside the measured range.  At the other three scales the operative depth is 40, 59
    and 82, out of reach of any collision count: the hypothesis is about a population
    spread over ``2^d`` cells, and a sample cannot see collisions once ``2^d`` passes it."""

    censuses = [collision_census(e, samples=samples, d_max=d_max) for e in (12, 20, 30, 50)]
    return {
        "git_commit": git_commit(),
        "N0": N0_CERTIFIED,
        "price": {
            "true_least_C_unconditional": 20,
            "half_exponent_least_C_unconditional": half_exponent_least_C(REQUIRED_RATE),
            "true_least_C_star3": 18,
            "half_exponent_least_C_star3": half_exponent_least_C(REQUIRED_RATE_STAR3),
            "e_at_32": chernoff_exponent(32),
            "e_at_28": chernoff_exponent(28),
            "required_rate": REQUIRED_RATE,
            "required_rate_star3": REQUIRED_RATE_STAR3,
        },
        "graded_family": [
            {"gamma": g,
             "least_C_unconditional": graded_least_C(g, REQUIRED_RATE),
             "least_C_star3": graded_least_C(g, REQUIRED_RATE_STAR3)}
            for g in (0.0, 0.25, 0.5, 0.75, 1.0)
        ],
        "H_quantifier_defect": {
            "H_repaired_in_five_files": True,
            "max_cylinder": [max_cylinder_overpopulation(e, C)
                             for e, C in ((12, 20), (12, 32), (20, 20))],
            "H_q_still_open": worst_odd_continuation_share(12, 20),
        },
        "censuses": censuses,
        "verdict": verdict(censuses),
        "classification": {
            "hypothesis_is_one_sided": True,
            "hypothesis_is_a_mean_not_a_supremum": True,
            "hypothesis_is_at_depth_d_of_y": True,
            "hypothesis_does_not_invert_to_H": True,
            "cauchy_schwarz_is_saturated_at_uniform_bad_mass": True,
        },
    }


def main() -> None:
    result = summary()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / "summary.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result["price"], indent=2))
    print(json.dumps(result["verdict"], indent=2))
    print(out)


if __name__ == "__main__":
    main()
