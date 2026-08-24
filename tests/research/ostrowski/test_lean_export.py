"""Ostrowski certificates link to existing Lean; |L_0| is not exported."""

from __future__ import annotations

from research.ostrowski.adapter import plan_np
from research.ostrowski.lean_export import (
    HUB_THEOREM,
    STEP_FST_THEOREM,
    export_plan_targets,
)
from research.ostrowski.negative_knowledge import L0_HYPOTHESIS
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.planner.hypothesis import HypothesisStatus
from research_engine.verification import assert_no_proof_tokens, render_lean_comment, render_yaml


def _by_attack(targets, name: str):
    return next(item for item in targets if item.attack == name)


def test_np_modular_links_existing_step_fst_dvd_three():
    targets = export_plan_targets(plan_np(4))
    modular = _by_attack(targets, "modular")
    assert modular.exportable is True
    assert modular.linked is True
    assert modular.name == "origin_mod3_invariant"
    assert modular.lean_theorem == STEP_FST_THEOREM
    yaml = render_yaml(modular)
    assert "origin_mod3_invariant" in yaml
    assert STEP_FST_THEOREM in yaml
    comment = render_lean_comment(modular)
    assert_no_proof_tokens(comment)
    assert "sorry" not in comment.lower()
    assert "admit" not in comment.lower()


def test_np_hub_block_links_existing_hub_nonreset():
    targets = export_plan_targets(plan_np(4))
    block = _by_attack(targets, "block")
    assert block.exportable is True
    assert block.linked is True
    assert block.name == "hub_nonreset"
    assert block.lean_theorem == HUB_THEOREM
    assert "(-3, -1, 0)" in block.statement or "(-3,-1,0)" in block.statement.replace(" ", "")


def test_parked_l0_is_not_exported():
    report = plan_np(4)
    live = next(item for item in report.hypotheses if item.id == L0_HYPOTHESIS.id)
    assert live.status is HypothesisStatus.PARKED
    assert live.kind is ClaimKind.LIVE
    assert live.intended_scope is SearchScope.EXACT
    targets = export_plan_targets(report)
    assert all(item.name != L0_HYPOTHESIS.id for item in targets)
    assert all(item.kind is not ClaimKind.LIVE for item in targets)
    recon = _by_attack(targets, "reconnaissance")
    assert recon.exportable is False
