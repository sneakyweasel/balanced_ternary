"""Tiny arithmetic AST compiling to coefficient normalization.

Not a Setun emulator and not cycle-accurate.

Prompt-level ISA details (``-+-`` normalize opcodes, 18-trit registers,
FMA-like micro-ops) are **HISTORICAL SKETCHES**. Only claims supported
by ``docs/theory/setun_connection.md`` or a ``literature/*.json`` record
are **HISTORICAL FACT**.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from bt.calculus.order import cmp3
from bt.normtheory.arithmetic import add_coeff, fma_fused, mul_coeff
from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.strategies import normal_form


@dataclass(frozen=True)
class Lit:
    value: int


@dataclass(frozen=True)
class Add:
    left: "AST"
    right: "AST"


@dataclass(frozen=True)
class Sub:
    left: "AST"
    right: "AST"


@dataclass(frozen=True)
class Mul:
    left: "AST"
    right: "AST"


@dataclass(frozen=True)
class Fma:
    p: "AST"
    q: "AST"
    r: "AST"


@dataclass(frozen=True)
class Shift:
    arg: "AST"


@dataclass(frozen=True)
class Normalize:
    arg: "AST"


@dataclass(frozen=True)
class Cmp3:
    left: "AST"
    right: "AST"


AST = Union[Lit, Add, Sub, Mul, Fma, Shift, Normalize, Cmp3]


SKETCHES = (
    "18-trit hardware registers as a universal Setun word size",
    "a dedicated -+- normalize opcode in the published ISA",
    "a fused multiply-add micro-operation as a documented Setun instruction",
)

FACTS = (
    "Setun used signed trits {-1,0,+1} (Hayes, Knuth, Malinovsky).",
    "Arithmetic used balanced-ternary addition/subtraction/multiplication "
    "with a local carry/borrow of at most one (setun_connection.md).",
    "The sign of a word was the leading trit; comparison used that sign.",
)


def eval_ast(expr: AST) -> CoeffWord:
    if isinstance(expr, Lit):
        return CoeffWord.from_value(expr.value)
    if isinstance(expr, Add):
        return normal_form(add_coeff(eval_ast(expr.left), eval_ast(expr.right)))
    if isinstance(expr, Sub):
        return normal_form(add_coeff(eval_ast(expr.left), _neg(eval_ast(expr.right))))
    if isinstance(expr, Mul):
        return normal_form(mul_coeff(eval_ast(expr.left), eval_ast(expr.right)))
    if isinstance(expr, Fma):
        return fma_fused(eval_ast(expr.p), eval_ast(expr.q), eval_ast(expr.r)).result
    if isinstance(expr, Shift):
        return CoeffWord((0,) + eval_ast(expr.arg).coeffs)
    if isinstance(expr, Normalize):
        return normal_form(eval_ast(expr.arg))
    if isinstance(expr, Cmp3):
        left = eval_ast(expr.left).value()
        right = eval_ast(expr.right).value()
        return CoeffWord((int(cmp3(left, right)),))
    raise TypeError(f"unknown AST node {type(expr).__name__}")


def _neg(word: CoeffWord) -> CoeffWord:
    return CoeffWord(tuple(-c for c in word.coeffs))


def label(claim: str) -> str:
    """Classify a claim as FACT or SKETCH. Never invent a new fact."""
    for fact in FACTS:
        if claim.lower() in fact.lower() or fact.lower() in claim.lower():
            return "HISTORICAL FACT"
    return "HISTORICAL SKETCH"
