"""Load frozen Juggler odd states for the Phase-11 macro-grammar falsifier."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.discovery import WINDOW as JUGGLER_WINDOW
from research.juggler_sequence.discovery import orbit as juggler_orbit
from research.juggler_sequence.discovery import step as juggler_step
from research.juggler_sequence.spec import FloorPowerSpec, map_images
from research.research_control.juggler_odd_odd_phase10 import frozen_seeds
from research_engine.control.juggler_macro import (
    DEPTH,
    EXPERIMENT_NAME,
    LEAN_COMBINED,
    LEAN_OE,
    LEAN_OO,
    MacroSample,
    complementary_odd_ge3,
    floor_power,
    in_d_oe,
    in_d_oo,
    macro_sample,
    phase11_payload,
    render_phase11_markdown,
)
from research_engine.control.juggler_odd_odd import odd_even_two_step, odd_odd_two_step
from research.juggler_sequence.lean_paths import (
    ENVELOPE,
    juggler_text,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "juggler_macro_phase11.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "juggler_macro_phase11.md"
LEAN_PATH = ENVELOPE
PHASE10_JSON = REPO_ROOT / "docs" / "research" / "juggler_odd_odd_phase10.json"


def _two_step(seed: int) -> tuple[int, int] | None:
    mid = juggler_step(seed)
    if mid is None:
        return None
    image = juggler_step(mid)
    if image is None:
        return None
    spec_mid = FloorPowerSpec(start=seed).successors(seed)
    if spec_mid != (mid,) or spec_mid != map_images(seed):
        raise ValueError(f"FloorPowerSpec disagrees with discovery step at {seed}")
    if floor_power(seed) != mid:
        raise ValueError(f"engine floor_power disagrees at {seed}")
    return mid, image


def frozen_odd_macro_samples() -> tuple[MacroSample, ...]:
    items: list[MacroSample] = []
    seen: set[int] = set()
    for seed in frozen_seeds():
        if seed % 2 == 0:
            continue
        pair = _two_step(seed)
        if pair is None:
            continue
        mid, image = pair
        item = macro_sample(seed)
        if item is None:
            raise ValueError(f"odd seed {seed} has no branch label")
        if item.mid != mid or item.image != image:
            raise ValueError(f"macro_sample disagrees at {seed}")
        if seed in seen:
            continue
        seen.add(seed)
        items.append(item)
    return tuple(items)


def lean_macro_combined() -> bool:
    text = juggler_text()
    return (
        f"theorem {LEAN_OE}" in text
        and f"theorem {LEAN_OO}" in text
        and f"theorem {LEAN_COMBINED}" in text
        and "sorry" not in text
        and "admit" not in text
    )


def run_phase11() -> dict:
    if DEPTH != 2:
        raise RuntimeError("Phase-11 depth must be 2")
    if EXPERIMENT_NAME != "juggler_macro_phase11":
        raise RuntimeError("gated experiment name is frozen")
    samples = frozen_odd_macro_samples()
    if not any(item.source == 1 and item.mid == 1 and item.image == 1 for item in samples):
        raise RuntimeError("exceptional state 1->1->1 is missing")
    if not any(item.source == 5 and item.mid == 11 and item.image == 36 for item in samples):
        raise RuntimeError("required probe 5->11->36 is missing")
    if not any(item.source == 15 and item.branch == "E" and item.image == 7 for item in samples):
        raise RuntimeError("required probe 15->58->7 is missing")
    for item in samples:
        if item.source == 1:
            if not in_d_oo(item.source) or in_d_oe(item.source):
                raise RuntimeError("n=1 must be D_OO and not D_OE")
            continue
        if item.source < 3 or item.source % 2 == 0:
            raise RuntimeError(f"unexpected even or sub-threshold odd sample {item.source}")
        if not complementary_odd_ge3(item.source):
            raise RuntimeError(f"odd n>=3 is missing a unique branch: {item.source}")
        if item.branch == "E":
            if not in_d_oe(item.source) or in_d_oo(item.source):
                raise RuntimeError(f"E-branch must be D_OE: {item.source}")
            if odd_even_two_step(item.source) != item.image:
                raise RuntimeError(f"odd_even_two_step disagrees at {item.source}")
        else:
            if not in_d_oo(item.source) or in_d_oe(item.source):
                raise RuntimeError(f"O-branch must be D_OO: {item.source}")
            if odd_odd_two_step(item.source) != item.image:
                raise RuntimeError(f"odd_odd_two_step disagrees at {item.source}")
    if not lean_macro_combined():
        raise RuntimeError("combined Lean lemma or existing branch lemmas are missing")
    payload = phase11_payload(samples)
    payload["lean_combined_present"] = True
    payload["phase10_record_intact"] = PHASE10_JSON.is_file()
    window = set(JUGGLER_WINDOW) | {int(item) for item in juggler_orbit(13)["path"]}
    if not {item.source for item in samples} <= window:
        raise RuntimeError("Phase-11 enlarged the frozen Juggler census")
    return payload


def write_artifacts(payload: dict | None = None) -> dict:
    data = payload if payload is not None else run_phase11()
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase11_markdown(data), encoding="utf-8")
    return data
