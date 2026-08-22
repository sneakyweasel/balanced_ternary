"""Symbolic expression language for the balanced-ternary calculus."""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.trit import Trit, as_trit


@dataclass(frozen=True)
class EInt:
    value: int


@dataclass(frozen=True)
class ETrit:
    value: Trit


@dataclass(frozen=True)
class EAdd:
    left: Expr
    right: Expr


@dataclass(frozen=True)
class EMul:
    left: Expr
    right: Expr


@dataclass(frozen=True)
class ENeg:
    arg: Expr


@dataclass(frozen=True)
class ED:
    arg: Expr


@dataclass(frozen=True)
class EIm:
    arg: Expr


@dataclass(frozen=True)
class EI0:
    arg: Expr


@dataclass(frozen=True)
class EIp:
    arg: Expr


@dataclass(frozen=True)
class EShift3:
    arg: Expr


@dataclass(frozen=True)
class ENormalize:
    arg: Expr


@dataclass(frozen=True)
class ECmp3:
    left: Expr
    right: Expr


@dataclass(frozen=True)
class ESelect3:
    cond: Expr
    x_minus: Expr
    x_zero: Expr
    x_plus: Expr


Expr = (
    EInt
    | ETrit
    | EAdd
    | EMul
    | ENeg
    | ED
    | EIm
    | EI0
    | EIp
    | EShift3
    | ENormalize
    | ECmp3
    | ESelect3
)


def e_int(n: int) -> EInt:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"integer node must be int, got {type(n).__name__}")
    return EInt(n)


def e_trit(a: Trit | int) -> ETrit:
    return ETrit(as_trit(int(a)))


def expr_size(expr: Expr) -> int:
    if isinstance(expr, (EInt, ETrit)):
        return 1
    if isinstance(expr, (ENeg, ED, EIm, EI0, EIp, EShift3, ENormalize)):
        return 1 + expr_size(expr.arg)
    if isinstance(expr, (EAdd, EMul, ECmp3)):
        return 1 + expr_size(expr.left) + expr_size(expr.right)
    if isinstance(expr, ESelect3):
        return 1 + expr_size(expr.cond) + expr_size(expr.x_minus) + expr_size(
            expr.x_zero
        ) + expr_size(expr.x_plus)
    raise TypeError(f"unknown expression {type(expr).__name__}")


def nesting_depth(expr: Expr) -> int:
    if isinstance(expr, (EInt, ETrit)):
        return 0
    if isinstance(expr, (ENeg, ED, EIm, EI0, EIp, EShift3, ENormalize)):
        return 1 + nesting_depth(expr.arg)
    if isinstance(expr, (EAdd, EMul, ECmp3)):
        return 1 + max(nesting_depth(expr.left), nesting_depth(expr.right))
    if isinstance(expr, ESelect3):
        return 1 + max(
            nesting_depth(expr.cond),
            nesting_depth(expr.x_minus),
            nesting_depth(expr.x_zero),
            nesting_depth(expr.x_plus),
        )
    raise TypeError(f"unknown expression {type(expr).__name__}")


def d_count(expr: Expr) -> int:
    if isinstance(expr, ED):
        return 1 + d_count(expr.arg)
    if isinstance(expr, (EInt, ETrit)):
        return 0
    if isinstance(expr, (ENeg, EIm, EI0, EIp, EShift3, ENormalize)):
        return d_count(expr.arg)
    if isinstance(expr, (EAdd, EMul, ECmp3)):
        return d_count(expr.left) + d_count(expr.right)
    if isinstance(expr, ESelect3):
        return (
            d_count(expr.cond)
            + d_count(expr.x_minus)
            + d_count(expr.x_zero)
            + d_count(expr.x_plus)
        )
    raise TypeError(f"unknown expression {type(expr).__name__}")


def render(expr: Expr) -> str:
    if isinstance(expr, EInt):
        return str(expr.value)
    if isinstance(expr, ETrit):
        return f"[{int(expr.value):+d}]"
    if isinstance(expr, EAdd):
        return f"({render(expr.left)} + {render(expr.right)})"
    if isinstance(expr, EMul):
        return f"({render(expr.left)} * {render(expr.right)})"
    if isinstance(expr, ENeg):
        return f"N({render(expr.arg)})"
    if isinstance(expr, ED):
        return f"D({render(expr.arg)})"
    if isinstance(expr, EIm):
        return f"I-({render(expr.arg)})"
    if isinstance(expr, EI0):
        return f"I0({render(expr.arg)})"
    if isinstance(expr, EIp):
        return f"I+({render(expr.arg)})"
    if isinstance(expr, EShift3):
        return f"S({render(expr.arg)})"
    if isinstance(expr, ENormalize):
        return f"Nrm({render(expr.arg)})"
    if isinstance(expr, ECmp3):
        return f"cmp3({render(expr.left)}, {render(expr.right)})"
    if isinstance(expr, ESelect3):
        return (
            f"select3({render(expr.cond)}, {render(expr.x_minus)}, "
            f"{render(expr.x_zero)}, {render(expr.x_plus)})"
        )
    raise TypeError(f"unknown expression {type(expr).__name__}")
