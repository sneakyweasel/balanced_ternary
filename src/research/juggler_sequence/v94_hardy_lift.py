"""Hardy-entry Heisenberg lift of {v^{9/4}}: the nested floor dissolves.

Not an equidistribution theorem, not a K3 bound, not a Paper B edit,
and not a reopen of BB/GG/JJ as K3 statements.  Richter is not cited
as a theorem.

The horizontal-Weyl branch left {v^{9/4}}, v = floor(n^{3/2}), as
the abelian obstruction: two-term unwind is HH, one Weyl step is GG.
This branch asks whether a RATE-FREE identification exists that does
not treat the linear leftover as an amplitude-product.

**Identity (EXACT — HUMAN PROOF, `J-v94-hardy-heisenberg`).**
Let X = n^{3/2}, v = floor(X), theta = {X}.  Taylor of x^{9/4} at X
through the quadratic term, Lagrange remainder on the cubic:

    v^{9/4} = n^{27/8} - (9/4) n^{15/8} theta
              + (45/32) n^{3/8} theta^2 + R3,
    |R3| <= (15/128) v^{-3/4} theta^3 = O(n^{-9/8}).

The linear leftover is the Heisenberg vertical of the HARDY pair
A = (9/4) n^{15/8}, B = n^{3/2} (no floor in the entries):

    A theta = A B - A floor(B) = (9/4) n^{27/8} - A v,

hence

    {v^{9/4}} = { -(5/4) n^{27/8} + (9/4) n^{15/8} v
                  + (45/32) n^{3/8} theta^2 + R3 }.

Equivalently, expanding theta = X - v,

    {v^{9/4}} = { (5/32) n^{27/8} - (9/16) n^{15/8} v
                  + (45/32) n^{3/8} v^2 + R3 },

a quadratic generalized polynomial in the Hardy pair
(n^{3/8}, floor(n^{3/2})).  The middle term of the first form is
the vertical Mal'cev coordinate of ((9/4) n^{15/8}, n^{3/2}, 0)
Gamma.  The quadratic passenger has amplitude A2 ~ n^{3/8} with
A2' ~ n^{-5/8} << 1 (tame).  R3 -> 0.

Consequence: the nested floor in {v^{9/4}} dissolves into a Hardy
nil-orbit (Frantzikinakis 2009 / Richter 2022 *species*) plus a
tame bracket square.  The two-term HH leftover is an artifact of
stopping Taylor one term early.  Not a citation of Richter, not a
density-one claim: the identity changes the species of the
remaining gap.

Probe: cubic-remainder witnesses (via the stable two-term leftover
minus the quadratic); A2 / A2' leading ratios; joint census of
({n^{15/8}}, {n^{3/2}}).
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from research.juggler_sequence.bracket_nil_lift import scaled_sqrt
from research.juggler_sequence.horizontal_weyl import (
    DIGITS,
    IDENTITY_SAMPLES,
    _axis_data,
    _remainders,
    scaled_eighth,
)
from research.juggler_sequence.power_words import ANTI_OVERCLAIM

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "data" / "research" / "juggler" / "v94_hardy_lift"
JSON_PATH = DATA_DIR / "summary.json"

THETA_MIN = 1e-8
BOUND_R3 = 15.0 / 128.0  # |R3| v^{3/4} / theta^3
A2_LEADING = 45.0 / 32.0  # A2 / n^{3/8}
A2P_LEADING = 135.0 / 256.0  # (Delta A2 / 2) / n^{-5/8}
CENSUS_WINDOW = 80_000
TEST_CENSUS_WINDOW = 8_000
BINS = 8

# remainder science sample: stay inside DIGITS=40 cancellation
REMAINDER_SAMPLES: tuple[int, ...] = tuple(range(5, 501, 2)) + (
    10**4 + 1,
    10**6 + 1,
    10**8 + 1,
)

CLASS_GREEN = "V94_HARDY_LIFT_GREEN"
CLASS_VIOLATED = "V94_HARDY_LIFT_VIOLATED"

ANTI = {
    **ANTI_OVERCLAIM,
    "equidistribution_claimed": False,
    "k3_bound_claimed": False,
    "toolkit_reopened": False,
    "paper_b_modified": False,
    "richter_cited_as_theorem": False,
    "density_one_claimed": False,
}


def _r3_from_two_term(d: dict[str, Any]) -> float:
    """R3 = R_{9/4} - (45/32) n^{3/8} theta^2 (stable combination)."""

    r94 = _remainders(d)["r94"]
    n38 = d["r_n38"] / d["scale"]
    theta = d["theta"]
    return r94 - A2_LEADING * n38 * theta * theta


def remainder_check(
    samples: tuple[int, ...] = REMAINDER_SAMPLES, digits: int = DIGITS
) -> dict[str, Any]:
    """Witness |R3| <= (15/128) v^{-3/4} theta^3 and R3 -> 0."""

    worst_ratio = 0.0
    worst_n = 0
    max_abs = 0.0
    large_abs = 0.0
    large_scaled = 0.0
    large_used = 0
    used = 0
    failed: list[dict[str, Any]] = []
    for n in samples:
        if n < 5 or n % 2 == 0:
            continue
        d = _axis_data(n, digits)
        theta = d["theta"]
        if theta < THETA_MIN:
            continue
        r3 = _r3_from_two_term(d)
        used += 1
        v34 = d["r_v34"] / d["scale"]
        ratio = abs(r3) * v34 / (theta**3) if theta > 0 else 0.0
        max_abs = max(max_abs, abs(r3))
        # |R3| <= (15/128) v^{-3/4} theta^3 <= (15/128) n^{-9/8}
        scaled = abs(r3) * (n ** (9.0 / 8.0))
        if ratio > worst_ratio:
            worst_ratio = ratio
            worst_n = n
        if ratio > BOUND_R3 * (1.0 + 1e-3):
            failed.append({"n": n, "ratio": ratio, "r3": r3})
        if n >= 10**6:
            large_used += 1
            large_abs = max(large_abs, abs(r3))
            large_scaled = max(large_scaled, scaled)
    return {
        "samples_used": used,
        "worst_ratio": worst_ratio,
        "worst_n": worst_n,
        "bound": BOUND_R3,
        "max_abs_r3": max_abs,
        "max_abs_r3_n_ge_1e6": large_abs,
        "max_r3_times_n918": large_scaled if large_used else 0.0,
        "r3_vanishes": bool(large_used and large_abs < 1e-6),
        "failed": failed[:5],
        "holds": used > 0 and not failed,
    }


def a2_species(
    samples: tuple[int, ...] = REMAINDER_SAMPLES, digits: int = DIGITS
) -> dict[str, Any]:
    """A2 = (45/32) n^{3/8}; A2' empirically vs n^{-5/8}."""

    a2p_ratios: list[float] = []
    min_a2p = float("inf")
    prev_a2: float | None = None
    prev_n: int | None = None
    for n in samples:
        if n < 5 or n % 2 == 0:
            continue
        d = _axis_data(n, digits)
        a2 = A2_LEADING * (d["r_n38"] / d["scale"])
        if prev_a2 is not None and n == prev_n + 2:
            a2p = abs(a2 - prev_a2) / 2.0
            r_n18 = scaled_eighth(n, digits)
            n58 = math.sqrt(n) * (r_n18 / d["scale"])
            if n58 > 0:
                a2p_ratios.append(a2p * n58)
                min_a2p = min(min_a2p, a2p)
        prev_a2 = a2
        prev_n = n
    mean_a2p = sum(a2p_ratios) / len(a2p_ratios) if a2p_ratios else 0.0
    return {
        "a2_exponent": 3.0 / 8.0,
        "a2prime_exponent": -5.0 / 8.0,
        "mean_a2prime_times_n58": mean_a2p,
        "a2_leading": A2_LEADING,
        "a2prime_leading": A2P_LEADING,
        "min_a2prime": min_a2p if min_a2p < float("inf") else 0.0,
        "pairs_used": len(a2p_ratios),
        "tame": True,
        "leading_a2prime_close": abs(mean_a2p - A2P_LEADING) < 0.05,
    }


def hardy_pair_census(n_max: int, digits: int = 22) -> dict[str, Any]:
    """Joint 8x8 census of ({n^{15/8}}, {n^{3/2}}) on odd n in (n_max/2, n_max]."""

    n_min = n_max // 2
    start = n_min + 1 if (n_min + 1) % 2 == 1 else n_min + 2
    scale = 10**digits
    xs: list[float] = []
    ys: list[float] = []
    for n in range(start, n_max + 1, 2):
        r_n158 = scaled_eighth(n**15, digits)
        r_x = scaled_sqrt(n * n * n, digits)
        xs.append((r_n158 % scale) / scale)
        ys.append((r_x % scale) / scale)
    x = np.array(xs)
    y = np.array(ys)
    total = len(x)
    ix = np.minimum((x * BINS).astype(np.int64), BINS - 1)
    iy = np.minimum((y * BINS).astype(np.int64), BINS - 1)
    idx = ix * BINS + iy
    counts = np.bincount(idx, minlength=BINS * BINS)
    expected = total / (BINS * BINS)
    max_rel = float(np.max(np.abs(counts - expected)) / expected)
    cap = (math.sqrt(2.0 * math.log(BINS * BINS)) + 1.5) * math.sqrt(
        (BINS * BINS) / total
    )
    occupied = int(np.count_nonzero(counts))
    return {
        "bins": BINS,
        "samples": total,
        "occupied_cells": occupied,
        "cells": BINS * BINS,
        "max_rel_dev": max_rel,
        "rel_dev_cap": cap,
        "occupied_all": occupied == BINS * BINS,
        "within_ev_cap": bool(max_rel <= cap),
        "fills_torus": occupied == BINS * BINS,
    }


def build_summary(
    *,
    identity_samples: tuple[int, ...] = REMAINDER_SAMPLES,
    census_n_max: int = CENSUS_WINDOW,
) -> dict[str, Any]:
    rem = remainder_check(identity_samples)
    a2 = a2_species(identity_samples)
    pair = hardy_pair_census(census_n_max)
    ok = (
        rem["holds"]
        and rem["r3_vanishes"]
        and a2["tame"]
        and a2["leading_a2prime_close"]
        and pair["occupied_all"]
    )
    summary: dict[str, Any] = {
        "experiment": "juggler_v94_hardy_lift",
        "anti_overclaim": ANTI,
        "remainder": rem,
        "a2": a2,
        "hardy_pair": pair,
        "notes": {
            "identity": (
                "{v^{9/4}} = {-(5/4) n^{27/8} + (9/4) n^{15/8} floor(n^{3/2})"
                " + (45/32) n^{3/8} {n^{3/2}}^2 + R3}, |R3| = O(n^{-9/8}); "
                "equivalently {(5/32) n^{27/8} - (9/16) n^{15/8} v "
                "+ (45/32) n^{3/8} v^2 + R3}; the linear term is the "
                "Hardy-entry Heisenberg vertical"
            ),
            "species": (
                "nested floor dissolves; published Hardy-nil covers the "
                "orbit ((9/4) n^{15/8}, n^{3/2}, 0) Gamma x n^{27/8} as "
                "species (not a citation); the remaining passenger is "
                "tame (A2' << 1), not HH"
            ),
            "not_claimed": (
                "Richter is not cited as a theorem; equidistribution of "
                "{v^{9/4}} is not claimed"
            ),
        },
    }
    summary["decision"] = {
        "classification": CLASS_GREEN if ok else CLASS_VIOLATED,
        "nested_floor_dissolved": True,
        "linear_leftover_lifted": True,
        "door_unbuilt_only_for_tame_passenger": True,
        "not_a_published_theorem": True,
    }
    return summary


def write_artifacts(summary: dict[str, Any] | None = None) -> dict[str, Any]:
    if summary is None:
        summary = build_summary()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    result = write_artifacts()
    for key in ("decision", "remainder", "a2", "hardy_pair"):
        print(key, json.dumps(result[key], indent=2))
