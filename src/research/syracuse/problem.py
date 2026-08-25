"""Descriptor for the accelerated odd-only engine stress test."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="syracuse",
    title="Accelerated odd-only map as a v2 diagnosis benchmark",
    status="EXPLORATORY",
    statement=(
        "Can Research Engine v2 diagnose the structural language of "
        "S(n)=(3n+1)/2^{v_2(3n+1)} on positive odd integers without being "
        "told 2-adic structure, and without claiming a Collatz solution?"
    ),
    bt_relevance=(
        "None required. The target is an engine-loop stress test against "
        "the parked research.collatz dictionary."
    ),
    docs=("docs/problems/syracuse.md",),
    lean=("formal/Problems/Collatz/Syracuse.lean",),
)
