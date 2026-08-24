"""Tests for UI view-models (no Streamlit required)."""

from __future__ import annotations

from visualization.views import (
    analyze_view,
    apply_operator_view,
    calculator_view,
    parse_value,
    affine_center_census_view,
    automaton_partition_rows,
    automaton_view,
    complexity_spectrum_rows,
    cylinder_view,
    entropy_comparison_rows,
    exponent_code_view,
    fraction_text,
    inverse_tree_view,
    joint_graph_view,
    number_view,
    odd_part_trace,
    symbolic_graph_rows,
    trajectory_rows,
    trajectory_view,
    transducer_complexity_rows,
    warp_view,
)


def test_number_view_27():
    view = number_view(27)
    assert view.n == 27
    assert view.T_n == 41
    assert view.v2 == 1
    assert view.bt_n == "+000"
    assert view.bt_y == "+000+"
    assert view.append_plus_matches
    assert view.features_match
    names = [row[0] for row in view.feature_rows]
    assert "length" in names
    assert "weight" in names


def test_trajectory_rows_five():
    rows = trajectory_rows(5, 10)
    assert rows[0]["n"] == 5
    assert rows[0]["T(n)"] == 1


def test_automaton_partition_rows():
    rows = automaton_partition_rows(4)
    labels = [r["class"] for r in rows]
    assert any("v2 = 1" == x or x.startswith("v2 = 1") for x in labels)
    assert sum(int(r["odd residues"]) for r in rows) == 8


def test_transducer_complexity_rows():
    rows = transducer_complexity_rows(3)
    assert rows[0]["k"] == 1
    assert rows[0]["naive_bound"] == 3
    assert rows[-1]["k"] == 3


def test_odd_part_trace_82():
    payload = odd_part_trace(82)
    assert payload["v2"] == 1
    assert payload["odd_part_BT"] == "+----"
    assert payload["trace"]


def test_cylinder_view_11():
    payload = cylinder_view("1,1")
    assert payload["class_count"] == 1
    assert payload["matches_haar"]
    assert payload["residues"] == [7]


def test_entropy_comparison_rows():
    rows = entropy_comparison_rows(3)
    assert rows[0]["ks"] == "empty (odds)"
    assert rows[1]["word_count"] <= rows[0]["word_count"]


def test_complexity_spectrum_rows():
    rows = complexity_spectrum_rows(3)
    assert rows[0]["N_k"] == 3
    assert rows[1]["N_k"] == 5
    assert rows[2]["N_k"] == 9


def test_symbolic_graph_rows():
    rows = symbolic_graph_rows(1, 3)
    assert any(r["ks"] == "()" for r in rows)
    assert any("(1,)" in r["ks"] for r in rows)


def test_trajectory_view_reuses_rows():
    view = trajectory_view(5, 10)
    assert view.reached_one
    assert view.rows[0]["n"] == 5
    assert trajectory_rows(5, 10) == list(view.rows)


def test_inverse_and_automaton_payloads():
    tree = inverse_tree_view(1, 1, 4)
    assert tree["node_count"] >= 1
    auto = automaton_view(4, 27)
    assert auto["modulus"] == 16
    assert auto["odd_states"] == 8
    assert auto["rows"]


def test_joint_graph_view_sample():
    payload = joint_graph_view(20)
    assert payload["edge_count"] > 0
    assert payload["images_divisible_by_three"] == 0
    assert payload["sample"][0]["n"] == 1


def test_fraction_text():
    from fractions import Fraction

    assert fraction_text(Fraction(4, 2)) == "2"
    assert fraction_text((5, 2)) == "5/2"
    assert fraction_text([-3, 1]) == "-3"


def test_exponent_code_view_142():
    view = exponent_code_view("1,4,2")
    coords = dict(view.coordinates)
    assert view.valuations == (1, 4, 2)
    assert coords["m"] == 3
    assert coords["K"] == 7
    assert coords["R"] == coords["r"] or coords["r"] == coords["R"] % (1 << coords["K"])
    assert view.balanced_ternary_R
    assert view.exact_drift == "27/128"
    assert view.regime in {"contracting", "expanding"}
    assert all(holds for _, holds in view.inequalities)


def test_exponent_code_view_rejects_empty():
    import pytest

    with pytest.raises(ValueError):
        exponent_code_view(())


def test_affine_center_census_view_small():
    view = affine_center_census_view(2, 2, critical_gap=1, closest_count=5)
    assert view.row_count == 6
    partitions = dict(view.partition_counts)
    assert sum(partitions.values()) == 6
    assert view.closest_rows
    assert all(row["failures"] == 0 for row in view.inequality_rows)
    orders = {row["relation"]: row for row in view.coordinate_order_rows}
    assert "n_star_le_R" in orders
    assert orders["R_le_M"]["false"] >= 1 or orders["M_le_R"]["false"] >= 1


def test_warp_view_21():
    view = warp_view(21)
    assert view.n == 21
    assert view.W_n == 7
    assert view.t_defined
    assert view.t_of_W_defined
    assert view.Comm_WT == view.W_T - view.T_W
    assert not view.palindrome_n


def test_parse_value_integer_and_word():
    from bt.representation import encode

    parsed = parse_value(source="integer", integer=27)
    assert parsed.ok
    assert parsed.n == 27
    assert parsed.word == "+000"
    assert parsed.was_canonical
    worded = parse_value(source="word", word="+000")
    assert worded.ok
    assert worded.n == 27
    assert worded.word == encode(27).word()
    spaced = parse_value(source="word", word=" + 0 0 0 ")
    assert spaced.ok
    assert spaced.n == 27


def test_parse_value_rejects_invalid_word():
    empty = parse_value(source="word", word="   ")
    assert not empty.ok
    invalid = parse_value(source="word", word="2")
    assert not invalid.ok
    unknown = parse_value(source="hex", integer=1)
    assert not unknown.ok


def test_calculator_add_and_shift():
    added = calculator_view(
        left_source="integer",
        left_integer=5,
        left_word="",
        operation="add",
        right_source="integer",
        right_integer=7,
        right_word="",
    )
    assert added.ok
    assert added.result_n == 12
    assert added.result_word == "++0"
    shifted = calculator_view(
        left_source="word",
        left_integer=0,
        left_word="+000",
        operation="S",
    )
    assert shifted.ok
    assert shifted.result_n == 81
    assert shifted.result_word.endswith("0")


def test_calculator_domain_errors():
    odd_half = calculator_view(
        left_source="integer",
        left_integer=27,
        left_word="",
        operation="H2",
    )
    assert not odd_half.ok
    assert odd_half.error
    not_div3 = calculator_view(
        left_source="integer",
        left_integer=5,
        left_word="",
        operation="divide_by_3",
    )
    assert not not_div3.ok
    unknown = calculator_view(
        left_source="integer",
        left_integer=1,
        left_word="",
        operation="not-an-op",
    )
    assert not unknown.ok


def test_analyze_view_27():
    view = analyze_view(27)
    assert view.n == 27
    assert view.word == "+000"
    assert view.canonical
    metrics = dict(view.metric_rows)
    assert metrics["weight"] == 1
    assert metrics["v3"] == "3"
    residues = dict(view.residue_rows)
    assert residues[2] == 1
    assert residues[3] == 0


def test_apply_operator_h2_and_m2():
    doubled = apply_operator_view("M2", 21)
    assert doubled.ok
    assert doubled.result_n == 42
    assert doubled.consistent
    failed = apply_operator_view("H2", 21)
    assert not failed.ok
    assert failed.error

