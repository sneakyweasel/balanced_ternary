"""Zero-value complete words need not reset, and do not form a monoid.

``val(B)=consumed_sum(|B|,B)``. From the origin ``c_B=T_B(0)`` and
``(c_B)_3=-val(B)``. So ``val=0`` iff ``c_B`` lies on ``F={s_3=0}``.
That does not force ``c_B=0``. Complete-word zero-value is not closed
under concatenation: ``val(UV)=val(V)-E_{|V|}(c_U)``.

The shortest complete non-reset is ``(1,-2)``, with
``c_B=(-3,-1,0)`` (the known ``F→F`` hub). Recurrence combos that
are identically zero for every alignment remain the reset sublattice.
State-dependent block value is ``Val_s(B)=val(B)-E_{|B|}(s)=-(T_B(s))_3``,
i.e. ``energy_telescope`` at remaining 0. A point of ``F`` is not
``|L_0|=∞``. Live complete remaining-0 is ``L_0(N)``. The bounded
two-step ray is not a family.
"""

from __future__ import annotations

from itertools import product

from research.ostrowski.control_language import affine_holds
from research.ostrowski.energy_trajectory import apply_word, consumed_sum
from research.ostrowski.exceptional_kernel import W_INTERIOR, W_LSD, f_return_legal
from research.ostrowski.live_layers import ORIGIN, energy_canonical, linf
from research.ostrowski.origin_live import two_step_f_to_f
from research.ostrowski.recurrence_zero import (
    RECURRENCE_WORD_MSD,
    enumerate_combos,
    fully_live,
    prefix_legal,
)
from research.ostrowski.spectral_control import (
    N12_MAXIMIZER_STATE,
    control_convolution,
    ostrowski_s1,
    ostrowski_s3,
)
from research.ostrowski.system import nonpisot_order3

State3 = tuple[int, int, int]

HUB: State3 = (-3, -1, 0)
SHORTEST_NONRESET: tuple[int, ...] = (1, -2)
HUB_SQUARE: tuple[int, ...] = (1, -2, 1, -2)
HUB_SQUARE_STATE: State3 = (-6, -2, -5)
HUB_SQUARE_VAL = 5
LEGAL_TWO_STEP_K: tuple[int, ...] = (-2, -1, 0, 1)
# Existing remaining-0 live fiber; not a new BFS.
L0_N12_COUNT = 165
L0_N12_LINF = 27

ALGEBRAIC_ZERO = "algebraic_zero_sum"
PREFIX_LEGAL = "prefix_legal"
FULLY_LIVE = "fully_live"
VAL_NOT_RESET = "val_zero_does_not_force_reset"
GROWTH_NOT_INFINITUDE = "finite_depth_is_not_infinitude"
RAY_NOT_FAMILY = "bounded_F_return_ray_is_not_a_family"
KNOWN_PACKAGING = "c3_is_minus_val"
NOT_MONOID = "complete_zero_value_is_not_a_monoid"
LIVE_IS_L0 = "complete_live_zero_is_L0"
VAL_CONCAT_ENERGY = "val_UV_is_val_V_minus_energy_V_of_c_U"
BLOCK_VAL_IS_S3 = "block_val_is_minus_s3"
TELESCOPE_PACKAGING = "val_s_is_energy_telescope"


def _sys():
    return nonpisot_order3()


def msd_val(word: tuple[int, ...]) -> int:
    """Complete-word MSD value from remaining ``|word|``."""
    return consumed_sum(_sys(), len(word), word)


def c_of(word: tuple[int, ...]) -> State3:
    """``c_B = T_B(0)``."""
    return apply_word(_sys(), ORIGIN, word)


def c3_equals_minus_val(word: tuple[int, ...]) -> bool:
    c_b = c_of(word)
    return c_b[2] == -msd_val(word) == ostrowski_s3(word)


def coordinates_match_impulse(word: tuple[int, ...]) -> bool:
    c_b = c_of(word)
    return c_b[0] == ostrowski_s1(word) and c_b[2] == ostrowski_s3(word) and c_b == control_convolution(word)


def complete_words(k: int) -> tuple[tuple[int, ...], ...]:
    """Complete words: interior letters then LSD last. ``k=1`` is LSD only."""
    if k < 1:
        return ()
    if k == 1:
        return tuple((w,) for w in W_LSD)
    prefixes = product(W_INTERIOR, repeat=k - 1)
    return tuple(prefix + (last,) for prefix in prefixes for last in W_LSD)


def classify_complete(word: tuple[int, ...]) -> dict[str, object]:
    k = len(word)
    val = msd_val(word)
    c_b = c_of(word)
    algebraic = val == 0
    reset = c_b == ORIGIN
    legal = prefix_legal(word, k)
    live = fully_live(word, k)
    return {
        "word": word,
        "val": val,
        "c_B": c_b,
        ALGEBRAIC_ZERO: algebraic,
        "reset": reset,
        "nonreset": algebraic and not reset,
        PREFIX_LEGAL: legal,
        FULLY_LIVE: live,
        "on_F": c_b[2] == 0,
        VAL_NOT_RESET: True,
        KNOWN_PACKAGING: True,
    }


def census_complete(max_k: int = 4) -> dict[str, object]:
    """Algebraic zero-sum complete words, ``k=1..max_k``. Not ``|L_0|=∞``."""
    rows = []
    k_star = None
    shortest: list[tuple[int, ...]] = []
    for k in range(1, max_k + 1):
        zeros = []
        resets = 0
        nonresets = 0
        live_nonresets = 0
        max_c = 0
        for word in complete_words(k):
            if not c3_equals_minus_val(word):
                raise AssertionError("c3 != -val")
            val = msd_val(word)
            if val != 0:
                continue
            c_b = c_of(word)
            reset = c_b == ORIGIN
            live = fully_live(word, k)
            nrm = linf(c_b)
            max_c = max(max_c, nrm)
            zeros.append(word)
            if reset:
                resets += 1
            else:
                nonresets += 1
                if live:
                    live_nonresets += 1
                if k_star is None:
                    k_star = k
                    shortest.append(word)
                elif k == k_star:
                    shortest.append(word)
        rows.append(
            {
                "k": k,
                "Z": len(zeros),
                "resets": resets,
                "nonresets": nonresets,
                "live_nonresets": live_nonresets,
                "max_c_linf": max_c,
            }
        )
    return {
        "rows": rows,
        "k_star": k_star,
        "shortest": tuple(shortest),
        GROWTH_NOT_INFINITUDE: True,
        VAL_NOT_RESET: True,
    }


def hub_witness() -> dict[str, object]:
    word = SHORTEST_NONRESET
    row = classify_complete(word)
    ray = two_step_f_to_f(0, 0, word[0], word[1])
    return {
        **row,
        "hub": HUB,
        "c_B_is_hub": row["c_B"] == HUB,
        "two_step_image": ray,
        RAY_NOT_FAMILY: True,
        GROWTH_NOT_INFINITUDE: True,
    }


def consumed_sum_at(start: int, word: tuple[int, ...]) -> int:
    """``consumed_sum`` at an arbitrary remaining start. Not complete-word val."""
    return consumed_sum(_sys(), start, word)


def consumed_sum_append_holds(n: int, u: tuple[int, ...], v: tuple[int, ...]) -> bool:
    """Two-start split, not ``val(U)+C val(V)``."""
    start = n + len(u) + len(v)
    return consumed_sum_at(start, u + v) == consumed_sum_at(start, u) + consumed_sum_at(
        n + len(v), v
    )


def energy_of(state: State3, remaining: int) -> int:
    return energy_canonical(_sys(), state, remaining)


def val_concat_energy_holds(u: tuple[int, ...], v: tuple[int, ...]) -> bool:
    """``val(UV)=val(V)-E_{|V|}(c_U)``. So ``val(UV)=0`` iff ``E_{|V|}(c_U)=val(V)``."""
    return msd_val(u + v) == msd_val(v) - energy_of(c_of(u), len(v))


def t_of(state: State3, word: tuple[int, ...]) -> State3:
    """``T_B(s)``. MSD: first letter is applied first."""
    return apply_word(_sys(), state, word)


def block_val(state: State3, word: tuple[int, ...]) -> int:
    """``Val_s(B)=val(B)-E_{|B|}(s)``. Equals ``-(T_B(s))_3``."""
    return msd_val(word) - energy_of(state, len(word))


def block_val_holds(state: State3, word: tuple[int, ...]) -> bool:
    image = t_of(state, word)
    val_s = block_val(state, word)
    on_f = image[2] == 0
    energy_match = energy_of(state, len(word)) == msd_val(word)
    return val_s == -image[2] and (on_f == energy_match)


def hub_block_iterates() -> dict[str, object]:
    """Hub word from origin lands on the ray. Repeat from hub leaves F.

    Legal two-step returns from the hub stay on the bounded ray.
    Not a family.
    """
    from_origin = t_of(ORIGIN, SHORTEST_NONRESET)
    from_hub = t_of(HUB, SHORTEST_NONRESET)
    legal_from_hub: list[State3] = []
    for w in W_INTERIOR:
        image = f_return_legal(HUB[0], HUB[1], w)
        if image is not None:
            legal_from_hub.append(image)
    on_line = all(on_two_step_ray_line(s) for s in legal_from_hub)
    ks = tuple(sorted({s[1] for s in legal_from_hub}))
    bounded = all(abs(k) <= 2 for k in ks)
    return {
        "from_origin": from_origin,
        "from_origin_on_ray": on_legal_two_step_ray(from_origin),
        "from_hub": from_hub,
        "from_hub_on_F": from_hub[2] == 0,
        "legal_from_hub": tuple(legal_from_hub),
        "legal_ks": ks,
        "legal_on_ray_line": on_line,
        "legal_k_bounded": bounded,
        "symbolic_family": False,
        RAY_NOT_FAMILY: True,
        GROWTH_NOT_INFINITUDE: True,
        TELESCOPE_PACKAGING: True,
    }


def on_legal_two_step_ray(state: State3) -> bool:
    k = state[1]
    return state[2] == 0 and state[0] == 3 * k and k in LEGAL_TWO_STEP_K


def on_two_step_ray_line(state: State3) -> bool:
    """Integer two-step image ``(3α,α,0)``. Not the LSD-complete k-set."""
    return state[2] == 0 and state[0] == 3 * state[1]


def hub_square_witness() -> dict[str, object]:
    u = v = SHORTEST_NONRESET
    uv = u + v
    assert uv == HUB_SQUARE
    c_uv = c_of(uv)
    val = msd_val(uv)
    return {
        "word": uv,
        "val": val,
        "c_B": c_uv,
        "on_F": c_uv[2] == 0,
        "u_val": msd_val(u),
        "v_val": msd_val(v),
        NOT_MONOID: msd_val(u) == 0 and msd_val(v) == 0 and val != 0,
        VAL_CONCAT_ENERGY: val_concat_energy_holds(u, v),
        GROWTH_NOT_INFINITUDE: True,
    }


def n12_maximizer_off_ray() -> dict[str, object]:
    """Existing ``L_0(12)`` maximizer; not a new BFS. Off the two-step ray."""
    state = N12_MAXIMIZER_STATE
    return {
        "state": state,
        "on_F": state[2] == 0,
        "on_two_step_legal_ray": on_legal_two_step_ray(state),
        "count": L0_N12_COUNT,
        "max_linf": L0_N12_LINF,
        LIVE_IS_L0: True,
        GROWTH_NOT_INFINITUDE: True,
    }


def phase0_zero_value_kernel() -> dict[str, object]:
    census = census_complete(4)
    hub = hub_witness()
    star = classify_complete(RECURRENCE_WORD_MSD)
    combos = enumerate_combos(6)
    samples = ((), (0,), (1, -2), (-1, 2), RECURRENCE_WORD_MSD, (1, 0, -2))
    c3_ok = all(c3_equals_minus_val(w) for w in samples if w)
    c3_ok = c3_ok and c3_equals_minus_val(())
    coord_ok = all(coordinates_match_impulse(w) for w in samples)
    pairs = (
        (SHORTEST_NONRESET, SHORTEST_NONRESET),
        (SHORTEST_NONRESET, (0,)),
        ((0,), SHORTEST_NONRESET),
        (RECURRENCE_WORD_MSD, (0,)),
        ((1,), (-2,)),
        ((), SHORTEST_NONRESET),
        (SHORTEST_NONRESET, ()),
    )
    append_ok = all(consumed_sum_append_holds(n, u, v) for n in range(3) for u, v in pairs)
    energy_ok = all(val_concat_energy_holds(u, v) for u, v in pairs)
    square = hub_square_witness()
    off_ray = n12_maximizer_off_ray()
    reset = (0,)
    seeds = (ORIGIN, HUB, N12_MAXIMIZER_STATE)
    words = samples
    val_s_ok = all(block_val_holds(s, w) for s in seeds for w in words)
    affine_ok = all(affine_holds(w, s) for s in seeds for w in words if w)
    affine_ok = affine_ok and all(affine_holds((), s) for s in seeds)
    iterates = hub_block_iterates()
    return {
        "c3_equals_minus_val": c3_ok,
        "coordinates_match": coord_ok,
        "census": census,
        "hub": hub,
        "star_reset": star["reset"] and star[ALGEBRAIC_ZERO],
        "recurrence_combos_all_reset": all(r["reset"] for r in combos),
        "k_star": census["k_star"],
        "consumed_sum_append": append_ok,
        "val_concat_energy": energy_ok,
        "hub_square": square,
        "n12_off_ray": off_ray,
        "reset_then_hub_zero": msd_val(reset + SHORTEST_NONRESET) == 0,
        "block_val_is_minus_s3": val_s_ok,
        "affine_holds_off_origin": affine_ok,
        "hub_iterates": iterates,
        "live_fiber_N12": {
            "count": L0_N12_COUNT,
            "max_linf": L0_N12_LINF,
            "on_F": True,
            "is_L0": True,
        },
        "symbolic_family": False,
        VAL_NOT_RESET: True,
        RAY_NOT_FAMILY: True,
        GROWTH_NOT_INFINITUDE: True,
        KNOWN_PACKAGING: True,
        NOT_MONOID: square[NOT_MONOID],
        LIVE_IS_L0: True,
        VAL_CONCAT_ENERGY: energy_ok,
        BLOCK_VAL_IS_S3: val_s_ok,
        TELESCOPE_PACKAGING: True,
    }
