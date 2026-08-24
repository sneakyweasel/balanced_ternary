"""Residual Explorer adapters wrap bt.calculus; they do not reimplement it."""

from __future__ import annotations

from bt.calculus.cubic import F_k, image_profile
from bt.calculus.poly_congruence import first_distinction_horizon, function_equiv
from bt.calculus.quadratic import pack_word
from bt.calculus.section import parse_poly
from visualization.residual_explorer import (
    PRESETS,
    census_view,
    compare_states,
    deficit_of,
    demo_delayed_pair,
    depth_from_mode,
    dual_census,
    expand_subtree_words,
    fibre_view,
    filter_nodes,
    format_word,
    inspect_node,
    parse_word,
    prefix_digits,
    residual_of,
    resolve_polynomial,
    tree_svg,
    visible_subtree,
    visibility_story,
)
import argparse

from cli.calculus import add_calculus_subparser
from visualization.theorem_ledger import badge_payload, claim_kind, theorem_entry


def test_presets_parse():
    for text in PRESETS:
        resolve_polynomial(text)


def test_select_x3_inspects_root():
    f = parse_poly("x^3")
    view = inspect_node(f, (), 10)
    assert view.state.source_poly == "x^3"
    assert view.state.m == 0
    assert view.state.p == 0
    assert view.state.exact == "x^3"
    assert view.source_is_x3
    assert len(view.newton.coords) == 4


def test_change_k_recolours_delayed_pair():
    f, wa, wb = demo_delayed_pair()
    left = residual_of(f, wa)
    right = residual_of(f, wb)
    assert function_equiv(left, right, 2)
    assert not function_equiv(left, right, 3)
    a2 = inspect_node(f, wa, 2)
    b2 = inspect_node(f, wb, 2)
    a3 = inspect_node(f, wa, 3)
    b3 = inspect_node(f, wb, 3)
    assert a2.newton.phi == b2.newton.phi
    assert a3.newton.phi != b3.newton.phi


def test_change_depth_deficit():
    assert depth_from_mode(10, mode="deficit", r=2) == 7
    assert deficit_of(10, 7) == 2
    assert depth_from_mode(10, mode="explicit", m=8) == 8
    story0 = visibility_story(parse_poly("x^3"), 9, 10)
    story1 = visibility_story(parse_poly("x^3"), 8, 10)
    story2 = visibility_story(parse_poly("x^3"), 7, 10)
    assert story0.r == 0
    assert "nothing" in story0.n2_sees
    assert story1.r == 1
    assert "mod 3" in story1.n2_sees
    assert story2.r == 2
    assert "mod 9" in story2.n2_sees
    assert story2.badge is not None
    assert story2.badge["kind"] == "exact"
    assert story2.badge["id"] == "BTA-x3-vis"


def test_select_residual_and_newton():
    f = parse_poly("x^3")
    word = (0, 0, 0, 0, 0, 0, 0)
    view = inspect_node(f, word, 10)
    assert view.state.m == 7
    assert view.state.p == 0
    assert view.visibility.r == 2
    assert "mod 9" in view.visibility.n2_sees
    names = [c.index for c in view.newton.coords]
    assert names == [0, 1, 2, 3]
    assert all(isinstance(c.exact, int) for c in view.newton.coords)
    n2 = view.newton.coords[2]
    assert n2.valuation is not None
    assert n2.bar
    assert view.digits == (0, 0, 0, 0, 0, 0, 0)


def test_valuations_and_phi_match_authoritative():
    f = parse_poly("x^3")
    word = (1, 0, -1)
    view = inspect_node(f, word, 6)
    assert view.state.p == pack_word(word)
    assert F_k(view.state.m, view.state.p, 6) == tuple(
        c.mod_value for c in view.newton.coords
    )


def test_fibre_of_known_x3_class():
    f = parse_poly("x^3")
    view = fibre_view(f, (1,), 2)
    prefixes = sorted(m.p for m in view.members)
    assert prefixes == [-1, 1]
    assert view.size == 2
    assert any("same Φ_k" in line or "equal" in line for line in view.criterion)


def test_compare_two_states():
    f = parse_poly("x^3")
    view = compare_states(f, (1,), (-1,), 3)
    assert view.same_class is False
    assert view.first_difference is not None
    assert any(not row.equal for row in view.newton_rows)
    assert view.difference_poly
    assert view.tau == 3


def test_delayed_distinction_splits_when_k_increases():
    f, wa, wb = demo_delayed_pair()
    merged = compare_states(f, wa, wb, 2)
    split = compare_states(f, wa, wb, 3)
    assert merged.same_class is True
    assert split.same_class is False
    assert merged.tau == 3
    assert split.tau == 3
    assert split.same_through == 2
    assert first_distinction_horizon(residual_of(f, wa), residual_of(f, wb)) == 3


def test_x2_census_has_no_merges():
    view = census_view(parse_poly("x^2"), 8)
    assert view.computed
    assert view.raw == view.observable == (3**8 - 1) // 2
    assert view.merged == 0
    assert view.badge is not None
    assert view.badge["id"] == "BTA-x2-mn"


def test_x3_census_matches_image_profile():
    view = census_view(parse_poly("x^3"), 4)
    rec = image_profile(4)
    assert view.raw == rec["R"]
    assert view.observable == rec["M"]
    assert view.merged == rec["collisions"]
    assert view.merged > 0


def test_x2_vs_x3_dual_census():
    x2, x3 = dual_census(4)
    assert x2.merged == 0
    assert x3.merged and x3.merged > 0


def test_expensive_census_is_opt_in():
    skipped = census_view(parse_poly("x^3"), 14)
    assert skipped.computed is False
    assert skipped.raw == (3**14 - 1) // 2
    assert "expensive" in skipped.warning.lower() or "enumerates" in skipped.warning.lower()


def test_tree_is_lazy_and_svg_marks_selection():
    f = parse_poly("x^3")
    nodes = visible_subtree(f, 10)
    assert len(nodes) <= 40
    assert any(n.id == "ε" for n in nodes)
    focused = visible_subtree(f, 10, focus_depth=7)
    depths = {n.depth for n in focused}
    assert 7 in depths
    assert len(focused) < 80
    svg = tree_svg(nodes, selected_id="ε")
    assert svg.startswith("<svg")
    assert "Residual prefix tree" in svg
    merged = filter_nodes(nodes, merged_only=True)
    assert all(n.merged_visible for n in merged)


def test_expand_subtree_is_capped():
    words = expand_subtree_words((), 10, cap=20)
    assert () in words
    assert len(words) <= 20
    assert all(len(w) < 10 for w in words)


def test_word_format_roundtrip():
    assert format_word(()) == "ε"
    assert parse_word("ε") == ()
    assert parse_word("-+0") == (-1, 1, 0)
    assert prefix_digits(0, 3) == (0, 0, 0)
    assert prefix_digits(1, 1) == (1,)


def test_calculus_explorer_cli_is_registered():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    add_calculus_subparser(sub)
    args = parser.parse_args(["calculus", "explorer"])
    assert args.cal_cmd == "explorer"


def test_theorem_ledger_distinguishes_claim_kinds():
    vis = theorem_entry("BTA-x3-vis")
    assert vis is not None
    assert vis["tag"] == "EXACT — LEAN VERIFIED"
    assert claim_kind(vis["tag"]) == "exact"
    refuted = badge_payload("BTA-x3-def2-n21n0")
    assert refuted is not None
    assert refuted["kind"] == "refuted"
    assert claim_kind(refuted["tag"]) != claim_kind(vis["tag"])
