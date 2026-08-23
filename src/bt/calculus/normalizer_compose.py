"""Bounded-alphabet transducers for ``hat D`` and residual/normalizer composition.

``hat D`` on unbounded integer coefficients is not one finite-state
transducer. For a fixed bound ``B``, LSD normalization is a Mealy machine
with carry in ``[-B, B]``, and canonical ``hat D`` is that machine followed
by dropping the first output trit.

Residual polynomial machines already emit canonical trits, so composing
``N_B`` on their *output* is the identity. The nontrivial interaction is
representation of residual *coefficients* in ``[-B, B]``, which fails once
``max |coeff| > B``.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.automata import profile_states
from bt.calculus.myhill_nerode import myhill_nerode_count
from bt.calculus.section import IntPoly
from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.hatd import hatD, milestone14_witness
from bt.normtheory.locality import BoundedNormalizeTransducer, carry_bound
from bt.representation import encode


def hatD_is_normalize_then_drop(word: CoeffWord) -> bool:
    """Canonical ``hat D(P)`` equals the tail of ``encode(value(P))``."""
    digits = list(encode(word.value()).digits_lsd())
    tail = digits[1:] if len(digits) > 1 else [0]
    return list(hatD(word).coeffs) == list(CoeffWord(tuple(tail)).coeffs)


def hatD_state_upper_bound(B: int) -> int:
    """Carry of ``N_B`` plus a one-trit output delay (drop first)."""
    if B < 1:
        raise ValueError("B must be >= 1")
    return 2 * (2 * carry_bound(B) + 1)


@dataclass(frozen=True)
class HatDTransducerProfile:
    bound: int
    carry_states: int
    delay_states_upper: int
    witness_two: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "bound": self.bound,
            "carry_states": self.carry_states,
            "delay_states_upper": self.delay_states_upper,
            "m14_witness_present": self.witness_two,
        }


def profile_hatD(B: int) -> HatDTransducerProfile:
    C = carry_bound(B)
    w = milestone14_witness()
    return HatDTransducerProfile(
        bound=B,
        carry_states=2 * C + 1,
        delay_states_upper=hatD_state_upper_bound(B),
        witness_two=w.coeffs == (2,) and hatD(w).value() == 1,
    )


@dataclass(frozen=True)
class NormalizerComposeProfile:
    poly: str
    depth: int
    bound: int
    M: int
    normalizer_states: int
    composed_upper: int
    max_coeff: int
    representable: bool
    obstruction: str | None

    def as_dict(self) -> dict[str, object]:
        return {
            "poly": self.poly,
            "depth": self.depth,
            "bound": self.bound,
            "M": self.M,
            "normalizer_states": self.normalizer_states,
            "composed_upper": self.composed_upper,
            "max_coeff": self.max_coeff,
            "representable": self.representable,
            "obstruction": self.obstruction,
        }


def profile_compose_normalizer(f: IntPoly, k: int, B: int) -> NormalizerComposeProfile:
    rec = profile_states(f, k)
    n_states = 2 * carry_bound(B) + 1
    ok = rec.max_coeff <= B
    # Output-side N_B is identity (outputs are already trits).
    # Coefficient-side product is defined only while residuals fit in [-B,B].
    return NormalizerComposeProfile(
        poly=rec.poly,
        depth=k,
        bound=B,
        M=rec.myhill_nerode,
        normalizer_states=n_states,
        composed_upper=rec.myhill_nerode * n_states if ok else rec.myhill_nerode * n_states,
        max_coeff=rec.max_coeff,
        representable=ok,
        obstruction=None if ok else f"max |coeff| = {rec.max_coeff} exceeds B = {B}",
    )


def apply_normalizer(word: CoeffWord, B: int):
    return BoundedNormalizeTransducer(B).apply(word)
