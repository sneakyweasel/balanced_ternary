"""Cycle finance inequality for the Juggler floor-power map.

Not a halt theorem, not an escape statement, not a corridor
extension, and not a windowed population census.

A hypothetical cycle word is formally expanding (2^L < 3^o) yet the
orbit returns exactly, so the multiplicative surplus is financed by
floor defects, which are relatively O(1/x) in logarithms. The
dossier docs/problems/juggler_cycle_finance.md proves

    1 - 2^L/3^o  <=  (6/5) * sum 1/(x_i ln x_i)  <=  (6/5) L/(n ln n)

for any cycle with all states >= 12, hence

    n ln n  <=  (6/5) * L * 3^o / (3^o - 2^L),

worst at the minimal admissible o. Phase 0 tabulates the resulting
per-length minimum bound n_max(L) exactly for L <= 10^5, verifies a
descent-induction floor (every n <= N0 reaches 1), and stress-tests
the per-step bound eps_i <= (6/5)/x_{i+1} on real orbit segments.
A verified floor N0 excludes every length with n_max(L) <= N0.
Lean: CycleFinance.lean (cycleMin_finance, no_cycle_word_length_le_eighteen,
cycle_word_length_nineteen_or_ge_thirty, cycle_word_eliahou_leftover).
Eliahou leftover: period 19, or a listed near-convergent, or >= 10^5.
"""

from __future__ import annotations

import json
import math
import subprocess
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

from research.juggler_sequence.lean_paths import (
    CYCLE_FINANCE,
    JUGGLER_DIR,
    JUGGLER_PAPER_BARREL,
    has_named,
    juggler_text,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "juggler_cycle_finance.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "juggler_cycle_finance.md"
DATA_DIR = REPO_ROOT / "data" / "research" / "juggler" / "cycle_finance"

CLASS_GREEN = "CYCLE_FINANCE_GREEN"
CLASS_PARK = "CYCLE_FINANCE_PARK"
CLASS_CLOSED = "CYCLE_FINANCE_CLOSED"
CLASS_INCOMPLETE = "CYCLE_FINANCE_INCOMPLETE"

EPS_CONST = 1.2  # -ln(1-d) <= (6/5) d on [0, 1/6]
MIN_STATE = 12  # Lean reachesOne_of_lt_twelve: every n <= 11 reaches 1
LEAN_FLOOR = 11

SCIENCE_L_MAX = 100_000
SCIENCE_FLOOR = 1_000_000
SCIENCE_SEEDS = (25, 27, 37, 365, 1999, 30817, 1_000_003)
TEST_L_MAX = 400
TEST_FLOOR = 2_000
TEST_SEEDS = (25, 37, 365)

REPORT_FLOORS = (11, 1_000, 1_000_000, 10**9)
GREEN_PREFIX = 100
STEP_CAP = 100_000
BIT_CAP = 10_000_000
EXCEPTION_LIST_CAP = 500
ELIAHOU_TABLE_CUTOFF = 100_000
ELIAHOU_LEAN_PERIOD = 19

# L <= 8 with n_max(L) <= 11: finance + the Lean residual floor kill
# these lengths without the census; {3, 6} stay census-only.
EXPECTED_LEAN_KILL = (1, 2, 4, 5, 7, 8)

EXISTING_LEAN = (
    "cycle_word_formally_expanding",
    "global_defect_identity",
    "no_cycle_word_length_le_eight",
    "reachesOne_of_lt_twelve",
    "cycle_peak_finance",
    "cycleMin_finance",
    "cycle_finance_min_thirteen",
    "no_cycle_word_length_le_ten",
    "cycle_word_length_eleven_or_ge_fourteen",
    "reachesOne_of_lt_fifty_three",
    "cycle_finance_min_fifty_three",
    "finance_excludes_length_eleven",
    "no_cycle_word_length_le_eleven",
    "cycle_word_length_ge_fourteen",
    "finance_excludes_length_fourteen",
    "no_cycle_word_length_le_eighteen",
    "cycle_word_length_nineteen_or_ge_thirty",
    "cycle_word_length_nineteen_or_ge_twenty",
    "eliahouTableCutoff",
    "EliahouLeftover",
    "EliahouTable",
    "cycle_word_eliahou_leftover",
)

FORBIDDEN_THEOREMS = (
    "juggler_reaches_one",
    "no_cycle_word_any_length",
    "no_juggler_escape",
    "no_cycle_word_length_eleven",
)

FORBIDDEN_NEW_API = (
    "FinanceInequality",
    "FinanceBound",
)

REQUIRED_LEAN_FILES = (CYCLE_FINANCE,)
FORBIDDEN_LEAN_FILES = (JUGGLER_DIR / "Finance.lean",)
PAPER_FORBIDDEN = ("CycleFinance", "FinanceInequality", "FinanceBound")


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def n_max_from_bound(bound: float) -> int:
    """Largest n >= 1 with n*ln(n) <= bound. Conservative upward margin."""

    bound = bound * (1.0 + 1e-9) + 1.0
    if 2 * math.log(2) > bound:
        return 1
    hi = 4
    while hi * math.log(hi) <= bound:
        hi *= 2
    lo = 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid * math.log(mid) <= bound:
            lo = mid
        else:
            hi = mid - 1
    return lo


def finance_rows(l_max: int) -> list[dict[str, Any]]:
    """Exact table L -> (o_min, theta, bound B, n_max). Bignum only.

    theta = (3^o - 2^L)/3^o = 1 - 2^L/3^o at the minimal admissible o.
    """

    rows: list[dict[str, Any]] = []
    pow2 = 1
    pow3 = 1
    o = 0
    best_theta = math.inf
    for length in range(1, l_max + 1):
        pow2 <<= 1
        while pow3 <= pow2:
            pow3 *= 3
            o += 1
        theta = (pow3 - pow2) / pow3
        bound = EPS_CONST * length / theta
        record = theta < best_theta
        if record:
            best_theta = theta
        rows.append(
            {
                "L": length,
                "o": o,
                "theta": theta,
                "bound": bound,
                "n_max": n_max_from_bound(bound),
                "record": record,
            }
        )
    return rows


def eliahou_leftover(
    length: int,
    exceptions: list[int] | tuple[int, ...] | set[int],
    *,
    cutoff: int = ELIAHOU_TABLE_CUTOFF,
) -> bool:
    """Eliahou leftover: period 19, listed near-convergent, or >= cutoff."""

    return (
        length == ELIAHOU_LEAN_PERIOD
        or length in exceptions
        or cutoff <= length
    )


def eliahou_exceptions(
    rows: list[dict[str, Any]],
    floor: int,
) -> list[int]:
    """Lengths whose finance n_max exceeds the verified floor."""

    return [row["L"] for row in rows if row["n_max"] > floor]


def eliahou_table_holds(
    rows: list[dict[str, Any]],
    floor: int,
    exceptions: list[int] | tuple[int, ...] | set[int],
    *,
    cutoff: int = ELIAHOU_TABLE_CUTOFF,
) -> bool:
    """Every L in [30, cutoff) outside exceptions has n_max <= floor."""

    exception_set = set(exceptions)
    for row in rows:
        length = row["L"]
        if 30 <= length < cutoff and length not in exception_set:
            if row["n_max"] > floor:
                return False
    return True


def eliahou_packaging(
    rows: list[dict[str, Any]],
    floor: int,
    *,
    cutoff: int = ELIAHOU_TABLE_CUTOFF,
) -> dict[str, Any]:
    """Theorem-shaped leftover from the existing finance table."""

    exceptions = eliahou_exceptions(rows, floor)
    nineteen = next((row for row in rows if row["L"] == ELIAHOU_LEAN_PERIOD), None)
    return {
        "lean_period": ELIAHOU_LEAN_PERIOD,
        "cutoff": cutoff,
        "exceptions": exceptions,
        "exception_count": len(exceptions),
        "table_holds": eliahou_table_holds(
            rows, floor, exceptions, cutoff=cutoff
        ),
        "nineteen_computationally_excluded": (
            nineteen is not None and nineteen["n_max"] <= floor
        ),
    }


def exception_summary(
    rows: list[dict[str, Any]],
    floors: tuple[int, ...] = REPORT_FLOORS,
) -> list[dict[str, Any]]:
    """Per floor: lengths whose finance bound exceeds the floor."""

    out = []
    for floor in floors:
        exceptions = [row["L"] for row in rows if row["n_max"] > floor]
        first = exceptions[0] if exceptions else None
        out.append(
            {
                "floor": floor,
                "count": len(exceptions),
                "first_exception": first,
                "contiguous_prefix": (first - 1) if first else rows[-1]["L"],
                "lengths": exceptions[:EXCEPTION_LIST_CAP],
                "truncated": len(exceptions) > EXCEPTION_LIST_CAP,
            }
        )
    return out


def census_cross_check(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare finance + Lean floor against the length-<=8 Lean census."""

    small = {row["L"]: row["n_max"] for row in rows if row["L"] <= 8}
    killed = tuple(sorted(length for length, nm in small.items() if nm <= LEAN_FLOOR))
    return {
        "n_max_by_length": small,
        "killed_by_lean_floor": killed,
        "matches_expected": killed == EXPECTED_LEAN_KILL,
        "census_only_lengths": tuple(
            sorted(set(small) - set(killed))
        ),
    }


def verify_floor(
    n_top: int,
    *,
    step_cap: int = STEP_CAP,
    bit_cap: int = BIT_CAP,
) -> dict[str, Any]:
    """Descent induction: every 2 <= n <= n_top has an iterate < n.

    By strong induction (base n=2 -> 1) every such n reaches 1.
    Exact integer arithmetic; failures list is expected empty.
    """

    max_steps = 0
    max_bits = 0
    hardest = 0
    failures: list[int] = []
    for n in range(2, n_top + 1):
        x = n
        steps = 0
        ok = True
        while x >= n:
            if x % 2 == 0:
                x = isqrt(x)
            else:
                x = isqrt(x * x * x)
            steps += 1
            bits = x.bit_length()
            if bits > max_bits:
                max_bits = bits
            if steps > step_cap or bits > bit_cap:
                failures.append(n)
                ok = False
                break
        if ok and steps > max_steps:
            max_steps = steps
            hardest = n
    return {
        "n_top": n_top,
        "verified": not failures,
        "failures": failures[:20],
        "max_first_passage_steps": max_steps,
        "hardest_seed": hardest,
        "max_bits_seen": max_bits,
    }


def orbit_slack(seed: int, *, max_steps: int = 400) -> dict[str, Any]:
    """Per-step finance bookkeeping along a real orbit segment.

    Checks the exact step identity x'^2 = x^e - d with 0 <= d <= 2x',
    the relative bound eps <= (6/5)/x' for states >= 12, and the
    unrolled identity t_k = P_k (t_0 - sum eps_i / P_{i+1}).
    """

    x = seed
    t0 = math.log(seed)
    partial = Fraction(1)
    eps_sum_scaled = 0.0
    steps = 0
    checked = 0
    step_ok = True
    d_ok = True
    worst_margin = math.inf
    identity_err = 0.0
    eps_over_t = 0.0
    bound_over_t = 0.0
    d_ratio_sum = 0.0
    for _ in range(max_steps):
        if x < 2:
            break
        exponent = 1 if x % 2 == 0 else 3
        power = x if exponent == 1 else x * x * x
        nxt = isqrt(power)
        defect = power - nxt * nxt
        if not 0 <= defect <= 2 * nxt:
            d_ok = False
        delta = defect / power
        eps = -0.5 * math.log1p(-delta)
        if nxt >= MIN_STATE:
            checked += 1
            # 1/nxt via logs: nxt may exceed float range.
            inv_nxt = math.exp(-math.log(nxt))
            ratio = eps / (EPS_CONST * inv_nxt) if inv_nxt > 0.0 else 0.0
            worst_margin = min(worst_margin, 1.0 - ratio)
            if ratio > 1.0 + 1e-9:
                step_ok = False
            t_next = math.log(nxt)
            eps_over_t += eps / t_next
            bound_over_t += EPS_CONST * inv_nxt / t_next
            d_ratio_sum += defect / (2 * nxt)
        partial *= Fraction(exponent, 2)
        eps_sum_scaled += eps / float(partial)
        steps += 1
        if nxt > 1:
            predicted = float(partial) * (t0 - eps_sum_scaled)
            actual = math.log(nxt)
            scale = max(abs(actual), 1.0)
            identity_err = max(identity_err, abs(predicted - actual) / scale)
        x = nxt
    return {
        "seed": seed,
        "steps": steps,
        "checked_states": checked,
        "reached_one": x < 2,
        "step_bound_ok": step_ok,
        "defect_bound_ok": d_ok,
        "worst_margin": None if worst_margin is math.inf else worst_margin,
        "identity_rel_err": identity_err,
        "tightness": (eps_over_t / bound_over_t) if bound_over_t else None,
        "mean_defect_ratio": (d_ratio_sum / checked) if checked else None,
    }


def lean_api_present() -> dict[str, bool]:
    combined = juggler_text()
    named = {name: has_named(combined, name) for name in EXISTING_LEAN}
    forbidden = {
        f"has_{name}": has_named(combined, name) for name in FORBIDDEN_THEOREMS
    }
    paper = JUGGLER_PAPER_BARREL.read_text(encoding="utf-8")
    return {
        "sorry_free": "sorry" not in combined and "admit" not in combined,
        **named,
        **forbidden,
        **{
            f"has_api_{name}": has_named(combined, name)
            for name in FORBIDDEN_NEW_API
        },
        "cycle_finance_present": all(
            path.is_file() for path in REQUIRED_LEAN_FILES
        ),
        "no_extra_finance_file": not any(
            path.is_file() for path in FORBIDDEN_LEAN_FILES
        ),
        "not_in_paper_barrel": all(name not in paper for name in PAPER_FORBIDDEN),
    }


def run_probe(
    *,
    l_max: int = TEST_L_MAX,
    floor: int = TEST_FLOOR,
    seeds: tuple[int, ...] = TEST_SEEDS,
) -> dict[str, Any]:
    rows = finance_rows(l_max)
    floors = tuple(sorted(set(REPORT_FLOORS) | {floor}))
    exceptions = exception_summary(rows, floors)
    census = census_cross_check(rows)
    floor_check = verify_floor(floor)
    slack = [orbit_slack(seed) for seed in seeds]
    records = [
        {key: row[key] for key in ("L", "o", "theta", "n_max")}
        for row in rows
        if row["record"]
    ]
    achieved = next(item for item in exceptions if item["floor"] == floor)
    leftover = eliahou_packaging(rows, floor, cutoff=min(l_max, ELIAHOU_TABLE_CUTOFF))
    return {
        "l_max": l_max,
        "floor": floor,
        "floor_check": floor_check,
        "records": records,
        "exceptions": exceptions,
        "eliahou": leftover,
        "achieved": achieved,
        "census": census,
        "slack": slack,
        "git": git_commit(),
        "halt_theorem": False,
        "no_cycle_all_lengths": False,
        "escape_claim": False,
        "corridor_extension": False,
        "population_census_reopen": False,
    }


def classify(scan: dict[str, Any], lean: dict[str, bool]) -> dict[str, Any]:
    lean_ok = (
        lean["sorry_free"]
        and all(lean[name] for name in EXISTING_LEAN)
        and not any(lean[f"has_{name}"] for name in FORBIDDEN_THEOREMS)
        and not any(lean[f"has_api_{name}"] for name in FORBIDDEN_NEW_API)
        and lean["cycle_finance_present"]
        and lean["no_extra_finance_file"]
        and lean["not_in_paper_barrel"]
    )
    if not lean_ok:
        return {"classification": CLASS_INCOMPLETE, "reason": f"lean_ok={lean_ok}"}
    if scan["halt_theorem"] or scan["no_cycle_all_lengths"]:
        return {
            "classification": CLASS_INCOMPLETE,
            "reason": "out-of-scope claim",
        }
    slack_ok = all(
        row["step_bound_ok"] and row["defect_bound_ok"] for row in scan["slack"]
    )
    if not slack_ok:
        return {
            "classification": CLASS_CLOSED,
            "reason": (
                "the per-step bound eps <= (6/5)/x' or the defect bound "
                "d <= 2x' failed on a real orbit segment; the derivation "
                "constant does not hold as stated"
            ),
        }
    floor_ok = scan["floor_check"]["verified"]
    census_ok = scan["census"]["matches_expected"]
    prefix = scan["achieved"]["contiguous_prefix"]
    if floor_ok and census_ok and prefix >= GREEN_PREFIX:
        return {
            "classification": CLASS_GREEN,
            "reason": (
                "per-step finance bounds hold on every measured orbit step; "
                f"descent induction verifies every n <= {scan['floor']} "
                "reaches 1; finance excludes every cycle length "
                f"L <= {prefix} at once, far beyond the length-8 census; "
                "exceptional lengths are exactly the near-convergent ones"
            ),
        }
    if floor_ok and census_ok:
        return {
            "classification": CLASS_PARK,
            "reason": (
                "the inequality holds but the contiguous excluded prefix "
                f"is only {prefix}; the floor is too low for the first "
                "near-convergent length"
            ),
        }
    return {
        "classification": CLASS_PARK,
        "reason": (
            f"floor verified={floor_ok}, census cross-check={census_ok}; "
            "one of the supporting computations is incomplete"
        ),
    }


def probe_payload(
    *,
    l_max: int = TEST_L_MAX,
    floor: int = TEST_FLOOR,
    seeds: tuple[int, ...] = TEST_SEEDS,
) -> dict[str, Any]:
    scan = run_probe(l_max=l_max, floor=floor, seeds=seeds)
    lean = lean_api_present()
    decision = classify(scan, lean)
    return {
        "experiment": "juggler_cycle_finance",
        "engine_control_layer_modified": False,
        "anti_overclaim": {
            "halt_theorem": False,
            "no_cycle_all_lengths": False,
            "escape_claim": False,
            "corridor_extension": False,
            "population_census_reopen": False,
            "lean_finance_added": True,
            "floor_is_lean_verified": False,
        },
        "scan": scan,
        "lean": lean,
        "decision": decision,
        "search_method": (
            f"exact gap table L<={l_max}; descent-induction floor {floor}; "
            f"slack seeds {list(seeds)}"
        ),
    }


def render_markdown(payload: dict[str, Any]) -> str:
    decision = payload["decision"]
    scan = payload["scan"]
    floor_check = scan["floor_check"]
    lines = [
        "# Juggler cycle finance inequality",
        "",
        f"Status: **{decision['classification']}**",
        "",
        "Finance bound n ln n <= (6/5) L 3^o/(3^o - 2^L) on cycle minima.",
        "Not a halt theorem. Not a no-cycle-of-any-length theorem.",
        "The floor is COMPUTATIONALLY VERIFIED, not Lean.",
        "",
        "## Metadata",
        "",
        f"- classification: **{decision['classification']}**",
        f"- gap table: L <= `{scan['l_max']}` exact bignum",
        f"- floor: every 2 <= n <= `{scan['floor']}` reaches 1: "
        f"`{floor_check['verified']}` "
        f"(max first-passage steps `{floor_check['max_first_passage_steps']}` "
        f"at seed `{floor_check['hardest_seed']}`, "
        f"peak `{floor_check['max_bits_seen']}` bits)",
        f"- contiguous excluded prefix at this floor: "
        f"L <= `{scan['achieved']['contiguous_prefix']}`",
        f"- exceptional lengths at this floor: "
        f"`{scan['achieved']['count']}`",
        f"- Eliahou leftover: period `{scan['eliahou']['lean_period']}`, or "
        f"one of `{scan['eliahou']['exception_count']}` listed "
        f"near-convergents, or `>= {scan['eliahou']['cutoff']}` "
        f"(table holds `{scan['eliahou']['table_holds']}`; "
        f"period 19 computationally excluded "
        f"`{scan['eliahou']['nineteen_computationally_excluded']}`)",
        "",
        decision["reason"] + ".",
        "",
        "## Census cross-check (L <= 8)",
        "",
        f"- n_max by length: `{scan['census']['n_max_by_length']}`",
        f"- killed by finance + Lean residual floor: "
        f"`{list(scan['census']['killed_by_lean_floor'])}`",
        f"- census-only lengths: "
        f"`{list(scan['census']['census_only_lengths'])}`",
        "",
        "## Record (near-convergent) lengths",
        "",
    ]
    for row in scan["records"]:
        lines.append(
            f"- L=`{row['L']}` o=`{row['o']}` theta=`{row['theta']:.3e}` "
            f"n_max=`{row['n_max']}`"
        )
    lines.extend(["", "## Exceptional lengths by floor", ""])
    for item in scan["exceptions"]:
        lines.append(
            f"- floor `{item['floor']}`: count `{item['count']}`, "
            f"first `{item['first_exception']}`, "
            f"contiguous prefix `{item['contiguous_prefix']}`"
        )
    lines.extend(["", "## Orbit slack", ""])
    for row in scan["slack"]:
        lines.append(
            f"- seed `{row['seed']}`: steps `{row['steps']}` "
            f"step bound ok `{row['step_bound_ok']}` "
            f"defect bound ok `{row['defect_bound_ok']}` "
            f"identity err `{row['identity_rel_err']:.2e}` "
            f"tightness `{row['tightness'] if row['tightness'] is None else round(row['tightness'], 4)}`"
        )
    lines.extend(
        [
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
        ]
    )
    return "\n".join(lines) + "\n"


def write_data_artifacts(payload: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    scan = payload["scan"]
    (DATA_DIR / "records.json").write_text(
        json.dumps(scan["records"], indent=2) + "\n", encoding="utf-8"
    )
    (DATA_DIR / "exceptions.json").write_text(
        json.dumps(scan["exceptions"], indent=2) + "\n", encoding="utf-8"
    )
    (DATA_DIR / "slack.json").write_text(
        json.dumps(scan["slack"], indent=2) + "\n", encoding="utf-8"
    )
    (DATA_DIR / "floor.json").write_text(
        json.dumps(scan["floor_check"], indent=2) + "\n", encoding="utf-8"
    )
    (DATA_DIR / "census_cross_check.json").write_text(
        json.dumps(scan["census"], indent=2) + "\n", encoding="utf-8"
    )
    summary = {
        "classification": payload["decision"]["classification"],
        "reason": payload["decision"]["reason"],
        "l_max": scan["l_max"],
        "floor": scan["floor"],
        "floor_verified": scan["floor_check"]["verified"],
        "contiguous_prefix": scan["achieved"]["contiguous_prefix"],
        "exception_count": scan["achieved"]["count"],
        "git": scan["git"],
    }
    (DATA_DIR / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    (DATA_DIR / "README.md").write_text(
        "# Cycle finance inequality\n\n"
        "Finance bound n ln n <= (6/5) L 3^o/(3^o - 2^L) on Juggler cycle\n"
        "minima, exact gap table, descent-induction floor, orbit slack.\n"
        "Not a halt theorem. The floor is COMPUTATIONALLY VERIFIED.\n\n"
        "Regenerate with `python -m research.juggler_sequence.cycle_finance`.\n",
        encoding="utf-8",
    )


def write_artifacts(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload if payload is not None else probe_payload()
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_markdown(data), encoding="utf-8")
    write_data_artifacts(data)
    return data


def main() -> None:
    payload = probe_payload(
        l_max=SCIENCE_L_MAX,
        floor=SCIENCE_FLOOR,
        seeds=SCIENCE_SEEDS,
    )
    write_artifacts(payload)
    scan = payload["scan"]
    print(payload["decision"]["classification"])
    print(payload["decision"]["reason"])
    print(
        f"floor_verified={scan['floor_check']['verified']} "
        f"prefix={scan['achieved']['contiguous_prefix']} "
        f"exceptions={scan['achieved']['count']} "
        f"records={len(scan['records'])}"
    )


if __name__ == "__main__":
    main()
