"""Exact series, inequalities, and censuses for fixed-integer affine geometry."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any

from research.collatz.affine_gap import affine_gap_from_orbit, next_affine_gap, step_addend
from research.collatz.core import collatz_step, collatz_valuation, require_positive_odd
from research.collatz.experiments.schema import ExperimentManifest, FIXED_INTEGER_SCHEMA_VERSION
from research.collatz.experiments.table_io import write_experiment
from research.collatz.fixed_integer import (
    InfiniteTrajectoryAffineState,
    exact_partition,
    iterate_states,
    next_C,
    normalized_C,
    normalized_C_finite_bounds,
    normalized_C_series,
)
from research.collatz.itinerary import affine_constant, partial_sums_K
from research.collatz.periodic_code import PeriodicFixedPointTheorem
from pathlib import Path


def positivity_inequalities(state: InfiniteTrajectoryAffineState) -> dict[str, object]:
    """Exact inequalities; tag which ones are itinerary-free tautologies."""
    one_over_lambda = Fraction(state.two_power, state.three_power)
    return {
        "x_ge_1": {
            "holds": state.x >= 1,
            "information": "positivity of an actual accelerated orbit; tautological",
        },
        "B_ge_lambda_inv": {
            "holds": state.B >= one_over_lambda,
            "information": "restates x >= 1 via B = (2^K/3^m) x",
        },
        "G_eq_two_power_times_n_minus_x": {
            "holds": state.G == state.two_power * (state.n - state.x),
            "information": "exact; sign of G is whether the orbit is below the start",
        },
        "expanding_implies_x_gt_n": {
            "holds": state.regime != "expanding" or state.x > state.n,
            "information": "lambda > 1 and C > 0 force x > n on expanding prefixes",
        },
        "n_star_le_n": {
            "holds": state.n_star_le_n() in (True, None),
            "information": (
                "equivalent to G/D >= 0; in the contracting regime this is x <= n"
            ),
        },
    }


def stronger_gap_statements(state: InfiniteTrajectoryAffineState) -> dict[str, object]:
    """Exact comparisons involving G that follow from the affine identity.

    ``G / 2^K = n - x`` is an integer identity, not a new obstruction.
    The only sign-transparent extra structure is the k=1 versus k>=2
    addend law in the G recurrence.
    """
    statements = {
        "G_divisible_by_two_power": {
            "holds": state.G % state.two_power == 0,
            "value": state.n - state.x,
            "information": "restates G = 2^K (n - x); tautological on actual orbits",
        },
        "G_over_three_power": {
            "value": Fraction(state.G, state.three_power),
            "information": "n(lambda^{-1} - 1) - A; same data as (n, A, lambda)",
        },
        "G_over_n": {
            "value": Fraction(state.G, state.n),
            "information": "D - C/n; not generally integral",
        },
    }
    if state.C != 0:
        statements["G_over_C"] = {
            "value": Fraction(state.G, state.C),
            "information": "n D / C - 1 = n / n_* - 1 when the center exists",
        }
    if state.valuations:
        k = state.valuations[-1]
        previous_two = state.two_power >> k
        addend = step_addend(state.n, previous_two, k)
        statements["last_addend"] = {
            "k": k,
            "addend": addend,
            "negative_iff_k_eq_1": (addend < 0) == (k == 1),
            "information": "k=1 contributes 2^K (-n-1)<0; k>=2 is nonnegative for n>=1",
        }
    return statements


def compare_two_K_three_m(two_power: int, three_power: int) -> str:
    """Exact comparison used instead of a floating K/m versus log2(3)."""
    if two_power == three_power:
        return "equal"
    return "contracting" if two_power > three_power else "expanding"


def walk_integer_ledger(
    n: int,
    max_steps: int,
    *,
    critical_gap: int = 1,
) -> list[dict[str, Any]]:
    """Fast integer ledger of an actual trajectory. No floats."""
    n = require_positive_odd(n)
    x = n
    C = 0
    K = 0
    m = 0
    two = 1
    three = 1
    G = 0
    ks: list[int] = []
    rows = [
        {
            "n": n,
            "m": 0,
            "K": 0,
            "C": 0,
            "x": n,
            "k": None,
            "G": 0,
            "two_power": 1,
            "three_power": 1,
            "regime": "empty",
            "partition": "empty",
            "A_num": 0,
            "A_den": 1,
        }
    ]
    steps = 0
    while steps < max_steps:
        k = collatz_valuation(x)
        G = next_affine_gap(G, n, two, k)
        C = 3 * C + two
        two <<= k
        K += k
        m += 1
        three *= 3
        ks.append(k)
        x = collatz_step(x)
        if G != affine_gap_from_orbit(n, x, two):
            raise ArithmeticError("integer ledger G recurrence failed")
        A = normalized_C(C, m)
        rows.append(
            {
                "n": n,
                "m": m,
                "K": K,
                "C": C,
                "x": x,
                "k": k,
                "G": G,
                "two_power": two,
                "three_power": three,
                "regime": "contracting" if two > three else "expanding",
                "partition": exact_partition(two, three, critical_gap),
                "A_num": A.numerator,
                "A_den": A.denominator,
                "n_star_le_n": G * (two - three) >= 0,
            }
        )
        steps += 1
        if x == 1:
            break
    if ks and affine_constant(tuple(ks)) != C:
        raise ArithmeticError("ledger C disagrees with affine_constant")
    predicted_C = 0
    two_check = 1
    for k in ks:
        predicted_C = next_C(predicted_C, two_check)
        two_check <<= k
    if ks and predicted_C != C:
        raise ArithmeticError("ledger C disagrees with next_C recurrence")
    if ks and normalized_C_series(partial_sums_K(tuple(ks))) != normalized_C(C, len(ks)):
        raise ArithmeticError("ledger A series disagrees with C/3^m")
    if ks:
        bounds = normalized_C_finite_bounds(partial_sums_K(tuple(ks)))
        if not (bounds["lower_K_j_ge_0"] <= bounds["A"] <= bounds["upper_K_j_le_K_last"]):
            raise ArithmeticError("normalized C escaped its exact finite bounds")
    return rows


def compatibility_ledger(n: int, max_steps: int) -> tuple[InfiniteTrajectoryAffineState, ...]:
    """Full exact states, including Kramer M and cylinder residues."""
    states = iterate_states(n, max_steps)
    for i in range(len(states) - 1):
        k = states[i + 1].valuations[-1]
        predicted = next_affine_gap(states[i].G, n, states[i].two_power, k)
        if predicted != states[i + 1].G:
            raise ArithmeticError("compatibility ledger G recurrence failed")
        if not states[i + 1].validates():
            raise ArithmeticError("compatibility ledger identity failed")
    return states


@dataclass
class FixedIntegerCensus:
    limit: int
    max_steps: int
    critical_gap: int
    odd_count: int
    contracting_prefixes: int
    expanding_prefixes: int
    critical_near_prefixes: int
    n_star_le_n_failure_count: int
    n_star_le_n_failures: tuple[dict[str, Any], ...]
    min_G: dict[str, Any] | None
    min_contracting_G: dict[str, Any] | None
    special_cases: dict[str, Any]
    schema_version: str = FIXED_INTEGER_SCHEMA_VERSION
    paths: dict[str, str] = field(default_factory=dict)


def _record_min_G(
    current: dict[str, Any] | None,
    n: int,
    m: int,
    G: int,
    x: int,
    regime: str,
) -> dict[str, Any] | None:
    payload = {"n": n, "m": m, "G": G, "x": x, "regime": regime}
    if current is None:
        return payload
    if (G, n, m) < (current["G"], current["n"], current["m"]):
        return payload
    return current


N_STAR_LE_N_SMALLEST_COUNTEREXAMPLE = {
    "n": 165,
    "m": 17,
    "x": 167,
    "K": 27,
    "C": 1106233681,
    "G": -268435456,
    "D": 5077565,
    "valuations": (4, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 3),
    "status": "REFUTED EXACTLY: contracting prefix with x > n, hence n_* > n",
}


def scan_n_star_le_n(
    limit: int,
    max_steps: int,
    *,
    critical_gap: int = 1,
    max_failures: int = 8,
) -> tuple[list[dict[str, Any]], dict[str, Any] | None, dict[str, Any] | None, dict[str, int]]:
    """Search actual odd trajectories for contracting prefixes with ``x > n``.

    Those are exactly the failures of ``n_* <= n``. The smallest exact
    witness is ``n=165``, ``m=17``.
    """
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be an integer >= 1")
    if isinstance(max_failures, bool) or not isinstance(max_failures, int) or max_failures < 0:
        raise ValueError("max_failures must be an integer >= 0")
    failures: list[dict[str, Any]] = []
    min_G = None
    min_contracting_G = None
    counts = {
        "odd_count": 0,
        "contracting_prefixes": 0,
        "expanding_prefixes": 0,
        "critical_near_prefixes": 0,
        "n_star_le_n_failures": 0,
    }
    for n in range(1, limit + 1, 2):
        counts["odd_count"] += 1
        x = n
        C = 0
        two = 1
        three = 1
        G = 0
        m = 0
        steps = 0
        while steps < max_steps:
            k = collatz_valuation(x)
            G = next_affine_gap(G, n, two, k)
            C = 3 * C + two
            two <<= k
            m += 1
            three *= 3
            x = collatz_step(x)
            D = two - three
            regime = "contracting" if D > 0 else "expanding"
            if abs(D) <= critical_gap:
                counts["critical_near_prefixes"] += 1
            elif D > 0:
                counts["contracting_prefixes"] += 1
            else:
                counts["expanding_prefixes"] += 1
            min_G = _record_min_G(min_G, n, m, G, x, regime)
            if D > 0:
                min_contracting_G = _record_min_G(min_contracting_G, n, m, G, x, regime)
            if D > 0 and G < 0:
                payload = {
                    "n": n,
                    "m": m,
                    "x": x,
                    "G": G,
                    "D": D,
                    "C": C,
                    "K": two.bit_length() - 1,
                }
                counts["n_star_le_n_failures"] += 1
                if len(failures) < max_failures:
                    failures.append(payload)
            steps += 1
            if x == 1:
                break
    return failures, min_G, min_contracting_G, counts


def special_case_report(max_steps: int = 40) -> dict[str, Any]:
    """Sanity checks named in the milestone."""
    report: dict[str, Any] = {}
    for n in (1, 3):
        states = iterate_states(n, max_steps)
        report[f"n={n}"] = {
            "valuations": list(states[-1].valuations),
            "final_x": states[-1].x,
            "regimes": [state.regime for state in states[1:]],
            "G": [state.G for state in states],
            "n_star_le_n": [state.n_star_le_n() for state in states[1:]],
        }
    report["n=2"] = {
        "status": "even; accelerated T is undefined. No signed-T convention.",
    }
    high = iterate_states(27, max_steps)
    first_contracting = next((state for state in high if state.regime == "contracting"), None)
    report["n=27"] = {
        "steps": len(high) - 1,
        "min_G": min(state.G for state in high),
        "first_contracting": None if first_contracting is None else first_contracting.m,
        "first_contracting_x": None if first_contracting is None else first_contracting.x,
        "n_star_le_n_failures": [
            state.m for state in high[1:] if state.n_star_le_n() is False
        ],
    }
    for n in (7, 41, 703, 6171):
        states = iterate_states(n, max_steps)
        contracting = [state for state in states[1:] if state.regime == "contracting"]
        report[f"n={n}"] = {
            "steps": len(states) - 1,
            "min_G": min(state.G for state in states),
            "min_contracting_G": (
                None if not contracting else min(state.G for state in contracting)
            ),
            "n_star_le_n_failures": [
                state.m for state in states[1:] if state.n_star_le_n() is False
            ],
        }
    ones = PeriodicFixedPointTheorem.from_valuations((1,) * 6)
    twos = PeriodicFixedPointTheorem.from_valuations((2,) * 6)
    report["all_ones_period_6"] = {
        "gap": ones.gap,
        "expanding_excludes_positive": ones.expanding_excludes_positive,
        "positive_candidate": ones.positive_candidate,
    }
    report["all_twos_period_6"] = {
        "gap": twos.gap,
        "positive_candidate": twos.positive_candidate,
        "note": "period (2) has candidate 1; repeating (2) still yields n=1",
    }
    report["n_star_le_n_smallest_counterexample"] = dict(
        N_STAR_LE_N_SMALLEST_COUNTEREXAMPLE
    )
    return report


def run_fixed_integer_census(
    limit: int,
    max_steps: int,
    *,
    critical_gap: int = 1,
    output_dir: Path | str | None = None,
    write_rows_limit: int = 200,
) -> FixedIntegerCensus:
    failures, min_G, min_contracting_G, counts = scan_n_star_le_n(
        limit, max_steps, critical_gap=critical_gap
    )
    special = special_case_report(max_steps=min(max_steps, 80))
    sample_rows = []
    for n in (1, 3, 7, 27, 41, 703):
        if n <= limit:
            sample_rows.extend(walk_integer_ledger(n, min(max_steps, 30), critical_gap=critical_gap))
    paths: dict[str, str] = {}
    if output_dir is not None:
        rows = sample_rows[:write_rows_limit]
        manifest = ExperimentManifest(
            experiment_name="fixed-integer-affine",
            parameters={
                "limit": limit,
                "max_steps": max_steps,
                "critical_gap": critical_gap,
                "sample": "named trajectories plus n_*<=n scan",
            },
            row_count=len(rows),
            claim_status="EXACT identities; n_*<=n scan is computational",
            schema_version=FIXED_INTEGER_SCHEMA_VERSION,
        )
        paths = write_experiment(rows, output_dir, "fixed_integer", manifest)
    return FixedIntegerCensus(
        limit=limit,
        max_steps=max_steps,
        critical_gap=critical_gap,
        odd_count=counts["odd_count"],
        contracting_prefixes=counts["contracting_prefixes"],
        expanding_prefixes=counts["expanding_prefixes"],
        critical_near_prefixes=counts["critical_near_prefixes"],
        n_star_le_n_failure_count=counts["n_star_le_n_failures"],
        n_star_le_n_failures=tuple(failures),
        min_G=min_G,
        min_contracting_G=min_contracting_G,
        special_cases=special,
        paths=paths,
    )
