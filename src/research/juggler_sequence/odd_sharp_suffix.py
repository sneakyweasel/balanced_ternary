"""Odd-start sharp even-tower suffixes.

Not a Research Engine control-layer experiment. Search uses integer
roots only: isqrt and binary-search cube roots. No n^{3/2} construction,
no cmp_pow census, and not a termination theorem.
"""

from __future__ import annotations

import json
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
                "the inverse-floor reduction is Lean-verified and no odd "
                "s ≥ 2 hit was found, but a finite-search empty set is not "
                "an impossibility theorem"
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
        "Mathematical target     Can odd n have T(n)=a^{2^s} for unbounded s",
        "                        (sharp OE^s)?",
        "Novelty hypothesis      s≥2 is impossible, or a finite exceptional",
        "                        family, or an infinite odd family",
        "Falsifier               An odd n with square_depth(T(n))≥2, or a failed",
        "                        obstruction",
        "Existing machinery      localDefectOdd, power_deficit_eq_local_odd_iff,",
        "                        HasPowTwoDepth, isqrt",
        "Maximum Phase-0 scope   Inverse-floor lemma; integer-root search past",
        "                        2000; smallest s≥2 obstruction or witness",
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
