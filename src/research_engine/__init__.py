"""Problem-independent experimental dynamics engine.

R2: exact affine, block, phase, and trajectory primitives.
R3: reachability, co-reachability, live slices, and suffix feasibility.
R4: integer recurrences, lattice inverses, and linear forms.
R5: typed recon/modular/affine/reverse/functional/block attacks.
R6: hypotheses, negative knowledge, and a deterministic planner.
R8: five synthetic benchmarks with known exact behavior.
R9: theorem targets from exact certificates (not proofs, not sorry).

This package must not import ``bt.*`` or ``research.*``. Problem
adapters live under ``research.*`` and may import this engine.
"""

from research_engine.acceptance import (
    TerminalSpec,
    co_live_extensions,
    filter_terminal,
    forward_live_layers,
    is_co_live,
    is_suffix_accepted,
    live_extensions,
    live_from_spec,
    live_intersection,
)
from research_engine.algebra.lattices import (
    characteristic_polynomial,
    integer_affine_preimage,
    inverse_over_q,
    matrix_det,
)
from research_engine.algebra.linear_functionals import LinearFunctional, dot, left_multiply
from research_engine.algebra.recurrences import RecurrenceSpec
from research_engine.attacks import (
    AffineInvariantAttack,
    AttackContext,
    AttackResult,
    AttackStatus,
    BlockDynamicsAttack,
    BlockKind,
    FunctionalBoundAttack,
    ModularInvariantAttack,
    ReconnaissanceAttack,
    ReverseGeometryAttack,
)
from research_engine.planner import (
    AttackPlanner,
    DecisionKind,
    Hypothesis,
    HypothesisStatus,
    LedgerError,
    NegativeKnowledge,
    ResearchLedger,
)
from research_engine.core.affine_system import (
    AffineSystem,
    affine_step,
    apply_matrix,
    identity_matrix,
    iterate_affine_word,
    matrix_power,
    multiply_matrices,
)
from research_engine.core.block import (
    BlockAction,
    block_action,
    compose_blocks,
)
from research_engine.core.phase import IntPhase
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, Control, Matrix, SearchScope, State, Vector
from research_engine.core.trajectory import LazyTrajectory, Trajectory, simulate
from research_engine.reachability import (
    DynamicsResult,
    forward_search,
    reverse_closure,
    reverse_co_live_layers,
    reverse_predecessors_among,
    shortest_word,
)
from research_engine.verification import (
    TheoremTarget,
    attach_lean,
    render_lean_comment,
    render_yaml,
    target_from_result,
    targets_from_report,
)

__all__ = [
    "AffineSystem",
    "AffineInvariantAttack",
    "AttackContext",
    "AttackResult",
    "AttackStatus",
    "AttackPlanner",
    "BlockAction",
    "BlockDynamicsAttack",
    "BlockKind",
    "ClaimKind",
    "Control",
    "DecisionKind",
    "DynamicsResult",
    "FunctionalBoundAttack",
    "Hypothesis",
    "HypothesisStatus",
    "IntPhase",
    "LazyTrajectory",
    "LedgerError",
    "LinearFunctional",
    "Matrix",
    "ModularInvariantAttack",
    "NegativeKnowledge",
    "ProblemSpec",
    "ReconnaissanceAttack",
    "RecurrenceSpec",
    "ResearchLedger",
    "ReverseGeometryAttack",
    "SearchScope",
    "State",
    "TerminalSpec",
    "TheoremTarget",
    "Trajectory",
    "Vector",
    "affine_step",
    "apply_matrix",
    "attach_lean",
    "block_action",
    "characteristic_polynomial",
    "co_live_extensions",
    "compose_blocks",
    "dot",
    "filter_terminal",
    "forward_live_layers",
    "forward_search",
    "identity_matrix",
    "is_co_live",
    "is_suffix_accepted",
    "integer_affine_preimage",
    "inverse_over_q",
    "iterate_affine_word",
    "left_multiply",
    "live_extensions",
    "live_from_spec",
    "live_intersection",
    "matrix_det",
    "matrix_power",
    "multiply_matrices",
    "reverse_closure",
    "reverse_co_live_layers",
    "render_lean_comment",
    "render_yaml",
    "reverse_predecessors_among",
    "shortest_word",
    "simulate",
    "target_from_result",
    "targets_from_report",
]
