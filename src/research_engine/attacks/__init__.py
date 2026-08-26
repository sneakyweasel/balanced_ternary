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
from research_engine.attacks.control_obstruction import (
    ControlObstructionAttack,
    ControlObstructionCertificate,
    length_one_divisor_class,
    run_control_obstruction,
)
from research_engine.attacks.control_word import (
    ComposedAffineRelation,
    ControlComposition,
    ControlWord,
    ControlWordAttack,
    ControlWordConstraint,
    compose_affine_steps,
    cycle_constraint,
    run_control_word,
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
from research_engine.attacks.parameter_domain import (
    AffineFamily,
    AffineFamilyCertificate,
    DomainCertificate,
    ParameterDomain,
    ParameterDomainAttack,
    run_parameter_domain,
)
from research_engine.attacks.piecewise_affine import (
    AffineBranch,
    BranchRegion,
    CensusKind,
    LatentControl,
    PiecewiseAffineCensus,
    PiecewiseAffineCensusAttack,
    candidate_affine_laws,
    infer_region,
    run_piecewise_affine_census,
)
from research_engine.attacks.reconnaissance import ReconnaissanceAttack
from research_engine.attacks.matrix_word_invariant import (
    MatrixWordCertificate,
    MatrixWordInvariant,
    MatrixWordInvariantAttack,
    run_matrix_word_invariant,
)
from research_engine.attacks.vector_affine import (
    VectorAffineCensus,
    VectorAffineCensusAttack,
    compose_vector_steps,
    cycle_matrix_constraint,
    run_vector_affine_census,
)
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
    "AffineBranch",
    "AffineFamily",
    "AffineFamilyCertificate",
    "AffineInvariantAttack",
    "Attack",
    "AttackContext",
    "AttackResult",
    "AttackStatus",
    "BehavioralSeparationAttack",
    "BlockDynamicsAttack",
    "BlockKind",
    "BranchRegion",
    "CensusKind",
    "ClosureLeakAttack",
    "ComposedAffineRelation",
    "ControlComposition",
    "ControlObstructionAttack",
    "ControlObstructionCertificate",
    "ControlWord",
    "ControlWordAttack",
    "ControlWordConstraint",
    "compose_affine_steps",
    "cycle_constraint",
    "run_control_word",
    "DescentLeakAttack",
    "DomainCertificate",
    "EnvelopeComparison",
    "EquivalenceSeparationAttack",
    "ExactReachabilityResult",
    "ExhaustiveClosureAttack",
    "FactorizationAttack",
    "FunctionalBoundAttack",
    "InvariantEnvelopeResult",
    "InvariantLeakAttack",
    "LatentControl",
    "ModularInvariantAttack",
    "ParameterDomain",
    "ParameterDomainAttack",
    "PiecewiseAffineCensus",
    "PiecewiseAffineCensusAttack",
    "ReconnaissanceAttack",
    "ReverseGeometryAttack",
    "SeparationResult",
    "SpectralClassificationAttack",
    "SymmetryAttack",
    "SymmetryCandidate",
    "SymmetryResult",
    "candidate_affine_laws",
    "classify_block",
    "compare_envelope_to_reachable",
    "compute_exact_reachable",
    "coordinate_forcing_gcds",
    "envelope_from_interval",
    "find_invariant",
    "reachable_from_ints",
    "infer_region",
    "run_parameter_domain",
    "run_piecewise_affine_census",
    "run_vector_affine_census",
    "run_matrix_word_invariant",
    "separate_states",
    "verify_symmetry",
    "VectorAffineCensus",
    "VectorAffineCensusAttack",
    "MatrixWordCertificate",
    "MatrixWordInvariant",
    "MatrixWordInvariantAttack",
    "compose_vector_steps",
    "cycle_matrix_constraint",
]
