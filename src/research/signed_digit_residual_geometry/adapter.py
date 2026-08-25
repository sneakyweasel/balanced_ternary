"""Geometry adapter: existing signed-digit spec, geometry hypotheses."""

from research.signed_digit_residual_geometry.lean_export import export_geometry_targets
from research.signed_digit_residual_geometry.planner import (
    plan_signed_digit_residual_geometry,
)
from research.signed_digit_residual_geometry.spec import geometry_spec

__all__ = [
    "export_geometry_targets",
    "geometry_spec",
    "plan_signed_digit_residual_geometry",
]
