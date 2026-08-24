"""Ostrowski problem adapter.

Energy, place values, and digit rules stay here. The engine sees only
``ProblemSpec`` plus optional affine/recurrence data. This package is
``research.ostrowski``, not a second ``problems/ostrowski_np`` tree.
"""

from research.ostrowski.lean_export import export_plan_targets, link_ostrowski_targets
from research.ostrowski.negative_knowledge import L0_HYPOTHESIS
from research.ostrowski.planner import ostrowski_ledger, plan_np
from research.ostrowski.spec import OstrowskiSpec, ostrowski_affine, ostrowski_spec

__all__ = [
    "L0_HYPOTHESIS",
    "OstrowskiSpec",
    "export_plan_targets",
    "link_ostrowski_targets",
    "ostrowski_affine",
    "ostrowski_ledger",
    "ostrowski_spec",
    "plan_np",
]
