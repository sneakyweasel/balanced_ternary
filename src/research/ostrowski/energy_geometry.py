"""Unread-tail energy transition and length-independent live forms.

Canonical energy (order 3):

    E_i(s) = s1 q_{i-2} + s2 q_{i-1} + s3 q_i

with ``q_j = 0`` for ``j < 0``. The residual step was derived from

    E_{i-1}(T_w s) = E_i(s) - w q_{i-1}.

This module names that constructional identity and the adjoint
``u_{i-1} A = u_i``. It is **KNOWN**, not an ``L_0`` bound.

Normalized ``E_i / q_i`` on live states restates the slab ``K_n``.
A linear form whose max grows between start remaining 16 and 20 is a
counterexample, not an invariant. Finite depth is not ``|L_0|=∞``.
"""

from __future__ import annotations

from itertools import product
from math import hypot

from research.ostrowski.live_growth import unread_tail_bounds
from research.ostrowski.live_layers import (
    REVERSE_BOX_NOT_A_PROOF,
    energy_canonical,
    forward_layers,
    linf,
    method_a_b_agree,
)
from research.ostrowski.spectral import cubic_roots
from research.ostrowski.spectral_residual import residual_matrix, transition_affine
from research.ostrowski.system import OstrowskiSystem, characteristic_poly_coeffs, nonpisot_order3
from research_engine.algebra.linear_functionals import left_multiply

State3 = tuple[int, int, int]
Vec3 = tuple[int, int, int]


def adjoint_u(system: OstrowskiSystem, remaining: int) -> Vec3:
    """``u_i = (q_{i-2}, q_{i-1}, q_i)``."""
    return (
        system.place_value(remaining - 2),
        system.place_value(remaining - 1),
        system.place_value(remaining),
    )


def mat_vec_left(u: Vec3, matrix: tuple[tuple[int, int, int], ...]) -> Vec3:
    """Row vector ``u`` times ``A``."""
    out = left_multiply(u, matrix)
    return (out[0], out[1], out[2])


def adjoint_covariance(system: OstrowskiSystem, remaining: int) -> bool:
    """``u_{i-1} A = u_i`` for ``i = remaining ≥ 1``."""
    if remaining < 1:
        raise ValueError("adjoint covariance is for remaining >= 1")
    matrix = residual_matrix(system)
    return mat_vec_left(adjoint_u(system, remaining - 1), matrix) == adjoint_u(
        system, remaining
    )


def energy_after_step(
    system: OstrowskiSystem,
    state: State3,
    w: int,
    remaining: int,
) -> int:
    """``E_{i-1}(T_w s)``."""
    if remaining < 1:
        raise ValueError("step identity is for remaining >= 1")
    return energy_canonical(system, transition_affine(system, state, w), remaining - 1)


def energy_step_rhs(
    system: OstrowskiSystem,
    state: State3,
    w: int,
    remaining: int,
) -> int:
    """``E_i(s) - w q_{i-1}``."""
    if remaining < 1:
        raise ValueError("step identity is for remaining >= 1")
    return energy_canonical(system, state, remaining) - w * system.place_value(
        remaining - 1
    )


def energy_step_identity(
    system: OstrowskiSystem,
    state: State3,
    w: int,
    remaining: int,
) -> bool:
    """Constructional identity ``E_{i-1}(T_w s) = E_i(s) - w q_{i-1}``."""
    return energy_after_step(system, state, w, remaining) == energy_step_rhs(
        system, state, w, remaining
    )


def combination_coeff(
    system: OstrowskiSystem,
    a: int,
    b: int,
    c: int,
    remaining: int,
) -> Vec3:
    """Coefficient vector of ``a E_i + b E_{i-1} + c E_{i-2}`` in ``s``.

    Evaluated at a fixed state with three remaining labels. Independent
    of ``s``.
    """
    u_i = adjoint_u(system, remaining)
    u_im1 = adjoint_u(system, remaining - 1)
    u_im2 = adjoint_u(system, remaining - 2)
    return (
        a * u_i[0] + b * u_im1[0] + c * u_im2[0],
        a * u_i[1] + b * u_im1[1] + c * u_im2[1],
        a * u_i[2] + b * u_im1[2] + c * u_im2[2],
    )


def length_independent_combinations(
    coeff_range: range = range(-4, 5),
    remaining_a: int = 8,
    remaining_b: int = 14,
) -> dict[str, object]:
    """Integer ``(a,b,c)`` whose energy combination has ``i``-independent coeffs."""
    sys = nonpisot_order3()
    hits: list[dict[str, object]] = []
    for a, b, c in product(coeff_range, repeat=3):
        if a == 0 and b == 0 and c == 0:
            continue
        v8 = combination_coeff(sys, a, b, c, remaining_a)
        v14 = combination_coeff(sys, a, b, c, remaining_b)
        v20 = combination_coeff(sys, a, b, c, 20)
        if v8 == v14 == v20:
            hits.append({"a": a, "b": b, "c": c, "coeff": v8})
    return {
        "length_independent": hits,
        "count": len(hits),
        "known_construction_not_L0": True,
    }


def ell(coeff: Vec3, state: State3) -> int:
    return coeff[0] * state[0] + coeff[1] * state[1] + coeff[2] * state[2]


def layer_form_extrema(
    start_remaining: int,
    forms: tuple[Vec3, ...],
) -> dict[str, object]:
    """Max ``|ℓ|`` on each remaining slice. Slice, not ``L_{≤N}``."""
    sys = nonpisot_order3()
    fwd = forward_layers(sys, start_remaining, live_only=True)
    layers = fwd["layers"]
    rows = []
    live_all: set[State3] = set()
    global_max: dict[Vec3, int] = {f: 0 for f in forms}
    coord_max = [0, 0, 0]
    for n in range(start_remaining + 1):
        lset = set(layers[n].get("states_L", ()))
        live_all |= lset
        if not lset:
            continue
        for s in lset:
            for k in range(3):
                coord_max[k] = max(coord_max[k], abs(s[k]))
        form_max = {}
        for f in forms:
            m = max(abs(ell(f, s)) for s in lset)
            form_max[f] = m
            global_max[f] = max(global_max[f], m)
        qn = sys.place_value(n)
        e_over = None
        if qn:
            e_over = max(
                abs(energy_canonical(sys, s, n)) / qn for s in lset
            )
        lo, hi = unread_tail_bounds(sys, n)
        rows.append(
            {
                "n": n,
                "L": len(lset),
                "max_s1": max(abs(s[0]) for s in lset),
                "max_s2": max(abs(s[1]) for s in lset),
                "max_s3": max(abs(s[2]) for s in lset),
                "max_linf": max(linf(s) for s in lset),
                "form_max": form_max,
                "max_abs_E_over_qn": e_over,
                "lo_over_qn": lo / qn if qn else None,
                "hi_over_qn": hi / qn if qn else None,
            }
        )
    return {
        "start_remaining": start_remaining,
        "rows": rows,
        "live_union_count": len(live_all),
        "coord_max": tuple(coord_max),
        "form_max_union": global_max,
        "is_slice_not_union_census": True,
        "finite_depth_is_not_infinitude": True,
        "states": live_all,
    }


DEFAULT_FORMS: tuple[Vec3, ...] = (
    (0, 0, 1),
    (1, 0, 0),
    (0, 1, 0),
    (1, 0, -3),
    (0, 1, -1),
    (1, 3, 2),
    (1, 1, 1),
)


def compare_horizons(
    n_small: int = 16,
    n_large: int = 20,
    forms: tuple[Vec3, ...] = DEFAULT_FORMS,
) -> dict[str, object]:
    """A form that grows from ``n_small`` to ``n_large`` is a counterexample."""
    small = layer_form_extrema(n_small, forms)
    large = layer_form_extrema(n_large, forms)
    growth = []
    for f in forms:
        a = small["form_max_union"][f]
        b = large["form_max_union"][f]
        growth.append(
            {
                "coeff": f,
                "max_at_small": a,
                "max_at_large": b,
                "grows": b > a,
                "counterexample_not_invariant": b > a,
            }
        )
    return {
        "small": {
            "N": n_small,
            "coord_max": small["coord_max"],
            "live_union_count": small["live_union_count"],
            "form_max_union": {str(k): v for k, v in small["form_max_union"].items()},
        },
        "large": {
            "N": n_large,
            "coord_max": large["coord_max"],
            "live_union_count": large["live_union_count"],
            "form_max_union": {str(k): v for k, v in large["form_max_union"].items()},
        },
        "growth": growth,
        "any_stable": any(not g["grows"] for g in growth),
        "s3_grows": any(g["coeff"] == (0, 0, 1) and g["grows"] for g in growth),
        "finite_depth_is_not_infinitude": True,
        "unbounded_K_does_not_imply_unbounded_L0": True,
        "_small_states": small["states"],
        "_large_states": large["states"],
    }


def scan_integer_forms(
    live_small: set[State3],
    live_large: set[State3],
    coeff_range: range = range(-3, 4),
) -> dict[str, object]:
    """All small integer forms: grow vs stay. Observation only."""
    rows = []
    for a, b, c in product(coeff_range, repeat=3):
        if a == 0 and b == 0 and c == 0:
            continue
        coeff = (a, b, c)
        mx_s = max(abs(ell(coeff, s)) for s in live_small) if live_small else 0
        mx_l = max(abs(ell(coeff, s)) for s in live_large) if live_large else 0
        rows.append(
            {
                "coeff": coeff,
                "max_small": mx_s,
                "max_large": mx_l,
                "grows": mx_l > mx_s,
                "stable": mx_l == mx_s,
            }
        )
    stable = [r for r in rows if r["stable"]]
    growing = [r for r in rows if r["grows"]]
    stable.sort(key=lambda r: r["max_large"])
    growing.sort(key=lambda r: -(r["max_large"] - r["max_small"]))
    return {
        "stable_count": len(stable),
        "growing_count": len(growing),
        "stable_sample": stable[:12],
        "all_nonzero_grow_or_none_stable": len(stable) == 0,
        "observation_is_not_an_invariant": True,
    }


def normalized_cone(live_states: set[State3]) -> dict[str, object]:
    """Empirical projective cloud. Not a theorem."""
    dirs = []
    for s in live_states:
        n = hypot(float(s[0]), hypot(float(s[1]), float(s[2])))
        if n == 0.0:
            continue
        dirs.append((s[0] / n, s[1] / n, s[2] / n))
    if not dirs:
        return {"count": 0, "not_a_cone_theorem": True}
    mins = tuple(min(d[k] for d in dirs) for k in range(3))
    maxs = tuple(max(d[k] for d in dirs) for k in range(3))
    # Supporting trial: coordinate signs occupying both sides => not a half-space.
    both_sides = [mins[k] < -1e-9 and maxs[k] > 1e-9 for k in range(3)]
    return {
        "count": len(dirs),
        "dir_min": mins,
        "dir_max": maxs,
        "occupies_both_sides": both_sides,
        "span_s1": maxs[0] - mins[0],
        "span_s2": maxs[1] - mins[1],
        "span_s3": maxs[2] - mins[2],
        "numerical_cone_is_not_a_theorem": True,
        "not_a_cone_theorem": True,
    }


def spectral_normalized(live_by_remaining: dict[int, set[State3]]) -> dict[str, object]:
    """``|ℓ_j(s)| / |λ_j|^{N-n}`` observation. Floats only."""
    sys = nonpisot_order3()
    poly = characteristic_poly_coeffs(sys)
    assert poly is not None
    roots = cubic_roots(poly)
    ns = sorted(live_by_remaining)
    if not ns:
        return {"not_a_spectral_theorem": True, "forms": []}
    start = max(ns)
    reports = []
    for lam in roots:
        v = (1 + 0j, lam, lam * lam)
        ratios = []
        for n, states in live_by_remaining.items():
            steps = start - n
            scale = abs(lam) ** steps if steps >= 0 else 1.0
            for s in states:
                val = abs(v[0] * s[0] + v[1] * s[1] + v[2] * s[2])
                if scale > 0:
                    ratios.append(val / scale)
        reports.append(
            {
                "lambda": lam,
                "abs_lambda": abs(lam),
                "max_ratio": max(ratios) if ratios else 0.0,
                "min_ratio": min(ratios) if ratios else 0.0,
                "floats_are_classification_only": True,
            }
        )
    return {
        "forms": reports,
        "not_a_spectral_theorem": True,
        "floats_are_classification_only": True,
    }


def live_by_remaining(start_remaining: int) -> dict[int, set[State3]]:
    sys = nonpisot_order3()
    fwd = forward_layers(sys, start_remaining, live_only=True)
    return {
        n: set(row.get("states_L", ()))
        for n, row in fwd["layers"].items()
    }


def normalized_energy_on_live(start_remaining: int = 12) -> dict[str, object]:
    """Live states occupy ``[lo(i)/q_i, hi(i)/q_i]``. Restates ``K_n``."""
    sys = nonpisot_order3()
    fwd = forward_layers(sys, start_remaining, live_only=True)
    rows = []
    for n in range(start_remaining + 1):
        lset = set(fwd["layers"][n].get("states_L", ()))
        qn = sys.place_value(n)
        lo, hi = unread_tail_bounds(sys, n)
        inside = True
        extrema = []
        for s in lset:
            e = energy_canonical(sys, s, n)
            if not (lo <= e <= hi):
                inside = False
            if qn:
                extrema.append(e / qn)
        rows.append(
            {
                "n": n,
                "inside_slab": inside,
                "lo_over_qn": lo / qn if qn else None,
                "hi_over_qn": hi / qn if qn else None,
                "live_E_over_qn_min": min(extrema) if extrema else None,
                "live_E_over_qn_max": max(extrema) if extrema else None,
            }
        )
    return {
        "rows": rows,
        "all_inside_slab": all(r["inside_slab"] for r in rows),
        "restates_Kn_not_origin_invariant": True,
    }


def phase0_energy_geometry() -> dict[str, object]:
    """Deterministic Phase-0 bundle. Not a proof of ``|L_0|``."""
    sys = nonpisot_order3()
    identity_ok = True
    samples = [
        ((0, 0, 0), 0, 1),
        ((0, 0, 0), 1, 1),
        ((2, -3, 1), -4, 1),
        ((-3, -1, 0), 2, 2),
        ((6, 5, 0), -2, 3),
        ((1, -7, 4), 2, 8),
        ((-9, 3, 2), -3, 12),
    ]
    for state, w, i in samples:
        if not energy_step_identity(sys, state, w, i):
            identity_ok = False
        if not adjoint_covariance(sys, i):
            identity_ok = False
    combos = length_independent_combinations()
    compare = compare_horizons(16, 20)
    scan = scan_integer_forms(compare["_small_states"], compare["_large_states"])
    cone16 = normalized_cone(compare["_small_states"])
    cone20 = normalized_cone(compare["_large_states"])
    by_rem = live_by_remaining(12)
    spectral = spectral_normalized(by_rem)
    energy_norm = normalized_energy_on_live(12)
    ab = method_a_b_agree(6, 0, 6)
    # Drop heavy state sets from the public report.
    compare_pub = {k: v for k, v in compare.items() if not k.startswith("_")}
    return {
        "identity_holds": identity_ok,
        "identity_is_known_construction": True,
        "combinations": combos,
        "horizons": compare_pub,
        "integer_scan": {
            "stable_count": scan["stable_count"],
            "growing_count": scan["growing_count"],
            "stable_sample": scan["stable_sample"],
            "all_nonzero_grow_or_none_stable": scan["all_nonzero_grow_or_none_stable"],
            "observation_is_not_an_invariant": True,
        },
        "cone16": cone16,
        "cone20": cone20,
        "spectral": spectral,
        "normalized_energy": {
            "all_inside_slab": energy_norm["all_inside_slab"],
            "restates_Kn_not_origin_invariant": True,
        },
        "method_ab": {
            "agree": ab["agree"],
            REVERSE_BOX_NOT_A_PROOF: True,
        },
        "s3_grows": compare["s3_grows"],
        "outcome_d_no_live_invariant": True,
        "finite_depth_is_not_infinitude": True,
        "unbounded_K_does_not_imply_unbounded_L0": True,
        "not_a_spectral_theorem": True,
    }
