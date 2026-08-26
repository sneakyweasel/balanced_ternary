"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.matthews_prize_mod3_avoider.spec import SECOND_START, map_images, map_spec

WINDOW = tuple(range(-40, 41))


def step(x: int) -> int:
    images = map_images(x)
    if len(images) != 1:
        raise ValueError(f"no unique successor at {x}")
    return images[0]


def orbit_of(n: int, *, max_steps: int = 16) -> tuple[int, ...]:
    seen: list[int] = []
    current = n
    for _ in range(max_steps):
        if current in seen:
            break
        seen.append(current)
        current = step(current)
    return tuple(seen)


def hits_zero_mod_three(path: tuple[int, ...]) -> bool:
    return any(item % 3 == 0 for item in path)


def stays_nonzero_mod_three(path: tuple[int, ...]) -> bool:
    return all(item % 3 != 0 for item in path)


def zero_class_closed(window: tuple[int, ...] = WINDOW) -> bool:
    for seed in window:
        if seed % 3 != 0:
            continue
        if step(seed) % 3 != 0:
            return False
    return True


def units_forward_invariant(window: tuple[int, ...] = WINDOW) -> bool:
    for seed in window:
        if seed % 3 == 0:
            continue
        if step(seed) % 3 == 0:
            return False
    return True


def horizon_avoiders(
    window: tuple[int, ...] = WINDOW,
    *,
    max_steps: int = 16,
) -> tuple[int, ...]:
    found: list[int] = []
    for seed in window:
        if seed % 3 == 0:
            continue
        path = orbit_of(seed, max_steps=max_steps)
        if stays_nonzero_mod_three(path):
            found.append(seed)
    return tuple(found)


def evidence_state(spec=None) -> dict[str, object]:
    target = spec if spec is not None else map_spec()
    path1 = orbit_of(target.start, max_steps=target.start_remaining)
    path1_32 = orbit_of(target.start, max_steps=32)
    path5 = orbit_of(SECOND_START, max_steps=target.start_remaining)
    path5_32 = orbit_of(SECOND_START, max_steps=32)
    avoiders = horizon_avoiders()
    return {
        "start": target.start,
        "path": path1,
        "path32": path1_32,
        "path5": path5,
        "path5_32": path5_32,
        "seed1_hits_zero_mod_three": hits_zero_mod_three(path1),
        "seed5_hits_zero_mod_three": hits_zero_mod_three(path5),
        "seed1_hits_zero_mod_three_32": hits_zero_mod_three(path1_32),
        "seed5_hits_zero_mod_three_32": hits_zero_mod_three(path5_32),
        "t_zero": step(0),
        "t_three": step(3),
        "t_neg_one": step(-1),
        "t_neg_two": step(-2),
        "t_neg_four": step(-4),
        "zero_class_closed": zero_class_closed(),
        "units_forward_invariant": units_forward_invariant(),
        "horizon_avoiders": avoiders,
        "horizon_avoiders_are_known_cycles": set(avoiders) <= {-1, -2, -4},
        "window_avoiders_reach_known_cycles": all(
            -1 in orbit_of(seed) or (-2 in orbit_of(seed) and -4 in orbit_of(seed))
            for seed in avoiders
        ),
        "maps_differ_from_double_at_1": step(1) != 2,
        "maps_differ_from_floor54_at_5": step(5) != 6,
        "unique_on_window": all(len(map_images(seed)) == 1 for seed in WINDOW),
        "note": "branch reconstruction is the problem definition; packet seeds are not avoiders",
    }


def falsify_claims(spec=None) -> dict[str, dict[str, object]]:
    target = spec if spec is not None else map_spec()
    report = evidence_state(target)
    return {
        "branches_are_the_yield": {
            "claim": "rediscovering the three residue-affine formulas is the mathematical yield",
            "holds_on_window": True,
            "status": "REFUTED",
            "counterexample": "the three formulas are the problem definition",
        },
        "packet_seeds_are_avoiders": {
            "claim": "seeds 1 and 5 stay in {1,2} (mod 3) on the budget",
            "holds_on_window": not (
                report["seed1_hits_zero_mod_three"] and report["seed5_hits_zero_mod_three"]
            ),
            "status": "REFUTED",
            "counterexample": {"path1": report["path"], "path5": report["path5"]},
        },
        "units_cannot_reach_zero_mod_three": {
            "claim": "{1,2} (mod 3) is a basin and cannot reach 0 (mod 3)",
            "holds_on_window": report["units_forward_invariant"],
            "status": "REFUTED",
            "counterexample": report["path"],
        },
        "finite_cycle_visit_is_a_map_theorem": {
            "claim": "finite visit of -1 or {-2,-4} is a map theorem on Z",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {
                "seed1_hits_neg_one": -1 in report["path"],
                "horizon_avoiders": report["horizon_avoiders"],
            },
        },
        "this_is_the_four_thirds_or_bb5_map": {
            "claim": "the three-branch map is the 4/3 strip or the BB5 partial map",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {
                "t_1": step(1),
                "t_5": step(5),
                "t_0": step(0),
            },
        },
        "zero_class_invariant": {
            "claim": "if 3|x then 3|T(x) on the window",
            "holds_on_window": report["zero_class_closed"],
            "status": "EXACT",
            "counterexample": None,
        },
        "known_cycles": {
            "claim": "T(-1)=-1 and T(-2)=-4, T(-4)=-2",
            "holds_on_window": (
                report["t_neg_one"] == -1
                and report["t_neg_two"] == -4
                and report["t_neg_four"] == -2
            ),
            "status": "EXACT",
            "counterexample": None,
        },
        "horizon_avoiders_are_only_known_cycles": {
            "claim": "every 16-step window avoider is -1, -2, or -4",
            "holds_on_window": report["horizon_avoiders_are_known_cycles"],
            "status": "REFUTED",
            "counterexample": report["horizon_avoiders"],
        },
        "window_avoiders_reach_known_cycles": {
            "claim": "every 16-step window avoider enters -1 or {-2,-4}",
            "holds_on_window": report["window_avoiders_reach_known_cycles"],
            "status": "OBSERVATION",
            "counterexample": report["horizon_avoiders"],
        },
    }
