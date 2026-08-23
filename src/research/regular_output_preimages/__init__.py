"""Phase-0 gate for regular-output preimages of nonlinear polynomials.

See ``docs/problems/regular_output_preimages.md``.
"""

from research.regular_output_preimages.problem import PROBLEM
from research.regular_output_preimages.triage import triage_report

__all__ = ["PROBLEM", "triage_report"]
