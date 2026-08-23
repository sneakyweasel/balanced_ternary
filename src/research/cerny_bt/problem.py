"""Descriptor for the closed Černý residual-quotient triage branch."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="cerny_bt",
    title="Transition-closed residual quotients for Černý-type automata",
    status="ARCHIVED",
    statement=(
        "The coarsest transition congruence contained in finite-horizon "
        "residual equivalence is full Mealy equivalence, which on Z[x] is "
        "raw polynomial equality. Affine residuals have a finite closure; "
        "every nonlinear polynomial has infinitely many distinct sections. "
        "No canonical finite transition-closed quotient exists for a "
        "non-affine family."
    ),
    bt_relevance=(
        "Balanced-ternary sections supply the residual Mealy machine, but "
        "the finite-state classification is the classical linear-versus-"
        "nonlinear dichotomy for polynomial rooted-tree endomorphisms."
    ),
    docs=("docs/problems/cerny_bt.md",),
)
