"""Bounded EXISTS_PATH / ALL_PATHS probes wrapping legal_controls and closure."""

from __future__ import annotations

from research_engine.attacks.result import AttackContext
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import State
from research_engine.quantifiers.relation import legal_images, seed_states, working_phase
from research_engine.quantifiers.types import PathQuantifier, PathStatus

DEFAULT_WINDOW = tuple(range(-12, 13))
CYCLE_CAP = 6
ORBIT_CAP = 24
PATH_CAP = 4000
VISIT_CAP = 8000


def _rotate(cycle: tuple[State, ...]) -> tuple[State, ...]:
    if not cycle:
        return cycle
    idx = min(range(len(cycle)), key=lambda i: cycle[i])
    return cycle[idx:] + cycle[:idx]


def existential_cycle_witness(
    spec: ProblemSpec,
    context: AttackContext,
    window: tuple[int, ...] | None = None,
    *,
    max_len: int = CYCLE_CAP,
    path_cap: int = PATH_CAP,
) -> tuple[State, ...] | None:
    """EXISTENTIAL: one legal cycle, if any. Not a universal cycle claim."""

    phase = working_phase(spec, context)
    seeds = seed_states(spec, window)
    for seed in seeds:
        stack: list[tuple[State, tuple[State, ...]]] = [(seed, (seed,))]
        seen_paths = 0
        while stack and seen_paths < path_cap:
            current, path = stack.pop()
            seen_paths += 1
            if len(path) > max_len:
                continue
            for nxt in legal_images(spec, current, phase):
                if nxt in path:
                    return _rotate(tuple(path[path.index(nxt) :]))
                stack.append((nxt, path + (nxt,)))
    return None


def universal_termination_on_seeds(
    spec: ProblemSpec,
    context: AttackContext,
    window: tuple[int, ...] | None = None,
    *,
    max_depth: int = ORBIT_CAP,
    max_len: int = CYCLE_CAP,
    path_cap: int = PATH_CAP,
    visit_cap: int = VISIT_CAP,
) -> dict[str, object]:
    """UNIVERSAL: every legal path from every window seed hits an empty menu.

    A cycle is a refutation. Truncation is UNKNOWN: NO_PATH_FOUND is not
    nonexistence, and a truncated path is not a terminating path.
    """

    window = DEFAULT_WINDOW if window is None else window
    cycle = existential_cycle_witness(
        spec, context, window, max_len=min(max_depth, max_len), path_cap=path_cap
    )
    if cycle is not None:
        return {
            "holds": False,
            "status": PathStatus.REFUTED,
            "quantifier": PathQuantifier.ALL_PATHS,
            "counterexample": cycle,
            "reason": "EXISTENTIAL_WITNESS of a cycle; not a proof that every path cycles",
        }
    phase = working_phase(spec, context)
    truncated_path: tuple[State, ...] | None = None
    for seed in seed_states(spec, window):
        stack: list[tuple[State, tuple[State, ...]]] = [(seed, (seed,))]
        visited = 0
        while stack and visited < visit_cap:
            current, path = stack.pop()
            visited += 1
            images = legal_images(spec, current, phase)
            if not images:
                continue
            if current in path[:-1]:
                return {
                    "holds": False,
                    "status": PathStatus.REFUTED,
                    "quantifier": PathQuantifier.ALL_PATHS,
                    "counterexample": path,
                    "reason": "EXISTENTIAL_WITNESS of a cycle; not a proof that every path cycles",
                }
            if len(path) > max_depth:
                truncated_path = path
                continue
            for nxt in images:
                stack.append((nxt, path + (nxt,)))
        if stack:
            return {
                "holds": None,
                "status": PathStatus.UNKNOWN,
                "quantifier": PathQuantifier.ALL_PATHS,
                "counterexample": truncated_path or (),
                "reason": "search bound; NO_PATH_FOUND is not a nonexistence theorem",
            }
    if truncated_path is not None:
        return {
            "holds": None,
            "status": PathStatus.UNKNOWN,
            "quantifier": PathQuantifier.ALL_PATHS,
            "counterexample": truncated_path,
            "reason": "truncated path; not a refutation and not a Z-theorem",
        }
    return {
        "holds": True,
        "status": PathStatus.CERTIFIED_ON_WINDOW,
        "quantifier": PathQuantifier.ALL_PATHS,
        "counterexample": (),
        "reason": "every explored legal path from the window hit an empty menu; not a Z-theorem",
    }
