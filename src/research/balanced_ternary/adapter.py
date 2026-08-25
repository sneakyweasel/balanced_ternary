"""Balanced-ternary adapters for the research engine."""

from research.balanced_ternary.expanding_spec import ExpandingDResidueSpec, expanding_d_spec
from research.balanced_ternary.lean_export import (
    export_expanding_d_targets,
    export_plan_targets,
    link_balanced_ternary_targets,
)
from research.balanced_ternary.perturbation import family_fingerprint, gain_spec
from research.balanced_ternary.planner import plan_doubled_trit, plan_expanding_d, plan_gain
from research.balanced_ternary.spec import DoubledTritSpec, doubled_trit_spec

BENCHMARK_MATRIX: tuple[dict[str, str], ...] = (
    {
        "name": "balanced_ternary_normalization",
        "class": "known_finite",
        "note": "doubled-trit residual closure {-1,0,1}",
    },
    {
        "name": "pisot_ostrowski",
        "class": "known_finite",
        "note": "existing Pisot adder; not reopened here",
    },
    {
        "name": "nonpisot_ostrowski",
        "class": "unknown_difficult",
        "note": "PARK |L_0|; do not reopen",
    },
    {
        "name": "balanced_ternary_expanding_d",
        "class": "observational_finite",
        "note": "T(n)=3n-lsd(n); LSD residual {-1,0,1}",
    },
    {
        "name": "benchmark_B",
        "class": "synthetic_infinite",
        "note": "engine InfiniteTranslateSpec",
    },
    {
        "name": "benchmark_C",
        "class": "synthetic_reset",
        "note": "engine ResetLoopSpec",
    },
)

__all__ = [
    "BENCHMARK_MATRIX",
    "DoubledTritSpec",
    "ExpandingDResidueSpec",
    "doubled_trit_spec",
    "expanding_d_spec",
    "export_expanding_d_targets",
    "export_plan_targets",
    "family_fingerprint",
    "gain_spec",
    "link_balanced_ternary_targets",
    "plan_doubled_trit",
    "plan_expanding_d",
    "plan_gain",
]
