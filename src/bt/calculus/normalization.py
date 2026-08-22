"""Normal forms for the operator-only fragment ``{D, I_a, S, N}``."""

from __future__ import annotations

from bt.calculus.expressions import (
    ED,
    EI0,
    EIm,
    EInt,
    EIp,
    ENeg,
    EShift3,
    ETrit,
    Expr,
    render,
)
from bt.calculus.rewrite import rewrite_expr
from bt.calculus.semantics import evaluate


OPERATOR_FRAGMENT = (ED, EIm, EI0, EIp, EShift3, ENeg, EInt, ETrit)


def is_operator_fragment(expr: Expr) -> bool:
    if isinstance(expr, (EInt, ETrit)):
        return True
    if isinstance(expr, (ED, EIm, EI0, EIp, EShift3, ENeg)):
        return is_operator_fragment(expr.arg)
    return False


def normalize_expr(expr: Expr) -> tuple[Expr, tuple[str, ...], int]:
    """Innermost normalizer. Unique NF is claimed only after confluence checks."""
    return rewrite_expr(expr)


def normal_form(expr: Expr) -> Expr:
    nf, _reasons, _steps = normalize_expr(expr)
    return nf


def normal_form_string(expr: Expr) -> str:
    return render(normal_form(expr))


def semantically_equal(left: Expr, right: Expr, sample: tuple[int, ...] | None = None) -> bool:
    """Evaluate both sides. For closed expressions this is exact equality."""
    if _is_closed(left) and _is_closed(right):
        return evaluate(left) == evaluate(right)
    domain = sample if sample is not None else tuple(range(-20, 21))
    return all(evaluate(left) == evaluate(right) for _n in domain)


def _is_closed(expr: Expr) -> bool:
    return True
