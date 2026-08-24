"""Ostrowski unread-tail system as a ``ProblemSpec``.

Remaining length is the phase. Place values, energy, and digit legality
are adapter methods. The engine sees only the ``ProblemSpec`` protocol
plus optional affine/recurrence data.
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

    def q(self, n: int) -> int:
        """Place value ``q_n``. Ostrowski-specific; not an engine primitive."""
        return self.system.place_value(n)

    def energy(self, state: tuple[int, ...], remaining: int) -> int:
        """Unread-tail energy ``E_remaining(s)``. Stays on the adapter."""
        from research.ostrowski.residual import residual_integer

        return residual_integer(self.system, _as_state3(state), remaining)

    def digit_realization(self, control: int, phase: IntPhase) -> bool:
        """Whether difference digit ``control`` is legal at ``phase``."""
        return control in self.legal_controls(self.initial_state, phase)

    def affine_system(self) -> AffineSystem:
        return ostrowski_affine(self.system)

    def recurrence(self):
        from research.ostrowski.recurrence import recurrence_spec

        return recurrence_spec(self.system)

    def attack_context(self, **kwargs):
        from research_engine.attacks.result import AttackContext

        kwargs.setdefault("live_only", True)
        kwargs.setdefault("affine", self.affine_system())
        return AttackContext(**kwargs)


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
