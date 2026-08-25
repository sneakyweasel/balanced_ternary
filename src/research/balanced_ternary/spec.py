"""Doubled-trit normalization as a ``ProblemSpec``.

The residual is the carry of ``BoundedNormalizeTransducer(2)`` on the
LSD-first stream ``2 d_i`` for canonical trits ``d_i``. The engine does
not know that the base is 3. Gain ``λ ≠ 1`` is a synthetic perturbation
and is not value-preserving normalization.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.operators import balanced_quotient, lsd_digit
from bt.representation import BalancedTernary, from_digits_lsd
from bt.transducers.mealy import mealy_partition, minimize_mealy_count
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

TRITS: tuple[int, int, int] = (-1, 0, 1)
CANONICAL_CARRIES: frozenset[State] = frozenset({(-1,), (0,), (1,)})
INPUT_LENGTH = 8


def emit(carry: int, digit: int, gain: int = 1) -> tuple[int, int]:
    """Next carry and output digit.

    ``gain=1`` is the existing balanced quotient ``DZ(c+2d)``. The boxed
    normalizer ``BoundedNormalizeTransducer(2)`` agrees on ``|c|<=2``.
    """
    total = carry + 2 * digit
    return gain * balanced_quotient(total), lsd_digit(total)


def sign_orbit(state: State) -> frozenset[State]:
    carry = state[0]
    if carry == 0:
        return frozenset({(0,)})
    return frozenset({(carry,), (-carry,)})


@dataclass(frozen=True)
class DoubledTritSpec:
    """Finite-control doubled-trit carry dynamics."""

    gain: int = 1
    start_remaining: int = INPUT_LENGTH
    name: str = "balanced_ternary"
    dimension: int = 1

    def __post_init__(self) -> None:
        if self.gain < 1:
            raise ValueError("gain must be a positive integer")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.gain != 1 and self.name == "balanced_ternary":
            object.__setattr__(self, "name", f"balanced_ternary_gain_{self.gain}")

    @property
    def initial_state(self) -> State:
        return (0,)

    def emit(self, carry: int, digit: int) -> tuple[int, int]:
        return emit(carry, digit, self.gain)

    def transition(self, state: State, control: int, phase: IntPhase) -> State:
        del phase
        nxt, _out = self.emit(state[0], control)
        return (nxt,)

    def output(self, state: State, control: int) -> int:
        _nxt, out = self.emit(state[0], control)
        return out

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[int, ...]:
        if phase.value > 0:
            return TRITS
        if state[0] == 0:
            return ()
        return (0,)

    def next_phase(self, phase: IntPhase, control: int) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        if self.is_accepting(state, phase):
            return True
        if phase.value > 0:
            return True
        nxt, _out = self.emit(state[0], 0)
        return abs(nxt) < abs(state[0])

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        return phase.value == 0 and state == (0,)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]),)

    def apply_word(self, digits: tuple[int, ...]) -> BalancedTernary:
        """Normalize the doubled stream, then flush the leftover carry."""
        carry = 0
        out: list[int] = []
        for digit in digits:
            carry, emitted = self.emit(carry, digit)
            out.append(emitted)
        while carry:
            carry, emitted = self.emit(carry, 0)
            out.append(emitted)
        return from_digits_lsd(out)

    def affine_system(self):
        """The step is piecewise balanced division, not one ``Ax+b(d)``."""
        return None

    def reverse_preimage(self, state: State) -> tuple[State, ...]:
        """Predecessors inside the canonical three-carry box."""
        target = state[0]
        found: set[State] = set()
        for carry in TRITS:
            for digit in TRITS:
                nxt, _out = emit(carry, digit, self.gain)
                if nxt == target:
                    found.add((carry,))
        return tuple(sorted(found))

    def attack_context(self, **kwargs) -> AttackContext:
        kwargs.setdefault("live_only", True)
        kwargs.setdefault("candidate_region", CANONICAL_CARRIES)
        kwargs.setdefault("reverse_preimage", self.reverse_preimage)
        kwargs.setdefault("reverse_seeds", tuple(sorted(CANONICAL_CARRIES)))
        kwargs.setdefault("reverse_max_depth", None)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def doubled_trit_spec(
    start_remaining: int = INPUT_LENGTH,
    gain: int = 1,
) -> DoubledTritSpec:
    return DoubledTritSpec(gain=gain, start_remaining=start_remaining)


def reference_normalize(digits: tuple[int, ...]) -> BalancedTernary:
    """Existing bounded normalizer on the doubled coefficient word."""
    from bt.normtheory.coeffword import CoeffWord
    from bt.normtheory.locality import BoundedNormalizeTransducer

    return BoundedNormalizeTransducer(2).apply(
        CoeffWord(tuple(2 * digit for digit in digits))
    )


def lyapunov(carry: int) -> int:
    return abs(carry)


def lyapunov_decreases_outside_box(carry: int, digit: int, gain: int = 1) -> bool:
    nxt, _out = emit(carry, digit, gain)
    return lyapunov(nxt) < lyapunov(carry)


def sign_equivariant(carry: int, digit: int, gain: int = 1) -> bool:
    nxt, out = emit(carry, digit, gain)
    neg_nxt, neg_out = emit(-carry, -digit, gain)
    return neg_nxt == -nxt and neg_out == -out


def mealy_step(state: State, digit: int, gain: int = 1) -> tuple[State, int]:
    nxt, out = emit(state[0], digit, gain)
    return (nxt,), out


def raw_state_count(states: frozenset[State] = CANONICAL_CARRIES) -> int:
    return len(states)


def sign_orbit_count(states: frozenset[State] = CANONICAL_CARRIES) -> int:
    orbits = {sign_orbit(state) for state in states}
    return len(orbits)


def minimized_state_count(
    states: frozenset[State] = CANONICAL_CARRIES,
    gain: int = 1,
) -> int:
    def step(state: State, digit: int) -> tuple[State, int]:
        return mealy_step(state, digit, gain)

    return minimize_mealy_count(states, TRITS, step)


def output_signatures(
    states: frozenset[State] = CANONICAL_CARRIES,
    gain: int = 1,
) -> dict[State, tuple[int, ...]]:
    return {
        state: tuple(mealy_step(state, digit, gain)[1] for digit in TRITS)
        for state in sorted(states)
    }


def mealy_classes(
    states: frozenset[State] = CANONICAL_CARRIES,
    gain: int = 1,
) -> tuple[frozenset[State], ...]:
    def step(state: State, digit: int) -> tuple[State, int]:
        return mealy_step(state, digit, gain)

    return mealy_partition(states, TRITS, step)
