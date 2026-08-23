"""State complexity of the 3-adic lifting machine.

The quotient chain under study, from coarsest description to minimal
state, at horizon `r` in the deep regime `k >= r`:

    Phi_r = (c, b) mod 3^r        3^{2r} states
    unit-scaling orbits            2*3^r - 1
    lifting behaviour              (3^{r+1} - 1)/2 + r

Both surjections are strict from `r = 2` on, so `Phi_r` is sufficient but
not minimal and unit scaling is only part of the collapse. The exact
minimal count and its refinement by `e = v_3(f'(n))` are the results of
this module; the experiments here are the falsification tests behind them.

The last arrow is now closed. `shift_law` pins the leaf shift inside a
ternary block to the balanced value of the word, `shifted_family_injectivity`
shows the resulting shifted family separates residues, and `normal_form`
and `strata` exhibit the minimal state as the unit-scaling orbit
degenerated to `v_3(c)` wherever the constant dominates the derivative.

Nothing is claimed about root counting. Deterministic
`poly(deg f, k log 3)` counting is known (`dwivedi-mittal-saxena-2019`).
"""

from __future__ import annotations

from collections.abc import Iterable

from bt.calculus.lifting import lift_tree, node_at
from bt.calculus.lifting_state import (
    behaviour_class,
    behaviour_count,
    behaviour_count_formula,
    behaviour_depth,
    behaviours_by_derivative_valuation,
    block_shift,
    capped_valuation,
    deep_behaviours,
    dominated_count,
    is_dead,
    is_dominated,
    is_truncated_tree,
    linear_state,
    minimal_state_key,
    row_overlap,
    shift_window,
    truncated_tree,
    undominated_count,
    unit_orbit_count,
    unit_scale,
    valuation_row_formula,
)
from bt.calculus.residual import TRITS
from bt.calculus.poly_congruence import phi_equal, phi_k
from bt.calculus.section import IntPoly
from bt.metrics import v3
from research.lifting.families import all_polys

EXPENSIVE_R = 6
UNITS: tuple[int, ...] = (-8, -7, -5, -4, -2, -1, 2, 4, 5, 7, 8)


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def _polys(polys: Iterable[IntPoly] | None) -> tuple[IntPoly, ...]:
    return tuple(polys) if polys is not None else all_polys()


# ------------------------------------------------------- quotient chain


def quotient_chain(r: int, *, allow_expensive: bool = False) -> dict[str, object]:
    """The three descriptions of a deep-regime state, counted exactly."""
    r = _require_nat(r, "r")
    if r >= EXPENSIVE_R and not allow_expensive:
        raise ValueError(f"r >= {EXPENSIVE_R} needs allow_expensive=True")
    phi = 3 ** (2 * r)
    orbits = unit_orbit_count(r) if r else 1
    behaviours = behaviour_count(r)
    return {
        "r": r,
        "phi_states": phi,
        "unit_orbits": orbits,
        "behaviours": behaviours,
        "formula": behaviour_count_formula(r),
        "formula_holds": behaviours == behaviour_count_formula(r),
        "phi_is_minimal": behaviours == phi,
        "orbits_are_minimal": behaviours == orbits,
        "phi_collapse": phi // behaviours if behaviours else None,
    }


def valuation_rows(r: int, *, allow_expensive: bool = False) -> dict[str, object]:
    """Behaviour counts per derivative valuation, against `3^{r-e} + e`."""
    r = _require_nat(r, "r")
    if r >= EXPENSIVE_R and not allow_expensive:
        raise ValueError(f"r >= {EXPENSIVE_R} needs allow_expensive=True")
    rows = behaviours_by_derivative_valuation(r)
    predicted = {e: valuation_row_formula(r, e) for e in rows}
    total = behaviour_count(r)
    return {
        "r": r,
        "rows": rows,
        "predicted": predicted,
        "rows_hold": rows == predicted,
        "row_sum": sum(rows.values()),
        "behaviours": total,
        "overlap": sum(rows.values()) - total,
        "predicted_overlap": row_overlap(r),
        "overlap_holds": sum(rows.values()) - total == row_overlap(r),
    }


# -------------------------------------------------- structure of a row


def row_structure(r: int, e: int) -> dict[str, object]:
    """Check the structure theorem for one valuation row.

    Unit scaling reduces the row to `b = 3^e`. The claim is that the
    behaviour splits by `m = v_3(c)`:

    * `m < e`  — every trit shifts the constant by a multiple of 3, so
      branching is uniform and the behaviour is the fully ternary tree of
      depth `m`;
    * `m >= e` — the first `e` levels are fully ternary, because writing
      `c = 3^e d` the constant after `j <= e` steps is
      `3^{e-j}(d + a_1 + … + a_j)`.
    """
    r = _require_nat(r, "r")
    e = _require_nat(e, "e")
    if e > r:
        raise ValueError("e must not exceed r")
    mod = 3**r if r else 1
    b = 3**e % mod
    low_ok = True
    high_ok = True
    low_seen: set[tuple] = set()
    high_seen: set[tuple] = set()
    for c in range(mod):
        val = v3(c)
        m = r if val is None else min(val, r)
        shape = behaviour_class(linear_state(c, b), r)
        if m < e:
            low_seen.add(shape)
            if shape != truncated_tree(m, r):
                low_ok = False
        else:
            high_seen.add(shape)
            if behaviour_depth(linear_state(c, b), r) < min(e, r):
                high_ok = False
            if not _ternary_to(shape, min(e, r)):
                high_ok = False
    return {
        "r": r,
        "e": e,
        "low_is_truncated_tree": low_ok,
        "low_count": len(low_seen),
        "low_predicted": min(e, r + 1),
        "high_has_ternary_block": high_ok,
        "high_count": len(high_seen),
        "high_predicted": 3 ** (r - e),
        "total": len(low_seen | high_seen),
        "total_predicted": valuation_row_formula(r, e),
    }


def shift_law(e_max: int = 4, span: int = 6) -> dict[str, object]:
    """The exact leaf shift inside a ternary block.

    The candidate shifts are the digit sum and the balanced value of the
    word. Only the second is correct, and the distinction is decisive: the
    digit sum ranges over ``2e+1`` values while the balanced value ranges
    over all ``3^e``, and the separation argument needs a complete residue
    system modulo ``3^e``.
    """
    from itertools import product

    from bt.calculus.residual import residual_along

    digit_sum_failures = 0
    packed_failures = 0
    total = 0
    for e in range(1, _require_nat(e_max, "e_max") + 1):
        for d in range(-span, span + 1):
            state = linear_state(3**e * d, 3**e)
            for word in product(TRITS, repeat=e):
                total += 1
                got = residual_along(state, word).coeffs
                if got != linear_state(d + sum(word), 3**e).coeffs:
                    digit_sum_failures += 1
                if got != linear_state(d + block_shift(word), 3**e).coeffs:
                    packed_failures += 1
    windows = {
        e: tuple(sorted(block_shift(w) for w in product(TRITS, repeat=e)))
        == shift_window(e)
        for e in range(1, e_max + 1)
    }
    return {
        "cases": total,
        "digit_sum_failures": digit_sum_failures,
        "packed_failures": packed_failures,
        "packed_holds": packed_failures == 0,
        "digit_sum_refuted": digit_sum_failures > 0,
        "window_is_complete_residue_system": windows,
    }


def shifted_family_injectivity(e_max: int = 4, budget: int = 6) -> dict[str, object]:
    """The separation question, settled.

    For a fixed ``e``, is ``d mod 3^R`` recovered from the tuple of
    depth-``R`` behaviours of the shifted states ``d + t``, ``t`` in the
    window? Yes: the window contains exactly one ``t`` with ``3^e | d+t``,
    that leaf is the unique one of depth at least ``min(e, R)``, and it
    recurses at horizon ``R - e``.
    """
    rows: list[dict[str, object]] = []
    for e in range(1, _require_nat(e_max, "e_max") + 1):
        for horizon in range(0, max(budget - e, 1)):
            mod = 3**horizon
            window = shift_window(e)
            seen: dict[tuple, int] = {}
            collisions: list[tuple[int, int]] = []
            for d in range(mod):
                key = tuple(
                    behaviour_class(linear_state(d + t, 3**e), horizon) for t in window
                )
                if key in seen:
                    collisions.append((seen[key], d))
                else:
                    seen[key] = d
            rows.append(
                {
                    "e": e,
                    "R": horizon,
                    "states": mod,
                    "distinct": len(seen),
                    "injective": len(seen) == mod,
                    "collisions": collisions[:3],
                }
            )
    return {
        "rows": rows,
        "injective": all(row["injective"] for row in rows),
        "deepest_leaf_identified": _deep_leaf_identification(e_max, budget),
    }


def _deep_leaf_identification(e_max: int, budget: int) -> bool:
    """The recursing leaf is the unique window entry of depth >= min(e, R)."""
    for e in range(1, e_max + 1):
        for horizon in range(1, max(budget - e, 1)):
            for d in range(3**horizon):
                window = shift_window(e)
                deep = [t for t in window if (d + t) % 3**e == 0]
                if len(deep) != 1:
                    return False
                if horizon <= e:
                    continue
                tall = [
                    t
                    for t in window
                    if behaviour_depth(linear_state(d + t, 3**e), horizon) >= min(e, horizon)
                ]
                if tall != deep:
                    return False
    return True


def normal_form(r_max: int = 4) -> dict[str, object]:
    """The minimal state as a normal form, not merely a count.

    The key is a complete invariant: dominated states are labelled by
    ``v_3(c)`` alone, undominated ones by their unit-scaling orbit.
    """
    rows: list[dict[str, object]] = []
    for r in range(1, _require_nat(r_max, "r_max") + 1):
        mod = 3**r
        key_to_behaviour: dict[tuple, tuple] = {}
        behaviour_to_key: dict[tuple, tuple] = {}
        clashes = 0
        dominated_bad = 0
        for b in range(mod):
            for c in range(mod):
                key = minimal_state_key(c, b, r)
                shape = behaviour_class(linear_state(c, b), r)
                if key_to_behaviour.setdefault(key, shape) != shape:
                    clashes += 1
                behaviour_to_key.setdefault(shape, key)
                if key[0] == "dominated" and shape != truncated_tree(key[1], r):
                    dominated_bad += 1
        rows.append(
            {
                "r": r,
                "keys": len(key_to_behaviour),
                "behaviours": len(behaviour_to_key),
                "formula": behaviour_count_formula(r),
                "clashes": clashes,
                "bijective": (
                    clashes == 0
                    and len(key_to_behaviour) == len(behaviour_to_key)
                    == behaviour_count_formula(r)
                ),
                "dominated_not_a_tree": dominated_bad,
                "dominated": dominated_count(r),
                "undominated": undominated_count(r),
            }
        )
    return {"rows": rows, "bijective": all(row["bijective"] for row in rows)}


def strata(r_max: int = 4) -> dict[str, object]:
    """The two strata: valuation collapse against unit-orbit rigidity."""
    rows: list[dict[str, object]] = []
    for r in range(1, _require_nat(r_max, "r_max") + 1):
        mod = 3**r
        units = [u for u in range(mod) if u % 3]
        tree_bad = 0
        orbit_to_behaviour: dict[tuple[int, int], tuple] = {}
        behaviour_to_orbit: dict[tuple, tuple[int, int]] = {}
        orbit_clashes = 0
        for b in range(mod):
            for c in range(mod):
                shape = behaviour_class(linear_state(c, b), r)
                if is_dominated(c, b, r):
                    # v_3 is unit-scaling invariant, so c needs no normalising.
                    if shape != truncated_tree(capped_valuation(c, r), r):
                        tree_bad += 1
                    continue
                orbit = min(((c * u) % mod, (b * u) % mod) for u in units)
                if orbit_to_behaviour.setdefault(orbit, shape) != shape:
                    orbit_clashes += 1
                behaviour_to_orbit.setdefault(shape, orbit)
        rows.append(
            {
                "r": r,
                "dominated_not_a_tree": tree_bad,
                "undominated_orbits": len(orbit_to_behaviour),
                "undominated_behaviours": len(behaviour_to_orbit),
                "orbit_clashes": orbit_clashes,
                "orbit_is_minimal_here": (
                    orbit_clashes == 0
                    and len(orbit_to_behaviour) == len(behaviour_to_orbit)
                    == undominated_count(r)
                ),
            }
        )
    return {
        "rows": rows,
        "dominated_collapses_to_valuation": all(
            row["dominated_not_a_tree"] == 0 for row in rows
        ),
        "undominated_is_exactly_the_unit_orbit": all(
            row["orbit_is_minimal_here"] for row in rows
        ),
    }


def _ternary_to(shape: tuple, depth: int) -> bool:
    """Whether every level above `depth` branches three ways."""
    if depth <= 0:
        return True
    if len(shape) != 3:
        return False
    return all(_ternary_to(sub, depth - 1) for _a, sub in shape)


def truncated_tree_rows(r: int) -> dict[str, object]:
    """Which valuation rows contain the truncated tree `T_j`.

    `T_j` occurs exactly in the rows `e > j`, so it is counted `r - j`
    times and the total excess is `sum_{j<r} (r-j-1) = C(r,2)`. This is
    the whole of the row overlap, so the total follows from the rows.
    """
    r = _require_nat(r, "r")
    mod = 3**r if r else 1
    where: dict[int, list[int]] = {}
    for j in range(r + 1):
        target = truncated_tree(j, r)
        rows = []
        for e in range(r + 1):
            b = (3**e) % mod
            if any(
                behaviour_class(linear_state(c, b), r) == target for c in range(mod)
            ):
                rows.append(e)
        where[j] = rows
    excess = sum(len(rows) - 1 for rows in where.values())
    return {
        "r": r,
        "rows_containing": where,
        "predicted": {j: [r] if j == r else list(range(j + 1, r + 1)) for j in range(r + 1)},
        "excess": excess,
        "row_overlap": row_overlap(r),
    }


# -------------------------------------------------- minimality witnesses


def minimality_witness(bound: int = 13, r: int = 3) -> dict[str, object]:
    """Smallest live pair with different `Phi_r` and identical behaviour.

    Dead states are excluded. Two dead states always share the empty
    behaviour whatever their jets, so including them turns the search
    into noise; the smallest such pair is `1` against `-1`.
    """
    r = _require_nat(r, "r")
    best: tuple[tuple[int, int], tuple[int, int], tuple[int, int]] | None = None
    for c1 in range(-bound, bound + 1):
        for b1 in range(-bound, bound + 1):
            left = linear_state(c1, b1)
            if is_dead(left):
                continue
            for c2 in range(-bound, bound + 1):
                for b2 in range(-bound, bound + 1):
                    if (c1, b1) >= (c2, b2):
                        continue
                    right = linear_state(c2, b2)
                    if is_dead(right):
                        continue
                    if phi_equal(left, right, r):
                        continue
                    if behaviour_class(left, r) != behaviour_class(right, r):
                        continue
                    score = (abs(c1) + abs(b1) + abs(c2) + abs(b2), abs(c1) + abs(b1))
                    if best is None or score < best[0]:
                        best = (score, (c1, b1), (c2, b2))
    if best is None:
        return {"r": r, "bound": bound, "found": False}
    _score, left_cb, right_cb = best
    left, right = linear_state(*left_cb), linear_state(*right_cb)
    return {
        "r": r,
        "bound": bound,
        "found": True,
        "left": left.render(),
        "right": right.render(),
        "left_state": list(left_cb),
        "right_state": list(right_cb),
        "phi_left": list(phi_k(left, r)),
        "phi_right": list(phi_k(right, r)),
        "shared_behaviour": repr(behaviour_class(left, r)),
        "is_unit_multiple": _unit_ratio(left_cb, right_cb),
    }


def _unit_ratio(left: tuple[int, int], right: tuple[int, int]) -> int | None:
    for lam in UNITS + (1,):
        if (left[0] * lam, left[1] * lam) == right:
            return lam
    return None


def scaling_invariance(
    polys: Iterable[IntPoly] | None = None,
    k_max: int = 4,
    r_max: int = 3,
) -> dict[str, object]:
    """Unit scaling must never change the behaviour, but must move `Phi_r`."""
    failures: list[dict[str, object]] = []
    checked = 0
    phi_moved = 0
    for f in _polys(polys):
        for node in lift_tree(f, k_max):
            for lam in UNITS:
                scaled = unit_scale(node.residual, lam)
                for r in range(1, r_max + 1):
                    checked += 1
                    if behaviour_class(node.residual, r) != behaviour_class(scaled, r):
                        failures.append(
                            {
                                "poly": f.render(),
                                "digits": node.digits or "e",
                                "lam": lam,
                                "r": r,
                            }
                        )
                    if not phi_equal(node.residual, scaled, r):
                        phi_moved += 1
    return {
        "claim": "unit scaling preserves the lifting behaviour but not Phi_r",
        "checked": checked,
        "ok": not failures,
        "phi_moved": phi_moved,
        "failures": failures[:8],
    }


# ---------------------------------------------------------- attainment


def realising_poly(c: int, b: int, r: int, *, degree: int = 1) -> IntPoly:
    """A polynomial with a level-`r` lifting node whose deep state is `(c, b)`.

    `f(x) = 3^r c + b x` has `f(0) = 3^r c` and `f'(0) = b`, so the origin
    is a level-`r` node and the residual along `0^r` is exactly `c + bx`.
    The quadratic variant adds `3^r x^2`, whose contribution to the
    residual is `3^{2r} x^2` and therefore invisible modulo `3^r`; it
    exists only to show the attainment is not an artefact of degree 1.
    """
    r = _require_nat(r, "r")
    if degree not in (1, 2):
        raise ValueError("degree must be 1 or 2")
    terms = {0: 3**r * c, 1: b}
    if degree == 2:
        terms[2] = 3**r
    return IntPoly.from_dict(terms)


def attainment(r: int, *, degree: int = 1) -> dict[str, object]:
    """Every counted behaviour is realised by a genuine lifting node.

    This turns `L_r` from an upper bound on the number of deep-regime
    behaviours into the exact value.
    """
    r = _require_nat(r, "r")
    mod = 3**r if r else 1
    word = (0,) * r
    target = set(deep_behaviours(r))
    realised: set[tuple] = set()
    bad: list[dict[str, object]] = []
    for c in range(mod):
        for b in range(mod):
            f = realising_poly(c, b, r, degree=degree)
            node = node_at(f, word)
            if node.f_value % node.modulus:
                bad.append({"c": c, "b": b, "reason": "not a lifting node"})
                continue
            if node.scaled_value % mod != c % mod or node.f_prime % mod != b % mod:
                bad.append({"c": c, "b": b, "reason": "wrong deep state"})
                continue
            realised.add(behaviour_class(node.residual, r))
    return {
        "r": r,
        "degree": degree,
        "behaviours": len(target),
        "realised": len(realised),
        "attained": realised == target,
        "missing": len(target - realised),
        "failures": bad[:8],
    }


# ------------------------------------------------------- shallow regime


def shallow_census(
    polys: Iterable[IntPoly] | None = None,
    k_max: int = 5,
    r_max: int = 4,
) -> dict[str, object]:
    """Behaviours against `Phi_r` classes for nodes with `k < r`.

    Reported, not theorised. In the shallow regime the higher jet
    coefficients survive modulo `3^r`, the state space is unbounded in
    degree, and no closed form is claimed.
    """
    rows: list[dict[str, object]] = []
    pool = _polys(polys)
    for r in range(1, r_max + 1):
        shallow_phi: set[tuple] = set()
        shallow_beh: set[tuple] = set()
        deep_phi: set[tuple] = set()
        deep_beh: set[tuple] = set()
        for f in pool:
            for node in lift_tree(f, k_max):
                phi = phi_k(node.residual, r)
                phi = phi + (0,) * (12 - len(phi))
                shape = behaviour_class(node.residual, r)
                if node.level < r:
                    shallow_phi.add(phi)
                    shallow_beh.add(shape)
                else:
                    deep_phi.add(phi)
                    deep_beh.add(shape)
        rows.append(
            {
                "r": r,
                "shallow_phi": len(shallow_phi),
                "shallow_behaviours": len(shallow_beh),
                "deep_phi": len(deep_phi),
                "deep_behaviours": len(deep_beh),
                "deep_bound": behaviour_count_formula(r),
                "deep_within_bound": len(deep_beh) <= behaviour_count_formula(r),
            }
        )
    return {"k_max": k_max, "r_max": r_max, "polynomials": len(pool), "rows": rows}


def behaviour_shapes_seen(
    polys: Iterable[IntPoly] | None = None,
    k_max: int = 5,
    r: int = 3,
) -> dict[str, object]:
    """Census of behaviour kinds over real lifting nodes."""
    r = _require_nat(r, "r")
    kinds = {"dead": 0, "path": 0, "truncated_tree": 0, "mixed": 0}
    for f in _polys(polys):
        for node in lift_tree(f, k_max):
            shape = behaviour_class(node.residual, r)
            if not shape:
                kinds["dead"] += 1
            elif is_truncated_tree(shape):
                kinds["truncated_tree"] += 1
            elif all(len(layer) == 1 for layer in _spine(shape)):
                kinds["path"] += 1
            else:
                kinds["mixed"] += 1
    return {"r": r, "k_max": k_max, "kinds": kinds}


def _spine(shape: tuple) -> list[tuple]:
    out = []
    layer = shape
    while layer:
        out.append(layer)
        layer = tuple(item for _a, sub in layer for item in sub)
    return out


# ------------------------------------------------------------- report


def deep_state_report(r_max: int = 4, *, allow_expensive: bool = False) -> dict[str, object]:
    """Full payload for the minimal-state phase."""
    r_max = _require_nat(r_max, "r_max")
    if r_max >= EXPENSIVE_R and not allow_expensive:
        raise ValueError(f"r_max >= {EXPENSIVE_R} needs allow_expensive=True")
    chain = [quotient_chain(r, allow_expensive=allow_expensive) for r in range(1, r_max + 1)]
    rows = [valuation_rows(r, allow_expensive=allow_expensive) for r in range(1, r_max + 1)]
    shift = shift_law(e_max=min(r_max, 3))
    separation = shifted_family_injectivity(e_max=min(r_max, 3), budget=min(r_max + 2, 6))
    form = normal_form(r_max=min(r_max, 4))
    layers = strata(r_max=min(r_max, 4))
    verdict = {
        "phi_minimal": any(row["phi_is_minimal"] for row in chain),
        "orbits_minimal": all(row["orbits_are_minimal"] for row in chain),
        "closed_form": all(row["formula_holds"] for row in chain),
        "rows_closed_form": all(row["rows_hold"] for row in rows),
        "overlap_closed_form": all(row["overlap_holds"] for row in rows),
        "scaling_invariant": scaling_invariance(k_max=3, r_max=2)["ok"],
        "attained": all(attainment(r)["attained"] for r in range(1, min(r_max, 3) + 1)),
        "shift_is_the_balanced_value": shift["packed_holds"],
        "shift_is_not_the_digit_sum": shift["digit_sum_refuted"],
        "shifted_family_separates": separation["injective"],
        "normal_form_is_complete": form["bijective"],
        "dominated_collapses_to_valuation": layers["dominated_collapses_to_valuation"],
        "undominated_is_the_unit_orbit": layers["undominated_is_exactly_the_unit_orbit"],
    }
    return {
        "r_max": r_max,
        "chain": chain,
        "valuation_rows": rows,
        "structure": [row_structure(r_max, e) for e in range(r_max + 1)],
        "witness": minimality_witness(bound=6, r=3),
        "shallow": shallow_census(k_max=4, r_max=min(r_max, 3)),
        "shift_law": shift,
        "separation": separation,
        "normal_form": form,
        "strata": layers,
        "verdict": verdict,
    }
