"""Exact integer dynamics primitives for constrained affine systems."""

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
from research_engine.core.semantics import CertificateKind, ClaimKind, Control, Matrix, SearchScope, State, Vector
from research_engine.core.trajectory import LazyTrajectory, Trajectory, simulate

__all__ = [
    "AffineSystem",
    "BlockAction",
    "CertificateKind",
    "ClaimKind",
    "Control",
    "IntPhase",
    "LazyTrajectory",
    "Matrix",
    "ProblemSpec",
    "SearchScope",
    "State",
    "Trajectory",
    "Vector",
    "affine_step",
    "apply_matrix",
    "block_action",
    "compose_blocks",
    "identity_matrix",
    "iterate_affine_word",
    "matrix_power",
    "multiply_matrices",
    "simulate",
]
