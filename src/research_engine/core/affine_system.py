"""Integer affine systems ``x' = A x + b_u``.

All arithmetic is exact. Spectral floats are not part of this module.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Hashable

from research_engine.core.semantics import Control, Matrix, Vector


def matrix_dimension(matrix: Matrix) -> int:
    if not matrix:
        raise ValueError("matrix must be nonempty")
    n = len(matrix)
    for row in matrix:
        if len(row) != n:
            raise ValueError("matrix must be square")
        if any(isinstance(entry, bool) or not isinstance(entry, int) for entry in row):
            raise ValueError("matrix entries must be integers")
    return n


def identity_matrix(dimension: int) -> Matrix:
    if dimension < 1:
        raise ValueError("dimension must be at least 1")
    return tuple(
        tuple(1 if i == j else 0 for j in range(dimension))
        for i in range(dimension)
    )


def zero_vector(dimension: int) -> Vector:
    if dimension < 1:
        raise ValueError("dimension must be at least 1")
    return tuple(0 for _ in range(dimension))


def add_vectors(left: Vector, right: Vector) -> Vector:
    if len(left) != len(right):
        raise ValueError("vector dimensions must match")
    return tuple(a + b for a, b in zip(left, right, strict=True))


def apply_matrix(matrix: Matrix, vector: Vector) -> Vector:
    n = matrix_dimension(matrix)
    if len(vector) != n:
        raise ValueError("vector dimension must match the matrix")
    if any(isinstance(entry, bool) or not isinstance(entry, int) for entry in vector):
        raise ValueError("vector entries must be integers")
    return tuple(sum(matrix[i][j] * vector[j] for j in range(n)) for i in range(n))


def multiply_matrices(left: Matrix, right: Matrix) -> Matrix:
    n = matrix_dimension(left)
    if matrix_dimension(right) != n:
        raise ValueError("matrix dimensions must match")
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(n)) for j in range(n))
        for i in range(n)
    )


def matrix_power(matrix: Matrix, exponent: int) -> Matrix:
    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    n = matrix_dimension(matrix)
    acc = identity_matrix(n)
    base = matrix
    remaining = exponent
    while remaining:
        if remaining & 1:
            acc = multiply_matrices(acc, base)
        base = multiply_matrices(base, base)
        remaining >>= 1
    return acc


def affine_step(matrix: Matrix, state: Vector, translation: Vector) -> Vector:
    """Exact ``A x + b``."""
    return add_vectors(apply_matrix(matrix, state), translation)


def iterate_affine_word(
    matrix: Matrix,
    start: Vector,
    word: Sequence[Control],
    translation_of: Callable[[Control], Vector],
) -> Vector:
    """Apply ``x' = A x + b_u`` along ``word`` without requiring a finite alphabet."""
    state = tuple(start)
    for control in word:
        state = affine_step(matrix, state, translation_of(control))
    return state


@dataclass(frozen=True)
class AffineSystem:
    """Finite-control integer affine system ``x' = A x + b_u``."""

    A: Matrix
    translations: Mapping[Hashable, Vector]
    controls: tuple[Hashable, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        dimension = matrix_dimension(self.A)
        frozen: dict[Hashable, Vector] = {}
        for control, translation in dict(self.translations).items():
            vec = tuple(translation)
            if len(vec) != dimension:
                raise ValueError("translation dimension must match A")
            if any(isinstance(entry, bool) or not isinstance(entry, int) for entry in vec):
                raise ValueError("translation entries must be integers")
            frozen[control] = vec
        object.__setattr__(self, "translations", MappingProxyType(frozen))
        if self.controls:
            missing = [control for control in self.controls if control not in frozen]
            if missing:
                raise ValueError(f"controls missing translations: {missing!r}")
        else:
            object.__setattr__(self, "controls", tuple(frozen))

    @property
    def dimension(self) -> int:
        return len(self.A)

    def translation(self, control: Control) -> Vector:
        return self.translations[control]

    def step(self, state: Vector, control: Control) -> Vector:
        return affine_step(self.A, state, self.translation(control))

    def apply_word(self, start: Vector, word: Sequence[Control]) -> Vector:
        return iterate_affine_word(self.A, start, word, self.translation)
