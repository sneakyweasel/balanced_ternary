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
    REQUIRED_RATE,
    REQUIRED_RATE_STAR3,
    chernoff_exponent,
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
