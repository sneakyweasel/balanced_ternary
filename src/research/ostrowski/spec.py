"""Ostrowski unread-tail system as a ``ProblemSpec``.

Remaining length is the phase. Energy, place values, and the NP inverse
stay in Ostrowski modules; the engine only sees transition, legality,
and terminal predicates.
"""

from __future__ import annotations

from dataclasses import dataclass

from research.ostrowski.spectral_residual import transition_affine
from research.ostrowski.system import OstrowskiSystem, nonpisot_order3
from research_engine.core.affine_system import AffineSystem
from research_engine.core.phase import IntPhase

State3 = tuple[int, int, int]


def _as_state3(state: tuple[int, ...]) -> State3:
    return (state[0], state[1], state[2])


@dataclass(frozen=True)
class OstrowskiSpec:
    """Phase-dependent Ostrowski adapter. Default system is ``Γ_NP``."""

    system: OstrowskiSystem
    start_remaining: int
    name: str = "ostrowski"

    def __post_init__(self) -> None:
        if self.start_remaining < 0:
            raise ValueError("start_remaining must be nonnegative")

    @property
    def dimension(self) -> int:
        return 3

    @property
    def initial_state(self) -> State3:
        return (0, 0, 0)

    def transition(
        self,
        state: tuple[int, ...],
        control: int,
        phase: IntPhase,
    ) -> State3:
        del phase
        return transition_affine(self.system, _as_state3(state), control)

    def legal_controls(self, state: tuple[int, ...], phase: IntPhase) -> tuple[int, ...]:
        del state
        if phase.value < 1:
            return ()
        from research.ostrowski.live_growth import legal_w

        return legal_w(self.system, phase.value - 1)

    def next_phase(self, phase: IntPhase, control: int) -> IntPhase:
        del control
        return IntPhase(phase.value - 1)

    def is_terminal(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        from research.ostrowski.live_growth import residual_is_live

        return residual_is_live(self.system, _as_state3(state), phase.value)

    def is_accepting(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        return phase.value == 0 and self.is_terminal(state, phase)

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: tuple[int, ...]) -> State3:
        return _as_state3(state)


def ostrowski_spec(
    start_remaining: int,
    system: OstrowskiSystem | None = None,
) -> OstrowskiSpec:
    return OstrowskiSpec(
        system=nonpisot_order3() if system is None else system,
        start_remaining=start_remaining,
    )


def ostrowski_affine(
    system: OstrowskiSystem | None = None,
    controls: tuple[int, ...] | None = None,
) -> AffineSystem:
    """Unread-tail affine system. Alphabet is not a global constant."""
    from research.ostrowski.spectral_residual import residual_matrix

    sys = nonpisot_order3() if system is None else system
    if controls is None:
        from research.ostrowski.live_growth import legal_w

        controls = tuple(sorted(set(legal_w(sys, 0)) | set(legal_w(sys, 1))))
    matrix = residual_matrix(sys)
    return AffineSystem(
        A=matrix,
        translations={w: (0, 0, -w) for w in controls},
        controls=controls,
    )
