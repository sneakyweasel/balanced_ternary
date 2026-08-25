"""Hidden 2-D vector-affine census. Ground truth lives here, not on the specs."""

from __future__ import annotations

from pathlib import Path

from research.euclidean_quotient.spec import euclidean_spec
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.attacks.vector_affine import (
    SAMPLE_RANGE,
    VectorAffineCensusAttack,
    compose_vector_steps,
    cycle_matrix_constraint,
    linear_system_status,
    run_vector_affine_census,
)
from research_engine.benchmarks.hidden_piecewise import HiddenCongruenceASpec
from research_engine.benchmarks.hidden_vector_affine import (
    HiddenDomainCoupledSpec,
    HiddenFalseAffineTrapSpec,
    HiddenFiniteAlphabetSpec,
    HiddenParameterizedMatrixSpec,
    HiddenParityShearSpec,
)
from research_engine.core.affine_system import AffineSystem, apply_matrix, identity_matrix
from research_engine.planner.orchestrator import AttackPlanner, DEFAULT_ATTACK_ORDER
from tests.research_engine.core.test_planner import CountdownSpec

EVEN_MATRIX = ((1, 0), (0, 1))
EVEN_OFFSET = (1, 0)
ODD_MATRIX = ((0, -1), (1, 0))
ODD_OFFSET = (0, 0)
SHEAR_DIRECTION = ((0, 1), (0, 0))
SHEAR_OFFSET = (1, 1)
COUPLED_OFFSET = (0, 0)
PARITY_EVEN = ((1, 1), (0, 1))
PARITY_ODD = ((1, 0), (1, 1))
EUCLID_DIRECTION = ((0, 0), (0, -1))
EUCLID_OFFSET = (0, 0)


def test_attack_source_does_not_seed_named_dynamics():
    text = Path(__file__).resolve().parents[3].joinpath(
        "src", "research_engine", "attacks", "vector_affine.py"
    ).read_text(encoding="utf-8")
    lowered = text.lower()
    assert "collatz" not in lowered
    assert "syracuse" not in lowered
    assert "euclidean" not in lowered
    assert "3 * n + 1" not in text


def test_one_d_and_explicit_affine_are_inapplicable():
    attack = VectorAffineCensusAttack()
    assert attack.applicable(HiddenCongruenceASpec(), AttackContext()) is False
    countdown = CountdownSpec()
    assert attack.applicable(countdown, AttackContext()) is False
    spec = HiddenFiniteAlphabetSpec()
    affine = AffineSystem(A=identity_matrix(2), translations={0: (0, 0)})
    assert attack.applicable(spec, AttackContext(affine=affine)) is False


def test_planner_keeps_scalar_chain_and_appends_vector():
    names = list(DEFAULT_ATTACK_ORDER)
    assert names[1] == "piecewise_affine"
    assert names[2] == "parameter_domain"
    assert names.index("vector_affine") == names.index("control_obstruction") + 1
    spec = HiddenCongruenceASpec()
    report = AttackPlanner().run(spec, spec.attack_context())
    ran = [item.name for item in report.results]
    assert ran[1] == "piecewise_affine"
    assert "vector_affine" not in ran
    assert any(item.attack == "vector_affine" for item in report.skipped)


def test_finite_alphabet_recovers_two_matrices():
    spec = HiddenFiniteAlphabetSpec()
    census = run_vector_affine_census(spec, spec.attack_context())
    matrices = {branch.matrix for branch in census.branches}
    offsets = {branch.offset for branch in census.branches}
    assert census.census_kind == "FINITE_CENSUS"
    assert EVEN_MATRIX in matrices
    assert ODD_MATRIX in matrices
    assert EVEN_OFFSET in offsets
    assert census.coverage >= 0.7
    domains = [item.get("domain") or {} for item in census.domains]
    assert any(item.get("kind") == "congruence" for item in domains)
    result = VectorAffineCensusAttack().run(spec, spec.attack_context())
    assert result.status is AttackStatus.OBSERVATION
    assert result.evidence.get("reconstructed_affine") is None


def test_parameterized_shear_recovers_family_and_class_obstruction():
    spec = HiddenParameterizedMatrixSpec()
    census = run_vector_affine_census(spec, spec.attack_context())
    assert census.census_kind == "PARAMETERIZED_CENSUS"
    assert census.family is not None
    assert census.family.direction in {SHEAR_DIRECTION, ((0, -1), (0, 0))}
    assert census.family.offset == SHEAR_OFFSET
    assert len(census.family.observed_k) >= 3
    region = census.family.region or {}
    assert region.get("kind") == "valuation"
    assert any(item.get("direction") in {"EXACT", "SUFFICIENT_ONLY"} for item in census.domains)
    assert census.relations
    scopes = {item.get("scope") for item in census.certificates}
    assert "WORD" in scopes
    assert "CLASS" in scopes


def test_domain_coupled_recovers_exact_predicate():
    spec = HiddenDomainCoupledSpec()
    census = run_vector_affine_census(spec, spec.attack_context())
    assert census.census_kind == "PARAMETERIZED_CENSUS"
    assert census.family is not None
    assert census.family.offset == COUPLED_OFFSET
    region = census.family.region or {}
    assert region.get("kind") == "valuation"
    assert region.get("form") == "x0-x1" or region.get("kind") == "valuation"
    assert any(item.get("direction") in {"EXACT", "SUFFICIENT_ONLY"} for item in census.domains)


def test_trap_refutes_global_identity():
    spec = HiddenFalseAffineTrapSpec()
    census = run_vector_affine_census(spec, spec.attack_context())
    identity = identity_matrix(2)
    ident_branches = [item for item in census.branches if item.matrix == identity and item.offset == (0, 0)]
    assert ident_branches
    assert all(item.status != "EXACTLY_CERTIFIED" for item in ident_branches)
    assert all(item.counterexamples for item in ident_branches)
    assert max(abs(part) for point in ident_branches[0].support for part in point) <= SAMPLE_RANGE


def test_composition_identity_and_cycle_constraint():
    matrix_a = ((1, 1), (0, 1))
    offset_a = (1, 0)
    matrix_c = ((0, -1), (1, 0))
    offset_c = (0, 1)
    composed, translation = compose_vector_steps(((matrix_a, offset_a), (matrix_c, offset_c)))
    expected_m = ((0, -1), (1, 1))
    expected_c = apply_matrix(matrix_c, offset_a)
    expected_c = (expected_c[0] + offset_c[0], expected_c[1] + offset_c[1])
    assert composed == expected_m
    assert translation == expected_c
    left, rhs = cycle_matrix_constraint(composed, translation)
    assert left == ((-1, -1), (1, 0))
    assert rhs == tuple(-part for part in translation)
    assert linear_system_status(left, rhs) in {"UNIQUE_NONINTEGRAL", "UNIQUE_INTEGER", "INCONSISTENT", "UNDERDETERMINED"}


def test_euclidean_consumer_recovers_quotient_family():
    spec = euclidean_spec()
    census = run_vector_affine_census(spec, spec.attack_context())
    assert census.census_kind == "PARAMETERIZED_CENSUS"
    assert census.family is not None
    assert census.family.offset == EUCLID_OFFSET
    assert census.family.direction in {EUCLID_DIRECTION, ((0, 0), (0, 1))}
    region = census.family.region or {}
    assert region.get("kind") == "quotient"
    assert {region.get("numerator"), region.get("denominator")} == {0, 1}
    assert any(item.get("direction") == "EXACT" for item in census.domains)
    assert census.relations
    report = AttackPlanner().run(spec, spec.attack_context())
    assert any(item.attack == "piecewise_affine" for item in report.skipped)
    assert any(item.name == "vector_affine" for item in report.results)


def test_unrelated_parity_shear_consumes_same_attack():
    spec = HiddenParityShearSpec()
    census = run_vector_affine_census(spec, spec.attack_context())
    matrices = {branch.matrix for branch in census.branches}
    assert PARITY_EVEN in matrices
    assert PARITY_ODD in matrices
    assert census.census_kind in {"FINITE_CENSUS", "PARAMETERIZED_CENSUS"}
    domains = [item.get("domain") or {} for item in census.domains]
    assert any(item.get("kind") == "congruence" and item.get("form") == "x0+x1" for item in domains)
    src = Path(__file__).resolve().parents[3] / "src" / "research_engine" / "benchmarks" / "hidden_vector_affine.py"
    text = src.read_text(encoding="utf-8")
    assert "a % b" not in text
    assert "euclidean" not in text.lower()


def test_lean_vector_affine_has_no_sorry():
    path = Path(__file__).resolve().parents[3] / "formal" / "Problems" / "Engine" / "VectorAffine.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert "compose_two_vector_affine" in text
    assert "cycle_of_vector_affine" in text


def test_problem_dossier_and_descriptor():
    from research.open_problems import get_problem
    from research.vector_affine.problem import PROBLEM

    assert get_problem("vector_affine") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/vector_affine.md",)
    dossier = Path(__file__).resolve().parents[3] / "docs" / "problems" / "vector_affine.md"
    text = dossier.read_text(encoding="utf-8")
    assert "## Decision" in text
    assert "`PARK`" in text
    assert "EuclideanControl" not in text or "no `EuclideanControl`" in text


def test_vector_recovery_continues_under_medium_delta():
    from research_engine.diagnosis.decision import decide_research
    from research_engine.diagnosis.types import (
        DeltaLevel,
        FamilyStatus,
        RegimeFingerprint,
        RegimeSimilarity,
        ResearchDecision,
        StructuralDelta,
    )
    from research_engine.planner.orchestrator import PlannerReport

    fingerprint = RegimeFingerprint(
        state_space_type="INTEGER_VECTOR",
        control_structure="SINGLETON",
        modular_structure="INAPPLICABLE",
        spectral_structure="INAPPLICABLE",
        block_structure="INAPPLICABLE",
        numerical_contraction="FINITE_CONTRACTING",
        eventual_region="FINITE_SEED_CLOSURE",
        piecewise_affine_structure="PARAMETERIZED",
        latent_control="PARAMETERIZED",
        parameter_domain="EXACT",
        latent_control_algebra="EXPLOITABLE",
        latent_control_obstruction="CLASS",
        affine_control_type="MATRIX_PARAMETERIZED",
    )
    similarity = RegimeSimilarity(
        score=0.6,
        compared_dimensions=("numerical_contraction",),
        matching_dimensions=("numerical_contraction",),
    )
    delta = StructuralDelta(
        level=DeltaLevel.MEDIUM,
        differing_dimensions=(("state_space_type", "INTEGER_1D", "INTEGER_VECTOR"),),
        similarity=similarity,
    )
    decision, reason = decide_research(
        fingerprint,
        FamilyStatus.ACTIVE,
        delta,
        PlannerReport(results=(), skipped=(), hypotheses=(), blocked_jumps=()),
    )
    assert decision is ResearchDecision.CONTINUE
    assert "latent parameterized family" in reason
