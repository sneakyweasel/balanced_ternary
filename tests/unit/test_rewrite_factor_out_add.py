"""Phase-0: finite exact factor-out Add versus AC / CAS.

Production ``bt.calculus.rewrite._step`` stays the unary fragment.
Candidate extras live only here and in
``test_rewrite_signature_enlargement.py``.

The finite exact-on-ℤ factor-out set is ``factor_add_pair``:
``S+S``, ``N+N``, ``I_a+S``, ``S+I_a``, and opposite-sign
``I++I- → S``. Same-sign ``I_a+I_a`` has no exact unary-constructor
right-hand side.

This file records:

* binary (adjacent-only) factor-out repairs ``D(S(x)+S(y))`` and
  joins the named unary overlaps, but leaves semantic twins that are
  not AC-equivalent (``S(x)+(S(y)+z)`` versus ``S(x+y)+z``);
* AC-matching of that same finite set collects non-adjacent ``S``
  summands, then fails local confluence modulo AC at
  ``I+(x)+S(y)+I+(z)`` (same-sign residue ``±2``);
* completing either system needs flattened AC matching plus constants
  or carry — already a computer-algebra engine. Not installed.
"""

from __future__ import annotations

from bt.calculus.expressions import (
    EAdd,
    ED,
    EI0,
    EIm,
    EInt,
    EIp,
    ENeg,
    EShift3,
    Expr,
    expr_size,
    render,
)
from bt.calculus.integral import I_minus, I_plus
from bt.calculus.rewrite import TREE_RULES, _step
from bt.calculus.semantics import evaluate

# Syntactic holes. Tree rules never inspect the integer payload.
X = EInt(0)
Y = EInt(1)
Z = EInt(2)


def _is_s(expr: Expr) -> bool:
    return isinstance(expr, (EShift3, EI0))


def factor_add_pair(left: Expr, right: Expr) -> tuple[Expr, str] | None:
    """Exact size-decreasing factor-out of one Add pair, or ``None``."""
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
    if isinstance(expr, EAdd):
        pair = factor_add_pair(expr.left, expr.right)
        if pair is not None:
            return pair
    return expr, None


ADD_FACTOR = [extra_add_factor]


def one_steps(expr: Expr, extras: list) -> list[Expr]:
    out: list[Expr] = []
    for fn in extras:
        nxt, reason = fn(expr)
        if reason is not None:
            out.append(nxt)
    nxt, reason = _step(expr)
    if reason is not None:
        out.append(nxt)
    if hasattr(expr, "arg"):
        for child in one_steps(expr.arg, extras):
            out.append(type(expr)(child))
    if isinstance(expr, EAdd):
        for child in one_steps(expr.left, extras):
            out.append(EAdd(child, expr.right))
        for child in one_steps(expr.right, extras):
            out.append(EAdd(expr.left, child))
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

# ---------------------------------------------------------------------------
# AC matching of the same finite pair table (test-only; not a CAS)
# ---------------------------------------------------------------------------


def flatten_add(expr: Expr) -> list[Expr]:
    if isinstance(expr, EAdd):
        return flatten_add(expr.left) + flatten_add(expr.right)
    return [expr]


def unflatten_add(parts: list[Expr]) -> Expr:
    if not parts:
        raise ValueError("empty sum")
    acc = parts[-1]
    for part in reversed(parts[:-1]):
        acc = EAdd(part, acc)
    return acc


def ac_canonical(expr: Expr) -> str:
    """Flatten-and-sort Add; unary structure is kept."""
    if isinstance(expr, EAdd):
        parts = sorted(ac_canonical(part) for part in flatten_add(expr))
        return "(" + "+".join(parts) + ")"
    if isinstance(expr, EInt):
        return str(expr.value)
    if hasattr(expr, "arg"):
        tag = {
            ENeg: "N",
            ED: "D",
            EIm: "I-",
            EI0: "I0",
            EIp: "I+",
            EShift3: "S",
        }[type(expr)]
        return f"{tag}({ac_canonical(expr.arg)})"
    return render(expr)


def ac_factor_root(expr: Expr) -> list[Expr]:
    if not isinstance(expr, EAdd):
        return []
    parts = flatten_add(expr)
    out: list[Expr] = []
    seen: set[str] = set()
    for i, left in enumerate(parts):
        for j, right in enumerate(parts):
            if j <= i:
                continue
            pair = factor_add_pair(left, right)
            if pair is None:
                continue
            factored, _reason = pair
            new_parts = [part for k, part in enumerate(parts) if k not in (i, j)]
            new_parts.append(factored)
            nxt = unflatten_add(new_parts)
            key = render(nxt)
            if key not in seen:
                seen.add(key)
                out.append(nxt)
    return out


def ac_one_steps(expr: Expr) -> list[Expr]:
    out = list(ac_factor_root(expr))
    nxt, reason = _step(expr)
    if reason is not None:
        out.append(nxt)
    if hasattr(expr, "arg"):
        for child in ac_one_steps(expr.arg):
            out.append(type(expr)(child))
    if isinstance(expr, EAdd):
        for child in ac_one_steps(expr.left):
            out.append(EAdd(child, expr.right))
        for child in ac_one_steps(expr.right):
            out.append(EAdd(expr.left, child))
    return out


def ac_descendants(expr: Expr, *, limit: int = 4_000) -> set[Expr]:
    seen = {expr}
    stack = [expr]
    while stack and len(seen) < limit:
        current = stack.pop()
        for nxt in ac_one_steps(current):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return seen


def ac_irreducibles(expr: Expr) -> set[Expr]:
    return {t for t in ac_descendants(expr) if not ac_one_steps(t)}


def ac_nf_keys(expr: Expr) -> set[str]:
    return {ac_canonical(t) for t in ac_irreducibles(expr)}


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


PROBES: tuple[dict[int, int], ...] = (
    {0: 3, 1: 5, 2: 7},
    {0: -4, 1: 2, 2: 1},
    {0: 0, 1: 0, 2: 0},
    {0: 1, 1: -1, 2: 8},
    {0: -2, 1: -3, 2: 4},
)


def fingerprints(expr: Expr) -> tuple[int, ...]:
    return tuple(evaluate(plug(expr, env)) for env in PROBES)


# ---------------------------------------------------------------------------
# Exactness of the finite pair table
# ---------------------------------------------------------------------------


def test_factor_pairs_are_exact_on_z():
    samples = ((3, 5), (-2, 4), (0, 1), (-7, -1))
    for a, b in samples:
        assert 3 * a + 3 * b == 3 * (a + b)
        assert -(a + b) == (-a) + (-b)
        assert I_plus(a) + 3 * b == I_plus(a + b)
        assert 3 * a + I_plus(b) == I_plus(a + b)
        assert I_minus(a) + 3 * b == I_minus(a + b)
        assert I_plus(a) + I_minus(b) == 3 * (a + b)
        assert I_minus(a) + I_plus(b) == 3 * (a + b)


def test_same_sign_pairs_are_not_in_the_finite_table():
    assert factor_add_pair(EIp(X), EIp(Y)) is None
    assert factor_add_pair(EIm(X), EIm(Y)) is None


def test_same_sign_i_plus_is_not_any_i_b_of_the_sum():
    """I+(x)+I+(y) = 3(x+y)+2, and 2 is not a trit."""
    for a, b in ((1, 1), (3, 5), (0, 0), (-2, 4)):
        value = I_plus(a) + I_plus(b)
        assert value == 3 * (a + b) + 2
        assert value != 3 * (a + b)
        assert value != I_plus(a + b)
        assert value != I_minus(a + b)


def test_same_sign_i_minus_is_not_any_i_b_of_the_sum():
    for a, b in ((1, 1), (3, 5), (0, 0)):
        value = I_minus(a) + I_minus(b)
        assert value == 3 * (a + b) - 2
        assert value != I_plus(a + b)
        assert value != I_minus(a + b)
        assert value != 3 * (a + b)


def test_factor_out_decreases_size():
    pairs = (
        EAdd(EShift3(X), EShift3(Y)),
        EAdd(ENeg(X), ENeg(Y)),
        EAdd(EIp(X), EShift3(Y)),
        EAdd(EIp(X), EIm(Y)),
        EAdd(EI0(X), EShift3(Y)),
    )
    for term in pairs:
        nxt, reason = extra_add_factor(term)
        assert reason is not None
        assert expr_size(nxt) == expr_size(term) - 1


def test_production_tree_rules_still_omit_factor_out():
    srcs = {src for src, _dst in TREE_RULES}
    assert "S(x)+S(y)" not in srcs
    assert "I+(x)+I-(y)" not in srcs
    assert "N(x)+N(y)" not in srcs
    assert ("N(D(x))", "D(N(x))") in TREE_RULES


# ---------------------------------------------------------------------------
# Binary matching: D∘S peak stays repaired; AC twins remain
# ---------------------------------------------------------------------------


def test_binary_factor_still_repairs_d_of_s_sum():
    peak = ED(EAdd(EShift3(X), EShift3(Y)))
    assert nfs_of(peak, ADD_FACTOR) == {render(EAdd(X, Y))}


def test_binary_factor_repairs_d_of_i_plus_s():
    peak = ED(EAdd(EIp(X), EShift3(Y)))
    assert nfs_of(peak, ADD_FACTOR) == {render(EAdd(X, Y))}


def test_binary_factor_opposite_sign_joins_to_s():
    term = EAdd(EIp(X), EIm(Y))
    assert nfs_of(term, ADD_FACTOR) == {render(EShift3(EAdd(X, Y)))}


def test_binary_n_s_overlap_joins():
    """N(S(x))+N(S(y)) joins by factor-out or by pushing N first."""
    peak = EAdd(ENeg(EShift3(X)), ENeg(EShift3(Y)))
    assert nfs_of(peak, ADD_FACTOR) == {render(EShift3(ENeg(EAdd(X, Y))))}


def test_binary_adjacent_s_misses_associated_sum():
    """S(x)+(S(y)+z) is irreducible; S(x+y)+z is a distinct AC-class."""
    nested = EAdd(EShift3(X), EAdd(EShift3(Y), Z))
    collected = EAdd(EShift3(EAdd(X, Y)), Z)
    assert not one_steps(nested, ADD_FACTOR)
    assert not one_steps(collected, ADD_FACTOR)
    assert ac_canonical(nested) != ac_canonical(collected)
    assert fingerprints(nested) == fingerprints(collected)


def test_binary_associated_s_sum_is_a_one_way_redex():
    """(S(x)+S(y))+z factors the adjacent pair; the other association does not."""
    left = EAdd(EAdd(EShift3(X), EShift3(Y)), Z)
    assert nfs_of(left, ADD_FACTOR) == {render(EAdd(EShift3(EAdd(X, Y)), Z))}
    right = EAdd(EShift3(X), EAdd(EShift3(Y), Z))
    assert nfs_of(right, ADD_FACTOR) == {render(right)}


def test_binary_i_plus_association_twins():
    """I+(x+y)+I+(z) and I+(x)+I+(y+z) are stuck and not AC-equivalent."""
    left = EAdd(EIp(EAdd(X, Y)), EIp(Z))
    right = EAdd(EIp(X), EIp(EAdd(Y, Z)))
    assert not one_steps(left, ADD_FACTOR)
    assert not one_steps(right, ADD_FACTOR)
    assert ac_canonical(left) != ac_canonical(right)
    assert fingerprints(left) == fingerprints(right)
    assert fingerprints(left) == tuple(3 * (env[0] + env[1] + env[2]) + 2 for env in PROBES)


def test_constant_twin_of_same_sign_i_plus():
    """If integer constants are summands, I+(x)+I+(y) twins S(x+y)+2."""
    left = EAdd(EIp(X), EIp(Y))
    right = EAdd(EShift3(EAdd(X, Y)), EInt(2))
    assert not one_steps(left, ADD_FACTOR)
    assert not one_steps(right, ADD_FACTOR)
    for a, b in ((3, 5), (0, 0), (-1, 4)):
        assert evaluate(EAdd(EIp(EInt(a)), EIp(EInt(b)))) == evaluate(
            EAdd(EShift3(EAdd(EInt(a), EInt(b))), EInt(2))
        )


# ---------------------------------------------------------------------------
# AC-matching: S-collection joins; same-sign I_a peak does not
# ---------------------------------------------------------------------------


def test_ac_matching_collects_nonadjacent_s():
    nested = EAdd(EShift3(X), EAdd(EShift3(Y), Z))
    assert ac_nf_keys(nested) == {ac_canonical(EAdd(EShift3(EAdd(X, Y)), Z))}


def test_ac_matching_three_s_join_modulo_ac():
    peak = EAdd(EShift3(X), EAdd(EShift3(Y), EShift3(Z)))
    assert ac_nf_keys(peak) == {ac_canonical(EShift3(EAdd(EAdd(X, Y), Z)))}


def test_ac_matching_opposite_sign_with_s_joins():
    peak = EAdd(EIp(X), EAdd(EShift3(Y), EIm(Z)))
    assert ac_nf_keys(peak) == {ac_canonical(EShift3(EAdd(EAdd(X, Y), Z)))}


def test_ac_matching_i_plus_s_i_plus_does_not_join():
    """Peak I+(x)+S(y)+I+(z): two factor-outs, two stuck same-sign sums."""
    peak = EAdd(EIp(X), EAdd(EShift3(Y), EIp(Z)))
    steps = ac_factor_root(peak)
    left = EAdd(EIp(EAdd(X, Y)), EIp(Z))
    right = EAdd(EIp(X), EIp(EAdd(Y, Z)))
    assert any(ac_canonical(t) == ac_canonical(left) for t in steps)
    assert any(ac_canonical(t) == ac_canonical(right) for t in steps)
    left_nf = ac_irreducibles(left)
    right_nf = ac_irreducibles(right)
    assert {ac_canonical(t) for t in left_nf} == {ac_canonical(left)}
    assert {ac_canonical(t) for t in right_nf} == {ac_canonical(right)}
    assert ac_canonical(left) != ac_canonical(right)
    assert fingerprints(left) == fingerprints(right)


def test_ac_matching_i_minus_s_i_minus_does_not_join():
    peak = EAdd(EIm(X), EAdd(EShift3(Y), EIm(Z)))
    keys = ac_nf_keys(peak)
    assert ac_canonical(EAdd(EIm(EAdd(X, Y)), EIm(Z))) in keys
    assert ac_canonical(EAdd(EIm(X), EIm(EAdd(Y, Z)))) in keys
    assert len(keys) >= 2


# ---------------------------------------------------------------------------
# Bounded census: small flattened sums of small unary atoms
# ---------------------------------------------------------------------------

UNARY = (ED, EIm, EI0, EIp, EShift3, ENeg)


def _unary_atoms() -> list[Expr]:
    holes = (X, Y, Z)
    atoms = list(holes)
    for hole in holes:
        for op in UNARY:
            atoms.append(op(hole))
    pairs = (EAdd(X, Y), EAdd(Y, Z), EAdd(X, Z))
    for pair in pairs:
        for op in (EShift3, EIp, EIm, ENeg, ED):
            atoms.append(op(pair))
    return atoms


def test_binary_census_unique_syntactic_nf_on_pairs():
    """Every Add of two small atoms has a unique binary-factor NF."""
    atoms = _unary_atoms()
    conflicts: list[str] = []
    for left in atoms:
        for right in atoms:
            expr = EAdd(left, right)
            nfs = irreducible_descendants(expr, ADD_FACTOR)
            if len(nfs) != 1:
                conflicts.append(render(expr))
                if len(conflicts) >= 8:
                    break
        if conflicts:
            break
    assert conflicts == []


def test_binary_census_finds_non_ac_semantic_twins():
    """Among pair-NFs, at least the documented S-association twins collide."""
    nested = EAdd(EShift3(X), EAdd(EShift3(Y), Z))
    collected = EAdd(EShift3(EAdd(X, Y)), Z)
    irreducibles = [
        t
        for t in (nested, collected)
        if not one_steps(t, ADD_FACTOR)
    ]
    assert len(irreducibles) == 2
    assert fingerprints(nested) == fingerprints(collected)
    assert ac_canonical(nested) != ac_canonical(collected)


def test_ac_census_triple_s_unique_and_i_plus_peak_present():
    """Bounded triple sums: S-only triples join; the I+ peak stays split."""
    s_triples = [
        EAdd(EShift3(X), EAdd(EShift3(Y), EShift3(Z))),
        EAdd(EAdd(EShift3(X), EShift3(Y)), EShift3(Z)),
        EAdd(EShift3(Z), EAdd(EShift3(X), EShift3(Y))),
    ]
    for term in s_triples:
        assert len(ac_nf_keys(term)) == 1
    peak = EAdd(EIp(X), EAdd(EShift3(Y), EIp(Z)))
    assert len(ac_nf_keys(peak)) >= 2
