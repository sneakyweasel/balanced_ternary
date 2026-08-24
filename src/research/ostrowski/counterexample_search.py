"""Search for accepting (or still-completable) paths with |s3| ≥ 3."""

from __future__ import annotations

from collections import deque

from research.ostrowski.residual_closure import State3, reachable_live
from research.ostrowski.transition_extremals import legal_w, order3_transition, residual_is_live


def find_escape(
    max_length: int,
    s3_bound: int = 2,
) -> dict[str, object]:
    """Smallest live path from (0,0,0) whose last coordinate exceeds ``s3_bound``.

    Returns the first BFS witness, or None if every live state at this
    length stays inside the bound. Finite search is not a proof.
    """
    start: State3 = (0, 0, 0)
    parent: dict[tuple[State3, int], tuple[tuple[State3, int], int] | None] = {
        (start, max_length): None
    }
    queue: deque[tuple[State3, int]] = deque([(start, max_length)])
    while queue:
        state, i = queue.popleft()
        if abs(state[2]) > s3_bound:
            path_w = _reconstruct_w(parent, (state, i))
            return {
                "found": True,
                "state": state,
                "remaining": i,
                "w_msd": path_w,
                "length": max_length,
                "s3_bound": s3_bound,
            }
        if i == 0:
            continue
        for w in legal_w(i - 1):
            nxt = order3_transition(state, w)
            if not residual_is_live(nxt, i - 1):
                continue
            key = (nxt, i - 1)
            if key not in parent:
                parent[key] = ((state, i), w)
                queue.append(key)
    return {
        "found": False,
        "state": None,
        "remaining": None,
        "w_msd": None,
        "length": max_length,
        "s3_bound": s3_bound,
        "live_states": reachable_live(max_length)["reachable_residual_states"],
    }


def _reconstruct_w(
    parent: dict[tuple[State3, int], tuple[tuple[State3, int], int] | None],
    node: tuple[State3, int],
) -> tuple[int, ...]:
    ws: list[int] = []
    cur = node
    while parent[cur] is not None:
        prev, w = parent[cur]  # type: ignore[misc]
        ws.append(w)
        cur = prev
    ws.reverse()
    return tuple(ws)


def scan_escapes(max_length: int, s3_bound: int = 2) -> dict[str, object]:
    """Run ``find_escape`` at every length from 1 to ``max_length``."""
    first = None
    rows = []
    for n in range(1, max_length + 1):
        row = find_escape(n, s3_bound=s3_bound)
        rows.append(
            {
                "length": n,
                "found": row["found"],
                "state": row["state"],
                "live_states": None if row["found"] else row.get("live_states"),
            }
        )
        if row["found"] and first is None:
            first = row
    return {
        "max_length": max_length,
        "s3_bound": s3_bound,
        "any_escape": first is not None,
        "first_escape": first,
        "rows": rows,
    }
