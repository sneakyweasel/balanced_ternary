"""Phase-0 census: unique syntactic NF for the operator-fragment tree TRS.

Fragment ``{D, I_a, S, N}`` under the tree rules in
``bt.calculus.rewrite`` (not the coefficient-word system, not
``WORD_REWRITE_RULES``). Open terms are unary trees with one hole.

This file records two facts:

* every critical pair joins, and every size-``≤ 6`` open term has a
  unique irreducible descendant under *all* redex orders
  (``COMPUTATIONALLY VERIFIED``);
* ``N(D(x))`` and ``D(N(x))`` are distinct irreducibles that agree on
  integer probes — the tree rules are not a complete equational
  canonical form for the integer operator algebra.
"""

from __future__ import annotations

from bt.calculus.expressions import (
    ED,
    EI0,
    EIm,
    EInt,
    EIp,
    ENeg,
    ENormalize,
    EShift3,
    Expr,
    expr_size,
    render,
)
from bt.calculus.rewrite import _step, rewrite_expr
from bt.calculus.semantics import evaluate

# Syntactic hole for open terms. Rules never inspect the integer.
VAR = EInt(0)

UNARY = (ED, EIm, EI0, EIp, EShift3, ENeg)

# Primitive tree rules of the fragment, matching TREE_RULES minus Nrm.
# The engine also contracts N(I0(x)) → S(N(x)); that is a derived
# shortcut of I0 → S followed by N(S) → S(N), included as a one-step.
PUSHABLE = (EShift3, EIm, EIp, EI0)


def _rebuild(expr: Expr, new_arg: Expr) -> Expr:
    return type(expr)(new_arg)


def one_steps(expr: Expr) -> list[Expr]:
    """Every single-redex contraction, any position (not just innermost)."""
    out: list[Expr] = []
    nxt, reason = _step(expr)
    if reason is not None:
        out.append(nxt)
    if isinstance(expr, (EInt,)):
        return out
    if hasattr(expr, "arg"):
        for child in one_steps(expr.arg):
            out.append(_rebuild(expr, child))
    return out


def is_irreducible(expr: Expr) -> bool:
    return not one_steps(expr)


def descendants(expr: Expr) -> set[Expr]:
    seen = {expr}
    stack = [expr]
    while stack:
        current = stack.pop()
        for nxt in one_steps(current):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


def irreducible_descendants(expr: Expr) -> set[Expr]:
    return {t for t in descendants(expr) if is_irreducible(t)}


def joinable(left: Expr, right: Expr) -> bool:
    return bool(descendants(left) & descendants(right))


def open_terms(max_size: int) -> list[Expr]:
    by_size: dict[int, list[Expr]] = {1: [VAR]}
    for size in range(2, max_size + 1):
        by_size[size] = [op(inner) for op in UNARY for inner in by_size[size - 1]]
    terms: list[Expr] = []
    for size in range(1, max_size + 1):
        terms.extend(by_size[size])
    return terms


def i0_count(expr: Expr) -> int:
    if isinstance(expr, EI0):
        return 1 + i0_count(expr.arg)
    if hasattr(expr, "arg"):
        return i0_count(expr.arg)
    return 0


def n_inversion(expr: Expr) -> int:
    """Pairs (N-node, pushable descendant). Decreases on every N-push."""

    def pushable_descendants(node: Expr) -> int:
        if isinstance(node, PUSHABLE):
            return 1 + pushable_descendants(node.arg)
        if hasattr(node, "arg"):
            return pushable_descendants(node.arg)
        return 0

    if isinstance(expr, ENeg):
        return pushable_descendants(expr.arg) + n_inversion(expr.arg)
    if hasattr(expr, "arg"):
        return n_inversion(expr.arg)
    return 0


def rank(expr: Expr) -> tuple[int, int, int]:
    return (i0_count(expr), n_inversion(expr), expr_size(expr))


# ---------------------------------------------------------------------------
# Critical pairs (Knuth–Bendix: non-variable overlap of two LHS)
# ---------------------------------------------------------------------------

def _x() -> Expr:
    return VAR


def critical_pairs() -> list[tuple[str, Expr, Expr, Expr]]:
    """Peak term and the two one-step contractions of each overlap."""
    x = _x()
    pairs: list[tuple[str, Expr, Expr, Expr]] = []

    # D(I0(x)): root D(I0) → x  vs  inner I0 → S, giving D(S(x))
    peak = ED(EI0(x))
    pairs.append(("D(I0(x))", peak, x, ED(EShift3(x))))

    # N(N(N(x))): outer N(N) vs inner N(N)
    peak = ENeg(ENeg(ENeg(x)))
    pairs.append(("N(N(N(x)))", peak, ENeg(x), ENeg(x)))

    # N(N(S(x))): outer N(N) vs inner N(S)
    peak = ENeg(ENeg(EShift3(x)))
    pairs.append(("N(N(S(x)))", peak, EShift3(x), ENeg(EShift3(ENeg(x)))))

    # N(N(I-(x))): outer N(N) vs inner N(I-)
    peak = ENeg(ENeg(EIm(x)))
    pairs.append(("N(N(I-(x)))", peak, EIm(x), ENeg(EIp(ENeg(x)))))

    # N(N(I+(x))): outer N(N) vs inner N(I+)
    peak = ENeg(ENeg(EIp(x)))
    pairs.append(("N(N(I+(x)))", peak, EIp(x), ENeg(EIm(ENeg(x)))))

    # N(I0(x)): engine shortcut N(I0) → S(N) vs inner I0 → S
    peak = ENeg(EI0(x))
    pairs.append(("N(I0(x))", peak, EShift3(ENeg(x)), ENeg(EShift3(x))))

    # N(N(I0(x))): outer N(N) vs inner N(I0) / I0
    peak = ENeg(ENeg(EI0(x)))
    pairs.append(("N(N(I0(x)))", peak, EI0(x), ENeg(EShift3(ENeg(x)))))

    return pairs


def test_critical_pairs_join():
    for name, peak, left, right in critical_pairs():
        steps = one_steps(peak)
        assert left in steps, f"{name}: missing left contraction {render(left)}"
        assert right in steps, f"{name}: missing right contraction {render(right)}"
        left_nfs = irreducible_descendants(left)
        right_nfs = irreducible_descendants(right)
        assert left_nfs == right_nfs, (
            f"{name} does not join: { {render(t) for t in left_nfs} } vs "
            f"{ {render(t) for t in right_nfs} }"
        )
        assert len(left_nfs) == 1, f"{name}: branched after the peak"
        assert joinable(left, right)


def test_one_step_rank_decreases():
    """Every tree-rule step strictly decreases (I0-count, N-inversion, size)."""
    for expr in open_terms(5):
        r0 = rank(expr)
        for nxt in one_steps(expr):
            assert rank(nxt) < r0, (
                f"{render(expr)} → {render(nxt)}: rank {rank(nxt)} not < {r0}"
            )


def test_open_terms_size_le_6_unique_nf():
    terms = open_terms(6)
    assert len(terms) == (6**6 - 1) // 5  # 1 + 6 + 36 + 216 + 1296 + 7776
    conflicts: list[str] = []
    for expr in terms:
        nfs = irreducible_descendants(expr)
        if len(nfs) != 1:
            conflicts.append(
                f"{render(expr)} → {{{', '.join(sorted(render(t) for t in nfs))}}}"
            )
            if len(conflicts) >= 8:
                break
        innermost, _reasons, _steps = rewrite_expr(expr)
        assert innermost in nfs
        assert is_irreducible(innermost)
    assert conflicts == []


def test_innermost_agrees_with_all_strategy_nf():
    """rewrite_expr (innermost-left) matches the unique all-strategy NF."""
    for expr in open_terms(5):
        nfs = irreducible_descendants(expr)
        assert len(nfs) == 1
        innermost, _, _ = rewrite_expr(expr)
        assert innermost == next(iter(nfs))


def _is_safe(expr: Expr) -> bool:
    """Legal argument of D in an irreducible: x, D(Safe), or N(Safe)."""
    if isinstance(expr, EInt):
        return True
    if isinstance(expr, ED):
        return _is_safe(expr.arg)
    if isinstance(expr, ENeg):
        return _is_safe(expr.arg) and not isinstance(expr.arg, (ENeg, *PUSHABLE))
    return False


def matches_nf_grammar(expr: Expr) -> bool:
    """N pushed past I±/S/I0; then I/S-spine; D only over a D-safe argument."""
    if isinstance(expr, EInt):
        return True
    if isinstance(expr, (EIm, EIp, EShift3)):
        return matches_nf_grammar(expr.arg)
    if isinstance(expr, ED):
        return _is_safe(expr.arg)
    if isinstance(expr, ENeg):
        return _is_safe(expr.arg) and not isinstance(expr.arg, (ENeg, *PUSHABLE))
    return False


def test_nf_grammar_matches_irreducibles():
    for expr in open_terms(6):
        if is_irreducible(expr):
            assert matches_nf_grammar(expr), render(expr)
        elif matches_nf_grammar(expr):
            raise AssertionError(f"grammar accepted a redex: {render(expr)}")


def test_nd_dn_are_distinct_irreducibles_with_equal_evaluate():
    """Semantic incompleteness, not a confluence failure.

    N(D(n)) and D(N(n)) are both irreducible under the tree rules and
    agree as integer functions. The Lean identity rewrite_N_D is not a
    tree rule. Unique *syntactic* NF can hold while the NF is not a
    unique representative of the integer operator algebra.
    """
    probes = list(range(-30, 31))
    for n in probes:
        t_nd = ENeg(ED(EInt(n)))
        t_dn = ED(ENeg(EInt(n)))
        assert t_nd != t_dn
        assert is_irreducible(t_nd)
        assert is_irreducible(t_dn)
        assert evaluate(t_nd) == evaluate(t_dn)
        nf_nd, _, _ = rewrite_expr(t_nd)
        nf_dn, _, _ = rewrite_expr(t_dn)
        assert nf_nd == t_nd
        assert nf_dn == t_dn


def test_nrm_is_a_destructor_and_does_not_create_a_new_overlap():
    """Optional TREE_RULES row Nrm(x) → x. No non-variable overlap."""
    x = VAR
    nrm = ENormalize(x)
    assert one_steps(nrm) == [x]
    nested = ENormalize(ENormalize(ED(x)))
    assert irreducible_descendants(nested) == {ED(x)}
    # Nrm does not appear in any other LHS, so no new critical pair.
    peak = ENeg(ENormalize(EShift3(x)))
    assert irreducible_descendants(peak) == {EShift3(ENeg(x))}


def test_documented_peaks_from_rewrite_calculus_join():
    """The two peaks already named on the theory page still join."""
    x = VAR
    d_i0 = ED(EI0(x))
    assert irreducible_descendants(d_i0) == {x}
    nns = ENeg(ENeg(EShift3(x)))
    assert irreducible_descendants(nns) == {EShift3(x)}
