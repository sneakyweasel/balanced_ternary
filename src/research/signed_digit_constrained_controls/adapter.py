"""Constrained-control adapter: no-repeat product spec, rigidity hypotheses."""

from research.signed_digit_constrained_controls.lean_export import export_constrained_targets
from research.signed_digit_constrained_controls.planner import (
    plan_signed_digit_constrained_controls,
)
from research.signed_digit_constrained_controls.spec import constrained_spec

__all__ = [
    "constrained_spec",
    "export_constrained_targets",
    "plan_signed_digit_constrained_controls",
]
