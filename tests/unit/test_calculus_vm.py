"""Postfix VM agrees with expression evaluation."""

from __future__ import annotations

from bt.calculus.derivative import D
from bt.calculus.expressions import EAdd, ED, EInt, expr_size
from bt.calculus.order import cmp3
from bt.calculus.semantics import evaluate
from bt.calculus.vm import evaluate_direct, run_postfix


def test_vm_arithmetic_and_d():
    assert evaluate_direct("2 3 ADD D") == D(5)
    assert evaluate_direct("4 NEG") == -4
    assert evaluate_direct("5 I+") == 16
    assert evaluate_direct("5 S") == 15
    assert evaluate_direct("6 H2") == 3
    assert evaluate_direct("7 M2") == 14
    rec = run_postfix("2 3 ADD D")
    assert rec.value == D(5)
    assert rec.stack_depth >= 1
    assert evaluate(rec.expr) == rec.value


def test_vm_select3():
    # x y CMP3 a b c SELECT3  =  a if x<y, b if x=y, c if x>y
    assert evaluate_direct("1 4 CMP3 10 20 30 SELECT3") == 10
    assert evaluate_direct("4 4 CMP3 10 20 30 SELECT3") == 20
    assert evaluate_direct("9 4 CMP3 10 20 30 SELECT3") == 30
    assert evaluate_direct("1 4 CMP3") == int(cmp3(1, 4))


def test_n_plus_one_sizes_are_observations():
    plus = EAdd(EInt(8), EInt(1))
    assert evaluate(plus) == 9
    assert expr_size(plus) == 3
