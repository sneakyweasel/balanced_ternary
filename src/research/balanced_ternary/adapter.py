"""Balanced-ternary adapters for the research engine."""

from research.balanced_ternary.d_add_spec import DAddResidualSpec, d_add_spec
from research.balanced_ternary.expanding_j2_spec import ExpandingJ2Spec, expanding_j2_spec
from research.balanced_ternary.expanding_j3_spec import ExpandingJ3Spec, expanding_j3_spec
from research.balanced_ternary.expanding_spec import ExpandingDResidueSpec, expanding_d_spec
from research.balanced_ternary.lean_export import (
    export_d_add_targets,
    export_expanding_d_targets,
    export_j2_targets,
    export_j3_targets,
    export_plan_targets,
    link_balanced_ternary_targets,
)
from research.balanced_ternary.perturbation import family_fingerprint, gain_spec
from research.balanced_ternary.planner import (
    plan_d_add,
    plan_doubled_trit,
    plan_expanding_d,
    plan_expanding_j2,
    plan_expanding_j3,
    plan_gain,
)
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
        "name": "balanced_ternary_expanding_j2",
        "class": "observational_finite",
        "note": "J2 residual of T; 9 trit pairs, T-image size 3",
    },
    {
        "name": "balanced_ternary_expanding_j3",
        "class": "observational_finite",
        "note": "J3 residual of T; 27 triples, factors through J2",
    },
    {
        "name": "balanced_ternary_d_add",
        "class": "observational_finite",
        "note": "D(x+y) residual; 3-state trit completion, 5-state bound-2",
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
    "DAddResidualSpec",
    "DoubledTritSpec",
    "ExpandingDResidueSpec",
    "ExpandingJ2Spec",
    "ExpandingJ3Spec",
    "d_add_spec",
    "doubled_trit_spec",
    "expanding_d_spec",
    "expanding_j2_spec",
    "expanding_j3_spec",
    "export_d_add_targets",
    "export_expanding_d_targets",
    "export_j2_targets",
    "export_j3_targets",
    "export_plan_targets",
    "family_fingerprint",
    "gain_spec",
    "link_balanced_ternary_targets",
    "plan_d_add",
    "plan_doubled_trit",
    "plan_expanding_d",
    "plan_expanding_j2",
    "plan_expanding_j3",
    "plan_gain",
]
