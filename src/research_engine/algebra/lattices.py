"""Exact integer-matrix algebra over ``Z`` and ``Q``.

No floating inverses. An integer preimage is ``None`` when the
solution is not a lattice point.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Sequence

from research_engine.core.affine_system import (
    add_vectors,
    apply_matrix,
    identity_matrix,
    matrix_dimension,
    multiply_matrices,
)
from research_engine.core.semantics import Matrix, Vector

FracMatrix = tuple[tuple[Fraction, ...], ...]
FracVector = tuple[Fraction, ...]


def subtract_vectors(left: Vector, right: Vector) -> Vector:
    if len(left) != len(right):
        raise ValueError("vector dimensions must match")
    return tuple(a - b for a, b in zip(left, right, strict=True))


def transpose(matrix: Matrix) -> Matrix:
    n = matrix_dimension(matrix)
    return tuple(tuple(matrix[j][i] for j in range(n)) for i in range(n))


def matrix_over_q(matrix: Matrix) -> FracMatrix:
    n = matrix_dimension(matrix)
    return tuple(tuple(Fraction(matrix[i][j]) for j in range(n)) for i in range(n))


def multiply_matrices_q(left: FracMatrix, right: FracMatrix) -> FracMatrix:
    n = len(left)
    if len(right) != n or any(len(row) != n for row in left + right):
        raise ValueError("matrix dimensions must match")
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(n)) for j in range(n))
        for i in range(n)
    )


def apply_matrix_q(matrix: FracMatrix, vector: FracVector) -> FracVector:
    n = len(matrix)
    if len(vector) != n:
        raise ValueError("vector dimension must match the matrix")
    return tuple(sum(matrix[i][j] * vector[j] for j in range(n)) for i in range(n))


def identity_matrix_q(dimension: int) -> FracMatrix:
    ident = identity_matrix(dimension)
    return tuple(tuple(Fraction(entry) for entry in row) for row in ident)


def matrix_det(matrix: Matrix) -> int:
    """Exact determinant over ``Z`` by Laplace expansion."""
    n = matrix_dimension(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    total = 0
    for j, entry in enumerate(matrix[0]):
        if entry == 0:
            continue
        minor = tuple(row[:j] + row[j + 1 :] for row in matrix[1:])
        sign = 1 if j % 2 == 0 else -1
        total += sign * entry * matrix_det(minor)
    return total


def _minor(matrix: Matrix, row: int, col: int) -> Matrix:
    return tuple(
        tuple(entry for j, entry in enumerate(r) if j != col)
        for i, r in enumerate(matrix)
        if i != row
    )


def adjugate(matrix: Matrix) -> Matrix:
    n = matrix_dimension(matrix)
    if n == 1:
        return ((1,),)
    return tuple(
        tuple((1 if (i + j) % 2 == 0 else -1) * matrix_det(_minor(matrix, j, i)) for j in range(n))
        for i in range(n)
    )


def inverse_over_q(matrix: Matrix) -> FracMatrix:
    det = matrix_det(matrix)
    if det == 0:
        raise ZeroDivisionError("matrix is singular")
    adj = adjugate(matrix)
    return tuple(tuple(Fraction(entry, det) for entry in row) for row in adj)


def solve_over_q(matrix: Matrix, rhs: Vector) -> FracVector | None:
    """Solve ``A x = rhs`` over ``Q``, or ``None`` if ``A`` is singular."""
    det = matrix_det(matrix)
    if det == 0:
        return None
    n = matrix_dimension(matrix)
    if len(rhs) != n:
        raise ValueError("rhs dimension must match the matrix")
    return apply_matrix_q(inverse_over_q(matrix), tuple(Fraction(v) for v in rhs))


def integer_affine_preimage(
    matrix: Matrix,
    translation: Vector,
    target: Vector,
) -> Vector | None:
    """Lattice solution of ``A s + b = target``, or ``None`` if not integral."""
    rhs = subtract_vectors(target, translation)
    solved = solve_over_q(matrix, rhs)
    if solved is None:
        return None
    ints: list[int] = []
    for value in solved:
        if value.denominator != 1:
            return None
        ints.append(int(value))
    predicted = add_vectors(apply_matrix(matrix, tuple(ints)), translation)
    if predicted != tuple(target):
        return None
    return tuple(ints)


def vector_gcd(vector: Sequence[int]) -> int:
    acc = 0
    for entry in vector:
        acc = gcd(acc, abs(int(entry)))
    return acc


def characteristic_polynomial(matrix: Matrix) -> tuple[int, ...]:
    """Monic ``det(xI-A)`` as ``(1, c_1, …, c_n)``.

    Faddeev–LeVerrier: ``M_1=A``, ``c_k=-(1/k) tr(M_k)``,
    ``M_{k+1}=A(M_k+c_k I)``. Traces divide exactly on ``Z``.
    """
    n = matrix_dimension(matrix)
    ident = identity_matrix(n)
    coeffs: list[int] = [1]
    current = matrix
    for k in range(1, n + 1):
        trace = sum(current[i][i] for i in range(n))
        if trace % k != 0:
            raise ValueError("Faddeev–LeVerrier trace is not divisible")
        coeff = -(trace // k)
        coeffs.append(coeff)
        if k == n:
            break
        shifted = tuple(
            tuple(current[i][j] + coeff * ident[i][j] for j in range(n))
            for i in range(n)
        )
        current = multiply_matrices(matrix, shifted)
    return tuple(coeffs)
