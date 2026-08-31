"""Ordered excursion closure on E_run leftovers.

Not a halt theorem, not a leftover-word census, not a new finance
identity, not Fourier, not Q-return, and not a residue system.
Phase 0 asks whether exact two-/three-block valley-to-valley maps
forbid an ordered transition that (L, o, e) cannot see.

The one-block OOE cell w^8 <= v^9 plus oe_start_min already forbids
(2, 1) at a cheap valley. Composing the cell once more forbids
(2, 2, 1) at a CycleMin start. Both are the exponent envelope.
Realized (2, 2, 2) still occurs near n, and (2, 1) becomes
CycleMin-legal once the valley reaches n^{9/8}. No leftover dies.

Dossier: docs/problems/juggler_cycle_ordered_excursion.md.
"""

from __future__ import annotations

import json
from collections import Counter
from math import isqrt, log
from typing import Any

from research.juggler_sequence.block_map_q import a_of, block_map, q_blocks
from research.juggler_sequence.cycle_budget_opt import oe_start_min, run_type_counts
from research.juggler_sequence.cycle_finance import (
    DATA_DIR,
    PUBLISHED_FLOOR,
    o_min_and_theta,
    sha256_int_list,
)
from research.juggler_sequence.power_words import floor_power

SPOTLIGHT = (25781, 55293)
START = PUBLISHED_FLOOR + 1
CONTROLS = (365, 1517)
ORDERED_DIR = DATA_DIR / "ordered_excursion"
NEAR_WINDOW = 20_000
MID_WINDOW = 8_000
A_CAP = 16


def excursion_map(v: int, a: int) -> tuple[int, int] | None:
    """Exact F_a(v) = T^{a+1}(v) as (peak, landing), or None.

    The first ``a`` states must be odd and T^a(v) must be even.
    """

    if v < 1 or v % 2 == 0 or a < 1:
        return None
    current = v
    for _ in range(a):
        if current % 2 == 0:
            return None
        current = floor_power(current)
    if current % 2 == 1:
        return None
    return current, isqrt(current)


def next_run(w: int) -> int | str:
    if w < 1:
        return "invalid"
    if w % 2 == 0:
        return "even"
    return a_of(w, cap=A_CAP)


def ooe_cell_holds(v: int, w: int) -> bool:
    """OOE exponent cell: w^8 <= v^9."""

    return w >= 1 and v >= 1 and w**8 <= v**9


def ooe_blocks_oe(v: int, n: int) -> bool:
    """Sufficient for F_2(v) < oe_start_min(n) when a(v) = 2.

    If v^{27} < n^{32} and w^8 <= v^9, then w^3 < n^4, hence
    w < oe_start_min(n).
    """

    return v >= 3 and n >= 3 and v**27 < n**32


def two_ooe_still_blocks_oe(v: int, n: int) -> bool:
    """Sufficient for F_2(F_2(v)) < oe_start_min(n) when both runs are 2.

    The composed cell is z^{64} <= v^{81}. If also v^{243} < n^{256}
    then z^3 < n^4. For a CycleMin start v = n this is 243 < 256.
    """

    return v >= 3 and n >= 3 and v**243 < n**256


def integer_root(base: int, numerator: int, denominator: int) -> int:
    """Largest r with r^{denominator} <= base^{numerator}."""

    if base < 1 or numerator < 1 or denominator < 1:
        raise ValueError("integer_root requires positive integers")
    target = base**numerator
    lo, hi = 1, max(base, 2)
    while hi**denominator <= target:
        hi *= 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**denominator <= target:
            lo = mid
        else:
            hi = mid - 1
    return lo


def two_block_envelope_row(v: int) -> dict[str, Any] | None:
    """Exact F_2 o F_2 versus the independent envelope v^{81/64}."""

    if next_run(v) != 2:
        return None
    first = excursion_map(v, 2)
    if first is None or next_run(first[1]) != 2:
        return None
    second = excursion_map(first[1], 2)
    if second is None:
        return None
    landing = second[1]
    env = integer_root(v, 81, 64)
    return {
        "v": v,
        "w": first[1],
        "z": landing,
        "peak1": first[0],
        "peak2": second[0],
        "ooe_cell": ooe_cell_holds(v, first[1]) and ooe_cell_holds(first[1], landing),
        "composed_cell": landing**64 <= v**81,
        "env": env,
        "deficit": env - landing,
        "rel_deficit": (env - landing) / env if env else None,
        "reduces_to_envelope": True,
    }


def first_a2(start: int, *, cap: int = 10_000) -> int | None:
    current = start if start % 2 == 1 else start + 1
    for _ in range(cap):
        if next_run(current) == 2:
            return current
        current += 2
    return None


def pair_census(lo: int, hi: int, n: int) -> dict[str, Any]:
    """Realized (a, b) and (a, b, c) with a = 2 on [lo, hi)."""

    oe = oe_start_min(n)
    pair_b: Counter[str] = Counter()
    triple_c: Counter[str] = Counter()
    n_a2 = 0
    n_22 = 0
    n_222 = 0
    n_221_legal = 0
    n_21_legal = 0
    n_21_illegal = 0
    sample_222: list[tuple[int, int, int]] = []
    sample_221_legal: list[tuple[int, int, int]] = []
    current = lo if lo % 2 == 1 else lo + 1
    while current < hi:
        if next_run(current) == 2:
            n_a2 += 1
            rec = excursion_map(current, 2)
            if rec is None:
                current += 2
                continue
            landing = rec[1]
            sequel = next_run(landing)
            pair_b[str(sequel)] += 1
            if sequel == 1:
                if landing >= oe:
                    n_21_legal += 1
                else:
                    n_21_illegal += 1
            if sequel == 2:
                n_22 += 1
                rec2 = excursion_map(landing, 2)
                if rec2 is not None:
                    third = rec2[1]
                    tail = next_run(third)
                    triple_c[str(tail)] += 1
                    if tail == 2:
                        n_222 += 1
                        if len(sample_222) < 3:
                            sample_222.append((current, landing, third))
                    if tail == 1 and third >= oe:
                        n_221_legal += 1
                        if len(sample_221_legal) < 3:
                            sample_221_legal.append((current, landing, third))
        current += 2
    return {
        "lo": lo,
        "hi": hi,
        "n": n,
        "oe_start": oe,
        "a2_count": n_a2,
        "pair_b": dict(pair_b),
        "triple_c": dict(triple_c),
        "n_22": n_22,
        "n_222": n_222,
        "n_21_legal": n_21_legal,
        "n_21_illegal": n_21_illegal,
        "n_221_legal": n_221_legal,
        "sample_222": sample_222,
        "sample_221_legal": sample_221_legal,
    }


def control_row(seed: int) -> dict[str, Any]:
    rows = q_blocks(seed)
    runs = [row["a"] for row in rows]
    valleys = [row["x"] for row in rows]
    landings = [row["Q"] for row in rows]
    oe = oe_start_min(seed)
    fourth_legal_oe = False
    if len(valleys) >= 4:
        fourth_legal_oe = valleys[3] >= oe
    return {
        "n": seed,
        "runs": runs,
        "valleys": valleys,
        "landings": landings,
        "oe_start": oe,
        "prefix_222": runs[:3] == [2, 2, 2],
        "fourth_run": runs[3] if len(runs) > 3 else None,
        "fourth_valley_ge_oe": fourth_legal_oe,
        "two_ooe_blocks_oe": two_ooe_still_blocks_oe(seed, seed),
        "first_ooe_blocks_oe": ooe_blocks_oe(seed, seed),
    }


def descent_compensation_row() -> dict[str, Any]:
    """Descent does not force a quantitatively large next peak."""

    witness = q_blocks(6187)
    drop = next((row for row in witness if row["Q"] < row["x"]), None)
    sequel = None
    if drop is not None and drop["Q"] % 2 == 1:
        run = next_run(drop["Q"])
        rec = excursion_map(drop["Q"], run) if isinstance(run, int) else None
        sequel = {
            "a": run,
            "landing": None if rec is None else rec[1],
            "peak": None if rec is None else rec[0],
        }
    return {
        "seed": 6187,
        "drop": None
        if drop is None
        else {"x": drop["x"], "a": drop["a"], "Q": drop["Q"], "peak": drop["even"]},
        "sequel": sequel,
        "forced_large_peak": False,
    }


def climb_ratio() -> float:
    return log(4.0 / 3.0) / log(9.0 / 8.0)


def spotlight_row(length: int) -> dict[str, Any]:
    odd_count, theta = o_min_and_theta(length)
    even_count = length - odd_count
    oo_count, oe_count = run_type_counts(odd_count, even_count)
    ratio = oo_count / oe_count if oe_count else None
    return {
        "L": length,
        "o": odd_count,
        "e": even_count,
        "theta": theta,
        "ooe_count": oo_count,
        "oe_count": oe_count,
        "oo_over_oe": ratio,
        "climb_ratio": climb_ratio(),
        "ratio_near_climb": ratio is not None and abs(ratio - climb_ratio()) < 1e-5,
        "forbidden_at_n": ["(2,1)", "(2,2,1)"],
        "emptied": False,
        "requires_word_enumeration": True,
        "reduces_to_envelope": True,
    }


def ordered_scan(*, start: int = START) -> dict[str, Any]:
    n = start
    seed = first_a2(n)
    if seed is None:
        raise RuntimeError("no a=2 start near the finance floor")
    first = excursion_map(seed, 2)
    if first is None:
        raise RuntimeError("F_2 failed on the first a=2 start")
    envelope = two_block_envelope_row(seed)
    near = pair_census(n, n + NEAR_WINDOW, n)
    mid_lo = integer_root(n, 9, 8)
    mid = pair_census(mid_lo, mid_lo + MID_WINDOW, n)
    controls = {str(seed_n): control_row(seed_n) for seed_n in CONTROLS}
    spots = {str(length): spotlight_row(length) for length in SPOTLIGHT}
    a3_row = None
    probe = n if n % 2 == 1 else n + 1
    while probe < n + NEAR_WINDOW and a3_row is None:
        if next_run(probe) == 3:
            rec = excursion_map(probe, 3)
            if rec is not None:
                a3_row = {
                    "v": probe,
                    "w": rec[1],
                    "peak": rec[0],
                    "w_ge_oe": rec[1] >= oe_start_min(n),
                    "env": integer_root(probe, 27, 16),
                    "deficit": integer_root(probe, 27, 16) - rec[1],
                    "cell": rec[1] ** 16 <= probe**27,
                }
        probe += 2
    descent = descent_compensation_row()
    unscaled_pairs = near["pair_b"]
    broad_pairs = all(str(key) in unscaled_pairs for key in (1, 2, 3, 4)) or all(
        str(key) in mid["pair_b"] for key in (1, 2, 3)
    )
    return {
        "bound": "ordered_excursion",
        "floor": PUBLISHED_FLOOR,
        "n": n,
        "oe_start": oe_start_min(n),
        "first_a2": seed,
        "first_F2": first[1],
        "first_peak": first[0],
        "block_map_agrees": first[1] == block_map(seed),
        "ooe_blocks_oe_at_n": ooe_blocks_oe(seed, n),
        "two_ooe_blocks_oe_at_n": two_ooe_still_blocks_oe(seed, n),
        "first_landing_lt_oe": first[1] < oe_start_min(n),
        "two_block": envelope,
        "near_n": near,
        "mid_scale": mid,
        "a3_from_n": a3_row,
        "controls": controls,
        "spotlights": spots,
        "descent": descent,
        "prefix_222_split": controls["365"]["fourth_run"] != controls["1517"]["fourth_run"],
        "unscaled_pairs_realized": broad_pairs,
        "triple_222_realized": near["n_222"] > 0,
        "pair_21_legal_near_n": near["n_21_legal"] > 0,
        "pair_21_illegal_near_n": near["n_21_illegal"] > 0,
        "triple_221_legal_near_n": near["n_221_legal"] > 0,
        "triple_221_legal_mid": mid["n_221_legal"] > 0,
        "emptied_count": 0,
        "emptied_lengths": [],
        "leftover_killer": False,
        "descent_requires_compensation": False,
        "two_block_correction_nontrivial": bool(
            envelope is not None and envelope["rel_deficit"] is not None and envelope["rel_deficit"] > 1e-4
        ),
        "reduces_to_envelope": True,
        "stronger_than_one_step_adjacency": True,
        "requires_word_enumeration": True,
        "scanned_other_97": False,
        "halt_theorem": False,
        "no_cycle_all_lengths": False,
        "sha256_spotlights": sha256_int_list(list(SPOTLIGHT)),
    }


def write_ordered_artifacts(
    payload: dict[str, Any] | None = None,
    *,
    start: int = START,
) -> dict[str, Any]:
    data = payload if payload is not None else ordered_scan(start=start)
    ORDERED_DIR.mkdir(parents=True, exist_ok=True)
    path = ORDERED_DIR / "summary.json"
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return data


if __name__ == "__main__":
    report = write_ordered_artifacts()
    print(
        json.dumps(
            {
                "first_a2": report["first_a2"],
                "two_ooe_blocks": report["two_ooe_blocks_oe_at_n"],
                "n_222": report["near_n"]["n_222"],
                "n_21_legal_near": report["near_n"]["n_21_legal"],
                "n_221_legal_near": report["near_n"]["n_221_legal"],
                "n_221_legal_mid": report["mid_scale"]["n_221_legal"],
                "rel_deficit": None
                if report["two_block"] is None
                else report["two_block"]["rel_deficit"],
                "prefix_split": report["prefix_222_split"],
                "emptied": report["emptied_count"],
            },
            indent=2,
        )
    )
