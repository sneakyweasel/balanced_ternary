"""Minimal finite-horizon state of the 3-adic lifting machine."""

from __future__ import annotations

import itertools

import pytest

from bt.calculus.lifting import depth_r_shape, lift_tree, node_at
from bt.calculus.lifting_state import (
    behaviour_class,
    behaviour_count,
    behaviour_count_formula,
    behaviour_depth,
    behaviour_equivalent,
    behaviours_by_derivative_valuation,
    block_shift,
    capped_valuation,
    deep_behaviours,
    deep_leaf,
    dominated_count,
    drop_lsd,
    is_dead,
    is_dominated,
    linear_children,
    linear_state,
    linear_step,
    linear_survives,
    minimal_state_key,
    newton_path,
    newton_quotient,
    row_overlap,
    shift_window,
    truncated_tree,
    undominated_count,
    unit_normal_form,
    unit_normal_pair,
    unit_orbit_count,
    unit_scale,
    units_mod,
    valuation_row_formula,
)
from bt.calculus.poly_congruence import function_equiv, phi_equal, phi_k
from bt.calculus.residual import TRITS, delta, residual_along
from bt.calculus.section import IntPoly, parse_poly, rho_int

STATES = [
    IntPoly(coeffs)
    for coeffs in (
        (0, 1),
        (1, 1),
        (-3, 3),
        (3, 3),
        (-9, 0),
        (9, 0),
        (0, 3),
        (1, 0),
        (-1, 0),
        (2, 5),
        (-6, 9),
        (4, -7),
    )
] + [parse_poly(t) for t in ("x^2-3", "x^3-x", "2x^4-x^2+5", "x^2+9", "x^2-9")]

UNITS = (-8, -7, -5, -4, -2, -1, 2, 4, 5, 7, 8)


# ------------------------------------------------- behaviour as observable

def test_behaviour_class_is_the_ordered_digit_shape():
    for g in STATES:
        for r in range(4):
            assert behaviour_class(g, r) == depth_r_shape(g, r, mode="digits")


def test_behaviour_equivalence_is_reflexive_symmetric_transitive():
    # It is a fibre of a function, so this is a sanity check, not a proof.
    for g, h in itertools.combinations(STATES, 2):
        assert behaviour_equivalent(g, g, 3)
        assert behaviour_equivalent(g, h, 3) == behaviour_equivalent(h, g, 3)
    for g, h, i in itertools.combinations(STATES[:6], 3):
        if behaviour_equivalent(g, h, 3) and behaviour_equivalent(h, i, 3):
            assert behaviour_equivalent(g, i, 3)


def test_dead_states_have_empty_behaviour_at_every_horizon():
    dead = IntPoly((1, 0))
    assert is_dead(dead)
    for r in range(5):
        assert behaviour_class(dead, r) == ()
    assert behaviour_depth(dead, 4) == 0


def test_behaviour_depth_counts_surviving_levels():
    # x^2 - 9 at the origin dies after two more levels on some branches.
    assert behaviour_depth(IntPoly((-9, 0)), 4) == 2
    assert behaviour_depth(IntPoly((0, 1)), 4) == 4


# --------------------------------------------------------- unit scaling

@pytest.mark.parametrize("r", (1, 2, 3, 4))
def test_unit_scaling_preserves_the_behaviour(r):
    for g in STATES:
        for lam in UNITS:
            assert behaviour_class(unit_scale(g, lam), r) == behaviour_class(g, r)


def test_unit_scaling_rejects_multiples_of_three():
    with pytest.raises(ValueError):
        unit_scale(IntPoly((1, 1)), 3)


def test_scaling_by_three_does_change_the_behaviour():
    g = IntPoly((1, 1))
    assert behaviour_class(g.scale(3), 2) != behaviour_class(g, 2)


def test_unit_scaling_moves_the_jet():
    # The invariance is not because Phi_r is preserved; it plainly is not.
    moved = 0
    for g in STATES:
        for lam in UNITS:
            for r in (1, 2, 3):
                if not phi_equal(g, unit_scale(g, lam), r):
                    moved += 1
    assert moved > 0


def test_phi_r_is_not_minimal_smallest_live_witness():
    # x and -x: both live, identical futures at every horizon, different
    # Newton jets. This is the unit-scaling orbit with lambda = -1, and it
    # is the smallest live witness over all linear states with |c|,|b| <= 13.
    g, h = IntPoly((0, 1)), IntPoly((0, -1))
    assert not is_dead(g) and not is_dead(h)
    for r in (1, 2, 3, 4, 5):
        assert behaviour_class(g, r) == behaviour_class(h, r)
        assert not phi_equal(g, h, r)
    assert behaviour_class(g, 3) == ((0, ((0, ((0, ()),)),)),)


def test_trivial_dead_witness_is_separate_from_the_live_one():
    # 1 and -1 are also jet-redundant, but only because both are dead;
    # such pairs are noise and must not be reported as the witness.
    g, h = IntPoly((1,)), IntPoly((-1,))
    assert is_dead(g) and is_dead(h)
    assert behaviour_class(g, 3) == behaviour_class(h, 3) == ()
    assert not phi_equal(g, h, 1)


def test_unit_orbits_are_coarser_than_phi_but_finer_than_behaviour():
    for r in (2, 3, 4):
        assert unit_orbit_count(r) == 2 * 3**r - 1
        assert unit_orbit_count(r) < 3 ** (2 * r)
        assert behaviour_count(r) < unit_orbit_count(r)
    # At r = 1 the two quotients happen to coincide.
    assert behaviour_count(1) == unit_orbit_count(1) == 5


def test_unit_normal_form_is_constant_on_an_orbit():
    for r in (1, 2, 3):
        for lam in units_mod(r):
            assert unit_normal_form(2, 5, r) == unit_normal_form(2 * lam, 5 * lam, r)


def test_unit_normal_form_needs_a_positive_horizon():
    with pytest.raises(ValueError):
        unit_normal_form(1, 1, 0)


# ------------------------------------------------ linear state dynamics

def test_linear_states_are_closed_under_the_section_operator():
    # D_a(c + bx) = D(c + ab) + bx, so b is invariant along the tree.
    for c in range(-9, 10):
        for b in range(-9, 10):
            for a in TRITS:
                got = delta(linear_state(c, b), a)
                assert got.coeffs == IntPoly((drop_lsd(c + a * b), b)).coeffs


def test_linear_step_agrees_with_the_section_operator_on_survivors():
    for c in range(-13, 14):
        for b in range(-13, 14):
            for a in TRITS:
                survives = linear_survives(c, b, a)
                assert survives == (linear_state(c, b).rho(a) == 0)
                if not survives:
                    with pytest.raises(ValueError):
                        linear_step(c, b, a)
                    continue
                nxt = linear_step(c, b, a)
                assert nxt == ((c + a * b) // 3, b)
                assert delta(linear_state(c, b), a).coeffs == IntPoly(nxt).coeffs


def test_linear_children_match_the_lifting_tree():
    for c in (-9, -3, 0, 1, 3, 9):
        for b in (0, 1, 3, -1, 9):
            kids = linear_children(c, b)
            assert tuple(a for a, _ in kids) == tuple(
                a for a in TRITS if linear_state(c, b).rho(a) == 0
            )


def test_derivative_valuation_is_invariant_along_the_tree():
    for c in range(-27, 28):
        for b in (0, 1, 3, 9, 27, -3, -9):
            for a, (_c2, b2) in linear_children(c, b):
                assert b2 == b
                assert a in TRITS


def test_singular_linear_branching_is_all_or_nothing():
    for c in range(-27, 28):
        for b in (0, 3, 9, -3, 27):
            count = len(linear_children(c, b))
            assert count == (3 if c % 3 == 0 else 0)


def test_linear_survives_rejects_non_trits():
    with pytest.raises(ValueError):
        linear_survives(1, 1, 2)


# -------------------------------------------------- Newton reformulation

def test_drop_lsd_is_the_section_of_an_integer():
    for n in range(-40, 41):
        assert 3 * drop_lsd(n) + rho_int(n) == n


@pytest.mark.parametrize("r", (1, 2, 3, 4))
def test_nonsingular_behaviour_depends_only_on_the_newton_quotient(r):
    seen: dict[int, tuple] = {}
    mod = 3**r
    for b in range(mod):
        if b % 3 == 0:
            continue
        for c in range(mod):
            u = newton_quotient(c, b, r)
            shape = behaviour_class(linear_state(c, b), r)
            assert seen.setdefault(u, shape) == shape
    assert len(seen) == mod
    assert len(set(seen.values())) == mod


@pytest.mark.parametrize("r", (1, 2, 3, 4))
def test_nonsingular_path_is_the_balanced_expansion_of_minus_the_quotient(r):
    mod = 3**r
    for b in range(1, mod, 1):
        if b % 3 == 0:
            continue
        for c in range(0, mod, max(mod // 27, 1)):
            path = newton_path(c, b, r)
            shape = behaviour_class(linear_state(c, b), r)
            walk: list[int] = []
            layer = shape
            while layer:
                assert len(layer) == 1
                a, sub = layer[0]
                walk.append(a)
                layer = sub
            assert tuple(walk) == path


def test_newton_path_reproduces_a_real_hensel_lift():
    # x^2 - 7 has a 3-adic square root, and every node of its tree is
    # nonsingular, so the Newton path must be the actual continuation.
    f = parse_poly("x^2-7")
    nodes = [n for n in lift_tree(f, 3) if n.level == 3]
    assert nodes
    for node in nodes:
        c, b = node.scaled_value, node.f_prime
        assert b % 3 != 0
        cur = node.word
        for a in newton_path(c, b, 3):
            cur = cur + (a,)
            assert node_at(f, cur).f_value % (3 ** len(cur)) == 0


def test_newton_quotient_requires_a_unit_derivative():
    with pytest.raises(ValueError):
        newton_quotient(1, 3, 2)
    with pytest.raises(ValueError):
        newton_path(1, 3, 2)


# ------------------------------------------------------- exact counting

@pytest.mark.parametrize("r", (0, 1, 2, 3, 4, 5))
def test_behaviour_count_matches_the_closed_form(r):
    assert behaviour_count(r) == behaviour_count_formula(r)


def test_behaviour_counts_are_the_recorded_sequence():
    assert [behaviour_count(r) for r in range(1, 6)] == [5, 15, 43, 125, 369]
    assert [3 ** (2 * r) for r in range(1, 6)] == [9, 81, 729, 6561, 59049]


@pytest.mark.parametrize("r", (1, 2, 3, 4))
def test_valuation_rows_match_the_closed_form(r):
    rows = behaviours_by_derivative_valuation(r)
    assert set(rows) == set(range(r + 1))
    for e, count in rows.items():
        assert count == valuation_row_formula(r, e)


@pytest.mark.parametrize("r", (1, 2, 3, 4))
def test_valuation_rows_overlap_by_a_triangular_number(r):
    rows = behaviours_by_derivative_valuation(r)
    assert sum(rows.values()) - behaviour_count(r) == row_overlap(r)


def test_nonsingular_row_is_the_newton_coordinate_count():
    for r in (1, 2, 3, 4):
        assert behaviours_by_derivative_valuation(r)[0] == 3**r


def test_deep_behaviours_are_exactly_the_counted_set():
    for r in (1, 2, 3):
        found = deep_behaviours(r)
        assert len(found) == behaviour_count(r)
        assert len(set(found)) == len(found)


def test_valuation_row_formula_rejects_e_above_r():
    with pytest.raises(ValueError):
        valuation_row_formula(2, 3)


# --------------------------------------- the deep regime really is linear

def test_deep_nodes_reduce_to_their_linear_surrogate():
    # The bridge from real polynomials to the linear state space.
    for text in ("x^2-9", "x^3-x", "x^2-7", "2x^4-x^2+5"):
        f = parse_poly(text)
        for r in (1, 2, 3):
            for node in lift_tree(f, 5):
                if node.level < r:
                    continue
                surrogate = node.linear_surrogate()
                assert function_equiv(node.residual, surrogate, r)
                assert behaviour_class(node.residual, r) == behaviour_class(surrogate, r)


def test_deep_node_behaviour_is_within_the_counted_set():
    for text in ("x^2-9", "x^3-x", "x^2-7", "x^4-1"):
        f = parse_poly(text)
        for r in (1, 2, 3):
            known = set(deep_behaviours(r))
            for node in lift_tree(f, 5):
                if node.level >= r:
                    assert behaviour_class(node.residual, r) in known


def test_phi_r_still_determines_the_behaviour():
    # Sufficiency from the earlier phase must survive; only minimality fails.
    seen: dict[tuple, tuple] = {}
    for g in STATES:
        for r in (1, 2, 3):
            key = (r, phi_k(g, r) + (0,) * (8 - len(phi_k(g, r))))
            shape = behaviour_class(g, r)
            assert seen.setdefault(key, shape) == shape


# ------------------------------------------------------- block shift law


@pytest.mark.parametrize("e", [1, 2, 3])
def test_leaf_shift_is_the_balanced_value_of_the_word(e):
    for d in range(-5, 6):
        state = linear_state(3**e * d, 3**e)
        for word in itertools.product(TRITS, repeat=e):
            leaf = residual_along(state, word)
            assert leaf.coeffs == linear_state(d + block_shift(word), 3**e).coeffs


@pytest.mark.parametrize("e", [2, 3])
def test_leaf_shift_is_not_the_digit_sum(e):
    # The digit sum was the plausible guess and it is wrong; the distinction
    # matters because it changes the shift window from 2e+1 to 3^e values.
    mismatches = 0
    for d in range(-5, 6):
        state = linear_state(3**e * d, 3**e)
        for word in itertools.product(TRITS, repeat=e):
            leaf = residual_along(state, word)
            if leaf.coeffs != linear_state(d + sum(word), 3**e).coeffs:
                mismatches += 1
    assert mismatches > 0


@pytest.mark.parametrize("e", [1, 2, 3, 4])
def test_shift_window_is_a_complete_residue_system_mod_three_to_the_e(e):
    window = shift_window(e)
    assert len(window) == 3**e
    assert window == tuple(sorted(window))
    assert sorted(block_shift(w) for w in itertools.product(TRITS, repeat=e)) == list(window)
    assert sorted(t % 3**e for t in window) == list(range(3**e))


@pytest.mark.parametrize("e", [1, 2, 3])
def test_exactly_one_window_shift_reaches_the_next_block(e):
    for d in range(3 ** (e + 1)):
        deep = [t for t in shift_window(e) if deep_leaf(d + t, e)]
        assert len(deep) == 1


@pytest.mark.parametrize("e", [1, 2, 3])
def test_intermediate_block_shift_law(e):
    # The induction that proves the leaf law needs the (j, i) generalisation.
    for j in range(1, e + 1):
        i = e - j
        for d in range(-4, 5):
            state = linear_state(3**j * d, 3 ** (j + i))
            for word in itertools.product(TRITS, repeat=j):
                leaf = residual_along(state, word)
                want = linear_state(d + 3**i * block_shift(word), 3 ** (j + i))
                assert leaf.coeffs == want.coeffs


# ------------------------------------------------------- separation


@pytest.mark.parametrize(("e", "horizon"), [(1, 3), (1, 4), (2, 2), (2, 3), (3, 2)])
def test_shifted_family_separates_residues(e, horizon):
    window = shift_window(e)
    seen: dict[tuple, int] = {}
    for d in range(3**horizon):
        key = tuple(behaviour_class(linear_state(d + t, 3**e), horizon) for t in window)
        assert key not in seen, f"d={d} collides with d={seen.get(key)}"
        seen[key] = d
    assert len(seen) == 3**horizon


@pytest.mark.parametrize(("e", "horizon"), [(1, 3), (2, 3), (2, 4), (3, 4)])
def test_the_recursing_leaf_is_the_unique_tall_one(e, horizon):
    for d in range(3 ** min(horizon, 3)):
        window = shift_window(e)
        deep = [t for t in window if deep_leaf(d + t, e)]
        tall = [
            t
            for t in window
            if behaviour_depth(linear_state(d + t, 3**e), horizon) >= min(e, horizon)
        ]
        assert tall == deep


# ------------------------------------------------------- minimal state


def test_capped_valuation_saturates_at_the_horizon():
    assert capped_valuation(0, 3) == 3
    assert capped_valuation(27, 3) == 3
    assert capped_valuation(9, 3) == 2
    assert capped_valuation(5, 3) == 0
    assert capped_valuation(-3, 3) == 1


@pytest.mark.parametrize("r", [1, 2, 3])
def test_unit_normal_pair_scales_the_derivative_to_a_power_of_three(r):
    mod = 3**r
    for b in range(mod):
        e, _ = unit_normal_pair(0, b, r)
        assert e == capped_valuation(b, r)
        for c in range(mod):
            e2, cn = unit_normal_pair(c, b, r)
            assert e2 == e
            if e < r:
                beta = (b % mod) // 3**e
                assert (b * pow(beta, -1, mod)) % mod == 3**e % mod
                assert (c * pow(beta, -1, mod)) % mod == cn


@pytest.mark.parametrize("r", [1, 2, 3])
def test_minimal_state_key_is_a_complete_invariant(r):
    mod = 3**r
    key_to_shape: dict[tuple, tuple] = {}
    shape_to_key: dict[tuple, tuple] = {}
    for b in range(mod):
        for c in range(mod):
            key = minimal_state_key(c, b, r)
            shape = behaviour_class(linear_state(c, b), r)
            assert key_to_shape.setdefault(key, shape) == shape
            shape_to_key.setdefault(shape, key)
    assert len(key_to_shape) == len(shape_to_key) == behaviour_count_formula(r)


@pytest.mark.parametrize("r", [1, 2, 3])
def test_dominated_stratum_collapses_to_the_valuation(r):
    mod = 3**r
    for b in range(mod):
        for c in range(mod):
            if not is_dominated(c, b, r):
                continue
            m = capped_valuation(c, r)
            assert m < capped_valuation(b, r)
            assert behaviour_class(linear_state(c, b), r) == truncated_tree(m, r)


@pytest.mark.parametrize("r", [1, 2, 3])
def test_undominated_stratum_is_exactly_the_unit_orbit(r):
    mod = 3**r
    units = [u for u in range(mod) if u % 3]
    orbit_to_shape: dict[tuple[int, int], tuple] = {}
    shape_to_orbit: dict[tuple, tuple[int, int]] = {}
    for b in range(mod):
        for c in range(mod):
            if is_dominated(c, b, r):
                continue
            orbit = min(((c * u) % mod, (b * u) % mod) for u in units)
            shape = behaviour_class(linear_state(c, b), r)
            assert orbit_to_shape.setdefault(orbit, shape) == shape
            shape_to_orbit.setdefault(shape, orbit)
    assert len(orbit_to_shape) == len(shape_to_orbit) == undominated_count(r)


@pytest.mark.parametrize("r", [0, 1, 2, 3, 4, 5])
def test_strata_counts_add_up_to_the_minimal_count(r):
    assert dominated_count(r) + undominated_count(r) == behaviour_count_formula(r)


def test_dominated_states_are_insensitive_to_the_derivative():
    # The point of the collapse: c = 3 dies at depth 1 whatever b is.
    shapes = {behaviour_class(linear_state(3, b), 3) for b in (9, 18, 27, 45, 81)}
    assert shapes == {truncated_tree(1, 3)}
