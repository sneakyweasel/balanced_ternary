"""Descriptor for shortcut-Collatz finite-descent residual search."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="collatz_finite_descent",
    title="Shortcut Collatz finite descent residual",
    status="ARCHIVED",
    statement=(
        "Does a finite residual together with bounded affine blocks certify "
        "strict descent for the shortcut map C (even n/2, odd (3n+1)/2), "
        "or is there an exact obstruction in the 2-adic class n mod 2^L? "
        "This module does not claim a proof or disproof of Collatz."
    ),
    bt_relevance=(
        "None required. The map is a two-control piecewise-affine integer "
        "system used as a stress test of the research engine, not a "
        "balanced-ternary coordinate."
    ),
    docs=("docs/problems/collatz_finite_descent.md",),
    lean=("formal/Problems/Collatz/Shortcut.lean",),
)
