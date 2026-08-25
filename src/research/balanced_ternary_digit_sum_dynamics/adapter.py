"""Digit-sum dynamics adapter: integer spec, orbit hypotheses, Lean export."""

from research.balanced_ternary_digit_sum_dynamics.lean_export import export_digit_sum_targets
from research.balanced_ternary_digit_sum_dynamics.planner import plan_digit_sum_dynamics
from research.balanced_ternary_digit_sum_dynamics.spec import DigitSumDynamicsSpec, digit_sum_spec

__all__ = [
    "DigitSumDynamicsSpec",
    "digit_sum_spec",
    "export_digit_sum_targets",
    "plan_digit_sum_dynamics",
]
