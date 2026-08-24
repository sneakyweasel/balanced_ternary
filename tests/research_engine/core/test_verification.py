"""Exact certificates become targets; LIVE and bounded censuses do not."""

from __future__ import annotations

from pathlib import Path

from research_engine.attacks.result import AttackResult, AttackStatus
from research_engine.benchmarks.pipeline import run_benchmark
from research_engine.core.semantics import ClaimKind, SearchScope
from research_engine.verification import (
    assert_no_proof_tokens,
    render_lean_comment,
    render_yaml,
    target_from_result,
    targets_from_report,
)


ROOT = Path(__file__).resolve().parents[3]
FORMAL = ROOT / "formal"


def _by_attack(targets, name: str):
    return next(item for item in targets if item.attack == name)


def test_benchmark_d_modular_is_exportable_without_proof_tokens():
    report = run_benchmark("D")
    targets = targets_from_report(report, problem="benchmark_modular_triple")
    modular = _by_attack(targets, "modular")
    assert modular.exportable is True
    assert modular.kind is ClaimKind.REACHABLE
    assert modular.scope is SearchScope.EXACT
    yaml = render_yaml(modular)
    comment = render_lean_comment(modular)
    assert "exportable: true" in yaml
    assert "name: benchmark_modular_triple_modular" in yaml
    assert_no_proof_tokens(yaml)
    assert_no_proof_tokens(comment)
    assert "sorry" not in comment.lower()
    assert "admit" not in comment.lower()
    assert "theorem " not in comment


def test_benchmark_b_reconnaissance_is_not_exportable():
    report = run_benchmark("B")
    targets = targets_from_report(report, problem="benchmark_infinite_translate")
    recon = _by_attack(targets, "reconnaissance")
    assert recon.exportable is False
    assert recon.kind is ClaimKind.LIVE_SLICE
    assert recon.scope is SearchScope.BOUNDED
    yaml = render_yaml(recon)
    assert "exportable: false" in yaml
    assert_no_proof_tokens(yaml)
    assert_no_proof_tokens(render_lean_comment(recon))


def test_live_claim_is_never_exportable_even_if_supported_exact():
    result = AttackResult(
        name="fake_live",
        status=AttackStatus.SUPPORTED,
        kind=ClaimKind.LIVE,
        scope=SearchScope.EXACT,
        claim="the live set is infinite",
    )
    target = target_from_result(result, problem="toy")
    assert target.exportable is False
    assert target.reason == "LIVE claims are not auto-exported"


def test_rendering_does_not_write_lean_files():
    ostrowski = FORMAL / "Problems" / "Ostrowski"
    before = {path.relative_to(ostrowski) for path in ostrowski.rglob("*.lean")}
    report = run_benchmark("D")
    modular = _by_attack(
        targets_from_report(report, problem="benchmark_modular_triple"),
        "modular",
    )
    render_lean_comment(modular)
    render_yaml(modular)
    after = {path.relative_to(ostrowski) for path in ostrowski.rglob("*.lean")}
    assert before == after
    generated = ostrowski / "Generated.lean"
    assert not generated.exists()
