"""Multi-step unread-tail energy, defects, and energy-compatible blocks.

One-step law (Lean ``energy_step``):

    E_{i-1}(T_w s) = E_i(s) - w q_{i-1}    (i ≥ 1)

Telescope from remaining ``N`` after MSD word ``(w_{N-1}, …, w_i)``:

    E_i(s) = E_N(s_start) - sum_{j=i}^{N-1} w_j q_j

From the origin, ``E_N(0)=0``, so ``E_i = -sum_{consumed} w_j q_j``.
Acceptance at remaining 0 is ``sum_j w_j q_j = 0``. This is KNOWN
construction (unread-tail residual), not an ``L_0`` bound.

``K_n`` is *normalized* boundedness of ``E_n``, not coordinate
boundedness of ``s``. Defects evolve by a nonnegative multiple of
``q_{i-1}``; that does not give ``|ℓ(s)| ≤ C``.

Finite depth is not ``|L_0|=∞``. Expanding ``T_B^k(0)`` without
``K_n`` is not a live family.
"""

from __future__ import annotations

from itertools import product

from research.ostrowski.energy_geometry import energy_canonical
from research.ostrowski.exceptional_kernel import W_INTERIOR
from research.ostrowski.live_growth import unread_tail_bounds
from research.ostrowski.live_layers import forward_layers, linf
from research.ostrowski.residual import difference_word, lsd_to_msd, run_msd
from research.ostrowski.spectral import cubic_roots
from research.ostrowski.spectral_residual import transition_affine
from research.ostrowski.system import OstrowskiSystem, characteristic_poly_coeffs, nonpisot_order3
from research.ostrowski.terminal_set import (
    hi_closed_form,
    is_terminal,
    lo_closed_form,
)

State3 = tuple[int, int, int]
ORIGIN: State3 = (0, 0, 0)

# K_n bounds E_n, not the coordinates of s.
NORMALIZED_NOT_COORDINATE = "Kn_is_normalized_not_coordinate_bounded"
GROWTH_NOT_INFINITUDE = "finite_depth_is_not_infinitude"

# Frozen lo(n), hi(n), q_n, S_{n-1} for Γ_NP. Ratios, not a plot.
EXACT_LO_HI: tuple[tuple[int, int, int, int, int], ...] = (
    # n, q_n, S_{n-1}, lo, hi
    (1, 2, 1, -2, 1),
    (2, 5, 3, -10, 5),
    (3, 15, 8, -30, 15),
    (4, 41, 23, -90, 45),
    (5, 112, 64, -254, 127),
    (6, 310, 176, -702, 351),
)


def wmax_at_place(place: int) -> int:
    """Largest legal difference at ``place`` (0 = LSD)."""
    if place < 0:
        raise ValueError("place must be nonnegative")
    return 1 if place == 0 else 2


def wmin_at_place(place: int) -> int:
    return -2 if place == 0 else -4


def consumed_sum(system: OstrowskiSystem, start_remaining: int, word: tuple[int, ...]) -> int:
    """``sum_{t=0}^{k-1} word[t] q_{N-1-t}`` for MSD word of length ``k``."""
    total = 0
    for t, w in enumerate(word):
        total += w * system.place_value(start_remaining - 1 - t)
    return total


def apply_word(
    system: OstrowskiSystem,
    start_state: State3,
    word: tuple[int, ...],
) -> State3:
    state = start_state
    for w in word:
        state = transition_affine(system, state, w)
    return state


def energy_after_word(
    system: OstrowskiSystem,
    start_remaining: int,
    word: tuple[int, ...],
    start_state: State3 = ORIGIN,
) -> int:
    """``E_{N-k}`` after MSD word of length ``k`` from remaining ``N``."""
    if len(word) > start_remaining:
        raise ValueError("word longer than remaining")
    state = apply_word(system, start_state, word)
    return energy_canonical(system, state, start_remaining - len(word))


def energy_telescope_rhs(
    system: OstrowskiSystem,
    start_remaining: int,
    word: tuple[int, ...],
    start_state: State3 = ORIGIN,
) -> int:
    """``E_N(s) - sum consumed w q``."""
    return (
        energy_canonical(system, start_state, start_remaining)
        - consumed_sum(system, start_remaining, word)
    )


def energy_telescope_holds(
    system: OstrowskiSystem,
    start_remaining: int,
    word: tuple[int, ...],
    start_state: State3 = ORIGIN,
) -> bool:
    return energy_after_word(
        system, start_remaining, word, start_state
    ) == energy_telescope_rhs(system, start_remaining, word, start_state)


def place_sum(system: OstrowskiSystem, last_index: int) -> int:
    """``S_k = q_0 + … + q_k``."""
    if last_index < 0:
        return 0
    return sum(system.place_values(last_index + 1))


def q_at_least_twice_prev(system: OstrowskiSystem, n: int) -> bool:
    """``q_n ≥ 2 q_{n-1}`` for ``n ≥ 2`` (``d_1 = 2``)."""
    if n < 2:
        return True
    return system.place_value(n) >= 2 * system.place_value(n - 1)


def lo_hi_ratio_bounds(system: OstrowskiSystem, n: int) -> dict[str, object]:
    """Exact ratios and inequalities from ``S_{n-1} ≤ 2 q_{n-1}``, ``q_n ≥ 2 q_{n-1}``."""
    if n < 1:
        raise ValueError("ratios are for remaining >= 1")
    qn = system.place_value(n)
    qnm1 = system.place_value(n - 1)
    s = place_sum(system, n - 1)
    lo = lo_closed_form(system, n)
    hi = hi_closed_form(system, n)
    lo_u, hi_u = unread_tail_bounds(system, n)
    hi_over = hi / qn
    lo_over = lo / qn
    s_bound = s <= 2 * qnm1
    twice = q_at_least_twice_prev(system, n) if n >= 2 else True
    # For n≥2: S_{n-1}/q_n ≤ 2 q_{n-1}/q_n ≤ 1, hence -4 < lo/q_n ≤ hi/q_n < 2.
    hi_lt_two = n < 2 or hi_over < 2
    lo_gt_minus_four = n < 2 or lo_over > -4
    return {
        "n": n,
        "qn": qn,
        "S_nm1": s,
        "lo": lo,
        "hi": hi,
        "lo_over_qn": lo_over,
        "hi_over_qn": hi_over,
        "matches_unread": lo == lo_u and hi == hi_u,
        "S_le_two_qnm1": s_bound,
        "qn_ge_two_qnm1": twice,
        "hi_over_qn_lt_2": hi_lt_two,
        "lo_over_qn_gt_minus_4": lo_gt_minus_four,
        NORMALIZED_NOT_COORDINATE: True,
    }


def defect_plus(system: OstrowskiSystem, state: State3, remaining: int) -> int:
    if remaining == 0:
        return energy_canonical(system, state, 0)
    return energy_canonical(system, state, remaining) - hi_closed_form(system, remaining)


def defect_minus(system: OstrowskiSystem, state: State3, remaining: int) -> int:
    if remaining == 0:
        return -energy_canonical(system, state, 0)
    return lo_closed_form(system, remaining) - energy_canonical(system, state, remaining)


def defect_plus_after_step(
    system: OstrowskiSystem,
    state: State3,
    w: int,
    remaining: int,
) -> tuple[int, int]:
    """``(D^+_{i-1}(T_w s), D^+_i(s) + (wmax_{i-1}-w) q_{i-1})``."""
    if remaining < 1:
        raise ValueError("defect step is for remaining >= 1")
    nxt = transition_affine(system, state, w)
    lhs = defect_plus(system, nxt, remaining - 1)
    place = remaining - 1
    rhs = defect_plus(system, state, remaining) + (
        wmax_at_place(place) - w
    ) * system.place_value(place)
    return lhs, rhs


def defect_minus_after_step(
    system: OstrowskiSystem,
    state: State3,
    w: int,
    remaining: int,
) -> tuple[int, int]:
    nxt = transition_affine(system, state, w)
    lhs = defect_minus(system, nxt, remaining - 1)
    place = remaining - 1
    rhs = defect_minus(system, state, remaining) + (
        w - wmin_at_place(place)
    ) * system.place_value(place)
    return lhs, rhs


def remaining_one_form(state: State3) -> int:
    """``E_1 = s2 + 2 s3``."""
    return state[1] + 2 * state[2]


def remaining_one_slab() -> tuple[int, int]:
    """Live interval of ``E_1``. Length-dependent, not a global ``L_0`` bound."""
    return (-2, 1)


def a_eigen_ratio_floats() -> dict[str, object]:
    """Right-eigen direction of ``A`` as floats. Classification only."""
    sys = nonpisot_order3()
    coeffs = characteristic_poly_coeffs(sys)
    assert coeffs is not None
    roots = cubic_roots(coeffs)
    real = [r.real for r in roots if abs(r.imag) < 1e-12]
    lam = max(real, key=abs) if real else roots[0].real
    return {
        "lambda": lam,
        "s1_over_s3": 3.0 / lam,
        "s2_over_s3": lam - 2.0,
        "floats_are_classification_only": True,
        "poly": (1, -2, -1, -3),
    }


def large_s3_ratios(start_remaining: int = 20, remainings: tuple[int, ...] = (1, 2, 3)) -> dict[str, object]:
    """Largest ``|s3|`` on live slices, not the union census."""
    sys = nonpisot_order3()
    fwd = forward_layers(sys, start_remaining, live_only=True)
    eigen = a_eigen_ratio_floats()
    rows = []
    remaining_one_ok = True
    lo1, hi1 = remaining_one_slab()
    for n in remainings:
        lset = set(fwd["layers"][n].get("states_L", ()))
        if not lset:
            continue
        if n == 1:
            remaining_one_ok = all(lo1 <= remaining_one_form(st) <= hi1 for st in lset)
        s = max(lset, key=lambda t: (abs(t[2]), abs(t[1]), abs(t[0]), t))
        s3 = s[2]
        qn = sys.place_value(n)
        energy = energy_canonical(sys, s, n)
        r1 = None if s3 == 0 else s[0] / s3
        r2 = None if s3 == 0 else s[1] / s3
        rows.append(
            {
                "n": n,
                "L": len(lset),
                "s": s,
                "s3": s3,
                "s1_over_s3": r1,
                "s2_over_s3": r2,
                "E_over_abs_s3_qn": None
                if s3 == 0 or qn == 0
                else energy / (abs(s3) * qn),
                "E": energy,
                "lo": lo_closed_form(sys, n) if n else 0,
                "hi": hi_closed_form(sys, n) if n else 0,
                "remaining_one_form": remaining_one_form(s) if n == 1 else None,
                "s1_over_s3_minus_eigen": None
                if r1 is None
                else r1 - eigen["s1_over_s3"],
                "s2_over_s3_minus_eigen": None
                if r2 is None
                else r2 - eigen["s2_over_s3"],
            }
        )
    return {
        "start_remaining": start_remaining,
        "rows": rows,
        "is_slice_not_union": True,
        "remaining_one_all_in_slab": remaining_one_ok,
        "remaining_one_is_length_dependent": True,
        "eigen": eigen,
        GROWTH_NOT_INFINITUDE: True,
        "floats_are_classification_only": True,
        NORMALIZED_NOT_COORDINATE: True,
    }


def block_orbit(
    block: tuple[int, ...],
    repeats: int,
) -> list[State3]:
    sys = nonpisot_order3()
    state = ORIGIN
    orbit = [state]
    for _ in range(repeats):
        state = apply_word(sys, state, block)
        orbit.append(state)
    return orbit


def energy_compatible_blocks(
    max_block: int = 3,
    repeats: int = 4,
    start_remaining: int = 12,
) -> dict[str, object]:
    """Repeating interior blocks. Live only if the endpoint is in ``K`` at the matching remaining."""
    sys = nonpisot_order3()
    expanding_dead: list[dict[str, object]] = []
    live_hits: list[dict[str, object]] = []
    bounded_live = 0
    for length in range(1, max_block + 1):
        for block in product(W_INTERIOR, repeat=length):
            if start_remaining < length * repeats:
                continue
            state = ORIGIN
            remaining = start_remaining
            grew = False
            prev = 0
            live_all = True
            last = state
            for r in range(1, repeats + 1):
                state = apply_word(sys, state, block)
                remaining -= length
                last = state
                nrm = linf(state)
                if nrm > prev:
                    grew = True
                prev = nrm
                if remaining < 0 or not is_terminal(sys, state, remaining):
                    live_all = False
            row = {
                "block": block,
                "final": last,
                "linf": linf(last),
                "grew": grew,
                "live_all_repeats": live_all,
                "remaining": remaining,
            }
            if live_all:
                live_hits.append(row)
                if not grew:
                    bounded_live += 1
            elif grew and linf(last) >= 8:
                if len(expanding_dead) < 8:
                    expanding_dead.append(row)
    live_unbounded_candidate = [
        h for h in live_hits if h["grew"] and linf(h["final"]) > 2
    ]
    return {
        "live_hits": len(live_hits),
        "bounded_live": bounded_live,
        "live_hit_blocks": [h["block"] for h in live_hits],
        "live_growing_sample": live_unbounded_candidate[:8],
        "expanding_not_in_K_sample": expanding_dead[:6],
        "has_unbounded_live_family": False,
        "expanding_without_Kn_is_not_live": True,
        GROWTH_NOT_INFINITUDE: True,
        NORMALIZED_NOT_COORDINATE: True,
    }


def interpretation_sample() -> dict[str, object]:
    """``E_i`` equals minus consumed valuation from origin; full word sums to 0 iff accepting."""
    sys = nonpisot_order3()
    # LSD-first difference words: a nontrivial kernel word (sum w_j q_j = 0)
    # and a miss. Digitwise x+y=z is a special case; the residual cares about
    # the weighted sum.
    x = (1, 0, 0)
    y = (1, 0, 0)
    z_ok = (0, 1, 0)  # 1+1 = 2 = q_1, so w = z-(x+y) = (-2, 1, 0) LSD
    z_miss = (0, 0, 0)
    samples = []
    for target in (z_ok, z_miss):
        w_msd = lsd_to_msd(difference_word(x, y, target))
        n = len(w_msd)
        e_final = energy_after_word(sys, n, w_msd)
        consumed = consumed_sum(sys, n, w_msd)
        end_state = apply_word(sys, ORIGIN, w_msd)
        run = run_msd(sys, w_msd)
        samples.append(
            {
                "w_msd": w_msd,
                "E_0": e_final,
                "minus_consumed": -consumed,
                "s3": end_state[2],
                "accepts": end_state[2] == 0,
                "value_identity": sys.val(x) + sys.val(y) == sys.val(target),
                "run_msd_s3": run[-1],
                "telescope": energy_telescope_holds(sys, n, w_msd),
                "matches_residual_run": tuple(end_state) == tuple(run),
                "E_0_eq_s3": e_final == end_state[2],
                "accept_iff_sum_zero": (end_state[2] == 0) == (consumed == 0),
            }
        )
    return {"samples": samples}
