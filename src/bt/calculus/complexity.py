"""Complexity measures for calculus expressions. Not circuit-complexity theorems."""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.expressions import Expr, d_count, expr_size, nesting_depth
from bt.calculus.rewrite import rewrite_expr
from bt.operators import get_operator


@dataclass(frozen=True)
class Complexity:
    expression_size: int
    d_operations: int
    nesting_depth: int
    rewrite_steps: int
    transducer_states: int | None
    notes: str


def measure(expr: Expr) -> Complexity:
    _nf, _reasons, steps = rewrite_expr(expr)
    return Complexity(
        expression_size=expr_size(expr),
        d_operations=d_count(expr),
        nesting_depth=nesting_depth(expr),
        rewrite_steps=steps,
        transducer_states=None,
        notes="Finite expression measures only. Not a complexity class claim.",
    )


def operator_states(symbol: str) -> int | None:
    return get_operator(symbol).metadata().state_count


def successor_representations(n: int) -> dict[str, int]:
    """Two ways of writing ``n+1``. Observation, not a lower bound."""
    from bt.calculus.expressions import EAdd, EInt, ENormalize

    plus = EAdd(EInt(n), EInt(1))
    nrm = ENormalize(EAdd(EInt(n), EInt(1)))
    return {
        "integer_add_size": expr_size(plus),
        "normalize_add_size": expr_size(nrm),
        "value": n + 1,
    }
