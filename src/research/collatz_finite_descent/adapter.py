"""Shortcut Collatz adapter for the research engine."""

from research.collatz_finite_descent.lean_export import (
    export_collatz_finite_descent_targets,
)
from research.collatz_finite_descent.planner import (
    plan_collatz_finite_descent,
    plan_perturbation_5_1,
    plan_terminal_cycle,
)
from research.collatz_finite_descent.spec import ShortcutSpec, shortcut_spec, terminal_spec

__all__ = [
    "ShortcutSpec",
    "export_collatz_finite_descent_targets",
    "plan_collatz_finite_descent",
    "plan_perturbation_5_1",
    "plan_terminal_cycle",
    "shortcut_spec",
    "terminal_spec",
]
