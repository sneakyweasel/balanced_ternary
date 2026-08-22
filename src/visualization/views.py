"""View-models for the research UI. No Streamlit import here."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from balanced_ternary.representation import encode
from collatz.affine_center import AffineCenterState
from collatz.automata.joint_graph import (
    build_joint_graph,
    synchronizing_digit_contexts,
)
from collatz.automata.symbolic_graph import build_symbolic_graph
from collatz.automata.two_adic import TwoAdicDigitAutomaton
from collatz.automata.valuation_shift import AdmissibleValuationAutomaton
from collatz.compatibility import CompatibilityState
from collatz.core import require_positive_odd
from collatz.cylinders import valuation_cylinder
from collatz.experiments.affine_center import run_affine_center_census
from collatz.experiments.complexity_spectrum import complexity_row
from collatz.features import NUMERIC_FEATURE_NAMES
from collatz.inverse import build_inverse_tree, format_inverse_tree
from collatz.languages.cylinder_dfa import entropy_report
from collatz.theorems import append_plus
from collatz.trajectory import collatz_trajectory
from collatz.transducers.divide_by_two import DivideByTwoTransducer
from collatz.transducers.divide_by_two_power import DivideByTwoPowerTransducer
from collatz.transducers.odd_part import odd_part_word
from collatz.transitions import feature_transition
from collatz.valuation import v2


@dataclass(frozen=True)
class NumberView:
    n: int
    bt_n: str
    three_n_plus_one: int
    bt_y: str
    v2: int
    T_n: int
    bt_t: str
    append_plus_word: str
    append_plus_matches: bool
    features_match: bool
    feature_rows: tuple[tuple[str, object, object, object, int], ...]


def number_view(n: int) -> NumberView:
    n = require_positive_odd(n)
    trans = feature_transition(n)
    rows = []
    fn = trans.features_n.as_dict()
    fy = trans.features_three_n_plus_one.as_dict()
    ft = trans.features_T_n.as_dict()
    for name in NUMERIC_FEATURE_NAMES:
        rows.append(
            (
                name,
                fn[name],
                fy[name],
                ft[name],
                trans.deltas[f"delta_{name}"],
            )
        )
    return NumberView(
        n=trans.n,
        bt_n=trans.balanced_ternary_n,
        three_n_plus_one=trans.three_n_plus_one,
        bt_y=trans.balanced_ternary_three_n_plus_one,
        v2=trans.v2_three_n_plus_one,
        T_n=trans.T_n,
        bt_t=trans.balanced_ternary_T_n,
        append_plus_word=append_plus(encode(n)).word(),
        append_plus_matches=trans.append_plus_matches,
        features_match=trans.append_plus_features_match,
        feature_rows=tuple(rows),
    )


def automaton_partition_rows(precision: int) -> list[dict[str, object]]:
    auto = TwoAdicDigitAutomaton(precision)
    part = auto.valuation_partition()
    rows: list[dict[str, object]] = []
    keys = sorted((k for k in part if k != "AT_LEAST_K"), key=int)
    if "AT_LEAST_K" in part:
        keys.append("AT_LEAST_K")
    odd = len(auto.odd_states())
    for key in keys:
        count = len(part[key])
        label = f"v2 = {key}" if key != "AT_LEAST_K" else f"v2 >= {precision}"
        rows.append(
            {
                "class": label,
                "odd residues": count,
                "share of odd states": round(count / odd, 4) if odd else 0.0,
            }
        )
    return rows


def transducer_complexity_rows(k_max: int) -> list[dict[str, int]]:
    rows = []
    for k in range(1, k_max + 1):
        rows.append(DivideByTwoPowerTransducer(k).complexity_report())
    return rows


def odd_part_trace(x: int) -> dict[str, object]:
    word = encode(x)
    k = v2(x)
    payload: dict[str, object] = {
        "x": x,
        "BT": word.word(),
        "v2": k,
        "odd_part_BT": odd_part_word(word).word(),
        "trace": [],
    }
    if x != 0 and x % 2 == 0:
        payload["trace"] = DivideByTwoTransducer().trace(word)
    return payload


def cylinder_view(ks: str, leftover_q: int = 1) -> dict[str, object]:
    cyl = valuation_cylinder(ks, leftover_q=leftover_q)
    return cyl.as_dict()


def entropy_comparison_rows(length: int) -> list[dict[str, object]]:
    prefixes: tuple[tuple[int, ...], ...] = ((), (1,), (2,), (1, 1), (1, 2), (2, 1))
    rows: list[dict[str, object]] = []
    for ks in prefixes:
        report = entropy_report(ks, length)
        rows.append(
            {
                "ks": "empty (odds)" if not ks else str(ks),
                "word_count": report.word_count,
                "canonical": report.canonical_count,
                "DFA states": report.minimized_states,
                "H_L base 3": (
                    None if report.h_base3 is None else round(report.h_base3, 6)
                ),
            }
        )
    return rows


def complexity_spectrum_rows(k_max: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for k in range(1, k_max + 1):
        row = complexity_row(k)
        rows.append(
            {
                "k": row["k"],
                "naive": row["naive_bound"],
                "reachable": row["reachable"],
                "N_k": row["N_k"],
                "A_k": row["A_k"],
                "A_k*N_k": row["C_k_product_bound"],
                "2^k+1": row["two_k_plus_one"],
                "N_k=2^k+1": row["matches_two_k_plus_one"],
            }
        )
    return rows


def symbolic_graph_rows(
    max_length: int, k_max: int, leftover_q: int = 1
) -> list[dict[str, object]]:
    graph = build_symbolic_graph(max_length, k_max, leftover_q=leftover_q)
    rows: list[dict[str, object]] = []
    for node in graph.nodes:
        kind = node.budget().kind if node.ks else "empty"
        rows.append(
            {
                "ks": str(node.ks) if node.ks else "()",
                "residue": node.residue,
                "P": node.precision,
                "budget": kind,
            }
        )
    return rows


@dataclass(frozen=True)
class TrajectoryView:
    reached_one: bool
    truncated: bool
    values: tuple[int, ...]
    rows: tuple[dict[str, object], ...]


def trajectory_view(n: int, max_steps: int) -> TrajectoryView:
    """Compute one trajectory and all of its presentation rows."""
    traj = collatz_trajectory(n, max_steps)
    rows: list[dict[str, object]] = []
    for i, step in enumerate(traj.steps):
        rec = feature_transition(step.n)
        rows.append(
            {
                "i": i,
                "n": step.n,
                "BT(n)": step.balanced_ternary_n,
                "v2": step.v2_three_n_plus_one,
                "T(n)": step.T_n,
                "BT(T)": step.balanced_ternary_T_n,
                "d_length": rec.deltas["delta_length"],
                "d_weight": rec.deltas["delta_weight"],
                "d_signed": rec.deltas["delta_signed_digit_sum"],
            }
        )
    return TrajectoryView(
        reached_one=traj.reached_one,
        truncated=traj.truncated,
        values=traj.values,
        rows=tuple(rows),
    )


def trajectory_rows(n: int, max_steps: int) -> list[dict[str, object]]:
    return list(trajectory_view(n, max_steps).rows)


def inverse_tree_view(root: int, depth: int, k_max: int) -> dict[str, object]:
    tree = build_inverse_tree(root, depth=depth, k_max=k_max, max_nodes=4000)
    return {
        "node_count": tree.node_count,
        "truncated": tree.truncated,
        "formatted": format_inverse_tree(tree),
    }


def automaton_view(precision: int, n: int) -> dict[str, object]:
    auto = TwoAdicDigitAutomaton(precision)
    word = encode(n)
    path = auto.run(word)
    part = auto.valuation_partition()
    keys = sorted((k for k in part if k != "AT_LEAST_K"), key=int)
    if "AT_LEAST_K" in part:
        keys.append("AT_LEAST_K")
    odd = len(auto.odd_states())
    rows = []
    for key in keys:
        count = len(part[key])
        rows.append(
            {
                "class": (
                    f"v2 = {key}" if key != "AT_LEAST_K" else f"v2 >= {precision}"
                ),
                "odd residues": count,
                "share of odd states": round(count / odd, 4) if odd else 0.0,
            }
        )
    return {
        "modulus": auto.modulus,
        "odd_states": odd,
        "reachable": len(auto.reachable_states()),
        "rows": rows,
        "report": auto.format_report(word),
        "final_residue": path[-1],
        "word": word.word(),
    }


def valuation_prefix_view(
    precision: int, k_max: int, max_length: int
) -> dict[str, object]:
    auto = AdmissibleValuationAutomaton(precision, k_max)
    report = auto.enumerate_admissible(max_length)
    rows: list[dict[str, object]] = []
    for length, words in report.by_length.items():
        for word in words[:30]:
            budget = report.budgets[word]
            rows.append(
                {
                    "length": length,
                    "k-word": str(word),
                    "sum k": budget.sum_k,
                    "2^{sum k}": budget.two_power,
                    "3^m": budget.three_power,
                    "budget": budget.kind,
                }
            )
    return {
        "prefix_count": len(report.prefixes),
        "contracting": report.contracting,
        "expanding": report.expanding,
        "start_count": report.start_count,
        "rows": rows,
        "counts": {
            "length": list(report.by_length),
            "prefixes": [len(report.by_length[length]) for length in report.by_length],
        },
    }


def joint_graph_view(limit: int) -> dict[str, object]:
    graph = build_joint_graph(limit)
    by_k = graph.out_degree_by_k()
    sample = [
        {
            "n": edge.n,
            "w": edge.w,
            "k": edge.k,
            "T(n)": edge.n_prime,
            "w'": edge.w_prime,
        }
        for edge in graph.edges[:40]
    ]
    return {
        "edge_count": len(graph.edges),
        "images_divisible_by_three": len(graph.images_divisible_by_three()),
        "by_k": {"k": list(by_k), "count": list(by_k.values())},
        "sample": sample,
    }


def synchronizing_context_view(precision: int, length: int) -> tuple[str, ...]:
    return tuple(synchronizing_digit_contexts(precision, length))


def fraction_text(value: Fraction | tuple[int, int] | list[int]) -> str:
    """Render exact rational data without introducing a floating approximation."""
    fraction = value if isinstance(value, Fraction) else Fraction(*value)
    if fraction.denominator == 1:
        return str(fraction.numerator)
    return f"{fraction.numerator}/{fraction.denominator}"


@dataclass(frozen=True)
class ExponentCodeView:
    valuations: tuple[int, ...]
    coordinates: tuple[tuple[str, object], ...]
    balanced_ternary_R: str
    lift_digits: tuple[int, ...]
    exact_drift: str
    floating_rates: tuple[tuple[str, float], ...]
    affine_rows: tuple[tuple[str, object], ...]
    inequalities: tuple[tuple[str, bool], ...]
    regime: str


def exponent_code_view(
    valuations: tuple[int, ...] | list[int] | str,
    *,
    critical_gap: int = 1,
) -> ExponentCodeView:
    state = CompatibilityState.from_valuations(valuations)
    diagnostic = state.diagnostic()
    if diagnostic.m == 0:
        raise ValueError("enter at least one valuation")
    center = AffineCenterState.from_valuations(state.valuations)
    return ExponentCodeView(
        valuations=diagnostic.valuations,
        coordinates=(
            ("m", diagnostic.m),
            ("K", diagnostic.K),
            ("C", diagnostic.C),
            ("R", diagnostic.R),
            ("r", diagnostic.r),
            ("M", diagnostic.M),
            ("X", diagnostic.canonical_endpoint),
        ),
        balanced_ternary_R=diagnostic.balanced_ternary_R,
        lift_digits=diagnostic.lift_digits,
        exact_drift=f"{diagnostic.three_power}/{diagnostic.two_power}",
        floating_rates=(
            ("d", diagnostic.d),
            ("rho_r", diagnostic.rho_r),
            ("rho_M", diagnostic.rho_M),
        ),
        affine_rows=(
            ("2^K - 3^m", str(center.gap)),
            ("partition", center.partition(critical_gap)),
            ("n*", fraction_text(center.n_star)),
            ("R - n*", fraction_text(center.R_minus_n_star)),
            ("X - n*", fraction_text(center.X_minus_n_star)),
            ("endpoint lift quotient", str(center.endpoint_lift_quotient)),
        ),
        inequalities=tuple(center.exact_inequalities().items()),
        regime=center.regime.value,
    )


@dataclass(frozen=True)
class AffineCenterCensusView:
    row_count: int
    partition_counts: tuple[tuple[str, int], ...]
    closest_rows: tuple[dict[str, object], ...]
    inequality_rows: tuple[dict[str, object], ...]
    coordinate_order_rows: tuple[dict[str, object], ...]


def affine_center_census_view(
    max_length: int,
    max_k: int,
    critical_gap: int,
    closest_count: int,
) -> AffineCenterCensusView:
    census = run_affine_center_census(
        max_length,
        max_k,
        critical_gap=critical_gap,
        closest_count=closest_count,
    )
    closest = []
    for row in census.closest_to_critical:
        closest.append(
            {
                "valuations": str(tuple(row["valuations"])),
                "m": row["m"],
                "K": row["K"],
                "gap": row["gap"],
                "partition": row["partition"],
                "R": row["R"],
                "M": row["M"],
                "X": row["X"],
                "n*": fraction_text(row["n_star"]),
            }
        )
    inequalities = tuple(
        {
            "relation": name,
            "applicable": report["applicable_count"],
            "failures": report["failure_count"],
            "status": report["status"],
        }
        for name, report in census.exact_inequalities.items()
    )
    coordinate_orders = []
    for name, report in census.coordinate_orders.items():
        false_witness = report["smallest_false"]
        coordinate_orders.append(
            {
                "relation": name,
                "true": report["true_count"],
                "false": report["false_count"],
                "universal on sample": report["universal_on_sample"],
                "smallest false code": (
                    None
                    if false_witness is None
                    else str(tuple(false_witness["valuations"]))
                ),
            }
        )
    return AffineCenterCensusView(
        row_count=len(census.rows),
        partition_counts=tuple(sorted(census.partition_counts.items())),
        closest_rows=tuple(closest),
        inequality_rows=inequalities,
        coordinate_order_rows=tuple(coordinate_orders),
    )
