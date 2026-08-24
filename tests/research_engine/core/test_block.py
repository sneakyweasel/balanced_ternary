"""Block composition uses affine orientation, not naive translation sums."""

from __future__ import annotations

from research_engine.core.affine_system import AffineSystem, apply_matrix
from research_engine.core.block import (
    block_action,
    compose_blocks,
    empty_block,
)


def doubling_system() -> AffineSystem:
    return AffineSystem(
        A=((2, 0), (0, 2)),
        translations={0: (0, 0), 1: (1, 0)},
    )


def test_empty_block_is_identity():
    system = doubling_system()
    empty = empty_block(2)
    assert empty.length == 0
    assert empty.matrix == ((1, 0), (0, 1))
    assert empty.translation == (0, 0)
    assert empty.apply((3, -4)) == (3, -4)
    assert block_action(system, ()).apply((3, -4)) == (3, -4)


def test_block_action_matches_word_iteration():
    system = doubling_system()
    word = (1, 0, 1)
    action = block_action(system, word)
    assert action.length == 3
    assert action.apply((0, 0)) == system.apply_word((0, 0), word)
    assert action.apply((1, -1)) == system.apply_word((1, -1), word)


def test_composition_is_tv_after_tu_not_naive_translation_sum():
    system = doubling_system()
    first = block_action(system, (1,))
    second = block_action(system, (0,))
    composed = compose_blocks(first, second)
    concatenated = block_action(system, (1, 0))
    naive = (
        first.translation[0] + second.translation[0],
        first.translation[1] + second.translation[1],
    )
    assert composed == concatenated
    assert composed.translation == (2, 0)
    assert naive == (1, 0)
    assert composed.translation != naive
    predicted = (
        apply_matrix(second.matrix, first.translation)[0] + second.translation[0],
        apply_matrix(second.matrix, first.translation)[1] + second.translation[1],
    )
    assert composed.translation == predicted
    assert composed.apply((0, 0)) == system.apply_word((0, 0), (1, 0))
