"""Descriptor for the rewrite-calculus classification artifact."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="rewrite_calculus",
    title="Rewrite calculus of balanced-ternary operators",
    status="PAPER_CANDIDATE",
    statement=(
        "The unary tree TRS on {D, I_a, S, N} including N(D)→D(N) is a "
        "complete canonical form. The next-state output D(x+y) does not "
        "factor through (D(x), D(y)); the exact carry identity explains "
        "the missing state, and the named carry-free push-in extension "
        "fails local confluence."
    ),
    bt_relevance=(
        "The constructors are the balanced-ternary drop/prepend maps "
        "and negation. The trit carry of 1+1 is the minimal witness that "
        "D(x+y) is not determined by the operand D-states."
    ),
    docs=(
        "docs/problems/rewrite_calculus.md",
        "docs/theory/rewrite_calculus.md",
        "docs/theory/rewrite_calculus_note.md",
        "docs/theory/rewrite_calculus_reviewer_packet.md",
    ),
    lean=(
        "formal/BTCalculus/OpFrag.lean",
        "formal/BTCalculus/OpFragNewman.lean",
        "formal/BTCalculus/OpFragSemantic.lean",
        "formal/BTCalculus/RewriteCore.lean",
        "formal/BTCalculus/RewriteAddBoundary.lean",
    ),
    conjectures=(
        "op_fragment_nd_semantic",
        "add_affine_only",
        "add_factor_cas_obstruction",
        "word_simp_nf",
        "word_wn_nf",
        "word_wnd_nf",
    ),
)
