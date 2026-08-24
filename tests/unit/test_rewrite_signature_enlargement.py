"""Phase-0: unary tree core plus Add / Mul / W.

The production engine in ``bt.calculus.rewrite`` stays the unary
fragment ``{D, I_a, S, N}`` with ``N(D) → D(N)``. Candidate Add/Mul
rules live only here. They are exact on ℤ when stated, and they are
**not** installed in ``_step``.

This file records:

* which natural binary rules are unsound (trit carry);
* that push-in ``S``-distributivity through Add or Mul creates a
  non-joining overlap with ``D(S(z)) → z``;
* that ``N``-through-Add alone is locally confluent on the named
  overlaps but not semantically complete;
* that a size-decreasing factor-out orientation repairs that Add peak;
  the finite exact Add factor-out set (including ``I+``/``I-``) is
  decided in ``test_rewrite_factor_out_add.py`` and is not a CAS;
* a bounded one-way word check for ``W``: the stock ``W``/``K3`` rules
  plus one-way ``N``–``D`` fail to join at ``N∘W∘W``, and the exact
  companion ``N∘K3 → K3∘N`` makes the bounded critical-pair list join.
  The full ``WORD_REWRITE_RULES`` table is not locally confluent;
  that production peak is recorded in ``test_rewrite_word_fragments.py``.
"""

from __future__ import annotations

from bt.calculus.derivative import D
from bt.calculus.expressions import (
    EAdd,
    ED,
    EI0,
    EIm,
    EInt,
    EIp,
    EMul,
    ENeg,
    EShift3,
    Expr,
    render,
)
from bt.calculus.integral import I_plus
from bt.calculus.rewrite import TREE_RULES, WORD_REWRITE_RULES, _step
from bt.calculus.semantics import evaluate

# Syntactic holes. Tree rules never inspect the integer payload.
X = EInt(0)
Y = EInt(1)
Z = EInt(2)


# ---------------------------------------------------------------------------
# Candidate extras (test-only). Production ``_step`` is unchanged.
# ---------------------------------------------------------------------------

def extra_n_through_add(expr: Expr) -> tuple[Expr, str | None]:
    if isinstance(expr, ENeg) and isinstance(expr.arg, EAdd):
        return (
            EAdd(ENeg(expr.arg.left), ENeg(expr.arg.right)),
            "N(x+y) → N(x)+N(y)",
        )
    return expr, None


def extra_s_through_add(expr: Expr) -> tuple[Expr, str | None]:
    if isinstance(expr, EShift3) and isinstance(expr.arg, EAdd):
        return (
            EAdd(EShift3(expr.arg.left), EShift3(expr.arg.right)),
            "S(x+y) → S(x)+S(y)",
        )
    return expr, None


def extra_i_through_add(expr: Expr) -> tuple[Expr, str | None]:
    if isinstance(expr, EIp) and isinstance(expr.arg, EAdd):
        return EAdd(EIp(expr.arg.left), EShift3(expr.arg.right)), "I+(x+y) → I+(x)+S(y)"
    if isinstance(expr, EIm) and isinstance(expr.arg, EAdd):
        return EAdd(EIm(expr.arg.left), EShift3(expr.arg.right)), "I-(x+y) → I-(x)+S(y)"
    if isinstance(expr, EI0) and isinstance(expr.arg, EAdd):
        return EAdd(EI0(expr.arg.left), EShift3(expr.arg.right)), "I0(x+y) → I0(x)+S(y)"
    return expr, None


def extra_n_through_mul(expr: Expr) -> tuple[Expr, str | None]:
    if isinstance(expr, ENeg) and isinstance(expr.arg, EMul):
        return EMul(ENeg(expr.arg.left), expr.arg.right), "N(x*y) → N(x)*y"
    return expr, None


def extra_s_through_mul(expr: Expr) -> tuple[Expr, str | None]:
    if isinstance(expr, EShift3) and isinstance(expr.arg, EMul):
        return EMul(EShift3(expr.arg.left), expr.arg.right), "S(x*y) → S(x)*y"
    return expr, None


def _is_s(expr: Expr) -> bool:
    """``I0 = S`` as integer maps; both are exact factor-out left-hand sides."""
    return isinstance(expr, (EShift3, EI0))


def factor_add_pair(left: Expr, right: Expr) -> tuple[Expr, str] | None:
    """Exact size-decreasing factor-out of one Add pair, or ``None``.

    Same-sign ``I_a(x)+I_a(y)`` is deliberately absent: it equals
    ``3(x+y)±2``, which is not ``I_b(x+y)`` for any trit ``b``.
    """
    if isinstance(left, ENeg) and isinstance(right, ENeg):
        return ENeg(EAdd(left.arg, right.arg)), "N(x)+N(y) → N(x+y)"
    if _is_s(left) and _is_s(right):
        return EShift3(EAdd(left.arg, right.arg)), "S(x)+S(y) → S(x+y)"
    if isinstance(left, EIp) and _is_s(right):
        return EIp(EAdd(left.arg, right.arg)), "I+(x)+S(y) → I+(x+y)"
    if _is_s(left) and isinstance(right, EIp):
        return EIp(EAdd(left.arg, right.arg)), "S(x)+I+(y) → I+(x+y)"
    if isinstance(left, EIm) and _is_s(right):
        return EIm(EAdd(left.arg, right.arg)), "I-(x)+S(y) → I-(x+y)"
    if _is_s(left) and isinstance(right, EIm):
        return EIm(EAdd(left.arg, right.arg)), "S(x)+I-(y) → I-(x+y)"
    if isinstance(left, EIp) and isinstance(right, EIm):
        return EShift3(EAdd(left.arg, right.arg)), "I+(x)+I-(y) → S(x+y)"
    if isinstance(left, EIm) and isinstance(right, EIp):
        return EShift3(EAdd(left.arg, right.arg)), "I-(x)+I+(y) → S(x+y)"
    return None


def extra_add_factor(expr: Expr) -> tuple[Expr, str | None]:
    """Size-decreasing opposite orientation. Documented, not a production core."""
    if isinstance(expr, EAdd):
        pair = factor_add_pair(expr.left, expr.right)
        if pair is not None:
            return pair
    return expr, None


def root_steps(expr: Expr, extras: list) -> list[Expr]:
    out: list[Expr] = []
    for fn in extras:
        nxt, reason = fn(expr)
        if reason is not None:
            out.append(nxt)
    nxt, reason = _step(expr)
    if reason is not None:
        out.append(nxt)
    return out


def one_steps(expr: Expr, extras: list) -> list[Expr]:
    """Every single-redex contraction, any position, unary + extras."""
    out = list(root_steps(expr, extras))
    if hasattr(expr, "arg"):
        for child in one_steps(expr.arg, extras):
            out.append(type(expr)(child))
    if isinstance(expr, (EAdd, EMul)):
        for child in one_steps(expr.left, extras):
            out.append(type(expr)(child, expr.right))
        for child in one_steps(expr.right, extras):
            out.append(type(expr)(expr.left, child))
    return out


def descendants(expr: Expr, extras: list, *, limit: int = 4_000) -> set[Expr]:
    seen = {expr}
    stack = [expr]
    while stack and len(seen) < limit:
        current = stack.pop()
        for nxt in one_steps(current, extras):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


def irreducible_descendants(expr: Expr, extras: list) -> set[Expr]:
    return {t for t in descendants(expr, extras) if not one_steps(t, extras)}


def nfs_of(expr: Expr, extras: list) -> set[str]:
    return {render(t) for t in irreducible_descendants(expr, extras)}


ADD_PUSH = [extra_n_through_add, extra_s_through_add, extra_i_through_add]
ADD_N_ONLY = [extra_n_through_add]
MUL_PUSH = [extra_n_through_mul, extra_s_through_mul]
ADD_FACTOR = [extra_add_factor]


# ---------------------------------------------------------------------------
# Rejected as unsound on ℤ
# ---------------------------------------------------------------------------

def test_d_through_add_is_unsound():
    """D(x+y) = D(x)+D(y) fails by balanced-trit carry. Witness x = y = 1."""
    assert D(1 + 1) == 1
    assert D(1) + D(1) == 0
    assert evaluate(ED(EAdd(EInt(1), EInt(1)))) == 1
    assert evaluate(EAdd(ED(EInt(1)), ED(EInt(1)))) == 0


def test_d_through_mul_is_unsound():
    """D(x*y) = D(x)*D(y) fails. Witness x = 2, y = 4."""
    assert D(2 * 4) == 3
    assert D(2) * D(4) == 1


def test_i_through_mul_is_unsound():
    """I_a(x*y) = I_a(x)*y fails. Witness a = +1, x = 1, y = 2."""
    assert I_plus(1 * 2) == 7
    assert I_plus(1) * 2 == 8


def test_i_plus_plus_i_plus_is_not_i_plus_of_sum():
    """I_a(x)+I_b(y) → I_{a+b}(x+y) is not total: a = b = +1 carries."""
    assert I_plus(1) + I_plus(1) == 8
    assert I_plus(1 + 1) == 7


def test_production_tree_rules_stay_unary():
    """Add/Mul extras must not land in the production TREE_RULES table."""
    srcs = {src for src, _dst in TREE_RULES}
    assert "N(x+y)" not in srcs
    assert "S(x+y)" not in srcs
    assert "S(x*y)" not in srcs
    assert ("N(D(x))", "D(N(x))") in TREE_RULES


# ---------------------------------------------------------------------------
# Add, push-in orientation (matches unary “N moves inward”)
# ---------------------------------------------------------------------------

def test_add_s_push_critical_pair_does_not_join():
    """Peak D(S(x+y)): D∘S → x+y versus S-distrib → D(S(x)+S(y))."""
    peak = ED(EShift3(EAdd(X, Y)))
    left = EAdd(X, Y)
    right = ED(EAdd(EShift3(X), EShift3(Y)))
    steps = one_steps(peak, ADD_PUSH)
    assert left in steps
    assert right in steps
    left_nf = irreducible_descendants(left, ADD_PUSH)
    right_nf = irreducible_descendants(right, ADD_PUSH)
    assert left_nf == {left}
    assert right_nf == {right}
    assert left_nf != right_nf
    # Semantic twins: both equal evaluate after plugging integers.
    for a, b in ((3, 5), (-4, 7), (0, 1), (-2, -2)):
        t_left = EAdd(EInt(a), EInt(b))
        t_right = ED(EAdd(EShift3(EInt(a)), EShift3(EInt(b))))
        assert evaluate(t_left) == evaluate(t_right) == a + b


def test_add_i_push_critical_pair_does_not_join():
    """Peak D(I+(x+y)): D∘I+ → x+y versus I-distrib → D(I+(x)+S(y))."""
    peak = ED(EIp(EAdd(X, Y)))
    left = EAdd(X, Y)
    right = ED(EAdd(EIp(X), EShift3(Y)))
    steps = one_steps(peak, ADD_PUSH)
    assert left in steps
    assert right in steps
    assert irreducible_descendants(left, ADD_PUSH) == {left}
    assert irreducible_descendants(right, ADD_PUSH) == {right}


def test_add_push_n_overlaps_join():
    """N-overlaps with Add remain joinable once N and S both distribute."""
    nny = ENeg(ENeg(EAdd(X, Y)))
    assert nfs_of(nny, ADD_PUSH) == {render(EAdd(X, Y))}
    nsy = ENeg(EShift3(EAdd(X, Y)))
    assert nfs_of(nsy, ADD_PUSH) == {render(EAdd(EShift3(ENeg(X)), EShift3(ENeg(Y))))}
    ndy = ENeg(ED(EAdd(X, Y)))
    assert nfs_of(ndy, ADD_PUSH) == {render(ED(EAdd(ENeg(X), ENeg(Y))))}


def test_add_n_only_named_overlaps_join():
    """N(x+y)→N(x)+N(y) alone: the N(N(Add)) overlap joins."""
    peak = ENeg(ENeg(EAdd(X, Y)))
    assert nfs_of(peak, ADD_N_ONLY) == {render(EAdd(X, Y))}
    # No S-distrib, so D(S(x+y)) has only the unary contraction.
    ds = ED(EShift3(EAdd(X, Y)))
    assert one_steps(ds, ADD_N_ONLY) == [EAdd(X, Y)]
    assert nfs_of(ds, ADD_N_ONLY) == {render(EAdd(X, Y))}


def test_add_n_only_has_s_semantic_twins():
    """Without S-distrib, S(x+y) and S(x)+S(y) are distinct irreducibles."""
    left = EShift3(EAdd(X, Y))
    right = EAdd(EShift3(X), EShift3(Y))
    assert left != right
    assert not one_steps(left, ADD_N_ONLY)
    assert not one_steps(right, ADD_N_ONLY)
    for a, b in ((3, 5), (-1, 8), (0, 0)):
        assert evaluate(EShift3(EAdd(EInt(a), EInt(b)))) == evaluate(
            EAdd(EShift3(EInt(a)), EShift3(EInt(b)))
        )


# ---------------------------------------------------------------------------
# Mul, push-in orientation
# ---------------------------------------------------------------------------

def test_mul_s_push_critical_pair_does_not_join():
    """Peak D(S(x*y)): D∘S → x*y versus S-distrib → D(S(x)*y)."""
    peak = ED(EShift3(EMul(X, Y)))
    left = EMul(X, Y)
    right = ED(EMul(EShift3(X), Y))
    steps = one_steps(peak, MUL_PUSH)
    assert left in steps
    assert right in steps
    assert irreducible_descendants(left, MUL_PUSH) == {left}
    assert irreducible_descendants(right, MUL_PUSH) == {right}
    for a, b in ((3, 5), (-2, 4), (1, 0)):
        assert evaluate(EMul(EInt(a), EInt(b))) == evaluate(
            ED(EMul(EShift3(EInt(a)), EInt(b)))
        )


def test_mul_push_n_overlaps_join():
    assert nfs_of(ENeg(ENeg(EMul(X, Y))), MUL_PUSH) == {render(EMul(X, Y))}
    nsy = ENeg(EShift3(EMul(X, Y)))
    assert nfs_of(nsy, MUL_PUSH) == {render(EMul(EShift3(ENeg(X)), Y))}


def test_mul_n_only_has_left_right_twins():
    """N(x)*y and x*N(y) are equal as functions; only left-push is a rule."""
    extras = [extra_n_through_mul]
    left = EMul(ENeg(X), Y)
    right = EMul(X, ENeg(Y))
    assert not one_steps(left, extras)
    assert not one_steps(right, extras)
    for a, b in ((3, 5), (-2, 7)):
        assert evaluate(EMul(ENeg(EInt(a)), EInt(b))) == evaluate(
            EMul(EInt(a), ENeg(EInt(b)))
        )


# ---------------------------------------------------------------------------
# Factor-out (opposite orientation): repairs the Add peak, then stop
# ---------------------------------------------------------------------------

def test_add_factor_repairs_d_of_s_sum():
    """S(x)+S(y) → S(x+y) makes D(S(x)+S(y)) join to x+y. Not a CAS."""
    peak = ED(EAdd(EShift3(X), EShift3(Y)))
    assert nfs_of(peak, ADD_FACTOR) == {render(EAdd(X, Y))}
    mixed = EAdd(ENeg(EShift3(X)), ENeg(EShift3(Y)))
    assert nfs_of(mixed, ADD_FACTOR) == {render(EShift3(ENeg(EAdd(X, Y))))}


def test_add_factor_does_not_identify_associated_sums():
    """(x+y)+z and x+(y+z) stay distinct irreducibles (KNOWN AC gap)."""
    left = EAdd(EAdd(X, Y), Z)
    right = EAdd(X, EAdd(Y, Z))
    assert not one_steps(left, ADD_FACTOR)
    assert not one_steps(right, ADD_FACTOR)
    assert evaluate(EAdd(EAdd(EInt(2), EInt(3)), EInt(4))) == evaluate(
        EAdd(EInt(2), EAdd(EInt(3), EInt(4)))
    )


# ---------------------------------------------------------------------------
# Small open-term census (one Add, unary wrappers, size ≤ 5)
# ---------------------------------------------------------------------------

UNARY = (ED, EIm, EI0, EIp, EShift3, ENeg)


def _binary_open_terms(max_size: int) -> list[Expr]:
    """Unary wrappers around one Add of holes, plus pure unary on X."""
    by_size: dict[int, list[Expr]] = {1: [X, Y]}
    terms: list[Expr] = [X, Y]
    for size in range(2, max_size + 1):
        found: list[Expr] = []
        for op in UNARY:
            for inner in by_size.get(size - 1, []):
                found.append(op(inner))
        if size >= 3:
            for left_size in range(1, size - 1):
                right_size = size - 1 - left_size
                for left in by_size.get(left_size, []):
                    for right in by_size.get(right_size, []):
                        found.append(EAdd(left, right))
        by_size[size] = found
        terms.extend(found)
    return terms


def test_add_push_census_finds_the_nonjoin():
    """Size-≤5 Add-unary terms: at least the documented D(S(Add)) non-join."""
    conflicts: list[str] = []
    for expr in _binary_open_terms(5):
        nfs = irreducible_descendants(expr, ADD_PUSH)
        if len(nfs) != 1:
            conflicts.append(
                f"{render(expr)} → {{{', '.join(sorted(render(t) for t in nfs))}}}"
            )
    assert any("D(S((" in c and "D((S(" in c for c in conflicts)
    # The peak itself is among them.
    peak = ED(EShift3(EAdd(X, Y)))
    assert len(irreducible_descendants(peak, ADD_PUSH)) == 2


def test_add_n_only_census_unique_nf_size_le_5():
    """N-through-Add alone: every size-≤5 term has a unique syntactic NF."""
    conflicts: list[str] = []
    for expr in _binary_open_terms(5):
        nfs = irreducible_descendants(expr, ADD_N_ONLY)
        if len(nfs) != 1:
            conflicts.append(render(expr))
            if len(conflicts) >= 6:
                break
    assert conflicts == []


# ---------------------------------------------------------------------------
# W: bounded one-way word fragment (not the full table)
# ---------------------------------------------------------------------------

ONE_WAY_W_RULES: list[tuple[tuple[str, ...], tuple[str, ...], str]] = [
    (("N", "N"), (), "NN"),
    (("D", "S"), (), "DS"),
    (("N", "S"), ("S", "N"), "NS"),
    (("N", "D"), ("D", "N"), "ND"),
    (("W", "W"), ("K3",), "WW"),
    (("W", "S"), ("W",), "WS"),
    (("K3", "S"), ("K3",), "K3S"),
    (("K3", "W"), ("W",), "K3W"),
    (("W", "K3"), ("W",), "WK3"),
    (("N", "W"), ("W", "N"), "NW"),
    (("K3", "K3"), ("K3",), "K3K3"),
]

N_K3 = (("N", "K3"), ("K3", "N"), "NK3")


def _word_steps(
    word: tuple[str, ...],
    rules: list[tuple[tuple[str, ...], tuple[str, ...], str]],
) -> list[tuple[str, ...]]:
    out: list[tuple[str, ...]] = []
    letters = list(word)
    for src, dst, _name in rules:
        k = len(src)
        for i in range(len(letters) - k + 1):
            if tuple(letters[i : i + k]) == src:
                out.append(tuple(letters[:i] + list(dst) + letters[i + k :]))
    return out


def _word_nfs(
    word: tuple[str, ...],
    rules: list[tuple[tuple[str, ...], tuple[str, ...], str]],
    *,
    limit: int = 400,
) -> set[tuple[str, ...]]:
    seen = {word}
    stack = [word]
    while stack and len(seen) < limit:
        current = stack.pop()
        for nxt in _word_steps(current, rules):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return {t for t in seen if not _word_steps(t, rules)}


def _word_critical_pairs(
    rules: list[tuple[tuple[str, ...], tuple[str, ...], str]],
) -> list[tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]]]:
    pairs: list[tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]]] = []
    for l1, r1, n1 in rules:
        for l2, r2, n2 in rules:
            for k in range(1, min(len(l1), len(l2)) + 1):
                if l1[-k:] != l2[:k]:
                    continue
                if k == len(l1) == len(l2) and (l1, r1) == (l2, r2):
                    continue
                peak = l1 + l2[k:]
                pairs.append((f"{n1} overlap {n2} k={k}", peak, r1 + l2[k:], l1[:-k] + r2))
            if len(l2) < len(l1):
                for i in range(len(l1) - len(l2) + 1):
                    if l1[i : i + len(l2)] == l2:
                        pairs.append(
                            (
                                f"{n2} in {n1} @{i}",
                                l1,
                                r1,
                                l1[:i] + r2 + l1[i + len(l2) :],
                            )
                        )
    return pairs


def test_word_table_still_has_two_way_nd_and_nw():
    """The production word table keeps reversible N∘D and N∘W; not a claim."""
    reasons = {rule.reason for rule in WORD_REWRITE_RULES}
    assert "N∘D = D∘N" in reasons
    assert "D∘N = N∘D" in reasons
    assert "N∘W = W∘N" in reasons
    assert "W∘N = N∘W" in reasons


def test_one_way_w_without_nk3_fails_at_nww():
    """N∘W∘W → K3∘N versus N∘K3: distinct irreducibles, equal as maps."""
    peak = ("N", "W", "W")
    left = ("W", "N", "W")
    right = ("N", "K3")
    steps = _word_steps(peak, ONE_WAY_W_RULES)
    assert left in steps
    assert right in steps
    assert _word_nfs(left, ONE_WAY_W_RULES) == {("K3", "N")}
    assert _word_nfs(right, ONE_WAY_W_RULES) == {("N", "K3")}
    failures = [
        name
        for name, _peak, lft, rgt in _word_critical_pairs(ONE_WAY_W_RULES)
        if _word_nfs(lft, ONE_WAY_W_RULES) != _word_nfs(rgt, ONE_WAY_W_RULES)
    ]
    assert failures


def test_one_way_w_with_nk3_bounded_cps_join():
    """Companion N∘K3 → K3∘N is exact; the bounded one-way CP list then joins.

    This is not a reason to install N∘K3 in WORD_REWRITE_RULES.
    The named opt-in fragment that does install it is WORD_WN_RULES
    (that fragment omits N∘D; the W+N+D enlargement with word I±
    sign-flips is WORD_WND_RULES).
    """
    rules = ONE_WAY_W_RULES + [N_K3]
    failures: list[str] = []
    for name, _peak, left, right in _word_critical_pairs(rules):
        if _word_nfs(left, rules) != _word_nfs(right, rules):
            failures.append(name)
    assert failures == []
    assert _word_nfs(("N", "W", "W"), rules) == {("K3", "N")}
    assert _word_nfs(("N", "K3"), rules) == {("K3", "N")}
