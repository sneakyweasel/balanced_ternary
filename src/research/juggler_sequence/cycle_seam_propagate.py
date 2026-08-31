"""Adjacent-seam incompatibility propagation.

Phase 0 only: a feasible block O^a E^r produces an output interval
for the next valley. That interval becomes the input constraint for
the next type (a', r'). This module asks whether the composed cell
empties a transition that both independent prefix tests allow, or
whether the finite type graph on bounded (a, r) is a DAG.

Not a halt theorem. A DAG would be a type-graph obstruction, not a
claim that every orbit reaches 1. Not a leftover-killer, not a
finance reopen, not a Q-state law, and not a reopen of local seams,
ordered excursion, cyclic feasibility, or the exponent budget.

Dossier: docs/problems/juggler_cycle_seam_propagate.md.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from typing import Any

from research.juggler_sequence.cycle_almost_search import circuits
from research.juggler_sequence.cycle_budget_opt import oe_start_min
from research.juggler_sequence.cycle_e_block import first_oe_block, prefix_allows_first_run
from research.juggler_sequence.cycle_exponent_budget import rho
from research.juggler_sequence.cycle_finance import DATA_DIR, PUBLISHED_FLOOR
from research.juggler_sequence.cycle_ordered_excursion import (
    excursion_map,
    ooe_blocks_oe,
    two_ooe_still_blocks_oe,
)
from research.juggler_sequence.cyclic_feasibility import (
    Bound,
    forward_image,
    propagate_cycle,
    with_parity,
)

PROPAGATE_DIR = DATA_DIR / "seam_propagate"
START = PUBLISHED_FLOOR + 1

CLASS_CLOSED = "SEAM_PROPAGATE_CLOSED"
CLASS_GREEN = "SEAM_PROPAGATE_GREEN"
CLASS_PARK = "SEAM_PROPAGATE_PARK"

REALIZED_LO = 13
REALIZED_HI = 2001
A_MAX = 6
R_MAX = 4
TUBE_SPAN = 4_000
SHRINK_LO = 1_001
SHRINK_HI = 3_001
LETTER_CAP = 80
SCAN_CAP = 8_000
CONTROLS = (365, 1517)

ARCHIVED = (
    "prefix_allows_first_run",
    "ooe_blocks_oe",
    "two_ooe_still_blocks_oe",
    "forward_image",
    "propagate_cycle",
    "rho",
    "J-block-map-q-state",
)

CLOSURE_WORDS = ("OOOOEE", "OOOOOOEEE", "OOEOOEOOEOE")

Type = tuple[int, int]


def block_word(a: int, r: int) -> str:
    if a < 1 or r < 1:
        raise ValueError("block_word requires a, r >= 1")
    return "O" * a + "E" * r


def bound_dict(bound: Bound) -> dict[str, int | None]:
    return {"lo": bound.lo, "hi": bound.hi}


def block_image(bound: Bound, a: int, r: int) -> Bound:
    """Interval hull of O^a E^r. The landing valley is odd."""

    word = block_word(a, r)
    current = bound
    for index, letter in enumerate(word):
        next_odd = True if index + 1 == len(word) else word[index + 1] == "O"
        current = forward_image(current, letter, next_odd)
        if current.empty():
            return current
    return current


def log_width(bound: Bound) -> float | None:
    if bound.empty() or bound.hi is None or bound.lo <= 0 or bound.hi <= bound.lo:
        return None
    return math.log(bound.hi) - math.log(bound.lo)


def is_archived_adjacency(a: int, r: int, a2: int, r2: int) -> bool:
    """Cheap OOE -> OE at a CycleMin start, including any r' on OE."""

    del r2
    return (a, r) == (2, 1) and a2 == 1


def independent_ok(a: int, r: int, a2: int, r2: int) -> bool:
    return prefix_allows_first_run(a, r) and prefix_allows_first_run(a2, r2)


def pair_row(src: Bound, a: int, r: int, a2: int, r2: int) -> dict[str, Any]:
    mid = block_image(src, a, r)
    out = Bound(1, 0) if mid.empty() else block_image(mid, a2, r2)
    return {
        "a": a,
        "r": r,
        "a2": a2,
        "r2": r2,
        "independent_ok": independent_ok(a, r, a2, r2),
        "archived_adjacency": is_archived_adjacency(a, r, a2, r2),
        "mid_empty": mid.empty(),
        "composed_empty": out.empty(),
        "mid": bound_dict(mid),
        "out": bound_dict(out),
    }


def pair_table(
    src: Bound,
    *,
    a_min: int,
    a_max: int = A_MAX,
    r_max: int = R_MAX,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    new_empty: list[dict[str, Any]] = []
    archived_hits = 0
    n_independent = 0
    n_composed_empty = 0
    for a in range(a_min, a_max + 1):
        for r in range(1, r_max + 1):
            for a2 in range(a_min, a_max + 1):
                for r2 in range(1, r_max + 1):
                    allowed = independent_ok(a, r, a2, r2)
                    archived = is_archived_adjacency(a, r, a2, r2)
                    # Prefix-forbidden pairs are not adjacent incompatibilities.
                    # Compose only the independently allowed edges.
                    if allowed:
                        n_independent += 1
                        row = pair_row(src, a, r, a2, r2)
                        composed = bool(row["composed_empty"])
                    else:
                        composed = False
                    compact = {
                        "a": a,
                        "r": r,
                        "a2": a2,
                        "r2": r2,
                        "independent_ok": allowed,
                        "archived_adjacency": archived,
                        "composed_empty": composed,
                    }
                    rows.append(compact)
                    if composed:
                        n_composed_empty += 1
                        if archived:
                            archived_hits += 1
                        elif allowed:
                            new_empty.append(compact)
    return {
        "src": bound_dict(src),
        "a_min": a_min,
        "a_max": a_max,
        "r_max": r_max,
        "n_rows": len(rows),
        "n_composed_empty": n_composed_empty,
        "n_independent_ok": n_independent,
        "n_archived_empty_and_independent": archived_hits,
        "new_empty": new_empty,
        "n_new_empty": len(new_empty),
    }


def first_ooe_start(n: int, *, span: int = 400) -> int | None:
    """Least odd v >= n whose first block is OOE."""

    start = n if n % 2 else n + 1
    for v in range(start, start + span, 2):
        rec = first_oe_block(v, cap=3)
        if rec["a0"] == 2 and rec["r"] == 1:
            return v
    return None


def cyclemin_oe_block(n: int) -> dict[str, Any]:
    """Recover archived cheap-OOE adjacency at a CycleMin start."""

    ooe_start = first_ooe_start(n)
    mapped = excursion_map(ooe_start, 2) if ooe_start is not None else None
    peak, landing = mapped if mapped is not None else (None, None)
    oe_min = oe_start_min(n)
    landing_below = landing is not None and landing < oe_min
    second = None
    two_landing = None
    two_below = False
    if landing is not None and landing % 2 == 1:
        second = excursion_map(landing, 2)
        if second is not None:
            two_landing = second[1]
            two_below = two_landing < oe_min
    return {
        "n": n,
        "ooe_start": ooe_start,
        "oe_start_min": oe_min,
        "ooe_blocks_oe": ooe_blocks_oe(n, n),
        "two_ooe_still_blocks_oe": two_ooe_still_blocks_oe(n, n),
        "excursion_peak": peak,
        "excursion_landing": landing,
        "landing_below_oe_min": landing_below,
        "two_ooe_landing": two_landing,
        "two_ooe_landing_below_oe_min": two_below,
        "prefix_2_1": prefix_allows_first_run(2, 1),
        "prefix_2_2": prefix_allows_first_run(2, 2),
        "prefix_3_2": prefix_allows_first_run(3, 2),
        "prefix_4_2": prefix_allows_first_run(4, 2),
    }


def walk_blocks(n: int, *, letter_cap: int = LETTER_CAP) -> list[dict[str, Any]]:
    """Successive O^a E^r blocks until the orbit drops below n."""

    if n < 1 or n % 2 == 0:
        raise ValueError("walk_blocks requires a positive odd n")
    blocks: list[dict[str, Any]] = []
    state = n
    letters = 0
    seen: set[int] = set()
    while state >= 2 and state % 2 == 1 and letters < letter_cap:
        if state in seen:
            break
        seen.add(state)
        rec = first_oe_block(state, cap=letter_cap - letters)
        if rec["a0"] < 1 or rec["r"] < 1:
            break
        letters += rec["a0"] + rec["r"]
        valley = rec["valley"]
        shaped = (
            rec["a0"] >= 2
            and prefix_allows_first_run(rec["a0"], rec["r"])
            and valley >= n
        )
        blocks.append(
            {
                "start": state,
                "a": rec["a0"],
                "r": rec["r"],
                "valley": valley,
                "cyclemin_shaped": shaped,
            }
        )
        if valley < n or valley < 2 or valley % 2 == 0:
            break
        state = valley
    return blocks


def _graph_stats(edges: list[tuple[Type, Type]]) -> dict[str, Any]:
    outgoing: dict[Type, set[Type]] = defaultdict(set)
    nodes: set[Type] = set()
    for src, dst in edges:
        outgoing[src].add(dst)
        nodes.add(src)
        nodes.add(dst)
    out_deg = {f"{a},{r}": len(outgoing[(a, r)]) for a, r in outgoing}
    return {
        "n_nodes": len(nodes),
        "n_edges": len(set(edges)),
        "n_edge_instances": len(edges),
        "has_directed_cycle": _has_directed_cycle(outgoing, nodes),
        "max_out_degree": max(out_deg.values(), default=0),
        "multivalued": any(deg >= 2 for deg in out_deg.values()),
        "self_loop_ooe": (2, 1) in outgoing and (2, 1) in outgoing[(2, 1)],
        "out_degree": out_deg,
        "edges": [
            {"src": [a, r], "dst": [a2, r2]}
            for (a, r), (a2, r2) in sorted(set(edges))
        ],
    }


def _has_directed_cycle(
    outgoing: dict[Type, set[Type]],
    nodes: set[Type],
) -> bool:
    white, gray, black = 0, 1, 2
    color = {node: white for node in nodes}

    def dfs(node: Type) -> bool:
        color[node] = gray
        for nxt in outgoing.get(node, ()):
            if nxt not in color:
                color[nxt] = white
            if color[nxt] == gray:
                return True
            if color[nxt] == white and dfs(nxt):
                return True
        color[node] = black
        return False

    return any(dfs(node) for node in list(nodes) if color[node] == white)


def realized_transition_graph(
    *,
    lo: int = REALIZED_LO,
    hi: int = REALIZED_HI,
) -> dict[str, Any]:
    edges: list[tuple[Type, Type]] = []
    shaped_edges: list[tuple[Type, Type]] = []
    n_starts = 0
    n_block_pairs = 0
    for start in range(lo if lo % 2 else lo + 1, hi, 2):
        blocks = walk_blocks(start)
        if not blocks:
            continue
        n_starts += 1
        for index in range(len(blocks) - 1):
            src = (blocks[index]["a"], blocks[index]["r"])
            dst = (blocks[index + 1]["a"], blocks[index + 1]["r"])
            edges.append((src, dst))
            n_block_pairs += 1
            if blocks[index]["cyclemin_shaped"] and blocks[index + 1]["cyclemin_shaped"]:
                shaped_edges.append((src, dst))
    full = _graph_stats(edges)
    shaped = _graph_stats(shaped_edges)
    return {
        "lo": lo,
        "hi": hi,
        "n_starts": n_starts,
        "n_block_pairs": n_block_pairs,
        "full": full,
        "cyclemin_shaped": shaped,
    }


def control_split(controls: tuple[int, ...] = CONTROLS) -> dict[str, Any]:
    """365 vs 1517 remain multi-valued; not a new state law."""

    rows = []
    type_lists: list[list[Type]] = []
    for n in controls:
        blocks = walk_blocks(n)
        types = [(rec["a"], rec["r"]) for rec in blocks]
        type_lists.append(types)
        rows.append({"n": n, "blocks": types[:6]})
    same_prefix = False
    split = False
    if len(type_lists) >= 2:
        left, right = type_lists[0], type_lists[1]
        prefix = 0
        while prefix < min(len(left), len(right)) and left[prefix] == right[prefix]:
            prefix += 1
        same_prefix = prefix >= 1
        split = prefix < min(len(left), len(right)) and left[prefix] != right[prefix]
    return {
        "controls": rows,
        "shared_prefix_then_split": same_prefix and split,
        "note": "multi-valued successors reconfirm J-block-map-q-state; not a new refutation",
    }


def shrink_row(lo: int, hi: int, a: int, r: int) -> dict[str, Any]:
    src = with_parity(Bound(lo, hi), True)
    out = block_image(src, a, r)
    width_in = log_width(src)
    width_out = log_width(out)
    rho_val = float(rho(a, r))
    ratio = None if width_in is None or width_out is None else width_out / width_in
    matches = ratio is not None and abs(ratio - rho_val) < 0.15
    return {
        "a": a,
        "r": r,
        "src": bound_dict(src),
        "out": bound_dict(out),
        "rho": str(rho(a, r)),
        "log_width_in": width_in,
        "log_width_out": width_out,
        "width_ratio": ratio,
        "matches_rho": matches,
    }


def shrink_check() -> dict[str, Any]:
    rows = [
        shrink_row(SHRINK_LO, SHRINK_HI, 2, 1),
        shrink_row(SHRINK_LO, SHRINK_HI, 1, 1),
        shrink_row(START, START + TUBE_SPAN, 2, 1),
    ]
    return {
        "rows": rows,
        "all_match_rho": all(row["matches_rho"] for row in rows),
        "note": "log-width ratio equals rho up to floor slack; that is the closed exponent budget",
    }


def word_expanding(word: str) -> bool:
    odd = word.count("O")
    return 2 ** len(word) < 3**odd


def block_propagate(
    word: str,
    cap: int | None,
    *,
    rounds: int | None = None,
) -> tuple[list[Bound], bool]:
    """Cyclic slot propagation on valleys. Same algorithm as propagate_cycle."""

    blocks = circuits(word)
    bounds = [with_parity(Bound(3, cap), True) for _ in blocks]
    limit = rounds if rounds is not None else 2 * len(blocks) + 6
    for _ in range(limit):
        changed = False
        for index, (a, r) in enumerate(blocks):
            nxt = (index + 1) % len(blocks)
            img = block_image(bounds[index], a, r)
            new = bounds[nxt].intersect(img)
            if new.lo != bounds[nxt].lo or new.hi != bounds[nxt].hi:
                changed = True
            bounds[nxt] = new
            if new.empty():
                return bounds, True
        if not changed:
            break
    return bounds, any(bound.empty() for bound in bounds)


def closure_row(word: str, cap: int | None = SCAN_CAP) -> dict[str, Any]:
    _letter_bounds, letter_empty = propagate_cycle(word, cap)
    _block_bounds, block_empty = block_propagate(word, cap)
    stronger = block_empty and not letter_empty
    return {
        "word": word,
        "blocks": list(circuits(word)),
        "expanding": word_expanding(word),
        "letter_empty": letter_empty,
        "block_empty": block_empty,
        "block_strictly_stronger": stronger,
        "agree": not stronger,
    }


def closure_check() -> dict[str, Any]:
    rows = [closure_row(word) for word in CLOSURE_WORDS]
    return {
        "rows": rows,
        "all_expanding": all(row["expanding"] for row in rows),
        "all_agree": all(row["agree"] for row in rows),
        "note": (
            "block-level C_{k+1}=C_1 is not strictly stronger than "
            "letter-level propagate_cycle; a finite cap may empty both"
        ),
    }


def classify(payload: dict[str, Any]) -> dict[str, Any]:
    archived = payload["archived_cyclemin"]
    wide = payload["wide_pairs"]
    tube = payload["tube_pairs"]
    middle = payload["middle_pairs"]
    graph = payload["realized_graph"]
    shrink = payload["shrink"]
    closure = payload["closure"]
    archived_ok = (
        bool(archived["ooe_blocks_oe"])
        and bool(archived["two_ooe_still_blocks_oe"])
        and archived["ooe_start"] is not None
        and bool(archived["landing_below_oe_min"])
        and bool(archived["prefix_2_1"])
        and not bool(archived["prefix_2_2"])
        and not bool(archived["prefix_3_2"])
        and bool(archived["prefix_4_2"])
    )
    new_empty = (
        int(wide["n_new_empty"])
        + int(tube["n_new_empty"])
        + int(middle["n_new_empty"])
    ) > 0
    cyclic = bool(graph["full"]["has_directed_cycle"])
    shaped_cyclic = bool(graph["cyclemin_shaped"]["has_directed_cycle"])
    shaped_edges = int(graph["cyclemin_shaped"]["n_edges"])
    shaped_dag = shaped_edges > 0 and not shaped_cyclic
    multivalued = bool(graph["full"]["multivalued"])
    shrink_ok = bool(shrink["all_match_rho"])
    closure_ok = bool(closure["all_agree"]) and bool(closure["all_expanding"])
    if archived_ok and not new_empty and cyclic and shaped_cyclic and shrink_ok and closure_ok:
        classification = CLASS_CLOSED
        decision = "CLOSE"
        reason = (
            "every composed emptiness is the archived cheap-OOE "
            "adjacency or a prefix-test failure; the realized type "
            "graph has a directed cycle (including the CycleMin-shaped "
            "subgraph); log-width shrink matches rho; block-level "
            "C_{k+1}=C_1 matches propagate_cycle"
        )
    elif new_empty or shaped_dag:
        classification = CLASS_GREEN
        decision = "PROMOTE"
        reason = (
            "a composed cell empties a transition both prefix tests "
            "allow that is not the archived cheap-OOE adjacency, or "
            "the CycleMin-legal bounded type graph is a DAG"
        )
    else:
        classification = CLASS_PARK
        decision = "PARK"
        reason = "the adjacent-seam census is mixed and does not decide"
    return {
        "classification": classification,
        "decision": decision,
        "reason": reason,
        "archived_recovered": archived_ok,
        "new_composed_emptiness": new_empty,
        "realized_graph_cyclic": cyclic,
        "cyclemin_shaped_cyclic": shaped_cyclic,
        "realized_graph_multivalued": multivalued,
        "shrink_matches_rho": shrink_ok,
        "block_closure_matches_letter": closure_ok,
        "type_graph_is_dag": shaped_dag,
        "leftover_killer": False,
        "reopens_ordered_excursion": False,
        "reopens_cyclic_feasibility": False,
        "reopens_exponent_budget": False,
        "halt_theorem": False,
        "raise_n0": False,
        "paper_a_edit": False,
        "archived": list(ARCHIVED),
    }


def probe_payload(*, n: int = START) -> dict[str, Any]:
    wide_src = with_parity(Bound(3, n), True)
    tube_src = with_parity(Bound(n, n + TUBE_SPAN), True)
    middle_src = with_parity(Bound(3, n), True)
    payload = {
        "bound": "seam_propagate",
        "n": n,
        "published_floor": PUBLISHED_FLOOR,
        "archived_cyclemin": cyclemin_oe_block(n),
        "wide_pairs": pair_table(wide_src, a_min=2),
        "tube_pairs": pair_table(tube_src, a_min=2),
        "middle_pairs": pair_table(middle_src, a_min=1),
        "realized_graph": realized_transition_graph(),
        "controls": control_split(),
        "shrink": shrink_check(),
        "closure": closure_check(),
    }
    payload["decision"] = classify(payload)
    return payload


def write_artifacts(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload if payload is not None else probe_payload()
    PROPAGATE_DIR.mkdir(parents=True, exist_ok=True)
    path = PROPAGATE_DIR / "summary.json"
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return data


def main() -> None:
    payload = write_artifacts()
    decision = payload["decision"]
    print(decision["classification"])
    print(decision["reason"])
    print(
        json.dumps(
            {
                "n": payload["n"],
                "landing_below_oe_min": payload["archived_cyclemin"][
                    "landing_below_oe_min"
                ],
                "wide_new_empty": payload["wide_pairs"]["n_new_empty"],
                "tube_new_empty": payload["tube_pairs"]["n_new_empty"],
                "middle_new_empty": payload["middle_pairs"]["n_new_empty"],
                "graph_cyclic": payload["realized_graph"]["full"]["has_directed_cycle"],
                "shaped_cyclic": payload["realized_graph"]["cyclemin_shaped"][
                    "has_directed_cycle"
                ],
                "self_loop_ooe": payload["realized_graph"]["full"]["self_loop_ooe"],
                "shrink_ok": payload["shrink"]["all_match_rho"],
                "closure_ok": payload["closure"]["all_agree"],
                "decision": decision["decision"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
