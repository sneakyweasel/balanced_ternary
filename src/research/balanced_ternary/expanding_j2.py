"""Two-digit integer jet of expanding ``T`` on existing BT operators.

``J₂(n) = integer_jet(n, 2) = (lsd(n), lsd(D(n)))``. This is not a new
digit model. Canonical ``T`` acts by ``(a, b) ↦ (-a, a)``; the second
digit is emitted at time 0 and then discarded.
"""

from __future__ import annotations

from collections import defaultdict

from bt.calculus.jets import integer_jet
from bt.operators import lsd_digit
from research.balanced_ternary.expanding_d import (
    TRITS,
    expanding_d,
    residue_step,
    sample_range,
)

Jet2 = tuple[int, int]
JET2_STATES: tuple[Jet2, ...] = tuple((a, b) for a in TRITS for b in TRITS)


def j2(n: int) -> Jet2:
    """Existing length-2 integer jet."""
    pair = integer_jet(n, 2)
    return (pair[0], pair[1])


def j2_transition(jet: Jet2, gain: int = 1) -> Jet2:
    """Exact ``J₂(T_λ(n))`` from the first digit alone.

    ``T_λ(n)=3n-λ a`` and ``r'=lsd(-λ a)`` give
    ``DZ(T_λ)=(3n-λ a-r')/3 = n-(λ a+r')/3``, so the next second
    digit is ``lsd(a - (λ a+r')/3)`` and does not use ``b`` or ``D²(n)``.
    """
    a, _b = jet
    if a not in TRITS:
        raise ValueError(f"jet digits must be trits, got {jet}")
    nxt_lsd = residue_step(a, gain)
    shift = (gain * a + nxt_lsd) // 3
    return (nxt_lsd, lsd_digit(a - shift))


def j2_section(jet: Jet2, digit: int) -> Jet2:
    """``J₂(I_c(n)) = (c, lsd(n))``. The old second digit is dropped."""
    a, _b = jet
    if digit not in TRITS:
        raise ValueError(f"section trit must be a trit, got {digit}")
    return (digit, a)


def j2_orbit(n: int, length: int, gain: int = 1) -> tuple[Jet2, ...]:
    current = n
    out: list[Jet2] = []
    for _ in range(length):
        out.append(j2(current))
        current = expanding_d(current, gain)
    return tuple(out)


def predicted_j2_orbit(n: int, length: int, gain: int = 1) -> tuple[Jet2, ...]:
    jet = j2(n)
    out: list[Jet2] = []
    for _ in range(length):
        out.append(jet)
        jet = j2_transition(jet, gain)
    return tuple(out)


def t_image(gain: int = 1) -> frozenset[Jet2]:
    return frozenset(j2_transition(jet, gain) for jet in JET2_STATES)


def observational_j2_classes(
    values: tuple[int, ...],
    length: int,
    gain: int = 1,
) -> dict[tuple[Jet2, ...], tuple[int, ...]]:
    buckets: dict[tuple[Jet2, ...], list[int]] = defaultdict(list)
    for n in values:
        buckets[j2_orbit(n, length, gain)].append(n)
    return {sig: tuple(group) for sig, group in buckets.items()}


def third_digit_separates(
    values: tuple[int, ...],
    length: int,
    gain: int = 1,
) -> tuple[int, int] | None:
    """Same ``J₂``, different ``lsd(D²)``, different future ``J₂`` stream."""
    by_jet: dict[Jet2, list[int]] = defaultdict(list)
    for n in values:
        by_jet[j2(n)].append(n)
    for group in by_jet.values():
        if len(group) < 2:
            continue
        first = group[0]
        first_sig = j2_orbit(first, length, gain)
        first_third = integer_jet(first, 3)[2]
        for other in group[1:]:
            if integer_jet(other, 3)[2] == first_third:
                continue
            if j2_orbit(other, length, gain) != first_sig:
                return first, other
    return None


def second_digit_affects_next_j2(
    values: tuple[int, ...],
    gain: int = 1,
) -> tuple[int, int] | None:
    """Witness that ``J₂(T(n))`` depends on the second digit, if any."""
    by_lsd: dict[int, list[int]] = defaultdict(list)
    for n in values:
        by_lsd[j2(n)[0]].append(n)
    for group in by_lsd.values():
        nxt = {j2(expanding_d(n, gain)) for n in group}
        if len(nxt) > 1:
            first = group[0]
            other = next(m for m in group if j2(expanding_d(m, gain)) != j2(expanding_d(first, gain)))
            return first, other
    return None


def discovery_report(
    limit: int = 40,
    length: int = 8,
    gain: int = 1,
) -> dict[str, object]:
    """Bounded ``J₂`` reconnaissance. Not an exact theorem."""
    values = sample_range(limit)
    classes = observational_j2_classes(values, length, gain)
    predicted_ok = all(
        j2_orbit(n, length, gain) == predicted_j2_orbit(n, length, gain) for n in values
    )
    live_j2 = {j2(n) for n in values}
    return {
        "scope": "BOUNDED",
        "status": "OBSERVATION",
        "sample_limit": limit,
        "orbit_length": length,
        "class_count": len(classes),
        "observed_j2_count": len(live_j2),
        "raw_j2_count": len(JET2_STATES),
        "predicted_matches_sample": predicted_ok,
        "third_digit_separates": third_digit_separates(values, length, gain),
        "second_digit_affects_next": second_digit_affects_next_j2(values, gain),
        "t_image": tuple(sorted(t_image(gain))),
        "same_j2_different_third": (1, 10),
        "same_lsd_different_j2": (1, 4),
    }
