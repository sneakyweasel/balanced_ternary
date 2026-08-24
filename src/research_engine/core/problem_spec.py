"""Canonical problem specification protocol.

Generic machinery depends only on this interface. Ostrowski-specific
recurrence, energy, and digit rules belong behind an adapter.
"""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

S = TypeVar("S")
C = TypeVar("C")
P = TypeVar("P")


@runtime_checkable
class ProblemSpec(Protocol[S, C, P]):
    """Constrained discrete dynamical system.

    ``legal_controls`` is evaluated at a state and phase. There is no
    global alphabet. Terminal and accepting predicates are distinct.
    """

    name: str
    dimension: int
    initial_state: S

    def transition(self, state: S, control: C, phase: P) -> S:
        """Exact successor state."""

    def legal_controls(self, state: S, phase: P) -> tuple[C, ...]:
        """Controls allowed at this state and phase."""

    def next_phase(self, phase: P, control: C) -> P:
        """Successor phase after consuming ``control``."""

    def is_terminal(self, state: S, phase: P) -> bool:
        """Whether ``state`` is in the terminal region at ``phase``."""

    def is_accepting(self, state: S, phase: P) -> bool:
        """Whether ``(state, phase)`` is an accepting configuration."""

    def initial_phase(self) -> P:
        """Starting phase for trajectories from ``initial_state``."""

    def canonicalize(self, state: S) -> S:
        """Return a canonical representative of ``state``."""
