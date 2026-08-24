"""Compatibility shim. Canonical implementation: :mod:`research.collatz.invariants`."""

from research.collatz.invariants import (
    CollatzInvariantReport,
    verify_collatz_invariants,
)

__all__ = ["CollatzInvariantReport", "verify_collatz_invariants"]
