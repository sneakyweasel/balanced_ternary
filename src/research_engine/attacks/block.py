"""Exact classification of T_B. Spectral radius is not used."""

from __future__ import annotations

from enum import Enum

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.core.affine_system import identity_matrix
from research_engine.core.block import BlockAction, block_action
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope


class BlockKind(str, Enum):
    IDENTITY = "IDENTITY"
    ORIGIN_RESET = "ORIGIN_RESET"
    TRANSLATION = "TRANSLATION"
    AFFINE = "AFFINE"


def classify_block(action: BlockAction) -> BlockKind:
    ident = identity_matrix(action.dimension)
    zero = tuple(0 for _ in range(action.dimension))
    if action.matrix == ident and action.translation == zero:
        return BlockKind.IDENTITY
    if action.translation == zero:
        return BlockKind.ORIGIN_RESET
    if action.matrix == ident:
        return BlockKind.TRANSLATION
    return BlockKind.AFFINE


class BlockDynamicsAttack:
    name = "block"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        del spec
        return context.block is not None or (context.affine is not None and context.word is not None)

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        del spec
        action = context.block
        if action is None:
            if context.affine is None or context.word is None:
                return inapplicable(
                    self.name,
                    "block attack needs BlockAction or AffineSystem plus word",
                    ClaimKind.REACHABLE,
                )
            action = block_action(context.affine, context.word)
        kind = classify_block(action)
        claim = (
            f"T_B is {kind.value} with length {action.length} and T_B(0)={action.translation}; "
            "this is map geometry, not live infinitude"
        )
        return AttackResult(
            name=self.name,
            status=AttackStatus.SUPPORTED,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.EXACT,
            claim=claim,
            evidence={
                "block_kind": kind.value,
                "length": action.length,
                "translation": action.translation,
                "fixes_origin": action.translation == tuple(0 for _ in range(action.dimension)),
            },
            certificates=({"block_kind": kind.value, "translation": action.translation},),
            recommended_next_attacks=("reverse", "reconnaissance"),
        )
