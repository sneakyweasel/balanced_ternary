"""Load frozen reverse-add one-step pair alignments for the Phase-6 falsifier."""

from __future__ import annotations

import json
from pathlib import Path

from bt.representation import digits, encode
from bt.sequences import bt_length, bt_reverse
from research.reverse_and_add_base3.discovery import WINDOW as REVERSE_WINDOW
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.discovery import step as reverse_step
from research.reverse_and_add_base3.spec import ReverseAddSpec, map_images
from research_engine.control.reverse_add_pair_interaction import (
    PairSample,
    classify,
    evaluate_candidate,
    pair_aggregates,
    pair_sums_lsd,
    phase6_payload,
    ranked_candidates,
    render_phase6_markdown,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "reverse_add_pair_interaction_phase6.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "reverse_add_pair_interaction_phase6.md"

SPECIAL_PROBE_ROLES = {
    1: "positive palindrome",
    2: "reverse-as-negation",
    5: "sign-changing successor",
    8: "successor 0",
    196: "packet seed",
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


def pair_sample_for(x: int, *, image: int, note: str = "reverse T") -> PairSample:
    left = digits(encode(x))
    right = digits(encode(bt_reverse(x)))
    sums = pair_sums_lsd(left, right)
    stats = pair_aggregates(sums)
    return PairSample(
        source=x,
        image=image,
        w_source=bt_reverse(x),
        len_source=bt_length(x),
        len_image=bt_length(image),
        pair_sums=sums,
        p0=stats["p0"],
        p2=stats["p2"],
        p_plus=stats["p_plus"],
        p_minus=stats["p_minus"],
        r_last=stats["r_last"],
        note=note,
    )


def reverse_samples() -> tuple[PairSample, ...]:
    items: list[PairSample] = []
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
        items.append(pair_sample_for(seed, image=image))
    return tuple(items)


def special_probes(samples: tuple[PairSample, ...]) -> list[dict]:
    by_source = {item.source: item for item in samples}
    probes: list[dict] = []
    for source, role in SPECIAL_PROBE_ROLES.items():
        item = by_source.get(source)
        if item is None:
            image = reverse_step(source)
            if image is None:
                continue
            item = pair_sample_for(source, image=image, note=role)
        payload = item.as_dict()
        payload["role"] = role
        probes.append(payload)
    return probes


def run_phase6(samples: tuple[PairSample, ...] | None = None):
    items = samples if samples is not None else reverse_samples()
    outcomes = tuple(evaluate_candidate(candidate, items) for candidate in ranked_candidates())
    classification, reason = classify(outcomes)
    return items, outcomes, classification, reason


def write_artifacts(samples: tuple[PairSample, ...] | None = None) -> dict:
    items, outcomes, classification, reason = run_phase6(samples)
    window = {
        "window": "range(1, 41)",
        "orbit_seed": 196,
        "orbit": [int(item) for item in reverse_orbit(196)["path"]],
        "sample_count": len(items),
        "composition_depth": 1,
        "census_bound": "frozen; not enlarged",
    }
    payload = phase6_payload(
        outcomes,
        classification=classification,
        decision_reason=reason,
        transition_window=window,
        special_probes=special_probes(items),
    )
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase6_markdown(payload), encoding="utf-8")
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
                f"P0={cex['p0']} P2={cex['p2']} P+={cex['p_plus']} P-={cex['p_minus']} "
                f"R={cex['r_last']} dL={cex['length_delta']}"
            )
        print(item["rank"], item["name"], mark, "checked=", item["checked"], extra)
    print("probes", result["special_probes"])
