"""Problem-independent experimental dynamics engine.

R2: exact affine, block, phase, and trajectory primitives.
R3: reachability, co-reachability, live slices, and suffix feasibility.

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

__all__ = [
    "AffineSystem",
    "BlockAction",
    "ClaimKind",
    "Control",
    "DynamicsResult",
    "IntPhase",
    "LazyTrajectory",
    "Matrix",
    "ProblemSpec",
    "SearchScope",
    "State",
    "TerminalSpec",
    "Trajectory",
    "Vector",
    "affine_step",
    "apply_matrix",
    "block_action",
    "co_live_extensions",
    "compose_blocks",
    "filter_terminal",
    "forward_live_layers",
    "forward_search",
    "identity_matrix",
    "is_co_live",
    "is_suffix_accepted",
    "iterate_affine_word",
    "live_extensions",
    "live_from_spec",
    "live_intersection",
    "matrix_power",
    "multiply_matrices",
    "reverse_closure",
    "reverse_co_live_layers",
    "reverse_predecessors_among",
    "shortest_word",
    "simulate",
]
