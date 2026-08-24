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
