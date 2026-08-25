"""Typed attacks on a ``ProblemSpec``. Symbolic attacks are not here."""

from research_engine.attacks.affine import AffineInvariantAttack
from research_engine.attacks.block import BlockDynamicsAttack, BlockKind, classify_block
from research_engine.attacks.closure import ExhaustiveClosureAttack
from research_engine.attacks.counterexample import (
    ClosureLeakAttack,
    DescentLeakAttack,
    EquivalenceSeparationAttack,
    InvariantLeakAttack,
)
from research_engine.attacks.envelope import (
    EnvelopeComparison,
    ExactReachabilityResult,
    InvariantEnvelopeResult,
    compare_envelope_to_reachable,
    compute_exact_reachable,
    envelope_from_interval,
    find_invariant,
    reachable_from_ints,
)
from research_engine.attacks.factorization import FactorizationAttack
from research_engine.attacks.functional import FunctionalBoundAttack
from research_engine.attacks.modular import ModularInvariantAttack, coordinate_forcing_gcds
from research_engine.attacks.reconnaissance import ReconnaissanceAttack
from research_engine.attacks.result import (
    Attack,
    AttackContext,
    AttackResult,
    AttackStatus,
)
from research_engine.attacks.reverse import ReverseGeometryAttack
from research_engine.attacks.separation import BehavioralSeparationAttack, SeparationResult, separate_states
from research_engine.attacks.spectral import SpectralClassificationAttack
from research_engine.attacks.symmetry import SymmetryAttack, SymmetryCandidate, SymmetryResult, verify_symmetry

__all__ = [
    "AffineInvariantAttack",
    "Attack",
    "AttackContext",
    "AttackResult",
    "AttackStatus",
    "BehavioralSeparationAttack",
    "BlockDynamicsAttack",
    "BlockKind",
    "ClosureLeakAttack",
    "DescentLeakAttack",
    "EnvelopeComparison",
    "EquivalenceSeparationAttack",
    "ExactReachabilityResult",
    "ExhaustiveClosureAttack",
    "FactorizationAttack",
    "FunctionalBoundAttack",
    "InvariantEnvelopeResult",
    "InvariantLeakAttack",
    "ModularInvariantAttack",
    "ReconnaissanceAttack",
    "ReverseGeometryAttack",
    "SeparationResult",
    "SpectralClassificationAttack",
    "SymmetryAttack",
    "SymmetryCandidate",
    "SymmetryResult",
    "classify_block",
    "compare_envelope_to_reachable",
    "compute_exact_reachable",
    "coordinate_forcing_gcds",
    "envelope_from_interval",
    "find_invariant",
    "reachable_from_ints",
    "separate_states",
    "verify_symmetry",
]
