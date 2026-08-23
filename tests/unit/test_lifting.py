"""Lifting trees of ``f(x) = 0 (mod 3^k)`` in the residual section calculus."""

from __future__ import annotations

import itertools

import pytest

from bt.calculus.lifting import (
    KINDS,
    brute_force_roots,
    depth_r_shape,
    derivative,
    divides_at_level,
    is_lift_node,
    level_counts,
    level_nodes,
    lift_children,
    lift_kind,
    lift_records,
    lift_tree,
    node_at,
    shape_widths,
    taylor_coeff,
    unordered_shape,
    tree_roots,
    word_digits,
    word_value,
)
from bt.calculus.poly_congruence import function_equiv, phi_k
from bt.calculus.section import IntPoly, parse_poly

FAMILY = [
    parse_poly(text)
    for text in ("x^2-1", "x^2-3", "x^2-9", "x^3-1", "x^3-x", "x^3-3", "x^4-1", "2x^4-x^2+5")
]


def _words(k: int):
    return itertools.product((-1, 0, 1), repeat=k)


def test_derivative_and_taylor_agree():
    f = parse_poly("2x^4-x^2+5")
    assert derivative(f).coeffs == (0, -2, 0, 8)
    for n in range(-4, 5):
        assert taylor_coeff(f, n, 0) == f.eval(n)
        assert taylor_coeff(f, n, 1) == derivative(f).eval(n)


def test_derivative_of_constant_is_zero():
    assert derivative(IntPoly.C(7)).coeffs == (0,)


def test_word_value_and_digits():
    assert word_value((1, 0, -1)) == 1 - 9
    assert word_digits((1, 0, -1)) == "-0+"
    assert word_digits(()) == ""


def test_word_rejects_non_trits():
    with pytest.raises(ValueError):
        word_value((2,))


# H1: the lifting tree is the zero-output subtree of the residual machine.

@pytest.mark.parametrize("f", FAMILY)
def test_zero_output_iff_divisible(f):
    for k in range(5):
        for word in _words(k):
            assert is_lift_node(f, word) == divides_at_level(f, word)


@pytest.mark.parametrize("f", FAMILY)
def test_tree_roots_match_brute_force(f):
    for k in range(7):
        assert tree_roots(f, k) == brute_force_roots(f, k)


def test_tree_nodes_are_all_lift_nodes():
    f = parse_poly("x^4-x^2")
    for node in lift_tree(f, 5):
        assert is_lift_node(f, node.word)
        assert node.f_value % node.modulus == 0


def test_level_counts_of_fermat_cubic():
    # x^3 - x vanishes mod 3 as a function, so the root splits three ways
    # and every branch then lifts uniquely.
    assert level_counts(parse_poly("x^3-x"), 6) == (1, 3, 3, 3, 3, 3, 3)


def test_pre_lifting_tail_of_scaled_fermat_cubic():
    # 3(x^3 - x) vanishes mod 9 as a function: two full levels survive.
    assert level_counts(parse_poly("3x^3-3x"), 3)[:3] == (1, 3, 9)


def test_terminating_branch():
    f = parse_poly("x^2+3")
    assert level_counts(f, 4) == (1, 1, 0, 0, 0)


# H2: the residual state is the scaled Taylor jet.

@pytest.mark.parametrize("f", FAMILY)
def test_residual_is_scaled_taylor_jet(f):
    for k in range(4):
        for word in _words(k):
            node = node_at(f, word)
            for j in range(1, f.degree + 1):
                assert node.residual.coefficient(j) == 3 ** (k * (j - 1)) * taylor_coeff(
                    f, node.residue, j
                )


@pytest.mark.parametrize("f", FAMILY)
def test_linear_coefficient_is_the_derivative(f):
    for k in range(4):
        for word in _words(k):
            node = node_at(f, word)
            assert node.residual.coefficient(1) == node.f_prime


def test_constant_coefficient_is_scaled_value_on_the_tree():
    f = parse_poly("x^2-9")
    for node in lift_tree(f, 5):
        assert node.residual.coefficient(0) == node.scaled_value
        assert node.scaled_value * node.modulus == node.f_value


def test_scaled_value_rejects_non_lift_node():
    node = node_at(parse_poly("x^2+1"), (0,))
    with pytest.raises(ValueError):
        node.scaled_value


# H3: the classical one-step trichotomy.

@pytest.mark.parametrize("f", FAMILY)
def test_one_step_trichotomy(f):
    for node in lift_tree(f, 6):
        if node.level == 0:
            continue
        count = len(node.children)
        if not node.singular:
            assert count == 1
        elif node.v3_f is None or node.v3_f >= node.level + 1:
            assert count == 3
        else:
            assert count == 0


def test_nonsingular_family_has_only_unique_lifts():
    # f' = 3x^2 - 1 is a unit at every integer.
    for f in (parse_poly("x^3-x-1"), parse_poly("x^3-x-3")):
        for node in lift_tree(f, 6):
            if node.level >= 1:
                assert len(node.children) == 1
                assert node.kind == "unique"


def test_singular_family_never_lifts_uniquely():
    # f' = 3x^2 is divisible by 3 at every integer.
    for node in lift_tree(parse_poly("x^3-9"), 5):
        if node.level >= 1:
            assert len(node.children) in {0, 3}
            assert node.kind in {"terminal", "singular-persistent"}


def test_level_zero_escapes_the_trichotomy():
    # x(x+1) has two roots mod 3 and a unit derivative at 0, a count the
    # one-step trichotomy forbids at every level above the root.
    node = node_at(parse_poly("x^2+x"), ())
    assert node.children == (-1, 0)
    assert not node.singular
    assert node.kind == "splitting"
    # x^2 - 1 also has two children, but singular at the origin.
    singular_root = node_at(parse_poly("x^2-1"), ())
    assert len(singular_root.children) == 2
    assert singular_root.kind == "singular-persistent"


def test_lift_kind_is_total():
    for count in (0, 1, 2, 3):
        for singular in (False, True):
            assert lift_kind(count, singular) in KINDS


# H4: finite-horizon determinacy of the subtree.

def test_phi_r_determines_depth_r_subtree():
    seen: dict[tuple, tuple] = {}
    for f in FAMILY:
        for node in lift_tree(f, 5):
            key = phi_k(node.residual, 3) + (0,) * (12 - len(phi_k(node.residual, 3)))
            shape = depth_r_shape(node.residual, 3)
            assert seen.setdefault(key, shape) == shape


def test_phi_r_minus_one_does_not_determine_depth_r_subtree():
    # x^2 and x^2 - 3 agree on Phi_1 but not at depth 2.
    f, g = parse_poly("x^2"), parse_poly("x^2-3")
    assert function_equiv(f, g, 1)
    assert not function_equiv(f, g, 2)
    assert depth_r_shape(f, 1) == depth_r_shape(g, 1)
    assert depth_r_shape(f, 2) != depth_r_shape(g, 2)


def test_valuations_do_not_determine_the_subtree():
    # x^2 + 9 and x^2 - 9 at the level-1 node 0: identical valuations,
    # different lifting behaviour, because -1 is not a square mod 3.
    plus = node_at(parse_poly("x^2+9"), (0,))
    minus = node_at(parse_poly("x^2-9"), (0,))
    assert plus.v3_f == minus.v3_f == 2
    assert plus.v3_f_prime is None and minus.v3_f_prime is None
    assert abs(plus.scaled_value) == abs(minus.scaled_value) == 3
    assert depth_r_shape(plus.residual, 2, mode="unordered") != depth_r_shape(
        minus.residual, 2, mode="unordered"
    )
    assert shape_widths(plus.residual, 2) == (3, 0)
    assert shape_widths(minus.residual, 2) == (3, 6)


def test_deep_residual_is_congruent_to_its_linear_surrogate():
    for f in FAMILY:
        for r in (1, 2, 3):
            for node in lift_tree(f, 5):
                if node.level < r:
                    continue
                assert function_equiv(node.residual, node.linear_surrogate(), r)


def test_shape_modes_are_ordered_by_strength():
    f = IntPoly((3, 3))
    g = IntPoly((12, 3))
    assert depth_r_shape(f, 3, mode="unordered") == depth_r_shape(g, 3, mode="unordered")
    assert unordered_shape(f, 3) == depth_r_shape(f, 3, mode="unordered")
    assert depth_r_shape(f, 3, mode="positional") != depth_r_shape(g, 3, mode="positional")


def test_unknown_shape_mode_rejected():
    with pytest.raises(ValueError):
        depth_r_shape(IntPoly((1, 1)), 1, mode="nope")


def test_shape_widths_pads_after_extinction():
    assert shape_widths(parse_poly("x^2+1"), 3) == (0, 0, 0)


def test_children_and_records():
    f = parse_poly("x^3-x")
    root = node_at(f, ())
    kids = lift_children(f, root)
    assert tuple(kid.residue for kid in kids) == (-1, 0, 1)
    assert all(kid.parent_word == () for kid in kids)
    records = lift_records(lift_tree(f, 2))
    assert records[0]["digits"] == "e"
    assert {rec["kind"] for rec in records} <= set(KINDS)


def test_level_nodes_selects_one_level():
    nodes = lift_tree(parse_poly("x^3-x"), 3)
    assert len(level_nodes(nodes, 0)) == 1
    assert len(level_nodes(nodes, 3)) == 3
