"""Place-value recurrence as a W-valued zero-sum block.

The unique length-4 consecutive relation is a multiple of
``(3, 1, 2, -1)``. The W-valued sign is LSD ``(-3, -1, -2, 1)``, MSD

    B* = (1, -2, -1, -3)

with ``val(B*) = q_{n+3} - 2 q_{n+2} - q_{n+1} - 3 q_n = 0``.
Last letter ``-3`` is interior-legal and not LSD. Algebraic zero-sum
is not fully live. A reset is not an expanding family.

The complete words ``U_k = (B*)^k · (1,-2)`` are live at remaining
``4k+2`` and all land on the hub. Arbitrarily long accepted words
do not force infinitely many terminals. Finite-horizon iteration is
not ``|L_0|=∞``.

Length 5–6 words are shift-combinations of the recurrence (lattice
points in ``W^L``), not a ``7^L`` census.
"""

from __future__ import annotations

from itertools import product

from research.ostrowski.control_language import affine_block
from research.ostrowski.energy_trajectory import apply_word, consumed_sum
from research.ostrowski.exceptional_kernel import W_INTERIOR, W_LSD
from research.ostrowski.live_growth import legal_w, residual_is_live
from research.ostrowski.live_layers import ORIGIN, linf
from research.ostrowski.nonpisot_search import HUB
from research.ostrowski.spectral_control import control_convolution
from research.ostrowski.spectral_residual import transition_affine
from research.ostrowski.system import nonpisot_order3

State3 = tuple[int, int, int]

GENERATOR: tuple[int, ...] = (3, 1, 2, -1)
RECURRENCE_WORD_MSD: tuple[int, ...] = (1, -2, -1, -3)
RECURRENCE_WORD_LSD: tuple[int, ...] = (-3, -1, -2, 1)
HUB_WORD: tuple[int, ...] = (1, -2)

ALGEBRAIC_ZERO = "algebraic_zero_sum"
PREFIX_LEGAL = "prefix_legal"
FULLY_LIVE = "fully_live"
RESET_NOT_FAMILY = "reset_is_not_expanding_family"
GROWTH_NOT_INFINITUDE = "finite_depth_is_not_infinitude"
KNOWN_PACKAGING = "val_is_q_rec"
LSD_NOT_INTERIOR = "lsd_alphabet_only_at_remaining_1"
LONG_WORDS_NOT_INFINITUDE = "arbitrarily_long_accepted_words_do_not_force_infinite_L0"


def _sys():
    return nonpisot_order3()


def msd_val(word: tuple[int, ...], start_remaining: int) -> int:
    """MSD weighted Ostrowski value. Equals ``consumed_sum``."""
    return consumed_sum(_sys(), start_remaining, word)


def val_equals_minus_s3(word: tuple[int, ...]) -> bool:
    """Complete word from remaining ``|word|``: ``s3 = -val``."""
    state = apply_word(_sys(), ORIGIN, word)
    return state[2] == -msd_val(word, len(word))


def convolution_matches_c_b(word: tuple[int, ...]) -> bool:
    return control_convolution(word) == apply_word(_sys(), ORIGIN, word)


def lsd_to_msd(lsd: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(reversed(lsd))


def in_w(digits: tuple[int, ...]) -> bool:
    return all(d in W_INTERIOR for d in digits)


def pad_shift(gen: tuple[int, ...], length: int, offset: int) -> tuple[int, ...]:
    row = [0] * length
    for i, c in enumerate(gen):
        row[offset + i] = c
    return tuple(row)


def combo_digits(length: int, coeffs: tuple[int, ...]) -> tuple[int, ...]:
    """``sum_i coeffs[i] * shift_i(GENERATOR)`` as an LSD consecutive vector."""
    acc = [0] * length
    width = len(GENERATOR)
    n_shifts = length - width + 1
    if len(coeffs) != n_shifts:
        raise ValueError("coeff count must equal number of shifts")
    for offset, a in enumerate(coeffs):
        sh = pad_shift(GENERATOR, length, offset)
        for i, c in enumerate(sh):
            acc[i] += a * c
    return tuple(acc)


def lattice_words(length: int, coeff_range: range = range(-4, 5)) -> list[tuple[int, ...]]:
    """W-valued MSD words from small integer combinations of recurrence shifts."""
    n_shifts = length - len(GENERATOR) + 1
    if n_shifts < 1:
        return []
    found: dict[tuple[int, ...], tuple[int, ...]] = {}
    for coeffs in product(coeff_range, repeat=n_shifts):
        if all(c == 0 for c in coeffs):
            continue
        lsd = combo_digits(length, coeffs)
        if not in_w(lsd):
            continue
        msd = lsd_to_msd(lsd)
        found.setdefault(msd, coeffs)
    return sorted(found)


def recurrence_word_val_zero(n: int = 0) -> bool:
    """``val(B*) = 0`` at start remaining ``n+4``."""
    return msd_val(RECURRENCE_WORD_MSD, n + 4) == 0


def prefix_legal(word: tuple[int, ...], start_remaining: int) -> bool:
    sys = _sys()
    remaining = start_remaining
    for w in word:
        if remaining < 1:
            return False
        if w not in legal_w(sys, remaining - 1):
            return False
        remaining -= 1
    return True


def fully_live(word: tuple[int, ...], start_remaining: int) -> bool:
    """Every prefix residual is live. Not infinitude."""
    sys = _sys()
    if not prefix_legal(word, start_remaining):
        return False
    state = ORIGIN
    remaining = start_remaining
    if not residual_is_live(sys, state, remaining):
        return False
    for w in word:
        state = transition_affine(sys, state, w)
        remaining -= 1
        if not residual_is_live(sys, state, remaining):
            return False
    return True


def iterate_block(
    word: tuple[int, ...],
    repeats: int,
    start_remaining: int,
) -> dict[str, object]:
    sys = _sys()
    state = ORIGIN
    remaining = start_remaining
    live_all = residual_is_live(sys, state, remaining)
    max_l = 0
    grew = False
    for _ in range(repeats):
        if remaining < len(word):
            live_all = False
            break
        if not prefix_legal(word, remaining):
            live_all = False
            break
        for w in word:
            state = transition_affine(sys, state, w)
            remaining -= 1
            if not residual_is_live(sys, state, remaining):
                live_all = False
        nrm = linf(state)
        if nrm > max_l:
            max_l = nrm
    final_linf = linf(state)
    return {
        "final": state,
        "remaining": remaining,
        "max_linf": max(max_l, final_linf),
        "grew": live_all and final_linf > 0,
        "live_all": live_all,
        GROWTH_NOT_INFINITUDE: True,
    }


def classify_word(word: tuple[int, ...]) -> dict[str, object]:
    """Three labels: algebraic zero-sum / prefix-legal / fully live."""
    length = len(word)
    vals = [msd_val(word, length + n) for n in range(5)]
    algebraic = all(v == 0 for v in vals)
    interior = all(d in W_INTERIOR for d in word)
    lsd_complete = interior and word[-1] in W_LSD if word else True
    start_interior = max(length + 2, 8)
    prefix_int = prefix_legal(word, start_interior)
    live_int = fully_live(word, start_interior)
    prefix_complete = prefix_legal(word, length)
    live_complete = fully_live(word, length)
    c_b = apply_word(_sys(), ORIGIN, word)
    reset = c_b == ORIGIN
    affine = affine_block(word)
    conv_ok = control_convolution(word) == c_b
    repeats = 4
    start_iter = repeats * length + 2
    iteration = iterate_block(word, repeats, start_iter)
    candidate = (
        algebraic
        and live_int
        and not reset
        and iteration["live_all"]
        and iteration["grew"]
    )
    return {
        "word": word,
        "length": length,
        "vals": vals,
        ALGEBRAIC_ZERO: algebraic,
        "interior_legal": interior,
        "lsd_legal_complete": lsd_complete,
        PREFIX_LEGAL: prefix_int,
        FULLY_LIVE: live_int,
        "prefix_legal_complete": prefix_complete,
        "fully_live_complete": live_complete,
        "c_B": c_b,
        "reset": reset,
        "A_k": affine["A_k"],
        "convolution_ok": conv_ok,
        "iteration": iteration,
        "candidate_expander": candidate,
        RESET_NOT_FAMILY: True,
        LSD_NOT_INTERIOR: True,
        GROWTH_NOT_INFINITUDE: True,
        KNOWN_PACKAGING: True,
    }


def enumerate_combos(max_length: int = 6) -> list[dict[str, object]]:
    rows = []
    seen: set[tuple[int, ...]] = set()
    for length in range(4, max_length + 1):
        for word in lattice_words(length):
            if word in seen:
                continue
            seen.add(word)
            rows.append(classify_word(word))
    return rows


def phase0_recurrence_zero() -> dict[str, object]:
    star = classify_word(RECURRENCE_WORD_MSD)
    combos = enumerate_combos(6)
    resets = [r for r in combos if r["reset"]]
    live_int = [r for r in combos if r[FULLY_LIVE]]
    lsd_ok = [r for r in combos if r["lsd_legal_complete"]]
    live_complete = [r for r in combos if r["fully_live_complete"]]
    expanders = [r for r in combos if r["candidate_expander"]]
    iterate_live = [
        r for r in combos if r["iteration"]["live_all"] and not r["reset"]
    ]
    val_ok = all(recurrence_word_val_zero(n) for n in range(6))
    s3_ok = val_equals_minus_s3(RECURRENCE_WORD_MSD)
    conv_ok = convolution_matches_c_b(RECURRENCE_WORD_MSD)
    return {
        "star": star,
        "n_combos": len(combos),
        "n_reset": len(resets),
        "n_interior_live": len(live_int),
        "n_lsd_complete": len(lsd_ok),
        "n_fully_live_complete": len(live_complete),
        "n_iterate_live_nonreset": len(iterate_live),
        "expanders": [r["word"] for r in expanders],
        "symbolic_family": False,
        "val_star_zero": val_ok,
        "val_equals_minus_s3": s3_ok,
        "convolution_ok": conv_ok,
        "combos": combos,
        RESET_NOT_FAMILY: True,
        GROWTH_NOT_INFINITUDE: True,
        KNOWN_PACKAGING: True,
        LSD_NOT_INTERIOR: True,
    }


def reset_pow_then_hub_word(k: int) -> tuple[int, ...]:
    """MSD word ``(B*)^k · (1,-2)``. Not a monoid of complete words."""
    if k < 0:
        raise ValueError("k must be nonnegative")
    return RECURRENCE_WORD_MSD * k + HUB_WORD


def classify_reset_pow_then_hub(k: int) -> dict[str, object]:
    """Complete live word of length ``4k+2`` landing on the hub.

    Algebraic image is Lean ``reset_pow_then_hub``. Liveness is Python.
    Distinct lengths with one terminal are not ``|L_0|=∞``.
    """
    word = reset_pow_then_hub_word(k)
    sys = _sys()
    start = len(word)
    reset_states: list[State3] = []
    state = ORIGIN
    for _ in range(k):
        state = apply_word(sys, state, RECURRENCE_WORD_MSD)
        reset_states.append(state)
    terminal = apply_word(sys, ORIGIN, word)
    return {
        "k": k,
        "word": word,
        "length": start,
        "terminal": terminal,
        "terminal_is_hub": terminal == HUB,
        "last_lsd": word[-1] in W_LSD,
        "prefix_legal": prefix_legal(word, start),
        "fully_live": fully_live(word, start),
        "reset_prefixes_origin": all(s == ORIGIN for s in reset_states),
        "convolution_ok": control_convolution(word) == terminal,
        LONG_WORDS_NOT_INFINITUDE: True,
        GROWTH_NOT_INFINITUDE: True,
        RESET_NOT_FAMILY: True,
        LSD_NOT_INTERIOR: True,
        KNOWN_PACKAGING: True,
    }


def phase0_reset_pow_then_hub(max_k: int = 4) -> dict[str, object]:
    """``U_k`` for ``k=0..max_k`` share the hub. Not infinitude of ``L_0``."""
    rows = [classify_reset_pow_then_hub(k) for k in range(max_k + 1)]
    terminals = {row["terminal"] for row in rows}
    lengths = {row["length"] for row in rows}
    return {
        "rows": rows,
        "n_k": len(rows),
        "n_lengths": len(lengths),
        "terminals": tuple(sorted(terminals)),
        "one_terminal": terminals == {HUB},
        "all_live_complete": all(bool(row["fully_live"]) for row in rows),
        "all_last_lsd": all(bool(row["last_lsd"]) for row in rows),
        "all_reset_prefixes_origin": all(
            bool(row["reset_prefixes_origin"]) for row in rows
        ),
        LONG_WORDS_NOT_INFINITUDE: True,
        GROWTH_NOT_INFINITUDE: True,
        RESET_NOT_FAMILY: True,
        KNOWN_PACKAGING: True,
    }
