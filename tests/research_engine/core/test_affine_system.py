"""Exact affine step, matrix power, and dimension validation."""

from __future__ import annotations

import pytest

from research_engine.core.affine_system import (
    AffineSystem,
    affine_step,
    apply_matrix,
    identity_matrix,
    iterate_affine_word,
    matrix_power,
    multiply_matrices,
)


def doubling_system() -> AffineSystem:
    return AffineSystem(
        A=((2, 0), (0, 2)),
        translations={0: (0, 0), 1: (1, 0), -1: (-1, 0)},
        controls=(0, 1, -1),
    )


def test_rejects_nonsquare_or_noninteger_matrix():
    with pytest.raises(ValueError, match="square"):
        AffineSystem(A=((1, 0), (0,)), translations={0: (0, 0)})
    with pytest.raises(ValueError, match="integers"):
        AffineSystem(A=((1.0, 0), (0, 1)), translations={0: (0, 0)})  # type: ignore[arg-type]


def test_rejects_mismatched_translation_dimension():
    with pytest.raises(ValueError, match="translation dimension"):
        AffineSystem(A=((1, 0), (0, 1)), translations={0: (0, 0, 1)})


def test_step_is_exact_ax_plus_b():
    system = doubling_system()
    assert system.dimension == 2
    assert system.step((1, 2), 1) == (3, 4)
    assert affine_step(system.A, (1, 2), (1, 0)) == (3, 4)
    assert apply_matrix(system.A, (1, 2)) == (2, 4)


def test_identity_and_matrix_power():
    ident = identity_matrix(2)
    assert ident == ((1, 0), (0, 1))
    a = ((2, 1), (0, 2))
    assert matrix_power(a, 0) == ident
    assert matrix_power(a, 1) == a
    assert matrix_power(a, 2) == multiply_matrices(a, a) == ((4, 4), (0, 4))
    with pytest.raises(ValueError, match="nonnegative"):
        matrix_power(a, -1)


def test_apply_word_matches_iterated_step():
    system = doubling_system()
    word = (1, 0, -1)
    expected = (0, 0)
    for control in word:
        expected = system.step(expected, control)
    assert system.apply_word((0, 0), word) == expected
    assert iterate_affine_word(system.A, (0, 0), word, system.translation) == expected
