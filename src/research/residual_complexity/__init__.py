"""Phase-0 gate for unrestricted residual complexity C_F(m,r).

See ``docs/problems/residual_complexity.md``.
"""

from research.residual_complexity.problem import PROBLEM
from research.residual_complexity.triage import triage_report

__all__ = ["PROBLEM", "triage_report"]
