"""v2.4 overlay store. Never writes historical.json or target_board.json."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from research_engine.control.types import (
    ENGINE_CONTROL_VERSION,
    CampaignControlRecord,
)
from research_engine.memory.store import BOARD_PATH, SEED_PATH

OVERLAY_PATH = Path(__file__).resolve().parent / "seed" / "overlay.json"


class ControlStore:
    """Writable overlay for v2.4 control records and replays."""

    def __init__(self, records: Iterable[CampaignControlRecord] = ()) -> None:
        self._records: dict[str, CampaignControlRecord] = {}
        for item in records:
            self._records[item.campaign_id] = item

    @property
    def records(self) -> tuple[CampaignControlRecord, ...]:
        return tuple(self._records.values())

    def get(self, campaign_id: str) -> CampaignControlRecord:
        return self._records[campaign_id]

    def add(self, record: CampaignControlRecord) -> CampaignControlRecord:
        self._records[record.campaign_id] = record
        return record

    def as_dict(self) -> dict[str, Any]:
        return {
            "engine_control_version": ENGINE_CONTROL_VERSION,
            "records": [item.as_dict() for item in self.records],
        }

    def to_json(self, path: Path) -> None:
        resolved = path.resolve()
        if resolved == SEED_PATH.resolve() or resolved == BOARD_PATH.resolve():
            raise RuntimeError("control overlay must not write historical.json or target_board.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.as_dict(), indent=2) + "\n", encoding="utf-8")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ControlStore:
        records = tuple(CampaignControlRecord.from_dict(item) for item in (data.get("records") or ()))
        return cls(records)

    @classmethod
    def from_json_path(cls, path: Path) -> ControlStore:
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))
