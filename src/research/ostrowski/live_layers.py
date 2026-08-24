"""Exact remaining-length layers ``R_n`` and ``L_n = R_n ∩ K_n``.

Canonical energy (order 3, ``residual_integer``):

    E_i(s) = s1 q_{i-2} + s2 q_{i-1} + s3 q_i

with ``q_j = 0`` for ``j < 0``. Do not shift the indices.

``R_n(N)`` is the remaining-``n`` slice of a legal-``w`` path from the
origin at start remaining ``N``. ``L_n(N) = R_n(N) ∩ K_n``. The union
census ``|L_{≤N}|`` in ``live_growth`` is not ``|L_n|``.

A live-only BFS (same filter as ``reachable_live``) visits only states
already in ``K_n``, so that slice equals ``L_n``. Legal-``w`` without
liveness is labeled separately.

Finite depth is not ``|L_0|=∞``. A reverse-box miss is not
unreachability. Unbounded ``K`` does not imply unbounded ``L_0``.
The kernel family ``t_n`` is one probe of ``K_n``, not the whole slab.
"""

from __future__ import annotations

from itertools import product
from math import hypot

from research.ostrowski.exceptional_kernel import GM_MODULI
from research.ostrowski.live_growth import legal_w, unread_tail_bounds
from research.ostrowski.nonpisot_search import HUB
from research.ostrowski.reverse_map import integer_preimage
from research.ostrowski.spectral import cubic_roots
from research.ostrowski.spectral_residual import residual_matrix, transition_affine
from research.ostrowski.spec import ostrowski_spec
from research.ostrowski.system import OstrowskiSystem, characteristic_poly_coeffs, nonpisot_order3
from research.ostrowski.terminal_set import is_terminal, kernel_family_state
from research_engine.core.phase import IntPhase
from research_engine.reachability.forward import forward_search

State3 = tuple[int, int, int]
StatePos = tuple[State3, int]
ORIGIN: State3 = (0, 0, 0)
# Finite reverse from a box is pattern discovery, not unreachability.
REVERSE_BOX_NOT_A_PROOF = "finite_reverse_box_is_not_unreachability"


def energy_canonical(system: OstrowskiSystem, state: State3, remaining: int) -> int:
    """``E_i = s1 q_{i-2} + s2 q_{i-1} + s3 q_i``. Identical to ``residual_integer``."""
    from research.ostrowski.residual import residual_integer

    return residual_integer(system, state, remaining)


def linf(state: State3) -> int:
    return max(abs(state[0]), abs(state[1]), abs(state[2]))


def _norm_dir(state: State3) -> tuple[float, float, float] | None:
    n = hypot(float(state[0]), hypot(float(state[1]), float(state[2])))
    if n == 0.0:
        return None
    return (state[0] / n, state[1] / n, state[2] / n)


def forward_layers(
    system: OstrowskiSystem,
    start_remaining: int,
    *,
    live_only: bool = True,
) -> dict[str, object]:
    """MSD BFS from the origin at remaining ``start_remaining``.

    ``live_only=True`` matches ``reachable_live`` (enqueue only ``K``).
    ``live_only=False`` is legal-``w`` reachability; ``L_n = R_n ∩ K_n``.
    """
    if start_remaining < 0:
        raise ValueError("start_remaining must be nonnegative")
    spec = ostrowski_spec(start_remaining, system)
    result = forward_search(spec, live_only=live_only)
    if not result.live_start:
        return {
            "start_remaining": start_remaining,
            "live_only": live_only,
            "live_start": False,
            "layers": {},
        }
    parent: dict[StatePos, tuple[StatePos, int]] = {}
    for (state, phase), ((pstate, pphase), w) in result.parents.items():
        parent[(state, int(phase))] = ((pstate, int(pphase)), w)
    by_rem: dict[int, set[State3]] = {}
    for n in range(start_remaining + 1):
        by_rem[n] = set(result.layer_at(IntPhase(n)))
    layers: dict[int, dict[str, object]] = {}
    for n in range(start_remaining + 1):
        rset = by_rem.get(n, set())
        if live_only:
            lset = set(rset)
        else:
            lset = {s for s in rset if is_terminal(system, s, n)}
        layers[n] = _layer_stats(system, n, rset, lset, parent, start_remaining)
    return {
        "start_remaining": start_remaining,
        "live_only": live_only,
        "live_start": True,
        "raw_pairs": len(result.configurations),
        "layers": layers,
        "union_is_not_Ln": True,
        "finite_depth_is_not_infinitude": True,
    }


def _prefix(parent: dict[StatePos, tuple[StatePos, int]], key: StatePos) -> tuple[int, ...]:
    word: list[int] = []
    cur = key
    while cur in parent:
        prev, w = parent[cur]
        word.append(w)
        cur = prev
    word.reverse()
    return tuple(word)


def _layer_stats(
    system: OstrowskiSystem,
    n: int,
    rset: set[State3],
    lset: set[State3],
    parent: dict[StatePos, tuple[StatePos, int]],
    start_remaining: int,
) -> dict[str, object]:
    if not rset:
        return {
            "n": n,
            "R": 0,
            "L": 0,
            "max_linf": None,
            "min_coords": None,
            "max_coords": None,
            "max_abs_E": None,
            "s_max": None,
            "prefix": None,
            "direction": None,
            "E_over_qn": None,
            "hub_in_L": False,
            "tn_in_L": False,
        }
    max_e = max(abs(energy_canonical(system, s, n)) for s in rset)
    min_c = (
        min(s[0] for s in rset),
        min(s[1] for s in rset),
        min(s[2] for s in rset),
    )
    max_c = (
        max(s[0] for s in rset),
        max(s[1] for s in rset),
        max(s[2] for s in rset),
    )
    s_max = None
    prefix = None
    direction = None
    e_over = None
    max_linf_l: int | None = None
    tn_in = False
    if lset:
        s_max = max(lset, key=lambda s: (linf(s), s[0], s[1], s[2]))
        max_linf_l = linf(s_max)
        prefix = _prefix(parent, (s_max, n))
        direction = _norm_dir(s_max)
        qn = system.place_value(n)
        if qn:
            e_over = energy_canonical(system, s_max, n) / qn
        tn = kernel_family_state(system, n) if n >= 1 else None
        tn_in = tn in lset if tn is not None else False
    return {
        "n": n,
        "R": len(rset),
        "L": len(lset),
        "max_linf": max_linf_l,
        "min_coords": min_c,
        "max_coords": max_c,
        "max_abs_E": max_e,
        "s_max": s_max,
        "prefix": prefix,
        "direction": direction,
        "E_over_qn": e_over,
        "hub_in_L": HUB in lset,
        "tn_in_L": tn_in,
        "states_L": frozenset(lset),
        "states_R": frozenset(rset),
    }


def layer_table(
    start_remaining: int,
    *,
    live_only: bool = True,
    system: OstrowskiSystem | None = None,
) -> list[dict[str, object]]:
    """Rows keyed by remaining ``n``, from a single start remaining."""
    sys = system if system is not None else nonpisot_order3()
    report = forward_layers(sys, start_remaining, live_only=live_only)
    layers = report["layers"]
    rows = []
    for n in range(start_remaining, -1, -1):
        row = dict(layers[n])
        row.pop("states_L", None)
        row.pop("states_R", None)
        row["start_remaining"] = start_remaining
        row["live_only"] = live_only
        rows.append(row)
    return rows


def union_layers(max_start: int, *, live_only: bool = True) -> dict[str, object]:
    """Union of remaining-``n`` slices over starts ``n..max_start``.

    Labeled as a union. Not ``|L_{≤N}|`` and not a proof of infinitude.
    """
    sys = nonpisot_order3()
    union_L: dict[int, set[State3]] = {n: set() for n in range(max_start + 1)}
    union_R: dict[int, set[State3]] = {n: set() for n in range(max_start + 1)}
    extrema: dict[int, State3 | None] = {n: None for n in range(max_start + 1)}
    for start in range(max_start + 1):
        report = forward_layers(sys, start, live_only=live_only)
        layers = report["layers"]
        for n, row in layers.items():
            union_R[n] |= set(row.get("states_R", ()))
            lset = set(row.get("states_L", ()))
            union_L[n] |= lset
            for s in lset:
                cur = extrema[n]
                if cur is None or (linf(s), s) > (linf(cur), cur):
                    extrema[n] = s
    rows = []
    for n in range(max_start + 1):
        s_max = extrema[n]
        rows.append(
            {
                "n": n,
                "R": len(union_R[n]),
                "L": len(union_L[n]),
                "max_linf": linf(s_max) if s_max is not None else None,
                "s_max": s_max,
                "direction": _norm_dir(s_max) if s_max is not None else None,
                "hub_in_L": HUB in union_L[n],
                "is_union_over_starts": True,
            }
        )
    return {
        "max_start": max_start,
        "rows": rows,
        "is_union_over_starts": True,
        "union_is_not_Ln_from_one_start": True,
        "finite_depth_is_not_infinitude": True,
    }


def q_ansatz_fit(
    states_by_n: dict[int, State3],
    system: OstrowskiSystem | None = None,
    coeff_range: range = range(-4, 5),
) -> dict[str, object]:
    """Try ``s_i(n) = α q_n + β q_{n-1} + γ q_{n-2} + c`` per coordinate."""
    sys = system if system is not None else nonpisot_order3()
    ns = sorted(n for n in states_by_n if n >= 2)
    if len(ns) < 4:
        return {"matched": False, "reason": "too_few_n"}
    coords: list[tuple[int, int, int, int] | None] = [None, None, None]
    for axis in range(3):
        found = None
        for a, b, c, const in product(coeff_range, repeat=4):
            ok = True
            for n in ns:
                pred = (
                    a * sys.place_value(n)
                    + b * sys.place_value(n - 1)
                    + c * sys.place_value(n - 2)
                    + const
                )
                if pred != states_by_n[n][axis]:
                    ok = False
                    break
            if ok:
                found = (a, b, c, const)
                break
        coords[axis] = found
    return {
        "matched": all(c is not None for c in coords),
        "coords": coords,
        "ns": ns,
        "kernel_family_is_not_the_only_probe": True,
    }


def recurrence_probe(seq: list[State3], lag: int = 1) -> dict[str, object]:
    """Check whether ``s_{i+lag} = M s_i + c`` for integer ``M`` on a window."""
    if len(seq) < lag + 4:
        return {"holds": False, "reason": "short"}
    # Use three consecutive pairs to try to solve M, c over Q, then test.
    # Affine: 12 unknowns (M 3x3 + c 3). Need 4 pairs; we only test identity
    # on first differences, not a full solver. Detect constant lag increment.
    diffs = [
        (
            seq[i + lag][0] - seq[i][0],
            seq[i + lag][1] - seq[i][1],
            seq[i + lag][2] - seq[i][2],
        )
        for i in range(len(seq) - lag)
    ]
    constant = all(d == diffs[0] for d in diffs)
    return {
        "lag": lag,
        "constant_increment": constant,
        "increment": diffs[0] if diffs else None,
        "holds": False,
        "not_a_proof": True,
    }


def bounded_functionals(
    live_states: set[State3],
    coeff_range: range = range(-3, 4),
) -> dict[str, object]:
    """Max ``|a s1 + b s2 + c s3|`` on observed live states. Observation only."""
    if not live_states:
        return {"forms": [], "max_linf": 0}
    max_box = max(linf(s) for s in live_states)
    forms = []
    for a, b, c in product(coeff_range, repeat=3):
        if a == 0 and b == 0 and c == 0:
            continue
        vals = [a * s[0] + b * s[1] + c * s[2] for s in live_states]
        bound = max(abs(v) for v in vals)
        forms.append(
            {
                "a": a,
                "b": b,
                "c": c,
                "bound": bound,
                "range": (min(vals), max(vals)),
                "strictly_tighter_than_linf": bound < max_box,
            }
        )
    forms.sort(key=lambda row: (row["bound"], abs(row["a"]) + abs(row["b"]) + abs(row["c"])))
    return {
        "max_linf": max_box,
        "tightest": forms[:8],
        "count": len(forms),
        "observation_is_not_an_invariant": True,
    }


def spectral_coordinates(live_states: set[State3]) -> dict[str, object]:
    """Left eigenfunctionals of ``A`` on observed live states. Floats only."""
    sys = nonpisot_order3()
    matrix = residual_matrix(sys)
    poly = characteristic_poly_coeffs(sys)
    assert poly is not None
    roots = cubic_roots(poly)
    # Left eigenvector for λ: v A = λ v, i.e. A^T v^T = λ v^T.
    # A = [[0,0,3],[1,0,1],[0,1,2]], A^T = [[0,1,0],[0,0,1],[3,1,2]].
    reports = []
    for lam in roots:
        # Solve (A^T - λ I) v = 0. From the companion shape:
        # v2 = λ v1, v3 = λ v2, and 3 v1 + v2 + 2 v3 = λ v3.
        v1 = 1 + 0j
        v2 = lam * v1
        v3 = lam * v2
        abs_vals = []
        for s in live_states:
            val = v1 * s[0] + v2 * s[1] + v3 * s[2]
            abs_vals.append(abs(val))
        reports.append(
            {
                "lambda": lam,
                "abs_lambda": abs(lam),
                "max_abs_ell": max(abs_vals) if abs_vals else 0.0,
                "min_abs_ell": min(abs_vals) if abs_vals else 0.0,
                "left_vec": (v1, v2, v3),
                "floats_are_classification_only": True,
            }
        )
    return {
        "matrix": matrix,
        "roots": roots,
        "forms": reports,
        "floats_are_classification_only": True,
        "not_a_spectral_theorem": True,
    }


def boxed_Kn(system: OstrowskiSystem, remaining: int, box: int) -> set[State3]:
    """Finite truncation of ``K_n``. Not ``|K_n|``."""
    out: set[State3] = set()
    lo, hi = unread_tail_bounds(system, remaining)
    for s1, s2, s3 in product(range(-box, box + 1), repeat=3):
        state = (s1, s2, s3)
        if remaining == 0:
            if s3 == 0:
                out.add(state)
            continue
        energy = energy_canonical(system, state, remaining)
        if lo <= energy <= hi:
            out.add(state)
    return out


def reverse_from_box(
    system: OstrowskiSystem,
    remaining: int,
    steps: int,
    box: int,
) -> dict[str, object]:
    """Legal reverse from ``K_n ∩ box``, ``steps`` times. Not unreachability."""
    layer = boxed_Kn(system, remaining, box)
    start_size = len(layer)
    hit_origin = ORIGIN in layer and steps == 0
    cur_rem = remaining
    for _ in range(steps):
        alphabet = legal_w(system, cur_rem)
        nxt: set[State3] = set()
        for t in layer:
            for w in alphabet:
                pred = integer_preimage(t, w)
                if pred is not None:
                    nxt.add(pred)
                    if pred == ORIGIN:
                        hit_origin = True
        layer = nxt
        cur_rem += 1
        if not layer:
            break
    return {
        "remaining": remaining,
        "steps": steps,
        "box": box,
        "boxed_Kn": start_size,
        "final_cardinality": len(layer),
        "origin_in_final": ORIGIN in layer,
        "hit_origin_anywhere": hit_origin,
        "final_remaining": cur_rem,
        REVERSE_BOX_NOT_A_PROOF: True,
        "states": frozenset(layer),
    }


def _reverse_hits_origin(
    system: OstrowskiSystem,
    seed: State3,
    remaining: int,
    steps: int,
) -> bool:
    """Independent reverse using ``integer_preimage`` only."""
    layer = {seed}
    rem = remaining
    for _ in range(steps):
        alphabet = legal_w(system, rem)
        nxt: set[State3] = set()
        for t in layer:
            if t[0] % 3 != 0:
                continue
            for w in alphabet:
                pred = integer_preimage(t, w)
                if pred is not None:
                    nxt.add(pred)
        layer = nxt
        rem += 1
        if not layer:
            return False
    return ORIGIN in layer


def method_a_b_agree(
    start_remaining: int,
    remaining: int,
    box: int,
) -> dict[str, object]:
    """Forward ``L_n ∩ box`` vs reverse-from-boxed-``K_n`` that hit the origin.

    Agreement is a finite check, not a proof. Reverse miss outside the
    box is possible. Method A uses ``transition_affine``; Method B uses
    ``integer_preimage``.
    """
    sys = nonpisot_order3()
    if remaining > start_remaining:
        raise ValueError("remaining cannot exceed start")
    steps = start_remaining - remaining
    fwd = forward_layers(sys, start_remaining, live_only=False)
    layer = fwd["layers"][remaining]
    l_box = {s for s in layer["states_L"] if linf(s) <= box}
    r_box = {s for s in layer["states_R"] if linf(s) <= box}
    kn = boxed_Kn(sys, remaining, box)
    rev_hits = {
        seed for seed in kn if _reverse_hits_origin(sys, seed, remaining, steps)
    }
    agree = l_box == rev_hits
    return {
        "start_remaining": start_remaining,
        "remaining": remaining,
        "box": box,
        "forward_L_in_box": len(l_box),
        "forward_R_in_box": len(r_box),
        "reverse_origin_hits": len(rev_hits),
        "agree": agree,
        "only_in_forward": sorted(l_box - rev_hits),
        "only_in_reverse": sorted(rev_hits - l_box),
        REVERSE_BOX_NOT_A_PROOF: True,
        "finite_check_is_not_a_proof": True,
    }


def extrema_report(start_remaining: int = 16) -> dict[str, object]:
    """Largest-norm live states per remaining, plus ansatz/functional probes."""
    sys = nonpisot_order3()
    fwd = forward_layers(sys, start_remaining, live_only=True)
    layers = fwd["layers"]
    s_max_by_n: dict[int, State3] = {}
    live_all: set[State3] = set()
    rows = []
    for n in range(start_remaining + 1):
        row = layers[n]
        live_all |= set(row.get("states_L", ()))
        if row["s_max"] is not None:
            s_max_by_n[n] = row["s_max"]
        rows.append(
            {
                "n": n,
                "R": row["R"],
                "L": row["L"],
                "max_linf": row["max_linf"],
                "s_max": row["s_max"],
                "prefix": row["prefix"],
                "direction": row["direction"],
                "E_over_qn": row["E_over_qn"],
                "min_coords": row["min_coords"],
                "max_coords": row["max_coords"],
                "max_abs_E": row["max_abs_E"],
                "hub_in_L": row["hub_in_L"],
                "tn_in_L": row["tn_in_L"],
            }
        )
    seq = [s_max_by_n[n] for n in sorted(s_max_by_n) if n <= start_remaining - 2]
    return {
        "start_remaining": start_remaining,
        "rows": rows,
        "q_ansatz": q_ansatz_fit(s_max_by_n, sys),
        "recurrence_lag1": recurrence_probe(seq, 1),
        "recurrence_lag2": recurrence_probe(seq, 2),
        "functionals": bounded_functionals(live_all),
        "spectral": spectral_coordinates(live_all),
        "live_union_count": len(live_all),
        "finite_depth_is_not_infinitude": True,
        "unbounded_K_does_not_imply_unbounded_L0": True,
        "kernel_family_is_not_the_only_probe": True,
    }


def phase0_live_geometry(
    start_remaining: int = 16,
    gm_moduli: tuple[int, ...] = GM_MODULI,
) -> dict[str, object]:
    """Deterministic Phase-0 bundle. Not a proof of ``|L_0|``."""
    from research.ostrowski.exceptional_kernel import (
        affine_augmented_search,
        length_window_extended,
        time_augmented_search,
    )

    gm = time_augmented_search(gm_moduli)
    affine = affine_augmented_search()
    window = length_window_extended()
    extrema = extrema_report(start_remaining)
    checks = [
        method_a_b_agree(6, n, 6) for n in range(0, 7)
    ]
    agree = all(c["agree"] for c in checks)
    any_sep = bool(gm["any_separates"] or affine["count"])
    family = extrema["q_ansatz"]["matched"]
    return {
        "time_augmented": gm,
        "affine_augmented": affine,
        "length_window": window,
        "extrema": extrema,
        "method_ab": checks,
        "method_ab_agree": agree,
        "closed_time_augmented_obstruction": any_sep,
        "symbolic_family": family,
        "outcome_e_no_theorem": not any_sep and not family,
        "unbounded_K_does_not_imply_unbounded_L0": True,
        "finite_depth_is_not_infinitude": True,
        "finite_quotient_is_not_unreachability": True,
        REVERSE_BOX_NOT_A_PROOF: True,
    }
