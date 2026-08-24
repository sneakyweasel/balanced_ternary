"""Ostrowski runners for the six engine attacks.

Energy, place values, and the recurrence word stay in other Ostrowski modules.
"""

from __future__ import annotations

from research.ostrowski.spec import ostrowski_affine, ostrowski_spec
from research.ostrowski.system import OstrowskiSystem
from research.ostrowski.zero_value_kernel import SHORTEST_NONRESET
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.affine import AffineInvariantAttack
from research_engine.attacks.block import BlockDynamicsAttack
from research_engine.attacks.functional import FunctionalBoundAttack
from research_engine.attacks.modular import ModularInvariantAttack
from research_engine.attacks.reconnaissance import ReconnaissanceAttack
from research_engine.attacks.result import AttackContext, AttackResult
from research_engine.attacks.reverse import ReverseGeometryAttack
from research_engine.core.semantics import State


def reconnaissance(start_remaining: int, system: OstrowskiSystem | None = None) -> AttackResult:
    return ReconnaissanceAttack().run(
        ostrowski_spec(start_remaining, system),
        AttackContext(live_only=True),
    )


def modular(system: OstrowskiSystem | None = None) -> AttackResult:
    affine = ostrowski_affine(system)
    return ModularInvariantAttack().run(
        ostrowski_spec(0, system),
        AttackContext(affine=affine),
    )


def affine_region(
    region: frozenset[State],
    remaining: int,
    system: OstrowskiSystem | None = None,
) -> AttackResult:
    from research_engine.core.phase import IntPhase

    spec = ostrowski_spec(remaining, system)
    return AffineInvariantAttack().run(
        spec,
        AttackContext(candidate_region=region, phases=(IntPhase(remaining),)),
    )


def reverse_origin(max_depth: int | None = 3) -> AttackResult:
    """Bounded reverse basin of the origin for ``Γ_NP``. Not ``L_0``."""
    from research.ostrowski.reverse_map import integer_preimage

    alphabet = ostrowski_affine().controls

    def predecessors(state: State) -> tuple[State, ...]:
        found: list[State] = []
        for w in alphabet:
            pred = integer_preimage((state[0], state[1], state[2]), w)
            if pred is not None:
                found.append(pred)
        return tuple(found)

    return ReverseGeometryAttack().run(
        ostrowski_spec(0),
        AttackContext(
            reverse_seeds=((0, 0, 0),),
            reverse_preimage=predecessors,
            reverse_max_depth=max_depth,
        ),
    )


def functional_s3(start_remaining: int, system: OstrowskiSystem | None = None) -> AttackResult:
    return FunctionalBoundAttack().run(
        ostrowski_spec(start_remaining, system),
        AttackContext(functional=LinearFunctional((0, 0, 1)), live_only=True),
    )


def hub_block(system: OstrowskiSystem | None = None) -> AttackResult:
    return BlockDynamicsAttack().run(
        ostrowski_spec(2, system),
        AttackContext(affine=ostrowski_affine(system), word=SHORTEST_NONRESET),
    )
