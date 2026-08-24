"""Exact semantic types for experimental dynamics.

Every search result that later uses these types must identify whether
it is exact, finite-horizon/bounded, or approximate. Floating point is
never an authoritative state.
"""

from __future__ import annotations

from enum import Enum
from typing import Hashable, TypeAlias

State: TypeAlias = tuple[int, ...]
Vector: TypeAlias = tuple[int, ...]
Matrix: TypeAlias = tuple[tuple[int, ...], ...]
Control: TypeAlias = Hashable


class SearchScope(str, Enum):
    """Completeness of a computational result.

    A bounded search is not an asymptotic theorem.
    """

    EXACT = "EXACT"
    BOUNDED = "BOUNDED"
    APPROXIMATE = "APPROXIMATE"


class ClaimKind(str, Enum):
    """Typed research target. These kinds do not imply one another.

    ``LIVE_SLICE`` is ``R ∩ K`` at the same phase. ``LIVE`` is
    ``R ∩ C(K)``. ``CO_REACHABLE`` of a seed is not the live set.
    ``TERMINAL`` geometry is not infinitude of ``LIVE``.
    """

    REACHABLE = "REACHABLE"
    CO_REACHABLE = "CO_REACHABLE"
    TERMINAL = "TERMINAL"
    LIVE_SLICE = "LIVE_SLICE"
    LIVE = "LIVE"
    SUFFIX = "SUFFIX"
