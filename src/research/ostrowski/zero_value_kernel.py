"""Zero-value complete words need not reset.

``val(B)=consumed_sum(|B|,B)``. From the origin ``c_B=T_B(0)`` and
``(c_B)_3=-val(B)``. So ``val=0`` iff ``c_B`` lies on ``F={s_3=0}``.
That does not force ``c_B=0``.

The shortest complete non-reset is ``(1,-2)``, with
``c_B=(-3,-1,0)`` (the known ``F→F`` hub). Recurrence combos that
are identically zero for every alignment remain the reset sublattice.
A point of ``F`` is not ``|L_0|=∞``. The bounded two-step ray is not
a family.
"""

from __future__ import annotations

from itertools import product

from research.ostrowski.energy_trajectory import apply_word, consumed_sum
from research.ostrowski.exceptional_kernel import W_INTERIOR, W_LSD
from research.ostrowski.live_layers import ORIGIN, linf
from research.ostrowski.origin_live import two_step_f_to_f
from research.ostrowski.recurrence_zero import (
    RECURRENCE_WORD_MSD,
    enumerate_combos,
    fully_live,
    prefix_legal,
)
from research.ostrowski.spectral_control import control_convolution, ostrowski_s1, ostrowski_s3
from research.ostrowski.system import nonpisot_order3

State3 = tuple[int, int, int]

HUB: State3 = (-3, -1, 0)
SHORTEST_NONRESET: tuple[int, ...] = (1, -2)
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


def phase0_zero_value_kernel() -> dict[str, object]:
    census = census_complete(4)
    hub = hub_witness()
    star = classify_complete(RECURRENCE_WORD_MSD)
    combos = enumerate_combos(6)
    samples = ((), (0,), (1, -2), (-1, 2), RECURRENCE_WORD_MSD, (1, 0, -2))
    c3_ok = all(c3_equals_minus_val(w) for w in samples if w)
    c3_ok = c3_ok and c3_equals_minus_val(())
    coord_ok = all(coordinates_match_impulse(w) for w in samples)
    return {
        "c3_equals_minus_val": c3_ok,
        "coordinates_match": coord_ok,
        "census": census,
        "hub": hub,
        "star_reset": star["reset"] and star[ALGEBRAIC_ZERO],
        "recurrence_combos_all_reset": all(r["reset"] for r in combos),
        "k_star": census["k_star"],
        "live_fiber_N12": {
            "count": L0_N12_COUNT,
            "max_linf": L0_N12_LINF,
            "on_F": True,
        },
        "symbolic_family": False,
        VAL_NOT_RESET: True,
        RAY_NOT_FAMILY: True,
        GROWTH_NOT_INFINITUDE: True,
        KNOWN_PACKAGING: True,
    }
