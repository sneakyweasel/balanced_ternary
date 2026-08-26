"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.linear_constraint_loops.spec import rplus_images
from research.weak_collatz_floor_5x4_rplus.spec import map_spec, strip_images

WINDOW = tuple(range(2, 81))
RPLUS_WINDOW = tuple(range(3, 81))


def step(x: int) -> int | None:
    images = strip_images(x)
    if len(images) != 1:
        return None
    return images[0]


def orbit_of(n: int, *, max_steps: int = 16) -> tuple[int, ...]:
    seen: list[int] = []
    current = n
    for _ in range(max_steps):
        if current in seen:
            break
        nxt = step(current)
        seen.append(current)
        if nxt is None:
            break
        current = nxt
    return tuple(seen)


def successor_counts(window: tuple[int, ...] = WINDOW) -> dict[int, int]:
    counts: dict[int, int] = {}
    for seed in window:
        n = len(strip_images(seed))
        counts[n] = counts.get(n, 0) + 1
    return counts


def remainder_pairs(window: tuple[int, ...] = WINDOW) -> frozenset[tuple[int, int]]:
    pairs: set[tuple[int, int]] = set()
    for seed in window:
        image = step(seed)
        if image is None:
            continue
        pairs.add((5 * seed - 4 * image, seed % 4))
    return frozenset(pairs)


def rplus_undefined(window: tuple[int, ...] = RPLUS_WINDOW) -> tuple[int, ...]:
    missing = [seed for seed in window if not rplus_images(seed)]
    return tuple(missing)


def undefined_in_domain(window: tuple[int, ...] = WINDOW) -> tuple[int, ...]:
    return tuple(seed for seed in window if step(seed) is None)


def evidence_state(spec=None) -> dict[str, object]:
    target = spec if spec is not None else map_spec()
    path = orbit_of(target.start, max_steps=target.start_remaining)
    path32 = orbit_of(target.start, max_steps=32)
    counts = successor_counts()
    pairs = remainder_pairs()
    rplus_gap = rplus_undefined()
    dropped = undefined_in_domain()
    below = tuple(x for x in range(-5, 2) if strip_images(x))
    fixed = tuple(seed for seed in (2, 3, 4) if step(seed) == seed)
    grew = all(path[i] > path[i - 1] for i in range(1, len(path)))
    return {
        "start": target.start,
        "path": path,
        "path32": path32,
        "path_undefined": step(path[-1]) is None,
        "path32_undefined": step(path32[-1]) is None,
        "path_grows": grew,
        "unique_on_window": counts == {1: len(WINDOW)},
        "successor_counts": counts,
        "undefined_in_domain": dropped,
        "images_below_domain": below,
        "fixed_points_2_3_4": fixed,
        "remainder_pairs": tuple(sorted(pairs)),
        "remainders_are_1_to_4": {item[0] for item in pairs} <= {1, 2, 3, 4},
        "rplus_undefined": rplus_gap,
        "rplus_can_be_undefined": bool(rplus_gap),
        "interval_length": 4,
        "coeff": 4,
        "rplus_interval_length": 2,
        "rplus_coeff": 3,
        "maps_differ_at_8": (step(8), rplus_images(8)[0] if rplus_images(8) else None),
        "horizon_unique_stable": successor_counts(tuple(range(2, 33))) == {1: 31},
        "note": "unique successor on x>=2 is not a basin obstruction and not a halt theorem",
    }


def falsify_claims(spec=None) -> dict[str, dict[str, object]]:
    target = spec if spec is not None else map_spec()
    report = evidence_state(target)
    return {
        "four_thirds_is_the_yield": {
            "claim": "rediscovering the 4/3 SLC language is the mathematical yield",
            "holds_on_window": True,
            "status": "REFUTED",
            "counterexample": "4/3 reconstruction is KNOWN infrastructure",
        },
        "this_is_the_four_thirds_loop": {
            "claim": "the 5x-4 strip is the same map as the 4x-2 strip",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": report["maps_differ_at_8"],
        },
        "every_orbit_loses_successor": {
            "claim": "every orbit on the closed strip loses its successor",
            "holds_on_window": bool(report["undefined_in_domain"]) or report["path_undefined"],
            "status": "REFUTED",
            "counterexample": {
                "unique_on_window": report["unique_on_window"],
                "fixed_points": report["fixed_points_2_3_4"],
                "path": report["path"],
            },
        },
        "finite_halt_is_a_map_theorem": {
            "claim": "finite seed halt on the budget is a map theorem on Z",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {
                "path_undefined": report["path_undefined"],
                "path_grows": report["path_grows"],
            },
        },
        "image_class_excludes_basin": {
            "claim": "a residue image class excludes a basin of losing the successor",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": "unique successor on x>=2; complementary classes still have successors",
        },
        "unique_successor": {
            "claim": "every x>=2 in the window has a unique integer successor",
            "holds_on_window": report["unique_on_window"],
            "status": "EXACT",
            "counterexample": None,
        },
        "rplus_always_defined": {
            "claim": "the 4/3 strip is defined at every x>=3, as this strip is at every x>=2",
            "holds_on_window": not report["rplus_can_be_undefined"],
            "status": "REFUTED",
            "counterexample": report["rplus_undefined"][:8],
        },
        "horizon_changes_uniqueness": {
            "claim": "widening the window inside the budget changes uniqueness",
            "holds_on_window": not report["horizon_unique_stable"],
            "status": "REFUTED",
            "counterexample": report["successor_counts"],
        },
    }
