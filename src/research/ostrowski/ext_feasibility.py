"""Live extension windows from energy_step and the unread-tail slab.

One-step live Ext (remaining ``n≥1``):

    w ∈ Ext_live(s, n)  iff  w ∈ alphabet(n)
        and  lo(n-1) ≤ E_n(s) − w q_{n-1} ≤ hi(n-1)

This is KNOWN packaging of ``energy_step``, not an ``L_0`` bound.
Endpoints restate the slab ``K_n``. ``u = s2+2 s3`` is ``E_1`` and
governs remaining 1 only.

Co-live Ext is a subset of live Ext. A hole there does not kill the
live-interval law. A hole in the unread-tail value set ``V_n`` would.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import product
from math import ceil, floor

from research.ostrowski.control_language import (
    FROZEN_EXT_TYPES,
    dag_at,
    ext_is_consecutive_interval,
)
from research.ostrowski.energy_trajectory import apply_word, remaining_one_form
from research.ostrowski.exceptional_kernel import W_INTERIOR
from research.ostrowski.live_growth import legal_w
from research.ostrowski.live_layers import energy_canonical
from research.ostrowski.spectral_residual import transition_affine
from research.ostrowski.system import OstrowskiSystem, nonpisot_order3
from research.ostrowski.terminal_set import hi_closed_form, is_terminal, lo_closed_form

State3 = tuple[int, int, int]
ORIGIN: State3 = (0, 0, 0)

NORMALIZED_NOT_COORDINATE = "Kn_is_normalized_not_coordinate_bounded"
GROWTH_NOT_INFINITUDE = "finite_depth_is_not_infinitude"
LIVE_NOT_COLIVE_EXT = "live_ext_is_not_colive_ext"
U_IS_E1 = "u_is_E1_remaining_one_only"
KNOWN_PACKAGING = "live_ext_is_energy_step_plus_slab"


def _sys() -> OstrowskiSystem:
    return nonpisot_order3()


def alphabet_at_remaining(remaining: int) -> tuple[int, ...]:
    if remaining < 1:
        return ()
    return legal_w(_sys(), remaining - 1)


def valuation_set(n: int) -> set[int]:
    """``V_n``: attainable ``sum_{j<n} w_j q_j`` over legal difference words."""
    sys = _sys()
    reachable = {0}
    for j in range(n):
        qj = sys.place_value(j)
        alph = legal_w(sys, j)
        reachable = {total + w * qj for total in reachable for w in alph}
    return reachable


def valuation_is_interval(n: int) -> dict[str, object]:
    sys = _sys()
    values = valuation_set(n)
    if n == 0:
        lo = hi = 0
    else:
        lo = lo_closed_form(sys, n)
        hi = hi_closed_form(sys, n)
    filled = set(range(lo, hi + 1))
    holes = sorted(filled - values)
    extra = sorted(values - filled)
    return {
        "n": n,
        "lo": lo,
        "hi": hi,
        "count": len(values),
        "span": hi - lo + 1,
        "holes": holes[:12],
        "hole_count": len(holes),
        "extra_count": len(extra),
        "is_interval": values == filled,
    }


def valuations_fill_through(max_n: int = 12) -> dict[str, object]:
    rows = [valuation_is_interval(n) for n in range(0, max_n + 1)]
    return {
        "rows": rows,
        "all_intervals": all(r["is_interval"] for r in rows),
        "first_hole_n": next((r["n"] for r in rows if not r["is_interval"]), None),
    }


def live_ext_bounds(state: State3, remaining: int) -> tuple[int, int] | None:
    """Integer bounds ``(w_lo, w_hi)`` from the energy slab, or None if ``q=0``."""
    if remaining < 1:
        return None
    sys = _sys()
    energy = energy_canonical(sys, state, remaining)
    q = sys.place_value(remaining - 1)
    if q <= 0:
        return None
    if remaining == 1:
        lo, hi = 0, 0
    else:
        lo = lo_closed_form(sys, remaining - 1)
        hi = hi_closed_form(sys, remaining - 1)
    w_lo = ceil((energy - hi) / q)
    w_hi = floor((energy - lo) / q)
    return (w_lo, w_hi)


def live_ext(state: State3, remaining: int) -> tuple[int, ...]:
    """One-step live Ext: alphabet ∩ energy-slab interval."""
    bounds = live_ext_bounds(state, remaining)
    if bounds is None:
        return ()
    w_lo, w_hi = bounds
    alph = alphabet_at_remaining(remaining)
    return tuple(w for w in alph if w_lo <= w <= w_hi)


def live_ext_by_oracle(state: State3, remaining: int) -> tuple[int, ...]:
    sys = _sys()
    letters = []
    for w in alphabet_at_remaining(remaining):
        nxt = transition_affine(sys, state, w)
        if is_terminal(sys, nxt, remaining - 1):
            letters.append(w)
    return tuple(letters)


def real_width(remaining: int) -> dict[str, object]:
    """Width of the real ``w``-interval at remaining ``n≥1``."""
    sys = _sys()
    if remaining < 1:
        raise ValueError("remaining must be >= 1")
    q = sys.place_value(remaining - 1)
    if remaining == 1:
        lo, hi = 0, 0
        s_nm2 = 0
    else:
        lo = lo_closed_form(sys, remaining - 1)
        hi = hi_closed_form(sys, remaining - 1)
        s_nm2 = sum(sys.place_values(remaining - 1))
    width = (hi - lo) / q if q else 0.0
    predicted = (6 * s_nm2 - 3) / q if remaining >= 2 else 0.0
    return {
        "n": remaining,
        "q_nm1": q,
        "S": s_nm2,
        "lo": lo,
        "hi": hi,
        "width": width,
        "predicted_6S_minus_3": predicted,
        "width_lt_4": width < 4,
        "width_le_4": width <= 4,
        "max_integers_in_open_length": floor(width) + 1,
    }


def width_table(max_n: int = 24) -> dict[str, object]:
    rows = [real_width(n) for n in range(1, max_n + 1)]
    return {
        "rows": rows,
        "all_width_lt_4": all(r["width_lt_4"] for r in rows),
        "all_width_le_4": all(r["width_le_4"] for r in rows),
        "max_width": max(r["width"] for r in rows),
        "first_width_ge_4": next((r["n"] for r in rows if not r["width_lt_4"]), None),
        NORMALIZED_NOT_COORDINATE: True,
    }


def formula_matches_oracle(state: State3, remaining: int) -> bool:
    return live_ext(state, remaining) == live_ext_by_oracle(state, remaining)


@lru_cache(maxsize=None)
def _colive_from(state: State3, remaining: int) -> bool:
    sys = _sys()
    if remaining == 0:
        return is_terminal(sys, state, 0)
    if not is_terminal(sys, state, remaining):
        return False
    for w in alphabet_at_remaining(remaining):
        nxt = transition_affine(sys, state, w)
        if _colive_from(nxt, remaining - 1):
            return True
    return False


def colive_ext(state: State3, remaining: int) -> tuple[int, ...]:
    sys = _sys()
    letters = []
    for w in alphabet_at_remaining(remaining):
        nxt = transition_affine(sys, state, w)
        if _colive_from(nxt, remaining - 1):
            letters.append(w)
    return tuple(letters)


def boxed_colive_search(remaining: int = 4, box: int = 6) -> dict[str, object]:
    """Co-live Ext on a box in ``K_n``, not origin-reachable census."""
    sys = _sys()
    _colive_from.cache_clear()
    holes = []
    singleton_m3 = []
    live_not_colive = 0
    checked = 0
    max_live_len = 0
    for coords in product(range(-box, box + 1), repeat=3):
        state = (coords[0], coords[1], coords[2])
        if not is_terminal(sys, state, remaining):
            continue
        checked += 1
        live = live_ext(state, remaining)
        colive = colive_ext(state, remaining)
        max_live_len = max(max_live_len, len(live))
        if live != colive:
            live_not_colive += 1
        if not ext_is_consecutive_interval(colive):
            holes.append({"s": state, "live": live, "colive": colive})
        if live == (-3,):
            singleton_m3.append(state)
    return {
        "remaining": remaining,
        "box": box,
        "checked_in_K": checked,
        "colive_holes": holes[:8],
        "colive_hole_count": len(holes),
        "live_ext_singleton_m3": singleton_m3[:8],
        "live_ext_singleton_m3_count": len(singleton_m3),
        "live_ne_colive_count": live_not_colive,
        "max_live_ext_len": max_live_len,
        LIVE_NOT_COLIVE_EXT: live_not_colive > 0,
    }


def origin_window_geometry(start_remaining: int = 12) -> dict[str, object]:
    """Ext-window extrema on origin-reachable co-live nodes. Not a bound."""
    dag = dag_at(start_remaining)
    sys = _sys()
    by_ext: dict[tuple[int, ...], dict[str, object]] = {}
    missing_m3 = True
    formula_ok = True
    u_unbounded = False
    s3_unbounded = False
    live_ne_colive = 0
    for state, remaining in dag.colive:
        ext = dag.ext((state, remaining))
        if remaining >= 1:
            if not formula_matches_oracle(state, remaining):
                formula_ok = False
            if live_ext(state, remaining) != ext:
                live_ne_colive += 1
        if ext == (-3,):
            missing_m3 = False
        u = remaining_one_form(state)
        energy = energy_canonical(sys, state, remaining)
        row = by_ext.setdefault(
            ext,
            {
                "count": 0,
                "min_s": list(state),
                "max_s": list(state),
                "min_u": u,
                "max_u": u,
                "min_E": energy,
                "max_E": energy,
                "min_s3": state[2],
                "max_s3": state[2],
            },
        )
        row["count"] += 1
        for i in range(3):
            row["min_s"][i] = min(row["min_s"][i], state[i])
            row["max_s"][i] = max(row["max_s"][i], state[i])
        row["min_u"] = min(row["min_u"], u)
        row["max_u"] = max(row["max_u"], u)
        row["min_E"] = min(row["min_E"], energy)
        row["max_E"] = max(row["max_E"], energy)
        row["min_s3"] = min(row["min_s3"], state[2])
        row["max_s3"] = max(row["max_s3"], state[2])
    for ext, row in by_ext.items():
        if ext != () and max(abs(row["min_u"]), abs(row["max_u"])) > 2:
            u_unbounded = True
        if ext != () and max(abs(row["min_s3"]), abs(row["max_s3"])) > 2:
            s3_unbounded = True
        row["min_s"] = tuple(row["min_s"])
        row["max_s"] = tuple(row["max_s"])
        row["u_span"] = row["max_u"] - row["min_u"]
        row["s3_span"] = row["max_s3"] - row["min_s3"]
    observed = tuple(sorted(by_ext, key=lambda t: (len(t), t)))
    return {
        "N": start_remaining,
        "windows": by_ext,
        "observed_types": observed,
        "matches_frozen": observed == FROZEN_EXT_TYPES,
        "origin_has_singleton_m3": not missing_m3,
        "formula_matches_on_dag": formula_ok,
        "live_ne_colive_on_dag": live_ne_colive,
        "u_grows_on_some_window": u_unbounded,
        "s3_grows_on_some_window": s3_unbounded,
        U_IS_E1: True,
        NORMALIZED_NOT_COORDINATE: True,
        GROWTH_NOT_INFINITUDE: True,
        KNOWN_PACKAGING: True,
    }


def consecutive_windows_of_w(max_len: int = 4) -> tuple[tuple[int, ...], ...]:
    letters = W_INTERIOR
    out: list[tuple[int, ...]] = [()]
    for length in range(1, max_len + 1):
        for i in range(len(letters) - length + 1):
            out.append(letters[i : i + length])
    return tuple(out)


def frozen_window_description() -> dict[str, object]:
    all_le4 = consecutive_windows_of_w(4)
    without_m3 = tuple(w for w in all_le4 if w != (-3,))
    return {
        "all_consecutive_le4_including_empty": all_le4,
        "count_including_m3": len(all_le4),
        "without_singleton_m3": without_m3,
        "count_without_m3": len(without_m3),
        "matches_frozen": without_m3 == FROZEN_EXT_TYPES,
        "singleton_m3_in_frozen": (-3,) in FROZEN_EXT_TYPES,
    }


def phase0_ext_feasibility() -> dict[str, object]:
    vals = valuations_fill_through(12)
    widths = width_table(24)
    geom = origin_window_geometry(12)
    boxed = boxed_colive_search(4, 6)
    desc = frozen_window_description()
    samples = (
        (ORIGIN, 5),
        ((-3, -1, 0), 4),
        ((6, 5, 1), 3),
        ((-3, -37, 19), 1),
    )
    formula_ok = all(formula_matches_oracle(s, n) for s, n in samples)
    return {
        "valuations": {
            "all_intervals": vals["all_intervals"],
            "first_hole_n": vals["first_hole_n"],
            "n_checked": 12,
        },
        "widths": {
            "all_width_lt_4": widths["all_width_lt_4"],
            "max_width": widths["max_width"],
            "first_width_ge_4": widths["first_width_ge_4"],
            "n1": widths["rows"][0],
            "n2": widths["rows"][1],
            "n24": widths["rows"][-1],
        },
        "geometry": {k: v for k, v in geom.items() if k != "windows"},
        "boxed": boxed,
        "window_desc": desc,
        "formula_on_samples": formula_ok,
        KNOWN_PACKAGING: True,
        NORMALIZED_NOT_COORDINATE: True,
        GROWTH_NOT_INFINITUDE: True,
        U_IS_E1: True,
    }


HUB: State3 = (-3, -1, 0)
SAME_E1_AS_ORIGIN: State3 = (0, -2, 1)
LSD_ZERO: tuple[int, ...] = (0,)


def on_f(state: State3) -> bool:
    return state[2] == 0


def same_energy_same_onf(
    left: State3, right: State3, suffix: tuple[int, ...]
) -> bool:
    """Equal ``E_|v|`` implies the same landing on ``F``. Lean ``same_energy_same_OnF``."""
    sys = _sys()
    n = len(suffix)
    if energy_canonical(sys, left, n) != energy_canonical(sys, right, n):
        return False
    return on_f(apply_word(sys, left, suffix)) == on_f(
        apply_word(sys, right, suffix)
    )


def suffix_separates_onf(
    left: State3, right: State3, suffix: tuple[int, ...]
) -> bool:
    """A legal suffix lands exactly one of the two states on ``F``."""
    sys = _sys()
    return on_f(apply_word(sys, left, suffix)) != on_f(
        apply_word(sys, right, suffix)
    )


def energy_future_collapse(
    start_remaining: int = 8, remaining: int = 4
) -> dict[str, object]:
    """Co-live ``|states|`` vs ``|E_n|`` vs ``|Ext|``. Collapse, not a Hankel rank."""
    sys = _sys()
    dag = dag_at(start_remaining)
    states: set[State3] = set()
    energies: set[int] = set()
    exts: set[tuple[int, ...]] = set()
    for state, rem in dag.colive:
        if rem != remaining:
            continue
        states.add(state)
        energies.add(energy_canonical(sys, state, remaining))
        exts.add(dag.ext((state, remaining)))
    n_states = len(states)
    n_energy = len(energies)
    n_ext = len(exts)
    return {
        "start_remaining": start_remaining,
        "remaining": remaining,
        "n_states": n_states,
        "n_energy": n_energy,
        "n_ext": n_ext,
        "states_exceed_energy": n_states > n_energy,
        "states_exceed_ext": n_states > n_ext,
        GROWTH_NOT_INFINITUDE: True,
        KNOWN_PACKAGING: True,
    }


def phase0_same_energy_same_onf() -> dict[str, object]:
    """Suffix landing on ``F`` is classified by ``E_n``, not by ``s``. Not ``|L_0|``."""
    sys = _sys()
    n = len(LSD_ZERO)
    same_e = energy_canonical(sys, ORIGIN, n) == energy_canonical(
        sys, SAME_E1_AS_ORIGIN, n
    )
    diff_e = energy_canonical(sys, ORIGIN, n) != energy_canonical(sys, HUB, n)
    collapse = energy_future_collapse(8, 4)
    return {
        "same_energy": same_e,
        "same_energy_same_live_ext": live_ext(ORIGIN, n)
        == live_ext(SAME_E1_AS_ORIGIN, n),
        "same_energy_same_onf": same_energy_same_onf(
            ORIGIN, SAME_E1_AS_ORIGIN, LSD_ZERO
        ),
        "different_energy": diff_e,
        "zero_separates_origin_hub": suffix_separates_onf(ORIGIN, HUB, LSD_ZERO),
        "origin_on_f": on_f(apply_word(sys, ORIGIN, LSD_ZERO)),
        "hub_on_f": on_f(apply_word(sys, HUB, LSD_ZERO)),
        "collapse": collapse,
        GROWTH_NOT_INFINITUDE: True,
        KNOWN_PACKAGING: True,
    }
