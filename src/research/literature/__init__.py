"""Literature registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED = (
    "id",
    "title",
    "authors",
    "year",
    "problem_area",
    "relevant_concepts",
    "project_relationship",
    "status",
    "notes",
)


def registry_root() -> Path:
    return Path(__file__).resolve().parents[3] / "literature"


def list_references() -> list[dict[str, Any]]:
    root = registry_root()
    if not root.is_dir():
        return []
    rows = []
    for path in sorted(root.glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        missing = [k for k in REQUIRED if k not in rec]
        if missing:
            raise ValueError(f"{path.name} missing fields: {missing}")
        rec["_path"] = str(path)
        rows.append(rec)
    return rows


def get_reference(ref_id: str) -> dict[str, Any]:
    for rec in list_references():
        if rec["id"] == ref_id:
            return rec
    raise KeyError(ref_id)


def cite(ref_id: str) -> str:
    rec = get_reference(ref_id)
    authors = ", ".join(rec.get("authors") or [])
    year = rec.get("year") or ""
    return f"{authors} ({year}). {rec['title']}"
