"""Origin-reachable live set versus the unbounded terminal family.

Three relations, never mixed:

- ``R(0)``: forward images of ``(0,0,0)`` under legal ``T_w`` (no
  liveness). After one step, ``s_1 = 3 s_3``, so every reachable state
  has ``s_1 ≡ 0 (mod 3)``.
- ``K_n``: unread-tail acceptance / liveness (``is_terminal``).
- ``L_0``: states that appear on some live path from the origin.
  Computationally ``∪_N reachable_live(N)``. Not proved finite or
  infinite.

The kernel family ``t_n = (q_{n-1}, -q_{n-2}, 0)`` is in ``K_n ∩ F``
and unbounded. That does not imply ``t_n ∈ R(0)`` or ``|L_0| = ∞``.

Pisot comparison: ``Γ_P`` has ``s_1' = s_3``, so ``s_1 ≡ 0 (mod 3)``
is not forced. ``B_MIN`` occupies all three residue classes.

Observed remaining-0 terminals span the full lattice ``3Z × Z`` in
``F``: extra congruence beyond ``3 | a`` fails at finite horizon.
That is not ``|L_0|=∞``. Reverse on ``F`` is ``integer_preimage``.
"""

from __future__ import annotations

from functools import reduce
from itertools import product
from math import gcd

from research.ostrowski.live_growth import legal_w, reachable_live
from research.ostrowski.nonpisot_search import HUB
from research.ostrowski.residual_closure import B_MIN
from research.ostrowski.reverse_map import integer_preimage
from research.ostrowski.spectral_residual import transition_affine
from research.ostrowski.system import OstrowskiSystem, nonpisot_order3, phase0_order3
from research.ostrowski.terminal_set import is_terminal, kernel_family_state

State3 = tuple[int, int, int]


def q_mod_period(system: OstrowskiSystem, modulus: int) -> tuple[int, ...]:
    """Smallest period of ``(q_n) mod m`` detected by repeating the first triple."""
    if modulus < 2:
        raise ValueError("modulus must be >= 2")
    start = (
        system.place_value(0) % modulus,
        system.place_value(1) % modulus,
        system.place_value(2) % modulus,
    )
    seq = [start[0], start[1], start[2]]
    for n in range(3, modulus**3 + 8):
        triple = (
            system.place_value(n - 2) % modulus,
            system.place_value(n - 1) % modulus,
            system.place_value(n) % modulus,
        )
        seq.append(triple[2])
        if triple == start:
            return tuple(seq[:-3])
    raise RuntimeError("place-value recurrence did not period modulo m")


def q_mod3_period() -> tuple[int, ...]:
    """``q_n ≡ (1,2,2,0,2,1,1,0)`` repeating. Recurrence drops the ``3 q_{n-3}`` term."""
    period = q_mod_period(nonpisot_order3(), 3)
    assert period == (1, 2, 2, 0, 2, 1, 1, 0)
    return period


def q_mod9_period() -> tuple[int, ...]:
    return q_mod_period(nonpisot_order3(), 9)


def forward_forces_s1_divisible_by_3(state: State3, w: int) -> bool:
    """``T_w(s)_1 = 3 s_3 ≡ 0 (mod 3)`` for ``Γ_NP`` (``d_3 = 3``)."""
    s1, s2, s3 = state
    image = (3 * s3, s1 + s3, s2 + 2 * s3 - w)
    return image[0] % 3 == 0 and image == transition_affine(nonpisot_order3(), state, w)


def origin_reachable_implies_s1_mod3_zero(state: State3) -> bool:
    """Necessary condition on ``R(0)``: origin has ``s_1=0``, and every image too."""
    return state[0] % 3 == 0


def kernel_family_s1_mod3(n: int) -> int:
    """``t_n`` has first coordinate ``q_{n-1}``."""
    period = q_mod3_period()
    return period[(n - 1) % 8]


def kernel_family_compatible_with_s1_mod3(n: int) -> bool:
    """Necessary residue for ``t_n ∈ R(0)``: ``q_{n-1} ≡ 0 (mod 3)``, i.e. ``n ≡ 0 (mod 4)``."""
    return kernel_family_s1_mod3(n) == 0


def kernel_predecessor_s1(system: OstrowskiSystem, n: int) -> int | None:
    """``s_1`` of every integer preimage of ``t_n``, independent of ``w``.

    ``s_1 = -q_{n-2} - q_{n-1}/3`` when ``3 | q_{n-1}``, else ``None``.
    """
    t = kernel_family_state(system, n)
    if t[0] % 3 != 0:
        return None
    return t[1] - t[0] // 3


def kernel_family_blocked_at_first_reverse(n: int) -> bool:
    """``t_n`` cannot be a forward image of any origin-reachable state.

    Immediate predecessors all share an ``s_1 ≢ 0 (mod 3)``.
    """
    s1 = kernel_predecessor_s1(nonpisot_order3(), n)
    if s1 is None:
        return True
    return s1 % 3 != 0


def two_step_f_to_f(s1: int, s2: int, w: int, v: int) -> State3 | None:
    """``F → {s_1=0} → F`` lands on the ray ``(3a, a, 0)`` with ``a = s_2 - w``.

    Second coordinate of the image is 0 iff ``v = s_1 + 2(s_2 - w)``.
    """
    mid: State3 = (0, s1, s2 - w)
    if v != s1 + 2 * (s2 - w):
        return None
    a = s2 - w
    image: State3 = (3 * a, a, 0)
    sys = nonpisot_order3()
    assert transition_affine(sys, (s1, s2, 0), w) == mid
    assert transition_affine(sys, mid, v) == image
    return image


def reverse_cone_hits_origin(
    target: State3,
    max_depth: int,
    alphabet: tuple[int, ...] | None = None,
) -> dict[str, object]:
    """Integer reverse BFS. Legal ``w`` from the interior alphabet by default."""
    sys = nonpisot_order3()
    letters = alphabet if alphabet is not None else legal_w(sys, 1)
    seen: set[State3] = {target}
    layer: set[State3] = {target}
    hit = target == (0, 0, 0)
    depth = 0
    for depth in range(1, max_depth + 1):
        nxt: set[State3] = set()
        for t in layer:
            if t[0] % 3 != 0:
                continue
            for w in letters:
                pred = integer_preimage(t, w)
                if pred is None or pred in seen:
                    continue
                seen.add(pred)
                nxt.add(pred)
                if pred == (0, 0, 0):
                    hit = True
        if not nxt or hit:
            break
        layer = nxt
    return {
        "target": target,
        "cardinality": len(seen),
        "depth": depth,
        "hit_origin": hit,
        "min_l1": min(abs(s[0]) + abs(s[1]) + abs(s[2]) for s in seen),
        "max_l1": max(abs(s[0]) + abs(s[1]) + abs(s[2]) for s in seen),
    }


def live_scan(max_length: int) -> dict[str, object]:
    """``L_{≤N}`` census. Growth is not infinitude; no ``t_n`` expected."""
    sys = nonpisot_order3()
    report = reachable_live(sys, max_length)
    states: frozenset[State3] = report["states"]  # type: ignore[assignment]
    on_f = [s for s in states if s[2] == 0]
    tn_hits = [
        n
        for n in range(1, max_length + 4)
        if kernel_family_state(sys, n) in states
    ]
    return {
        "N": max_length,
        "L_card": report["live_states"],
        "max_abs": (
            report["max_abs_s1"],
            report["max_abs_s2"],
            report["max_abs_s3"],
        ),
        "max_l1": report["max_l1"],
        "F_card": len(on_f),
        "all_s1_mod3_zero": all(s[0] % 3 == 0 for s in states),
        "kernel_family_hits": tn_hits,
        "hub_in_L": HUB in states,
        "finite_depth_is_not_infinitude": True,
    }


def pisot_has_no_s1_mod3_trap() -> dict[str, object]:
    residues = sorted({s[0] % 3 for s in B_MIN})
    return {
        "b_min_s1_mod3": residues,
        "occupies_all_three_classes": residues == [0, 1, 2],
        "np_map_forces_s1_mod3_zero": True,
        "structural_difference": "NP has s1' = 3 s3; Pisot has s1' = s3",
    }


def kernel_family_reachability_report(max_n: int = 24) -> dict[str, object]:
    sys = nonpisot_order3()
    rows = []
    for n in range(1, max_n + 1):
        t = kernel_family_state(sys, n)
        s1_pred = kernel_predecessor_s1(sys, n)
        blocked = kernel_family_blocked_at_first_reverse(n)
        rows.append(
            {
                "n": n,
                "t_n": t,
                "q_nm1_mod3": kernel_family_s1_mod3(n),
                "s1_mod3_ok": kernel_family_compatible_with_s1_mod3(n),
                "pred_s1": s1_pred,
                "pred_s1_mod3": None if s1_pred is None else s1_pred % 3,
                "blocked_at_first_reverse": blocked,
                "in_K_n": is_terminal(sys, t, n),
            }
        )
    remaining = [r["n"] for r in rows if not r["blocked_at_first_reverse"]]
    return {
        "rows": rows,
        "blocked_count": sum(1 for r in rows if r["blocked_at_first_reverse"]),
        "open_n": remaining,
        "open_n_are_0_or_12_mod_24": all(n % 24 in (0, 12) for n in remaining),
        "unbounded_K_does_not_imply_unbounded_L0": True,
    }


def remaining_zero_states(start_remaining: int) -> set[State3]:
    """Origin-live remaining-0 slice ``L_0(N)``. Not infinitude."""
    from research.ostrowski.live_layers import forward_layers

    report = forward_layers(nonpisot_order3(), start_remaining, live_only=True)
    return set(report["layers"][0].get("states_L", ()))


def on_two_step_ray(state: State3) -> bool:
    return state[2] == 0 and state[0] == 3 * state[1]


def _gcd_all(values: list[int]) -> int:
    return abs(reduce(gcd, values, 0))


EXTRA_CONGRUENCE_REFUTED = "extra_terminal_congruence_beyond_3_divides_a_refuted"
GROWTH_NOT_INFINITUDE = "finite_depth_is_not_infinitude"
REVERSE_IS_STEP = "f_predecessor_is_integer_preimage"


def terminal_span_report(n_small: int = 12, n_large: int = 16) -> dict[str, object]:
    """Observed ``L_0(N)`` spans the full ``3Z × Z`` lattice in ``F``.

    Extra modulus on ``b``, or ``9 | a``, fails at these horizons.
    New terminals at 16 versus 12 are not ``|L_0|=∞``. Reverse on ``F``
    is ``integer_preimage``, Lean ``unique_predecessor``.
    """
    small = remaining_zero_states(n_small)
    large = remaining_zero_states(n_large)
    new = large - small
    gcd_a = _gcd_all([s[0] for s in small])
    gcd_b = _gcd_all([s[1] for s in small])
    off_ray_small = {s for s in small if not on_two_step_ray(s)}
    form_rows = []
    for alpha, beta in product(range(-3, 4), repeat=2):
        if alpha == 0 and beta == 0:
            continue
        mx_s = max(abs(alpha * s[0] + beta * s[1]) for s in small)
        mx_l = max(abs(alpha * s[0] + beta * s[1]) for s in large)
        form_rows.append(
            {
                "coeff": (alpha, beta),
                "max_small": mx_s,
                "max_large": mx_l,
                "grows": mx_l > mx_s,
            }
        )
    extra_congruence = gcd_a != 3 or gcd_b != 1 or all(s[0] % 9 == 0 for s in small)
    from research.ostrowski.live_layers import linf

    max_small = max(linf(s) for s in small) if small else 0
    max_large = max(linf(s) for s in large) if large else 0
    return {
        "n_small": n_small,
        "n_large": n_large,
        "L0_small": len(small),
        "L0_large": len(large),
        "new_terminals": len(new),
        "gcd_a": gcd_a,
        "gcd_b": gcd_b,
        "spans_3Z_x_Z": gcd_a == 3 and gcd_b == 1,
        "all_on_F": all(s[2] == 0 for s in small | large),
        "all_a_div3": all(s[0] % 3 == 0 for s in small | large),
        "not_all_a_div9": any(s[0] % 9 != 0 for s in small),
        "off_ray_small": len(off_ray_small),
        "hub_in_small": HUB in small,
        "maximizer_small": max(
            small, key=lambda s: (max(abs(s[0]), abs(s[1]), abs(s[2])), s)
        ),
        "max_linf_small": max_small,
        "max_linf_large": max_large,
        "f_forms_all_grow": all(row["grows"] for row in form_rows),
        "f_form_stable_count": sum(1 for row in form_rows if not row["grows"]),
        EXTRA_CONGRUENCE_REFUTED: not extra_congruence,
        GROWTH_NOT_INFINITUDE: True,
        REVERSE_IS_STEP: True,
    }


def cumulative_remaining_zero(max_n: int = 8) -> dict[str, object]:
    """``C(N)=|∪_{m≤N} L_0(m)|``. Reset padding is not first appearance.

    Finite-horizon growth of ``C(N)`` is not ``|L_0|=∞``. Hub has
    ``ℓ_min=2``. Primitive image ``P`` equals ``L_0`` by shortest
    realizations; that is not a new census.
    """
    from research.ostrowski.live_layers import linf

    acc: set[State3] = set()
    rows: list[dict[str, object]] = []
    hub_first: int | None = None
    for n in range(max_n + 1):
        layer = remaining_zero_states(n)
        new = layer - acc
        acc |= layer
        if hub_first is None and HUB in acc:
            hub_first = n
        max_linf = max((linf(s) for s in acc), default=0)
        rows.append(
            {
                "N": n,
                "L0": len(layer),
                "C": len(acc),
                "delta": len(new),
                "M": max_linf,
            }
        )
    return {
        "max_n": max_n,
        "rows": rows,
        "C_final": len(acc),
        "C_grows": len(acc) > (rows[0]["C"] if rows else 0),
        "hub_ell_min": hub_first,
        GROWTH_NOT_INFINITUDE: True,
    }
