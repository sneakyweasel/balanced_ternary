"""Load frozen reverse-add one-step weighted pair summaries for Phase 7."""

from __future__ import annotations

import json
from pathlib import Path

from bt.representation import digits, encode
from bt.sequences import bt_length, bt_reverse
from research.research_control.reverse_add_pair_interaction_phase6 import frozen_seeds
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.discovery import step as reverse_step
from research.reverse_and_add_base3.spec import ReverseAddSpec, map_images
from research_engine.control.reverse_add_pair_interaction import pair_sums_lsd
from research_engine.control.reverse_add_weighted_pair import (
    WeightedSample,
    classify,
    evaluate_candidate,
    phase7_payload,
    positional_profile,
    ranked_candidates,
    render_phase7_markdown,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "reverse_add_weighted_pair_phase7.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "reverse_add_weighted_pair_phase7.md"

SPECIAL_PROBE_ROLES = {
    1: "positive palindrome",
    2: "reverse-as-negation",
    5: "sign-changing successor",
    8: "successor 0",
    196: "packet seed",
    -672: "phase-6 pair-count counterexample",
}


def weighted_sample_for(x: int, *, image: int, note: str = "reverse T") -> WeightedSample:
    left = digits(encode(x))
    right = digits(encode(bt_reverse(x)))
    sums = pair_sums_lsd(left, right)
    stats = positional_profile(sums)
    return WeightedSample(
        source=x,
        image=image,
        w_source=bt_reverse(x),
        len_source=bt_length(x),
        len_image=bt_length(image),
        pair_sums=sums,
        h=stats["h"],
        sign_h=stats["sign_h"],
        m_plus=stats["m_plus"],
        m_minus=stats["m_minus"],
        h2=stats["h2"],
        sign_h2=stats["sign_h2"],
        note=note,
    )


def reverse_samples() -> tuple[WeightedSample, ...]:
    items: list[WeightedSample] = []
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
        if image != seed + bt_reverse(seed):
            raise ValueError(f"integer successor disagrees with ReverseAddSpec at {seed}")
        items.append(weighted_sample_for(seed, image=image))
    return tuple(items)


def special_probes(samples: tuple[WeightedSample, ...]) -> list[dict]:
    by_source = {item.source: item for item in samples}
    probes: list[dict] = []
    for source, role in SPECIAL_PROBE_ROLES.items():
        item = by_source.get(source)
        if item is None:
            image = reverse_step(source)
            if image is None:
                continue
            item = weighted_sample_for(source, image=image, note=role)
        payload = item.as_dict()
        payload["role"] = role
        probes.append(payload)
    return probes


def run_phase7(samples: tuple[WeightedSample, ...] | None = None):
    items = samples if samples is not None else reverse_samples()
    outcomes = tuple(evaluate_candidate(candidate, items) for candidate in ranked_candidates())
    classification, reason = classify(outcomes)
    return items, outcomes, classification, reason


def _secondary_length(outcomes: tuple, items: tuple[WeightedSample, ...]) -> str:
    sign_survivors = [
        item for item in outcomes if item.survived and item.rank in {1, 2}
    ]
    if not sign_survivors:
        return "no sign candidate survived; no secondary length observation"
    growing = sum(1 for item in items if item.length_delta >= 1)
    return (
        "length was not a primary candidate. On the frozen sample, "
        f"{growing} one-step states have ΔL>=1; positional sign laws do not "
        "claim a length identity."
    )


def write_artifacts(samples: tuple[WeightedSample, ...] | None = None) -> dict:
    items, outcomes, classification, reason = run_phase7(samples)
    window = {
        "window": "range(1, 41)",
        "orbit_seed": 196,
        "orbit": [int(item) for item in reverse_orbit(196)["path"]],
        "sample_count": len(items),
        "composition_depth": 1,
        "census_bound": "frozen; not enlarged",
    }
    payload = phase7_payload(
        outcomes,
        classification=classification,
        decision_reason=reason,
        transition_window=window,
        special_probes=special_probes(items),
        secondary_length_observation=_secondary_length(outcomes, items),
    )
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase7_markdown(payload), encoding="utf-8")
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
                f"h={cex['h']} sign_h={cex['sign_h']} "
                f"m+={cex['m_plus']} m-={cex['m_minus']} "
                f"h2={cex['h2']} sign_h2={cex['sign_h2']}"
            )
        print(item["rank"], item["name"], mark, "checked=", item["checked"], extra)
    print("probes", result["special_probes"])
