"""Exact affine block actions.

A block ``B`` induces ``T_B(x) = A^{|B|} x + c_B``. Concatenation uses

    T_{UV} = T_V ∘ T_U

so ``c_{UV} = A^{|V|} c_U + c_V``. Naive numerical concatenation of
translations is not the composition law.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from research_engine.core.affine_system import (
    AffineSystem,
    add_vectors,
    apply_matrix,
    identity_matrix,
    iterate_affine_word,
    matrix_dimension,
    matrix_power,
    multiply_matrices,
    zero_vector,
)
from research_engine.core.semantics import Control, Matrix, Vector


@dataclass(frozen=True)
class BlockAction:
    """Immutable affine map ``x |-> matrix x + translation`` of a control word."""

    matrix: Matrix
    translation: Vector
    length: int

    def __post_init__(self) -> None:
        n = matrix_dimension(self.matrix)
        if len(self.translation) != n:
            raise ValueError("translation dimension must match the block matrix")
        if self.length < 0:
            raise ValueError("length must be nonnegative")

    @property
    def dimension(self) -> int:
        return len(self.translation)

    def apply(self, state: Vector) -> Vector:
        return add_vectors(apply_matrix(self.matrix, state), self.translation)


def block_action(
    system: AffineSystem,
    word: Sequence[Control],
) -> BlockAction:
    """``T_B`` for a word over a finite-control affine system."""
    return block_action_of_word(system.A, word, system.translation)


def block_action_of_word(
    matrix: Matrix,
    word: Sequence[Control],
    translation_of: Callable[[Control], Vector],
) -> BlockAction:
    k = len(word)
    powered = matrix_power(matrix, k)
    origin = zero_vector(matrix_dimension(matrix))
    particular = iterate_affine_word(matrix, origin, word, translation_of)
    return BlockAction(matrix=powered, translation=particular, length=k)


def empty_block(dimension: int) -> BlockAction:
    return BlockAction(
        matrix=identity_matrix(dimension),
        translation=zero_vector(dimension),
        length=0,
    )


def compose_blocks(first: BlockAction, second: BlockAction) -> BlockAction:
    """Action of concatenating ``first`` then ``second``.

    Orientation: ``T_{UV} = T_V ∘ T_U``.
    """
    if first.dimension != second.dimension:
        raise ValueError("block dimensions must match")
    matrix = multiply_matrices(second.matrix, first.matrix)
    translation = add_vectors(
        apply_matrix(second.matrix, first.translation),
        second.translation,
    )
    return BlockAction(
        matrix=matrix,
        translation=translation,
        length=first.length + second.length,
    )
