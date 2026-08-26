"""Load frozen v2.3 transitions for the symbolic-composition Phase-2 falsifier."""

from __future__ import annotations

import json
from pathlib import Path

from bt.sequences import bt_length
from research.home_prime_49.discovery import WINDOW as HOME_WINDOW
from research.home_prime_49.discovery import is_fixed_prime
from research.home_prime_49.discovery import orbit as home_orbit
from research.home_prime_49.discovery import step as home_step
from research.home_prime_49.spec import factor_trial
from research.juggler_sequence.discovery import WINDOW as JUGGLER_WINDOW
from research.juggler_sequence.discovery import orbit as juggler_orbit
from research.juggler_sequence.discovery import step as juggler_step
from research.reverse_and_add_base3.discovery import WINDOW as REVERSE_WINDOW
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.discovery import step as reverse_step
from research_engine.control.symbolic_composition import (
    CompositionSample,
    Phase2Decision,
    decide_phase2,
    falsify_home,
    falsify_juggler,
    falsify_reverse,
    floor_power,
    odd_even_two_step,
    phase2_payload,
    render_phase2_markdown,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "symbolic_composition_phase2.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "symbolic_composition_phase2.md"
JUGGLER_EXTENSION = tuple(range(1, 201))


def _unique(items: list[int]) -> tuple[int, ...]:
    seen: set[int] = set()
    ordered: list[int] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return tuple(ordered)


def juggler_samples() -> tuple[CompositionSample, ...]:
    seeds = list(JUGGLER_WINDOW) + [int(item) for item in juggler_orbit(13)["path"]] + list(JUGGLER_EXTENSION)
    items: list[CompositionSample] = []
    seen: set[int] = set()
    for seed in _unique(seeds):
        if seed % 2 == 0 or seed < 2:
            continue
        mid = juggler_step(seed)
        if mid is None or mid % 2 != 0:
            continue
        image = juggler_step(mid)
        if image is None:
            continue
        composed = odd_even_two_step(seed)
        if composed != image or floor_power(seed) != mid:
            continue
        if seed in seen:
            continue
        seen.add(seed)
        items.append(
            CompositionSample(source=seed, mid=mid, image=image, note="juggler odd-even T^2")
        )
    return tuple(items)


def reverse_samples() -> tuple[CompositionSample, ...]:
    seeds = list(REVERSE_WINDOW) + [int(item) for item in reverse_orbit(196)["path"]]
    items: list[CompositionSample] = []
    seen: set[int] = set()
    for seed in _unique(seeds):
        mid = reverse_step(seed)
        if mid is None:
            continue
        image = reverse_step(mid)
        if image is None:
            continue
        if seed in seen:
            continue
        seen.add(seed)
        items.append(
            CompositionSample(
                source=seed,
                mid=mid,
                image=image,
                note="reverse T^2",
                extra={
                    "len_source": bt_length(seed),
                    "len_mid": bt_length(mid),
                    "len_image": bt_length(image),
                },
            )
        )
    return tuple(items)


def _omega(n: int) -> int:
    factors = factor_trial(n) or {}
    return sum(factors.values())


def _dec_len(n: int) -> int:
    return len(str(abs(n))) if n != 0 else 1


def home_samples() -> tuple[CompositionSample, ...]:
    seeds = list(HOME_WINDOW)
    for start in (49, 4, 10):
        seeds.extend(int(item) for item in home_orbit(start, max_steps=8)["path"])
    items: list[CompositionSample] = []
    seen: set[int] = set()
    for seed in _unique(seeds):
        if is_fixed_prime(seed) or seed < 2:
            continue
        mid = home_step(seed)
        if mid is None:
            continue
        image = home_step(mid)
        if image is None:
            continue
        if seed in seen:
            continue
        seen.add(seed)
        items.append(
            CompositionSample(
                source=seed,
                mid=mid,
                image=image,
                note="home T^2",
                extra={
                    "len_source": _dec_len(seed),
                    "len_mid": _dec_len(mid),
                    "len_image": _dec_len(image),
                    "omega_source": _omega(seed),
                    "omega_mid": _omega(mid),
                    "omega_image": _omega(image),
                    "mid_prime": int(is_fixed_prime(mid)),
                    "image_prime": int(is_fixed_prime(image)),
                },
            )
        )
    return tuple(items)


def run_phase2(*, lean_status: str = "PROVED") -> tuple:
    juggler = falsify_juggler(juggler_samples(), lean_status=lean_status)
    reverse = falsify_reverse(reverse_samples())
    home = falsify_home(home_samples())
    return (juggler, reverse, home)


def write_artifacts(reports=None, *, lean_status: str = "PROVED") -> dict:
    items = reports if reports is not None else run_phase2(lean_status=lean_status)
    decision, reason = decide_phase2(items)
    promoted = "none"
    juggler = next((item for item in items if item.target == "juggler_sequence"), None)
    if (
        juggler is not None
        and juggler.classification == "SYMBOLIC_COMPOSITION_PROMISING"
        and decision in {Phase2Decision.MIXED, Phase2Decision.PROMOTE_SYMBOLIC_COMPOSITION}
    ):
        promoted = "odd_even_symbolic_composition"
    payload = phase2_payload(
        items, decision=decision, decision_reason=reason, promoted_concept=promoted
    )
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase2_markdown(payload), encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = write_artifacts(lean_status="PROVED")
    print(result["phase2_decision"], result["promoted_concept"])
    print(result["decision_reason"])
    for row in result["target_matrix"]:
        print(row["target"], row["classification"], row["lean_status"])
