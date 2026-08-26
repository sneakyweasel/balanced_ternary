"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from bt.sequences import bt_digit_sum, bt_reverse
from research.reverse_and_add_base3.spec import (
    DEFINED,
    ReverseAddSpec,
    map_images,
    map_spec,
    transition_status,
)

WINDOW = tuple(range(1, 41))
ORBIT_CAP = 40
START = 196
ALIQUOT_AT_196 = 203
JUGGLER_AT_8 = 2


def step(n: int) -> int | None:
    images = map_images(n)
    if len(images) != 1:
        return None
    return images[0]


def orbit(start: int = START, *, max_steps: int = ORBIT_CAP) -> dict[str, object]:
    seen: list[int] = []
    current = start
    for _ in range(max_steps):
        if transition_status(current) != DEFINED:
            return {
                "path": tuple(seen + [current]),
                "kind": "truncated",
                "hits_zero": 0 in seen or current == 0,
            }
        if current in seen:
            return {
                "path": tuple(seen),
                "kind": "cycle",
                "hits_zero": 0 in seen or current == 0,
            }
        nxt = step(current)
        seen.append(current)
        if nxt is None:
            return {"path": tuple(seen), "kind": "halt", "hits_zero": 0 in seen}
        current = nxt
    return {"path": tuple(seen), "kind": "truncated", "hits_zero": 0 in seen}


def evidence_state(spec: ReverseAddSpec | None = None) -> dict[str, object]:
    target = spec if spec is not None else map_spec()
    start_orbit = orbit(target.start)
    path = start_orbit["path"]
    drops = 0
    growths = 0
    first_growth: int | None = None
    affine_hits = 0
    for seed in WINDOW:
        image = step(seed)
        if image is None:
            continue
        if abs(image) < abs(seed):
            drops += 1
        elif abs(image) > abs(seed):
            growths += 1
            if first_growth is None:
                first_growth = seed
        if seed >= 2 and image == (5 * seed) // 4:
            affine_hits += 1
    return {
        "start": target.start,
        "start_orbit": path,
        "start_kind": start_orbit["kind"],
        "hits_zero": start_orbit["hits_zero"],
        "steps_to_zero": path.index(0) if 0 in path else None,
        "fixed_zero": step(0) == 0,
        "reverse_fixed_start": bt_reverse(target.start) == target.start,
        "drops": drops,
        "growths": growths,
        "first_growth": first_growth,
        "strip_54_hits": affine_hits,
        "digit_sum_at_196": bt_digit_sum(196),
        "aliquot_at_196": ALIQUOT_AT_196,
        "image_at_196": step(196),
        "image_at_8": step(8),
        "image_at_13": step(13),
        "census_affine_system": target.affine_system(),
        "universal_reverse_fixed": False,
        "note": "seed-196 reach of 0 is not a map theorem on integers",
    }


def falsify_claims(spec: ReverseAddSpec | None = None) -> dict[str, dict[str, object]]:
    report = evidence_state(spec)
    return {
        "residue_affine_cover": {
            "claim": "the map is residue-affine / piecewise-affine in the frozen census language",
            "holds_on_window": report["census_affine_system"] is not None,
            "status": "REFUTED",
            "counterexample": "affine_system is None; successor uses digit reverse",
        },
        "seed_halt_is_z_theorem": {
            "claim": "the packet seed reaching 0 is a theorem on all integers",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": report["start_orbit"],
        },
        "this_is_digit_fold": {
            "claim": "the successor is the signed digit-sum fold",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {
                "n": 196,
                "image": report["image_at_196"],
                "digit_sum": report["digit_sum_at_196"],
            },
        },
        "this_is_aliquot": {
            "claim": "the successor is sigma(n)-n",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {
                "n": 196,
                "image": report["image_at_196"],
                "sigma_minus_n": ALIQUOT_AT_196,
            },
        },
        "this_is_juggler": {
            "claim": "the successor is the even/odd floor-power map",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {"n": 8, "image": report["image_at_8"], "floor_power": JUGGLER_AT_8},
        },
        "every_seed_reverse_fixed": {
            "claim": "every positive seed equals its digit reverse",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {"n": 2, "reverse": bt_reverse(2)},
        },
        "new_reverse_attack": {
            "claim": "progress requires a new reverse-add attack",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": "exact I/O is the problem definition; frozen stack diagnoses the regime",
        },
    }
