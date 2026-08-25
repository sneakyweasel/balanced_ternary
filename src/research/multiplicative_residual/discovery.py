"""Exact product-control residual of ``λ·D(s+h(c))``.

The step reuses ``signed_step``. Product of trits is ordinary integer
multiplication, already the local factor in ``lsd(xy)=lsd(x)lsd(y)``.
This is not a multiplication engine.
"""

from __future__ import annotations

from collections.abc import Sequence

from bt.transducers.mealy import minimize_mealy_count
from research.signed_digit_residual.discovery import (
    TRITS,
    is_constant_unbounded_family,
    reachable_from,
    signed_step,
)

Pair = tuple[int, int]
Triple = tuple[int, int, int]


def pair_controls() -> tuple[Pair, ...]:
    return tuple((a, b) for a in TRITS for b in TRITS)


def triple_controls() -> tuple[Triple, ...]:
    return tuple((a, b, c) for a in TRITS for b in TRITS for c in TRITS)


def product_raw(digits: Sequence[int]) -> int:
    acc = 1
    for digit in digits:
        acc *= digit
    return acc


def product_step(
    state: int,
    digits: Sequence[int],
    gain: int = 1,
    scale: int = 1,
) -> tuple[int, int]:
    """``s' = λ·D(s + scale·∏ d_i)``. Scale ``2`` is the doubled-trit coefficient."""
    return signed_step(state, scale * product_raw(digits), gain)


def raw_image(controls: Sequence[Sequence[int]], scale: int = 1) -> frozenset[int]:
    return frozenset(scale * product_raw(ctrl) for ctrl in controls)


def raw_fibers(
    controls: Sequence[Sequence[int]],
    scale: int = 1,
) -> dict[int, tuple[tuple[int, ...], ...]]:
    buckets: dict[int, list[tuple[int, ...]]] = {}
    for ctrl in controls:
        key = scale * product_raw(ctrl)
        buckets.setdefault(key, []).append(tuple(ctrl))
    return {key: tuple(values) for key, values in sorted(buckets.items())}


def separator_equal_raw(
    controls: Sequence[Sequence[int]],
    gain: int = 1,
    scale: int = 1,
    states: Sequence[int] = range(-4, 5),
) -> tuple[tuple[int, ...], tuple[int, ...], int] | None:
    """Equal raw contribution but different ``(s', out)``. None means no witness."""
    ctrls = [tuple(ctrl) for ctrl in controls]
    for i, left in enumerate(ctrls):
        for right in ctrls[i + 1 :]:
            if scale * product_raw(left) != scale * product_raw(right):
                continue
            for state in states:
                if product_step(state, left, gain, scale) != product_step(
                    state, right, gain, scale
                ):
                    return left, right, int(state)
    return None


def reachable_product(
    controls: Sequence[Sequence[int]],
    gain: int = 1,
    scale: int = 1,
    cap: int = 256,
) -> frozenset[int] | None:
    alphabet = tuple(scale * product_raw(ctrl) for ctrl in controls)
    return reachable_from(0, alphabet, gain, cap=cap)


def mealy_count_product(
    states: Sequence[int],
    controls: Sequence[Sequence[int]],
    gain: int = 1,
    scale: int = 1,
) -> int:
    ctrls = tuple(tuple(ctrl) for ctrl in controls)

    def mealy(state: int, control: Sequence[int]) -> tuple[int, int]:
        return product_step(state, control, gain, scale)

    return minimize_mealy_count(states, ctrls, mealy)


def control_output_classes(
    state: int,
    controls: Sequence[Sequence[int]],
    gain: int = 1,
    scale: int = 1,
) -> int:
    """Number of distinct one-step output signatures at a fixed residual."""
    signatures = {
        product_step(state, ctrl, gain, scale)[1] for ctrl in controls
    }
    return len(signatures)


def two_trit_report(gain: int = 1) -> dict[str, object]:
    controls = pair_controls()
    image = raw_image(controls)
    reached = reachable_product(controls, gain)
    assert reached is not None
    states = tuple(sorted(reached))
    u1 = reachable_from(0, TRITS, gain)
    return {
        "gain": gain,
        "raw_controls": 9,
        "raw_contributions": tuple(sorted(image)),
        "raw_contribution_count": len(image),
        "fibers": {key: value for key, value in raw_fibers(controls).items()},
        "reachable": states,
        "reachable_count": len(states),
        "mealy": mealy_count_product(states, controls, gain),
        "control_output_classes_at_0": control_output_classes(0, controls, gain),
        "u1_reachable": tuple(sorted(u1)) if u1 is not None else None,
        "separator": separator_equal_raw(controls, gain),
        "factors_through_raw": True,
        "classification": "EXACT FINITE",
    }


def three_trit_report(gain: int = 1) -> dict[str, object]:
    controls = triple_controls()
    image = raw_image(controls)
    reached = reachable_product(controls, gain)
    assert reached is not None
    two = two_trit_report(gain)
    return {
        "gain": gain,
        "raw_controls": 27,
        "raw_contributions": tuple(sorted(image)),
        "reachable": tuple(sorted(reached)),
        "mealy": mealy_count_product(tuple(sorted(reached)), controls, gain),
        "matches_two_trit_reachable": tuple(sorted(reached)) == two["reachable"],
        "separator": separator_equal_raw(controls, gain),
    }


def doubled_product_report(gain: int = 1) -> dict[str, object]:
    """Perturbation: ``u=2 d1 d2``, the existing doubled-trit coefficient."""
    controls = pair_controls()
    image = raw_image(controls, scale=2)
    reached = reachable_product(controls, gain, scale=2)
    infinite = gain == 3 and is_constant_unbounded_family(2, 3)
    classification = "EXACT INFINITE" if infinite else (
        "EXACT FINITE" if reached is not None else "OBSERVATION"
    )
    states = tuple(sorted(reached)) if reached is not None else None
    return {
        "gain": gain,
        "raw_contributions": tuple(sorted(image)),
        "reachable": states,
        "mealy": None if states is None else mealy_count_product(states, controls, gain, scale=2),
        "unbounded_witness": infinite,
        "classification": classification,
        "separator": separator_equal_raw(controls, gain, scale=2),
    }


def universality_fingerprint() -> dict[str, object]:
    two = {gain: two_trit_report(gain) for gain in (1, 2, 3)}
    three = {gain: three_trit_report(gain) for gain in (1, 2, 3)}
    doubled = {gain: doubled_product_report(gain) for gain in (1, 2, 3)}
    return {
        "two_trit": two,
        "three_trit": three,
        "doubled_product": doubled,
        "universality": all(
            two[gain]["reachable"] == three[gain]["reachable"]
            and two[gain]["separator"] is None
            and three[gain]["separator"] is None
            for gain in (1, 2, 3)
        ),
    }
