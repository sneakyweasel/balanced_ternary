"""Terminal / accepting predicates.

A terminal region may be a finite set, a slab, or an arbitrary exact
predicate. The engine never assumes it is finite or linear.
"""

from __future__ import annotations

from typing import Protocol, TypeVar

S = TypeVar("S")
P = TypeVar("P")


class TerminalSpec(Protocol[S, P]):
    """Acceptance geometry independent of origin-reachability."""

    def accepts(self, state: S, phase: P) -> bool:
        """Whether ``(state, phase)`` lies in the terminal region."""
