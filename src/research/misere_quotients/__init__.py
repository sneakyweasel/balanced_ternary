"""Phase-0 gate: finite-context signatures versus misere quotients.

Balanced-ternary arithmetic is not used. The only transferred object is
the laboratory pattern

    position → finite context signature → distinguishing context → quotient.

See ``docs/problems/misere_quotients.md``.
"""

from research.misere_quotients.problem import PROBLEM
from research.misere_quotients.triage import triage_report

__all__ = ["PROBLEM", "triage_report"]
