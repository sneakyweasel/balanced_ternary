"""Typed attacks keep ClaimKind and SearchScope; a census is not infinitude."""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.algebra.lattices import integer_affine_preimage
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.affine import AffineInvariantAttack
from research_engine.attacks.block import BlockDynamicsAttack, BlockKind
from research_engine.attacks.functional import FunctionalBoundAttack
from research_engine.attacks.modular import ModularInvariantAttack, coordinate_forcing_gcds
from research_engine.attacks.reconnaissance import ReconnaissanceAttack
from research_engine.attacks.result import AttackContext, AttackStatus
from research_engine.attacks.reverse import ReverseGeometryAttack
from research_engine.core.affine_system import AffineSystem
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import ClaimKind, SearchScope


@dataclass(frozen=True)
class CountdownSpec:
    name: str = "countdown_toy"
    dimension: int = 1
    initial_state: tuple[int, ...] = (0,)
    start_remaining: int = 2

    def transition(self, state: tuple[int, ...], control: int, phase: IntPhase) -> tuple[int, ...]:
        del phase
        return (state[0] + control,)

    def legal_controls(self, state: tuple[int, ...], phase: IntPhase) -> tuple[int, ...]:
        del state
        if phase.value <= 0:
            return ()
        return (-1, 0, 1)

    def next_phase(self, phase: IntPhase, control: int) -> IntPhase:
        del control
        return IntPhase(phase.value - 1)

    def is_terminal(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        del state
        return True

    def is_accepting(self, state: tuple[int, ...], phase: IntPhase) -> bool:
        return phase.value == 0 and state[0] == 0

    def initial_phase(self) -> IntPhase:
        return IntPhase(self.start_remaining)

    def canonicalize(self, state: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(state)


def tripling_system() -> AffineSystem:
    return AffineSystem(A=((3,),), translations={0: (0,)})


def doubling_system() -> AffineSystem:
    return AffineSystem(A=((2, 0), (0, 2)), translations={0: (0, 0), 1: (1, 0)})


def test_reconnaissance_is_bounded_observation_not_infinitude():
    result = ReconnaissanceAttack().run(CountdownSpec(), AttackContext(live_only=True))
    assert result.status == AttackStatus.OBSERVATION
    assert result.scope == SearchScope.BOUNDED
    assert result.kind == ClaimKind.LIVE_SLICE
    assert result.evidence["union_size"] > result.evidence["terminal_image_size"]
    assert "infinitude" in result.claim


def test_modular_forcing_is_exact_map_law():
    spec = CountdownSpec()
    missing = ModularInvariantAttack().run(spec, AttackContext())
    assert missing.status == AttackStatus.INAPPLICABLE
    tripling = ModularInvariantAttack().run(spec, AttackContext(affine=tripling_system()))
    assert tripling.status == AttackStatus.SUPPORTED
    assert tripling.scope == SearchScope.EXACT
    assert tripling.kind == ClaimKind.REACHABLE
    assert coordinate_forcing_gcds(tripling_system()) == (3,)
    doubling = ModularInvariantAttack().run(spec, AttackContext(affine=doubling_system()))
    assert doubling.status == AttackStatus.SUPPORTED
    assert coordinate_forcing_gcds(doubling_system())[1] == 2
    assert doubling.kind != ClaimKind.LIVE


def test_affine_region_leak_is_refuted_not_an_invariant():
    spec = CountdownSpec()
    leak = AffineInvariantAttack().run(
        spec,
        AttackContext(candidate_region=frozenset({(0,)})),
    )
    assert leak.status == AttackStatus.REFUTED
    assert leak.scope == SearchScope.BOUNDED
    vacuous = AffineInvariantAttack().run(
        CountdownSpec(start_remaining=0),
        AttackContext(candidate_region=frozenset({(0,)})),
    )
    assert vacuous.status == AttackStatus.OBSERVATION
    assert "not an invariant theorem" in vacuous.claim


def test_reverse_basin_is_co_reachable_not_live():
    spec = CountdownSpec()

    def doubling_preds(state: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
        found = integer_affine_preimage(((2,),), (0,), state)
        return () if found is None else (found,)

    exact = ReverseGeometryAttack().run(
        spec,
        AttackContext(reverse_seeds=((0,),), reverse_preimage=doubling_preds),
    )
    assert exact.status == AttackStatus.SUPPORTED
    assert exact.kind == ClaimKind.CO_REACHABLE
    assert exact.scope == SearchScope.EXACT
    assert exact.evidence["union_size"] == 1

    def shift_preds(state: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
        x = state[0]
        return ((x - 1,), (x,), (x + 1,))

    bounded = ReverseGeometryAttack().run(
        spec,
        AttackContext(
            reverse_seeds=((0,),),
            reverse_preimage=shift_preds,
            reverse_max_depth=2,
        ),
    )
    assert bounded.status == AttackStatus.OBSERVATION
    assert bounded.scope == SearchScope.BOUNDED
    assert bounded.kind == ClaimKind.CO_REACHABLE


def test_functional_sample_max_is_not_supported():
    spec = CountdownSpec()
    result = FunctionalBoundAttack().run(
        spec,
        AttackContext(functional=LinearFunctional((1,)), live_only=True),
    )
    assert result.status == AttackStatus.REFUTED
    assert result.scope == SearchScope.BOUNDED
    assert result.status != AttackStatus.SUPPORTED


def test_block_classification_is_exact_and_avoids_spectral_radius():
    spec = CountdownSpec()
    identity = BlockDynamicsAttack().run(
        spec,
        AttackContext(affine=doubling_system(), word=()),
    )
    reset = BlockDynamicsAttack().run(
        spec,
        AttackContext(affine=doubling_system(), word=(0,)),
    )
    moved = BlockDynamicsAttack().run(
        spec,
        AttackContext(affine=doubling_system(), word=(1,)),
    )
    assert identity.evidence["block_kind"] == BlockKind.IDENTITY.value
    assert reset.evidence["block_kind"] == BlockKind.ORIGIN_RESET.value
    assert moved.evidence["block_kind"] == BlockKind.AFFINE.value
    assert identity.status == reset.status == moved.status == AttackStatus.SUPPORTED
    assert identity.scope == SearchScope.EXACT
    assert identity.kind == ClaimKind.REACHABLE
