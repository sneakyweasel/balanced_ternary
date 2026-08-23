"""Descriptor for the local-versus-global stabilization triage."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="stabilization",
    title="Local residual horizon versus global root-count bounds",
    status="ARCHIVED",
    statement=(
        "The finite-horizon residual Phi_r determines the next r lifting "
        "levels at a node, which is the Taylor jet. The global threshold "
        "k0 = d(Delta+1)+1 of Dwivedi–Saxena 2020 is a closed form for "
        "N_k(f), using the discriminant valuation of rad(f). These answer "
        "different questions; the local state does not improve k0."
    ),
    bt_relevance=(
        "Balanced digits identify the lifting tree with the residual "
        "machine, so the comparison can be read off existing LiftNode "
        "data. That identification is already a reparameterization."
    ),
    docs=(
        "docs/problems/stabilization.md",
        "docs/theory/local_vs_global_stabilization.md",
    ),
)
