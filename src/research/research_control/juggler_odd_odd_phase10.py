"""Load frozen Juggler odd-odd two-step samples for the Phase-10 falsifier."""

from __future__ import annotations

import json
from pathlib import Path

from research.juggler_sequence.discovery import WINDOW as JUGGLER_WINDOW
from research.juggler_sequence.discovery import orbit as juggler_orbit
from research.juggler_sequence.discovery import step as juggler_step
from research.juggler_sequence.spec import FloorPowerSpec, map_images
from research.juggler_sequence.lean_paths import DYNAMICS, juggler_text
from research_engine.control.juggler_odd_odd import (
    DEPTH,
    OddOddSample,
    floor_power,
    in_d_oe,
    in_d_oo,
    odd_even_two_step,
    odd_odd_two_step,
    phase10_payload,
    render_phase10_markdown,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "juggler_odd_odd_phase10.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "juggler_odd_odd_phase10.md"
LEAN_PATH = DYNAMICS


def frozen_seeds() -> tuple[int, ...]:
    seeds = list(JUGGLER_WINDOW)
    for item in juggler_orbit(13)["path"]:
        seeds.append(int(item))
    seen: set[int] = set()
    ordered: list[int] = []
    for seed in seeds:
        if seed in seen:
            continue
        seen.add(seed)
        ordered.append(seed)
    return tuple(ordered)


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


def odd_odd_samples() -> tuple[OddOddSample, ...]:
    items: list[OddOddSample] = []
    seen: set[int] = set()
    for seed in frozen_seeds():
        if seed % 2 == 0:
            continue
        pair = _two_step(seed)
        if pair is None:
            continue
        mid, image = pair
        if mid % 2 == 0:
            continue
        composed = odd_odd_two_step(seed)
        if composed != image:
            raise ValueError(f"odd_odd_two_step disagrees at {seed}: {composed} vs {image}")
        if not in_d_oo(seed) or in_d_oe(seed):
            raise ValueError(f"domain leak: {seed} must be D_OO and not D_OE")
        if seed in seen:
            continue
        seen.add(seed)
        items.append(OddOddSample(source=seed, mid=mid, image=image))
    return tuple(items)


def odd_even_samples() -> tuple[OddOddSample, ...]:
    items: list[OddOddSample] = []
    seen: set[int] = set()
    for seed in frozen_seeds():
        if seed % 2 == 0 or seed < 2:
            continue
        pair = _two_step(seed)
        if pair is None:
            continue
        mid, image = pair
        if mid % 2 != 0:
            continue
        composed = odd_even_two_step(seed)
        if composed != image:
            raise ValueError(f"odd_even_two_step disagrees at {seed}")
        if not in_d_oe(seed) or in_d_oo(seed):
            raise ValueError(f"domain leak: {seed} must be D_OE and not D_OO")
        if seed in seen:
            continue
        seen.add(seed)
        items.append(
            OddOddSample(source=seed, mid=mid, image=image, note="juggler odd-even T^2 control")
        )
    return tuple(items)


def lean_odd_odd_proved() -> bool:
    text = juggler_text()
    return (
        "theorem floorPower_odd_even_two_step_lt" in text
        and "theorem floorPower_odd_odd_two_step_gt" in text
        and "sorry" not in text
        and "admit" not in text
    )


def run_phase10() -> dict:
    if DEPTH != 2:
        raise RuntimeError("Phase-10 depth must be 2")
    samples = odd_odd_samples()
    oe = odd_even_samples()
    if not any(item.source == 3 and item.mid == 5 and item.image == 11 for item in samples):
        raise RuntimeError("required probe 3->5->11 is missing from frozen D_OO")
    if any(item.source % 2 == 0 or item.mid % 2 == 0 for item in samples):
        raise RuntimeError("D_OO sample is not odd-odd")
    if any(item.mid % 2 == 1 for item in oe):
        raise RuntimeError("D_OE control contains an odd mid")
    payload = phase10_payload(samples, len(oe), lean_proved=lean_odd_odd_proved())
    return payload


def write_artifacts(payload: dict | None = None) -> dict:
    data = payload if payload is not None else run_phase10()
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase10_markdown(data), encoding="utf-8")
    return data
