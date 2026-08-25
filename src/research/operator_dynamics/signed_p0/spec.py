"""Integer iterates of ``N ∘ I_0 ∘ D`` as a ``ProblemSpec``.

State is the integer ``n``. The map is autonomous. Affine/spectral
attacks stay inapplicable: LSD is not one ``Ax+b``.
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.calculus.derivative import D, lsd
from bt.calculus.integral import I_zero, P_zero
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.result import AttackContext
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State

CONTROL = 0
DEFAULT_START = 4
BOX_BOUND = 2
INPUT_LENGTH = 8
INTEGER_STATE_CAP = 64


def integer_sign(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0


def signed_p0(n: int) -> int:
    """``F(n) = N(I_0(D(n))) = lsd(n) - n = -P_0(n)``."""
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError(f"n must be int, got {type(n).__name__}")
    return -I_zero(D(n))


def lsd_int(n: int) -> int:
    return int(lsd(n))


def predecessors(m: int) -> tuple[int, ...]:
    """Exact preimages of ``m`` under ``signed_p0``."""
    if isinstance(m, bool) or not isinstance(m, int):
        raise TypeError(f"m must be int, got {type(m).__name__}")
    found: list[int] = []
    for digit in (-1, 0, 1):
        n = digit - m
        if lsd_int(n) == digit:
            found.append(n)
    return tuple(sorted(found))


def interval_box(bound: int = BOX_BOUND) -> frozenset[State]:
    if isinstance(bound, bool) or not isinstance(bound, int) or bound < 0:
        raise ValueError(f"bound must be a nonnegative int, got {bound!r}")
    return frozenset((n,) for n in range(-bound, bound + 1))


@dataclass(frozen=True)
class SignedP0Spec:
    """Integer dynamics of ``N ∘ I_0 ∘ D`` with sign observation."""

    start: int = DEFAULT_START
    start_remaining: int = INPUT_LENGTH
    state_cap: int = INTEGER_STATE_CAP
    box_bound: int = BOX_BOUND
    name: str = "operator_dynamics_benchmark"
    dimension: int = 1

    def __post_init__(self) -> None:
        if isinstance(self.start, bool) or not isinstance(self.start, int):
            raise TypeError(f"start must be int, got {type(self.start).__name__}")
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")
        if self.state_cap < 1:
            raise ValueError("state_cap must be a positive integer")
        if self.box_bound < 0:
            raise ValueError("box_bound must be nonnegative")

    @property
    def initial_state(self) -> State:
        return (self.start,)

    @property
    def candidate_region(self) -> frozenset[State]:
        return interval_box(self.box_bound)

    def transition(self, state: State, control: object, phase: IntPhase) -> State:
        del control, phase
        return (signed_p0(state[0]),)

    def output(self, state: State, control: object, phase: IntPhase | None = None) -> int:
        del control, phase
        return integer_sign(state[0])

    def legal_controls(self, state: State, phase: IntPhase) -> tuple[object, ...]:
        del state
        if phase.value <= 0:
            return ()
        return (CONTROL,)

    def next_phase(self, phase: IntPhase, control: object) -> IntPhase:
        del control
        if phase.value > 0:
            return IntPhase(phase.value - 1)
        return phase

    def is_terminal(self, state: State, phase: IntPhase) -> bool:
        if self.is_accepting(state, phase):
            return True
        return phase.value > 0

    def is_accepting(self, state: State, phase: IntPhase) -> bool:
        return phase.value == 0 and state == (0,)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: State) -> State:
        return (int(state[0]),)

    def affine_system(self):
        return None

    def reverse_preimage(self, state: State) -> tuple[State, ...]:
        return tuple((pred,) for pred in predecessors(state[0]))

    def attack_context(self, **kwargs) -> AttackContext:
        nxt = signed_p0(self.start)
        kwargs.setdefault("live_only", False)
        kwargs.setdefault("max_states", self.state_cap)
        kwargs.setdefault("max_steps", self.start_remaining)
        kwargs.setdefault("candidate_region", self.candidate_region)
        kwargs.setdefault("functional", LinearFunctional((1,)))
        kwargs.setdefault("reverse_preimage", self.reverse_preimage)
        kwargs.setdefault("reverse_seeds", ((0,),))
        kwargs.setdefault("reverse_max_depth", None)
        kwargs.setdefault("pair", (self.initial_state, (nxt,)))
        kwargs.setdefault("phases", (self.initial_phase(), IntPhase(0)))
        return AttackContext(**kwargs)


def signed_p0_spec(
    start_remaining: int = INPUT_LENGTH,
    start: int = DEFAULT_START,
) -> SignedP0Spec:
    return SignedP0Spec(start=start, start_remaining=start_remaining)


def p0(n: int) -> int:
    return P_zero(n)
