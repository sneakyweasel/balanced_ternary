"""Load frozen reverse-add involution objects for the Phase-8 falsifier."""

from __future__ import annotations

import json
from pathlib import Path

from bt.representation import encode
from bt.sequences import bt_length, bt_reverse
from research.research_control.reverse_add_pair_interaction_phase6 import frozen_seeds
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.discovery import step as reverse_step
from research.reverse_and_add_base3.spec import ReverseAddSpec, map_images
from research_engine.control.reverse_add_involution import (
    InvolutionSample,
    classify,
    evaluate_candidate,
    phase8_payload,
    ranked_candidates,
    render_phase8_markdown,
    reverse_gap_from_msd,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "reverse_add_involution_phase8.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "reverse_add_involution_phase8.md"

SPECIAL_PROBE_ROLES = {
    1: "positive palindrome",
    2: "reverse-as-negation",
    5: "sign-changing successor",
    6: "phase-7 collision counterexample",
    8: "successor 0",
    196: "packet seed",
    -672: "phase-6 pair-count counterexample",
}


def _msd(n: int) -> int:
    return int(encode(n).digits_msd[0])


def involution_sample_for(x: int, *, image: int, note: str = "reverse T") -> InvolutionSample:
    w_x = bt_reverse(x)
    w_t = bt_reverse(image)
    return InvolutionSample(
        source=x,
        image=image,
        w_source=w_x,
        w_image=w_t,
        ww_source=bt_reverse(w_x),
        len_source=bt_length(x),
        len_image=bt_length(image),
        gap_source=reverse_gap_from_msd(encode(x).digits_msd),
        gap_image=reverse_gap_from_msd(encode(image).digits_msd),
        msd_source=_msd(x),
        msd_w=_msd(w_x),
        msd_t=_msd(image),
        note=note,
    )


def reverse_samples() -> tuple[InvolutionSample, ...]:
    items: list[InvolutionSample] = []
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
        items.append(involution_sample_for(seed, image=image))
    return tuple(items)


def special_probes(samples: tuple[InvolutionSample, ...]) -> list[dict]:
    by_source = {item.source: item for item in samples}
    probes: list[dict] = []
    for source, role in SPECIAL_PROBE_ROLES.items():
        item = by_source.get(source)
        if item is None:
            image = reverse_step(source)
            if image is None:
                continue
            item = involution_sample_for(source, image=image, note=role)
        payload = item.as_dict()
        payload["role"] = role
        probes.append(payload)
    return probes


def run_phase8(samples: tuple[InvolutionSample, ...] | None = None):
    items = samples if samples is not None else reverse_samples()
    outcomes = tuple(evaluate_candidate(candidate, items) for candidate in ranked_candidates())
    classification, reason = classify(outcomes)
    return items, outcomes, classification, reason


def write_artifacts(samples: tuple[InvolutionSample, ...] | None = None) -> dict:
    items, outcomes, classification, reason = run_phase8(samples)
    window = {
        "window": "range(1, 41)",
        "orbit_seed": 196,
        "orbit": [int(item) for item in reverse_orbit(196)["path"]],
        "sample_count": len(items),
        "composition_depth": 1,
        "census_bound": "frozen; not enlarged",
        "objects": ["x", "W(x)", "T(x)", "W(T(x))"],
    }
    payload = phase8_payload(
        outcomes,
        classification=classification,
        decision_reason=reason,
        transition_window=window,
        special_probes=special_probes(items),
    )
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase8_markdown(payload), encoding="utf-8")
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
                f"W={cex['w_source']} WT={cex['w_image']} R={cex['residual']} "
                f"gap={cex['gap_source']}->{cex['gap_image']}"
            )
        print(item["rank"], item["name"], mark, "checked=", item["checked"], extra)
    print("specificity", result["reverse_specificity_check"])
    print("probes", result["special_probes"])
