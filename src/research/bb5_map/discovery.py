"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.bb5_map.spec import PartialFiveThreeSpec, map_spec

WINDOW = tuple(range(0, 81))
ORBIT_CAP = 80
CYCLE_CAP = 6


def step(spec: PartialFiveThreeSpec, x: int) -> int | None:
    images = spec.successors(x)
    if len(images) != 1:
        return None
    return images[0]


def orbit(spec: PartialFiveThreeSpec, start: int, *, max_steps: int | None = None) -> tuple[int, ...]:
    if max_steps is None:
        max_steps = max(ORBIT_CAP, abs(start) + 2)
    seen: list[int] = []
    current = start
    for _ in range(max_steps):
        if current in seen:
            return tuple(seen)
        nxt = step(spec, current)
        if nxt is None:
            seen.append(current)
            return tuple(seen)
        seen.append(current)
        current = nxt
    return tuple(seen)


def empirical_termination(spec: PartialFiveThreeSpec, window: tuple[int, ...] = WINDOW) -> dict[str, int]:
    stopped = 0
    cyclic = 0
    truncated = 0
    for seed in window:
        path = orbit(spec, seed)
        last = path[-1]
        if step(spec, last) is None:
            stopped += 1
        elif last in path[:-1]:
            cyclic += 1
        else:
            truncated += 1
    return {
        "stopped": stopped,
        "cyclic": cyclic,
        "truncated": truncated,
        "nonstopped": cyclic + truncated,
        "sampled": len(window),
    }


def magnitude_census(spec: PartialFiveThreeSpec, window: tuple[int, ...] = WINDOW) -> dict[str, int]:
    drops = 0
    growths = 0
    equals = 0
    undefined = 0
    for seed in window:
        image = step(spec, seed)
        if image is None:
            undefined += 1
            continue
        if image < seed:
            drops += 1
        elif image > seed:
            growths += 1
        else:
            equals += 1
    return {
        "drops": drops,
        "growths": growths,
        "equals": equals,
        "undefined": undefined,
        "sampled": len(window),
    }


def short_cycles(
    spec: PartialFiveThreeSpec,
    window: tuple[int, ...] = WINDOW,
    *,
    max_len: int = CYCLE_CAP,
) -> dict[int, tuple[tuple[int, ...], ...]]:
    found: dict[int, list[tuple[int, ...]]] = {length: [] for length in range(1, max_len + 1)}
    seen_loops: set[tuple[int, ...]] = set()
    for seed in window:
        current = seed
        path = [current]
        for _ in range(max_len):
            nxt = step(spec, current)
            if nxt is None:
                break
            if nxt in path:
                start = path.index(nxt)
                cycle = tuple(path[start:])
                rotated = _rotate(cycle)
                if rotated not in seen_loops:
                    seen_loops.add(rotated)
                    found[len(cycle)].append(rotated)
                break
            path.append(nxt)
            current = nxt
    return {length: tuple(items) for length, items in found.items() if items}


def _rotate(cycle: tuple[int, ...]) -> tuple[int, ...]:
    if not cycle:
        return cycle
    idx = min(range(len(cycle)), key=lambda i: cycle[i])
    return cycle[idx:] + cycle[:idx]


def falsify_claims(spec: PartialFiveThreeSpec | None = None) -> dict[str, dict[str, object]]:
    target = spec if spec is not None else map_spec()
    mag = magnitude_census(target)
    cycles = short_cycles(target)
    term = empirical_termination(target)
    monotone = mag["growths"] == 0 and mag["equals"] == 0 and mag["drops"] > 0
    no_cycle = not cycles
    all_stop = term["nonstopped"] == 0 and term["stopped"] > 0
    return {
        "monotone_descent": {
            "claim": "every defined step strictly decreases",
            "holds_on_window": monotone,
            "counterexample": None if monotone else _first_growth(target),
            "census": mag,
            "quantifier": "UNIVERSAL",
        },
        "no_nontrivial_cycle": {
            "claim": "no cycle of length at most 6 in the nonnegative window",
            "holds_on_window": no_cycle,
            "cycles": {str(k): v for k, v in cycles.items()},
            "quantifier": "UNIVERSAL",
            "status": "NO PATH FOUND" if no_cycle else "EXISTENTIAL_WITNESS",
        },
        "empirical_termination": {
            "claim": "every window seed eventually has an empty successor menu",
            "holds_on_window": all_stop,
            "census": term,
            "quantifier": "UNIVERSAL",
            "status": "CERTIFIED_ON_WINDOW" if all_stop else "UNKNOWN",
        },
        "one_step_contraction": {
            "claim": "every defined image satisfies |y| < |x| for x != 0",
            "holds_on_window": _contraction_holds(target),
            "counterexample": _first_noncontraction(target),
            "quantifier": "UNIVERSAL",
        },
    }


def _first_growth(spec: PartialFiveThreeSpec) -> int | None:
    for seed in WINDOW:
        image = step(spec, seed)
        if image is not None and image > seed:
            return seed
    return None


def _contraction_holds(spec: PartialFiveThreeSpec) -> bool:
    return _first_noncontraction(spec) is None


def _first_noncontraction(spec: PartialFiveThreeSpec) -> int | None:
    for seed in WINDOW:
        if seed == 0:
            continue
        image = step(spec, seed)
        if image is not None and abs(image) >= abs(seed):
            return seed
    return None
