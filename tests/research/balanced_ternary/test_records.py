"""Attack records distinguish OBSERVED from EXACT/LEAN_VERIFIED."""

from __future__ import annotations

from research.balanced_ternary.adapter import export_plan_targets, plan_doubled_trit
from research.balanced_ternary.lean_export import CLOSURE_MODULE, CLOSURE_THEOREM
from research.balanced_ternary.records import record_status, render_record, write_records
from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import SearchScope


def test_record_status_does_not_promote_bounded_recon(tmp_path):
    report = plan_doubled_trit(4)
    targets = export_plan_targets(report)
    recon = next(item for item in report.results if item.name == "reconnaissance")
    closure = next(item for item in report.results if item.name == "closure")
    assert recon.status is AttackStatus.OBSERVATION
    assert recon.scope is SearchScope.BOUNDED
    assert record_status(recon) == "OBSERVED"
    assert record_status(closure) == "EXACT"
    assert record_status(closure, lean_theorem=f"{CLOSURE_MODULE}.{CLOSURE_THEOREM}") == "LEAN_VERIFIED"
    text = render_record(recon)
    assert "status: OBSERVED" in text
    assert "PROVED" not in text
    written = write_records(report, targets, directory=tmp_path)
    names = {path.name for path in written}
    assert "reconnaissance.yaml" in names
    assert "closure.yaml" in names
    closure_text = (tmp_path / "closure.yaml").read_text(encoding="utf-8")
    assert "status: LEAN_VERIFIED" in closure_text
    assert CLOSURE_THEOREM in closure_text
