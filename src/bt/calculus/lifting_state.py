"""Minimal finite-horizon state of the 3-adic lifting machine.

The lifting tree of ``f(x) ≡ 0 (mod 3^k)`` is the zero-output subtree of
the residual Mealy machine (see :mod:`bt.calculus.lifting`). This module
asks how much of a residual state is actually needed to determine the
next ``r`` levels of that subtree, and answers it exactly in the deep
regime.

Behaviour
---------

The observable is the ordered, trit-labelled depth-``r`` subtree, already
computed by :func:`bt.calculus.lifting.depth_r_shape` in ``digits`` mode.
Two states are ``r``-equivalent when those trees coincide, so the
equivalence is a fibre of a function and needs no separate closure work.

Unit scaling
------------

On a *surviving* branch ``ρ_a(g) = 0``, hence

    𝔇_a(λg)(x) = (λg(a+3x) - 0)/3 = λ 𝔇_a g(x)

and ``3 | λg(a)`` iff ``3 | g(a)`` for ``λ`` coprime to 3. By induction
on ``r`` the whole ordered depth-``r`` subtree is invariant under
``g ↦ λg``, while ``Φ_r(λg) ≠ Φ_r(g)`` in general. So ``Φ_r`` is
sufficient but **not** minimal, and the failure is structural rather than
a sporadic coincidence.

Deep regime
-----------

For a node at level ``k ≥ r`` the residual is ``≡_r`` the linear state
``c + bx`` with ``c = f(n)/3^k`` and ``b = f'(n)``, and linear states are
closed under the section operators:

    𝔇_a(c + bx) = 𝔇(c + ab) + b x

so ``b`` is invariant along the tree and only the constant moves. On a
surviving branch the constant is exactly ``(c + ab)/3``. Two consequences,
both exact:

* ``3 ∤ b``: one child per level, the surviving trit at each step is
  ``-ρ(u)`` for ``u = c/b``, and the state evolves by ``u ↦ 𝔇(u)``. The
  lifting path is the balanced expansion of ``-c/b``. This is Newton's
  iteration in balanced digits, so the *identification* is a
  reparameterization; the counting statement around it is not.
* ``3 | b``: survival is ``3 | c`` regardless of the trit, so branching is
  all-or-nothing and the subtree is either empty or fully ternary.

Counting these gives ``3^{r-e} + e`` behaviours at ``e = min(v_3(b), r)``
and ``L_r = Σ_{j≤r} 3^j + r`` in total.

The block shift law
-------------------

The singular count turns on one exact identity. Scaling so that
``b = 3^e``, a trit word ``w`` of length ``j ≤ e`` sends the state
``(3^j d, 3^{j+i})`` to ``(d + 3^i · packWord(w), 3^{j+i})``. At
``i = 0``, ``j = e`` the leaf reached by ``w`` is

    (d + packWord(w), 3^e),

so the shift is the *balanced value* of the word, not its digit sum, and
``packWord`` is a bijection from length-``e`` trit words onto the window

    W_e = [-(3^e-1)/2, (3^e-1)/2]

of ``3^e`` consecutive integers. That window is a complete residue system
modulo ``3^e``, so it contains exactly one ``t`` with ``3^e | d + t``, and
that single deep leaf drives the whole recursion.

Minimal state
-------------

The upshot is a normal form rather than only a count. Scale so that
``b ≡ 3^e`` with ``e = min(v_3(b), r)``, and split by whether the constant
or the derivative dominates:

* ``v_3(c) < e`` — *dominated*. The behaviour is the fully ternary tree
  truncated at depth ``v_3(c)``, and nothing else about the state
  survives. ``r`` classes.
* ``v_3(c) ≥ e`` — *undominated*. The behaviour is exactly the
  unit-scaling orbit of ``(c, b)`` modulo ``3^r``, with no further
  collapse. ``(3^{r+1}-1)/2`` classes.

So the minimal state is the unit orbit, degenerated to ``v_3(c)`` where
the constant dominates. Both halves are classical valuation data —
Newton-polygon dominance and Hensel rigidity — in residual coordinates.

Nothing here counts roots or lifts faster than the classical algorithms;
the object of study is the state space, not the count.
"""

from __future__ import annotations

from functools import cache

from bt.calculus.lifting import depth_r_shape
from bt.calculus.residual import TRITS, pack_trits
from bt.calculus.section import IntPoly, rho_int
from bt.metrics import v3


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def _require_pos(n: int, name: str) -> int:
    n = _require_nat(n, name)
    if n == 0:
        raise ValueError(f"{name} must be >= 1")
    return n


# ------------------------------------------------------------ behaviour


def behaviour_class(state: IntPoly, r: int) -> tuple:
    """The depth-``r`` lifting behaviour of a residual state.

    The ordered, trit-labelled subtree of surviving branches. Equality of
    these values *is* the ``r``-step lifting equivalence, so the relation
    is reflexive, symmetric, and transitive by construction.
    """
    return depth_r_shape(state, _require_nat(r, "r"), mode="digits")


def behaviour_equivalent(left: IntPoly, right: IntPoly, r: int) -> bool:
    """Whether two states have the same depth-``r`` lifting behaviour."""
    return behaviour_class(left, r) == behaviour_class(right, r)


def is_dead(state: IntPoly) -> bool:
    """No surviving branch at all, so the behaviour is empty at every ``r``."""
    return all(state.rho(a) != 0 for a in TRITS)


def _shape_depth(shape: tuple) -> int:
    if not shape:
        return 0
    return 1 + max(_shape_depth(sub) for _a, sub in shape)


def behaviour_depth(state: IntPoly, r: int) -> int:
    """Deepest level with a surviving branch, capped at ``r``."""
    return _shape_depth(behaviour_class(state, _require_nat(r, "r")))


# ---------------------------------------------------------- unit scaling


def unit_scale(state: IntPoly, lam: int) -> IntPoly:
    """``λ·g`` for ``λ`` coprime to 3. Preserves the lifting behaviour."""
    if lam % 3 == 0:
        raise ValueError("scalar must be coprime to 3")
    return state.scale(lam)


def units_mod(r: int) -> tuple[int, ...]:
    """Representatives of the units modulo ``3^r``."""
    mod = 3 ** _require_pos(r, "r")
    return tuple(lam for lam in range(mod) if lam % 3)


def unit_normal_form(c: int, b: int, r: int) -> tuple[int, int]:
    """Least representative of the unit-scaling orbit of ``(c, b)`` mod ``3^r``.

    The orbit is ``{(λc, λb) : 3 ∤ λ}``. Members of one orbit always have
    the same behaviour, so this is a sound but not complete reduction.
    """
    mod = 3 ** _require_pos(r, "r")
    return min(((lam * c) % mod, (lam * b) % mod) for lam in units_mod(r))


def unit_orbit_count(r: int) -> int:
    """Number of unit-scaling orbits of linear states modulo ``3^r``.

    Equals ``2·3^r - 1``, which exceeds :func:`behaviour_count` from
    ``r = 2`` on: scaling is a proper intermediate quotient.
    """
    r = _require_pos(r, "r")
    return 2 * 3**r - 1


# ------------------------------------------------- linear state dynamics


def linear_state(c: int, b: int) -> IntPoly:
    """The linear residual ``c + bx``."""
    return IntPoly((c, b))


def linear_survives(c: int, b: int, a: int) -> bool:
    """Whether trit ``a`` keeps ``c + bx`` on the lifting tree."""
    if a not in TRITS:
        raise ValueError(f"input must be a trit, got {a}")
    return (c + a * b) % 3 == 0


def linear_step(c: int, b: int, a: int) -> tuple[int, int]:
    """``(c, b) ↦ ((c + ab)/3, b)`` on a surviving branch.

    This is ``𝔇_a`` restricted to linear states, and it shows that ``b``
    is invariant along the whole lifting tree in the deep regime.
    """
    if not linear_survives(c, b, a):
        raise ValueError(f"trit {a} does not survive at ({c}, {b})")
    return (c + a * b) // 3, b


def linear_children(c: int, b: int) -> tuple[tuple[int, tuple[int, int]], ...]:
    """Surviving trits of ``c + bx`` with the states they lead to."""
    return tuple((a, linear_step(c, b, a)) for a in TRITS if linear_survives(c, b, a))


# ----------------------------------------------------- Newton coordinate


def newton_quotient(c: int, b: int, r: int) -> int:
    """``u = c·b^{-1} mod 3^r``, the nonsingular deep-regime state.

    Requires ``3 ∤ b``. The depth-``r`` behaviour of ``c + bx`` depends
    only on ``u``, and all ``3^r`` values are behaviourally distinct.
    """
    r = _require_nat(r, "r")
    if b % 3 == 0:
        raise ValueError("newton quotient needs a derivative coprime to 3")
    mod = 3**r if r else 1
    return (c * pow(b, -1, mod)) % mod if r else 0


def drop_lsd(n: int) -> int:
    """``𝔇(n) = (n - ρ(n))/3``, the least-significant-trit drop."""
    return (n - rho_int(n)) // 3


def newton_path(c: int, b: int, r: int) -> tuple[int, ...]:
    """The unique length-``r`` lifting path of a nonsingular linear state.

    The trits are the balanced-ternary digits of ``-c/b``, LSD first,
    generated by ``u ↦ 𝔇(u)`` with emitted trit ``-ρ(u)``. Equivalently
    they are the digits of the Newton correction, which is why this half
    of the classification is a reparameterization of Hensel lifting.
    """
    r = _require_nat(r, "r")
    if b % 3 == 0:
        raise ValueError("newton path needs a derivative coprime to 3")
    u = newton_quotient(c, b, r) if r else 0
    out: list[int] = []
    for _ in range(r):
        a = -rho_int(u)
        out.append(a)
        u = drop_lsd(u + a)
    return tuple(out)


# ----------------------------------------------------------- state count


@cache
def deep_behaviours(r: int) -> tuple[tuple, ...]:
    """Every depth-``r`` behaviour realised by a linear state.

    The deep regime reduces to linear states modulo ``3^r``, so this is
    the complete behaviour set, not a sample.
    """
    r = _require_nat(r, "r")
    mod = 3**r if r else 1
    seen: set[tuple] = set()
    for c in range(mod):
        for b in range(mod):
            seen.add(behaviour_class(linear_state(c, b), r))
    return tuple(sorted(seen, key=repr))


def behaviour_count(r: int) -> int:
    """``L_r``: distinct depth-``r`` behaviours of deep-regime states."""
    return len(deep_behaviours(r))


def behaviour_count_formula(r: int) -> int:
    """``L_r = (3^{r+1} - 1)/2 + r = Σ_{j≤r} 3^j + r``."""
    r = _require_nat(r, "r")
    return (3 ** (r + 1) - 1) // 2 + r


def behaviours_by_derivative_valuation(r: int) -> dict[int, int]:
    """Distinct depth-``r`` behaviours grouped by ``e = min(v_3(b), r)``.

    The value at ``e`` is ``3^{r-e} + e``. Rows overlap, because the
    truncated fully-ternary behaviours occur at several valuations, so the
    row sum exceeds :func:`behaviour_count` by ``C(r, 2)``.
    """
    r = _require_nat(r, "r")
    mod = 3**r if r else 1
    rows: dict[int, set[tuple]] = {}
    for b in range(mod):
        val = v3(b)
        e = r if val is None else min(val, r)
        bucket = rows.setdefault(e, set())
        for c in range(mod):
            bucket.add(behaviour_class(linear_state(c, b), r))
    return {e: len(sub) for e, sub in sorted(rows.items())}


def truncated_tree(j: int, r: int) -> tuple:
    """Behaviour of the fully ternary tree of depth ``min(j, r)``.

    Realised by the state ``3^j + 0·x``, where every trit survives while
    the constant is still divisible by 3. These are the behaviours shared
    between valuation rows, and they are why the rows double-count.
    """
    j = _require_nat(j, "j")
    return behaviour_class(linear_state(3**j, 0), _require_nat(r, "r"))


def is_truncated_tree(shape: tuple) -> bool:
    """Whether a behaviour is fully ternary down to its depth."""
    if not shape:
        return True
    if len(shape) != 3:
        return False
    return all(is_truncated_tree(sub) for _a, sub in shape)


def valuation_row_formula(r: int, e: int) -> int:
    """``3^{r-e} + e``, the behaviour count at derivative valuation ``e``."""
    r = _require_nat(r, "r")
    e = _require_nat(e, "e")
    if e > r:
        raise ValueError("e must not exceed r")
    return 3 ** (r - e) + e


# ------------------------------------------------------- block shift law


def block_shift(word: tuple[int, ...]) -> int:
    """The constant shift a surviving word applies inside a ternary block.

    Scaled to ``b = 3^e``, the word ``w`` of length ``e`` carries the state
    ``(3^e d, 3^e)`` to ``(d + packWord(w), 3^e)``. The shift is the
    *balanced value* of the word, not its digit sum: at step ``j`` the
    constant is ``3^{e-j}(d + a_1 + 3a_2 + … + 3^{j-1}a_j)``.
    """
    for a in word:
        if a not in TRITS:
            raise ValueError(f"word must consist of trits, got {a}")
    return pack_trits(tuple(word))


def shift_window(e: int) -> tuple[int, ...]:
    """``W_e``, the balanced window of ``3^e`` consecutive integers.

    ``block_shift`` is a bijection from length-``e`` trit words onto this
    window, so ``W_e`` is a complete residue system modulo ``3^e`` and
    contains exactly one multiple of ``3^e``. That is what makes the
    shifted family separate residues.
    """
    e = _require_nat(e, "e")
    half = (3**e - 1) // 2
    return tuple(range(-half, half + 1))


def deep_leaf(t: int, e: int) -> bool:
    """Whether the leaf at shift ``t`` is the one that recurses.

    Exactly one ``t`` in ``shift_window(e)`` satisfies this for a given
    residue, since the window is a complete residue system.
    """
    return t % 3 ** _require_nat(e, "e") == 0


# ------------------------------------------------------- minimal state


def capped_valuation(n: int, r: int) -> int:
    """``min(v_3(n), r)``, with ``v_3(0) = ∞`` read as ``r``.

    Nothing below the horizon is observable, so the horizon is where every
    valuation saturates.
    """
    r = _require_nat(r, "r")
    val = v3(n % 3**r if r else 0)
    return r if val is None else min(val, r)


def derivative_valuation(b: int, r: int) -> int:
    """``e = min(v_3(b), r)``, the conserved quantity of a deep branch."""
    return capped_valuation(b, r)


def unit_normal_pair(c: int, b: int, r: int) -> tuple[int, int]:
    """Scale by a unit so that ``b ≡ 3^e``, returning ``(e, c)`` modulo ``3^r``.

    Unit scaling preserves the behaviour, so this is a canonical
    representative to reason about, and it turns each valuation row into a
    one-parameter family.
    """
    r = _require_pos(r, "r")
    mod = 3**r
    e = derivative_valuation(b, r)
    if e >= r:
        return r, c % mod
    beta = (b % mod) // 3**e
    return e, (c * pow(beta, -1, mod)) % mod


def is_dominated(c: int, b: int, r: int) -> bool:
    """Whether the constant dominates, ``v_3(c) < min(v_3(b), r)``.

    On this stratum the branch dies at depth ``v_3(c)`` whatever the
    derivative is, which is the Newton-polygon reason the state collapses.
    """
    r = _require_pos(r, "r")
    e, cn = unit_normal_pair(c, b, r)
    return capped_valuation(cn, r) < e


def minimal_state_key(c: int, b: int, r: int) -> tuple:
    """A complete invariant of the depth-``r`` lifting behaviour.

    Two deep-regime states have the same depth-``r`` behaviour exactly when
    these keys agree. On the dominated stratum the key is the valuation of
    the constant alone; otherwise it is the unit-scaling orbit, here
    represented by the normalised pair.
    """
    r = _require_pos(r, "r")
    e, cn = unit_normal_pair(c, b, r)
    m = capped_valuation(cn, r)
    if m < e:
        return ("dominated", m)
    return ("orbit", e, cn)


def dominated_count(r: int) -> int:
    """``r``: the truncated trees ``T_0, …, T_{r-1}``."""
    return _require_nat(r, "r")


def undominated_count(r: int) -> int:
    """``(3^{r+1}-1)/2 = Σ_{j≤r} 3^j``: one class per unit orbit."""
    r = _require_nat(r, "r")
    return (3 ** (r + 1) - 1) // 2


def row_overlap(r: int) -> int:
    """``C(r, 2)``: how much the valuation rows double-count."""
    r = _require_nat(r, "r")
    return r * (r - 1) // 2
