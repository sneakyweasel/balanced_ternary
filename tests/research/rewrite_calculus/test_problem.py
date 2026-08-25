"""Rewrite-calculus artifact is a registered paper-candidate dossier."""

from research.open_problems import get_problem
from research.rewrite_calculus.problem import PROBLEM


def test_rewrite_calculus_is_a_paper_candidate():
    assert PROBLEM.id == "rewrite_calculus"
    assert PROBLEM.status == "PAPER_CANDIDATE"
    assert get_problem("rewrite_calculus") is PROBLEM
    assert "docs/problems/rewrite_calculus.md" in PROBLEM.docs
    assert "docs/theory/rewrite_calculus_reviewer_packet.md" in PROBLEM.docs
    assert "docs/theory/rewrite_calculus_prior_art.md" in PROBLEM.docs
    assert PROBLEM.lean


def test_novelty_sources_are_registered():
    from research.literature import get_reference

    for ref_id in (
        "newman-1942-confluence",
        "baader-nipkow-1998-term-rewriting",
        "avizienis-1961-signed-digit",
        "contejean-marche-rabehasaina-1997-rta",
        "contejean-marche-rabehasaina-1997-report",
        "heuberger-prodinger-2003-carry",
        "frougny-pelantova-svobodova-2011-parallel-addition",
        "frougny-pelantova-svobodova-2013-minimal-digits",
        "frougny-heller-pelantova-svobodova-2014-k-block",
        "walters-zantema-1994-integer-arithmetic",
        "bergstra-ponse-2016-ddrs-integers",
        "peterson-stickel-1981-unification-ac",
    ):
        rec = get_reference(ref_id)
        assert rec["project_relationship"] == "known"
