"""Streamlit-free view-model for the congruence / lifting explorer view."""

from __future__ import annotations

from bt.calculus.section import parse_poly
from visualization.residual_explorer import (
    LIFT_KIND_COLORS,
    LIFT_KIND_LABEL,
    lift_table_rows,
    lift_tree_svg,
    lifting_view,
)


def test_lifting_view_of_the_fermat_cubic():
    view = lifting_view(parse_poly("x^3-x"), 3, 2)
    assert view.poly == "-x + x^3"
    assert view.level_counts == (1, 3, 3, 3)
    assert view.brute_force_agrees
    assert not view.truncated
    kinds = dict(view.kind_census)
    assert kinds["unique"] == 9
    assert kinds["splitting"] == 1


def test_lifting_view_records_singular_nodes():
    view = lifting_view(parse_poly("x^2-9"), 3, 2)
    kinds = dict(view.kind_census)
    assert "singular-persistent" in kinds
    node = next(n for n in view.nodes if n.digits == "0" and n.depth == 1)
    assert node.residue == 0
    assert node.f_value == -9
    assert node.v3_f == 2
    assert node.v3_f_prime is None
    assert node.residual == "-3 + 3x^2"
    assert node.lift_trits == (-1, 0, 1)


def test_lifting_view_of_a_polynomial_without_solutions():
    view = lifting_view(parse_poly("x^2+3"), 3, 2)
    assert view.level_counts == (1, 1, 0, 0)
    assert view.brute_force_agrees
    assert dict(view.kind_census)["terminal"] == 1


def test_lifting_view_parent_and_children_links_are_consistent():
    view = lifting_view(parse_poly("x^4-x^2"), 3, 2)
    ids = {node.id for node in view.nodes}
    for node in view.nodes:
        assert set(node.children_ids) <= ids
        if node.depth == 0:
            assert node.parent_id is None
        else:
            assert node.parent_id in ids


def test_lifting_view_notes_disclaim_novelty():
    view = lifting_view(parse_poly("x^3-x"), 2, 2)
    joined = " ".join(view.notes)
    assert "zero-output subtree" in joined
    assert "scaled Taylor jet" in joined
    assert "No " in joined and "complexity" in joined


def test_lift_tree_svg_renders_every_node():
    view = lifting_view(parse_poly("x^3-x"), 2, 2)
    svg = lift_tree_svg(view.nodes, selected_id=view.nodes[0].id)
    assert svg.startswith("<svg")
    assert svg.count("<circle") + svg.count("<rect") == len(view.nodes)
    for kind, _ in view.kind_census:
        assert LIFT_KIND_COLORS[kind] in svg


def test_lift_tree_svg_of_an_empty_tree():
    svg = lift_tree_svg(())
    assert "no solutions" in svg


def test_lift_table_rows_expose_the_state():
    view = lifting_view(parse_poly("x^2-9"), 2, 2)
    rows = lift_table_rows(view.nodes)
    assert rows
    assert set(rows[0]) == {
        "word",
        "level",
        "x",
        "f(x)",
        "v3(f)",
        "v3(f')",
        "residual",
        "newton",
        "lift type",
        "lifts",
    }
    assert all(row["lift type"] in LIFT_KIND_LABEL for row in rows)
