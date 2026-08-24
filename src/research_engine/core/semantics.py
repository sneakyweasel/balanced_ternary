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
