"""Load frozen reverse-add one-step additions for the Phase-5 carry falsifier."""

from __future__ import annotations

import json
from pathlib import Path

from bt.normalization import add_with_trace
from bt.representation import decode, encode
from bt.sequences import bt_length, bt_reverse
from research.reverse_and_add_base3.discovery import WINDOW as REVERSE_WINDOW
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.discovery import step as reverse_step
from research.reverse_and_add_base3.spec import ReverseAddSpec, map_images
from research_engine.control.reverse_add_carry import (
    CarrySample,
    carry_chain_length,
    classify,
    evaluate_candidate,
    phase5_payload,
    ranked_candidates,
    render_phase5_markdown,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "reverse_add_carry_phase5.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "reverse_add_carry_phase5.md"

SPECIAL_PROBE_ROLES = {
    1: "positive palindrome",
    196: "packet seed",
    2: "W(x)<0",
    8: "successor 0",
}


def _unique(items: list[int]) -> tuple[int, ...]:
    seen: set[int] = set()
    ordered: list[int] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return tuple(ordered)


def frozen_seeds() -> tuple[int, ...]:
    seeds = list(REVERSE_WINDOW) + [int(item) for item in reverse_orbit(196)["path"]]
    return _unique(seeds)


def carry_trace_for(x: int):
    """Existing addition ledger for x + W(x). Does not rewrite arithmetic."""
    return add_with_trace(encode(x), encode(bt_reverse(x)))


def carry_statistic(x: int) -> int:
    trace = carry_trace_for(x)
    steps = tuple((step.carry_in, step.carry_out) for step in trace.steps)
    return carry_chain_length(steps, final_carry=trace.final_carry)


def successor_from_trace(x: int) -> int:
    return decode(carry_trace_for(x).result)


def reverse_samples() -> tuple[CarrySample, ...]:
    items: list[CarrySample] = []
    seen: set[int] = set()
    for seed in frozen_seeds():
        image = reverse_step(seed)
        if image is None:
            continue
        if seed in seen:
            continue
        seen.add(seed)
        spec_image = ReverseAddSpec(start=seed).successors(seed)
        if spec_image != (image,) or spec_image != map_images(seed):
            raise ValueError(f"ReverseAddSpec disagrees with discovery step at {seed}")
        traced = successor_from_trace(seed)
        if traced != image:
            raise ValueError(f"add_with_trace disagrees with ReverseAddSpec at {seed}")
        items.append(
            CarrySample(
                source=seed,
                image=image,
                w_source=bt_reverse(seed),
                len_source=bt_length(seed),
                len_image=bt_length(image),
                carry_chain=carry_statistic(seed),
                note="reverse T",
            )
        )
    return tuple(items)


def special_probes(samples: tuple[CarrySample, ...]) -> list[dict]:
    by_source = {item.source: item for item in samples}
    probes: list[dict] = []
    for source, role in SPECIAL_PROBE_ROLES.items():
        item = by_source.get(source)
        if item is None:
            image = reverse_step(source)
            if image is None:
                continue
            item = CarrySample(
                source=source,
                image=image,
                w_source=bt_reverse(source),
                len_source=bt_length(source),
                len_image=bt_length(image),
                carry_chain=carry_statistic(source),
                note=role,
            )
        payload = item.as_dict()
        payload["role"] = role
        probes.append(payload)
    return probes


def run_phase5(samples: tuple[CarrySample, ...] | None = None):
    items = samples if samples is not None else reverse_samples()
    outcomes = tuple(evaluate_candidate(candidate, items) for candidate in ranked_candidates())
    classification, reason = classify(outcomes)
    return items, outcomes, classification, reason


def write_artifacts(samples: tuple[CarrySample, ...] | None = None) -> dict:
    items, outcomes, classification, reason = run_phase5(samples)
    window = {
        "window": "range(1, 41)",
        "orbit_seed": 196,
        "orbit": [int(item) for item in reverse_orbit(196)["path"]],
        "sample_count": len(items),
        "composition_depth": 1,
        "census_bound": "frozen; not enlarged",
    }
    payload = phase5_payload(
        outcomes,
        classification=classification,
        decision_reason=reason,
        transition_window=window,
        special_probes=special_probes(items),
    )
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase5_markdown(payload), encoding="utf-8")
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
            extra = (
                f" cex={cex['source']}->{cex['image']} "
                f"C={cex['carry_chain']} dL={cex['length_delta']}"
            )
        print(item["rank"], item["name"], mark, "checked=", item["checked"], extra)
    print("probes", result["special_probes"])
