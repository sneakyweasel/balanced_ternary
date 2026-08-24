"""Spectral companion classification is not live infinitude."""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.attacks.spectral import SpectralClassificationAttack
from research_engine.benchmarks.pipeline import run_benchmark
from research_engine.core.affine_system import AffineSystem
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import ClaimKind, SearchScope


@dataclass(frozen=True)
class DummySpec:
    name: str = "spectral_toy"
    dimension: int = 3
    initial_state: tuple[int, ...] = (0, 0, 0)

    def transition(self, state, control, phase):
        del control, phase
        return state

    def legal_controls(self, state, phase):
        del state, phase
        return ()

    def next_phase(self, phase, control):
        del control
        return phase

    def is_terminal(self, state, phase):
        del state, phase
        return True

    def is_accepting(self, state, phase):
        del state, phase
        return True

    def initial_phase(self):
        return IntPhase(0)

    def canonicalize(self, state):
        return tuple(state)


def test_np_companion_is_exact_perron_non_pisot_not_live():
    affine = AffineSystem(
        A=((0, 0, 3), (1, 0, 1), (0, 1, 2)),
        translations={0: (0, 0, 0)},
    )
    result = SpectralClassificationAttack().run(
        DummySpec(),
        AttackContext(affine=affine),
    )
    assert result.status is AttackStatus.SUPPORTED
    assert result.scope is SearchScope.EXACT
    assert result.kind is ClaimKind.REACHABLE
    assert result.kind is not ClaimKind.LIVE
    assert result.evidence["certificate"]["perron_non_pisot"]
    assert result.evidence["floats_are_labels_only"] is True
    assert result.evidence["root_moduli_labels"]
    assert "live infinitude" in result.claim


def test_pisot_companion_is_exact_and_unlinked_to_live():
    affine = AffineSystem(
        A=((0, 0, 1), (1, 0, 1), (0, 1, 2)),
        translations={0: (0, 0, 0)},
    )
    result = SpectralClassificationAttack().run(
        DummySpec(),
        AttackContext(affine=affine),
    )
    assert result.status is AttackStatus.SUPPORTED
    assert result.evidence["certificate"]["pisot"]
    assert result.kind is not ClaimKind.LIVE


def test_benchmark_d_spectral_is_not_a_cubic_and_not_live():
    report = run_benchmark("D")
    spectral = next(item for item in report.results if item.name == "spectral")
    assert spectral.status is AttackStatus.OBSERVATION
    assert spectral.kind is ClaimKind.REACHABLE
    assert spectral.kind is not ClaimKind.LIVE
    assert spectral.scope is SearchScope.EXACT
    modular = next(item for item in report.results if item.name == "modular")
    assert modular.status is AttackStatus.SUPPORTED
    assert modular.kind is ClaimKind.REACHABLE
