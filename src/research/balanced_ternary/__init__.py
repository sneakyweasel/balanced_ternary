"""Phase-0 doubled-trit dynamics and Phase-1 expanding-D residual."""

from research.balanced_ternary.expanding_j2_spec import ExpandingJ2Spec, expanding_j2_spec
from research.balanced_ternary.expanding_j3_spec import ExpandingJ3Spec, expanding_j3_spec
from research.balanced_ternary.expanding_spec import ExpandingDResidueSpec, expanding_d_spec
from research.balanced_ternary.problem import PROBLEM
from research.balanced_ternary.spec import DoubledTritSpec, doubled_trit_spec

__all__ = [
    "DoubledTritSpec",
    "ExpandingDResidueSpec",
    "ExpandingJ2Spec",
    "ExpandingJ3Spec",
    "PROBLEM",
    "doubled_trit_spec",
    "expanding_d_spec",
    "expanding_j2_spec",
    "expanding_j3_spec",
]
