"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.home_prime_49.spec import (
    DEFINED,
    FactorConcatSpec,
    TRANSITION_UNRESOLVED,
    map_images,
    map_spec,
    transition_status,
)

WINDOW = tuple(range(2, 41))
ORBIT_CAP = 40
START = 49
ALIQUOT_AT_49 = 8
JUGGLER_AT_49 = 343
REVERSE_ADD_AT_8 = 0


def step(n: int) -> int | None:
    images = map_images(n)
    if len(images) != 1:
        return None
    return images[0]


def is_fixed_prime(n: int) -> bool:
    image = step(n)
    return image == n and n >= 2


def orbit(start: int = START, *, max_steps: int = ORBIT_CAP) -> dict[str, object]:
    seen: list[int] = []
    current = start
    for _ in range(max_steps):
        status = transition_status(current)
        if status != DEFINED:
            return {
                "path": tuple(seen + [current]),
                "kind": "truncated" if status == TRANSITION_UNRESOLVED else "halt",
                "hits_prime": any(is_fixed_prime(item) for item in seen) or is_fixed_prime(current),
            }
        if current in seen:
            return {
                "path": tuple(seen),
                "kind": "cycle",
                "hits_prime": any(is_fixed_prime(item) for item in seen) or is_fixed_prime(current),
            }
        nxt = step(current)
        seen.append(current)
        if nxt is None:
            return {"path": tuple(seen), "kind": "halt", "hits_prime": any(is_fixed_prime(item) for item in seen)}
        current = nxt
    return {
        "path": tuple(seen),
        "kind": "truncated",
        "hits_prime": any(is_fixed_prime(item) for item in seen),
    }


def evidence_state(spec: FactorConcatSpec | None = None) -> dict[str, object]:
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
        if image < seed:
            drops += 1
        elif image > seed:
            growths += 1
            if first_growth is None:
                first_growth = seed
        if seed >= 2 and image == (5 * seed) // 4:
            affine_hits += 1
    four_orbit = orbit(4, max_steps=8)
    ten_orbit = orbit(10, max_steps=8)
    return {
        "start": target.start,
        "start_orbit": path,
        "start_kind": start_orbit["kind"],
        "hits_prime": start_orbit["hits_prime"],
        "steps_to_prime": next((i for i, item in enumerate(path) if is_fixed_prime(item)), None),
        "fixed_seven": step(7) == 7,
        "four_orbit": four_orbit["path"],
        "four_hits_prime": four_orbit["hits_prime"],
        "ten_orbit": ten_orbit["path"],
        "drops": drops,
        "growths": growths,
        "first_growth": first_growth,
        "strip_54_hits": affine_hits,
        "aliquot_at_49": ALIQUOT_AT_49,
        "juggler_at_49": JUGGLER_AT_49,
        "image_at_49": step(49),
        "image_at_8": step(8),
        "census_affine_system": target.affine_system(),
        "universal_reach_prime": False,
        "note": "seed-49 prefix is not a map theorem on integers >= 2",
    }


def falsify_claims(spec: FactorConcatSpec | None = None) -> dict[str, dict[str, object]]:
    report = evidence_state(spec)
    return {
        "residue_affine_cover": {
            "claim": "the map is residue-affine / piecewise-affine in the frozen census language",
            "holds_on_window": report["census_affine_system"] is not None,
            "status": "REFUTED",
            "counterexample": "affine_system is None; successor concatenates prime factors",
        },
        "seed_halt_is_z_theorem": {
            "claim": "the packet-seed prefix is a theorem that every n>=2 reaches a prime",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": report["start_orbit"],
        },
        "this_is_aliquot": {
            "claim": "the successor is sigma(n)-n",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {
                "n": 49,
                "image": report["image_at_49"],
                "sigma_minus_n": ALIQUOT_AT_49,
            },
        },
        "this_is_juggler": {
            "claim": "the successor is the even/odd floor-power map",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {"n": 49, "image": report["image_at_49"], "floor_power": JUGGLER_AT_49},
        },
        "this_is_reverse_add": {
            "claim": "the successor is balanced-ternary reverse-plus-add",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {"n": 8, "image": report["image_at_8"], "reverse_add": REVERSE_ADD_AT_8},
        },
        "new_concat_attack": {
            "claim": "progress requires a new factorization-concatenation attack",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": "exact I/O is the problem definition; frozen stack diagnoses the regime",
        },
    }
