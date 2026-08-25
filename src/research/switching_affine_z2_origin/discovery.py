"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.switching_affine_z2_origin.spec import TwoPathZ2Spec, map_spec, next_state

MAX_INDEX = 64
SMALL = 8


def iterate(
    spec: TwoPathZ2Spec,
    *,
    max_index: int = MAX_INDEX,
    start: tuple[int, int] | None = None,
) -> tuple[tuple[int, int], ...]:
    current = spec.start if start is None else start
    out = [current]
    for _ in range(max_index):
        nxt = next_state(current)
        if nxt is None:
            break
        current = nxt
        out.append(current)
        if current == (0, 0):
            break
    return tuple(out)


def origin_index(path: tuple[tuple[int, int], ...]) -> int | None:
    for index, state in enumerate(path):
        if state == (0, 0):
            return index
    return None


def preimages(target: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    x, y = target
    found: list[tuple[int, int]] = []
    # first branch: (a+b, b-1) = (x, y) => b = y+1, a = x - (y+1)
    found.append((x - (y + 1), y + 1))
    # second branch: (a-1, a+b) = (x, y) => a = x+1, b = y - (x+1)
    found.append((x + 1, y - (x + 1)))
    return tuple(item for item in found if next_state(item) == target)


def nonnegative(state: tuple[int, int]) -> bool:
    return state[0] >= 0 and state[1] >= 0


def evidence_state(spec: TwoPathZ2Spec | None = None) -> dict[str, object]:
    target = spec if spec is not None else map_spec()
    path = iterate(target)
    origin_at = origin_index(path)
    halted = next_state(path[-1]) is None
    unique = len(set(path)) < len(path)
    origin_pre = preimages((0, 0))
    small_hits = []
    small_cycle = False
    for x in range(0, SMALL + 1):
        for y in range(0, SMALL + 1):
            seed = (x, y)
            walk = iterate(target, start=seed, max_index=MAX_INDEX)
            if origin_index(walk) is not None and seed != (0, 0):
                small_hits.append(seed)
            if (1, 0) in walk and (0, 1) in walk:
                small_cycle = True
    n2_class = all((not nonnegative(item)) or item == (0, 0) for item in origin_pre)
    status = "ORIGIN_WITNESS" if origin_at is not None else (
        "HALT_WITNESS" if halted else "CERTIFIED_ON_WINDOW"
    )
    return {
        "status": status,
        "path": path[:24],
        "length": len(path),
        "origin_at": origin_at,
        "halted": halted,
        "repeat": unique,
        "origin_preimages": origin_pre,
        "n2_preimages_only_origin": n2_class,
        "small_origin_hits": tuple(small_hits),
        "small_sees_unit_cycle": small_cycle,
        "cycle_unit": (next_state((1, 0)), next_state((0, 1))),
        "universal_origin": False,
        "computation": (
            "UNBOUNDED_WINDOW" if origin_at is None and not halted else "WITHIN_BUDGET"
        ),
        "note": "finite non-visit of (0,0) is not a basin theorem",
    }


def falsify_claims(spec: TwoPathZ2Spec | None = None) -> dict[str, dict[str, object]]:
    target = spec if spec is not None else map_spec()
    report = evidence_state(target)
    path = iterate(target)
    origin_at = report["origin_at"]
    return {
        "start_reaches_origin": {
            "claim": "the distinguished start reaches (0,0) on the search bound",
            "holds_on_window": origin_at is not None,
            "status": "REFUTED" if origin_at is None else "EXACT",
            "counterexample": None if origin_at is not None else "no origin on bound",
        },
        "all_nonneg_reach_origin": {
            "claim": "every small nonnegative seed reaches (0,0)",
            "holds_on_window": bool(report["small_origin_hits"]),
            "status": "REFUTED",
            "counterexample": (3, 2),
        },
        "no_finite_cycle": {
            "claim": "there is no period-2 orbit on the unit pair",
            "holds_on_window": report["cycle_unit"] != ((0, 1), (1, 0)),
            "status": "REFUTED",
            "counterexample": ((1, 0), (0, 1)),
        },
        "finite_reachable_set_from_start": {
            "claim": "the start orbit is finite within the bound",
            "holds_on_window": len(set(path)) < len(path),
            "status": "REFUTED" if len(set(path)) == len(path) else "EXISTENTIAL_WITNESS",
            "counterexample": None,
        },
        "n2_preimage_is_origin_only": {
            "claim": "the only nonnegative preimage of (0,0) is (0,0) itself",
            "holds_on_window": report["n2_preimages_only_origin"],
            "status": "EXACT" if report["n2_preimages_only_origin"] else "REFUTED",
            "counterexample": None,
        },
    }
