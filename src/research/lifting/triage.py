"""Phase 0 triage of the 3-adic lifting-tree hypotheses.

Each function is a falsification test, not a demonstration. The
hypotheses under test are

H1  the lifting tree is the zero-output subtree of the residual machine;
H2  the residual state at a node is the scaled Taylor jet of ``f``;
H3  the classical one-step trichotomy follows from H1 and H2;
H4  the depth-``r`` subtree is determined by the finite-horizon class
    ``Phi_r`` of the residual, sharply, and in the deep regime
    ``k >= r`` by the two residues ``(f(n)/3^k, f'(n))`` modulo ``3^r``.

The negative half of H4 is reported under the ``unordered`` shape mode,
where sibling subtrees are sorted, so a separation there is the
strongest available. The positive half is reported under ``digits``,
where branch trits are retained, so determinacy there is the strongest
available.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Iterator

from bt.calculus.lifting import (
    LiftNode,
    brute_force_roots,
    depth_r_shape,
    divides_at_level,
    is_lift_node,
    lift_tree,
    node_at,
    taylor_coeff,
    tree_roots,
)
from bt.calculus.poly_congruence import function_equiv, pad_phi, phi_k
from bt.calculus.residual import TRITS
from bt.calculus.section import IntPoly
from bt.metrics import v3
from research.lifting.families import all_polys

Item = tuple[IntPoly, LiftNode]

_PHI_WIDTH = 12


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def _polys(polys: Iterable[IntPoly] | None) -> tuple[IntPoly, ...]:
    return tuple(polys) if polys is not None else all_polys()


def nodes_of(polys: Iterable[IntPoly] | None, k_max: int) -> Iterator[Item]:
    """Every lifting node of every polynomial up to level ``k_max``."""
    k_max = _require_nat(k_max, "k_max")
    for f in _polys(polys):
        for node in lift_tree(f, k_max):
            yield f, node


def _all_words(k: int) -> Iterator[tuple[int, ...]]:
    frontier: list[tuple[int, ...]] = [()]
    for _ in range(k + 1):
        yield from frontier
        frontier = [w + (a,) for w in frontier for a in TRITS]


def cap_v3(n: int, r: int) -> int:
    """``min(v_3(n), r)``, with ``v_3(0)`` treated as ``r``."""
    val = v3(n)
    return r if val is None else min(val, r)


# ---------------------------------------------------------------- H1

def h1_identification(
    polys: Iterable[IntPoly] | None = None,
    k_max: int = 7,
    word_depth: int = 5,
) -> dict[str, object]:
    """Zero output trits, divisibility, and brute force must all agree."""
    k_max = _require_nat(k_max, "k_max")
    word_depth = _require_nat(word_depth, "word_depth")
    failures: list[dict[str, object]] = []
    checked = 0
    for f in _polys(polys):
        for k in range(k_max + 1):
            checked += 1
            tree = tree_roots(f, k)
            brute = brute_force_roots(f, k)
            if tree != brute:
                failures.append(
                    {"poly": f.render(), "k": k, "tree": list(tree), "brute": list(brute)}
                )
        for word in _all_words(word_depth):
            checked += 1
            if is_lift_node(f, word) != divides_at_level(f, word):
                failures.append({"poly": f.render(), "word": list(word), "kind": "output-vs-divisibility"})
    return {
        "hypothesis": "H1",
        "claim": "3^k | f(n_w) iff every output trit along w vanishes",
        "checked": checked,
        "k_max": k_max,
        "word_depth": word_depth,
        "ok": not failures,
        "failures": failures[:8],
    }


# ---------------------------------------------------------------- H2

def h2_taylor_jet(
    polys: Iterable[IntPoly] | None = None,
    word_depth: int = 4,
) -> dict[str, object]:
    """Coefficient of ``x^j`` in ``D_w f`` must be ``3^{k(j-1)} f^{(j)}(n_w)/j!``."""
    word_depth = _require_nat(word_depth, "word_depth")
    failures: list[dict[str, object]] = []
    checked = 0
    for f in _polys(polys):
        degree = max(f.degree, 0)
        for word in _all_words(word_depth):
            node = node_at(f, word)
            k = node.level
            for j in range(1, degree + 1):
                checked += 1
                left = node.residual.coefficient(j)
                right = 3 ** (k * (j - 1)) * taylor_coeff(f, node.residue, j)
                if left != right:
                    failures.append(
                        {
                            "poly": f.render(),
                            "word": list(word),
                            "j": j,
                            "residual_coeff": left,
                            "scaled_taylor": right,
                        }
                    )
            if is_lift_node(f, word):
                checked += 1
                if node.residual.coefficient(0) * node.modulus != node.f_value:
                    failures.append(
                        {"poly": f.render(), "word": list(word), "j": 0, "kind": "constant term"}
                    )
    return {
        "hypothesis": "H2",
        "claim": "the residual state is the scaled Taylor jet; the linear coefficient is f'(n_w)",
        "checked": checked,
        "word_depth": word_depth,
        "ok": not failures,
        "failures": failures[:8],
        "classification": "REPARAMETERIZATION",
    }


# ---------------------------------------------------------------- H3

def predicted_children(node: LiftNode) -> int:
    """Classical one-step count, valid for ``level >= 1``."""
    if not node.singular:
        return 1
    deeper = node.v3_f is None or node.v3_f >= node.level + 1
    return 3 if deeper else 0


def h3_trichotomy(
    polys: Iterable[IntPoly] | None = None,
    k_max: int = 6,
) -> dict[str, object]:
    """Child count at level ``>= 1`` must be 1, 3, or 0 by the classical rule."""
    failures: list[dict[str, object]] = []
    counts = {0: 0, 1: 0, 3: 0}
    checked = 0
    root_counts: dict[int, int] = {}
    for f, node in nodes_of(polys, k_max):
        if node.level == 0:
            root_counts[len(node.children)] = root_counts.get(len(node.children), 0) + 1
            continue
        checked += 1
        actual = len(node.children)
        counts[actual] = counts.get(actual, 0) + 1
        if actual != predicted_children(node):
            failures.append(
                {
                    "poly": f.render(),
                    "level": node.level,
                    "residue": node.residue,
                    "actual": actual,
                    "predicted": predicted_children(node),
                }
            )
    return {
        "hypothesis": "H3",
        "claim": "for k >= 1 the child count is 1 if 3 does not divide f'(n), else 3 when v_3(f(n)) > k and 0 otherwise",
        "checked": checked,
        "child_count_census": dict(sorted(counts.items())),
        "level_zero_census": dict(sorted(root_counts.items())),
        "ok": not failures,
        "failures": failures[:8],
        "classification": "KNOWN",
    }


# ---------------------------------------------------------------- H4

@dataclass(frozen=True)
class Separation:
    """Two states sharing a key but differing in depth-``r`` subtree."""

    r: int
    mode: str
    key: str
    left: dict[str, object]
    right: dict[str, object]

    def as_dict(self) -> dict[str, object]:
        return {
            "r": self.r,
            "mode": self.mode,
            "key": self.key,
            "left": self.left,
            "right": self.right,
        }


def _node_record(f: IntPoly, node: LiftNode, r: int, mode: str) -> dict[str, object]:
    return {
        "poly": f.render(),
        "level": node.level,
        "residue": node.residue,
        "digits": node.digits or "e",
        "residual": node.residual.render(),
        "scaled_value": node.scaled_value,
        "f_prime": node.f_prime,
        "v3_scaled_value": node.v3_f if node.v3_f is None else node.v3_f - node.level,
        "v3_f_prime": node.v3_f_prime,
        "newton": list(node.newton),
        "shape": repr(depth_r_shape(node.residual, r, mode=mode)),
    }


def _rank(item: Item) -> tuple[int, int, int, int]:
    f, node = item
    return (node.level, max(f.degree, 0), max(abs(c) for c in f.coeffs), abs(node.residue))


def _scan(
    items: Iterable[Item],
    key_fn: Callable[[Item], object],
    r: int,
    mode: str,
) -> tuple[int, int, Separation | None]:
    groups: dict[object, dict[tuple, Item]] = {}
    for item in items:
        shape = depth_r_shape(item[1].residual, r, mode=mode)
        bucket = groups.setdefault(key_fn(item), {})
        prev = bucket.get(shape)
        if prev is None or _rank(item) < _rank(prev):
            bucket[shape] = item
    violations = [(key, bucket) for key, bucket in groups.items() if len(bucket) > 1]
    best: Separation | None = None
    best_rank: tuple[int, int, int, int] | None = None
    for key, bucket in violations:
        pair = sorted(bucket.values(), key=_rank)[:2]
        rank = _rank(pair[1])
        if best_rank is None or rank < best_rank:
            best_rank = rank
            best = Separation(
                r=r,
                mode=mode,
                key=repr(key),
                left=_node_record(pair[0][0], pair[0][1], r, mode),
                right=_node_record(pair[1][0], pair[1][1], r, mode),
            )
    return len(violations), len(groups), best


def _phi_key(r: int) -> Callable[[Item], object]:
    def key(item: Item) -> object:
        return pad_phi(phi_k(item[1].residual, r), _PHI_WIDTH)

    return key


def _valuation_key(r: int) -> Callable[[Item], object]:
    def key(item: Item) -> object:
        node = item[1]
        return (cap_v3(node.scaled_value, r), cap_v3(node.f_prime, r))

    return key


def _pair_key(r: int) -> Callable[[Item], object]:
    mod = 3**r

    def key(item: Item) -> object:
        node = item[1]
        return (node.scaled_value % mod, node.f_prime % mod)

    return key


def _regime(items: Iterable[Item], regime: str, r: int) -> Iterator[Item]:
    if regime not in {"all", "shallow", "deep", "positive"}:
        raise ValueError(f"unknown regime {regime!r}")
    for item in items:
        level = item[1].level
        if regime == "all":
            yield item
        elif regime == "positive" and level >= 1:
            yield item
        elif regime == "shallow" and level < r:
            yield item
        elif regime == "deep" and level >= r:
            yield item


def phi_determinacy(
    polys: Iterable[IntPoly] | None = None,
    k_max: int = 6,
    r: int = 3,
    *,
    mode: str = "digits",
) -> dict[str, object]:
    """``Phi_r`` of the residual must determine the depth-``r`` subtree."""
    r = _require_nat(r, "r")
    bad, total, sep = _scan(nodes_of(polys, k_max), _phi_key(r), r, mode)
    return {
        "hypothesis": "H4a",
        "claim": "equal Phi_r implies equal depth-r subtree",
        "r": r,
        "mode": mode,
        "classes": total,
        "violations": bad,
        "ok": bad == 0,
        "separation": None if sep is None else sep.as_dict(),
    }


def phi_sharpness(
    polys: Iterable[IntPoly] | None = None,
    k_max: int = 6,
    r: int = 3,
    *,
    mode: str = "digits",
) -> dict[str, object]:
    """``Phi_{r-1}`` must *not* determine the depth-``r`` subtree."""
    r = _require_nat(r, "r")
    if r == 0:
        raise ValueError("sharpness needs r >= 1")
    bad, total, sep = _scan(nodes_of(polys, k_max), _phi_key(r - 1), r, mode)
    return {
        "hypothesis": "H4b",
        "claim": "Phi_{r-1} does not determine the depth-r subtree, so Phi_r is minimal in the horizon",
        "r": r,
        "mode": mode,
        "classes": total,
        "violations": bad,
        "ok": bad > 0,
        "separation": None if sep is None else sep.as_dict(),
    }


def valuation_determinacy(
    polys: Iterable[IntPoly] | None = None,
    k_max: int = 6,
    r: int = 3,
    *,
    regime: str = "all",
    mode: str = "unordered",
) -> dict[str, object]:
    """Do the two capped valuations alone determine the depth-``r`` subtree?"""
    r = _require_nat(r, "r")
    bad, total, sep = _scan(_regime(nodes_of(polys, k_max), regime, r), _valuation_key(r), r, mode)
    return {
        "hypothesis": "H4c",
        "claim": "(v_3(f(n)/3^k), v_3(f'(n))) capped at r determines the depth-r subtree",
        "r": r,
        "regime": regime,
        "mode": mode,
        "classes": total,
        "violations": bad,
        "determined": bad == 0,
        "separation": None if sep is None else sep.as_dict(),
    }


def pair_determinacy(
    polys: Iterable[IntPoly] | None = None,
    k_max: int = 6,
    r: int = 3,
    *,
    regime: str = "deep",
    mode: str = "digits",
) -> dict[str, object]:
    """Do the two residues ``(f(n)/3^k, f'(n))`` modulo ``3^r`` determine the subtree?"""
    r = _require_nat(r, "r")
    bad, total, sep = _scan(_regime(nodes_of(polys, k_max), regime, r), _pair_key(r), r, mode)
    return {
        "hypothesis": "H4d",
        "claim": "in the deep regime the minimal state is the pair of residues modulo 3^r",
        "r": r,
        "regime": regime,
        "mode": mode,
        "classes": total,
        "violations": bad,
        "determined": bad == 0,
        "separation": None if sep is None else sep.as_dict(),
    }


def linearization(
    polys: Iterable[IntPoly] | None = None,
    k_max: int = 6,
    r: int = 3,
) -> dict[str, object]:
    """For ``k >= r`` the residual must be ``=_r`` its linear surrogate."""
    r = _require_nat(r, "r")
    failures: list[dict[str, object]] = []
    checked = 0
    for f, node in nodes_of(polys, k_max):
        if node.level < r:
            continue
        checked += 1
        if not function_equiv(node.residual, node.linear_surrogate(), r):
            failures.append(
                {
                    "poly": f.render(),
                    "level": node.level,
                    "residue": node.residue,
                    "residual": node.residual.render(),
                    "surrogate": node.linear_surrogate().render(),
                }
            )
    return {
        "hypothesis": "H4e",
        "claim": "for k >= r the residual is congruent mod 3^r to f(n)/3^k + f'(n) x",
        "r": r,
        "checked": checked,
        "ok": not failures,
        "failures": failures[:8],
    }


def linear_state_determinacy(
    r: int = 3,
    c_bound: int = 121,
    b_bound: int = 40,
    *,
    mode: str = "unordered",
) -> dict[str, object]:
    """Exhaustive valuation determinacy over linear states ``c + b x``.

    The deep regime reduces to these states by :func:`linearization`, so
    this is the decisive test there rather than a sample.
    """
    r = _require_nat(r, "r")
    groups: dict[tuple[int, int], dict[tuple, tuple[int, int]]] = {}
    for c in range(-c_bound, c_bound + 1):
        for b in range(-b_bound, b_bound + 1):
            state = IntPoly((c, b))
            shape = depth_r_shape(state, r, mode=mode)
            groups.setdefault((cap_v3(c, r), cap_v3(b, r)), {}).setdefault(shape, (c, b))
    witness = None
    for key, bucket in sorted(groups.items()):
        if len(bucket) > 1:
            pair = sorted(bucket.values(), key=lambda cb: (abs(cb[0]), abs(cb[1])))[:2]
            witness = {"key": list(key), "left": list(pair[0]), "right": list(pair[1])}
            break
    return {
        "hypothesis": "H4f",
        "claim": "valuations determine the depth-r shape of a linear state",
        "r": r,
        "mode": mode,
        "c_bound": c_bound,
        "b_bound": b_bound,
        "states": (2 * c_bound + 1) * (2 * b_bound + 1),
        "classes": len(groups),
        "violations": sum(1 for bucket in groups.values() if len(bucket) > 1),
        "determined": all(len(bucket) == 1 for bucket in groups.values()),
        "witness": witness,
    }


def unordered_shape_census(r: int = 4) -> dict[str, object]:
    """Complete deep-regime check of the valuation formula for ``U_r``.

    Every pair ``(c, b)`` modulo ``3^r`` is a deep-regime linear state.
    The test records whether ``U_r(c + b x)`` equals the closed form
    built from ``(min(v_3(c), r), min(v_3(b), r))`` alone, and whether
    each valuation class contains a single unlabeled shape.
    """
    from bt.calculus.lifting_state import (
        linear_unordered_shape,
        valuation_unordered_shape,
    )

    r = _require_nat(r, "r")
    mod = 3**r
    groups: dict[tuple[int, int], set[tuple]] = {}
    mismatches = 0
    for b in range(mod):
        for c in range(mod):
            key = (cap_v3(c, r), cap_v3(b, r))
            got = linear_unordered_shape(c, b, r)
            groups.setdefault(key, set()).add(got)
            if got != valuation_unordered_shape(c, b, r):
                mismatches += 1
    return {
        "r": r,
        "states": mod * mod,
        "valuation_classes": len(groups),
        "formula_mismatches": mismatches,
        "formula_holds": mismatches == 0,
        "determined": all(len(bucket) == 1 for bucket in groups.values()),
        "distinct_shapes": len({shape for bucket in groups.values() for shape in bucket}),
    }


# ---------------------------------------------------------- state counts

def state_census(
    polys: Iterable[IntPoly] | None = None,
    k_max: int = 6,
    r: int = 3,
) -> dict[str, object]:
    """Distinct ``Phi_r`` classes and distinct depth-``r`` subtrees per level.

    This is the compression statement: the number of subtree shapes at
    level ``k`` is bounded by the number of finite-horizon classes, which
    does not grow with ``k``, whereas the residue count grows like
    ``3^k``.
    """
    r = _require_nat(r, "r")
    per_level: dict[int, dict[str, set]] = {}
    for _f, node in nodes_of(polys, k_max):
        entry = per_level.setdefault(node.level, {"phi": set(), "shape": set(), "nodes": set()})
        entry["phi"].add(pad_phi(phi_k(node.residual, r), _PHI_WIDTH))
        entry["shape"].add(depth_r_shape(node.residual, r, mode="digits"))
        entry["nodes"].add((node.residue, node.residual.coeffs))
    rows = [
        {
            "level": level,
            "nodes": len(entry["nodes"]),
            "phi_classes": len(entry["phi"]),
            "distinct_subtrees": len(entry["shape"]),
            "residues_mod_3k": 3**level,
        }
        for level, entry in sorted(per_level.items())
    ]
    return {"r": r, "k_max": k_max, "rows": rows}


# --------------------------------------------------------------- report

def triage_report(k_max: int = 6, r_max: int = 3) -> dict[str, object]:
    """Full Phase 0 payload, including the go/stop verdict."""
    k_max = _require_nat(k_max, "k_max")
    r_max = _require_nat(r_max, "r_max")
    polys = all_polys()
    h1 = h1_identification(polys, k_max=min(k_max + 1, 7))
    h2 = h2_taylor_jet(polys, word_depth=4)
    h3 = h3_trichotomy(polys, k_max=k_max)
    determinacy = []
    for r in range(1, r_max + 1):
        determinacy.append(
            {
                "r": r,
                "phi": phi_determinacy(polys, k_max, r),
                "sharpness": phi_sharpness(polys, k_max, r),
                "valuation_all": valuation_determinacy(polys, k_max, r, regime="all"),
                "valuation_shallow": valuation_determinacy(polys, k_max, r, regime="shallow"),
                "valuation_deep": valuation_determinacy(polys, k_max, r, regime="deep"),
                "pair_deep": pair_determinacy(polys, k_max, r, regime="deep"),
                "linearization": linearization(polys, k_max, r),
                "linear_states": linear_state_determinacy(r),
            }
        )
    phi_ok = all(row["phi"]["ok"] for row in determinacy)
    sharp_ok = any(row["sharpness"]["ok"] for row in determinacy)
    lin_ok = all(row["linearization"]["ok"] for row in determinacy)
    deep_val = all(row["valuation_deep"]["determined"] for row in determinacy)
    shallow_fails = any(
        not row["valuation_shallow"]["determined"] for row in determinacy if row["r"] >= 2
    )
    verdict = {
        "h1": h1["ok"],
        "h2": h2["ok"],
        "h3": h3["ok"],
        "phi_determinacy": phi_ok,
        "phi_sharp": sharp_ok,
        "deep_linearization": lin_ok,
        "deep_valuation_determinacy": deep_val,
        "shallow_valuation_insufficient": shallow_fails,
    }
    proceed = bool(h1["ok"] and h2["ok"] and h3["ok"] and phi_ok and sharp_ok and lin_ok)
    return {
        "k_max": k_max,
        "r_max": r_max,
        "polynomials": len(polys),
        "h1": h1,
        "h2": h2,
        "h3": h3,
        "determinacy": determinacy,
        "state_census": state_census(polys, k_max, min(r_max, 3)),
        "verdict": verdict,
        "proceed": proceed,
    }
