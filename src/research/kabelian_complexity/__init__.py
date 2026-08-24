"""Phase-0 gate for k-abelian residual signatures of automatic sequences.

The general regularity conjecture is not opened. The only object of this
package is whether a laboratory residual/signature state explains known
b-regular k-abelian complexity, or whether that state is the classical
k-block-coding construction. See ``docs/problems/kabelian_complexity.md``.
"""

from research.kabelian_complexity.problem import PROBLEM
from research.kabelian_complexity.triage import triage_report

__all__ = ["PROBLEM", "triage_report"]
