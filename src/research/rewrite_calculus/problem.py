"""Descriptor for the rewrite-calculus classification artifact."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="rewrite_calculus",
    title="Rewrite calculus of balanced-ternary operators",
    status="PAPER_CANDIDATE",
    statement=(
        "The unary tree TRS on {D, I_a, S, N} including N(D)→D(N) is a "
        "complete canonical form, and it is maximal among exact "
        "push-in or factor-out extensions by Add or Mul. Integer sums "
        "of constructor terms canonicalize as affine maps / coefficient "
        "words, never as a tree TRS on Add."
    ),
    bt_relevance=(
        "The constructors are the balanced-ternary drop/prepend maps "
        "and negation. The trit carry of 1+1 is what excludes Add from "
        "the tree engine."
    ),
    docs=(
        "docs/problems/rewrite_calculus.md",
        "docs/theory/rewrite_calculus.md",
    ),
    lean=(
        "formal/BTCalculus/OpFrag.lean",
        "formal/BTCalculus/OpFragNewman.lean",
        "formal/BTCalculus/OpFragSemantic.lean",
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
