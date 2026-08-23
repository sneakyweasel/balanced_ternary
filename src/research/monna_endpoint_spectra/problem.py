"""Descriptor for the balanced-Monna endpoint-spectra triage branch."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="monna_endpoint_spectra",
    title="Balanced-Monna endpoint preservation and jump-depth spectra",
    status="STRUCTURAL",
    statement=(
        "For F(x)=x^3, classify balanced-Monna endpoint pairs, decide "
        "whether F preserves their equivalence, and derive the exact "
        "3-adic divergence-depth spectrum of F(u)-F(v)."
    ),
    bt_relevance=(
        "Balanced residues give a polar digit alphabet on which the "
        "Monna map is the digit-weight reversal of the residual "
        "section expansion. Endpoint pairs are opposite infinite tails "
        "after a finite prefix, not Collatz 3-adic endpoints and not "
        "bt_reverse."
    ),
    docs=("docs/problems/monna_endpoint_spectra.md",),
)
