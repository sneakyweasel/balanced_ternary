"""Descriptor for the regular-output preimage triage branch."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="regular_output_preimages",
    title="Regular-output preimages of nonlinear 3-adic polynomials",
    status="STRUCTURAL",
    statement=(
        "For F(x)=x^2 and the infinite regular output constraint "
        "Y={0,+}^ω, decide whether the input preimage X=F^{-1}(Y) is a "
        "sofic language despite F having infinitely many polynomial "
        "sections."
    ),
    bt_relevance=(
        "The residual Mealy machine of bt.calculus supplies the exact "
        "product of a polynomial section with a two-state safety "
        "automaton on output trits. Balanced digits are the output "
        "alphabet of that machine, not a new coordinate."
    ),
    docs=("docs/problems/regular_output_preimages.md",),
)
