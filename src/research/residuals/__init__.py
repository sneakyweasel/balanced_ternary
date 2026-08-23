"""Cubic residual fibres and the Newton-stratum analysis.

The closed form of the ``x^3`` residual and ``F_k`` stay in
``bt.calculus.cubic``. This package studies fibres, layers, and the
mismatched-width quotient.
"""

from research.residuals.problem import PROBLEM
from research.residuals.stratum import newton_stratum

__all__ = ["PROBLEM", "newton_stratum"]
