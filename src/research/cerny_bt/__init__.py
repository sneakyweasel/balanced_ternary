"""Phase-0 gate for a transition-closed residual quotient.

The Černý/synchronization question is not opened. The only object of
this package is whether residual polynomials admit a natural finite
transition congruence. See ``docs/problems/cerny_bt.md``.
"""

from research.cerny_bt.problem import PROBLEM
from research.cerny_bt.triage import triage_report

__all__ = ["PROBLEM", "triage_report"]
