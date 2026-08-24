"""Bounded hypothesis explorer for normalization theory.

Candidates are never auto-promoted to **EXACT — HUMAN PROOF**. Failures keep the
smallest counterexample and a commented Lean skeleton (not written into
``formal/``).
"""

from __future__ import annotations

from dataclasses import dataclass

from bt.normtheory.arithmetic import compare_fma
from bt.normtheory.calculus_link import D_normalize_words_equal
from bt.normtheory.coeffword import CoeffWord
from bt.normtheory.complexity import enumerate_words, measure
from bt.normtheory.graph import geodesic_equals_excess
from bt.normtheory.rewrite import weighted_l1_increases_on_two
from bt.normtheory.strategies import all_strategies


@dataclass(frozen=True)
class HypothesisResult:
    name: str
    status: str
    domain: str
    counterexample: tuple[int, ...] | None
    notes: str
    lean_skeleton: str

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "status": self.status,
            "domain": self.domain,
            "counterexample": list(self.counterexample) if self.counterexample else None,
            "notes": self.notes,
            "lean_skeleton": self.lean_skeleton,
        }


def _skel(name: str, body: str) -> str:
    return f"-- candidate only; not admitted in formal/\n-- {name}\n-- {body}\n"


def discover(width: int = 4, bound: int = 2) -> list[HypothesisResult]:
    words = enumerate_words(width, bound)
    return [
        _weighted_l1(),
        _rewrite_equals_excess(words),
        _ab_same_count(words),
        _geodesic_excess(words),
        _d_commutes(words),
        _fma_always_cheaper(words),
    ]


def _weighted_l1() -> HypothesisResult:
    fails = weighted_l1_increases_on_two()
    return HypothesisResult(
        name="weighted_l1_alpha_3_2_decreases",
        status="REFUTED" if fails else "CONJECTURE",
        domain="[2] -> [-1,1]",
        counterexample=(2,) if fails else None,
        notes="Σ |c_i| (3/2)^i increases on 2 → -1 with carry +1.",
        lean_skeleton=_skel(
            "weighted_l1",
            "example : ¬ (weighted (step [2] 0) < weighted [2]) := by -- counterexample",
        ),
    )


def _rewrite_equals_excess(words: list[CoeffWord]) -> HypothesisResult:
    for w in words:
        if measure(w).rewrite_A != w.excess():
            return HypothesisResult(
                name="rewrite_A_equals_excess",
                status="REFUTED",
                domain=f"width<={max(w.width() for w in words)} |c|<={max(w.peak() for w in words)}",
                counterexample=w.coeffs,
                notes="Strategy A rewrite count is not the L1 excess.",
                lean_skeleton=_skel("rewrite_eq_excess", "example : rewriteA w ≠ excess w"),
            )
    return HypothesisResult(
        name="rewrite_A_equals_excess",
        status="COMPUTATIONALLY VERIFIED",
        domain=f"{len(words)} words",
        counterexample=None,
        notes="No counterexample on this box. Not a theorem.",
        lean_skeleton=_skel("rewrite_eq_excess", "theorem? rewriteA = excess"),
    )


def _ab_same_count(words: list[CoeffWord]) -> HypothesisResult:
    for w in words:
        traces = all_strategies(w)
        if traces["A"].rewrite_count != traces["B"].rewrite_count:
            return HypothesisResult(
                name="strategy_A_B_same_rewrite_count",
                status="REFUTED",
                domain="enumerated box",
                counterexample=w.coeffs,
                notes="A and B can disagree on rewrite count.",
                lean_skeleton=_skel("A_eq_B_count", "example : rewriteA w ≠ rewriteB w"),
            )
    return HypothesisResult(
        name="strategy_A_B_same_rewrite_count",
        status="COMPUTATIONALLY VERIFIED",
        domain=f"{len(words)} words",
        counterexample=None,
        notes="No count gap on this box. Not a theorem.",
        lean_skeleton=_skel("A_eq_B_count", "theorem? rewriteA = rewriteB"),
    )


def _geodesic_excess(words: list[CoeffWord]) -> HypothesisResult:
    for w in words:
        eq = geodesic_equals_excess(w)
        if eq is False:
            return HypothesisResult(
                name="geodesic_equals_excess",
                status="REFUTED",
                domain="enumerated box",
                counterexample=w.coeffs,
                notes="Shortest rewrite path is not the excess score.",
                lean_skeleton=_skel("geo_eq_excess", "example : dist w ≠ excess w"),
            )
    return HypothesisResult(
        name="geodesic_equals_excess",
        status="COMPUTATIONALLY VERIFIED",
        domain=f"{len(words)} words",
        counterexample=None,
        notes="No geodesic/excess gap on this box, or graph truncated.",
        lean_skeleton=_skel("geo_eq_excess", "theorem? dist = excess"),
    )


def _d_commutes(words: list[CoeffWord]) -> HypothesisResult:
    for w in words:
        if not D_normalize_words_equal(w):
            return HypothesisResult(
                name="D_normalize_commutes",
                status="REFUTED",
                domain="enumerated box",
                counterexample=w.coeffs,
                notes="Fails when c_0 is noncanonical until rewritten.",
                lean_skeleton=_skel("D_nf", "example : D (nf P) ≠ nf (D_coeff P)"),
            )
    return HypothesisResult(
        name="D_normalize_commutes",
        status="COMPUTATIONALLY VERIFIED",
        domain=f"{len(words)} words",
        counterexample=None,
        notes="No failure on this box.",
        lean_skeleton=_skel("D_nf", "theorem? D ∘ nf = nf ∘ D_coeff"),
    )


def _fma_always_cheaper(words: list[CoeffWord]) -> HypothesisResult:
    # Use short prefixes as (P,Q,R).
    sample = words[:40]
    for p in sample:
        for q in sample[:6]:
            for r in sample[:6]:
                cmp = compare_fma(p, q, r)
                if cmp.staged_cheaper:
                    return HypothesisResult(
                        name="fma_fused_always_fewer_rewrites",
                        status="REFUTED",
                        domain="small P,Q,R box",
                        counterexample=p.coeffs + (99,) + q.coeffs + (99,) + r.coeffs,
                        notes=(
                            f"Staged cheaper: fused={cmp.fused.rewrite_count} "
                            f"staged={cmp.staged.rewrite_count}. Values still equal."
                        ),
                        lean_skeleton=_skel("fma_cost", "example : stagedRewrites < fusedRewrites"),
                    )
    return HypothesisResult(
        name="fma_fused_always_fewer_rewrites",
        status="COMPUTATIONALLY VERIFIED",
        domain="small P,Q,R sample",
        counterexample=None,
        notes="No staged-cheaper witness in this sample. Not a theorem.",
        lean_skeleton=_skel("fma_cost", "theorem? fused <= staged"),
    )
