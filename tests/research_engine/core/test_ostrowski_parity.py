"""Generic affine/block operations match the Ostrowski reference implementation."""

from __future__ import annotations

from research.ostrowski.control_language import affine_block, affine_holds, matrix_power
from research.ostrowski.energy_trajectory import apply_word
from research.ostrowski.spectral_residual import (
    apply_matrix,
    residual_matrix,
    transition_affine,
)
from research.ostrowski.system import nonpisot_order3, phase0_order3
from research.ostrowski.zero_value_kernel import HUB, SHORTEST_NONRESET
from research_engine.core.affine_system import (
    affine_step,
    apply_matrix as engine_apply_matrix,
    iterate_affine_word,
    matrix_power as engine_matrix_power,
)
from research_engine.core.block import block_action_of_word, compose_blocks


def _translation(control: int) -> tuple[int, int, int]:
    return (0, 0, -control)


def test_apply_matrix_and_transition_match_engine_primitives():
    for system in (phase0_order3(), nonpisot_order3()):
        matrix = residual_matrix(system)
        for state in ((0, 0, 0), (1, -1, 2), (-2, 3, -1)):
            assert apply_matrix(matrix, state) == engine_apply_matrix(matrix, state)
            for w in range(-4, 3):
                assert transition_affine(system, state, w) == affine_step(
                    matrix, state, _translation(w)
                )


def test_apply_word_matches_generic_iteration():
    system = nonpisot_order3()
    matrix = residual_matrix(system)
    samples = ((), (0,), (1, -2), SHORTEST_NONRESET, (1, 0, -2, 1))
    for word in samples:
        image = apply_word(system, (0, 0, 0), word)
        generic = iterate_affine_word(matrix, (0, 0, 0), word, _translation)
        assert image == generic
        action = block_action_of_word(matrix, word, _translation)
        assert action.apply((0, 0, 0)) == image
        assert action.apply((1, -2, 3)) == apply_word(system, (1, -2, 3), word)
        assert affine_holds(word, (1, -2, 3))


def test_affine_block_matches_generic_block_action():
    system = nonpisot_order3()
    matrix = residual_matrix(system)
    word = (1, -2, 0)
    data = affine_block(word)
    action = block_action_of_word(matrix, word, _translation)
    assert data["A_k"] == action.matrix == engine_matrix_power(matrix, len(word))
    assert data["c_B"] == action.translation == apply_word(system, (0, 0, 0), word)
    assert matrix_power(matrix, 5) == engine_matrix_power(matrix, 5)


def test_hub_word_uses_affine_composition_not_naive_concat():
    system = nonpisot_order3()
    matrix = residual_matrix(system)
    first = block_action_of_word(matrix, (1,), _translation)
    second = block_action_of_word(matrix, (-2,), _translation)
    composed = compose_blocks(first, second)
    concatenated = block_action_of_word(matrix, SHORTEST_NONRESET, _translation)
    naive = (
        first.translation[0] + second.translation[0],
        first.translation[1] + second.translation[1],
        first.translation[2] + second.translation[2],
    )
    assert SHORTEST_NONRESET == (1, -2)
    assert concatenated.translation == HUB == (-3, -1, 0)
    assert composed.translation == HUB
    assert naive == (0, 0, 1)
    assert naive != HUB
    assert apply_word(system, (0, 0, 0), SHORTEST_NONRESET) == HUB


def test_forward_live_layers_match_ostrowski_remaining_four():
    from research.ostrowski.ext_feasibility import live_ext, live_ext_by_oracle
    from research.ostrowski.live_layers import ORIGIN, forward_layers
    from research.ostrowski.spec import ostrowski_spec
    from research_engine.acceptance.suffix import live_extensions
    from research_engine.core.phase import IntPhase
    from research_engine.core.semantics import ClaimKind, SearchScope
    from research_engine.reachability.forward import forward_search

    system = nonpisot_order3()
    report = forward_layers(system, 4, live_only=True)
    result = forward_search(ostrowski_spec(4, system), live_only=True)
    assert result.scope == SearchScope.BOUNDED
    assert result.kind == ClaimKind.LIVE_SLICE
    assert result.complete
    assert result.union != result.terminal_image
    for n in range(5):
        layer = result.layer_at(IntPhase(n))
        assert len(layer) == report["layers"][n]["R"] == report["layers"][n]["L"]
    assert live_ext(ORIGIN, 4) == live_ext_by_oracle(ORIGIN, 4)
    assert live_extensions(ostrowski_spec(4, system), ORIGIN, IntPhase(4)) == live_ext_by_oracle(
        ORIGIN, 4
    )


def test_recurrence_and_lattice_inverse_match_ostrowski():
    from fractions import Fraction

    from research.ostrowski.energy_geometry import adjoint_u, mat_vec_left
    from research.ostrowski.recurrence import (
        companion_matches_residual,
        recurrence_matches_place_values,
        recurrence_spec,
    )
    from research.ostrowski.reverse_map import integer_preimage, np_inverse_matrix
    from research.ostrowski.spectral_residual import charpoly_of_matrix
    from research_engine.algebra.lattices import characteristic_polynomial, integer_affine_preimage
    from research_engine.algebra.linear_functionals import left_multiply

    for system in (phase0_order3(), nonpisot_order3()):
        assert recurrence_matches_place_values(system, 8)
        assert companion_matches_residual(system)
        spec = recurrence_spec(system)
        assert spec is not None
        matrix = residual_matrix(system)
        assert spec.companion_matrix() == matrix
        assert charpoly_of_matrix(matrix) == spec.characteristic_polynomial()
        assert characteristic_polynomial(matrix) == charpoly_of_matrix(matrix)
        u = adjoint_u(system, 5)
        assert mat_vec_left(u, matrix) == left_multiply(u, matrix)

    np_sys = nonpisot_order3()
    matrix = residual_matrix(np_sys)
    assert integer_preimage((1, 0, 0), 0) is None
    assert integer_affine_preimage(matrix, (0, 0, 0), (1, 0, 0)) is None
    assert integer_preimage((3, 1, 0), 0) == integer_affine_preimage(
        matrix, (0, 0, 0), (3, 1, 0)
    ) == (0, -2, 1)
    inv = np_inverse_matrix()
    assert inv[0][0] == Fraction(-1, 3)
    np_spec = recurrence_spec(np_sys)
    assert np_spec is not None
    assert np_spec.companion_charpoly_matches()


def test_typed_attacks_do_not_promote_np_census_to_live_infinitude():
    from research.ostrowski.attacks import (
        affine_region,
        functional_s3,
        hub_block,
        modular,
        reconnaissance,
        reverse_origin,
    )
    from research.ostrowski.live_layers import ORIGIN, forward_layers
    from research.ostrowski.zero_value_kernel import HUB, SHORTEST_NONRESET
    from research_engine.attacks.result import AttackStatus
    from research_engine.core.semantics import ClaimKind, SearchScope

    census = reconnaissance(4)
    report = forward_layers(nonpisot_order3(), 4, live_only=True)
    assert census.status == AttackStatus.OBSERVATION
    assert census.scope == SearchScope.BOUNDED
    assert census.kind == ClaimKind.LIVE_SLICE
    for n in range(5):
        assert census.evidence["layer_sizes"][n] == report["layers"][n]["L"]
    residue = modular()
    assert residue.status == AttackStatus.SUPPORTED
    assert residue.scope == SearchScope.EXACT
    assert residue.kind == ClaimKind.REACHABLE
    assert residue.evidence["forcing_gcds"][0] == 3
    leak = affine_region(frozenset({ORIGIN}), 4)
    assert leak.status == AttackStatus.REFUTED
    block = hub_block()
    assert block.status == AttackStatus.SUPPORTED
    assert block.evidence["translation"] == HUB
    assert block.evidence["block_kind"] == "AFFINE"
    assert SHORTEST_NONRESET == (1, -2)
    rev = reverse_origin(max_depth=1)
    assert rev.kind == ClaimKind.CO_REACHABLE
    assert "not the adder live set" in rev.claim
    bound = functional_s3(2)
    assert bound.status != AttackStatus.SUPPORTED
    assert bound.scope == SearchScope.BOUNDED
