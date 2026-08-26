"""Structured grey-loot retrieval. Never writes into a blind attack packet."""

from __future__ import annotations

from typing import Any

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
    blob = repr(packet.as_dict()) + repr(packet.attack_payload())
    for item in loot:
        if item.id and item.id in blob:
            raise AssertionError("grey loot leaked into blind packet")
        if item.statement and item.kind is GreyLootKind.COUNTEREXAMPLE and item.statement in blob:
            raise AssertionError("grey-loot statement leaked into blind packet")


def assert_hypotheses_not_injected(
    packet: BlindPacket,
    hypotheses: tuple[Any, ...] | list[Any],
) -> None:
    """A hypothesis born on target A must not enter target B's attack payload."""

    payload = repr(packet.attack_payload())
    spec = packet.spec_name
    for item in hypotheses:
        source = getattr(item, "source_target", "") or getattr(item, "target", "")
        if source in {spec, ""}:
            continue
        hyp_id = getattr(item, "id", "")
        statement = getattr(item, "statement", "")
        if hyp_id and hyp_id in payload:
            raise AssertionError("research hypothesis id leaked into blind packet")
        if statement and statement in payload:
            raise AssertionError("research hypothesis statement leaked into blind packet")
        status = getattr(item, "closest_known_result", "")
        if status and status in payload and "KNOWN" in str(status):
            raise AssertionError("known-result text leaked into blind packet")
