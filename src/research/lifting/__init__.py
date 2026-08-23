"""Polynomial congruences and 3-adic lifting trees.

Imports :mod:`bt.calculus.lifting` for the exact tree and state objects;
this package holds only the classification experiments and the problem
descriptor.
"""

from research.lifting.problem import PROBLEM
from research.lifting.triage import triage_report

__all__ = ["PROBLEM", "triage_report"]
