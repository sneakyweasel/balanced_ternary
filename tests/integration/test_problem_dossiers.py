"""Every problem dossier carries a branch budget and a decision."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROBLEMS = ROOT / "docs" / "problems"

REQUIRED = ("## Branch budget", "## Decision", "## Publication assessment")
DECISIONS = ("PROMOTE", "PARK", "CLOSE")


def _dossiers() -> list[Path]:
    return sorted(PROBLEMS.glob("*.md"))


def test_dossiers_exist():
    assert _dossiers()


def test_dossiers_carry_the_required_sections():
    missing: list[str] = []
    for path in _dossiers():
        text = path.read_text(encoding="utf-8")
        for heading in REQUIRED:
            if heading not in text:
                missing.append(f"{path.name}: missing {heading}")
    assert missing == []


def test_every_dossier_states_one_decision():
    """The Decision section must name PROMOTE, PARK, or CLOSE."""
    bad: list[str] = []
    for path in _dossiers():
        if path.name == "TEMPLATE.md":
            continue
        text = path.read_text(encoding="utf-8")
        section = re.split(r"^## Decision$", text, flags=re.M)[1]
        section = re.split(r"^## ", section, flags=re.M)[0]
        if not any(word in section for word in DECISIONS):
            bad.append(path.name)
    assert bad == []
