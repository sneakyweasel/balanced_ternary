"""Rewrite-calculus companion instantiates Lean witnesses; it does not add rules."""

from visualization.rewrite_explorer import (
    EXACT_TRIPLES,
    OPERATOR_HELP,
    UNARY_OPS,
    UNARY_PRESETS,
    constructor_sum_view,
    carry_view,
    normalize_unary,
    push_in_peak,
    step_unary,
    unary_from_ops,
    wrap_unary,
)


def test_operator_help_covers_unary_ops():
    assert tuple(OPERATOR_HELP) == UNARY_OPS


def test_carry_witness_matches_lean():
    z = carry_view(0, 0)
    o = carry_view(1, 1)
    assert z.d_x == z.d_y == o.d_x == o.d_y == 0
    assert z.d_sum == 0
    assert o.d_sum == 1
    assert o.d_sum != o.d_sum_naive
    assert o.not_d_local_witness
    assert not z.not_d_local_witness


def test_same_sign_ip_is_not_exact():
    view = constructor_sum_view("I+", "I+", "S")
    assert not view.exact
    assert view.residue == 2
    assert constructor_sum_view("S", "S", "S").exact
    assert ("I+", "S", "I+") in EXACT_TRIPLES


def test_push_in_peak_twins():
    view = push_in_peak(2, 3)
    assert view.left_value == 5
    assert view.right_value == 5
    assert view.agree


def test_unary_nd_normalizes_to_dn():
    term = unary_from_ops(UNARY_PRESETS["N(D(x))"])
    nf, reasons, steps = normalize_unary(term)
    assert nf.render() == "D(N(x))"
    assert steps >= 1
    assert any("N(D" in r for r in reasons)


def test_unary_step_and_wrap():
    raw = unary_from_ops(())
    wrapped = wrap_unary(wrap_unary(raw, "S"), "D")
    assert wrapped.render() == "D(S(x))"
    nxt, reason = step_unary(wrapped)
    assert nxt.render() == "x"
    assert reason is not None
