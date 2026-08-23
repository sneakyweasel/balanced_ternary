"""Phase-0: sums of constructor terms are affine / coefficient-word only.

Production ``bt.calculus.rewrite._step`` stays the unary fragment.
This file records the architectural classification:

* the only exact-on-ℤ identities ``U(x)+V(y) = W(x+y)`` for
  ``U,V,W ∈ {S, I+, I-, N}`` are the six known factor-out / push-in
  pairs (``I0`` counts as ``S``);
* same-sign ``I_a`` and mixed ``N`` have no such ``W``; ``D+D`` is
  unsound (carry of ``1+1``);
* the named factor-out twins share one affine form and one
  coefficient-word NF after evaluation — that is the complete
  finite canonicalizer, not a tree TRS on ``Add``.

No Add rule is installed. No census of alternative tree systems.
"""

from __future__ import annotations

from itertools import product

from bt.calculus.derivative import D
from bt.calculus.expressions import (
    EAdd,
    EIm,
    EInt,
    EIp,
    ENeg,
    EShift3,
    Expr,
)
from bt.calculus.integral import I_minus, I_plus
from bt.calculus.rewrite import TREE_RULES, _step
from bt.calculus.semantics import evaluate
from bt.normtheory.arithmetic import add_coeff, normalize_add
from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.strategies import normal_form
from bt.representation import encode

# Syntactic holes. Tree rules never inspect the integer payload.
X = EInt(0)
Y = EInt(1)
Z = EInt(2)

SAMPLES: tuple[tuple[int, int], ...] = (
    (0, 0),
    (1, 1),
    (3, 5),
    (-2, 4),
    (0, 1),
    (-7, -1),
    (2, -3),
)

# Integer maps of the affine constructors. I0 = S.
CONSTRUCTORS: dict[str, object] = {
    "S": lambda t: 3 * t,
    "I+": I_plus,
    "I-": I_minus,
    "N": lambda t: -t,
}

# The only exact U(x)+V(y) = W(x+y) rows.
EXACT_TRIPLES: dict[tuple[str, str], str] = {
    ("S", "S"): "S",
    ("N", "N"): "N",
    ("I+", "S"): "I+",
    ("S", "I+"): "I+",
    ("I-", "S"): "I-",
    ("S", "I-"): "I-",
    ("I+", "I-"): "S",
    ("I-", "I+"): "S",
}


def plug(expr: Expr, env: dict[int, int]) -> Expr:
    if isinstance(expr, EInt):
        if expr.value in env:
            return EInt(env[expr.value])
        return expr
    if hasattr(expr, "arg"):
        return type(expr)(plug(expr.arg, env))
    if isinstance(expr, EAdd):
        return EAdd(plug(expr.left, env), plug(expr.right, env))
    raise TypeError(f"unsupported {type(expr).__name__}")


def affine_form(expr: Expr) -> tuple[int, int, int, int]:
    """Coefficients ``(cx, cy, cz, c0)`` of an affine form on holes X,Y,Z."""
    c0 = evaluate(plug(expr, {0: 0, 1: 0, 2: 0}))
    cx = evaluate(plug(expr, {0: 1, 1: 0, 2: 0})) - c0
    cy = evaluate(plug(expr, {0: 0, 1: 1, 2: 0})) - c0
    cz = evaluate(plug(expr, {0: 0, 1: 0, 2: 1})) - c0
    return (cx, cy, cz, c0)


def coeffword_nf(n: int) -> tuple[int, ...]:
    return normal_form(CoeffWord.from_value(n)).coeffs


# ---------------------------------------------------------------------------
# Classification of exact U(x)+V(y) = W(x+y)
# ---------------------------------------------------------------------------


def test_exact_add_identities_are_exactly_the_six_rows():
    """Finite check of the classification lemma on a probe set."""
    names = tuple(CONSTRUCTORS)
    for u_name, v_name in product(names, names):
        u_fn = CONSTRUCTORS[u_name]
        v_fn = CONSTRUCTORS[v_name]
        matches = [
            w_name
            for w_name, w_fn in CONSTRUCTORS.items()
            if all(u_fn(x) + v_fn(y) == w_fn(x + y) for x, y in SAMPLES)
        ]
        expected = EXACT_TRIPLES.get((u_name, v_name))
        if expected is None:
            assert matches == [], (u_name, v_name, matches)
        else:
            assert matches == [expected], (u_name, v_name, matches)


def test_i0_counts_as_s_in_the_classification():
    """I0(n) = 3n = S(n); it does not add a seventh row."""
    for x, y in SAMPLES:
        assert 3 * x + 3 * y == 3 * (x + y)
        assert I_plus(x) + 3 * y == I_plus(x + y)
        assert 3 * x + I_minus(y) == I_minus(x + y)


def test_same_sign_i_plus_is_exact_but_needs_a_constant():
    """I+(x)+I+(y) = 3(x+y)+2; 2 is not a trit, so no W(x+y)."""
    for x, y in SAMPLES:
        value = I_plus(x) + I_plus(y)
        assert value == 3 * (x + y) + 2
        assert value != 3 * (x + y)
        assert value != I_plus(x + y)
        assert value != I_minus(x + y)
        assert value != -(x + y)


def test_same_sign_i_minus_is_exact_but_needs_a_constant():
    for x, y in SAMPLES:
        value = I_minus(x) + I_minus(y)
        assert value == 3 * (x + y) - 2
        assert value != I_plus(x + y)
        assert value != I_minus(x + y)
        assert value != 3 * (x + y)


def test_mixed_n_has_slope_two_or_minus_four():
    """N(x)+S(y) = -x+3y has slope 2 in (x+y); not a constructor of x+y."""
    def agrees(lhs, rhs) -> bool:
        return all(lhs(x, y) == rhs(x, y) for x, y in SAMPLES)

    n_plus_s = lambda x, y: (-x) + 3 * y
    n_plus_ip = lambda x, y: (-x) + I_plus(y)
    assert not agrees(n_plus_s, lambda x, y: 3 * (x + y))
    assert not agrees(n_plus_s, lambda x, y: I_plus(x + y))
    assert not agrees(n_plus_s, lambda x, y: I_minus(x + y))
    assert not agrees(n_plus_s, lambda x, y: -(x + y))
    assert not agrees(n_plus_ip, lambda x, y: 3 * (x + y))


def test_d_through_add_is_unsound_by_the_same_carry():
    """The 1+1 carry that blocks every Add-tree orientation."""
    assert D(1) + D(1) == 0
    assert D(2) == 1


# ---------------------------------------------------------------------------
# Affine / coefficient-word canonicalizer joins the named twins
# ---------------------------------------------------------------------------


def test_s_association_twins_share_affine_form():
    """S(x)+(S(y)+z) and S(x+y)+z are both 3x+3y+z."""
    nested = EAdd(EShift3(X), EAdd(EShift3(Y), Z))
    collected = EAdd(EShift3(EAdd(X, Y)), Z)
    assert affine_form(nested) == (3, 3, 1, 0)
    assert affine_form(nested) == affine_form(collected)


def test_i_plus_association_twins_share_affine_form():
    """I+(x+y)+I+(z) and I+(x)+I+(y+z) are both 3x+3y+3z+2."""
    left = EAdd(EIp(EAdd(X, Y)), EIp(Z))
    right = EAdd(EIp(X), EIp(EAdd(Y, Z)))
    assert affine_form(left) == (3, 3, 3, 2)
    assert affine_form(left) == affine_form(right)


def test_same_sign_constant_twin_is_the_affine_form():
    """I+(x)+I+(y) and S(x+y)+2 are the same affine map.

    The constant ``2`` cannot live in the hole encoding (``EInt(2)`` is
    ``Z``), so the identity is checked on integer samples.
    """
    left = EAdd(EIp(X), EIp(Y))
    assert affine_form(left) == (3, 3, 0, 2)
    for a, b in SAMPLES:
        assert I_plus(a) + I_plus(b) == 3 * (a + b) + 2
        assert evaluate(EAdd(EIp(EInt(a)), EIp(EInt(b)))) == evaluate(
            EAdd(EShift3(EAdd(EInt(a), EInt(b))), EInt(2))
        )


def test_single_variable_sum_is_affine_with_slope_six():
    """S(x)+I+(x) = 6x+1: affine, but not a single 3^k x + c."""
    term = EAdd(EShift3(X), EIp(X))
    assert affine_form(term) == (6, 0, 0, 1)
    for n in (0, 1, -2, 5):
        assert evaluate(plug(term, {0: n, 1: 0, 2: 0})) == 6 * n + 1


def test_closed_twins_share_coefficient_word_nf():
    """Evaluate then unique BT word: the complete finite NF of a closed sum."""
    twins = (
        (
            EAdd(EShift3(X), EAdd(EShift3(Y), Z)),
            EAdd(EShift3(EAdd(X, Y)), Z),
        ),
        (
            EAdd(EIp(EAdd(X, Y)), EIp(Z)),
            EAdd(EIp(X), EIp(EAdd(Y, Z))),
        ),
    )
    envs = (
        {0: 3, 1: 5, 2: 7},
        {0: -4, 1: 2, 2: 1},
        {0: 0, 1: 0, 2: 0},
        {0: 1, 1: -1, 2: 8},
    )
    for left, right in twins:
        for env in envs:
            lv = evaluate(plug(left, env))
            rv = evaluate(plug(right, env))
            assert lv == rv
            assert coeffword_nf(lv) == coeffword_nf(rv)
            assert coeffword_nf(lv) == tuple(encode(lv).digits_lsd())
    for a, b in SAMPLES:
        lv = I_plus(a) + I_plus(b)
        rv = 3 * (a + b) + 2
        assert lv == rv
        assert coeffword_nf(lv) == coeffword_nf(rv)
        assert coeffword_nf(lv) == tuple(encode(lv).digits_lsd())


def test_coeffword_add_is_the_sum_canonicalizer():
    """add_coeff + Strategy A is evaluate-then-encode, not a tree TRS."""
    for a, b in SAMPLES:
        left = CoeffWord.from_value(I_plus(a))
        right = CoeffWord.from_value(I_plus(b))
        raw = add_coeff(left, right)
        nf = normalize_add(left, right).result
        total = I_plus(a) + I_plus(b)
        assert raw.value() == total
        assert nf.coeffs == tuple(encode(total).digits_lsd())
        assert nf.coeffs == coeffword_nf(total)


# ---------------------------------------------------------------------------
# Production unary TREE_RULES unchanged
# ---------------------------------------------------------------------------


def test_production_tree_rules_omit_every_add_identity():
    srcs = {src for src, _dst in TREE_RULES}
    for forbidden in (
        "S(x)+S(y)",
        "S(x+y)",
        "N(x)+N(y)",
        "N(x+y)",
        "I+(x)+I-(y)",
        "I+(x)+I+(y)",
        "I+(x+y)",
    ):
        assert forbidden not in srcs
    assert ("N(D(x))", "D(N(x))") in TREE_RULES
    assert _step(EAdd(EShift3(X), EShift3(Y))) == (
        EAdd(EShift3(X), EShift3(Y)),
        None,
    )
    assert _step(EAdd(EIp(X), EIm(Y))) == (EAdd(EIp(X), EIm(Y)), None)
    assert _step(EAdd(ENeg(X), ENeg(Y))) == (EAdd(ENeg(X), ENeg(Y)), None)
