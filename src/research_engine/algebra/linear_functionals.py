"""Integer linear forms.

Evaluating ``a · x`` on a finite sample is an observation, not an
invariant and not an asymptotic bound.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from research_engine.core.semantics import Matrix, Vector


def dot(left: Vector, right: Vector) -> int:
    if len(left) != len(right):
        raise ValueError("vector dimensions must match")
    if any(isinstance(x, bool) or not isinstance(x, int) for x in (*left, *right)):
        raise ValueError("vector entries must be integers")
    return sum(a * b for a, b in zip(left, right, strict=True))


def left_multiply(covector: Vector, matrix: Matrix) -> Vector:
    """Row vector ``u`` times ``A``."""
    n = len(matrix)
    if len(covector) != n:
        raise ValueError("covector dimension must match the matrix")
    if any(len(row) != n for row in matrix):
        raise ValueError("matrix must be square")
    return tuple(
        sum(covector[i] * matrix[i][j] for i in range(n))
        for j in range(n)
    )


@dataclass(frozen=True)
class LinearFunctional:
    coefficients: Vector

    def __post_init__(self) -> None:
        if not self.coefficients:
            raise ValueError("coefficients must be nonempty")
        if any(
            isinstance(c, bool) or not isinstance(c, int) for c in self.coefficients
        ):
            raise ValueError("coefficients must be integers")

    def __call__(self, state: Vector) -> int:
        return dot(self.coefficients, state)

    def values_on(self, states: Iterable[Vector]) -> tuple[int, ...]:
        return tuple(self(state) for state in states)

    def observed_bound(self, states: Iterable[Vector]) -> int:
        """``max |ℓ(s)|`` on a finite sample. Not an invariant."""
        vals = self.values_on(states)
        if not vals:
            return 0
        return max(abs(v) for v in vals)
