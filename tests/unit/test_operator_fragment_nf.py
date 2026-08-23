"""Phase-0 census: enlarged operator-fragment TRS with N(D) → D(N).

Fragment ``{D, I_a, S, N}`` under the tree rules in
``bt.calculus.rewrite``, including ``N(D(x)) → D(N(x))`` (not the
coefficient-word system, not ``WORD_REWRITE_RULES``). Open terms are
unary trees with one hole.

This file records:

* every critical pair of the *enlarged* system joins, and every
  size-``≤ 6`` open term has a unique irreducible descendant under
  *all* redex orders (``COMPUTATIONALLY VERIFIED``);
* ``N(D(x))`` and ``D(N(x))`` now share the NF ``D(N(x))``;
* distinct irreducibles of size ``≤ 6`` disagree on a probe set that
  separates high ``D``-powers (``EXACT — HUMAN PROOF`` of uniqueness
  is the NF grammar plus unique balanced-ternary words; the census
  is the finite check).
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
from bt.calculus.rewrite import TREE_RULES, _step, rewrite_expr
from bt.calculus.semantics import evaluate

# Syntactic hole for open terms. Rules never inspect the integer.
VAR = EInt(0)

UNARY = (ED, EIm, EI0, EIp, EShift3, ENeg)

# Pushable constructors for the termination rank: N moves inward past
# each of these, including D after the new commute rule.
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

    # --- new pairs involving N(D(x)) → D(N(x)) ---

    # N(N(D(x))): outer N(N) vs inner N(D)
    peak = ENeg(ENeg(ED(x)))
    pairs.append(("N(N(D(x)))", peak, ED(x), ENeg(ED(ENeg(x)))))

    # N(D(I-(x))): outer N(D) vs inner D(I-)
    peak = ENeg(ED(EIm(x)))
    pairs.append(("N(D(I-(x)))", peak, ED(ENeg(EIm(x))), ENeg(x)))

    # N(D(I+(x))): outer N(D) vs inner D(I+)
    peak = ENeg(ED(EIp(x)))
    pairs.append(("N(D(I+(x)))", peak, ED(ENeg(EIp(x))), ENeg(x)))

    # N(D(I0(x))): outer N(D) vs inner D(I0)
    peak = ENeg(ED(EI0(x)))
    pairs.append(("N(D(I0(x)))", peak, ED(ENeg(EI0(x))), ENeg(x)))

    # N(D(S(x))): outer N(D) vs inner D(S)
    peak = ENeg(ED(EShift3(x)))
    pairs.append(("N(D(S(x)))", peak, ED(ENeg(EShift3(x))), ENeg(x)))

    return pairs


def test_tree_rules_include_n_d_commute():
    assert ("N(D(x))", "D(N(x))") in TREE_RULES


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


def test_nd_commute_drops_inversion_not_size():
    """N(D(x)) → D(N(x)) keeps size and drops the N-inversion coordinate."""
    peak = ENeg(ED(VAR))
    nxt = ED(ENeg(VAR))
    assert one_steps(peak) == [nxt]
    assert expr_size(peak) == expr_size(nxt)
    assert i0_count(peak) == i0_count(nxt) == 0
    assert n_inversion(peak) == 1
    assert n_inversion(nxt) == 0
    assert rank(nxt) < rank(peak)


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


def _is_core(expr: Expr) -> bool:
    """D-chain over x or N(x). N sits only on the hole."""
    if isinstance(expr, EInt):
        return True
    if isinstance(expr, ENeg):
        return isinstance(expr.arg, EInt)
    if isinstance(expr, ED):
        return _is_core(expr.arg)
    return False


def matches_nf_grammar(expr: Expr) -> bool:
    """I±/S spine over a D-chain ending in x or N(x)."""
    if isinstance(expr, (EIm, EIp, EShift3)):
        return matches_nf_grammar(expr.arg)
    return _is_core(expr)


def test_nf_grammar_matches_irreducibles():
    for expr in open_terms(6):
        if is_irreducible(expr):
            assert matches_nf_grammar(expr), render(expr)
        elif matches_nf_grammar(expr):
            raise AssertionError(f"grammar accepted a redex: {render(expr)}")


def test_nd_and_dn_share_nf():
    """The old semantic twins join after N(D) → D(N) is a tree rule."""
    probes = list(range(-30, 31))
    for n in probes:
        t_nd = ENeg(ED(EInt(n)))
        t_dn = ED(ENeg(EInt(n)))
        assert t_nd != t_dn
        assert not is_irreducible(t_nd)
        assert is_irreducible(t_dn)
        assert evaluate(t_nd) == evaluate(t_dn)
        nf_nd, _, _ = rewrite_expr(t_nd)
        nf_dn, _, _ = rewrite_expr(t_dn)
        assert nf_nd == t_dn
        assert nf_dn == t_dn
    # Open hole: same join.
    assert irreducible_descendants(ENeg(ED(VAR))) == {ED(ENeg(VAR))}


def _semantic_probes() -> list[int]:
    """Rich enough to separate D^d for d ≤ 5 (3^4 = 81 already exceeds 30)."""
    probes = set(range(-40, 41))
    for k in range(0, 9):
        p = 3**k
        for t in (-2, -1, 1, 2):
            for r in (-1, 0, 1):
                probes.add(t * p + r)
        probes.add(p)
        probes.add(-p)
    return sorted(probes)


def _plug(expr: Expr, n: int) -> Expr:
    if isinstance(expr, EInt):
        return EInt(n)
    if hasattr(expr, "arg"):
        return type(expr)(_plug(expr.arg, n))
    raise TypeError(f"unexpected node {type(expr).__name__}")


def test_distinct_irreducibles_disagree_on_probes():
    """No two distinct size-≤6 irreducibles agree on the probe set."""
    probes = _semantic_probes()
    signatures: dict[tuple[int, ...], Expr] = {}
    twins: list[str] = []
    for expr in open_terms(6):
        if not is_irreducible(expr):
            continue
        sig = tuple(evaluate(_plug(expr, n)) for n in probes)
        previous = signatures.get(sig)
        if previous is not None:
            twins.append(f"{render(previous)} ≡ {render(expr)}")
        else:
            signatures[sig] = expr
    assert twins == []


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
    # Nrm under N(D) still joins to the commute NF.
    nd_nrm = ENeg(ED(ENormalize(x)))
    assert irreducible_descendants(nd_nrm) == {ED(ENeg(x))}


def test_documented_peaks_from_rewrite_calculus_join():
    """Named peaks on the theory page still join, including the new N(D) ones."""
    x = VAR
    d_i0 = ED(EI0(x))
    assert irreducible_descendants(d_i0) == {x}
    nns = ENeg(ENeg(EShift3(x)))
    assert irreducible_descendants(nns) == {EShift3(x)}
    nnd = ENeg(ENeg(ED(x)))
    assert irreducible_descendants(nnd) == {ED(x)}
    nds = ENeg(ED(EShift3(x)))
    assert irreducible_descendants(nds) == {ENeg(x)}
    ndim = ENeg(ED(EIm(x)))
    assert irreducible_descendants(ndim) == {ENeg(x)}
