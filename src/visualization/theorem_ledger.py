"""Read-only access to ``docs/theory/theorem_ledger.json``.

The UI must not invent claim status. Every badge comes from this ledger
or from an explicit display label already used in the mathematical record.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

LEDGER_PATH = (
    Path(__file__).resolve().parents[2] / "docs" / "theory" / "theorem_ledger.json"
)

EXACT_TAGS = frozenset(
    {
        "EXACT — LEAN VERIFIED",
        "EXACT — HUMAN PROOF",
    }
)
COMPUTED_TAGS = frozenset({"COMPUTATIONALLY VERIFIED"})
CONJECTURE_TAGS = frozenset({"CONJECTURE"})
REFUTED_TAGS = frozenset({"REFUTED"})
REPARAM_TAGS = frozenset({"REPARAMETERIZATION"})


@lru_cache(maxsize=1)
def load_ledger() -> tuple[dict[str, Any], ...]:
    raw = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return tuple(raw)


@lru_cache(maxsize=1)
def ledger_by_id() -> dict[str, dict[str, Any]]:
    return {entry["id"]: entry for entry in load_ledger()}


def theorem_entry(theorem_id: str) -> dict[str, Any] | None:
    """Return the ledger row for ``theorem_id``, or ``None`` if absent."""
    return ledger_by_id().get(theorem_id)


def claim_kind(tag: str) -> str:
    """Coarse visual family. Conjectures never share the exact family."""
    if tag in EXACT_TAGS:
        return "exact"
    if tag in COMPUTED_TAGS:
        return "computed"
    if tag in CONJECTURE_TAGS:
        return "conjecture"
    if tag in REFUTED_TAGS:
        return "refuted"
    if tag in REPARAM_TAGS:
        return "reparameterization"
    return "other"


def badge_payload(theorem_id: str) -> dict[str, str] | None:
    """Structured badge for research-mode panels."""
    entry = theorem_entry(theorem_id)
    if entry is None:
        return None
    tag = str(entry.get("tag", ""))
    return {
        "id": theorem_id,
        "tag": tag,
        "kind": claim_kind(tag),
        "statement": str(entry.get("statement", "")),
        "lean": str(entry.get("lean", "")),
        "source": str(entry.get("source", "")),
    }
