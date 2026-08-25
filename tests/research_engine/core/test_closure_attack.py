"""Queue exhaustion is exact residual closure; a cap is not infinitude."""

from __future__ import annotations

from research_engine.attacks.closure import ExhaustiveClosureAttack
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.benchmarks.systems import FiniteClosureSpec, InfiniteTranslateSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, SearchScope
from tests.research_engine.core.test_attacks import CountdownSpec


def test_finite_collapse_is_exact_closure():
    result = ExhaustiveClosureAttack().run(FiniteClosureSpec(), AttackContext())
    assert result.status is AttackStatus.SUPPORTED
    assert result.scope is SearchScope.EXACT
    assert result.kind is ClaimKind.REACHABLE
    assert result.evidence["union_size"] == 1
    assert result.evidence["complete"] is True
    assert result.certificate_kind is CertificateKind.EXACT_CLOSURE


def test_infinite_translate_hits_the_cap():
    result = ExhaustiveClosureAttack().run(
        InfiniteTranslateSpec(),
        AttackContext(max_states=8),
    )
    assert result.status is AttackStatus.INCONCLUSIVE
    assert result.scope is SearchScope.BOUNDED
    assert result.kind is ClaimKind.REACHABLE
    assert result.evidence["complete"] is False
    assert "infinitude" in result.claim
    assert result.certificate_kind is None


def test_countdown_residual_is_not_faked_finite():
    result = ExhaustiveClosureAttack().run(
        CountdownSpec(),
        AttackContext(max_states=16),
    )
    assert result.status is AttackStatus.INCONCLUSIVE
    assert result.scope is SearchScope.BOUNDED
