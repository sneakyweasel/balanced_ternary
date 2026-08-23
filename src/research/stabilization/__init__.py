"""Local finite-horizon state versus global root-count bounds.

Literature triage only. The novelty question is closed: every precise
reading is KNOWN or a REPARAMETERIZATION of Hensel / Newton-polygon /
Dwivedi–Saxena 2020. See docs/problems/stabilization.md.
"""

from research.stabilization.problem import PROBLEM
from research.stabilization.triage import local_vs_global_report, witness_mixed_clusters

__all__ = ["PROBLEM", "local_vs_global_report", "witness_mixed_clusters"]
