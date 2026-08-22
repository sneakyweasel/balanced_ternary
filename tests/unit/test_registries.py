"""Schema consistency for conjecture and literature registries."""

from __future__ import annotations

from research.conjectures import REQUIRED as CONJ_REQUIRED
from research.conjectures import STATUSES, get_conjecture, list_conjectures
from research.literature import REQUIRED as LIT_REQUIRED
from research.literature import get_reference, list_references


def test_conjectures_have_required_fields_and_valid_status():
    rows = list_conjectures()
    assert rows
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids))
    for rec in rows:
        for key in CONJ_REQUIRED:
            assert key in rec
        assert rec["status"] in STATUSES


def test_refuted_hypotheses_are_present():
    for cid in (
        "W_not_involution",
        "W_three_n",
        "W_commutes_T",
        "BT_R_suffix_determines_next_valuation",
        "n_star_le_n",
        "H_BT_independence",
        "S_circ_D_id",
    ):
        rec = get_conjecture(cid)
        assert rec["status"] == "REFUTED"
        assert rec["counterexamples"]


def test_nk_is_not_silently_a_theorem():
    rec = get_conjecture("Nk_state_count")
    assert rec["status"] == "COMPUTATIONALLY_SUPPORTED"


def test_literature_records_have_required_fields():
    rows = list_references()
    assert rows
    for rec in rows:
        for key in LIT_REQUIRED:
            assert key in rec
    assert get_reference("kramer-2026")["project_relationship"] == "reproduced"
