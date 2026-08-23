"""Descriptor for the closed 3-adic polynomial dynamics triage branch."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="padic_dynamics",
    title="3-adic polynomial cycle dynamics",
    status="ARCHIVED",
    statement=(
        "Depth-r cycle-lift behaviour is the bounded functional behaviour "
        "of the classical return map f^q on a 3-adic fibre. The residual "
        "function class determines it but is not minimal; the bounded "
        "quotient found here is standard tree equivalence and supplies no "
        "new dynamical theorem."
    ),
    bt_relevance=(
        "Balanced digits give exact coordinates for the fibre and residual "
        "sections, but the resulting local return function is the classical "
        "Taylor return map in different coordinates."
    ),
    docs=("docs/problems/padic_dynamics.md",),
)
