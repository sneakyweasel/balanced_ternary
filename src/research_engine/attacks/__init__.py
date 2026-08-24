"""Typed attacks on a ``ProblemSpec``. Symbolic attacks are not here."""

from research_engine.attacks.affine import AffineInvariantAttack
from research_engine.attacks.block import BlockDynamicsAttack, BlockKind, classify_block
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
from research_engine.attacks.spectral import SpectralClassificationAttack

__all__ = [
    "AffineInvariantAttack",
    "Attack",
    "AttackContext",
    "AttackResult",
    "AttackStatus",
    "BlockDynamicsAttack",
    "BlockKind",
    "FunctionalBoundAttack",
    "ModularInvariantAttack",
    "ReconnaissanceAttack",
    "ReverseGeometryAttack",
    "SpectralClassificationAttack",
    "classify_block",
    "coordinate_forcing_gcds",
]
