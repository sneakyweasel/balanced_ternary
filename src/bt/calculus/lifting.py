"""Lifting trees of polynomial congruences ``f(x) ≡ 0 (mod 3^k)``.

A residue modulo ``3^k`` is a balanced-ternary word ``w = (a_0,…,a_{k-1})``
of length ``k`` with value ``n_w = Σ a_i 3^i``, which ranges bijectively
over ``[-(3^k-1)/2, (3^k-1)/2]``.

Iterating the section reconstruction ``f(a+3x) = ρ_a(f) + 3 𝔇_a f(x)`` gives

    f(n_w + 3^k x) = Σ_{i<k} ρ_i 3^i  +  3^k · (𝔇_w f)(x)

where ``ρ_i`` are the output trits of the residual Mealy machine along
``w``. Since ``|Σ_{i<k} ρ_i 3^i| ≤ (3^k-1)/2 < 3^k``, that sum vanishes
modulo ``3^k`` only when it is zero, hence

    3^k | f(n_w)   iff   every output trit along ``w`` is 0.

So the tree of solutions of ``f(x) ≡ 0 (mod 3^k)`` is exactly the
**zero-output subtree** of the residual machine, and the children of a
node are ``{a : ρ_a(𝔇_w f) = 0}``. Reading off the same identity for
``j ≥ 1`` shows the residual state is the scaled Taylor jet: the
coefficient of ``x^j`` in ``𝔇_w f`` is ``3^{k(j-1)} f^{(j)}(n_w)/j!``,
in particular the linear coefficient is exactly ``f'(n_w)`` and, on the
tree, the constant coefficient is ``f(n_w)/3^k``.

Nothing here is a Hensel implementation for its own sake; the module
exists so that lifting behaviour can be compared against the residual
``≡_k`` machinery of :mod:`bt.calculus.poly_congruence`.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from bt.calculus.poly_congruence import newton_coeffs
from bt.calculus.residual import TRITS, delta, output_along, pack_trits, residual_along
from bt.calculus.section import IntPoly
from bt.metrics import v3

_DIGIT_CHARS: dict[int, str] = {-1: "-", 0: "0", 1: "+"}

KINDS: tuple[str, ...] = ("terminal", "unique", "splitting", "singular-persistent")


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def _require_word(word: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    out = tuple(int(a) for a in word)
    for a in out:
        if a not in TRITS:
            raise ValueError(f"word entries must be trits, got {a}")
    return out


def derivative(f: IntPoly) -> IntPoly:
    """Ordinary formal derivative ``f'`` in ``Z[x]``."""
    if f.degree <= 0:
        return IntPoly((0,))
    return IntPoly(tuple(i * c for i, c in enumerate(f.coeffs))[1:])


def taylor_coeff(f: IntPoly, n: int, j: int) -> int:
    """Coefficient of ``x^j`` in ``f(n + x)``, that is ``f^{(j)}(n)/j!``."""
    j = _require_nat(j, "j")
    return f.compose(IntPoly((n, 1))).coefficient(j)


def word_value(word: tuple[int, ...] | list[int]) -> int:
    """``n_w = Σ a_i 3^i`` for an LSD-first trit word."""
    return pack_trits(_require_word(word))


def word_digits(word: tuple[int, ...] | list[int]) -> str:
    """Balanced digits of a word, most significant first. Empty for level 0."""
    return "".join(_DIGIT_CHARS[a] for a in reversed(_require_word(word)))


def is_lift_node(f: IntPoly, word: tuple[int, ...] | list[int]) -> bool:
    """Whether every output trit of the residual machine along ``word`` is 0."""
    return all(t == 0 for t in output_along(f, _require_word(word)))


def divides_at_level(f: IntPoly, word: tuple[int, ...] | list[int]) -> bool:
    """Whether ``3^{|w|}`` divides ``f(n_w)``, computed directly."""
    w = _require_word(word)
    return f.eval(pack_trits(w)) % (3 ** len(w)) == 0


def lift_kind(child_count: int, singular: bool) -> str:
    """Coarse label of a node.

    ``singular`` takes precedence over branching, because for ``k ≥ 1`` a
    singular node with any child always has three, so a plain
    ``splitting`` label would hide the singularity. ``splitting``
    therefore only occurs at level 0, where the one-step trichotomy does
    not yet apply.
    """
    if child_count == 0:
        return "terminal"
    if singular:
        return "singular-persistent"
    if child_count == 1:
        return "unique"
    return "splitting"


@dataclass(frozen=True)
class LiftNode:
    """One node of a lifting tree: a residue modulo ``3^k`` with its state."""

    word: tuple[int, ...]
    residue: int
    residual: IntPoly
    f_value: int
    f_prime: int
    v3_f: int | None
    v3_f_prime: int | None
    newton: tuple[int, ...]
    children: tuple[int, ...]
    kind: str

    @property
    def level(self) -> int:
        return len(self.word)

    @property
    def modulus(self) -> int:
        return 3 ** len(self.word)

    @property
    def parent_word(self) -> tuple[int, ...] | None:
        return None if not self.word else self.word[:-1]

    @property
    def digits(self) -> str:
        return word_digits(self.word)

    @property
    def singular(self) -> bool:
        """``3 | f'(n_w)``, with ``f'(n_w) = 0`` counted as singular."""
        return self.v3_f_prime is None or self.v3_f_prime >= 1

    @property
    def terminal(self) -> bool:
        return not self.children

    @property
    def scaled_value(self) -> int:
        """``f(n_w)/3^k``, the constant coefficient of the residual."""
        mod = self.modulus
        if self.f_value % mod:
            raise ValueError("node is not a lifting node")
        return self.f_value // mod

    def linear_surrogate(self) -> IntPoly:
        """``f(n_w)/3^k + f'(n_w) x``: the deep-regime state of the node."""
        return IntPoly((self.scaled_value, self.f_prime))

    def as_dict(self) -> dict[str, object]:
        return {
            "level": self.level,
            "word": list(self.word),
            "digits": self.digits or "e",
            "residue": self.residue,
            "modulus": self.modulus,
            "residual": self.residual.render(),
            "residual_coeffs": list(self.residual.coeffs),
            "f_value": self.f_value,
            "f_prime": self.f_prime,
            "v3_f": self.v3_f,
            "v3_f_prime": self.v3_f_prime,
            "newton": list(self.newton),
            "children": list(self.children),
            "child_count": len(self.children),
            "kind": self.kind,
            "singular": self.singular,
        }


def node_at(f: IntPoly, word: tuple[int, ...] | list[int]) -> LiftNode:
    """Build the node of ``f`` at ``word`` without checking liftability."""
    w = _require_word(word)
    residual = residual_along(f, w)
    n = pack_trits(w)
    f_value = f.eval(n)
    f_prime = derivative(f).eval(n)
    v3_prime = v3(f_prime)
    children = tuple(a for a in TRITS if residual.rho(a) == 0)
    singular = v3_prime is None or v3_prime >= 1
    return LiftNode(
        word=w,
        residue=n,
        residual=residual,
        f_value=f_value,
        f_prime=f_prime,
        v3_f=v3(f_value),
        v3_f_prime=v3_prime,
        newton=newton_coeffs(residual),
        children=children,
        kind=lift_kind(len(children), singular),
    )


def lift_children(f: IntPoly, node: LiftNode) -> tuple[LiftNode, ...]:
    """Nodes one level deeper that still satisfy the congruence."""
    return tuple(node_at(f, node.word + (a,)) for a in node.children)


def lift_tree(f: IntPoly, k_max: int) -> tuple[LiftNode, ...]:
    """Breadth-first lifting tree of ``f`` up to level ``k_max``.

    The result is a flat tuple in level order; edges are recovered from
    :attr:`LiftNode.parent_word`.
    """
    k_max = _require_nat(k_max, "k_max")
    root = node_at(f, ())
    nodes: list[LiftNode] = [root]
    frontier: list[LiftNode] = [root]
    for _ in range(k_max):
        nxt: list[LiftNode] = []
        for node in frontier:
            for child in lift_children(f, node):
                nodes.append(child)
                nxt.append(child)
        if not nxt:
            break
        frontier = nxt
    return tuple(nodes)


def level_nodes(nodes: tuple[LiftNode, ...], k: int) -> tuple[LiftNode, ...]:
    """Nodes of a tree at exactly level ``k``."""
    k = _require_nat(k, "k")
    return tuple(node for node in nodes if node.level == k)


def tree_roots(f: IntPoly, k: int) -> tuple[int, ...]:
    """Solutions of ``f(x) ≡ 0 (mod 3^k)`` found by the lifting tree."""
    k = _require_nat(k, "k")
    return tuple(sorted(node.residue for node in level_nodes(lift_tree(f, k), k)))


def brute_force_roots(f: IntPoly, k: int) -> tuple[int, ...]:
    """Solutions of ``f(x) ≡ 0 (mod 3^k)`` by exhaustive search. Verification only."""
    k = _require_nat(k, "k")
    mod = 3**k
    half = (mod - 1) // 2
    return tuple(x for x in range(-half, half + 1) if f.eval(x) % mod == 0)


def level_counts(f: IntPoly, k_max: int) -> tuple[int, ...]:
    """``N_k(f)`` for ``k = 0,…,k_max`` read off the lifting tree."""
    k_max = _require_nat(k_max, "k_max")
    nodes = lift_tree(f, k_max)
    return tuple(len(level_nodes(nodes, k)) for k in range(k_max + 1))


SHAPE_MODES: tuple[str, ...] = ("digits", "positional", "unordered")


@lru_cache(maxsize=None)
def _shape(coeffs: tuple[int, ...], r: int, mode: str) -> tuple:
    if r == 0:
        return ()
    g = IntPoly(coeffs)
    out: list[object] = []
    for a in TRITS:
        if g.rho(a) != 0:
            continue
        sub = _shape(delta(g, a).coeffs, r - 1, mode)
        out.append((a, sub) if mode == "digits" else sub)
    if mode == "unordered":
        return tuple(sorted(out))  # type: ignore[type-var]
    return tuple(out)


def depth_r_shape(residual: IntPoly, r: int, *, mode: str = "digits") -> tuple:
    """Depth-``r`` subtree below a state, as a nested tuple.

    ``digits`` records the branch trits, so the result determines the
    residues of every descendant. ``positional`` drops the trits but
    keeps each branch in its slot. ``unordered`` sorts sibling subtrees,
    so it retains only the bare tree shape; a separation witnessed under
    ``unordered`` is therefore the strongest kind.

    The unordered encoding is the canonical ``U_r``: ``()`` is a node
    with no surviving children (a leaf at this remaining depth), and a
    node with children is the sorted tuple of their unordered shapes.
    Multiplicity of identical children is the number of equal entries.
    """
    if mode not in SHAPE_MODES:
        raise ValueError(f"mode must be one of {SHAPE_MODES}, got {mode!r}")
    return _shape(residual.coeffs, _require_nat(r, "r"), mode)


def unordered_shape(residual: IntPoly, r: int) -> tuple:
    """The unlabeled depth-``r`` lifting shape ``U_r``.

    Recursively: forget the trit on each surviving edge, keep the
    multiset of child shapes. Equal to ``depth_r_shape(..., mode="unordered")``.
    """
    return depth_r_shape(residual, r, mode="unordered")


def shape_widths(residual: IntPoly, r: int) -> tuple[int, ...]:
    """Number of surviving descendants of a state at depths ``1,…,r``."""
    r = _require_nat(r, "r")
    widths: list[int] = []
    layer = [residual]
    for _ in range(r):
        nxt = [delta(g, a) for g in layer for a in TRITS if g.rho(a) == 0]
        widths.append(len(nxt))
        if not nxt:
            widths.extend([0] * (r - len(widths)))
            break
        layer = nxt
    return tuple(widths)


def lift_records(nodes: tuple[LiftNode, ...]) -> list[dict[str, object]]:
    """Serialisable records for the CLI and the explorer."""
    return [node.as_dict() for node in nodes]
