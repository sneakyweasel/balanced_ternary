"""Cyclic valley-necklace finance versus independent run-type packing.

Phase 0 only: the finance relaxation treats valleys as a path with
a free first state. A cycle is a closed necklace
v1 -> p1 -> v2 -> ... -> vm -> pm -> v1. This probe asks whether
the wrap-around edge forces a deficit that cannot be rotated away.

Not a halt theorem, not a leftover-word census, not a
branch-and-bound engine, and not a floor raise.

Dossier: docs/problems/juggler_cycle_cyclic_valley.md.
"""

from __future__ import annotations

import json
import math
from itertools import product
from typing import Any

from research.juggler_sequence.block_map_q import a_of
from research.juggler_sequence.cycle_almost_search import (
    PHASE1_L,
    circuits,
    packed_block_word,
)
from research.juggler_sequence.cycle_budget_opt import (
    budget_excludes,
    budget_rhs,
    inv_log,
    oe_start_min,
    run_type_counts,
)
from research.juggler_sequence.cycle_conditioned_closure import deficit_row
from research.juggler_sequence.cycle_finance import (
    DATA_DIR,
    EPS_CONST,
    MIN_STATE,
    PARITY_ABS_PAD,
    PARITY_REL_GUARD,
    PUBLISHED_FLOOR,
    first_odd_image,
    o_min_and_theta,
    parity_excludes,
)
from research.juggler_sequence.cycle_ordered_excursion import excursion_map
from research.juggler_sequence.cycle_prefix_feasibility import (
    ceiling_christoffel_word,
    extremal_word,
    prefix_admissible,
)
from research.juggler_sequence.cycle_valley_coupling import nine_eighths_height

CYCLIC_DIR = DATA_DIR / "cyclic_valley"
START = max(PUBLISHED_FLOOR + 1, MIN_STATE)
LOG2_98 = 2.0 * math.log(3.0) / math.log(2.0) - 3.0  # log2(9/8)
LOG2_43 = 2.0 - math.log(3.0) / math.log(2.0)  # log2(4/3)
CHEAP_LOG2 = LOG2_98
WITNESSES = (365, 1_000_057, 1_517)
SMALL_M = 5
A_MAX = 3

CLASS_CLOSED = "CYCLIC_VALLEY_CLOSED"
CLASS_GREEN = "CYCLIC_VALLEY_GREEN"
CLASS_PARK = "CYCLIC_VALLEY_PARK"


def two_type_cheap_cap(odd_count: int, even_count: int) -> int:
    """On a two-type CycleMin necklace, N_cheap(α < 9/8) ≤ N_OE.

    An OOE run from α ≥ 1 lands at ≥ 9/8, so a cheap valley cannot
    be an OOE landing. The only other two-type landing is OE. On a
    cycle the unique min is the wrap-around landing, not a free
    first valley. Hence every cheap valley is an OE landing.
    """

    _oo_count, oe_count = run_type_counts(odd_count, even_count)
    return oe_count


def two_type_cyclic_sum_terms(n: int, length: int, odd_count: int) -> float:
    """Height-consistent two-type upper bound on Σ 1/(x ln x).

    Charge N_OE valleys at the unique-visit pair (n, n+2), the
    remaining OOE starts at the 9/8 integer height, OE starts at
    oe_start_min, internals of those runs at T of the start, and
    evens at n^2. This is an envelope-scale charge: the 9/8 height
    is the laboratory integer proxy, not a floor-free lower cell.
    """

    if n < 3:
        return math.inf
    even_count = length - odd_count
    oo_count, oe_count = run_type_counts(odd_count, even_count)
    cheap = min(oo_count, two_type_cheap_cap(odd_count, even_count))
    high = max(oo_count - cheap, 0)
    high_v = nine_eighths_height(n)
    oe_v = oe_start_min(n)
    valley = inv_log(n)
    if cheap > 1:
        valley += (cheap - 1) * inv_log(n + 2)
    if high:
        valley += high * inv_log(high_v)
    climb = inv_log(first_odd_image(n)) if cheap else 0.0
    if cheap > 1:
        climb += (cheap - 1) * inv_log(first_odd_image(n + 2))
    if high:
        climb += high * inv_log(max(first_odd_image(high_v), high_v))
    high_oe = oe_count * inv_log(oe_v)
    even_term = even_count * inv_log(n * n)
    return valley + climb + high_oe + even_term


def two_type_cyclic_rhs(
    n: int,
    length: int,
    odd_count: int,
    *,
    const: float = EPS_CONST,
) -> float:
    return const * two_type_cyclic_sum_terms(n, length, odd_count)


def _excludes(theta: float, rhs: float) -> bool:
    return theta * (1.0 - PARITY_REL_GUARD) > rhs * (1.0 + PARITY_REL_GUARD) + PARITY_ABS_PAD


def run_multiplier(odd_run: int, even_run: int) -> tuple[int, int]:
    """Envelope multiplier 3^{odd} / 2^{odd+even} as (exp3, exp2)."""

    return odd_run, odd_run + even_run


def envelope_legal(exp3: int, exp2: int) -> bool:
    if exp3 < 0 or exp2 < 0:
        return False
    if exp3 <= 40 and exp2 <= 80:
        return 3**exp3 >= (1 << exp2)
    return exp3 * math.log(3.0) + 1e-15 >= exp2 * math.log(2.0)


def log2_of(exp3: int, exp2: int) -> float:
    return exp3 * math.log(3.0) / math.log(2.0) - exp2


def walk_runs(runs: list[tuple[int, int]]) -> dict[str, Any]:
    """Cyclic envelope walk on a valley necklace of run pairs."""

    exp3, exp2 = 0, 0
    valley_logs: list[float] = []
    cheap = 0
    illegal = 0
    oe_illegal = 0
    for odd_run, even_run in runs:
        log_val = log2_of(exp3, exp2)
        valley_logs.append(log_val)
        if log_val + 1e-12 < 0.0:
            illegal += 1
        if odd_run == 1 and log_val < LOG2_43 - 1e-12:
            oe_illegal += 1
        if log_val + 1e-12 >= 0.0 and log_val < CHEAP_LOG2 - 1e-12:
            cheap += 1
        d3, d2 = run_multiplier(odd_run, even_run)
        exp3 += d3
        exp2 += d2
    wrap_log = log2_of(exp3, exp2)
    wrap_legal = envelope_legal(exp3, exp2)
    all_legal = illegal == 0 and oe_illegal == 0
    return {
        "valleys": len(runs),
        "valley_logs": valley_logs,
        "cheap": cheap,
        "illegal_below_one": illegal,
        "oe_illegal": oe_illegal,
        "all_cyclemin": all_legal,
        "wrap_log2": wrap_log,
        "wrap_legal": wrap_legal,
        "wrap_is_cheap": wrap_log + 1e-12 >= 0.0 and wrap_log < CHEAP_LOG2 - 1e-12,
        "final_exp3": exp3,
        "final_exp2": exp2,
        "min_log2": min(valley_logs) if valley_logs else None,
        "max_log2": max(valley_logs) if valley_logs else None,
        "start_log2": valley_logs[0] if valley_logs else None,
        "last_log2": valley_logs[-1] if valley_logs else None,
    }


def height_finance(n: int, valley_logs: list[float], even_count: int) -> float:
    """Σ 1/(n^α α ln n) plus evens at n^2. Envelope-scale observation."""

    if n < 3 or not valley_logs:
        return 0.0
    log_n = math.log(n)
    total = 0.0
    for log2_alpha in valley_logs:
        if log2_alpha > 1000.0:
            continue
        alpha = 2.0**log2_alpha
        log_height = alpha * log_n
        if log_height > 700.0:
            continue
        height = math.exp(log_height)
        if height < 3:
            continue
        total += 1.0 / (height * alpha * log_n)
    total += even_count * inv_log(n * n)
    return EPS_CONST * total


def rotate_runs(runs: list[tuple[int, int]], shift: int) -> list[tuple[int, int]]:
    if not runs:
        return []
    cut = shift % len(runs)
    return runs[cut:] + runs[:cut]


def rotation_table(runs: list[tuple[int, int]], *, sample: int = 12) -> dict[str, Any]:
    """Cheap-count and wrap legality at equally spaced cyclic cuts."""

    if not runs:
        return {
            "count": 0,
            "legal_count": 0,
            "cheap_span": 0,
            "wrap_legal_all": True,
            "rows": [],
        }
    total = len(runs)
    step = max(1, total // sample)
    shifts = list(range(0, total, step))[:sample]
    if 0 not in shifts:
        shifts = [0] + shifts
    rows = []
    cheap_vals = []
    wrap_ok = True
    for shift in shifts:
        if runs[shift][0] < 2:
            continue
        walked = walk_runs(rotate_runs(runs, shift))
        if not walked["all_cyclemin"]:
            continue
        cheap_vals.append(walked["cheap"])
        wrap_ok = wrap_ok and walked["wrap_legal"]
        rows.append(
            {
                "shift": shift,
                "cheap": walked["cheap"],
                "illegal": walked["illegal_below_one"],
                "oe_illegal": walked["oe_illegal"],
                "wrap_log2": walked["wrap_log2"],
                "last_log2": walked["last_log2"],
                "all_cyclemin": walked["all_cyclemin"],
            }
        )
    return {
        "count": len(shifts),
        "legal_count": len(rows),
        "cheap_min": min(cheap_vals) if cheap_vals else None,
        "cheap_max": max(cheap_vals) if cheap_vals else None,
        "cheap_span": (max(cheap_vals) - min(cheap_vals)) if cheap_vals else 0,
        "wrap_legal_all": wrap_ok,
        "rows": rows,
    }


def necklace_row(name: str, word: str, n: int) -> dict[str, Any]:
    runs = circuits(word)
    walked = walk_runs(runs)
    rotations = rotation_table(runs)
    odd = word.count("O")
    length = len(word)
    packed = budget_rhs(n, length, odd)
    cyclic_bound = two_type_cyclic_rhs(n, length, odd)
    height_rhs = height_finance(n, walked["valley_logs"], length - odd)
    return {
        "name": name,
        "two_type": all(even_run == 1 and odd_run in (1, 2) for odd_run, even_run in runs),
        "circuits": len(runs),
        "prefix_admissible": prefix_admissible(word),
        "cheap": walked["cheap"],
        "cheap_cap": two_type_cheap_cap(odd, length - odd),
        "cheap_at_or_below_cap": walked["cheap"] <= two_type_cheap_cap(odd, length - odd),
        "illegal_below_one": walked["illegal_below_one"],
        "oe_illegal": walked["oe_illegal"],
        "all_cyclemin": walked["all_cyclemin"],
        "wrap_log2": walked["wrap_log2"],
        "wrap_legal": walked["wrap_legal"],
        "rotation_legal_count": rotations["legal_count"],
        "rotation_cheap_span": rotations["cheap_span"],
        "rotation_cheap_max": rotations["cheap_max"],
        "rotation_wrap_legal_all": rotations["wrap_legal_all"],
        "height_rhs": height_rhs,
        "cyclic_bound_rhs": cyclic_bound,
        "packed_rhs": packed,
        "height_below_packed": height_rhs + PARITY_ABS_PAD < packed,
    }


def motif_runs(odd_run: int, even_run: int, copies: int) -> list[tuple[int, int]]:
    return [(odd_run, even_run)] * copies


def motif_row(name: str, odd_run: int, even_run: int, odd_budget: int, even_budget: int, n: int) -> dict[str, Any]:
    copies = min(odd_budget // odd_run, even_budget // even_run)
    runs = motif_runs(odd_run, even_run, copies)
    leftover_o = odd_budget - copies * odd_run
    leftover_e = even_budget - copies * even_run
    walked = walk_runs(runs)
    length = copies * (odd_run + even_run)
    odd = copies * odd_run
    height_rhs = height_finance(n, walked["valley_logs"], copies * even_run)
    return {
        "name": name,
        "k": odd_run,
        "ell": even_run,
        "copies": copies,
        "leftover_o": leftover_o,
        "leftover_e": leftover_e,
        "cheap": walked["cheap"],
        "oe_illegal": walked["oe_illegal"],
        "all_cyclemin": walked["all_cyclemin"],
        "wrap_log2": walked["wrap_log2"],
        "wrap_legal": walked["wrap_legal"],
        "height_rhs": height_rhs,
        "L_used": length,
        "o_used": odd,
    }


def small_m_compare(n: int) -> dict[str, Any]:
    """Exhaustive cyclic vs independent packing for m ≤ SMALL_M, a ≤ A_MAX."""

    best_cyclic = None
    best_gap = None
    legal = 0
    beats_independent = 0
    for m in range(2, SMALL_M + 1):
        for types in product(range(1, A_MAX + 1), repeat=m):
            runs = [(odd_run, 1) for odd_run in types]
            walked = walk_runs(runs)
            if not walked["all_cyclemin"]:
                continue
            legal += 1
            odd = sum(types)
            length = odd + m
            cyclic = height_finance(n, walked["valley_logs"], m)
            independent = budget_rhs(n, length, odd)
            gap = independent - cyclic
            if cyclic + PARITY_ABS_PAD > independent:
                beats_independent += 1
            rec = {
                "types": list(types),
                "L": length,
                "o": odd,
                "cyclic": cyclic,
                "independent": independent,
                "gap": gap,
                "cheap": walked["cheap"],
                "wrap_log2": walked["wrap_log2"],
                "wrap_legal": walked["wrap_legal"],
            }
            if best_cyclic is None or cyclic > best_cyclic["cyclic"]:
                best_cyclic = rec
            if best_gap is None or gap > best_gap["gap"]:
                best_gap = rec
    return {
        "m_max": SMALL_M,
        "a_max": A_MAX,
        "legal_necklaces": legal,
        "cyclic_beats_independent": beats_independent,
        "best_cyclic": best_cyclic,
        "largest_gap": best_gap,
        "independent_strictly_larger": (
            best_cyclic is not None and best_cyclic["gap"] > PARITY_ABS_PAD
        ),
    }


def exact_chain(n: int, *, cap: int = 8) -> dict[str, Any]:
    """Realized valley chain and exact wrap attempts at every cut."""

    valleys = [n]
    runs: list[int] = []
    peaks: list[int] = []
    current = n
    for _ in range(cap):
        if current % 2 == 0:
            break
        odd_run = a_of(current, cap=16)
        if not isinstance(odd_run, int) or odd_run < 1:
            break
        rec = excursion_map(current, odd_run)
        if rec is None:
            break
        peak, landing = rec
        runs.append(odd_run)
        peaks.append(peak)
        valleys.append(landing)
        current = landing
        if landing < n:
            break
    body = [value for value in valleys if value >= n]
    if len(valleys) > len(body) and valleys[len(body)] < n:
        last = body[-1] if body else n
    else:
        last = body[-1] if body else n
    first = body[0] if body else n
    attempted = []
    for odd_run in (1, 2, 3, 5, 12):
        rec = excursion_map(last, odd_run) if last % 2 == 1 else None
        landing = rec[1] if rec is not None else None
        attempted.append(
            {
                "a": odd_run,
                "landing": landing,
                "hits_first": landing == first,
                "gap": None if landing is None else landing - first,
            }
        )
    existing = []
    for index, odd_run in enumerate(runs):
        if index + 1 >= len(valleys):
            break
        rec = excursion_map(valleys[index], odd_run)
        existing.append(
            {
                "from": valleys[index],
                "a": odd_run,
                "to": valleys[index + 1],
                "is_recorded_edge": rec is not None and rec[1] == valleys[index + 1],
            }
        )
    return {
        "n": n,
        "valleys": valleys,
        "cyclemin_valleys": body,
        "runs": runs,
        "peaks": [_int_out(peak) for peak in peaks],
        "wrap_first": first,
        "wrap_last": last,
        "true_wrap_closes": any(row["hits_first"] for row in attempted),
        "wrap_attempts": attempted,
        "existing_edges": existing,
    }


def _int_out(value: int) -> int | str:
    if value.bit_length() <= 64:
        return value
    return f"bits:{value.bit_length()}"


def almost_closed_motif(n: int, types: tuple[int, ...], *, window: int = 4000) -> dict[str, Any]:
    """Scan a=types[0] starts for an exact closed walk of the motif."""

    hits = 0
    best = None
    seed = n if n % 2 == 1 else n + 1
    scanned = 0
    while scanned < window:
        if seed % 2 == 1 and a_of(seed, cap=16) == types[0]:
            current = seed
            ok = True
            landings = [seed]
            for odd_run in types:
                rec = excursion_map(current, odd_run)
                if rec is None:
                    ok = False
                    break
                current = rec[1]
                landings.append(current)
            scanned += 1
            if ok:
                gap = landings[-1] - seed
                rec = {
                    "v": seed,
                    "landings": landings,
                    "gap": gap,
                    "rel_gap": gap / seed if seed else None,
                    "closes": landings[-1] == seed,
                }
                hits += 1
                if best is None or abs(gap) < abs(best["gap"]):
                    best = rec
                if rec["closes"]:
                    break
        seed += 2
    return {
        "types": list(types),
        "scanned": scanned,
        "hits": hits,
        "best": best,
        "closed_found": bool(best and best["closes"]),
    }


def catalog_words(length: int, odd: int) -> list[tuple[str, str]]:
    n_ooe, n_oe = run_type_counts(odd, length - odd)
    packed = packed_block_word(length, odd)
    bunched = "OOE" * n_ooe + "OE" * n_oe
    interleave = ("OOE" + "OE") * min(n_oe, n_ooe) + "OOE" * max(n_ooe - n_oe, 0)
    return [
        ("packed_mechanical", packed),
        ("bunched_ooe", bunched),
        ("interleave", interleave),
        ("extremal_letter", extremal_word(length)),
        ("christoffel", ceiling_christoffel_word(length, odd)),
    ]


def classify(payload: dict[str, Any]) -> dict[str, Any]:
    slack = payload["slack"]
    cyclic = payload["two_type_cyclic"]
    rotations = payload["necklaces"]
    small = payload["small_m"]
    wraps = payload["exact_wraps"]
    cap_strict = cyclic["cheap_cap"] < cyclic["n_ooe"]
    cyclic_excludes = cyclic["excludes"]
    still_above = cyclic["rhs"] > slack["theta"]
    wrap_closes = any(row["true_wrap_closes"] for row in wraps)
    legal_necklaces = [row for row in rotations if row["two_type"] and row["all_cyclemin"]]
    cheap_span = max((row["rotation_cheap_span"] for row in legal_necklaces), default=0)
    cap_survives_cuts = bool(legal_necklaces) and all(
        row["cheap"] <= row["cheap_cap"]
        and (row["rotation_cheap_max"] is None or row["rotation_cheap_max"] <= row["cheap_cap"])
        for row in legal_necklaces
    )
    wrap_privileged = not cap_survives_cuts
    independent_larger = bool(small["independent_strictly_larger"])
    leftover_killer = bool(cyclic_excludes)
    if leftover_killer:
        classification = CLASS_GREEN
        decision = "PROMOTE"
        reason = (
            "the two-type cyclic necklace bound excludes L=25781 "
            "at the published floor"
        )
    elif cap_strict and still_above and cap_survives_cuts and not wrap_closes:
        classification = CLASS_CLOSED
        decision = "CLOSE"
        reason = (
            "on a two-type necklace N_cheap ≤ N_OE, so the first "
            "valley is an OE landing and not a free boundary; the "
            "charged cyclic RHS stays above theta; every cyclic cut "
            "respects the cap; exact wrap does not close"
        )
    else:
        classification = CLASS_PARK
        decision = "PARK"
        reason = "cyclic necklace data are mixed and do not yield a uniform charge"
    return {
        "classification": classification,
        "decision": decision,
        "reason": reason,
        "cheap_cap_strictly_below_packing": cap_strict,
        "two_type_cyclic_excludes": cyclic_excludes,
        "two_type_cyclic_above_theta": still_above,
        "wrap_rotation_cheap_span": cheap_span,
        "cap_survives_every_cut": cap_survives_cuts,
        "wrap_is_privileged": wrap_privileged,
        "exact_wrap_closes": wrap_closes,
        "small_m_independent_larger": independent_larger,
        "leftover_killer": leftover_killer,
        "halt_theorem": False,
        "raise_n0": False,
        "open_55293": False,
        "branch_and_bound": False,
    }


def probe_payload() -> dict[str, Any]:
    odd, theta = o_min_and_theta(PHASE1_L)
    even = PHASE1_L - odd
    n_ooe, n_oe = run_type_counts(odd, even)
    slack = deficit_row(PHASE1_L, floor=PUBLISHED_FLOOR)
    cap = two_type_cheap_cap(odd, even)
    cyclic_rhs = two_type_cyclic_rhs(START, PHASE1_L, odd)
    packed = budget_rhs(START, PHASE1_L, odd)
    necklaces = [necklace_row(name, word, START) for name, word in catalog_words(PHASE1_L, odd)]
    motifs = [
        motif_row("repeated_ooe", 2, 1, odd, even, START),
        motif_row("five_three", 5, 3, odd, even, START),
        motif_row("twelve_seven", 12, 7, odd, even, START),
        motif_row("fiftythree_thirtyone", 53, 31, odd, even, START),
    ]
    # (OOE)^3 OE is four runs; rebuild that motif separately.
    climb_copies = min(n_ooe // 3, n_oe)
    climb_runs = [(2, 1), (2, 1), (2, 1), (1, 1)] * climb_copies
    climb_walk = walk_runs(climb_runs)
    motifs.append(
        {
            "name": "climb3_oe",
            "k": "2+2+2+1",
            "ell": 4,
            "copies": climb_copies,
            "leftover_o": odd - climb_copies * 7,
            "leftover_e": even - climb_copies * 4,
            "cheap": climb_walk["cheap"],
            "all_cyclemin": climb_walk["all_cyclemin"],
            "wrap_log2": climb_walk["wrap_log2"],
            "wrap_legal": climb_walk["wrap_legal"],
            "height_rhs": height_finance(START, climb_walk["valley_logs"], climb_copies * 4),
            "L_used": climb_copies * 10,
            "o_used": climb_copies * 7,
        }
    )
    small = small_m_compare(START)
    wraps = [exact_chain(seed) for seed in WITNESSES]
    almost = almost_closed_motif(START, (2, 2, 2, 1), window=800)
    payload = {
        "bound": "cyclic_valley",
        "L": PHASE1_L,
        "n": START,
        "slack": {
            "L": slack["L"],
            "o": slack["o"],
            "theta": slack["theta"],
            "packed": slack["packed"],
            "margin": slack["margin"],
            "packed_over_theta": slack["packed_over_theta"],
            "k_lose_cheap": slack["k_lose_cheap"],
            "deepen_all_still_above_theta": slack["deepen_all_still_above_theta"],
        },
        "two_type_cyclic": {
            "n_ooe": n_ooe,
            "n_oe": n_oe,
            "cheap_cap": cap,
            "lost_vs_packing": n_ooe - cap,
            "inside_k_lose": (n_ooe - cap) <= slack["k_lose_cheap"],
            "rhs": cyclic_rhs,
            "packed": packed,
            "theta": theta,
            "gap_vs_packed": packed - cyclic_rhs,
            "over_theta": cyclic_rhs / theta if theta else None,
            "excludes": _excludes(theta, cyclic_rhs),
        },
        "necklaces": necklaces,
        "motifs": motifs,
        "small_m": small,
        "exact_wraps": wraps,
        "almost_closed_2211": almost,
        "charged_excludes": {
            "parity_excludes": parity_excludes(PHASE1_L, odd, theta, PUBLISHED_FLOOR),
            "budget_excludes": budget_excludes(PHASE1_L, odd, theta, PUBLISHED_FLOOR),
        },
        "published_floor": PUBLISHED_FLOOR,
        "start": START,
    }
    payload["decision"] = classify(payload)
    return payload


def write_artifacts(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload if payload is not None else probe_payload()
    CYCLIC_DIR.mkdir(parents=True, exist_ok=True)
    path = CYCLIC_DIR / "summary.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data


def main() -> None:
    payload = write_artifacts()
    decision = payload["decision"]
    print(decision["classification"])
    print(decision["reason"])
    cyclic = payload["two_type_cyclic"]
    print(
        f"cheap_cap={cyclic['cheap_cap']} n_ooe={cyclic['n_ooe']} "
        f"rhs={cyclic['rhs']:.6e} theta={cyclic['theta']:.6e} "
        f"excludes={cyclic['excludes']}"
    )


if __name__ == "__main__":
    main()
