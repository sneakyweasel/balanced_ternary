"""View-models for the research UI. No Streamlit import here."""

from __future__ import annotations

from dataclasses import dataclass

from balanced_ternary.representation import encode
from collatz.automata.symbolic_graph import build_symbolic_graph
from collatz.automata.two_adic import TwoAdicDigitAutomaton
from collatz.core import require_positive_odd
from collatz.cylinders import valuation_cylinder
from collatz.experiments.complexity_spectrum import complexity_row
from collatz.features import NUMERIC_FEATURE_NAMES
from collatz.languages.cylinder_dfa import entropy_report
from collatz.features import NUMERIC_FEATURE_NAMES
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


def trajectory_rows(n: int, max_steps: int) -> list[dict[str, object]]:
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
    return rows


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
