"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.juggler_sequence.spec import (
    DEFINED,
    FloorPowerSpec,
    map_images,
    map_spec,
    transition_status,
)

WINDOW = tuple(range(1, 41))
ORBIT_CAP = 40
START = 13


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
            return {"path": tuple(seen + [current]), "kind": "truncated", "hits_one": 1 in seen}
        if current in seen:
            return {"path": tuple(seen), "kind": "cycle", "hits_one": 1 in seen or current == 1}
        nxt = step(current)
        seen.append(current)
        if nxt is None:
            return {"path": tuple(seen), "kind": "halt", "hits_one": 1 in seen}
        current = nxt
    return {"path": tuple(seen), "kind": "truncated", "hits_one": 1 in seen}


def evidence_state(spec: FloorPowerSpec | None = None) -> dict[str, object]:
    target = spec if spec is not None else map_spec()
    start_orbit = orbit(target.start)
    drops = 0
    growths = 0
    first_growth: int | None = None
    affine_hits = 0
    for seed in WINDOW:
        image = step(seed)
        if image is None:
            continue
        if image < seed:
            drops += 1
        elif image > seed:
            growths += 1
            if first_growth is None:
                first_growth = seed
        if seed >= 2 and image == (5 * seed) // 4:
            affine_hits += 1
    return {
        "start": target.start,
        "start_orbit": start_orbit["path"],
        "start_kind": start_orbit["kind"],
        "hits_one": start_orbit["hits_one"],
        "steps_to_one": (
            start_orbit["path"].index(1) if 1 in start_orbit["path"] else None
        ),
        "fixed_one": step(1) == 1,
        "drops": drops,
        "growths": growths,
        "first_growth": first_growth,
        "strip_54_hits": affine_hits,
        "aliquot_at_13": 1,
        "image_at_13": step(13),
        "census_affine_system": target.affine_system(),
        "universal_reach_one": False,
        "note": "seed-13 halt is not a map theorem on positive integers",
    }


def falsify_claims(spec: FloorPowerSpec | None = None) -> dict[str, dict[str, object]]:
    report = evidence_state(spec)
    return {
        "residue_affine_cover": {
            "claim": "the map is residue-affine / piecewise-affine in the frozen census language",
            "holds_on_window": report["census_affine_system"] is not None,
            "status": "REFUTED",
            "counterexample": "affine_system is None; odd branch is a floor power",
        },
        "seed_halt_is_z_theorem": {
            "claim": "the packet seed reaching 1 is a theorem on all positive integers",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": report["start_orbit"],
        },
        "this_is_aliquot": {
            "claim": "the successor is sigma(n)-n",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {"n": 13, "image": report["image_at_13"], "sigma_minus_n": 1},
        },
        "this_is_floor_5x4": {
            "claim": "the successor is the expanding 5x/4 strip map",
            "holds_on_window": report["strip_54_hits"] == len(WINDOW),
            "status": "REFUTED",
            "counterexample": {"n": 8, "image": step(8), "floor_5x4": 10},
        },
        "strict_descent": {
            "claim": "every positive n decreases",
            "holds_on_window": report["growths"] == 0,
            "status": "REFUTED",
            "counterexample": report["first_growth"],
        },
        "new_radical_attack": {
            "claim": "progress requires a new radical/floor-power attack",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": "exact I/O is the problem definition; frozen stack diagnoses the regime",
        },
    }
