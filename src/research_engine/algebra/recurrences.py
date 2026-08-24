"""Constant-coefficient integer recurrences.

``q_n = d_1 q_{n-1} + ⋯ + d_m q_{n-m}`` with ``q_j = 0`` for ``j < 0``.
The engine does not interpret the terms as Ostrowski place values.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from research_engine.algebra.lattices import characteristic_polynomial
from research_engine.core.semantics import Matrix


@dataclass(frozen=True)
class RecurrenceSpec:
    """Linear recurrence with ``coefficients = (d_1, …, d_m)``:

    ``q_n = d_1 q_{n-1} + ⋯ + d_m q_{n-m}``.

    ``initial_values`` supplies ``q_0, q_1, …``. Later terms use the
    recurrence; negative indices are ``0``.
    """

    coefficients: tuple[int, ...]
    initial_values: tuple[int, ...] = (1,)

    def __post_init__(self) -> None:
        if not self.coefficients:
            raise ValueError("coefficients must be nonempty")
        if any(isinstance(d, bool) or not isinstance(d, int) for d in self.coefficients):
            raise ValueError("coefficients must be integers")
        if not self.initial_values:
            raise ValueError("initial_values must be nonempty")
        if any(isinstance(q, bool) or not isinstance(q, int) for q in self.initial_values):
            raise ValueError("initial_values must be integers")

    @property
    def order(self) -> int:
        return len(self.coefficients)

    def sequence(self, length: int) -> tuple[int, ...]:
        if length < 0:
            raise ValueError("length must be nonnegative")
        values: list[int] = []
        for n in range(length):
            if n < len(self.initial_values):
                values.append(self.initial_values[n])
                continue
            acc = 0
            for k, coeff in enumerate(self.coefficients, start=1):
                prev_index = n - k
                prev = 0 if prev_index < 0 else values[prev_index]
                acc += coeff * prev
            values.append(acc)
        return tuple(values)

    def term(self, n: int) -> int:
        if n < 0:
            return 0
        return self.sequence(n + 1)[-1]

    def companion_matrix(self) -> Matrix:
        """Companion orientation matching a residual unread-tail matrix."""
        m = self.order
        rows: list[tuple[int, ...]] = []
        for i in range(m):
            row = [0] * m
            if i >= 1:
                row[i - 1] = 1
            row[m - 1] = self.coefficients[m - 1 - i]
            rows.append(tuple(row))
        return tuple(rows)

    def characteristic_polynomial(self) -> tuple[int, ...]:
        """``(1, -d_1, …, -d_m)`` for ``x^m - d_1 x^{m-1} - ⋯ - d_m``."""
        return (1, *(-d for d in self.coefficients))

    def verify_recurrence(self, values: Sequence[int]) -> bool:
        computed = self.sequence(len(values))
        if tuple(values) != computed:
            return False
        for n in range(self.order, len(values)):
            acc = sum(
                coeff * (values[n - k] if n - k >= 0 else 0)
                for k, coeff in enumerate(self.coefficients, start=1)
            )
            if acc != values[n]:
                return False
        return True

    def companion_charpoly_matches(self) -> bool:
        return characteristic_polynomial(self.companion_matrix()) == self.characteristic_polynomial()
