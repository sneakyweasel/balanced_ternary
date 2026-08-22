"""Machine-readable conjecture registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STATUSES = (
    "ACTIVE",
    "PROVED",
    "REFUTED",
    "COMPUTATIONALLY_SUPPORTED",
    "REPARAMETERIZATION",
    "ARCHIVED",
)

REQUIRED = (
    "id",
    "title",
    "statement",
    "mathematical_domain",
    "origin",
    "status",
    "first_seen",
    "tested_range",
    "counterexamples",
    "proof_reference",
    "lean_reference",
    "literature",
    "notes",
)

_STATUS_DIR = {
    "ACTIVE": "active",
    "PROVED": "proved",
    "REFUTED": "refuted",
    "COMPUTATIONALLY_SUPPORTED": "active",
    "REPARAMETERIZATION": "archived",
    "ARCHIVED": "archived",
}


def registry_root() -> Path:
    return Path(__file__).resolve().parents[3] / "conjectures"


def _iter_files() -> list[Path]:
    root = registry_root()
    if not root.is_dir():
        return []
    return sorted(root.rglob("*.json"))


def _load(path: Path) -> dict[str, Any]:
    rec = json.loads(path.read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED if k not in rec]
    if missing:
        raise ValueError(f"{path.name} missing fields: {missing}")
    if rec["status"] not in STATUSES:
        raise ValueError(f"{path.name} has invalid status {rec['status']!r}")
    rec["_path"] = str(path)
    return rec


def list_conjectures(status: str | None = None) -> list[dict[str, Any]]:
    rows = [_load(path) for path in _iter_files()]
    if status:
        rows = [r for r in rows if r["status"] == status]
    return rows


def get_conjecture(conjecture_id: str) -> dict[str, Any]:
    for rec in list_conjectures():
        if rec["id"] == conjecture_id:
            return rec
    raise KeyError(conjecture_id)


def register_conjecture(record: dict[str, Any]) -> Path:
    status = record["status"]
    if status not in STATUSES:
        raise ValueError(f"invalid status {status!r}")
    folder = registry_root() / _STATUS_DIR[status]
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{record['id']}.json"
    payload = {k: record.get(k) for k in REQUIRED}
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def update_status(conjecture_id: str, status: str) -> dict[str, Any]:
    rec = get_conjecture(conjecture_id)
    old = Path(rec["_path"])
    rec["status"] = status
    rec.pop("_path", None)
    new_path = register_conjecture(rec)
    if old.resolve() != new_path.resolve() and old.exists():
        old.unlink()
    return get_conjecture(conjecture_id)


def add_counterexample(conjecture_id: str, witness: str) -> dict[str, Any]:
    rec = get_conjecture(conjecture_id)
    examples = list(rec.get("counterexamples") or [])
    if witness not in examples:
        examples.append(witness)
    rec["counterexamples"] = examples
    rec.pop("_path", None)
    register_conjecture(rec)
    return get_conjecture(conjecture_id)


def add_proof(conjecture_id: str, reference: str) -> dict[str, Any]:
    rec = get_conjecture(conjecture_id)
    rec["proof_reference"] = reference
    rec.pop("_path", None)
    register_conjecture(rec)
    return get_conjecture(conjecture_id)


def add_lean_proof(conjecture_id: str, reference: str) -> dict[str, Any]:
    rec = get_conjecture(conjecture_id)
    rec["lean_reference"] = reference
    rec.pop("_path", None)
    register_conjecture(rec)
    return get_conjecture(conjecture_id)
