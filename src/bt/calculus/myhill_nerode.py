"""Finite-horizon Myhill–Nerode equivalence for residual polynomial states.

Two states are equivalent at horizon ``k`` when they emit the same output
word on every balanced input of length ``k``. Equivalently, by prefix
locality, they produce the same length-``k`` integer jet of ``f(n_w)``
for every section word ``w``, independent of the residual argument after
``w``.

Horizon 0 is the unit relation. For ``r > 0``:

    f ≡_r g  iff  ∀ a ∈ {-1,0,+1},
        ρ_a(f) = ρ_a(g)  and  𝔇_a f ≡_{r-1} 𝔇_a g.

This file implements that characterization exactly. Sample LSD signatures
are a different, weaker predicate and must not be labelled ``M_k``.
"""

from __future__ import annotations

from itertools import product

from bt.calculus.residual import TRITS, delta, output_along, rho
from bt.calculus.section import IntPoly


def equiv_recursive(f: IntPoly, g: IntPoly, r: int) -> bool:
    """Exact ``≡_r`` by the recursive characterization."""
    if r < 0:
        raise ValueError("remaining horizon must be >= 0")
    if r == 0:
        return True
    for a in TRITS:
        if rho(f, a) != rho(g, a):
            return False
        if not equiv_recursive(delta(f, a), delta(g, a), r - 1):
            return False
    return True


def equiv_by_outputs(f: IntPoly, g: IntPoly, k: int) -> bool:
    """Exact ``≡_k`` by enumerating all input words of length ``k``."""
    if k < 0:
        raise ValueError("horizon must be >= 0")
    if k == 0:
        return True
    for word in product(TRITS, repeat=k):
        if output_along(f, word) != output_along(g, word):
            return False
    return True


def reachable_layers(f: IntPoly, max_len: int) -> dict[int, list[IntPoly]]:
    """Unique residuals ``f_w`` with ``|w| = length``, for ``0 ≤ length ≤ max_len``."""
    if max_len < 0:
        raise ValueError("max_len must be >= 0")
    layers: dict[int, list[IntPoly]] = {0: [f]}
    frontier = [f]
    for length in range(1, max_len + 1):
        seen: set[tuple[int, ...]] = set()
        nxt: list[IntPoly] = []
        for poly in frontier:
            for a in TRITS:
                child = delta(poly, a)
                if child.coeffs not in seen:
                    seen.add(child.coeffs)
                    nxt.append(child)
        layers[length] = nxt
        frontier = nxt
    return layers


def all_reachable(f: IntPoly, max_len: int) -> list[IntPoly]:
    """Unique residuals with ``|w| ≤ max_len``."""
    found: dict[tuple[int, ...], IntPoly] = {}
    for layer in reachable_layers(f, max_len).values():
        for poly in layer:
            found[poly.coeffs] = poly
    return list(found.values())


def raw_count(f: IntPoly, k: int, *, closed: bool = False) -> int:
    """``R_k(f)``: distinct residual polynomials.

    Default: ``|w| < k`` (emitting nodes of the depth-``k`` unfolding).
    If ``closed``, include ``|w| = k``.
    """
    if k < 0:
        raise ValueError("k must be >= 0")
    if k == 0:
        return 1
    max_len = k if closed else k - 1
    return len(all_reachable(f, max_len))


def semantic_count(f: IntPoly, k: int, *, closed: bool = False) -> int:
    """Extensionally distinct residuals as functions ``Z → Z``.

    Ordinary ``Z[x]`` polynomials that agree as functions are equal as
    polynomials, so this coincides with :func:`raw_count`.
    """
    return raw_count(f, k, closed=closed)


def _keys(polys: list[IntPoly], prev: dict[tuple[int, ...], int]) -> dict[tuple[int, ...], tuple]:
    out: dict[tuple[int, ...], tuple] = {}
    for poly in polys:
        out[poly.coeffs] = tuple((rho(poly, a), prev[delta(poly, a).coeffs]) for a in TRITS)
    return out


def _ids_from_keys(keys: dict[tuple[int, ...], tuple]) -> dict[tuple[int, ...], int]:
    table: dict[tuple, int] = {}
    mapping: dict[tuple[int, ...], int] = {}
    for coeffs, key in keys.items():
        if key not in table:
            table[key] = len(table)
        mapping[coeffs] = table[key]
    return mapping


def levelled_class_tables(f: IntPoly, k: int) -> tuple[list[dict[tuple[int, ...], int]], dict[int, list[IntPoly]]]:
    """``classes[r]`` maps residual coeffs at depth ``k-r`` to an ``≡_r`` id.

    ``classes[0]`` is the unit class on depth-``k`` residuals.
    """
    if k < 0:
        raise ValueError("k must be >= 0")
    layers = reachable_layers(f, k)
    classes: list[dict[tuple[int, ...], int]] = []
    zero: dict[tuple[int, ...], int] = {}
    for layer in layers.values():
        for poly in layer:
            zero[poly.coeffs] = 0
    classes.append(zero)
    for r in range(1, k + 1):
        depth = k - r
        prev = classes[r - 1]
        keys = _keys(layers[depth], prev)
        classes.append(_ids_from_keys(keys))
    return classes, layers


def levelled_mealy_count(f: IntPoly, k: int) -> int:
    """Remaining-depth unfolding size: sum over ``r=1..k`` of ``≡_r``-widths.

    This counts a clocked implementation, not ``M_k``. For ``f(x)=x`` it
    grows as ``k`` even though there is a single residual polynomial.
    """
    if k < 0:
        raise ValueError("k must be >= 0")
    if k == 0:
        return 0
    classes, _layers = levelled_class_tables(f, k)
    return sum(len(set(classes[r].values())) for r in range(1, k + 1))


def mealy_width(f: IntPoly, k: int) -> int:
    """Maximum number of ``≡_r``-classes at any remaining depth ``r ≥ 1``."""
    if k <= 0:
        return 0
    classes, _layers = levelled_class_tables(f, k)
    return max(len(set(classes[r].values())) for r in range(1, k + 1))


def _behavior_signature(poly: IntPoly, r: int, cache: dict) -> object:
    if r == 0:
        return 0
    key = (poly.coeffs, r)
    hit = cache.get(key)
    if hit is not None:
        return hit
    val = tuple((_rho_delta_sig(poly, a, r, cache) for a in TRITS))
    cache[key] = val
    return val


def _rho_delta_sig(poly: IntPoly, a: int, r: int, cache: dict) -> tuple:
    return (rho(poly, a), _behavior_signature(delta(poly, a), r - 1, cache))


def myhill_nerode_count(f: IntPoly, k: int) -> int:
    """``M_k(f)``: number of ``≡_k``-classes among residuals with ``|w| < k``.

    This is the exact finite-horizon Myhill–Nerode count, not a sample
    signature and not a remaining-depth clock.
    """
    if k < 0:
        raise ValueError("k must be >= 0")
    universe = all_reachable(f, max(k - 1, 0))
    cache: dict = {}
    return len({_behavior_signature(p, k, cache) for p in universe})


def uniform_mn_count(f: IntPoly, k: int) -> int:
    """Alias of :func:`myhill_nerode_count` (same-horizon quotient of ``R_k``)."""
    return myhill_nerode_count(f, k)


def distinguish(f: IntPoly, g: IntPoly, k: int) -> tuple[int, ...] | None:
    """A shortest trit word of length ``≤ k`` on which ``f`` and ``g`` differ."""
    if k < 0:
        raise ValueError("k must be >= 0")
    for length in range(1, k + 1):
        for word in product(TRITS, repeat=length):
            if output_along(f, word) != output_along(g, word):
                return word
    return None


def distinguish_pair(f: IntPoly, g: IntPoly, k: int) -> dict[str, object]:
    """Shortest distinguishing word of length ``≤ k``, plus the canonical cubic probe."""
    from bt.calculus.quadratic import canonical_distinguishing_word, coeff_triple, invariant_mod

    word = distinguish(f, g, k)
    canon = canonical_distinguishing_word(f, g, k)
    return {
        "f": f.render(),
        "g": g.render(),
        "f_coeffs": list(coeff_triple(f)),
        "g_coeffs": list(coeff_triple(g)),
        "invariant_f": list(invariant_mod(f, k)),
        "invariant_f": list(invariant_mod(f, k)),
        "invariant_g": list(invariant_mod(g, k)),
        "invariant_g": list(invariant_mod(g, k)),
        "equiv": word is None,
        "shortest": list(word) if word is not None else None,
        "canonical": list(canon) if canon is not None else None,
        "shortest_depth": len(word) if word is not None else None,
        "shortest_depth": len(word) if word is not None else None,
    }


def merge_examples(f: IntPoly, k: int, limit: int = 8) -> list[dict[str, object]]:
    """Distinct residual polynomials that are ``≡_k``-equivalent.

    These are finite-horizon merges. Distinct ordinary ``Z[x]`` polynomials
    cannot remain equivalent at every horizon.
    """
    from bt.calculus.quadratic import coeff_triple, residuals_with_words

    if k < 0:
        raise ValueError("k must be >= 0")
    if k == 0:
        return []
    found = residuals_with_words(f, max(k - 1, 0))
    cache: dict = {}
    groups: dict[object, list[tuple[IntPoly, tuple[int, ...]]]] = {}
    for poly, word in found.values():
        sig = _behavior_signature(poly, k, cache)
        groups.setdefault(sig, []).append((poly, word))
    rows: list[dict[str, object]] = []
    for members in groups.values():
        if len(members) < 2:
            continue
        base_poly, base_word = members[0]
        for poly, word in members[1:]:
            delayed = None
            if k + 1 <= 8:
                delayed = not equiv_recursive(base_poly, poly, k + 1)
            d = [base_poly.coefficient(i) - poly.coefficient(i)
                 for i in range(max(len(base_poly.coeffs), len(poly.coeffs)))]
            while len(d) > 1 and d[-1] == 0:
                d.pop()
            rows.append(
                {
                    "p": base_poly.render(),
                    "q": poly.render(),
                    "word_p": list(base_word),
                    "word_p": list(base_word),
                    "word_q": list(word),
                    "word_q": list(word),
                    "diff": d,
                    "diff_ABC": [
                        coeff_triple(base_poly)[0] - coeff_triple(poly)[0],
                        coeff_triple(base_poly)[1] - coeff_triple(poly)[1],
                        coeff_triple(base_poly)[2] - coeff_triple(poly)[2],
                    ],
                    "equiv_k": True,
                    "split_at_k_plus_1": delayed,
                    "split_at_k_plus_1": delayed,
                }
            )
            if len(rows) >= limit:
                return rows
    return rows


def witness_table(f: IntPoly, k: int, limit: int = 12) -> list[dict[str, object]]:
    """Pairwise distinguishing data for distinct residuals in ``U_k``."""
    from bt.calculus.quadratic import canonical_distinguishing_word, residuals_with_words

    found = list(residuals_with_words(f, max(k - 1, 0)).values())
    rows: list[dict[str, object]] = []
    for i, (p, wp) in enumerate(found):
        for q, wq in found[i + 1 :]:
            word = distinguish(p, q, k)
            canon = canonical_distinguishing_word(p, q, k)
            rows.append(
                {
                    "word_p": list(wp),
                    "word_q": list(wq),
                    "p": p.render(),
                    "q": q.render(),
                    "shortest": list(word) if word is not None else None,
                    "shortest_depth": len(word) if word is not None else None,
                    "canonical": list(canon) if canon is not None else None,
                }
            )
            if len(rows) >= limit:
                return rows
    return rows


def distinguishing_pairs(f: IntPoly, k: int, limit: int = 20) -> list[dict[str, object]]:
    """Explicit witnesses that distinct remaining-depth classes are separable."""
    if k <= 0:
        return []
    classes, layers = levelled_class_tables(f, k)
    pairs: list[dict[str, object]] = []
    for r in range(1, k + 1):
        depth = k - r
        reps: dict[int, IntPoly] = {}
        for poly in layers[depth]:
            reps.setdefault(classes[r][poly.coeffs], poly)
        items = list(reps.values())
        for i, p in enumerate(items):
            for q in items[i + 1 :]:
                word = distinguish(p, q, r)
                pairs.append(
                    {
                        "remaining": r,
                        "p": p.render(),
                        "q": q.render(),
                        "word": list(word) if word is not None else None,
                    }
                )
                if len(pairs) >= limit:
                    return pairs
    return pairs
