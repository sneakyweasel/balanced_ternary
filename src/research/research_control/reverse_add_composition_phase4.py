"""Load frozen reverse-add transitions for the Phase-4 composition falsifier."""

from __future__ import annotations

import json
from pathlib import Path

from bt.sequences import bt_length, bt_reverse
from research.reverse_and_add_base3.discovery import WINDOW as REVERSE_WINDOW
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.discovery import step as reverse_step
from research_engine.control.reverse_add_composition import (
    ReverseSample,
    classify,
    evaluate_candidate,
    phase4_payload,
    ranked_candidates,
    render_phase4_markdown,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "reverse_add_composition_phase4.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "reverse_add_composition_phase4.md"


def _unique(items: list[int]) -> tuple[int, ...]:
    seen: set[int] = set()
    ordered: list[int] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return tuple(ordered)


def reverse_samples() -> tuple[ReverseSample, ...]:
    seeds = list(REVERSE_WINDOW) + [int(item) for item in reverse_orbit(196)["path"]]
    items: list[ReverseSample] = []
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
            ReverseSample(
                source=seed,
                mid=mid,
                image=image,
                w_source=bt_reverse(seed),
                w_mid=bt_reverse(mid),
                len_source=bt_length(seed),
                len_mid=bt_length(mid),
                len_image=bt_length(image),
                note="reverse T^2",
            )
        )
    return tuple(items)


def run_phase4(samples: tuple[ReverseSample, ...] | None = None):
    items = samples if samples is not None else reverse_samples()
    outcomes = tuple(evaluate_candidate(candidate, items) for candidate in ranked_candidates())
    classification, reason = classify(outcomes)
    return items, outcomes, classification, reason


def write_artifacts(samples: tuple[ReverseSample, ...] | None = None) -> dict:
    items, outcomes, classification, reason = run_phase4(samples)
    window = {
        "window": "range(1, 41)",
        "orbit_seed": 196,
        "orbit": [int(item) for item in reverse_orbit(196)["path"]],
        "sample_count": len(items),
        "composition_depth": 2,
    }
    payload = phase4_payload(
        outcomes,
        classification=classification,
        decision_reason=reason,
        transition_window=window,
    )
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase4_markdown(payload), encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = write_artifacts()
    print(result["decision"], result["green_loot"], result["lean_status"])
    print(result["decision_reason"])
    for item in result["candidate_statements"]:
        mark = "survived" if item["survived"] else "failed"
        cex = item.get("counterexample")
        extra = ""
        if cex:
            extra = f" cex={cex['source']}->{cex['mid']}->{cex['image']}"
        print(item["rank"], item["name"], mark, extra)
