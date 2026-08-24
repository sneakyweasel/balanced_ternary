"""Opaque phase tokens.

A problem may interpret a phase as remaining length, digit position,
terminal mode, or nothing at all. The engine does not choose.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IntPhase:
    """Integer phase token with problem-defined meaning."""

    value: int

    def __int__(self) -> int:
        return self.value
