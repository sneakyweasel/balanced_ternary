"""Structured grey-loot retrieval. Never writes into a blind attack packet."""

from __future__ import annotations

from research_engine.memory.types import (
    BlindPacket,
    FailureClass,
    GreyLoot,
    GreyLootKind,
    LootEvidence,
)


def query_loot(
    items: tuple[GreyLoot, ...] | list[GreyLoot],
    *,
    kind: GreyLootKind | None = None,
    failure_class: FailureClass | None = None,
    bottleneck: str | None = None,
    evidence: LootEvidence | None = None,
    target: str | None = None,
) -> tuple[GreyLoot, ...]:
    """Post-run / planning query. Does not mutate AttackContext or BlindPacket."""

    found: list[GreyLoot] = []
    for item in items:
        if kind is not None and item.kind is not kind:
            continue
        if failure_class is not None and item.failure_class is not failure_class:
            continue
        if bottleneck is not None and item.bottleneck != bottleneck:
            continue
        if evidence is not None and item.evidence is not evidence:
            continue
        if target is not None and item.target != target:
            continue
        found.append(item)
    return tuple(found)


def assert_not_injected(packet: BlindPacket, loot: tuple[GreyLoot, ...] | list[GreyLoot]) -> None:
    blob = repr(packet.as_dict())
    for item in loot:
        if item.id and item.id in blob:
            raise AssertionError("grey loot leaked into blind packet")
        if item.statement and item.kind is GreyLootKind.COUNTEREXAMPLE and item.statement in blob:
            raise AssertionError("grey-loot statement leaked into blind packet")
