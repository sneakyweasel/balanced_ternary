"""Evidence-driven retrospective over the nine v2.3 campaigns."""

from research_engine.control import (
    build_retrospective,
    load_v2_3_baseline,
    v2_3_control_records,
)
from research_engine.control.types import V2_3_CAMPAIGN_ORDER


def test_retrospective_is_not_a_concatenation():
    baseline = load_v2_3_baseline()
    records = v2_3_control_records(baseline)
    experiments = tuple(baseline.experiment(name) for name in V2_3_CAMPAIGN_ORDER)
    report = build_retrospective(experiments, records)
    assert report.campaign_ids == V2_3_CAMPAIGN_ORDER
    assert "problem normalization to ProblemSpec / BlindPacket" in report.successful_capabilities
    assert "mathematical fingerprinting (RegimeFingerprint)" in report.successful_capabilities
    assert "candidate falsification by exact counterexample" in report.successful_capabilities
    assert report.recurring_failure_modes
    assert report.recurring_missing_capabilities
    names = [item[0] for item in report.recurring_missing_capabilities]
    assert any("ranking" in name.lower() or "predecessor" in name.lower() or "nonlinear" in name.lower() for name in names)
    assert all(count >= 1 for _, count in report.recurring_missing_capabilities)
