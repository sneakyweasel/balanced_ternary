"""Phase-0 census: unique syntactic NF for the operator-fragment tree TRS.

Fragment ``{D, I_a, S, N}`` under the tree rules in
``bt.calculus.rewrite`` (not the coefficient-word system, not
``WORD_REWRITE_RULES``). Open terms are unary trees with one hole.

This file records the fragment with the oriented commute
``N(D(x)) → D(N(x))`` (Lean ``rewrite_N_D``). Without that rule the
irreducibles ``N(D(x))`` and ``D(N(x))`` were a semantic pair; with it
they join, every critical pair still joins, and irreducibles inject
into integer functions on the size-``≤ 6`` box.
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
# D is pushable once N(D) → D(N) is a tree rule.
PUSHABLE = (EShift3, EIm, EIp, EI0, ED)


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

    # N(N(D(x))): outer N(N) vs inner N(D)
    peak = ENeg(ENeg(ED(x)))
    pairs.append(("N(N(D(x)))", peak, ED(x), ENeg(ED(ENeg(x)))))

    # N(D(I_a(x))) / N(D(S(x))): inner D-section vs outer N(D)
    peak = ENeg(ED(EIm(x)))
    pairs.append(("N(D(I-(x)))", peak, ENeg(x), ED(ENeg(EIm(x)))))
    peak = ENeg(ED(EIp(x)))
    pairs.append(("N(D(I+(x)))", peak, ENeg(x), ED(ENeg(EIp(x)))))
    peak = ENeg(ED(EI0(x)))
    pairs.append(("N(D(I0(x)))", peak, ENeg(x), ED(ENeg(EI0(x)))))
    peak = ENeg(ED(EShift3(x)))
    pairs.append(("N(D(S(x)))", peak, ENeg(x), ED(ENeg(EShift3(x)))))

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


def _is_depth_core(expr: Expr) -> bool:
    """D^k(x) or D^k(N(x))."""
    if isinstance(expr, EInt):
        return True
    if isinstance(expr, ENeg):
        return isinstance(expr.arg, EInt)
    if isinstance(expr, ED):
        return _is_depth_core(expr.arg)
    return False


def matches_nf_grammar(expr: Expr) -> bool:
    """{I-, I+, S}* then D^k then optional N at the hole."""
    if isinstance(expr, (EIm, EIp, EShift3)):
        return matches_nf_grammar(expr.arg)
    return _is_depth_core(expr)


def test_nf_grammar_matches_irreducibles():
    for expr in open_terms(6):
        if is_irreducible(expr):
            assert matches_nf_grammar(expr), render(expr)
        elif matches_nf_grammar(expr):
            raise AssertionError(f"grammar accepted a redex: {render(expr)}")


def test_nd_joins_to_dn():
    """The former semantic pair is now a one-step redex."""
    probes = list(range(-30, 31))
    for n in probes:
        t_nd = ENeg(ED(EInt(n)))
        t_dn = ED(ENeg(EInt(n)))
        assert t_nd != t_dn
        assert t_dn in one_steps(t_nd)
        assert is_irreducible(t_dn)
        assert not is_irreducible(t_nd)
        assert evaluate(t_nd) == evaluate(t_dn)
        nf_nd, _, _ = rewrite_expr(t_nd)
        nf_dn, _, _ = rewrite_expr(t_dn)
        assert nf_nd == nf_dn == t_dn


def _subst_hole(expr: Expr, n: int) -> Expr:
    if isinstance(expr, EInt):
        return EInt(n)
    return type(expr)(_subst_hole(expr.arg, n))


def _fingerprint(expr: Expr) -> tuple[int, ...]:
    probes = tuple(range(-20, 21)) + tuple(3**k for k in range(1, 6)) + tuple(
        (3**k - 1) // 2 for k in range(1, 6)
    )
    return tuple(evaluate(_subst_hole(expr, n)) for n in probes)


def test_irreducibles_have_unique_evaluate_fingerprints_size_le_6():
    """No two distinct NFs of size ≤ 6 agree on the probe set."""
    seen: dict[tuple[int, ...], Expr] = {}
    for expr in open_terms(6):
        if not is_irreducible(expr):
            continue
        key = _fingerprint(expr)
        prior = seen.get(key)
        assert prior is None or prior == expr, (
            f"{render(expr)} and {render(prior)} agree on probes"
        )
        seen[key] = expr


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
    nd = ENeg(ED(x))
    assert irreducible_descendants(nd) == {ED(ENeg(x))}
