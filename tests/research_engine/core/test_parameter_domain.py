"""Domain certification of reconstructed affine families. Ground truth is here."""

from __future__ import annotations

from pathlib import Path

from research_engine.attacks.parameter_domain import (
    DomainEvidence,
    ParameterDomainAttack,
    PredicateDirection,
    run_parameter_domain,
)
from research_engine.attacks.piecewise_affine import (
    PiecewiseAffineCensusAttack,
    run_piecewise_affine_census,
)
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.benchmarks.hidden_piecewise import (
    HiddenCongruenceASpec,
    HiddenMixedResidueSpec,
    HiddenOddPrimeClearSpec,
    HiddenPowerClearDSpec,
)
from research_engine.core.semantics import CertificateKind, SearchScope
from research_engine.planner.orchestrator import AttackPlanner, DEFAULT_ATTACK_ORDER
from tests.research_engine.core.test_planner import CountdownSpec


def _source_text() -> str:
    root = Path(__file__).resolve().parents[3]
    return "\n".join(
        (root / "src" / "research_engine" / "attacks" / name).read_text(encoding="utf-8")
        for name in ("parameter_domain.py", "piecewise_affine.py")
    )


def _certify(spec) -> object:
    census = PiecewiseAffineCensusAttack().run(spec, spec.attack_context())
    context = AttackContext(
        live_only=False,
        max_states=32,
        max_steps=spec.start_remaining,
        prior_results=(census,),
    )
    return run_parameter_domain(spec, context)


def test_attack_source_does_not_seed_collatz_structure():
    text = _source_text()
    lowered = text.lower()
    assert "collatz" not in lowered
    assert "syracuse" not in lowered
    assert "3 * n + 1" not in text
    assert "v_2(3" not in text


def test_countdown_is_inapplicable_without_census():
    spec = CountdownSpec()
    attack = ParameterDomainAttack()
    assert attack.applicable(spec, AttackContext()) is False


def test_a_maximal_v2_is_exact_not_mere_divisibility():
    spec = HiddenPowerClearDSpec()
    certificate = _certify(spec)
    assert certificate is not None
    assert certificate.family is not None
    assert certificate.family.base == 2
    assert certificate.family.p == 1 and certificate.family.r == 1
    assert certificate.domains
    assert all(item.direction == PredicateDirection.EXACT.value for item in certificate.domains)
    assert all(
        item.domain.kind == "maximal_divisibility" for item in certificate.domains
    )
    assert any(item.evidence == DomainEvidence.LEAN_CERTIFIED.value for item in certificate.domains)
    assert certificate.lean == "Problems.Engine.mul_pow_eq_iff_padicValInt"


def test_b_nonmaximal_divisibility_is_necessary_only():
    spec = HiddenPowerClearDSpec()
    certificate = _certify(spec)
    assert certificate is not None
    assert len(certificate.family.observed_k) >= 2
    assert certificate.divisibility_checks
    assert all(
        item.direction == PredicateDirection.NECESSARY_ONLY.value
        for item in certificate.divisibility_checks
    )
    assert all(
        item.domain.kind != "divisibility" or item.direction != PredicateDirection.EXACT.value
        for item in certificate.domains
    )


def test_c_odd_prime_base_is_not_secretly_two():
    spec = HiddenOddPrimeClearSpec()
    census = run_piecewise_affine_census(spec, spec.attack_context())
    assert census.census_kind == "PARAMETERIZED_CENSUS"
    assert census.family is not None
    assert census.family.base == 3
    certificate = _certify(spec)
    assert certificate is not None
    assert certificate.family.base == 3
    assert all(item.direction == PredicateDirection.EXACT.value for item in certificate.domains)
    assert all(item.domain.kind == "maximal_divisibility" for item in certificate.domains)


def test_d_mixed_residue_and_maximal():
    spec = HiddenMixedResidueSpec()
    census = run_piecewise_affine_census(spec, spec.attack_context())
    assert census.census_kind == "PARAMETERIZED_CENSUS"
    certificate = _certify(spec)
    assert certificate is not None
    mixed = [item for item in certificate.domains if item.domain.kind == "conjunction"]
    assert mixed
    assert all(item.direction == PredicateDirection.EXACT.value for item in mixed)
    kinds = {
        str(part.get("kind"))
        for item in mixed
        for part in item.domain.parameters.get("parts", ())
    }
    assert "residue_set" in kinds
    assert "maximal_divisibility" in kinds


def test_e_finite_congruence_table():
    spec = HiddenCongruenceASpec()
    census = run_piecewise_affine_census(spec, spec.attack_context())
    assert census.census_kind == "FINITE_CENSUS"
    certificate = _certify(spec)
    assert certificate is not None
    assert certificate.family is None
    assert len(certificate.domains) == 3
    assert all(item.direction == PredicateDirection.EXACT.value for item in certificate.domains)
    assert all(item.domain.kind == "congruence" for item in certificate.domains)


def test_f_unbounded_family_is_not_an_infinite_table():
    spec = HiddenPowerClearDSpec()
    census = run_piecewise_affine_census(spec, spec.attack_context())
    assert census.census_kind == "PARAMETERIZED_CENSUS"
    assert census.branches == ()
    certificate = _certify(spec)
    assert certificate is not None
    assert certificate.family is not None
    assert certificate.parameter_completeness != "finite"


def test_lean_identity_has_no_sorry():
    path = Path(__file__).resolve().parents[3] / "formal" / "Problems" / "Engine" / "ParameterDomain.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert "mul_pow_eq_iff_padicValInt" in text


def test_planner_chains_prior_results_and_does_not_inject_affine():
    spec = HiddenPowerClearDSpec()
    context = spec.attack_context()
    assert context.affine is None
    report = AttackPlanner().run(spec, context)
    names = [item.name for item in report.results]
    assert names[0] == "reconnaissance"
    assert names[1] == "piecewise_affine"
    assert names[2] == "parameter_domain"
    assert DEFAULT_ATTACK_ORDER.index("parameter_domain") == DEFAULT_ATTACK_ORDER.index("piecewise_affine") + 1
    domain = next(item for item in report.results if item.name == "parameter_domain")
    assert domain.status is AttackStatus.SUPPORTED
    assert domain.scope is SearchScope.EXACT
    assert domain.certificate_kind is CertificateKind.EXACT_ARITHMETIC_IDENTITY
    assert domain.evidence.get("reconstructed_affine") is None
    assert spec.attack_context().affine is None
    assert "map globality" in domain.claim
