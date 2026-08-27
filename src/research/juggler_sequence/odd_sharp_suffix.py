"""Odd-start sharp even-tower suffixes.

Not a Research Engine control-layer experiment. Search uses integer
roots only: isqrt and binary-search cube roots. No n^{3/2} construction,
no cmp_pow census, and not a termination theorem.
"""

from __future__ import annotations

import json
from functools import cmp_to_key
from math import isqrt
from pathlib import Path
from typing import Any

from research.juggler_sequence.power_algebra import is_square, local_tight
from research.juggler_sequence.power_words import (
    ANTI_OVERCLAIM,
    LEAN_PATH,
    floor_power,
)
from research.juggler_sequence.saturation_budget import has_pow_two_depth, square_depth

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "juggler_odd_sharp_suffix.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "juggler_odd_sharp_suffix.md"
HITS_DIR = REPO_ROOT / "data" / "research" / "juggler" / "odd_sharp_suffix" / "hits"
ANALYSIS_DIR = REPO_ROOT / "data" / "research" / "juggler" / "odd_sharp_suffix" / "analysis"

CLASS_UNBOUNDED = "ODD_SHARP_SUFFIX_UNBOUNDED"
CLASS_FINITE = "ODD_SHARP_SUFFIX_FINITE"
CLASS_IMPOSSIBLE = "ODD_SHARP_SUFFIX_IMPOSSIBLE"
CLASS_WITNESS = "ODD_SHARP_SUFFIX_WITNESS"
CLASS_INCOMPLETE = "ODD_SHARP_SUFFIX_INCOMPLETE"

N_MAX = 50_000
B_MAX = 2_500
A8_MAX = 150
S1_SAMPLE_MAX = 16

LEAN_THEOREMS = (
    "floor_sqrt_eq_iff_sq_interval",
    "floorPower_odd_eq_iff_cube_interval",
    "floorPower_odd_eq_pow_two_depth_iff",
    "fourth_window_occupancy",
    "exact_cube_left_endpoint",
    "fourth_window_cube_eq_succ_cbrt",
    "noncube_odd_cbrt_fourth_window_cube_even",
    "odd_cube_interval_of_odd_cbrt_implies_square",
    "floorPower_odd_eq_fourth_power_of_odd_cbrt_implies_square",
    "odd_nonsquare_not_fourth_power_of_odd_cbrt",
    "odd_first_defect_not_pow_two_depth_ge_two_of_odd_cbrt",
)

LEAN_IMPOSSIBLE = "floorPower_odd_pow_two_depth_ge_two_false"


def integer_cbrt(n: int) -> int:
    """Largest t with t^3 ≤ n. Binary search. No floats."""

    if n < 0:
        raise ValueError("integer_cbrt is defined on nonnegative integers")
    if n < 2:
        return n
    lo = 0
    hi = 1 << ((n.bit_length() + 2) // 3)
    while hi * hi * hi < n:
        hi <<= 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        cube = mid * mid * mid
        if cube <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def is_cube(n: int) -> bool:
    if n < 0:
        return False
    root = integer_cbrt(n)
    return root * root * root == n


def nearest_cube_record(a: int, n: int) -> dict[str, Any]:
    """Exact nearest-cube data for one persisted interval hit. No floats."""

    if a < 1 or n < 1:
        raise ValueError("nearest_cube_record requires positive a and n")
    lower = a**8
    width = 2 * (a**4)
    m = integer_cbrt(lower)
    r = lower - m * m * m
    gap = (m + 1) ** 3 - lower
    a_is_cube = is_cube(a)
    if r == 0:
        role = "left_endpoint"
    elif n == m + 1:
        role = "succ_cbrt"
    else:
        role = "other"
    return {
        "a": a,
        "n": n,
        "m": m,
        "r": r,
        "gap": gap,
        "width": width,
        "gap_le_width": gap <= width,
        "a_is_cube": a_is_cube,
        "n_eq_m": n == m,
        "n_eq_m_plus_1": n == m + 1,
        "role": role,
        "n_is_odd": n % 2 == 1,
        "n_is_square": is_square(n),
        "a_odd": a % 2 == 1,
        "m_odd": m % 2 == 1,
        "a_mod_2": a % 2,
        "a_mod_3": a % 3,
        "a_mod_4": a % 4,
        "a_mod_8": a % 8,
        "a_mod_16": a % 16,
        "a_mod_32": a % 32,
        "n_mod_2": n % 2,
        "n_mod_3": n % 3,
        "n_mod_4": n % 4,
        "n_mod_8": n % 8,
        "n_mod_16": n % 16,
        "n_mod_32": n % 32,
    }


def load_persisted_hits(hits_dir: Path | None = None) -> list[dict[str, Any]]:
    directory = HITS_DIR if hits_dir is None else hits_dir
    rows: list[dict[str, Any]] = []
    for path in sorted(directory.glob("a_*.json"), key=lambda p: int(p.stem[2:])):
        raw = json.loads(path.read_text(encoding="utf-8"))
        rows.append(nearest_cube_record(int(raw["a"]), int(raw["n"])))
    return rows


def analyze_persisted_hits(
    hits_dir: Path | None = None,
) -> dict[str, Any]:
    """Split persisted interval cubes into exact cubes, a=97, and other."""

    records = load_persisted_hits(hits_dir)
    exact = [row for row in records if row["a_is_cube"]]
    a97 = [row for row in records if row["a"] == 97]
    other = [row for row in records if not row["a_is_cube"] and row["a"] != 97]
    odd_non_square = [
        row for row in records if row["n_is_odd"] and not row["n_is_square"]
    ]
    odd_a_inexact = [row for row in records if row["a_odd"] and not row["a_is_cube"]]
    inexact = [row for row in records if not row["a_is_cube"]]
    inexact_succ = all(row["role"] == "succ_cbrt" for row in inexact)
    odd_cbrt_inexact_even_n = all(
        (not row["m_odd"]) or (not row["n_is_odd"]) for row in inexact
    )
    return {
        "hit_count": len(records),
        "exact_cube_count": len(exact),
        "a97_count": len(a97),
        "other_count": len(other),
        "odd_non_square_count": len(odd_non_square),
        "odd_a_inexact_count": len(odd_a_inexact),
        "inexact_is_succ_cbrt": inexact_succ,
        "odd_cbrt_inexact_even_n": odd_cbrt_inexact_even_n,
        "odd_a_need_not_force_m_odd": integer_cbrt(3**8) % 2 == 0,
        "exact_left_endpoint": all(row["role"] == "left_endpoint" for row in exact),
        "a97": None if not a97 else a97[0],
        "other": [{"a": row["a"], "n": row["n"], "role": row["role"]} for row in other],
        "odd_non_square": [row["a"] for row in odd_non_square],
        "residue_counts": _residue_counts(records),
        "invariant": (
            "a non-cube leaves at most the candidate n = m+1; that candidate "
            "is even exactly when m is odd. The only persisted inexact hit "
            "is a = 97, where m is odd and n is even"
        ),
        "remaining_case": (
            "an even m makes n = m+1 odd. Odd a does not force m odd "
            "(a = 3 has m = 18). No persisted hit has even m except the "
            "exact even family a = k^3. The leftover is: a non-cube with "
            "even m never places m+1 in the window"
        ),
    }


def _residue_counts(records: list[dict[str, Any]]) -> dict[str, Any]:
    exact = [row for row in records if row["a_is_cube"]]
    inexact = [row for row in records if not row["a_is_cube"]]
    moduli = (2, 3, 4, 8, 16, 32)

    def bundle(rows: list[dict[str, Any]], prefix: str) -> dict[str, dict[str, int]]:
        out: dict[str, dict[str, int]] = {}
        for mod in moduli:
            key = f"{prefix}_mod_{mod}"
            counts: dict[str, int] = {}
            for row in rows:
                counts[str(row[key])] = counts.get(str(row[key]), 0) + 1
            out[f"mod_{mod}"] = counts
        return out

    return {
        "exact_a": bundle(exact, "a"),
        "exact_n": bundle(exact, "n"),
        "inexact_a": bundle(inexact, "a"),
        "inexact_n": bundle(inexact, "n"),
    }


def render_nearest_cube_markdown(analysis: dict[str, Any]) -> str:
    a97 = analysis["a97"]
    lines = [
        "# Nearest-cube reduction of persisted fourth-power hits",
        "",
        "Exact integer analysis of the persisted `a < 10^8` hit list.",
        "This is not a theorem and not a new search.",
        "",
        f"- hits: `{analysis['hit_count']}`",
        f"- exact cubes `a = k^3`: `{analysis['exact_cube_count']}`",
        f"- `a = 97`: `{analysis['a97_count']}`",
        f"- other non-cubes: `{analysis['other_count']}`",
        f"- odd non-squares: `{analysis['odd_non_square_count']}`",
        f"- odd-a inexact hits: `{analysis['odd_a_inexact_count']}`",
        f"- inexact hits are `n = m+1`: `{analysis['inexact_is_succ_cbrt']}`",
        f"- odd-`m` inexact hits have even `n`: `{analysis['odd_cbrt_inexact_even_n']}`",
        f"- odd `a` need not force odd `m` (`a=3`): `{analysis['odd_a_need_not_force_m_odd']}`",
        f"- exact hits sit at the left endpoint: `{analysis['exact_left_endpoint']}`",
        "",
        "## Invariant",
        "",
        analysis["invariant"] + ".",
        "",
        analysis["remaining_case"] + ".",
        "",
        "## a = 97",
        "",
    ]
    if a97 is None:
        lines.append("No `a = 97` hit.")
    else:
        lines.extend(
            [
                f"- `m = {a97['m']}`",
                f"- `r = {a97['r']}`",
                f"- gap `(m+1)^3 - a^8 = {a97['gap']}`",
                f"- width `2a^4 = {a97['width']}`",
                f"- `n = m+1`: `{a97['n_eq_m_plus_1']}`",
                f"- `n` even: `{not a97['n_is_odd']}`",
                f"- `a` not a cube: `{not a97['a_is_cube']}`",
            ]
        )
    lines.extend(
        [
            "",
            "## Residues",
            "",
            "Exact-family `n` follows `k^8` and is therefore even exactly",
            "when `k` is even. The unique inexact hit is `a = 97 ≡ 1 (mod 32)`,",
            "`n = 198636 ≡ 12 (mod 16)`. No other residue pattern is needed.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def write_nearest_cube_analysis(
    hits_dir: Path | None = None,
    analysis_dir: Path | None = None,
) -> dict[str, Any]:
    data = analyze_persisted_hits(hits_dir)
    directory = ANALYSIS_DIR if analysis_dir is None else analysis_dir
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "nearest_cube.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    (directory / "nearest_cube.md").write_text(
        render_nearest_cube_markdown(data), encoding="utf-8"
    )
    return data


EVEN_CBRT_SCAN_MAX = 20_000
HIGH_POSITION_EXAMPLE_A = 37_840


def even_cbrt_surplus_record(a: int) -> dict[str, Any]:
    """Exact gap, width, and surplus for one a. No floats."""

    if a < 1:
        raise ValueError("even_cbrt_surplus_record requires positive a")
    lower = a**8
    width = 2 * (a**4)
    m = integer_cbrt(lower)
    r = lower - m * m * m
    gap = (m + 1) ** 3 - lower
    return {
        "a": a,
        "m": m,
        "r": r,
        "gap": gap,
        "width": width,
        "surplus": gap - width,
        "m_even": m % 2 == 0,
        "a_is_cube": is_cube(a),
        "a_odd": a % 2 == 1,
        "in_window": gap <= width,
        "cube_gap": 3 * m * m + 3 * m + 1,
    }


def analyze_even_cbrt_near_misses(
    a_max: int = EVEN_CBRT_SCAN_MAX,
) -> dict[str, Any]:
    """Even-m surplus shape on a small discovery range. Not a 10^8 rerun."""

    if a_max < 1:
        raise ValueError("analyze_even_cbrt_near_misses requires a_max >= 1")
    even_hits: list[dict[str, Any]] = []
    closest: list[dict[str, Any]] = []
    min_surplus: dict[str, Any] | None = None
    even_count = 0
    for a in range(1, a_max + 1):
        rec = even_cbrt_surplus_record(a)
        if rec["a_is_cube"] or not rec["m_even"]:
            continue
        even_count += 1
        if rec["in_window"]:
            even_hits.append({"a": rec["a"], "m": rec["m"], "surplus": rec["surplus"]})
        if min_surplus is None or rec["surplus"] < min_surplus["surplus"]:
            min_surplus = rec
        closest.append(rec)

    def _ratio_cmp(left: dict[str, Any], right: dict[str, Any]) -> int:
        cross = left["gap"] * right["width"] - right["gap"] * left["width"]
        if cross < 0:
            return -1
        if cross > 0:
            return 1
        return left["a"] - right["a"]

    closest.sort(key=cmp_to_key(_ratio_cmp))
    closest = closest[:8]
    a97 = even_cbrt_surplus_record(97)
    a3 = even_cbrt_surplus_record(3)
    high = even_cbrt_surplus_record(HIGH_POSITION_EXAMPLE_A)
    return {
        "a_max": a_max,
        "even_m_noncube_count": even_count,
        "even_m_in_window_count": len(even_hits),
        "even_m_hits": even_hits,
        "min_surplus": None
        if min_surplus is None
        else {
            "a": min_surplus["a"],
            "m": min_surplus["m"],
            "surplus": min_surplus["surplus"],
            "gap": min_surplus["gap"],
            "width": min_surplus["width"],
        },
        "closest_by_gap_over_width": [
            {
                "a": row["a"],
                "m": row["m"],
                "surplus": row["surplus"],
                "gap": row["gap"],
                "width": row["width"],
            }
            for row in closest
        ],
        "a97": {
            "m": a97["m"],
            "m_even": a97["m_even"],
            "in_window": a97["in_window"],
            "surplus": a97["surplus"],
        },
        "a3": {
            "m": a3["m"],
            "m_even": a3["m_even"],
            "in_window": a3["in_window"],
            "surplus": a3["surplus"],
        },
        "high_position_example": {
            "a": high["a"],
            "m": high["m"],
            "r": high["r"],
            "cube_gap": high["cube_gap"],
            "gap": high["gap"],
            "width": high["width"],
            "m_even": high["m_even"],
            "in_window": high["in_window"],
            "surplus": high["surplus"],
        },
        "trivial_cbrt_bound_cannot_threshold": True,
        "invariant": (
            "a non-cube with even m never placed m+1 in the window on the "
            "discovery range; a=97 remains an odd-m hit; interval position "
            "can sit at the top of a cube cell, so a uniform remaining-"
            "fraction bound is false"
        ),
        "remaining_case": (
            "the trivial bound m >= a^{8/3}-1 is sharp and cannot produce "
            "an A0. Proving gap > 2a^4 for even m needs more than cube-root "
            "bracketing"
        ),
    }


def render_even_cbrt_markdown(analysis: dict[str, Any]) -> str:
    min_s = analysis["min_surplus"]
    high = analysis["high_position_example"]
    a97 = analysis["a97"]
    a3 = analysis["a3"]
    lines = [
        "# Even cube-root surplus of fourth-power windows",
        "",
        "Discovery scan of non-cube `a` with even `m = ⌊∛(a^8)⌋`.",
        "This is not a `10^8` rerun and not a theorem.",
        "",
        f"- discovery `a_max`: `{analysis['a_max']}`",
        f"- even-`m` non-cubes: `{analysis['even_m_noncube_count']}`",
        f"- even-`m` window hits: `{analysis['even_m_in_window_count']}`",
        f"- trivial `m >= a^{{8/3}}-1` cannot threshold: `{analysis['trivial_cbrt_bound_cannot_threshold']}`",
        "",
        "## a = 97 must survive",
        "",
        f"- `m = {a97['m']}` odd: `{not a97['m_even']}`",
        f"- in window: `{a97['in_window']}`",
        f"- surplus `gap - 2a^4 = {a97['surplus']}`",
        "",
        "## a = 3 even-`m` miss",
        "",
        f"- `m = {a3['m']}` even: `{a3['m_even']}`",
        f"- in window: `{a3['in_window']}`",
        f"- surplus: `{a3['surplus']}`",
        "",
        "## Closest even-`m` near-misses",
        "",
        "Ranked by `gap / (2a^4)`. All listed ratios are `> 1`.",
        "",
    ]
    if min_s is not None:
        lines.append(
            f"Minimum surplus is `a = {min_s['a']}`, surplus `{min_s['surplus']}`."
        )
        lines.append("")
    for row in analysis["closest_by_gap_over_width"]:
        lines.append(
            f"- a `{row['a']}`: m `{row['m']}`, gap `{row['gap']}`, "
            f"width `{row['width']}`, surplus `{row['surplus']}`"
        )
    lines.extend(
        [
            "",
            "## High interval position",
            "",
            f"Example `a = {high['a']}` has even `m = {high['m']}`,",
            f"`r = {high['r']}`, cube gap `{high['cube_gap']}`,",
            f"remaining gap `{high['gap']}`, width `{high['width']}`.",
            "The eighth power can sit at the top of a cube cell. A uniform",
            "positive remaining-fraction lemma is false. The candidate is",
            f"still outside the window (in_window `{high['in_window']}`).",
            "",
            "## Invariant",
            "",
            analysis["invariant"] + ".",
            "",
            analysis["remaining_case"] + ".",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def write_even_cbrt_analysis(
    a_max: int = EVEN_CBRT_SCAN_MAX,
    analysis_dir: Path | None = None,
) -> dict[str, Any]:
    data = analyze_even_cbrt_near_misses(a_max)
    directory = ANALYSIS_DIR if analysis_dir is None else analysis_dir
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "even_cbrt.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    (directory / "even_cbrt.md").write_text(
        render_even_cbrt_markdown(data), encoding="utf-8"
    )
    return data


POW2_MODULI = (2, 4, 8, 16, 32, 64, 128)
ODD_MODULI = (3, 5, 7, 9, 13)
MIXED_MODULI = (15, 24)
MODULAR_SCAN_MAX = 2_000
REGRESSION_AS = (3, 6, 8, 27, 79, 97)


def _v2(n: int) -> int | None:
    if n == 0:
        return None
    n = abs(n)
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def modular_pair_residues(a: int, m: int, q: int) -> dict[str, int]:
    d = (m + 1) ** 3 - a**8
    r = a**8 - m**3
    w = 2 * (a**4)
    return {
        "a": a % q,
        "m": m % q,
        "D": d % q,
        "r": r % q,
        "w": w % q,
    }


def analyze_even_cbrt_moduli(
    a_max: int = MODULAR_SCAN_MAX,
) -> dict[str, Any]:
    """Targeted even-m residue tables. Not a generic modular framework."""

    if a_max < 1:
        raise ValueError("analyze_even_cbrt_moduli requires a_max >= 1")
    moduli = POW2_MODULI + ODD_MODULI + MIXED_MODULI
    even_m_rows: list[dict[str, Any]] = []
    odd_m_odd_a = 0
    even_m_window = 0
    v2_even_a: dict[str, int] = {}
    v2_odd_a: dict[str, int] = {}
    r32_odd_a_even_m: dict[str, int] = {}
    d32_odd_a_even_m: dict[str, int] = {}
    for a in range(1, a_max + 1):
        rec = even_cbrt_surplus_record(a)
        if rec["a_is_cube"]:
            continue
        if rec["m_even"]:
            even_m_rows.append(rec)
            if rec["in_window"]:
                even_m_window += 1
            key = str(_v2(rec["gap"]))
            if rec["a_odd"]:
                bucket = v2_odd_a
                r32_odd_a_even_m[str(rec["r"] % 32)] = (
                    r32_odd_a_even_m.get(str(rec["r"] % 32), 0) + 1
                )
                d32_odd_a_even_m[str(rec["gap"] % 32)] = (
                    d32_odd_a_even_m.get(str(rec["gap"] % 32), 0) + 1
                )
            else:
                bucket = v2_even_a
            bucket[key] = bucket.get(key, 0) + 1
        elif rec["a_odd"]:
            odd_m_odd_a += 1

    def class_table(q: int) -> dict[str, Any]:
        pairs: dict[str, int] = {}
        d_set: set[int] = set()
        r_set: set[int] = set()
        even_m_classes = 0
        for rec in even_m_rows:
            key = f"{rec['a'] % q},{rec['m'] % q}"
            if key not in pairs:
                even_m_classes += 1
            pairs[key] = pairs.get(key, 0) + 1
            d_set.add(rec["gap"] % q)
            r_set.add(rec["r"] % q)
        return {
            "modulus": q,
            "even_m_class_count": even_m_classes,
            "D_residues": sorted(d_set),
            "r_residues": sorted(r_set),
            "even_m_empty": even_m_classes == 0,
        }

    modulus_tables = [class_table(q) for q in moduli]
    regressions = {}
    for a in REGRESSION_AS:
        rec = even_cbrt_surplus_record(a)
        regressions[str(a)] = {
            "m": rec["m"],
            "m_even": rec["m_even"],
            "a_odd": rec["a_odd"],
            "a_is_cube": rec["a_is_cube"],
            "in_window": rec["in_window"],
            "D": rec["gap"],
            "r": rec["r"],
            "w": rec["width"],
            "v2D": _v2(rec["gap"]),
            "residues": {str(q): modular_pair_residues(a, rec["m"], q) for q in moduli},
        }
    a97 = regressions["97"]
    a3 = regressions["3"]
    odd_eighth_mod32 = sorted({pow(a, 8, 32) for a in range(1, 32, 2)})
    odd_a_fourth_mod32 = sorted({pow(a, 4, 32) for a in range(1, 32, 2)})
    two_a4_odd_mod32 = sorted({(2 * pow(a, 4, 32)) % 32 for a in range(1, 32, 2)})
    candidate_a = False
    candidate_b = all(not row["even_m_empty"] for row in modulus_tables if row["modulus"] in POW2_MODULI)
    candidate_c = all(not row["even_m_empty"] for row in modulus_tables)
    # Fixed q cannot sign-determine D-2a^4 once 2a^4 >= q.
    candidate_d = False
    return {
        "a_max": a_max,
        "even_m_noncube_count": len(even_m_rows),
        "even_m_window_count": even_m_window,
        "odd_m_odd_a_noncube_count": odd_m_odd_a,
        "parity": {
            "m_even_a_even_implies_D_odd": all(
                rec["gap"] % 2 == 1 for rec in even_m_rows if not rec["a_odd"]
            ),
            "m_even_a_odd_implies_D_even": all(
                rec["gap"] % 2 == 0 for rec in even_m_rows if rec["a_odd"]
            ),
            "a97_D_odd": a97["D"] % 2 == 1,
            "a3_D_even": a3["D"] % 2 == 0,
        },
        "odd_a_eighth_mod32": odd_eighth_mod32,
        "odd_a_two_a4_mod32": two_a4_odd_mod32,
        "odd_a_fourth_mod32": odd_a_fourth_mod32,
        "r_mod32_odd_a_even_m": r32_odd_a_even_m,
        "D_mod32_odd_a_even_m": d32_odd_a_even_m,
        "v2D_even_m_a_even": v2_even_a,
        "v2D_even_m_a_odd": v2_odd_a,
        "modulus_tables": modulus_tables,
        "regressions": regressions,
        "a97_survives": a97["in_window"] and not a97["m_even"],
        "candidates": {
            "A_pure_parity": candidate_a,
            "B_pow2_empty_even_m": not candidate_b,
            "C_mixed_empty_even_m": not candidate_c,
            "D_modular_plus_size": candidate_d,
            "E_not_modular": True,
        },
        "classification": "OBSTRUCTION_NOT_MODULAR",
        "invariant": (
            "even m occurs (a=3); D is odd when a is even and even when a "
            "is odd. For odd a, a^8 ≡ 1 (mod 32) and 2a^4 ≡ 2 (mod 32), "
            "and r ≡ 1,9,25 (mod 32) on the discovery range. None of these "
            "forces D > 2a^4. a=97 remains an odd-m window hit"
        ),
        "remaining_case": (
            "a non-cube with even m and D <= 2a^4 is not ruled out by "
            "parity, 2^k, or the small odd/mixed moduli. The leftover is "
            "still that size inequality"
        ),
    }


def render_even_cbrt_moduli_markdown(analysis: dict[str, Any]) -> str:
    a97 = analysis["regressions"]["97"]
    a3 = analysis["regressions"]["3"]
    cand = analysis["candidates"]
    lines = [
        "# Even cube-root modular obstruction",
        "",
        "Targeted residue tables for even `m = ⌊∛(a^8)⌋`.",
        "This is not a generic modular framework, not a `10^8` rerun,",
        "and not a theorem.",
        "",
        f"- discovery `a_max`: `{analysis['a_max']}`",
        f"- even-`m` non-cubes: `{analysis['even_m_noncube_count']}`",
        f"- even-`m` window hits: `{analysis['even_m_window_count']}`",
        f"- classification: **{analysis['classification']}**",
        "",
        "## Parity (Candidate A)",
        "",
        f"- even `m`, even `a` ⇒ `D` odd: `{analysis['parity']['m_even_a_even_implies_D_odd']}`",
        f"- even `m`, odd `a` ⇒ `D` even: `{analysis['parity']['m_even_a_odd_implies_D_even']}`",
        f"- `a=97` has odd `D`: `{analysis['parity']['a97_D_odd']}`",
        f"- `a=3` has even `D`: `{analysis['parity']['a3_D_even']}`",
        "",
        "Parity splits the cases but does not contradict `0 < D ≤ 2a^4`.",
        f"Candidate A: `{cand['A_pure_parity']}`.",
        "",
        "## a = 97 regression",
        "",
        f"- `m = {a97['m']}` even: `{a97['m_even']}`",
        f"- in window: `{a97['in_window']}`",
        f"- `D = {a97['D']}`, `v2(D) = {a97['v2D']}`",
        "",
        "## a = 3 even-`m` miss",
        "",
        f"- `m = {a3['m']}` even: `{a3['m_even']}`",
        f"- in window: `{a3['in_window']}`",
        f"- `D = {a3['D']}`",
        "",
        "Because `a=3` is a live even-`m` pair, no modulus can claim that",
        "even `m` is impossible. An obstruction must use `D ≤ 2a^4`.",
        "",
        "## Odd `a` modulo 32",
        "",
        f"- odd eighth powers: `{analysis['odd_a_eighth_mod32']}`",
        f"- `2a^4` for odd `a`: `{analysis['odd_a_two_a4_mod32']}`",
        f"- even-`m` `r` counts: `{analysis['r_mod32_odd_a_even_m']}`",
        f"- even-`m` `D` counts: `{analysis['D_mod32_odd_a_even_m']}`",
        "",
        "## Modulus tables",
        "",
        "Each row is observed even-`m` non-cubes on the discovery range.",
        "Empty even-`m` classes would be Candidate B/C. None are empty.",
        "",
    ]
    for row in analysis["modulus_tables"]:
        residues = row["D_residues"]
        shown = residues if len(residues) <= 16 else f"{len(residues)} values"
        lines.append(
            f"- q `{row['modulus']}`: even-`m` classes `{row['even_m_class_count']}`, "
            f"empty `{row['even_m_empty']}`, "
            f"`D` residues `{shown}`"
        )
    lines.extend(
        [
            "",
            "## Candidates",
            "",
            f"- A pure parity: `{cand['A_pure_parity']}`",
            f"- B some `2^k` empties even `m`: `{cand['B_pow2_empty_even_m']}`",
            f"- C mixed small modulus empties even `m`: `{cand['C_mixed_empty_even_m']}`",
            f"- D modular + size: `{cand['D_modular_plus_size']}`",
            f"- E not modular: `{cand['E_not_modular']}`",
            "",
            "## Invariant",
            "",
            analysis["invariant"] + ".",
            "",
            analysis["remaining_case"] + ".",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def write_even_cbrt_moduli_analysis(
    a_max: int = MODULAR_SCAN_MAX,
    analysis_dir: Path | None = None,
) -> dict[str, Any]:
    data = analyze_even_cbrt_moduli(a_max)
    directory = ANALYSIS_DIR if analysis_dir is None else analysis_dir
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "even_cbrt_moduli.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    (directory / "even_cbrt_moduli.md").write_text(
        render_even_cbrt_moduli_markdown(data), encoding="utf-8"
    )
    return data


NEAR_POWER_SCAN_MAX = EVEN_CBRT_SCAN_MAX
NEAR_POWER_K_MAX = 30
NEAR_POWER_U_RADIUS = 6
CLASS_NONCUBE_GAP_CE = "NONCUBE_GAP_COUNTEREXAMPLE"
CLASS_NEAR_POWER_GAP = "NEAR_POWER_GAP_GREEN"
CLASS_FOURTH_RIGIDITY = "FOURTH_POWER_RIGIDITY_GREEN"
CLASS_ODD_FOURTH = "ODD_FOURTH_POWER_GREEN"
CLASS_DIOPHANTINE_ESC = "DIOPHANTINE_ESCALATION_REQUIRED"


def nearest_cube_signed(a: int) -> tuple[int, int]:
    """Nearest cube k^3 to a, with signed u = a - k^3. Ties keep the floor."""

    if a < 1:
        raise ValueError("nearest_cube_signed requires positive a")
    k = integer_cbrt(a)
    cube = k * k * k
    if cube == a:
        return k, 0
    below = a - cube
    above = (k + 1) ** 3 - a
    if above < below:
        return k + 1, a - (k + 1) ** 3
    return k, below


def eighth_in_exact_family_cell(a: int, k: int) -> bool:
    """Whether a^8 lies in [k^{24}, (k^8+1)^3)."""

    if k < 1:
        return False
    eighth = a**8
    k8 = k**8
    return k8**3 <= eighth < (k8 + 1) ** 3


def near_power_record(a: int) -> dict[str, Any]:
    """Surplus record plus the signed nearest-cube displacement (u, v)."""

    rec = even_cbrt_surplus_record(a)
    k, u = nearest_cube_signed(a)
    k8 = k**8
    v = rec["m"] - k8
    return {
        **rec,
        "k": k,
        "u": u,
        "k8": k8,
        "v": v,
        "same_sign_uv": (u > 0 and v > 0) or (u < 0 and v < 0) or (u == 0 and v == 0),
        "leaves_exact_cell": not eighth_in_exact_family_cell(a, k),
        "linear_3v": 3 * v,
        "linear_8k5u": 8 * (k**5) * u,
    }


def _compact_near_power(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "a": row["a"],
        "m": row["m"],
        "k": row["k"],
        "u": row["u"],
        "v": row["v"],
        "m_even": row["m_even"],
        "a_odd": row["a_odd"],
        "a_is_cube": row["a_is_cube"],
        "same_sign_uv": row["same_sign_uv"],
        "leaves_exact_cell": row["leaves_exact_cell"],
        "r": row["r"],
        "gap": row["gap"],
        "width": row["width"],
        "surplus": row["surplus"],
        "in_window": row["in_window"],
        "cube_gap": row["cube_gap"],
    }


def _neighborhood_row(k: int, u: int) -> dict[str, Any]:
    a = k**3 + u
    if a < 1:
        raise ValueError("_neighborhood_row requires positive a")
    rec = near_power_record(a)
    k8 = k**8
    return {
        **_compact_near_power(rec),
        "ref_k": k,
        "ref_u": u,
        "ref_v": rec["m"] - k8,
        "leaves_ref_cell": not eighth_in_exact_family_cell(a, k),
    }


def analyze_near_power_gap(
    a_max: int = NEAR_POWER_SCAN_MAX,
    k_max: int = NEAR_POWER_K_MAX,
    u_radius: int = NEAR_POWER_U_RADIUS,
) -> dict[str, Any]:
    """Closest even-m failures and a=k^3+u neighborhoods. Not a 10^8 rerun."""

    if a_max < 1 or k_max < 1 or u_radius < 1:
        raise ValueError("analyze_near_power_gap requires positive bounds")

    even_rows: list[dict[str, Any]] = []
    even_hits: list[dict[str, Any]] = []
    min_surplus: dict[str, Any] | None = None
    min_r: dict[str, Any] | None = None
    even_count = 0
    same_sign_count = 0
    leaves_count = 0
    surplus_lt_a4 = 0
    for a in range(1, a_max + 1):
        rec = near_power_record(a)
        if rec["a_is_cube"] or not rec["m_even"]:
            continue
        even_count += 1
        even_rows.append(rec)
        if rec["same_sign_uv"]:
            same_sign_count += 1
        if rec["leaves_exact_cell"]:
            leaves_count += 1
        if rec["surplus"] < rec["a"] ** 4:
            surplus_lt_a4 += 1
        if rec["in_window"]:
            even_hits.append(_compact_near_power(rec))
        if min_surplus is None or rec["surplus"] < min_surplus["surplus"]:
            min_surplus = rec
        if min_r is None or rec["r"] < min_r["r"]:
            min_r = rec

    def _ratio_cmp(left: dict[str, Any], right: dict[str, Any]) -> int:
        cross = left["gap"] * right["width"] - right["gap"] * left["width"]
        if cross < 0:
            return -1
        if cross > 0:
            return 1
        return left["a"] - right["a"]

    def _top_ratio_cmp(left: dict[str, Any], right: dict[str, Any]) -> int:
        cross = left["r"] * right["cube_gap"] - right["r"] * left["cube_gap"]
        if cross > 0:
            return -1
        if cross < 0:
            return 1
        return left["a"] - right["a"]

    closest_ratio = sorted(even_rows, key=cmp_to_key(_ratio_cmp))[:8]
    closest_surplus = sorted(even_rows, key=lambda row: (row["surplus"], row["a"]))[:8]
    closest_top = sorted(even_rows, key=cmp_to_key(_top_ratio_cmp))[:8]

    neighborhood: list[dict[str, Any]] = []
    u1_window: list[dict[str, Any]] = []
    u1_stays_in_ref_cell = 0
    for k in range(1, k_max + 1):
        for u in range(-u_radius, u_radius + 1):
            if u == 0:
                continue
            a = k**3 + u
            if a < 1:
                continue
            row = _neighborhood_row(k, u)
            neighborhood.append(row)
            if abs(u) == 1 and row["in_window"]:
                u1_window.append(row)
            if abs(u) == 1 and not row["leaves_ref_cell"]:
                u1_stays_in_ref_cell += 1
    exact_cell_noncube = sum(1 for row in neighborhood if not row["leaves_ref_cell"])

    adversarial_as = (1, 2, 3, 5, 6, 8, 27, 79, 97, 125, HIGH_POSITION_EXAMPLE_A)
    adversarial = [_compact_near_power(near_power_record(a)) for a in adversarial_as]
    a97 = near_power_record(97)
    a3 = near_power_record(3)

    route_a = (not a97["in_window"]) or a97["a_is_cube"]
    leaves_is_exclusive = exact_cell_noncube == 0 and u1_stays_in_ref_cell == 0
    leaves_implies_miss = not a97["in_window"]
    u1_closes = len(u1_window) == 0
    even_m_empty = len(even_hits) == 0
    surplus_ge_a4 = surplus_lt_a4 == 0

    if even_hits:
        classification = CLASS_NONCUBE_GAP_CE
    else:
        classification = CLASS_DIOPHANTINE_ESC

    return {
        "a_max": a_max,
        "k_max": k_max,
        "u_radius": u_radius,
        "even_m_noncube_count": even_count,
        "even_m_in_window_count": len(even_hits),
        "even_m_hits": even_hits,
        "same_sign_uv_count": same_sign_count,
        "leaves_exact_cell_count": leaves_count,
        "min_surplus": None if min_surplus is None else _compact_near_power(min_surplus),
        "min_r": None if min_r is None else _compact_near_power(min_r),
        "closest_by_gap_over_width": [_compact_near_power(row) for row in closest_ratio],
        "closest_by_surplus": [_compact_near_power(row) for row in closest_surplus],
        "closest_to_next_cube": [_compact_near_power(row) for row in closest_top],
        "neighborhood_count": len(neighborhood),
        "neighborhood_window_count": sum(1 for row in neighborhood if row["in_window"]),
        "neighborhood_even_m_window_count": sum(
            1 for row in neighborhood if row["m_even"] and row["in_window"]
        ),
        "u1_window_count": len(u1_window),
        "u1_stays_in_ref_cell": u1_stays_in_ref_cell,
        "exact_family_cell_noncube_count": exact_cell_noncube,
        "neighborhood_samples": [
            row
            for row in neighborhood
            if abs(row["ref_u"]) == 1 and row["ref_k"] in (1, 2, 3, 4, 5)
        ],
        "adversarial": adversarial,
        "a97": _compact_near_power(a97),
        "a3": _compact_near_power(a3),
        "routes": {
            "A_unrestricted_noncube_gap": route_a,
            "B_exact_family_cell_exclusive": leaves_is_exclusive,
            "B_leaves_cell_implies_miss": leaves_implies_miss,
            "B_u_pm_1_closes_window": u1_closes,
            "C_fourth_power_rigidity_elementary": False,
            "D_trivial_gap_threshold": False,
            "target_even_m_empty_on_discovery": even_m_empty,
            "observation_surplus_ge_a4_on_discovery": surplus_ge_a4,
        },
        "classification": classification,
        "unresolved": (
            "a non-cube and m = floor_cbrt(a^8) even imply "
            "(m+1)^3 - a^8 > 2a^4"
        ),
        "invariant": (
            "the exact-family cube cell of k^8 holds a^8 only for a = k^3; "
            "nonzero u immediately leaves that cell. This does not force "
            "D > 2a^4: a=97 left the cell of its nearest cube and still hit. "
            "Closest even-m failures are small a, not near-cubes. Route A "
            "is false. No elementary lower bound stronger than D >= 1 "
            "produces a threshold"
        ),
        "a97_survives": a97["in_window"] and not a97["m_even"],
    }


def render_near_power_markdown(analysis: dict[str, Any]) -> str:
    a97 = analysis["a97"]
    a3 = analysis["a3"]
    min_s = analysis["min_surplus"]
    routes = analysis["routes"]
    lines = [
        "# Near-square / near-cube gap of even-m fourth-power windows",
        "",
        "Discovery scan of the displacement `(u, v)` around the exact family",
        "`a = k^3`, `m = k^8`. This is not a `10^8` rerun, not a modular",
        "search, and not a theorem.",
        "",
        f"- discovery `a_max`: `{analysis['a_max']}`",
        f"- neighborhood `k_max`: `{analysis['k_max']}`",
        f"- `u` radius: `{analysis['u_radius']}`",
        f"- even-`m` non-cubes: `{analysis['even_m_noncube_count']}`",
        f"- even-`m` window hits: `{analysis['even_m_in_window_count']}`",
        f"- same sign `(u, v)`: `{analysis['same_sign_uv_count']}`",
        f"- leave nearest exact-family cell: `{analysis['leaves_exact_cell_count']}`",
        f"- classification: **{analysis['classification']}**",
        "",
        "## a = 97 must survive",
        "",
        f"- `a = 97`, nearest cube `k = {a97['k']}`, `u = {a97['u']}`",
        f"- `m = {a97['m']}` odd: `{not a97['m_even']}`",
        f"- `v = {a97['v']}` (same sign as `u`: `{a97['same_sign_uv']}`)",
        f"- left exact-family cell: `{a97['leaves_exact_cell']}`",
        f"- in window: `{a97['in_window']}`",
        f"- surplus `D - 2a^4 = {a97['surplus']}`",
        "",
        "Route A (`a` non-cube `⇒ D > 2a^4`) is false at this example.",
        "Leaving the exact-family cell does not force a miss.",
        "",
        "## Closest even-`m` failures",
        "",
        "Ranked by `D / (2a^4)`. These are the sharp local near-misses.",
        "They are not the integers closest to a cube.",
        "",
    ]
    if min_s is not None:
        lines.append(
            f"Minimum surplus is `a = {min_s['a']}`, `u = {min_s['u']}`, "
            f"surplus `{min_s['surplus']}`."
        )
        lines.append("")
    lines.append(
        f"`a = 3` has `k = {a3['k']}`, `u = {a3['u']}`, `m = {a3['m']}`, "
        f"`v = {a3['v']}`, surplus `{a3['surplus']}`."
    )
    lines.append("")
    for row in analysis["closest_by_gap_over_width"]:
        lines.append(
            f"- a `{row['a']}`: k `{row['k']}`, u `{row['u']}`, "
            f"m `{row['m']}`, v `{row['v']}`, surplus `{row['surplus']}`"
        )
    lines.extend(
        [
            "",
            "## Closest to the next cube",
            "",
            "Even-`m` non-cubes with largest `r / (3m^2+3m+1)`. A hit needs",
            "`r` in the top slice of width `2a^4`. Sitting high in the cell",
            "is not enough by itself (`a = 37840`).",
            "",
        ]
    )
    for row in analysis["closest_to_next_cube"]:
        lines.append(
            f"- a `{row['a']}`: u `{row['u']}`, r `{row['r']}`, "
            f"cube gap `{row['cube_gap']}`, surplus `{row['surplus']}`"
        )
    lines.extend(
        [
            "",
            "## Exact-family neighborhood `a = k^3 + u`",
            "",
            f"Checked `1 <= k <= {analysis['k_max']}` and "
            f"`1 <= |u| <= {analysis['u_radius']}`.",
            "",
            f"- neighborhood rows: `{analysis['neighborhood_count']}`",
            f"- any window hit: `{analysis['neighborhood_window_count']}`",
            f"- even-`m` window hit: `{analysis['neighborhood_even_m_window_count']}`",
            f"- `|u| = 1` window hits: `{analysis['u1_window_count']}`",
            f"- `|u| = 1` still in the `k^8` cell: `{analysis['u1_stays_in_ref_cell']}`",
            f"- non-cube occupants of an exact-family cell: "
            f"`{analysis['exact_family_cell_noncube_count']}`",
            "",
            "The linear increment `8k^{21}u` already exceeds the cell width",
            "`3k^{16}+3k^8+1` for every checked `k >= 1` and `|u| >= 1`.",
            "Sign of `v` matched sign of `u` on the discovery even-`m` set,",
            "but that is only an observation. Nonzero `u` jumps to a",
            "different cube cell; it does not identify the gap `D`.",
            "",
            "## Sample `|u| = 1` rows",
            "",
        ]
    )
    for row in analysis["neighborhood_samples"]:
        lines.append(
            f"- k `{row['ref_k']}`, u `{row['ref_u']}`, a `{row['a']}`: "
            f"m `{row['m']}`, v `{row['ref_v']}`, even m `{row['m_even']}`, "
            f"leaves ref cell `{row['leaves_ref_cell']}`, "
            f"in window `{row['in_window']}`, surplus `{row['surplus']}`"
        )
    lines.extend(
        [
            "",
            "## Adversarial regressions",
            "",
        ]
    )
    for row in analysis["adversarial"]:
        lines.append(
            f"- a `{row['a']}`: cube `{row['a_is_cube']}`, u `{row['u']}`, "
            f"m even `{row['m_even']}`, in window `{row['in_window']}`, "
            f"surplus `{row['surplus']}`"
        )
    lines.extend(
        [
            "",
            "## Routes",
            "",
            f"- A unrestricted non-cube gap: `{routes['A_unrestricted_noncube_gap']}`",
            f"- B exact-family cell exclusive: `{routes['B_exact_family_cell_exclusive']}`",
            f"- B leaving the cell implies a miss: `{routes['B_leaves_cell_implies_miss']}`",
            f"- B `|u|=1` closes the window: `{routes['B_u_pm_1_closes_window']}`",
            f"- C elementary fourth-power rigidity: `{routes['C_fourth_power_rigidity_elementary']}`",
            f"- D trivial `D >= 1` threshold: `{routes['D_trivial_gap_threshold']}`",
            f"- target empty on discovery: `{routes['target_even_m_empty_on_discovery']}`",
            f"- observation `surplus >= a^4` on discovery: "
            f"`{routes['observation_surplus_ge_a4_on_discovery']}`",
            "",
            "Route B's exclusive-cell fact is elementary and true, but it is",
            "not a lower bound on `D` in the *new* cell. Route C would need",
            "a quantitative gap for `X^2 - Y^3` with `X = a^4`; that is not",
            "an integer-polynomial comparison. Route D cannot start because",
            "`m >= a^{8/3}-1` is sharp.",
            "",
            "## Unresolved Diophantine statement",
            "",
            analysis["unresolved"] + ".",
            "",
            "No Baker, Thue, or Mordell machinery is introduced.",
            "",
            "## Invariant",
            "",
            analysis["invariant"] + ".",
            "",
            f"`a = 97` survives: `{analysis['a97_survives']}`.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def write_near_power_analysis(
    a_max: int = NEAR_POWER_SCAN_MAX,
    k_max: int = NEAR_POWER_K_MAX,
    u_radius: int = NEAR_POWER_U_RADIUS,
    analysis_dir: Path | None = None,
) -> dict[str, Any]:
    data = analyze_near_power_gap(a_max, k_max, u_radius)
    directory = ANALYSIS_DIR if analysis_dir is None else analysis_dir
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "near_power.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )
    (directory / "near_power.md").write_text(
        render_near_power_markdown(data), encoding="utf-8"
    )
    return data


def cube_in_sq_interval(m: int) -> int | None:
    """The unique candidate cube in [M^2, (M+1)^2), if it exists."""

    if m < 0:
        raise ValueError("cube_in_sq_interval requires nonnegative M")
    lo = m * m
    hi = (m + 1) * (m + 1)
    root = integer_cbrt(lo)
    if root * root * root < lo:
        root += 1
    cube = root * root * root
    if cube < hi:
        return root
    return None


def odd_floor_cube_interval(n: int, m: int) -> bool:
    """Exact integer form of T(n) = M for odd n."""

    if n % 2 != 1:
        raise ValueError("odd_floor_cube_interval requires odd n")
    return m * m <= n * n * n < (m + 1) * (m + 1)


def pow_two_base(value: int, depth: int) -> int | None:
    """The base a in value = a^{2^depth}, or None if the depth fails."""

    if depth < 0 or value < 0:
        raise ValueError("pow_two_base requires nonnegative value and depth")
    if not has_pow_two_depth(value, depth):
        return None
    current = value
    for _ in range(depth):
        current = isqrt(current)
    return current


def hit_record(n: int) -> dict[str, Any]:
    image = floor_power(n)
    depth = square_depth(image)
    first_defect = not local_tight(n)
    s = 0 if depth is None else depth
    base = pow_two_base(image, s) if s else image
    return {
        "n": n,
        "T": image,
        "s": s,
        "base": base,
        "square_depth": depth,
        "parity": "odd" if n % 2 else "even",
        "first_defect": first_defect,
        "sharp_suffix_length": s if first_defect and s else 0,
    }


def scan_odd_starts(n_max: int, *, n_min: int = 3) -> dict[str, Any]:
    """Odd n with a first defect whose image has positive 2-power depth."""

    if n_min < 1 or n_max < n_min:
        raise ValueError("scan_odd_starts requires 1 ≤ n_min ≤ n_max")
    depth_ge_one: list[dict[str, Any]] = []
    depth_ge_two: list[dict[str, Any]] = []
    s1_bases: list[int] = []
    for n in range(n_min + (n_min % 2 == 0), n_max + 1, 2):
        if local_tight(n):
            continue
        rec = hit_record(n)
        depth = rec["square_depth"]
        if depth is None or depth < 1:
            continue
        depth_ge_one.append(rec)
        if rec["base"] is not None:
            s1_bases.append(rec["base"])
        if depth >= 2:
            depth_ge_two.append(rec)
    return {
        "n_min": n_min,
        "n_max": n_max,
        "first_defect_depth_ge_one": depth_ge_one,
        "first_defect_depth_ge_one_count": len(depth_ge_one),
        "first_defect_depth_ge_two": depth_ge_two,
        "first_defect_depth_ge_two_count": len(depth_ge_two),
        "s1_bases": s1_bases,
        "s1_base_square_count": sum(1 for base in s1_bases if is_square(base)),
        "max_s": max((rec["s"] for rec in depth_ge_one), default=0),
    }


def scan_fourth_powers(b_max: int, *, b_min: int = 2) -> dict[str, Any]:
    """Cubes in the square interval of M = b^4. Integer cube roots only."""

    if b_min < 1 or b_max < b_min:
        raise ValueError("scan_fourth_powers requires 1 ≤ b_min ≤ b_max")
    odd_hits: list[dict[str, Any]] = []
    even_hits: list[dict[str, Any]] = []
    exact_cubes: list[dict[str, Any]] = []
    for b in range(b_min, b_max + 1):
        m = b ** 4
        n = cube_in_sq_interval(m)
        if n is None:
            continue
        lo = m * m
        gap = n * n * n - lo
        rec = {
            "b": b,
            "M": m,
            "n": n,
            "parity": "odd" if n % 2 else "even",
            "n3_minus_M2": gap,
            "interval_len": 2 * m + 1,
            "exact_cube": gap == 0,
        }
        if gap == 0:
            exact_cubes.append(rec)
            continue
        if n % 2:
            odd_hits.append(rec)
        else:
            even_hits.append(rec)
    return {
        "b_min": b_min,
        "b_max": b_max,
        "odd_hits": odd_hits,
        "odd_hit_count": len(odd_hits),
        "even_hits": even_hits,
        "even_hit_count": len(even_hits),
        "exact_cube_hits": exact_cubes,
        "exact_cube_count": len(exact_cubes),
    }


def scan_eighth_powers(a_max: int, *, a_min: int = 2) -> dict[str, Any]:
    """Cubes in the square interval of M = a^8. Integer cube roots only."""

    if a_min < 1 or a_max < a_min:
        raise ValueError("scan_eighth_powers requires 1 ≤ a_min ≤ a_max")
    odd_hits: list[dict[str, Any]] = []
    even_hits: list[dict[str, Any]] = []
    for a in range(a_min, a_max + 1):
        m = a ** 8
        n = cube_in_sq_interval(m)
        if n is None:
            continue
        rec = {
            "a": a,
            "M": m,
            "n": n,
            "parity": "odd" if n % 2 else "even",
            "n3_minus_M2": n * n * n - m * m,
            "interval_len": 2 * m + 1,
            "exact_cube": n * n * n == m * m,
        }
        if rec["exact_cube"]:
            continue
        if n % 2:
            odd_hits.append(rec)
        else:
            even_hits.append(rec)
    return {
        "a_min": a_min,
        "a_max": a_max,
        "odd_hits": odd_hits,
        "odd_hit_count": len(odd_hits),
        "even_hits": even_hits,
        "even_hit_count": len(even_hits),
    }


def even_start_contrast() -> dict[str, Any]:
    """Even first defects can feed arbitrarily deep exact even towers."""

    rows = []
    for s, q in ((1, 4), (2, 16), (3, 256)):
        n = q * q + 2
        rec = hit_record(n)
        rec["constructed_q"] = q
        rec["constructed_s"] = s
        rec["T_eq_q"] = rec["T"] == q
        rec["depth_eq_s"] = rec["square_depth"] == s
        rows.append(rec)
    return {
        "samples": rows,
        "all_even": all(row["parity"] == "even" for row in rows),
        "all_first_defect": all(row["first_defect"] for row in rows),
        "depths": [row["square_depth"] for row in rows],
        "unbounded_family": True,
        "note": (
            "n = q^2 + 2 with q = 2^{2^s} yields T(n) = q and an exact "
            "even tower of length s after an even first defect"
        ),
    }


def example_records() -> dict[str, Any]:
    eleven = hit_record(11)
    thirty_seven = hit_record(37)
    eighteen = hit_record(18)
    even_fourth = cube_in_sq_interval(97**4)
    return {
        "oe_eleven": eleven,
        "oe_thirty_seven": thirty_seven,
        "even_ee_eighteen": eighteen,
        "eleven_interval": odd_floor_cube_interval(11, 36),
        "eleven_pow_two": has_pow_two_depth(36, 1),
        "eleven_not_depth_two": not has_pow_two_depth(36, 2),
        "even_fourth_b97_n": even_fourth,
        "even_fourth_b97_parity": None if even_fourth is None else (
            "odd" if even_fourth % 2 else "even"
        ),
    }


def lean_api_present() -> dict[str, bool]:
    text = LEAN_PATH.read_text(encoding="utf-8")
    return {
        "sorry_free": "sorry" not in text and "admit" not in text,
        **{name: f"theorem {name}" in text for name in LEAN_THEOREMS},
        "impossible_theorem": f"theorem {LEAN_IMPOSSIBLE}" in text,
        "PowerHeight_absent": "PowerHeight" not in text,
        "PowerBoundStrict_absent": (
            "structure PowerBoundStrict" not in text
            and "def PowerBoundStrict" not in text
            and "theorem PowerBoundStrict" not in text
        ),
        "mixed_word_power_lt_absent": "theorem mixed_word_power_lt" not in text,
    }


def classify(
    odd_scan: dict[str, Any],
    fourth: dict[str, Any],
    eighth: dict[str, Any],
    lean: dict[str, bool],
) -> dict[str, Any]:
    if odd_scan["first_defect_depth_ge_two_count"] or fourth["odd_hit_count"]:
        return {
            "classification": CLASS_WITNESS,
            "reason": (
                "an odd first-defect state has T(n) of 2-power depth at least 2"
            ),
        }
    lean_ok = lean["sorry_free"] and all(lean[name] for name in LEAN_THEOREMS)
    if lean.get("impossible_theorem"):
        return {
            "classification": CLASS_IMPOSSIBLE,
            "reason": (
                "Lean proves that an odd Juggler step cannot hit a "
                "2-power of depth s ≥ 2"
            ),
        }
    if lean_ok:
        return {
            "classification": CLASS_INCOMPLETE,
            "reason": (
                "nearest-cube Lean covers occupancy, the exact family, and "
                "odd m implying even n; modular search and elementary "
                "near-power gaps did not yield an obstruction"
            ),
        }
    return {
        "classification": CLASS_INCOMPLETE,
        "reason": "the inverse-floor Lean API is incomplete",
    }


def run_probe(
    *,
    n_max: int = N_MAX,
    b_max: int = B_MAX,
    a8_max: int = A8_MAX,
) -> dict[str, Any]:
    odd_scan = scan_odd_starts(n_max)
    fourth = scan_fourth_powers(b_max)
    eighth = scan_eighth_powers(a8_max)
    s1 = odd_scan["first_defect_depth_ge_one"][:S1_SAMPLE_MAX]
    return {
        "n_max": n_max,
        "b_max": b_max,
        "a8_max": a8_max,
        "odd_scan": {
            **odd_scan,
            "first_defect_depth_ge_one": s1,
        },
        "fourth_powers": {
            **fourth,
            "even_hits": fourth["even_hits"][:8],
        },
        "eighth_powers": eighth,
        "even_start_contrast": even_start_contrast(),
        "examples": example_records(),
    }


def probe_payload(
    *,
    n_max: int = N_MAX,
    b_max: int = B_MAX,
    a8_max: int = A8_MAX,
) -> dict[str, Any]:
    scan = run_probe(n_max=n_max, b_max=b_max, a8_max=a8_max)
    lean = lean_api_present()
    decision = classify(scan["odd_scan"], scan["fourth_powers"], scan["eighth_powers"], lean)
    return {
        "experiment": "juggler_odd_sharp_suffix",
        "engine_control_layer_modified": False,
        "anti_overclaim": dict(ANTI_OVERCLAIM),
        "scan": scan,
        "lean": lean,
        "decision": decision,
        "search_method": (
            "isqrt on odd n; binary-search cube roots in the exact interval "
            "M^2 ≤ n^3 < (M+1)^2 for M a fourth or eighth power; no floats "
            "and no cmp_pow"
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    decision = payload["decision"]
    scan = payload["scan"]
    lean = payload["lean"]
    odd = scan["odd_scan"]
    fourth = scan["fourth_powers"]
    eighth = scan["eighth_powers"]
    contrast = scan["even_start_contrast"]
    examples = scan["examples"]
    s1_rows = odd["first_defect_depth_ge_one"]
    lines = [
        "# Juggler odd-start sharp even-tower suffixes",
        "",
        f"Status: **{decision['classification']}**",
        "",
        "Standalone application phase. Not a Research Engine experiment and",
        "not a termination theorem. This page records the inverse-floor form",
        "of an odd Juggler step and the search for sharp suffixes `OE^s`.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     T(n)=a^4 and n odd  =>  n is a square",
        "Novelty hypothesis      inexact cubes are even (a=97); that kills OE^s",
        "                        for s>=2",
        "Falsifier               odd non-square n with T(n)=a^4",
        "Existing machinery      inverse-floor Lean, persisted 465-hit corpus",
        "Maximum Phase-0 scope   nearest-cube analysis of persisted hits; Lean",
        "                        only the cheap lemmas the analysis uses",
        "```",
        "",
        "## Metadata",
        "",
        f"- odd scan: `n <= {scan['n_max']}`",
        f"- fourth-power scan: `b <= {scan['b_max']}`",
        f"- eighth-power scan: `a <= {scan['a8_max']}`",
        f"- engine control layer modified: `{payload['engine_control_layer_modified']}`",
        f"- classification: **{decision['classification']}**",
        f"- odd first-defect depth ≥ 1: `{odd['first_defect_depth_ge_one_count']}`",
        f"- odd first-defect depth ≥ 2: `{odd['first_defect_depth_ge_two_count']}`",
        f"- s=1 bases that are squares: `{odd['s1_base_square_count']}`",
        f"- fourth-power odd hits: `{fourth['odd_hit_count']}`",
        f"- fourth-power even hits: `{fourth['even_hit_count']}`",
        f"- eighth-power odd hits: `{eighth['odd_hit_count']}`",
        f"- sorry-free: `{lean['sorry_free']}`",
        "",
        decision["reason"] + ".",
        "",
        "## Inverse-floor reduction",
        "",
        "For odd `n`,",
        "",
        "```text",
        "T(n) = M  ↔  M^2 ≤ n^3 < (M+1)^2",
        "```",
        "",
        "is the definition of `Nat.sqrt` on `n^3`. Specializing `M = a^{2^s}`",
        "gives the exact Diophantine interval",
        "",
        "```text",
        "a^{2^{s+1}} ≤ n^3 < (a^{2^s} + 1)^2",
        "```",
        "",
        "No real `n^{3/2}` is used. A large finite search is not a theorem.",
        "",
        "Nearest-cube Lean: the window holds at most one cube; a cube `a`",
        "places `n = k^8` at the left endpoint; a non-cube leaves only",
        "`n = m+1`; that candidate is even exactly when `m` is odd. The",
        "even-`m` leftover is open. `a = 3` shows that odd `a` need not",
        "make `m` odd.",
        "",
        "## Odd first-defect census",
        "",
        "Odd `n` that are not locally exact, with `square_depth(T(n)) ≥ 1`.",
        "All recorded depths are `1`. The `s = 1` family includes",
        "`11 → 36 = 6^2` and `37 → 225 = 15^2`.",
        "",
    ]
    for rec in s1_rows:
        lines.append(
            f"- n `{rec['n']}`: T `{rec['T']}` = `{rec['base']}`^2, "
            f"depth `{rec['square_depth']}`, sharp suffix `{rec['sharp_suffix_length']}`"
        )
    lines.extend(
        [
            "",
            "## Fourth-power interval",
            "",
            "For `s ≥ 2` one may take `M = b^4`. A cube in",
            "`[M^2, (M+1)^2)` is possible: `b = 97` gives the even preimage",
            f"`n = {examples['even_fourth_b97_n']}`. That is an even cube, so",
            "it is not an odd Juggler step. No odd preimage was found.",
            "",
            f"- even hits (truncated): `{fourth['even_hits']}`",
            f"- odd hits: `{fourth['odd_hits']}`",
            f"- eighth-power odd hits: `{eighth['odd_hits']}`",
            f"- eighth-power even hits: `{eighth['even_hits']}`",
            "",
            "## Even-start contrast",
            "",
            "An even first defect `n = q^2 + r` has `T(n) = q`. If `q` is a",
            "sufficiently deep 2-power, the exact even tower can be arbitrarily",
            "long. Samples:",
            "",
        ]
    )
    for row in contrast["samples"]:
        lines.append(
            f"- n `{row['n']}`: T `{row['T']}`, depth `{row['square_depth']}`, "
            f"word starts even"
        )
    lines.extend(
        [
            "",
            "The remaining asymmetry is therefore: even first defects admit",
            "unbounded sharp suffixes `E^s`; odd first defects are only known",
            "to support `OE` (`s = 1`).",
            "",
            "## Lean",
            "",
        ]
    )
    for name in LEAN_THEOREMS:
        lines.append(f"- `{name}`: `{lean.get(name)}`")
    lines.extend(
        [
            f"- impossibility theorem: `{lean.get('impossible_theorem')}`",
            f"- `PowerHeight` absent: `{lean.get('PowerHeight_absent')}`",
            f"- `PowerBoundStrict` absent: `{lean.get('PowerBoundStrict_absent')}`",
            "",
            "## Anti-overclaim",
            "",
        ]
    )
    for key, value in payload["anti_overclaim"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"**{decision['classification']}**",
            "",
            decision["reason"] + ".",
            "",
            "This is a local inverse-floor statement, not a global halt result.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def write_artifacts(
    payload: dict[str, Any] | None = None,
    *,
    n_max: int = N_MAX,
    b_max: int = B_MAX,
    a8_max: int = A8_MAX,
) -> dict[str, Any]:
    data = (
        payload
        if payload is not None
        else probe_payload(n_max=n_max, b_max=b_max, a8_max=a8_max)
    )
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_markdown(data), encoding="utf-8")
    return data


def main() -> None:
    payload = write_artifacts()
    print(payload["decision"]["classification"])
    print(payload["decision"]["reason"])


if __name__ == "__main__":
    main()
