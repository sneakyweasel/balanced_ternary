"""Accepting / live terminal geometry of the unread-tail residual.

Four objects, never mixed:

- ``K_0 = F = {s_3 = 0}``. Machine acceptance at remaining 0, because
  ``E_0 = s_3``. Infinite plane. Canonical digits do not constrain
  ``(s_1, s_2)`` at remaining 0.
- ``K_n = {s : lo(n) ≤ E_n(s) ≤ hi(n)}`` for ``n ≥ 1``. Same predicate
  as ``residual_is_live``. Infinite slab.
- ``R_≤N``: forward live-reachable from ``(0,0,0)``.
- ``L``: infinite-horizon live set from the origin. Not established.

``is_terminal(s, n)`` is liveness at remaining ``n``, which is existence
of a legal unread tail realizing ``E_n``. That tail is an accepting
suffix, so this is not inferred from reachability from the origin.

``w_j = z_j - (x_j + y_j)`` as in ``residual.py``. Singleton ``{(0,0,0)}``
is not ``K``. Unbounded ``K`` is not infinitude of ``L``.
"""

from __future__ import annotations

from research.ostrowski.live_growth import (
    legal_w,
    residual_is_live,
    unread_tail_bounds,
)
from research.ostrowski.nonpisot_search import HUB
from research.ostrowski.residual import residual_integer
from research.ostrowski.residual_closure import B_MIN
from research.ostrowski.system import OstrowskiSystem, nonpisot_order3, phase0_order3

State3 = tuple[int, int, int]

SAMPLE_ACCEPTING: State3 = (30, 25, 0)
WINDOW_M = 4


def is_terminal(system: OstrowskiSystem, state: State3, remaining: int) -> bool:
    """Exact terminal / live predicate at remaining length ``remaining``.

    Remaining 0 is ``s_3 = 0``. Remaining ``n ≥ 1`` is the unread-tail
    slab. Identical to ``residual_is_live``.
    """
    return residual_is_live(system, state, remaining)


def energy_on_f(system: OstrowskiSystem, s1: int, s2: int, remaining: int) -> int:
    """``E_n(s1, s2, 0)``. At remaining 0 this is 0."""
    return residual_integer(system, (s1, s2, 0), remaining)


def kernel_family_state(system: OstrowskiSystem, n: int) -> State3:
    """``t_n = (q_{n-1}, -q_{n-2}, 0)`` for ``n ≥ 1``."""
    if n < 1:
        raise ValueError("kernel family is defined for remaining n >= 1")
    return (system.place_value(n - 1), -system.place_value(n - 2), 0)


def zero_seed_family_state(k: int) -> State3:
    """``(k, 0, 0) ∈ K_0`` for every integer ``k``."""
    return (k, 0, 0)


def lo_hi_straddle_zero(system: OstrowskiSystem, remaining: int) -> bool:
    """``lo(n) < 0 < hi(n)`` for ``n ≥ 1``, from signed alphabets."""
    if remaining < 1:
        raise ValueError("straddle is for remaining >= 1")
    lo, hi = unread_tail_bounds(system, remaining)
    lsd = legal_w(system, 0)
    return lo <= lsd[0] and hi >= lsd[-1] and lo < 0 < hi


def kernel_family_is_terminal(system: OstrowskiSystem, n: int) -> bool:
    """``E_n(t_n) = 0 ∈ [lo(n), hi(n)]``."""
    t = kernel_family_state(system, n)
    energy = residual_integer(system, t, n)
    return energy == 0 and is_terminal(system, t, n) and lo_hi_straddle_zero(system, n)


def place_values_strictly_increasing(system: OstrowskiSystem, n: int) -> bool:
    """``q_k > q_{k-1}`` for ``1 ≤ k < n``, hence ``|t_n| → ∞``."""
    if n < 2:
        return True
    qs = system.place_values(n)
    return all(qs[k] > qs[k - 1] for k in range(1, n))


def last_step_lands_in_f(state: State3, w: int) -> bool:
    """``T_w(s)_3 = 0`` iff ``w = s_2 + 2 s_3`` (constant ``d_1 = 2``)."""
    return state[1] + 2 * state[2] - w == 0


def lsd_last_step_is_remaining_one_liveness(
    system: OstrowskiSystem,
    state: State3,
) -> bool:
    """Live at remaining 1 iff the unique ``w`` landing in ``F`` is LSD-legal.

    For this pair of systems ``E_1 = s_2 + 2 s_3`` and ``W_LSD = {-2,…,1}``.
    """
    energy = residual_integer(system, state, 1)
    lo, hi = unread_tail_bounds(system, 1)
    live = lo <= energy <= hi
    w = state[1] + 2 * state[2]
    lsd = legal_w(system, 0)
    return live == (w in lsd) and energy == w


def kn_is_infinite_slab(system: OstrowskiSystem, n: int) -> dict[str, object]:
    """``|K_n| = ∞`` and ``|K_n ∩ F| = ∞``. Not a finite census."""
    if n == 0:
        return {
            "n": 0,
            "cardinality": "infinite",
            "plane_cardinality": "infinite",
            "reason": "K_0 = F = {s3 = 0}",
            "lo_hi": (0, 0),
        }
    t = kernel_family_state(system, n)
    lo, hi = unread_tail_bounds(system, n)
    # Distinct kernel points (k t_n) stay in F with energy 0.
    distinct = {(k * t[0], k * t[1], 0) for k in range(-5, 6)}
    return {
        "n": n,
        "cardinality": "infinite",
        "plane_cardinality": "infinite",
        "lo_hi": (lo, hi),
        "linear_form": "s1 q_{n-2} + s2 q_{n-1} + s3 q_n",
        "kernel_sample_in_f": t,
        "distinct_kernel_points_on_f": len(distinct),
        "kernel_family_terminal": kernel_family_is_terminal(system, n),
    }


def boxed_window_count(
    system: OstrowskiSystem,
    n: int,
    box: int = WINDOW_M,
) -> dict[str, int]:
    """``|K_n ∩ [-M,M]^3|``. A window, not ``|K_n|``."""
    count = 0
    plane = 0
    for s1 in range(-box, box + 1):
        for s2 in range(-box, box + 1):
            for s3 in range(-box, box + 1):
                if is_terminal(system, (s1, s2, s3), n):
                    count += 1
                    if s3 == 0:
                        plane += 1
    return {"n": n, "M": box, "window_count": count, "window_plane_count": plane}


def hi_closed_form(system: OstrowskiSystem, n: int) -> int:
    """``hi(n) = 2 S_{n-1} - 1`` for these alphabets (``d_1 = 2``)."""
    if n < 1:
        return 0
    s = sum(system.place_values(n))
    return 2 * s - 1


def lo_closed_form(system: OstrowskiSystem, n: int) -> int:
    """``lo(n) = -4 S_{n-1} + 2`` for these alphabets."""
    if n < 1:
        return 0
    s = sum(system.place_values(n))
    return -4 * s + 2


def sample_accepting_only_at_remaining_zero(system: OstrowskiSystem) -> dict[str, object]:
    """``(30, 25, 0) ∈ K_0`` and not in any ``K_n`` for ``n ≥ 1``.

    For ``n ≥ 1``, ``E_n ≥ 25 q_{n-1}`` and ``hi(n) = 2 S_{n-1} - 1``.
    Place sums satisfy ``S_k ≤ 2 q_k``, so ``hi(n) ≤ 4 q_{n-1} - 1 < 25 q_{n-1}``.
    """
    sample = SAMPLE_ACCEPTING
    in_k0 = is_terminal(system, sample, 0)
    s_bound = place_sum_at_most_twice_last(system, 24)
    never_later = True
    for n in range(1, 25):
        if is_terminal(system, sample, n):
            never_later = False
            break
        q = system.place_value(n - 1)
        energy = energy_on_f(system, sample[0], sample[1], n)
        if not (energy >= 25 * q and hi_closed_form(system, n) <= 4 * q - 1):
            never_later = False
            break
    return {
        "state": sample,
        "in_K_0": in_k0,
        "in_any_K_n_for_n_ge_1": not never_later,
        "place_sum_bound": s_bound,
        "live_remaining_lengths": (0,) if in_k0 and never_later else None,
        "only_remaining_zero": in_k0 and never_later,
    }


def place_sum_at_most_twice_last(system: OstrowskiSystem, up_to: int) -> bool:
    """``S_k ≤ 2 q_k`` for ``0 ≤ k ≤ up_to``, used in the (30,25,0) gap."""
    qs = system.place_values(up_to + 1)
    total = 0
    for k, q in enumerate(qs):
        total += q
        if total > 2 * q:
            return False
    return True


def place_sum_bound_inductive(system: OstrowskiSystem) -> bool:
    """``q_n ≥ 2 q_{n-1}`` for ``n ≥ 2`` implies ``S_n ≤ 2 q_n`` inductively.

    Both comparison systems have ``d_1 = 2`` and nonnegative remaining
    coefficients, so ``q_n = 2 q_{n-1} + … ≥ 2 q_{n-1}``. Base ``S_0 = 1 ≤ 2``.
    """
    digits = (system.d(1, 1), system.d(2, 1), system.d(3, 1))
    if digits[0] != 2:
        return False
    q0, q1 = system.place_value(0), system.place_value(1)
    if q0 != 1 or q0 > 2 * q0:
        return False
    s1 = q0 + q1
    return s1 <= 2 * q1 and digits[1] >= 0 and digits[2] >= 0


def hub_in_every_kn(system: OstrowskiSystem, max_n: int) -> bool:
    return all(is_terminal(system, HUB, n) for n in range(max_n + 1))


def pisot_terminal_comparison() -> dict[str, object]:
    """Same ``K_0 = F`` for both systems. ``B_MIN`` is reachable-live, not ``K``."""
    control = phase0_order3()
    np_sys = nonpisot_order3()
    terminals = {s for s in B_MIN if s[2] == 0}
    return {
        "control_K_0_is_F": all(
            is_terminal(control, (k, 0, 0), 0) for k in (-4, 0, 7, 30)
        ),
        "np_K_0_is_F": all(is_terminal(np_sys, (k, 0, 0), 0) for k in (-4, 0, 7, 30)),
        "b_min_cardinality": len(B_MIN),
        "b_min_in_F": len(terminals),
        "b_min_is_not_K_0": True,
        "structural_change": "reachable live set, not the terminal predicate",
    }


def terminal_report(max_n: int = 8, box: int = WINDOW_M) -> dict[str, object]:
    """Exact characterization plus a boxed window. Window ≠ |K_n|."""
    sys = nonpisot_order3()
    rows = []
    for n in range(max_n + 1):
        window = boxed_window_count(sys, n, box)
        lo, hi = unread_tail_bounds(sys, n)
        row = {
            "n": n,
            "K_n_cardinality": "infinite",
            "K_n_cap_F_cardinality": "infinite",
            "lo": lo,
            "hi": hi,
            "window_M": box,
            "window_count": window["window_count"],
            "window_plane_count": window["window_plane_count"],
        }
        if n >= 1:
            t = kernel_family_state(sys, n)
            row["t_n"] = t
            row["t_n_l1"] = abs(t[0]) + abs(t[1])
            row["t_n_terminal"] = kernel_family_is_terminal(sys, n)
        rows.append(row)
    return {
        "rows": rows,
        "sample": sample_accepting_only_at_remaining_zero(sys),
        "hub_in_K_0_through_max": hub_in_every_kn(sys, max_n),
        "singleton_zero_is_not_K": True,
        "unbounded_K_is_not_infinitude_of_L": True,
        "pisot": pisot_terminal_comparison(),
        "place_values_increasing": place_values_strictly_increasing(sys, max_n + 2),
        "lsd_last_step_check": lsd_last_step_is_remaining_one_liveness(
            sys, (1, -1, 2)
        ),
    }
