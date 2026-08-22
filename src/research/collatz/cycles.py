"""Exact periodic exponent codes for the accelerated Collatz map.

A word is an *algebraic candidate* when ``D = 2^K - 3^p > 0`` and
``n = C / D`` is a positive rational. It is *integral* when that rational
is a positive odd integer. It is an *exact cycle* only when the actual
accelerated valuations match the word, the orbit closes, and the word is
primitive.

The affine identity ``n(2^K - 3^p) = C`` is **not new**; it is the existing
periodic fixed-point formula. Affine closure is kept separate from the
valuation-matching test.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from balanced_ternary.representation import encode
from research.collatz.amplitude import CycleAmplitude, cycle_amplitude
from research.collatz.core import collatz_step, collatz_valuation, require_positive_odd
from research.collatz.cycle_codes import (
    exponent_root,
    is_primitive,
    lex_min_rotation,
    rotation_index_of_canonical,
    rotations,
)
from research.collatz.cylinders import belongs_to_cylinder, parse_ks
from research.collatz.itinerary import ValuationItinerary
from research.collatz.min_realizer import min_realizer
from research.collatz.zero_lift import lift_digits


@dataclass(frozen=True)
class PeriodicExponentCode:
    """Exact snapshot of one finite exponent word as a cycle candidate."""

    code: tuple[int, ...]
    primitive_period: tuple[int, ...]
    p: int
    K: int
    C: int
    denominator: int
    candidate_n: Fraction | None
    candidate_states: tuple[int, ...] | None
    is_primitive: bool
    is_contracting: bool
    is_integral: bool
    is_positive: bool
    valuations_match: bool
    is_exact_period: bool
    is_exact_cycle: bool
    amplitude: CycleAmplitude | None
    min_realizer: int
    lift_digits: tuple[int, ...]
    canonical_code: tuple[int, ...]
    rotation_index: int
    status: str
    reason: str

    def as_dict(self) -> dict[str, object]:
        n = self.candidate_n
        amp = None if self.amplitude is None else self.amplitude.as_dict()
        return {
            "code": list(self.code),
            "primitive_period": list(self.primitive_period),
            "p": self.p,
            "K": self.K,
            "C": self.C,
            "denominator": self.denominator,
            "candidate_n": None if n is None else [n.numerator, n.denominator],
            "candidate_states": (
                None if self.candidate_states is None else list(self.candidate_states)
            ),
            "is_primitive": self.is_primitive,
            "is_contracting": self.is_contracting,
            "is_integral": self.is_integral,
            "is_positive": self.is_positive,
            "valuations_match": self.valuations_match,
            "is_exact_period": self.is_exact_period,
            "is_exact_cycle": self.is_exact_cycle,
            "amplitude": amp,
            "min_realizer": self.min_realizer,
            "lift_digits": list(self.lift_digits),
            "canonical_code": list(self.canonical_code),
            "rotation_index": self.rotation_index,
            "status": self.status,
            "reason": self.reason,
        }


def _algebraic_candidate(it: ValuationItinerary) -> tuple[Fraction | None, str]:
    D = it.denominator - it.numerator_multiplier
    if D < 0:
        return None, "expanding: C/(2^K-3^p) is negative"
    if D == 0:
        return None, "2^K = 3^p is impossible for p >= 1"
    return Fraction(it.C, D), "algebraic candidate C/D"


def _iterate_if_integral(n: int, code: tuple[int, ...]) -> tuple[tuple[int, ...], bool, bool]:
    """Return states, valuation-match flag, and exact p-step closure."""
    states = [n]
    x = n
    match = True
    for k in code:
        actual = collatz_valuation(x)
        if actual != k:
            match = False
        x = collatz_step(x)
        states.append(x)
    closed = states[-1] == n
    return tuple(states[:-1]), match, closed


def candidate_cycle(code: tuple[int, ...] | str | list[int]) -> PeriodicExponentCode:
    """Exact cycle diagnostics for one nonempty exponent word."""
    ks = parse_ks(code)
    if not ks:
        raise ValueError("a periodic exponent code must be nonempty")
    it = ValuationItinerary.from_ks(ks)
    D = it.denominator - it.numerator_multiplier
    primitive = is_primitive(ks)
    root = exponent_root(ks)
    candidate, reason = _algebraic_candidate(it)
    contracting = D > 0
    integral = False
    positive = False
    states: tuple[int, ...] | None = None
    match = False
    closed = False
    exact_period = False
    exact_cycle = False
    amp = None
    status = "EXACT affine diagnostics; cycle only if valuations match"

    if candidate is not None:
        positive = candidate > 0
        if candidate.denominator == 1:
            n = candidate.numerator
            if n > 0 and n % 2 == 1:
                integral = True
                states, match, closed = _iterate_if_integral(n, ks)
                in_cyl = belongs_to_cylinder(n, ks)
                exact_period = match and closed and in_cyl
                exact_cycle = exact_period and primitive
                if exact_cycle:
                    amp = cycle_amplitude(states)
                    reason = "primitive exact positive cycle"
                elif exact_period:
                    reason = "exact period of a shorter primitive cycle"
                elif not match:
                    reason = "affine candidate exists but valuations do not match"
                elif not closed:
                    reason = "affine candidate is not a T-orbit of this word"
                elif not in_cyl:
                    reason = "candidate not in the valuation cylinder"
            else:
                reason = "algebraic candidate is not a positive odd integer"
        else:
            reason = "algebraic candidate is not an integer"

    lifts = lift_digits(ks)

    return PeriodicExponentCode(
        code=ks,
        primitive_period=root,
        p=it.m,
        K=it.K,
        C=it.C,
        denominator=D,
        candidate_n=candidate,
        candidate_states=states,
        is_primitive=primitive,
        is_contracting=contracting,
        is_integral=integral,
        is_positive=positive,
        valuations_match=match,
        is_exact_period=exact_period,
        is_exact_cycle=exact_cycle,
        amplitude=amp,
        min_realizer=min_realizer(ks),
        lift_digits=lifts,
        canonical_code=lex_min_rotation(ks),
        rotation_index=rotation_index_of_canonical(ks),
        status=status,
        reason=reason,
    )


def rotated_affine_constant(C: int, D: int, k0: int) -> int:
    """``C' = (3C + D) / 2^{k0}`` for a one-step rotation.

    **PROVED** when ``2^{k0}`` divides ``3C+D``, which holds for every
    exact cycle and is checked for algebraic candidates.
    """
    if k0 < 1:
        raise ValueError("k0 must be >= 1")
    num = 3 * C + D
    den = 1 << k0
    if num % den != 0:
        raise ValueError("3C+D is not divisible by 2^{k0}; not a rotation of an exact affine block")
    return num // den


def rotation_preserves_cycle(code: tuple[int, ...]) -> bool:
    """All rotations of an exact cycle are exact cycles of the same states."""
    original = candidate_cycle(code)
    if not original.is_exact_cycle or original.candidate_states is None:
        return False
    states = original.candidate_states
    for i, rot in enumerate(rotations(code)):
        other = candidate_cycle(rot)
        if not other.is_exact_cycle:
            return False
        if other.candidate_states != states[i:] + states[:i]:
            return False
        if other.amplitude != original.amplitude:
            return False
    return True


def balanced_ternary_range(states: tuple[int, ...]) -> tuple[str, str]:
    """Canonical BT words of the min and max odd states."""
    amp = cycle_amplitude(states)
    return encode(amp.min_state).word(), encode(amp.max_state).word()
