"""Phase-0 realization: which Mealy machines arise as residual machines.

A residual machine has ``ρ_a(f)=[f(a)]_3`` and ``δ(f,a)=𝔇_a f``. Output
is not an independent table. One-state machines force ``𝔇_a f=f``.
"""

from __future__ import annotations

from itertools import product

from bt.calculus.residual import TRITS, residual_along
from bt.calculus.section import IntPoly

ONE_STATE_ABSTRACT = 3 ** (2 * 3)


def is_one_state_residual(f: IntPoly) -> bool:
    """``𝔇_a f = f`` for every input trit."""

    return all(f.section_deriv(a) == f for a in TRITS)


def one_state_polynomials() -> tuple[IntPoly, ...]:
    """Exact list: ``ax`` for ``a ∈ {-1,0,+1}``."""

    return (IntPoly((0,)), IntPoly((0, 1)), IntPoly((0, -1)))


def one_state_outputs(f: IntPoly) -> tuple[int, ...]:
    return tuple(f.rho(a) for a in TRITS)


def two_state_residual_graphs(max_degree: int = 2, coeff_bound: int = 2) -> int:
    """Distinct reachable 2-state residual graphs in a coefficient box."""

    box = range(-coeff_bound, coeff_bound + 1)
    graphs: set[tuple] = set()
    for coeffs in product(box, repeat=max_degree + 1):
        f = IntPoly(coeffs)
        if f.degree < 0:
            continue
        states = {f}
        for a in TRITS:
            states.add(f.section_deriv(a))
        if len(states) != 2:
            continue
        labeled = tuple(sorted(states, key=lambda p: p.coeffs))
        table = []
        for s in labeled:
            for a in TRITS:
                nxt = s.section_deriv(a)
                table.append((s.coeffs, a, s.rho(a), nxt.coeffs))
        graphs.add(tuple(table))
    return len(graphs)


def residual_along_closed(f: IntPoly, word: tuple[int, ...]) -> bool:
    """Sanity: the residual machine stays in ``Z[x]``."""

    return residual_along(f, word).coeffs is not None
