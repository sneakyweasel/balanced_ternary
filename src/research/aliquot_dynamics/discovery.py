"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.aliquot_dynamics.spec import (
    DEFINED,
    TERMINAL,
    TRANSITION_UNRESOLVED,
    SigmaMinusNSpec,
    map_spec,
    transition_status,
)

WINDOW = tuple(range(1, 61))
ORBIT_CAP = 40
CYCLE_CAP = 6


def step(spec: SigmaMinusNSpec, x: int) -> int | None:
    if transition_status(x) == TRANSITION_UNRESOLVED:
        return None
    images = spec.successors(x)
    if len(images) != 1:
        return None
    return images[0]


def orbit(spec: SigmaMinusNSpec, start: int, *, max_steps: int | None = None) -> dict[str, object]:
    if max_steps is None:
        max_steps = max(ORBIT_CAP, 8)
    seen: list[int] = []
    current = start
    for _ in range(max_steps):
        status = transition_status(current)
        if status == TRANSITION_UNRESOLVED:
            return {
                "path": tuple(seen + [current]),
                "status": TRANSITION_UNRESOLVED,
                "kind": "truncated",
            }
        if current in seen:
            return {"path": tuple(seen), "status": DEFINED, "kind": "cycle"}
        nxt = step(spec, current)
        seen.append(current)
        if nxt is None:
            return {
                "path": tuple(seen),
                "status": TERMINAL if status == TERMINAL or current <= 0 else DEFINED,
                "kind": "halt",
            }
        current = nxt
    return {"path": tuple(seen), "status": DEFINED, "kind": "truncated"}


def magnitude_census(spec: SigmaMinusNSpec, window: tuple[int, ...] = WINDOW) -> dict[str, object]:
    drops = 0
    growths = 0
    equals = 0
    undefined = 0
    unresolved = 0
    first_growth: int | None = None
    first_equal: int | None = None
    for seed in window:
        status = transition_status(seed)
        if status == TRANSITION_UNRESOLVED:
            unresolved += 1
            continue
        image = step(spec, seed)
        if image is None:
            undefined += 1
            continue
        if image < seed:
            drops += 1
        elif image > seed:
            growths += 1
            if first_growth is None:
                first_growth = seed
        else:
            equals += 1
            if first_equal is None:
                first_equal = seed
    if growths == 0 and equals == 0 and drops > 0:
        contraction = "CONTRACTION"
    elif growths > 0 and drops > 0:
        contraction = "REFUTED"
    elif equals > 0 and growths == 0:
        contraction = "PARTIAL_CONTRACTION"
    else:
        contraction = "UNKNOWN"
    return {
        "drops": drops,
        "growths": growths,
        "equals": equals,
        "undefined": undefined,
        "unresolved": unresolved,
        "sampled": len(window),
        "contraction": contraction,
        "first_growth": first_growth,
        "first_equal": first_equal,
        "quantifier": "UNIVERSAL",
        "scope": "CERTIFIED ON WINDOW" if unresolved == 0 else TRANSITION_UNRESOLVED,
    }


def short_cycles(
    spec: SigmaMinusNSpec,
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
            if transition_status(current) != DEFINED:
                break
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


def falsify_claims(spec: SigmaMinusNSpec | None = None) -> dict[str, dict[str, object]]:
    target = spec if spec is not None else map_spec(start=12)
    mag = magnitude_census(target)
    cycles = short_cycles(target)
    return {
        "strict_descent": {
            "claim": "every defined image satisfies A(n) < n",
            "holds_on_window": mag["contraction"] == "CONTRACTION",
            "status": mag["contraction"],
            "counterexample": mag["first_growth"],
            "census": mag,
            "quantifier": "UNIVERSAL",
            "evidence": "CERTIFIED ON WINDOW" if mag["contraction"] == "REFUTED" else mag["scope"],
        },
        "no_fixed_point": {
            "claim": "no n with A(n) = n in the window",
            "holds_on_window": mag["equals"] == 0,
            "counterexample": mag["first_equal"],
            "quantifier": "UNIVERSAL",
            "status": "EXISTENTIAL_WITNESS" if mag["equals"] else "NO PATH FOUND",
        },
        "no_short_cycle": {
            "claim": "no cycle of length at most 6 in the window",
            "holds_on_window": not cycles,
            "cycles": {str(k): v for k, v in cycles.items()},
            "quantifier": "UNIVERSAL",
            "status": "EXISTENTIAL_WITNESS" if cycles else "NO PATH FOUND",
        },
    }
