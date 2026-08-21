"""Tests for UI view-models (no Streamlit required)."""

from __future__ import annotations

from visualization.views import (
    automaton_partition_rows,
    complexity_spectrum_rows,
    cylinder_view,
    entropy_comparison_rows,
    number_view,
    odd_part_trace,
    symbolic_graph_rows,
    trajectory_rows,
    transducer_complexity_rows,
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
