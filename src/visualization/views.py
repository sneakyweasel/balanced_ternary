"""View-models for the research UI. No Streamlit import here."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from bt.representation import decode, encode, is_canonical, normalize
from bt.arithmetic import (
    add,
    add_one,
    divide_by_2_on_domain,
    divide_by_3_on_domain,
    format_factorization,
    is_prime,
    multiply_by_2,
    multiply_by_three,
    negate,
    subtract,
)
from bt.metrics import (
    lsd_nonzero_index,
    signed_digit_sum as bt_signed_digit_sum,
    v2 as bt_v2,
    v3 as bt_v3,
    weight as bt_weight,
)
from bt.operators import OPERATORS, OperatorDomainError, get_operator
from bt.transducers.divide_by_two import LeftoverCarryError
from research.collatz.affine_center import AffineCenterState
from research.collatz.automata.joint_graph import (
    build_joint_graph,
    synchronizing_digit_contexts,
)
from research.collatz.automata.symbolic_graph import build_symbolic_graph
from research.collatz.automata.two_adic import TwoAdicDigitAutomaton
from research.collatz.automata.valuation_shift import AdmissibleValuationAutomaton
from research.collatz.compatibility import CompatibilityState
from research.collatz.core import require_positive_odd
from research.collatz.cylinders import valuation_cylinder
from research.collatz.experiments.affine_center import run_affine_center_census
from research.collatz.experiments.complexity_spectrum import complexity_row
from research.collatz.features import NUMERIC_FEATURE_NAMES
from research.collatz.inverse import build_inverse_tree, format_inverse_tree
from research.collatz.languages.cylinder_dfa import entropy_report
from research.collatz.theorems import append_plus
from research.collatz.trajectory import collatz_trajectory
from research.collatz.transducers.divide_by_two import DivideByTwoTransducer
from research.collatz.transducers.divide_by_two_power import DivideByTwoPowerTransducer
from research.collatz.transducers.odd_part import odd_part_word
from research.collatz.transitions import feature_transition
from research.collatz.valuation import v2


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


@dataclass(frozen=True)
class WarpView:
    n: int
    bt_n: str
    W_n: int
    bt_W: str
    T_n: int | None
    W_T: int | None
    T_W: int | None
    Comm_WT: int | None
    palindrome_n: bool
    palindrome_T: bool | None
    t_defined: bool
    t_of_W_defined: bool
    delta_s: int | None
    delta_L: int | None
    s3_n: int
    L3_n: int


def warp_view(n: int) -> WarpView:
    from research.collatz.warp import warp_state

    state = warp_state(n)
    return WarpView(
        n=state.n,
        bt_n=state.bt_n,
        W_n=state.W_n,
        bt_W=state.bt_W,
        T_n=state.T_n,
        W_T=state.W_T,
        T_W=state.T_W,
        Comm_WT=state.Comm_WT,
        palindrome_n=state.palindrome_n,
        palindrome_T=state.palindrome_T,
        t_defined=state.t_defined,
        t_of_W_defined=state.t_of_W_defined,
        delta_s=state.delta_s,
        delta_L=state.delta_L,
        s3_n=state.s3_n,
        L3_n=state.L3_n,
    )


BINARY_CALCULATOR_OPS: frozenset[str] = frozenset({"add", "subtract"})
UNARY_CALCULATOR_OPS: dict[str, object] = {
    "negate": negate,
    "add_one": add_one,
    "multiply_by_2": multiply_by_2,
    "multiply_by_3": multiply_by_three,
    "divide_by_2": divide_by_2_on_domain,
    "divide_by_3": divide_by_3_on_domain,
}
CALCULATOR_OPERATIONS: tuple[str, ...] = (
    "add",
    "subtract",
    *UNARY_CALCULATOR_OPS,
    *OPERATORS,
)


@dataclass(frozen=True)
class ParsedValue:
    ok: bool
    error: str | None
    n: int | None
    word: str | None
    was_canonical: bool | None


@dataclass(frozen=True)
class CalculatorView:
    ok: bool
    error: str | None
    operation: str
    left: ParsedValue | None
    right: ParsedValue | None
    result_n: int | None
    result_word: str | None
    metric_rows: tuple[tuple[str, object], ...]


@dataclass(frozen=True)
class AnalyzeView:
    n: int
    word: str
    canonical: bool
    metric_rows: tuple[tuple[str, object], ...]
    residue_rows: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class OperatorApplyView:
    ok: bool
    error: str | None
    symbol: str
    n: int
    word: str
    result_n: int | None
    result_word: str | None
    consistent: bool
    metadata: tuple[tuple[str, object], ...]


def parse_value(
    *,
    source: str,
    integer: int = 0,
    word: str = "",
) -> ParsedValue:
    """Parse an integer or a display word into a canonical pair."""
    if source == "integer":
        if isinstance(integer, bool) or not isinstance(integer, int):
            return ParsedValue(False, "integer must be an int", None, None, None)
        encoded = encode(integer)
        return ParsedValue(True, None, integer, encoded.word(), True)
    if source != "word":
        return ParsedValue(False, f"unknown source {source!r}", None, None, None)
    text = "".join(ch for ch in word if not ch.isspace())
    if not text:
        return ParsedValue(False, "empty word is not a valid balanced ternary string", None, None, None)
    try:
        canonical = normalize(text)
    except (TypeError, ValueError) as exc:
        return ParsedValue(False, str(exc), None, None, None)
    return ParsedValue(
        True,
        None,
        decode(canonical),
        canonical.word(),
        is_canonical(text),
    )


def _valuation_text(value: int | None) -> str:
    return "∞" if value is None else str(value)


def value_metric_rows(n: int, word: str) -> tuple[tuple[str, object], ...]:
    encoded = normalize(word)
    lsd = lsd_nonzero_index(encoded)
    return (
        ("length", len(encoded)),
        ("weight", bt_weight(encoded)),
        ("weight parity", bt_weight(encoded) % 2),
        ("signed digit sum", bt_signed_digit_sum(encoded)),
        ("v2", _valuation_text(bt_v2(n))),
        ("v3", _valuation_text(bt_v3(n))),
        ("least-significant nonzero position", "none" if lsd is None else lsd),
        ("prime", is_prime(n)),
        ("factorization", format_factorization(n)),
    )


def analyze_view(n: int) -> AnalyzeView:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    encoded = encode(n)
    word = encoded.word()
    return AnalyzeView(
        n=n,
        word=word,
        canonical=is_canonical(word),
        metric_rows=value_metric_rows(n, word),
        residue_rows=tuple((q, n % q) for q in (2, 3, 5, 7)),
    )


def operator_catalog_rows() -> list[dict[str, object]]:
    return [op.metadata().as_dict() for op in OPERATORS.values()]


def apply_operator_view(symbol: str, n: int) -> OperatorApplyView:
    parsed = parse_value(source="integer", integer=n)
    if not parsed.ok:
        return OperatorApplyView(
            False, parsed.error, symbol, n, "", None, None, False, ()
        )
    try:
        op = get_operator(symbol)
    except KeyError as exc:
        return OperatorApplyView(
            False, str(exc), symbol, n, parsed.word or "", None, None, False, ()
        )
    metadata = tuple(op.metadata().as_dict().items())
    try:
        result_n = op.apply(n)
        result_word = op.apply_word(encode(n)).word()
    except (OperatorDomainError, LeftoverCarryError, ValueError, TypeError) as exc:
        return OperatorApplyView(
            False,
            str(exc),
            symbol,
            n,
            parsed.word or "",
            None,
            None,
            False,
            metadata,
        )
    consistent = decode(result_word) == result_n
    return OperatorApplyView(
        True,
        None if consistent else "integer and word results disagree",
        symbol,
        n,
        parsed.word or "",
        result_n,
        result_word,
        consistent,
        metadata,
    )


def calculator_view(
    *,
    left_source: str,
    left_integer: int,
    left_word: str,
    operation: str,
    right_source: str = "integer",
    right_integer: int = 0,
    right_word: str = "",
) -> CalculatorView:
    """Exact calculator over canonical words. Domain errors become ``ok=False``."""
    left = parse_value(source=left_source, integer=left_integer, word=left_word)
    if not left.ok:
        return CalculatorView(False, left.error, operation, left, None, None, None, ())
    right: ParsedValue | None = None
    try:
        if operation in BINARY_CALCULATOR_OPS:
            right = parse_value(
                source=right_source, integer=right_integer, word=right_word
            )
            if not right.ok:
                return CalculatorView(
                    False, right.error, operation, left, right, None, None, ()
                )
            fn = add if operation == "add" else subtract
            result = fn(left.word, right.word)
            result_n = decode(result)
            result_word = result.word()
        elif operation in UNARY_CALCULATOR_OPS:
            result = UNARY_CALCULATOR_OPS[operation](left.word)
            result_n = decode(result)
            result_word = result.word()
        elif operation in OPERATORS:
            applied = apply_operator_view(operation, left.n)
            if not applied.ok:
                return CalculatorView(
                    False, applied.error, operation, left, None, None, None, ()
                )
            result_n = applied.result_n
            result_word = applied.result_word
        else:
            known = ", ".join(CALCULATOR_OPERATIONS)
            return CalculatorView(
                False,
                f"unknown operation {operation!r}; known: {known}",
                operation,
                left,
                None,
                None,
                None,
                (),
            )
    except (OperatorDomainError, LeftoverCarryError, ValueError, TypeError) as exc:
        return CalculatorView(False, str(exc), operation, left, right, None, None, ())
    return CalculatorView(
        True,
        None,
        operation,
        left,
        right,
        result_n,
        result_word,
        value_metric_rows(result_n, result_word),
    )
