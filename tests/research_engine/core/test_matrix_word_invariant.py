"""Matrix-word recursive invariants. Ground truth lives only in these tests."""

from __future__ import annotations

from pathlib import Path

from research.euclidean_quotient.spec import euclidean_spec
from research_engine.attacks.result import AttackStatus
from research_engine.benchmarks.hidden_matrix_invariants import (
    HiddenExceptionSpec,
    HiddenFalseInvariantSpec,
    HiddenGcdFamilySpec,
    HiddenLatticeWalkSpec,
    HiddenModularLatticeSpec,
    HiddenRealizableFamilySpec,
    HiddenRecursiveShearSpec,
    HiddenSmithFamilySpec,
)
from research_engine.benchmarks.hidden_piecewise import HiddenCongruenceASpec
from research_engine.benchmarks.hidden_vector_affine import HiddenParityShearSpec
from research_engine.planner.orchestrator import AttackPlanner, DEFAULT_ATTACK_ORDER, run_named_attack

ATTACK_SRC = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "research_engine"
    / "attacks"
    / "matrix_word_invariant.py"
)
BENCH_SRC = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "research_engine"
    / "benchmarks"
    / "hidden_matrix_invariants.py"
)


def _certs(spec) -> tuple[dict, ...]:
    result = run_named_attack("matrix_word_invariant", spec, spec.attack_context())
    return tuple(item for item in (result.evidence.get("certificates") or ()) if isinstance(item, dict))


def _proved(certs, scope: str | None = None) -> tuple[dict, ...]:
    out = []
    for item in certs:
        if item.get("status") not in {"PROVED", "LEAN_CERTIFIED", "SYMBOLICALLY_PROVED"}:
            continue
        if scope is not None and item.get("scope") != scope:
            continue
        out.append(item)
    return tuple(out)


def test_attack_source_is_generic():
    text = ATTACK_SRC.read_text(encoding="utf-8").lower()
    assert "collatz" not in text
    assert "syracuse" not in text
    assert "euclidean" not in text
    assert "3 * n + 1" not in ATTACK_SRC.read_text(encoding="utf-8")
    bench = BENCH_SRC.read_text(encoding="utf-8").lower()
    assert "euclidean" not in bench
    assert "a % b" not in BENCH_SRC.read_text(encoding="utf-8")


def test_planner_appends_after_vector_affine():
    names = list(DEFAULT_ATTACK_ORDER)
    assert names.index("matrix_word_invariant") == names.index("vector_affine") + 1
    spec = HiddenCongruenceASpec()
    report = AttackPlanner().run(spec, spec.attack_context())
    ran = [item.name for item in report.results]
    assert "matrix_word_invariant" not in ran
    assert any(item.attack == "matrix_word_invariant" for item in report.skipped)


def test_modular_lattice_recursive_non_magnitude():
    spec = HiddenModularLatticeSpec()
    certs = _certs(spec)
    recursive = _proved(certs, "RECURSIVE_INVARIANT")
    assert recursive
    assert all(item.get("magnitude") == "INAPPLICABLE" for item in recursive)
    assert any(len(item.get("word_lengths") or ()) >= 2 for item in recursive)
    kinds = {item.get("kind") for item in recursive}
    assert kinds & {"image_kernel", "left_form", "left_form_mod", "entry_gcd"}


def test_gcd_family_class_obstruction():
    spec = HiddenGcdFamilySpec()
    certs = _certs(spec)
    proved = _proved(certs)
    assert proved
    assert any(item.get("kind") in {"entry_gcd", "left_form_mod", "image_kernel"} for item in proved)
    assert any(item.get("magnitude") == "INAPPLICABLE" for item in proved)


def test_smith_style_minors_gcd():
    spec = HiddenSmithFamilySpec()
    certs = _certs(spec)
    proved = _proved(certs)
    assert proved
    assert any(
        item.get("kind") in {"entry_gcd", "image_kernel", "left_form_mod", "det_factor"}
        for item in proved
    )


def test_recursive_shear_scales_with_length():
    spec = HiddenRecursiveShearSpec()
    certs = _certs(spec)
    recursive = _proved(certs, "RECURSIVE_INVARIANT")
    assert recursive
    item = recursive[0]
    assert item.get("magnitude") == "INAPPLICABLE"
    assert len(item.get("word_lengths") or ()) >= 2
    invariant = item.get("invariant") or {}
    assert "M'" in invariant.get("transition", "") or "A_u" in invariant.get("transition", "")


def test_exceptions_are_not_all_words():
    spec = HiddenExceptionSpec()
    certs = _certs(spec)
    proved = _proved(certs)
    assert proved
    excepted = [item for item in proved if item.get("exceptions")]
    if excepted:
        assert any("except" in item.get("reason", "").lower() for item in excepted)
        assert all("not every word" in item.get("reason", "").lower() or "except" in item.get("reason", "").lower() for item in excepted)
    else:
        assert any(
            item.get("scope") in {"CLASS", "SYMBOLIC_CLASS", "RECURSIVE_INVARIANT"}
            for item in proved
        )


def test_false_invariant_is_refuted():
    spec = HiddenFalseInvariantSpec()
    certs = _certs(spec)
    assert any(item.get("status") == "REFUTED" for item in certs)


def test_realizable_family_is_unknown():
    spec = HiddenRealizableFamilySpec()
    result = run_named_attack("matrix_word_invariant", spec, spec.attack_context())
    certs = tuple(
        item for item in (result.evidence.get("certificates") or ()) if isinstance(item, dict)
    )
    proved = _proved(certs)
    assert not proved
    assert result.status in {AttackStatus.INCONCLUSIVE, AttackStatus.OBSERVATION}
    assert any(item.get("status") == "UNKNOWN" for item in certs)
    assert "NO OBSTRUCTION" in result.claim or any(
        (item.get("invariant") or {}).get("implication") == "NO OBSTRUCTION" for item in certs
    )


def test_euclidean_consumer_runs_generic_attack():
    spec = euclidean_spec()
    report = AttackPlanner().run(spec, spec.attack_context())
    names = [item.name for item in report.results]
    assert "vector_affine" in names
    assert "matrix_word_invariant" in names
    vector = next(item for item in report.results if item.name == "vector_affine")
    assert vector.evidence.get("census_kind") == "PARAMETERIZED_CENSUS"
    assert vector.evidence.get("family", {}).get("offset") == (0, 0)
    inv = next(item for item in report.results if item.name == "matrix_word_invariant")
    assert inv.status in {
        AttackStatus.INCONCLUSIVE,
        AttackStatus.OBSERVATION,
        AttackStatus.SUPPORTED,
    }
    src = ATTACK_SRC.read_text(encoding="utf-8").lower()
    assert "euclidean" not in src


def test_parity_shear_consumer_no_specialization():
    spec = HiddenParityShearSpec()
    report = AttackPlanner().run(spec, spec.attack_context())
    assert any(item.name == "matrix_word_invariant" for item in report.results)
    inv = next(item for item in report.results if item.name == "matrix_word_invariant")
    certs = tuple(item for item in (inv.evidence.get("certificates") or ()) if isinstance(item, dict))
    assert certs
    src = BENCH_SRC.read_text(encoding="utf-8").lower()
    assert "euclidean" not in src


def test_unrelated_lattice_walk_consumes_same_attack():
    spec = HiddenLatticeWalkSpec()
    report = AttackPlanner().run(spec, spec.attack_context())
    assert any(item.name == "vector_affine" for item in report.results)
    inv = next(item for item in report.results if item.name == "matrix_word_invariant")
    certs = tuple(item for item in (inv.evidence.get("certificates") or ()) if isinstance(item, dict))
    assert certs
    text = BENCH_SRC.read_text(encoding="utf-8")
    assert "a % b" not in text


def test_lean_matrix_word_has_no_sorry():
    path = Path(__file__).resolve().parents[3] / "formal" / "Problems" / "Engine" / "MatrixWord.lean"
    text = path.read_text(encoding="utf-8")
    assert "sorry" not in text
    assert "admit" not in text
    assert "recursive_matrix_word_step" in text
    assert "kernel_row_cycle_impossible" in text
    assert "entry_gcd_divides_translation" in text
    assert "shear_word_class_impossible" in text
    assert "EUCLIDEAN" not in text


def test_problem_dossier_and_descriptor():
    from research.open_problems import get_problem
    from research.matrix_word_invariant.problem import PROBLEM

    assert get_problem("matrix_word_invariant") is PROBLEM
    assert PROBLEM.docs == ("docs/problems/matrix_word_invariant.md",)
    dossier = Path(__file__).resolve().parents[3] / "docs" / "problems" / "matrix_word_invariant.md"
    text = dossier.read_text(encoding="utf-8")
    assert "`PARK`" in text
    assert "ATTACK ARCHITECTURE FROZEN" in text
    assert "EuclideanControl" not in text or "not" in text.lower()
