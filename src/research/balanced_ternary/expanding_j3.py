"""Three-digit integer jet of expanding ``T`` on existing BT operators.

``J₃(n) = integer_jet(n, 3)``. Canonical ``T`` acts by the shift

    (a, b, c) ↦ (-a, a, b)

which is ``(-lsd(n))`` concatenated with ``J₂(n)``. The third digit is
emitted at time 0 and then discarded. The second digit survives.
"""

from __future__ import annotations

from collections import defaultdict

from bt.calculus.jets import integer_jet
from research.balanced_ternary.expanding_d import TRITS, expanding_d, sample_range
from research.balanced_ternary.expanding_j2 import j2_transition

Jet3 = tuple[int, int, int]
JET3_STATES: tuple[Jet3, ...] = tuple(
    (a, b, c) for a in TRITS for b in TRITS for c in TRITS
)


def j3(n: int) -> Jet3:
    """Existing length-3 integer jet, LSD-first."""
    trip = integer_jet(n, 3)
    return (trip[0], trip[1], trip[2])


def j3_transition(jet: Jet3, gain: int = 1) -> Jet3:
    """Exact ``J₃(T_λ(n))`` from ``J₂`` alone: prefix ``J₂(T_λ)`` plus ``b``.

    Canonical ``λ = 1`` is ``(-a, a, b)``. The input ``c`` is unused.
    """
    a, b, _c = jet
    if a not in TRITS or b not in TRITS:
        raise ValueError(f"jet digits must be trits, got {jet}")
    prefix = j2_transition((a, b), gain)
    return (prefix[0], prefix[1], b)


def j3_section(jet: Jet3, digit: int) -> Jet3:
    """``J₃(I_d(n)) = (d, lsd(n), lsd(D(n)))``. The old third digit is dropped."""
    a, b, _c = jet
    if digit not in TRITS:
        raise ValueError(f"section trit must be a trit, got {digit}")
    return (digit, a, b)


def j3_from_j2(jet2: tuple[int, int], gain: int = 1) -> Jet3:
    """Factorization ``J₃ ∘ T_λ = F_λ ∘ J₂``."""
    a, b = jet2
    return j3_transition((a, b, 0), gain)


def j3_orbit(n: int, length: int, gain: int = 1) -> tuple[Jet3, ...]:
    current = n
    out: list[Jet3] = []
    for _ in range(length):
        out.append(j3(current))
        current = expanding_d(current, gain)
    return tuple(out)


def predicted_j3_orbit(n: int, length: int, gain: int = 1) -> tuple[Jet3, ...]:
    jet = j3(n)
    out: list[Jet3] = []
    for _ in range(length):
        out.append(jet)
        jet = j3_transition(jet, gain)
    return tuple(out)


def t_image(gain: int = 1) -> frozenset[Jet3]:
    return frozenset(j3_transition(jet, gain) for jet in JET3_STATES)


def j1_insufficient_witness(
    values: tuple[int, ...],
    gain: int = 1,
) -> tuple[int, int] | None:
    """Same ``lsd``, different ``J₃(T(n))``."""
    by_lsd: dict[int, list[int]] = defaultdict(list)
    for n in values:
        by_lsd[j3(n)[0]].append(n)
    for group in by_lsd.values():
        nxt = {j3(expanding_d(n, gain)) for n in group}
        if len(nxt) > 1:
            first = group[0]
            other = next(
                m for m in group if j3(expanding_d(m, gain)) != j3(expanding_d(first, gain))
            )
            return first, other
    return None


def j2_insufficient_for_next(
    values: tuple[int, ...],
    gain: int = 1,
) -> tuple[int, int] | None:
    """Same ``J₂``, different ``J₃(T(n))`` — would refute factorization through ``J₂``."""
    by_j2: dict[tuple[int, int], list[int]] = defaultdict(list)
    for n in values:
        jet = j3(n)
        by_j2[(jet[0], jet[1])].append(n)
    for group in by_j2.values():
        nxt = {j3(expanding_d(n, gain)) for n in group}
        if len(nxt) > 1:
            first = group[0]
            other = next(
                m for m in group if j3(expanding_d(m, gain)) != j3(expanding_d(first, gain))
            )
            return first, other
    return None


def third_digit_affects_next(
    values: tuple[int, ...],
    gain: int = 1,
) -> tuple[int, int] | None:
    """Same ``J₂``, different third digit, different ``J₃(T(n))``."""
    return j2_insufficient_for_next(values, gain)


def discovery_report(
    limit: int = 80,
    length: int = 6,
    gain: int = 1,
) -> dict[str, object]:
    """Bounded ``J₃`` reconnaissance. Not an exact theorem."""
    values = sample_range(limit)
    predicted_ok = all(
        j3_orbit(n, length, gain) == predicted_j3_orbit(n, length, gain) for n in values
    )
    live = {j3(n) for n in values}
    return {
        "scope": "BOUNDED",
        "status": "OBSERVATION",
        "sample_limit": limit,
        "orbit_length": length,
        "observed_j3_count": len(live),
        "raw_j3_count": len(JET3_STATES),
        "predicted_matches_sample": predicted_ok,
        "j1_insufficient": j1_insufficient_witness(values, gain),
        "j2_insufficient_for_next": j2_insufficient_for_next(values, gain),
        "t_image": tuple(sorted(t_image(gain))),
        "same_j2_different_j3": (1, 10),
        "same_j1_different_j2": (1, 4),
    }
