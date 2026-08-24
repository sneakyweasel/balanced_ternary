"""Ostrowski runners for the six engine attacks.

Energy, place values, and the recurrence word stay in other Ostrowski modules.
"""

from __future__ import annotations

from research.ostrowski.spec import ostrowski_spec
from research.ostrowski.system import OstrowskiSystem
from research.ostrowski.zero_value_kernel import SHORTEST_NONRESET
from research_engine.algebra.linear_functionals import LinearFunctional
from research_engine.attacks.affine import AffineInvariantAttack
from research_engine.attacks.block import BlockDynamicsAttack
from research_engine.attacks.functional import FunctionalBoundAttack
from research_engine.attacks.modular import ModularInvariantAttack
from research_engine.attacks.reconnaissance import ReconnaissanceAttack
from research_engine.attacks.result import AttackResult
from research_engine.attacks.reverse import ReverseGeometryAttack
from research_engine.core.phase import IntPhase
from research_engine.core.semantics import State


def reconnaissance(start_remaining: int, system: OstrowskiSystem | None = None) -> AttackResult:
    spec = ostrowski_spec(start_remaining, system)
    return ReconnaissanceAttack().run(spec, spec.attack_context())


def modular(system: OstrowskiSystem | None = None) -> AttackResult:
    spec = ostrowski_spec(0, system)
    return ModularInvariantAttack().run(spec, spec.attack_context())


def affine_region(
    region: frozenset[State],
    remaining: int,
    system: OstrowskiSystem | None = None,
) -> AttackResult:
    spec = ostrowski_spec(remaining, system)
    return AffineInvariantAttack().run(
        spec,
        spec.attack_context(candidate_region=region, phases=(IntPhase(remaining),)),
    )


def reverse_origin(max_depth: int | None = 3) -> AttackResult:
    """Bounded reverse basin of the origin for ``Γ_NP``. Not ``L_0``."""
    from research.ostrowski.reverse_map import integer_preimage

    spec = ostrowski_spec(0)
    alphabet = spec.affine_system().controls

    def predecessors(state: State) -> tuple[State, ...]:
        found: list[State] = []
        for w in alphabet:
            pred = integer_preimage((state[0], state[1], state[2]), w)
            if pred is not None:
                found.append(pred)
        return tuple(found)

    return ReverseGeometryAttack().run(
        spec,
        spec.attack_context(
            reverse_seeds=((0, 0, 0),),
            reverse_preimage=predecessors,
            reverse_max_depth=max_depth,
        ),
    )


def functional_s3(start_remaining: int, system: OstrowskiSystem | None = None) -> AttackResult:
    spec = ostrowski_spec(start_remaining, system)
    return FunctionalBoundAttack().run(
        spec,
        spec.attack_context(functional=LinearFunctional((0, 0, 1))),
    )


def hub_block(system: OstrowskiSystem | None = None) -> AttackResult:
    spec = ostrowski_spec(2, system)
    return BlockDynamicsAttack().run(
        spec,
        spec.attack_context(word=SHORTEST_NONRESET),
    )
