"""Multiplicative residual adapter for the research engine."""

from research.multiplicative_residual.lean_export import export_multiplicative_targets
from research.multiplicative_residual.planner import (
    plan_multiplicative_residual,
    plan_product_pair,
)
from research.multiplicative_residual.spec import ProductResidualSpec, product_spec

__all__ = [
    "ProductResidualSpec",
    "export_multiplicative_targets",
    "plan_multiplicative_residual",
    "plan_product_pair",
    "product_spec",
]
