"""Phase-0 gate for generalized Ostrowski order-(m) addition.

See ``docs/problems/ostrowski_order_m_adder.md``. Mathematics lives
here, not in ``bt.*``.
"""

from research.ostrowski.adder_search import phase0_report
from research.ostrowski.problem import PROBLEM

__all__ = ["PROBLEM", "phase0_report"]
