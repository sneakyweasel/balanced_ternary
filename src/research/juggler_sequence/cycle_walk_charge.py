"""Exact cyclic exponent-walk charge for CycleMin finance.

The length-only parity/run-pack tables price valleys independently.
This probe computes the exact optimum of the coupled walk charge:
every state x_k on a CycleMin cycle satisfies n <= x_k <= n^(2^u_k),
where u_k = log2(3/2) * (#odds among first k letters) - (#evens),
u_0 = 0, u_k >= 0 (upper envelope is defect-free: floor(x^1.5) <=
x^1.5 and floor(sqrt x) <= sqrt x). Charging state k at the height
n^(max(2^u_k - eta, 1)) gives an upper bound on Sum 1/(x_i ln x_i)
once the lower-envelope defect transport eta is certified; eta is a
sensitivity band here, not a theorem. Phase-0 numbers only. Not a
halt theorem, not a no-cycle-of-any-length claim.
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np

from research.juggler_sequence.cycle_finance import (
    EPS_CONST,
    PARITY_REL_GUARD,
    PUBLISHED_FLOOR,
    git_commit,
    o_min_and_theta,
    parity_rhs_upper,
)

DATA_DIR = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "research"
    / "juggler"
    / "cycle_walk_charge"
)

MU = math.log2(1.5)  # up-step of the exponent walk per odd letter
STEP = 1.0 + MU  # u(k, a) = STEP * a - k
CERTIFIED_FLOOR = 26_254_995  # J-residual-floor-twenty-six-million
TARGET_LENGTH = 50_508
CALIBRATION_LENGTH = 25_781
SURVEY_L_MAX = 200_000
U_TOL = 1e-9


def transport_bound(length: int, odd_count: int, n: int) -> float:
    """Crude worst-case eta for the lower-envelope defect transport.

    Log-deficit recursion: E' <= (3/2)E + 2 x^{-3/2} (odd),
    E' <= E/2 + 2 x^{-1/2} (even); amplification from injection j to
    state k is exactly w_k / w_j, so at a charged state
    E_k / w_k <= sum_j inj_j / w_j. Even states have w >= 2 (the walk
    is >= 1 after the down step), odd states w >= 1, and x >= n^w
    up to the bootstrap factor e^{E/2} <= 1.01. This is a numerical
    bound for the sensitivity band, not yet a certified lemma.
    """

    even_count = length - odd_count
    deficit = 1.01 * (even_count / n + 2.0 * odd_count / n**1.5)
    return deficit / math.log(n)


def charge_row(u: np.ndarray, n: int, eta: float) -> np.ndarray:
    """f(u) = 1 / (x ln x) at the walk price x = n^max(2^u - eta, 1)."""

    log_n = math.log(n)
    # Large u overflows w to inf and the charge to exactly 0 — correct.
    with np.errstate(under="ignore", over="ignore"):
        w = np.maximum(np.exp2(u) - eta, 1.0)
        return np.exp(-w * log_n - np.log(w * log_n))


def walk_budget(
    length: int,
    odd_count: int,
    n: int,
    *,
    eta: float = 0.0,
) -> dict[str, Any]:
    """Exact max of Sum_k f(u_k) over nonneg exponent walks.

    DP over (step k, odds used a); u = STEP * a - k is exact on the
    lattice. States x_0..x_{L-1} are charged; the return to x_0 is
    not charged twice. Any binary word with o odds, e evens, and
    u_k >= 0 is admitted (a relaxation of realizability).
    """

    even_count = length - odd_count
    started = time.perf_counter()
    neg = -math.inf
    values = np.full(odd_count + 1, neg)
    values[0] = charge_row(np.zeros(1), n, eta)[0]
    a_axis = np.arange(odd_count + 1, dtype=np.float64)
    for k in range(1, length + 1):
        stay = values
        step_up = np.full_like(values, neg)
        step_up[1:] = values[:-1]
        values = np.maximum(stay, step_up)
        u = STEP * a_axis - k
        feasible = (
            (u >= -U_TOL)
            & (a_axis <= min(odd_count, k))
            & (k - a_axis <= even_count)
        )
        values = np.where(feasible, values, neg)
        if k < length:
            values = values + np.where(
                feasible, charge_row(np.maximum(u, 0.0), n, eta), 0.0
            )
    best = float(values[odd_count])
    return {
        "length": length,
        "odd_count": odd_count,
        "even_count": even_count,
        "n": n,
        "eta": eta,
        "walk_sum": best,
        "surplus_u": STEP * odd_count - length,
        "elapsed_s": time.perf_counter() - started,
    }


def brute_force_budget(
    length: int,
    odd_count: int,
    n: int,
    *,
    eta: float = 0.0,
) -> float:
    """Exhaustive check of the DP on tiny lengths."""

    best = -math.inf
    for mask in range(1 << length):
        if bin(mask).count("1") != odd_count:
            continue
        u = 0.0
        total = charge_row(np.zeros(1), n, eta)[0]
        ok = True
        for k in range(length):
            u += MU if (mask >> k) & 1 else -1.0
            if u < -U_TOL:
                ok = False
                break
            if k + 1 < length:
                total += charge_row(np.array([max(u, 0.0)]), n, eta)[0]
        if ok:
            best = max(best, total)
    return best


def kill_report(
    length: int,
    n0: int,
    *,
    const: float = EPS_CONST,
    etas: tuple[float, ...] | None = None,
) -> dict[str, Any]:
    """Walk charge versus theta at cycle minimum >= n0 + 1."""

    odd_count, theta = o_min_and_theta(length)
    n = n0 + 1
    eta_star = transport_bound(length, odd_count, n)
    if etas is None:
        etas = (0.0, eta_star, 10.0 * eta_star, 100.0 * eta_star)
    parity_rhs = parity_rhs_upper(n, length, odd_count, const=const)
    rows = []
    for eta in etas:
        budget = walk_budget(length, odd_count, n, eta=eta)
        rhs = (
            const * budget["walk_sum"] * (1.0 + PARITY_REL_GUARD)
        )
        rows.append(
            {
                "eta": eta,
                "walk_sum": budget["walk_sum"],
                "walk_rhs": rhs,
                "theta": theta,
                "kill_margin": theta / rhs if rhs > 0 else math.inf,
                "walk_excludes": theta * (1.0 - PARITY_REL_GUARD) > rhs,
                "elapsed_s": budget["elapsed_s"],
            }
        )
    return {
        "length": length,
        "odd_count": odd_count,
        "theta": theta,
        "floor": n0,
        "const": const,
        "transport_eta": eta_star,
        "parity_rhs": parity_rhs,
        "parity_margin": theta / parity_rhs,
        "improvement_over_parity": parity_rhs / rows[0]["walk_rhs"],
        "eta_rows": rows,
    }


def survivor_survey(
    n0: int = CERTIFIED_FLOOR,
    *,
    l_max: int = SURVEY_L_MAX,
    const: float = EPS_CONST,
) -> dict[str, Any]:
    """Walk-charge kill table over the parity survivors at the floor.

    Each survivor is tested at its own transport bound eta. The
    resulting cutoff is hypothetical (the transport lemma is not yet
    certified); recorded as numbers, not as a theorem.
    """

    from research.juggler_sequence.cycle_finance import parity_excludes
    from research.juggler_sequence.cycle_floor_sensitivity import iter_o_min

    rows = []
    for length, odd_count, theta in iter_o_min(l_max):
        if parity_excludes(length, odd_count, theta, n0, const=const):
            continue
        n = n0 + 1
        eta = transport_bound(length, odd_count, n)
        budget = walk_budget(length, odd_count, n, eta=eta)
        rhs = const * budget["walk_sum"] * (1.0 + PARITY_REL_GUARD)
        row = {
            "length": length,
            "odd_count": odd_count,
            "theta": theta,
            "eta": eta,
            "walk_rhs": rhs,
            "kill_margin": theta / rhs if rhs > 0 else math.inf,
            "walk_excludes": theta * (1.0 - PARITY_REL_GUARD) > rhs,
            "elapsed_s": budget["elapsed_s"],
        }
        rows.append(row)
        print(
            f"survey L={length} margin={row['kill_margin']:.3f} "
            f"excludes={row['walk_excludes']} ({row['elapsed_s']:.0f}s)",
            flush=True,
        )
    killed = [row["length"] for row in rows if row["walk_excludes"]]
    alive = [row["length"] for row in rows if not row["walk_excludes"]]
    return {
        "floor": n0,
        "l_max": l_max,
        "const": const,
        "parity_survivors": [row["length"] for row in rows],
        "walk_killed": killed,
        "walk_alive": alive,
        "hypothetical_first_survivor": alive[0] if alive else None,
        "hypothetical_prefix": (alive[0] - 1) if alive else l_max,
        "certified": False,
        "rows": rows,
        "git_commit": git_commit(),
    }


def probe_payload() -> dict[str, Any]:
    target = kill_report(TARGET_LENGTH, CERTIFIED_FLOOR)
    calibration = kill_report(
        CALIBRATION_LENGTH, PUBLISHED_FLOOR
    )
    return {
        "model": (
            "coupled exponent-walk charge; states priced at "
            "n^max(2^u - eta, 1); u >= 0 from the defect-free upper "
            "envelope; eta is an uncertified sensitivity band"
        ),
        "target": target,
        "calibration": calibration,
        "classification": classify(target),
        "not_a_halt_theorem": True,
        "no_cycle_all_lengths": False,
        "git_commit": git_commit(),
    }


def classify(target: dict[str, Any]) -> dict[str, Any]:
    rows = {row["eta"]: row for row in target["eta_rows"]}
    eta_star = target["transport_eta"]
    at_zero = rows.get(0.0)
    at_star = rows.get(eta_star)
    at_ten = rows.get(10.0 * eta_star)
    if all(
        row is not None and row["walk_excludes"]
        for row in (at_zero, at_star, at_ten)
    ):
        label = "WALK_CHARGE_GREEN"
        reason = (
            "the coupled walk optimum excludes the target at eta = 0, "
            "at the worst-case transport bound, and at ten times it; "
            "a certified transport lemma would make this a theorem"
        )
    elif at_star is not None and at_star["walk_excludes"]:
        label = "WALK_CHARGE_AMBER"
        reason = (
            "the walk optimum excludes the target at the transport "
            "bound but not at ten times it; the margin is thin"
        )
    else:
        label = "WALK_CHARGE_PARK"
        reason = (
            "the coupled walk optimum does not exclude the target at "
            "the transport bound; the adversary budget stays above theta"
        )
    return {"label": label, "reason": reason}


def write_artifacts(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or probe_payload()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "summary.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    return payload


def write_survey(survey: dict[str, Any] | None = None) -> dict[str, Any]:
    survey = survey or survivor_survey()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "survey.json").write_text(
        json.dumps(survey, indent=2) + "\n", encoding="utf-8"
    )
    return survey


def main() -> None:
    import sys

    if "--survey" in sys.argv:
        survey = write_survey()
        for row in survey["rows"]:
            print(
                f"L={row['length']:<7} margin={row['kill_margin']:.3f} "
                f"excludes={row['walk_excludes']} "
                f"({row['elapsed_s']:.0f}s)",
                flush=True,
            )
        print(f"walk killed {len(survey['walk_killed'])} of "
              f"{len(survey['rows'])}; hypothetical first survivor "
              f"{survey['hypothetical_first_survivor']}")
        return
    payload = write_artifacts()
    target = payload["target"]
    print(f"L={target['length']} floor={target['floor']}")
    print(f"theta          = {target['theta']:.6e}")
    print(f"parity RHS     = {target['parity_rhs']:.6e}")
    print(f"transport eta  = {target['transport_eta']:.3e}")
    for row in target["eta_rows"]:
        print(
            f"eta={row['eta']:.3e} walk RHS = {row['walk_rhs']:.6e} "
            f"margin = {row['kill_margin']:.3f} "
            f"excludes = {row['walk_excludes']}"
        )
    print(payload["classification"]["label"])


if __name__ == "__main__":
    main()
