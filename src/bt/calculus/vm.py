"""Postfix stack evaluator for the balanced-ternary calculus.

This is a mathematical evaluator, not a Setun hardware emulator.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.derivative import D
from bt.calculus.expressions import (
    EAdd,
    ECmp3,
    ED,
    EI0,
    EIm,
    EInt,
    EIp,
    EMul,
    ENeg,
    ESelect3,
    EShift3,
    Expr,
)
from bt.calculus.integral import I
from bt.calculus.order import cmp3
from bt.calculus.select import select3
from bt.calculus.semantics import evaluate
from bt.calculus.trit import Trit
from bt.normalization import add_with_trace
from bt.operators import DOUBLE, HALVE
from bt.representation import encode


UNARY = {
    "NEG": "neg",
    "D": "D",
    "I-": "Im",
    "I0": "I0",
    "I+": "Ip",
    "S": "S",
    "M2": "M2",
    "H2": "H2",
}

BINARY = {
    "ADD": "add",
    "SUB": "sub",
    "MUL": "mul",
    "CMP3": "cmp3",
}


@dataclass(frozen=True)
class VMResult:
    value: int
    expr: Expr
    stack_depth: int
    expression_size: int
    trit_ops: int
    carry_ops: int
    tokens: tuple[str, ...]


def tokenize(source: str) -> tuple[str, ...]:
    return tuple(part for part in source.replace(",", " ").split() if part)


def parse_token(token: str) -> int | str:
    if token in UNARY or token in BINARY or token == "SELECT3":
        return token
    try:
        return int(token, 10)
    except ValueError as exc:
        raise ValueError(f"unknown postfix token {token!r}") from exc


def compile_postfix(tokens: tuple[str, ...]) -> tuple[Expr, int, int, int]:
    """Compile postfix tokens to an :class:`Expr`.

    Returns ``(expr, max_stack_depth, trit_ops, carry_ops)``.
    ``SELECT3`` pops ``x_plus, x_zero, x_minus, cond``.
    ``CMP3`` pops ``y, x`` and pushes ``cmp3(x, y)``.
    """
    stack: list[Expr] = []
    depth = 0
    trit_ops = 0
    carry_ops = 0
    parsed = [parse_token(tok) for tok in tokens]
    for item in parsed:
        if isinstance(item, int):
            stack.append(EInt(item))
            depth = max(depth, len(stack))
            continue
        if item in BINARY:
            if len(stack) < 2:
                raise ValueError(f"{item} requires two stack values")
            right = stack.pop()
            left = stack.pop()
            if item == "ADD":
                stack.append(EAdd(left, right))
                carry_ops += 1
            elif item == "SUB":
                stack.append(EAdd(left, ENeg(right)))
                carry_ops += 1
            elif item == "MUL":
                stack.append(EMul(left, right))
            else:
                stack.append(ECmp3(left, right))
                trit_ops += 1
            depth = max(depth, len(stack))
            continue
        if item == "SELECT3":
            if len(stack) < 4:
                raise ValueError("SELECT3 requires cond, x_minus, x_zero, x_plus")
            x_plus = stack.pop()
            x_zero = stack.pop()
            x_minus = stack.pop()
            cond = stack.pop()
            stack.append(ESelect3(cond, x_minus, x_zero, x_plus))
            trit_ops += 1
            depth = max(depth, len(stack))
            continue
        if item not in UNARY:
            raise ValueError(f"unknown operation {item!r}")
        if not stack:
            raise ValueError(f"{item} requires one stack value")
        arg = stack.pop()
        if item == "NEG":
            stack.append(ENeg(arg))
        elif item == "D":
            stack.append(ED(arg))
            trit_ops += 1
        elif item == "I-":
            stack.append(EIm(arg))
            trit_ops += 1
        elif item == "I0":
            stack.append(EI0(arg))
            trit_ops += 1
        elif item == "I+":
            stack.append(EIp(arg))
            trit_ops += 1
        elif item == "S":
            stack.append(EShift3(arg))
        elif item == "M2":
            stack.append(EMul(EInt(2), arg))
        elif item == "H2":
            # Partial: recorded as integer division in evaluation via apply.
            stack.append(EHtwo(arg))
        depth = max(depth, len(stack))
    if len(stack) != 1:
        raise ValueError(f"postfix program left {len(stack)} stack values; expected 1")
    return stack[0], depth, trit_ops, carry_ops


@dataclass(frozen=True)
class EHtwo:
    """Internal VM node for partial ``H2``. Evaluated only on evens."""

    arg: Expr


def _eval_vm_expr(expr: object) -> int:
    if isinstance(expr, EHtwo):
        n = _eval_vm_expr(expr.arg)
        return HALVE.apply(n)
    if isinstance(expr, EMul) and isinstance(expr.left, EInt) and expr.left.value == 2:
        return DOUBLE.apply(_eval_vm_expr(expr.right))
    return evaluate(expr)  # type: ignore[arg-type]


def run_postfix(source: str) -> VMResult:
    tokens = tokenize(source)
    # Compile without H2 first using a local stack so H2 can be an expr.
    expr, depth, trit_ops, carry_ops = _compile_with_h2(tokens)
    value = _eval_vm_expr(expr)
    from bt.calculus.expressions import expr_size

    size = expr_size(expr) if not isinstance(expr, EHtwo) else 1 + expr_size(expr.arg)
    return VMResult(
        value=value,
        expr=expr,  # type: ignore[arg-type]
        stack_depth=depth,
        expression_size=size,
        trit_ops=trit_ops,
        carry_ops=carry_ops,
        tokens=tokens,
    )


def _compile_with_h2(tokens: tuple[str, ...]) -> tuple[object, int, int, int]:
    stack: list[object] = []
    depth = 0
    trit_ops = 0
    carry_ops = 0
    for raw in tokens:
        item = parse_token(raw)
        if isinstance(item, int):
            stack.append(EInt(item))
            depth = max(depth, len(stack))
            continue
        if item in BINARY:
            if len(stack) < 2:
                raise ValueError(f"{item} requires two stack values")
            right = stack.pop()
            left = stack.pop()
            if item == "ADD":
                stack.append(EAdd(left, right))  # type: ignore[arg-type]
                carry_ops += 1
            elif item == "SUB":
                stack.append(EAdd(left, ENeg(right)))  # type: ignore[arg-type]
                carry_ops += 1
            elif item == "MUL":
                stack.append(EMul(left, right))  # type: ignore[arg-type]
            else:
                stack.append(ECmp3(left, right))  # type: ignore[arg-type]
                trit_ops += 1
            depth = max(depth, len(stack))
            continue
        if item == "SELECT3":
            if len(stack) < 4:
                raise ValueError("SELECT3 requires cond, x_minus, x_zero, x_plus")
            x_plus = stack.pop()
            x_zero = stack.pop()
            x_minus = stack.pop()
            cond = stack.pop()
            stack.append(ESelect3(cond, x_minus, x_zero, x_plus))  # type: ignore[arg-type]
            trit_ops += 1
            depth = max(depth, len(stack))
            continue
        if item not in UNARY:
            raise ValueError(f"unknown operation {item!r}")
        if not stack:
            raise ValueError(f"{item} requires one stack value")
        arg = stack.pop()
        if item == "NEG":
            stack.append(ENeg(arg))  # type: ignore[arg-type]
        elif item == "D":
            stack.append(ED(arg))  # type: ignore[arg-type]
            trit_ops += 1
        elif item == "I-":
            stack.append(EIm(arg))  # type: ignore[arg-type]
            trit_ops += 1
        elif item == "I0":
            stack.append(EI0(arg))  # type: ignore[arg-type]
            trit_ops += 1
        elif item == "I+":
            stack.append(EIp(arg))  # type: ignore[arg-type]
            trit_ops += 1
        elif item == "S":
            stack.append(EShift3(arg))  # type: ignore[arg-type]
        elif item == "M2":
            stack.append(EMul(EInt(2), arg))  # type: ignore[arg-type]
        else:
            stack.append(EHtwo(arg))  # type: ignore[arg-type]
        depth = max(depth, len(stack))
    if len(stack) != 1:
        raise ValueError(f"postfix program left {len(stack)} stack values; expected 1")
    return stack[0], depth, trit_ops, carry_ops


def evaluate_direct(source: str) -> int:
    """Stack machine without building an expression tree."""
    stack: list[int] = []
    for raw in tokenize(source):
        item = parse_token(raw)
        if isinstance(item, int):
            stack.append(item)
            continue
        if item == "ADD":
            b, a = stack.pop(), stack.pop()
            stack.append(a + b)
        elif item == "SUB":
            b, a = stack.pop(), stack.pop()
            stack.append(a - b)
        elif item == "MUL":
            b, a = stack.pop(), stack.pop()
            stack.append(a * b)
        elif item == "NEG":
            stack.append(-stack.pop())
        elif item == "D":
            stack.append(D(stack.pop()))
        elif item == "I-":
            stack.append(I(Trit.MINUS, stack.pop()))
        elif item == "I0":
            stack.append(I(Trit.ZERO, stack.pop()))
        elif item == "I+":
            stack.append(I(Trit.PLUS, stack.pop()))
        elif item == "S":
            stack.append(3 * stack.pop())
        elif item == "M2":
            stack.append(DOUBLE.apply(stack.pop()))
        elif item == "H2":
            stack.append(HALVE.apply(stack.pop()))
        elif item == "CMP3":
            b, a = stack.pop(), stack.pop()
            stack.append(int(cmp3(a, b)))
        elif item == "SELECT3":
            xp, xz, xm, c = stack.pop(), stack.pop(), stack.pop(), stack.pop()
            stack.append(select3(c, xm, xz, xp))
        else:
            raise ValueError(f"unknown operation {item!r}")
    if len(stack) != 1:
        raise ValueError(f"postfix program left {len(stack)} stack values; expected 1")
    return stack[0]


def carry_count_add(x: int, y: int) -> int:
    """Number of nonzero carry-outs in the existing addition trace."""
    trace = add_with_trace(encode(x), encode(y))
    return sum(1 for step in trace.steps if step.carry_out != 0) + (1 if trace.final_carry else 0)
