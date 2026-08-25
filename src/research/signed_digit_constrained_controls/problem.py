"""Descriptor for signed-digit constrained controls."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="signed_digit_constrained_controls",
    title="Signed-digit constrained controls",
    status="STRUCTURAL",
    statement=(
        "If λ is not divisible by 3 and s≠t, every word of length "
        "v_3(s-t)+1 distinguishes the lsd output streams of F_{λ,U}. "
        "A common cyclic letter is not required. Finite control automata "
        "that admit a legal word of that length from a control state keep "
        "distinct residuals at that state observationally inequivalent. "
        "Control-state bisimulation can collapse the product without "
        "merging distinct residuals."
    ),
    bt_relevance=(
        "The residual step is existing D; the control automaton only "
        "restricts which words exist. No second digit model."
    ),
    docs=("docs/problems/signed_digit_constrained_controls.md",),
    lean=("formal/Problems/BalancedTernary/SignedDigitConstrainedControls.lean",),
)
