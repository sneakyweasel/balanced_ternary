"""Load frozen Juggler states for the Phase-12 parity-drift falsifier."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.discovery import WINDOW as JUGGLER_WINDOW
from research.juggler_sequence.discovery import orbit as juggler_orbit
from research.juggler_sequence.discovery import step as juggler_step
from research.juggler_sequence.spec import FloorPowerSpec, map_images
from research.research_control.juggler_odd_odd_phase10 import frozen_seeds
from research_engine.control.juggler_parity_drift import (
    EXPERIMENT_NAME,
    LEAN_OE,
    LEAN_OO,
    LEAN_OOOEE,
    MAX_DEPTH,
    WORD_EE,
    WORD_OOOEE,
    DriftSample,
    floor_power,
    make_sample,
    phase12_payload,
    render_phase12_markdown,
    shortest_negative_word,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "juggler_parity_drift_phase12.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "juggler_parity_drift_phase12.md"
LEAN_PATH = REPO_ROOT / "formal" / "Problems" / "Engine" / "FloorPower.lean"
PHASE11_JSON = REPO_ROOT / "docs" / "research" / "juggler_macro_phase11.json"


def _agree_one_step(seed: int) -> int:
    mid = juggler_step(seed)
    if mid is None:
        raise ValueError(f"discovery step missing at {seed}")
    spec_mid = FloorPowerSpec(start=seed).successors(seed)
    if spec_mid != (mid,) or spec_mid != map_images(seed):
        raise ValueError(f"FloorPowerSpec disagrees with discovery step at {seed}")
    if floor_power(seed) != mid:
        raise ValueError(f"engine floor_power disagrees at {seed}")
    return mid


def frozen_drift_samples() -> tuple[DriftSample, ...]:
    items: list[DriftSample] = []
    seen: set[tuple[int, str]] = set()
    for seed in frozen_seeds():
        _agree_one_step(seed)
        for steps, note in (
            (1, "juggler one-step increment"),
            (len(WORD_EE), "juggler EE block"),
            (len(WORD_OOOEE), "juggler OOOEE block"),
        ):
            item = make_sample(seed, steps, note=note)
            key = (item.source, item.word)
            if key in seen:
                continue
            seen.add(key)
            items.append(item)
    return tuple(items)


def lean_oooee_proved() -> bool:
    text = LEAN_PATH.read_text(encoding="utf-8")
    return (
        f"theorem {LEAN_OE}" in text
        and f"theorem {LEAN_OO}" in text
        and f"theorem {LEAN_OOOEE}" in text
        and "sorry" not in text
        and "admit" not in text
    )


def run_phase12() -> dict:
    if MAX_DEPTH != 5:
        raise RuntimeError("Phase-12 depth must be 5")
    if EXPERIMENT_NAME != "juggler_parity_drift_phase12":
        raise RuntimeError("gated experiment name is frozen")
    if shortest_negative_word() != WORD_EE:
        raise RuntimeError("C3 must be EE, selected before testing")
    samples = frozen_drift_samples()
    if not any(item.source == 1 and item.depth == 1 and item.image == 1 for item in samples):
        raise RuntimeError("exceptional state 1 is missing")
    if not any(item.word == WORD_OOOEE and item.source == 3 for item in samples):
        raise RuntimeError("required OOOEE probe 3 is missing")
    if not any(item.word == WORD_EE and item.source == 4 for item in samples):
        raise RuntimeError("required EE probe 4 is missing")
    window = set(JUGGLER_WINDOW) | {int(item) for item in juggler_orbit(13)["path"]}
    if not {item.source for item in samples} <= window:
        raise RuntimeError("Phase-12 enlarged the frozen Juggler census")
    if any(len(item.word) > MAX_DEPTH for item in samples):
        raise RuntimeError("Phase-12 exceeded depth 5")
    payload = phase12_payload(samples, lean_proved=lean_oooee_proved())
    payload["phase11_record_intact"] = PHASE11_JSON.is_file()
    return payload


def write_artifacts(payload: dict | None = None) -> dict:
    data = payload if payload is not None else run_phase12()
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase12_markdown(data), encoding="utf-8")
    return data
