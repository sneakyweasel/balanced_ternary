"""Minimality adapter: existing signed-digit spec, minimality hypotheses."""

from research.signed_digit_residual_minimality.lean_export import export_minimality_targets
from research.signed_digit_residual_minimality.planner import (
    plan_signed_digit_residual_minimality,
)
from research.signed_digit_residual_minimality.spec import minimality_spec

__all__ = [
    "export_minimality_targets",
    "minimality_spec",
    "plan_signed_digit_residual_minimality",
]
