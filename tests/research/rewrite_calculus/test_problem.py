"""Rewrite-calculus artifact is a registered paper-candidate dossier."""

from research.open_problems import get_problem
from research.rewrite_calculus.problem import PROBLEM


def test_rewrite_calculus_is_a_paper_candidate():
    assert PROBLEM.id == "rewrite_calculus"
    assert PROBLEM.status == "PAPER_CANDIDATE"
    assert get_problem("rewrite_calculus") is PROBLEM
    assert "docs/problems/rewrite_calculus.md" in PROBLEM.docs
    assert "docs/theory/rewrite_calculus_reviewer_packet.md" in PROBLEM.docs
    assert PROBLEM.lean


def test_novelty_sources_are_registered():
    from research.literature import get_reference

    for ref_id in (
        "newman-1942-confluence",
        "baader-nipkow-1998-term-rewriting",
        "avizienis-1961-signed-digit",
        "peterson-stickel-1981-unification-ac",
    ):
        rec = get_reference(ref_id)
        assert rec["project_relationship"] == "known"
