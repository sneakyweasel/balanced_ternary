"""Signed-digit residual adapter for the research engine."""

from research.signed_digit_residual.lean_export import export_signed_digit_targets
from research.signed_digit_residual.planner import (
    plan_signed_digit_pair,
    plan_signed_digit_residual,
)
from research.signed_digit_residual.spec import (
    SignedDigitResidualSpec,
    signed_digit_spec,
)

__all__ = [
    "SignedDigitResidualSpec",
    "export_signed_digit_targets",
    "plan_signed_digit_pair",
    "plan_signed_digit_residual",
    "signed_digit_spec",
]
