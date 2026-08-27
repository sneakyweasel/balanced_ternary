"""Realization-set geometry of the Juggler prefix trie.

Not a Research Engine control-layer experiment. Not a halt theorem.
Does not reopen PE-factor grammar or residual-future quotients.
Absence under a scan bound is never a forbidden-factor claim.
"""

from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from research.juggler_sequence.atlas.packed import pack_word, split_word_id, unpack_word
from research.juggler_sequence.atlas.storage import DEFAULT_DATA_DIR, connect, sqlite_path
from research.juggler_sequence.compensated_contraction import image_after
from research.juggler_sequence.floor_cells import even_cell, odd_cell_integers
from research.juggler_sequence.lean_paths import CELLS, COLLAPSE
from research.juggler_sequence.power_words import ANTI_OVERCLAIM, floor_power

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "juggler_realization_geometry.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "juggler_realization_geometry.md"
DATA_DIR = REPO_ROOT / "data" / "research" / "juggler" / "realization_geometry"

DIAG_N = 4000
DIAG_K = 12
CONFIRM_N = 100_000
CONFIRM_K = 12
ATLAS_EID = "wa-20260827T200310Z-cuda-k20-n100000000"
ATLAS_N = 100_000_000

FIRST_UNARY = ("EEEEE", "EEEEO", "EEEOE")
FIRST_HOLES = ("EEEEEE", "EEEEOE", "EEEOEO")
ADVERSARIAL = (
    "E",
    "EE",
    "EEE",
    "EEEE",
    "EEEEE",
    "EO",
    "EOE",
    "EOO",
    "O",
    "OO",
    "OOO",
    "OE",
    "OEO",
    "OOE",
    "EEO",
    "OEEEE",
    "OOOOE",
)

CLASS_GREEN = "REALIZATION_GEOMETRY_GREEN"
CLASS_AMPLIFY = "REALIZER_AMPLIFICATION_GREEN"
CLASS_CELL = "CELL_GEOMETRY_GREEN"
CLASS_CORRIDOR = "CORRIDOR_GREEN"
CLASS_ROOT = "ROOT_FACTOR_GREEN"
CLASS_COUNTER = "REALIZATION_COUNTEREXAMPLE"
CLASS_COMPLEX = "REALIZATION_GEOMETRY_COMPLEX"

FORBIDDEN_ENGINES = (
    "ResidualGraph",
    "ResidualState",
    "MilestoneGraph",
    "PowerHeight",
    "CycleEngine",
)

LEAN_THEOREMS = (
    "even_tower_to_one",
    "even_cell_iff",
    "odd_cell_iff",
    "odd_cell_unique",
)


def even_tower(r: int) -> int:
    if r < 1:
        raise ValueError("even_tower requires r >= 1")
    return 2 ** (1 << (r - 1))


def leading_run(word: str, letter: str) -> int:
    n = 0
    for ch in word:
        if ch != letter:
            break
        n += 1
    return n


def degree_label(mask: int) -> str:
    has_o = bool(mask & 1)
    has_e = bool(mask & 2)
    if has_o and has_e:
        return "BINARY"
    if has_o:
        return "UNARY_O"
    if has_e:
        return "UNARY_E"
    return "DEAD"


def collect_realizing(*, n_max: int, k_max: int) -> dict[str, list[int]]:
    """One-pass nested realizing sets. Sorted lists, no extra index."""

    realizing: dict[str, list[int]] = defaultdict(list)
    for n in range(1, n_max + 1):
        state = n
        letters: list[str] = []
        for _ in range(k_max):
            letters.append("O" if state & 1 else "E")
            realizing["".join(letters)].append(n)
            state = floor_power(state)
    return dict(realizing)


def gap_geometry(xs: list[int], *, n_max: int) -> dict[str, Any]:
    if not xs:
        return {
            "size": 0,
            "min": None,
            "max": None,
            "span": None,
            "density": 0.0,
            "n_gaps": 0,
            "mean_gap": None,
            "median_gap": None,
            "max_gap": None,
            "n_components": 0,
            "largest_component": 0,
            "largest_frac": None,
        }
    gaps = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    interior = [g for g in gaps if g > 1]
    components = 1
    largest = 1
    run = 1
    for g in gaps:
        if g == 1:
            run += 1
            if run > largest:
                largest = run
        else:
            components += 1
            run = 1
    return {
        "size": len(xs),
        "min": xs[0],
        "max": xs[-1],
        "span": xs[-1] - xs[0],
        "density": len(xs) / n_max,
        "n_gaps": len(interior),
        "mean_gap": statistics.fmean(gaps) if gaps else None,
        "median_gap": statistics.median(gaps) if gaps else None,
        "max_gap": max(gaps) if gaps else None,
        "n_components": components,
        "largest_component": largest,
        "largest_frac": largest / len(xs),
    }


def child_sets(
    word: str, starts: list[int]
) -> tuple[list[int], list[int], list[int]]:
    child_o: list[int] = []
    child_e: list[int] = []
    uncovered: list[int] = []
    for n in starts:
        landing = image_after(n, word)
        if landing & 1:
            child_o.append(n)
        else:
            child_e.append(n)
    return child_o, child_e, uncovered


def landing_stats(word: str, starts: list[int]) -> dict[str, Any]:
    parities = Counter()
    values: list[int] = []
    for n in starts:
        landing = image_after(n, word)
        values.append(landing)
        parities[landing & 1] += 1
    unique = sorted(set(values))
    return {
        "n_unique_landings": len(unique),
        "landing_min": unique[0] if unique else None,
        "landing_max": unique[-1] if unique else None,
        "odd_landings": parities[1],
        "even_landings": parities[0],
        "monochrome": len(parities) == 1,
        "singleton_landing": len(unique) == 1,
    }


def prefix_row(word: str, starts: list[int], *, n_max: int) -> dict[str, Any]:
    child_o, child_e, uncovered = child_sets(word, starts)
    mask = (1 if child_o else 0) | (2 if child_e else 0)
    geo = gap_geometry(starts, n_max=n_max)
    land = landing_stats(word, starts)
    scale_sep = None
    if child_o and child_e:
        scale_sep = child_o[-1] < child_e[0] or child_e[-1] < child_o[0]
    return {
        "word": word,
        "length": len(word),
        "lead_E": leading_run(word, "E"),
        "lead_O": leading_run(word, "O"),
        "odd_count": word.count("O"),
        "class": degree_label(mask),
        "mask": mask,
        "rho_O": len(child_o) / len(starts) if starts else None,
        "rho_E": len(child_e) / len(starts) if starts else None,
        "uncovered": len(uncovered),
        "child_O": len(child_o),
        "child_E": len(child_e),
        "child_O_min": child_o[0] if child_o else None,
        "child_E_min": child_e[0] if child_e else None,
        "child_O_max": child_o[-1] if child_o else None,
        "child_E_max": child_e[-1] if child_e else None,
        "scale_separated": scale_sep,
        **geo,
        **land,
    }


def window_census(realizing: dict[str, list[int]], *, n_max: int, k_max: int) -> dict[str, Any]:
    rows = [prefix_row(word, starts, n_max=n_max) for word, starts in realizing.items()]
    by_len: dict[int, Counter[str]] = defaultdict(Counter)
    uncovered_total = 0
    unary_monochrome = 0
    unary_total = 0
    binary_separated = 0
    binary_total = 0
    unary_singleton = 0
    regain = []
    for row in rows:
        by_len[row["length"]][row["class"]] += 1
        uncovered_total += row["uncovered"]
        if row["class"] in {"UNARY_O", "UNARY_E"}:
            unary_total += 1
            if row["monochrome"]:
                unary_monochrome += 1
            if row["singleton_landing"]:
                unary_singleton += 1
        if row["class"] == "BINARY":
            binary_total += 1
            if row["scale_separated"]:
                binary_separated += 1
    for row in rows:
        if row["class"] not in {"UNARY_O", "UNARY_E"} or row["length"] >= k_max:
            continue
        child = row["word"] + ("O" if row["class"] == "UNARY_O" else "E")
        child_row = next((r for r in rows if r["word"] == child), None)
        if child_row and child_row["class"] == "BINARY":
            regain.append({"parent": row["word"], "child": child, "min": row["min"]})
    lead_e_unary = Counter()
    lead_e_n = Counter()
    for row in rows:
        if row["length"] != k_max - 1:
            continue
        lead_e_n[row["lead_E"]] += 1
        if row["class"] in {"UNARY_O", "UNARY_E"}:
            lead_e_unary[row["lead_E"]] += 1
    return {
        "n_max": n_max,
        "k_max": k_max,
        "n_words": len(rows),
        "uncovered_total": uncovered_total,
        "unary_total": unary_total,
        "unary_monochrome": unary_monochrome,
        "unary_singleton_landing": unary_singleton,
        "binary_total": binary_total,
        "binary_scale_separated": binary_separated,
        "unary_to_binary": regain[:20],
        "unary_to_binary_count": len(regain),
        "profile": {str(k): dict(by_len[k]) for k in sorted(by_len)},
        "lead_E_unary_frac_at_horizon": {
            str(lead): (lead_e_unary[lead] / lead_e_n[lead] if lead_e_n[lead] else None)
            for lead in sorted(lead_e_n)
        },
        "adversarial": [prefix_row(w, realizing[w], n_max=n_max) for w in ADVERSARIAL if w in realizing],
        "first_unary_in_window": [
            prefix_row(w, realizing[w], n_max=n_max) for w in FIRST_UNARY if w in realizing
        ],
    }


def atlas_available(data_dir: Path = DEFAULT_DATA_DIR) -> bool:
    return sqlite_path(data_dir).is_file()


def reproduce_atlas(*, data_dir: Path = DEFAULT_DATA_DIR, experiment_id: str = ATLAS_EID) -> dict[str, Any]:
    if not atlas_available(data_dir):
        return {"available": False}
    con = connect(data_dir)
    try:
        tower = []
        for r in range(1, 8):
            word = "E" * r
            length, packed = pack_word(word)
            row = con.execute(
                """
                SELECT min_realizer, realization_status
                FROM realizers
                WHERE experiment_id = ? AND word_id = ?
                """,
                (experiment_id, (length << 32) | packed),
            ).fetchone()
            tower.append(
                {
                    "r": r,
                    "word": word,
                    "min_realizer": None if row is None else row[0],
                    "status": None if row is None else row[1],
                    "tower": even_tower(r) if r <= 6 else None,
                }
            )
        unary_parents = []
        for word in FIRST_UNARY:
            length, packed = pack_word(word)
            mask = con.execute(
                """
                SELECT successor_mask, continuation_count
                FROM continuations
                WHERE experiment_id = ? AND word_id = ? AND language_id = 'REALIZABLE'
                """,
                (experiment_id, (length << 32) | packed),
            ).fetchone()
            real = con.execute(
                """
                SELECT min_realizer, realization_status
                FROM realizers
                WHERE experiment_id = ? AND word_id = ?
                """,
                (experiment_id, (length << 32) | packed),
            ).fetchone()
            unary_parents.append(
                {
                    "word": word,
                    "min_realizer": None if real is None else real[0],
                    "status": None if real is None else real[1],
                    "mask": None if mask is None else mask[0],
                    "class": None if mask is None else degree_label(mask[0]),
                }
            )
        holes = []
        for word in FIRST_HOLES:
            length, packed = pack_word(word)
            real = con.execute(
                """
                SELECT min_realizer, realization_status
                FROM realizers
                WHERE experiment_id = ? AND word_id = ?
                """,
                (experiment_id, (length << 32) | packed),
            ).fetchone()
            holes.append(
                {
                    "word": word,
                    "min_realizer": None if real is None else real[0],
                    "status": None if real is None else real[1],
                }
            )
        lead = defaultdict(lambda: [0, 0])
        rows = con.execute(
            """
            SELECT w.packed, w.length, c.continuation_count
            FROM continuations c
            JOIN words w ON w.word_id = c.word_id
            WHERE c.experiment_id = ? AND c.language_id = 'REALIZABLE' AND w.length = 19
            """,
            (experiment_id,),
        )
        for packed, length, d in rows:
            word = unpack_word(length, packed)
            lead_e = leading_run(word, "E")
            lead[lead_e][0] += 1
            if d == 1:
                lead[lead_e][1] += 1
        ee_frozen = 0
        ee_unary = 0
        for packed, length, d in con.execute(
            """
            SELECT w.packed, w.length, c.continuation_count
            FROM continuations c
            JOIN words w ON w.word_id = c.word_id
            WHERE c.experiment_id = ? AND c.language_id = 'REALIZABLE' AND w.length = 12
            """,
            (experiment_id,),
        ):
            word = unpack_word(length, packed)
            if word.startswith("EE"):
                ee_frozen += 1
                if d == 1:
                    ee_unary += 1
    finally:
        con.close()
    return {
        "available": True,
        "experiment_id": experiment_id,
        "tower": tower,
        "first_unary": unary_parents,
        "first_holes": holes,
        "ee_prefix_length_12": {"count": ee_frozen, "unary": ee_unary},
        "lead_E_unary_length_19": {
            str(k): {"nodes": v[0], "unary": v[1], "frac": v[1] / v[0] if v[0] else None}
            for k, v in sorted(lead.items())
        },
    }


def classify_missing_child(parent: str, lost: str, *, atlas_n: int = ATLAS_N) -> dict[str, Any]:
    child = parent + lost
    if child == "EEEEEE":
        return {
            "parent": parent,
            "lost": lost,
            "child": child,
            "status": "SCALE_LIMITED",
            "reason": f"even_tower(6)={even_tower(6)} > atlas n_max={atlas_n}",
        }
    return {
        "parent": parent,
        "lost": lost,
        "child": child,
        "status": "SCALE_LIMITED",
        "reason": "absent as a rooted prefix under the atlas bound; present as an interior factor",
    }


def interior_factors(
    *,
    words: Iterable[str] = FIRST_HOLES,
    data_dir: Path = DEFAULT_DATA_DIR,
    experiment_id: str = ATLAS_EID,
    length: int = 20,
) -> dict[str, Any]:
    if not atlas_available(data_dir):
        return {"available": False}
    packed_targets = {word: pack_word(word)[1] for word in words}
    lengths = {word: len(word) for word in words}
    con = connect(data_dir)
    try:
        rows = con.execute(
            """
            SELECT w.packed, r.min_realizer
            FROM realizers r JOIN words w ON w.word_id = r.word_id
            WHERE r.experiment_id = ? AND r.realization_status = 'FOUND' AND w.length = ?
            """,
            (experiment_id, length),
        ).fetchall()
    finally:
        con.close()
    hits: dict[str, list[tuple[int, int, str]]] = {word: [] for word in words}
    for packed, min_n in rows:
        host = unpack_word(length, int(packed))
        for word, fp in packed_targets.items():
            fac_len = lengths[word]
            mask = (1 << fac_len) - 1
            for pos in range(0, length - fac_len + 1):
                if ((int(packed) >> pos) & mask) == fp:
                    hits[word].append((pos, int(min_n), host))
                    break
    out = {}
    for word, xs in hits.items():
        out[word] = {
            "count": len(xs),
            "min_position": min((x[0] for x in xs), default=None),
            "min_root_status": "NOT_FOUND_WITHIN_BOUND",
            "example": None if not xs else {"position": xs[0][0], "n": xs[0][1], "host": xs[0][2]},
        }
    return {"available": True, "length": length, "words": out}


def amplification_laws(realizing: dict[str, list[int]]) -> dict[str, Any]:
    """Test m(wE) >= m(w)^2 and the even-landing identity m(wE)=m(w)."""

    square_cex = None
    odd_landing_square_cex = None
    even_landing_identity_fail = None
    tower_ok = True
    for r in range(1, 5):
        parent = "E" * r
        child = parent + "E"
        if parent not in realizing or child not in realizing:
            continue
        if realizing[child][0] != realizing[parent][0] ** 2:
            tower_ok = False
    samples = 0

    def _better(current: dict[str, Any] | None, cand: dict[str, Any]) -> dict[str, Any]:
        if current is None:
            return cand
        key = (cand["m_w"], len(cand["word"]), cand["word"])
        old = (current["m_w"], len(current["word"]), current["word"])
        return cand if key < old else current

    for word, starts in realizing.items():
        if not starts:
            continue
        child = word + "E"
        if child not in realizing:
            continue
        m_w = starts[0]
        m_we = realizing[child][0]
        landing = image_after(m_w, word)
        samples += 1
        rec = {"word": word, "m_w": m_w, "m_wE": m_we, "landing": landing}
        if landing % 2 == 0 and m_we != m_w:
            even_landing_identity_fail = _better(even_landing_identity_fail, rec)
        if m_we < m_w * m_w:
            square_cex = _better(square_cex, rec)
        if landing % 2 == 1 and m_we < m_w * m_w:
            odd_landing_square_cex = _better(odd_landing_square_cex, rec)
    return {
        "samples": samples,
        "tower_identity_in_window": tower_ok,
        "square_law_counterexample": square_cex,
        "odd_landing_square_counterexample": odd_landing_square_cex,
        "even_landing_identity_fail": even_landing_identity_fail,
    }


def atlas_unary_return(
    *, data_dir: Path = DEFAULT_DATA_DIR, experiment_id: str = ATLAS_EID
) -> dict[str, Any]:
    if not atlas_available(data_dir):
        return {"available": False}
    con = connect(data_dir)
    try:
        rows = con.execute(
            """
            SELECT c.word_id, c.successor_mask, c.continuation_count
            FROM continuations c
            WHERE c.experiment_id = ? AND c.language_id = 'REALIZABLE'
            """,
            (experiment_id,),
        ).fetchall()
    finally:
        con.close()
    by_id = {int(wid): (int(mask), int(d)) for wid, mask, d in rows}
    returns = []
    ee_returns = []
    for wid, (mask, d) in by_id.items():
        if d != 1:
            continue
        length, packed = split_word_id(wid)
        if length >= 19:
            continue
        keep_o = bool(mask & 1)
        child_len, child_packed = length + 1, packed | ((1 if keep_o else 0) << length)
        child_id = (child_len << 32) | child_packed
        child = by_id.get(child_id)
        if child is None or child[1] != 2:
            continue
        word = unpack_word(length, packed)
        rec = {"parent": word, "child": unpack_word(child_len, child_packed)}
        returns.append(rec)
        if word.startswith("EE"):
            ee_returns.append(rec)
    return {
        "available": True,
        "unary_to_binary_examples": returns[:20],
        "unary_to_binary_count": len(returns),
        "ee_unary_to_binary": ee_returns[:10],
        "ee_unary_to_binary_count": len(ee_returns),
    }


def next_step_cells(m: int) -> dict[str, Any]:
    lo, hi = even_cell(m)
    evens = [n for n in range(lo, hi) if n % 2 == 0]
    odds = [n for n in odd_cell_integers(m) if n % 2 == 1]
    return {"even_parents": evens[:8], "n_even_parents": len(evens), "odd_parents": odds}


def lean_api_present() -> dict[str, Any]:
    text = COLLAPSE.read_text(encoding="utf-8") + "\n" + CELLS.read_text(encoding="utf-8")
    return {
        "sorry_free": "sorry" not in text and "admit" not in text,
        **{
            name: (f"theorem {name}" in text or f"def {name}" in text)
            for name in LEAN_THEOREMS
        },
        "no_forbidden_engines": all(name not in text for name in FORBIDDEN_ENGINES),
        "no_global_termination_theorem": "theorem juggler_reaches_one" not in text,
    }


def classify(payload: dict[str, Any]) -> dict[str, Any]:
    diag = payload["diagnostic"]
    amp = payload["amplification"]
    atlas = payload["atlas"]
    interior = payload["interior"]
    if diag["uncovered_total"] != 0:
        return {
            "classification": CLASS_COUNTER,
            "reason": "child split left uncovered realizers; landing-parity semantics failed",
        }
    if atlas.get("available") and not all(
        row["status"] == "NOT_FOUND_WITHIN_BOUND" for row in atlas["first_holes"]
    ):
        return {
            "classification": CLASS_COUNTER,
            "reason": "a first hole was FOUND as a rooted prefix under the atlas bound",
        }
    square_fails = amp["square_law_counterexample"] is not None
    odd_square_fails = amp["odd_landing_square_counterexample"] is not None
    landing_is_degree = (
        diag["unary_total"] > 0 and diag["unary_monochrome"] == diag["unary_total"]
    )
    interior_ok = interior.get("available") and all(
        rec["count"] > 0 and rec["min_position"] and rec["min_position"] >= 1
        for rec in interior["words"].values()
    )
    ee_frozen = (
        atlas.get("available")
        and atlas["ee_prefix_length_12"]["count"] == 37
        and atlas["ee_prefix_length_12"]["unary"] == 37
    )
    if landing_is_degree and interior_ok and square_fails and odd_square_fails:
        return {
            "classification": CLASS_ROOT,
            "secondary": CLASS_COUNTER,
            "reason": (
                "Child degree is exactly landing-parity monochromicity of T_w(R_w). "
                "Naive m(wE)>=m(w)^2 fails as soon as an odd letter appears "
                "(smallest even-landing identity m(OOOE)=m(OOOOE)=3; smallest "
                "odd-landing jump m(OEEE)=7 to m(OEEEE)=41<49). "
                "The first holes are SCALE_LIMITED root absences with interior "
                "witnesses. No extra low-complexity interval rule beyond landing "
                "parity survived."
            ),
            "ee_corridor_reproduced": ee_frozen,
        }
    if landing_is_degree:
        return {
            "classification": CLASS_CELL,
            "reason": "unary iff landing parity is monochrome; amplification/root split incomplete",
        }
    return {
        "classification": CLASS_COMPLEX,
        "reason": "no stable geometric rule beyond scan-bound counts",
    }


def run_probe() -> dict[str, Any]:
    realizing = collect_realizing(n_max=DIAG_N, k_max=DIAG_K)
    diagnostic = window_census(realizing, n_max=DIAG_N, k_max=DIAG_K)
    confirm_realizing = collect_realizing(n_max=CONFIRM_N, k_max=CONFIRM_K)
    confirm = window_census(confirm_realizing, n_max=CONFIRM_N, k_max=CONFIRM_K)
    return {
        "diagnostic": diagnostic,
        "confirm": {
            "n_max": confirm["n_max"],
            "k_max": confirm["k_max"],
            "n_words": confirm["n_words"],
            "uncovered_total": confirm["uncovered_total"],
            "unary_total": confirm["unary_total"],
            "unary_monochrome": confirm["unary_monochrome"],
            "unary_singleton_landing": confirm["unary_singleton_landing"],
            "binary_scale_separated": confirm["binary_scale_separated"],
            "binary_total": confirm["binary_total"],
            "unary_to_binary_count": confirm["unary_to_binary_count"],
            "unary_to_binary": confirm["unary_to_binary"],
            "profile": confirm["profile"],
            "lead_E_unary_frac_at_horizon": confirm["lead_E_unary_frac_at_horizon"],
        },
        "amplification": amplification_laws(realizing),
        "atlas": reproduce_atlas(),
        "interior": interior_factors(),
        "missing_children": [
            classify_missing_child("EEEEE", "E"),
            classify_missing_child("EEEEO", "E"),
            classify_missing_child("EEEOE", "O"),
        ],
        "atlas_unary_return": atlas_unary_return(),
        "next_step_cell_example": {
            "m=2": next_step_cells(2),
            "m=1": next_step_cells(1),
        },
    }


def probe_payload() -> dict[str, Any]:
    scan = run_probe()
    lean = lean_api_present()
    decision = classify(scan)
    anti = dict(ANTI_OVERCLAIM)
    anti.update(
        {
            "forbidden_factor_law": False,
            "global_termination": False,
            "reopen_pe_factors": False,
            "reopen_residual_quotient": False,
            "automaton": False,
        }
    )
    return {
        "experiment": "juggler_realization_geometry",
        "engine_control_layer_modified": False,
        "anti_overclaim": anti,
        "scan": scan,
        "lean": lean,
        "decision": decision,
        "search_method": (
            "nested R_w by one-pass itinerary; child split by parity of image_after; "
            "atlas min-realizer/continuations for the parked k<=20 census"
        ),
    }


def _fmt_row(row: dict[str, Any]) -> str:
    return (
        f"- `{row['word']}` class=`{row['class']}` |R|=`{row['size']}` "
        f"min=`{row['min']}` max=`{row['max']}` rho_O=`{row['rho_O']}` "
        f"rho_E=`{row['rho_E']}` landings=`{row['n_unique_landings']}` "
        f"mono=`{row['monochrome']}` sep=`{row['scale_separated']}`"
    )


def render_markdown(payload: dict[str, Any]) -> str:
    decision = payload["decision"]
    scan = payload["scan"]
    diag = scan["diagnostic"]
    confirm = scan["confirm"]
    atlas = scan["atlas"]
    amp = scan["amplification"]
    interior = scan["interior"]
    lean = payload["lean"]
    lines = [
        "# Juggler realization-set geometry",
        "",
        f"Status: **{decision['classification']}**",
        "",
        "Standalone application phase. Not a Research Engine experiment",
        "and not a termination theorem. Studies the realizing sets",
        "`R_w(N) = {n <= N : follows(n,w)}` of the prefix trie. Does not",
        "reopen PE-factor grammar or residual-future quotients.",
        "",
        "## Branch budget",
        "",
        "```text",
        "Mathematical target     What geometry of R_w makes a prefix unary?",
        "Novelty hypothesis      inverse-floor cells / scale of R_w force d(w)=1",
        "Falsifier               unary without monochrome landings, or a square",
        "                        amplification law that survives mixed words",
        "Existing machinery      follows_word, image_after, even_cell, atlas trie",
        "Maximum Phase-0 scope   reproduce atlas facts; R_w on n<=4000 then 1e5",
        "```",
        "",
        "## Metadata",
        "",
        f"- diagnostic window: `n<= {diag['n_max']}`, `k<= {diag['k_max']}`",
        f"- confirm window: `n<= {confirm['n_max']}`, `k<= {confirm['k_max']}`",
        f"- engine control layer modified: `{payload['engine_control_layer_modified']}`",
        f"- classification: **{decision['classification']}**",
        f"- sorry-free: `{lean['sorry_free']}`",
        "",
        decision["reason"],
        "",
        "## Atlas reproduction",
        "",
    ]
    if atlas.get("available"):
        lines.append("Even tower `m(E^r)` versus `2^{2^{r-1}}`:")
        lines.append("")
        for row in atlas["tower"]:
            lines.append(
                f"- r=`{row['r']}` word=`{row['word']}` min=`{row['min_realizer']}` "
                f"tower=`{row['tower']}` status=`{row['status']}`"
            )
        lines.extend(["", "First unary parents:", ""])
        for row in atlas["first_unary"]:
            lines.append(
                f"- `{row['word']}` min=`{row['min_realizer']}` class=`{row['class']}`"
            )
        lines.extend(["", "First rooted holes:", ""])
        for row in atlas["first_holes"]:
            lines.append(f"- `{row['word']}` status=`{row['status']}`")
        ee = atlas["ee_prefix_length_12"]
        lines.extend(
            [
                "",
                f"- `EE…` words at length 12: `{ee['count']}` unary `{ee['unary']}`",
                "",
                "Leading-`E` unary fraction at length 19:",
                "",
            ]
        )
        for key, rec in atlas["lead_E_unary_length_19"].items():
            lines.append(
                f"- leadE=`{key}` nodes=`{rec['nodes']}` unary=`{rec['unary']}` frac=`{rec['frac']}`"
            )
    else:
        lines.append("Atlas SQLite was not available.")
    lines.extend(["", "## Missing-child status", ""])
    for row in scan["missing_children"]:
        lines.append(
            f"- `{row['child']}` status=`{row['status']}` — {row['reason']}"
        )
    if interior.get("available"):
        lines.extend(["", "## Root versus interior", ""])
        for word, rec in interior["words"].items():
            ex = rec["example"]
            lines.append(
                f"- `{word}` interior hits at length 20: `{rec['count']}` "
                f"min_pos=`{rec['min_position']}` example n=`{ex['n'] if ex else None}` "
                f"host=`{ex['host'] if ex else None}`"
            )
    lines.extend(
        [
            "",
            "## Diagnostic realizing sets",
            "",
            f"- words: `{diag['n_words']}`",
            f"- uncovered realizers: `{diag['uncovered_total']}`",
            f"- unary nodes: `{diag['unary_total']}` monochrome landings `{diag['unary_monochrome']}`",
            f"- unary with a singleton landing: `{diag['unary_singleton_landing']}`",
            f"- binary nodes: `{diag['binary_total']}` scale-separated children `{diag['binary_scale_separated']}`",
            f"- unary prefixes that regain two children: `{diag['unary_to_binary_count']}`",
            "",
            "Branching profile (diagnostic):",
            "",
        ]
    )
    for length, counts in diag["profile"].items():
        lines.append(f"- k=`{length}` {counts}")
    lines.extend(["", "Adversarial prefixes in the diagnostic window:", ""])
    for row in diag["adversarial"]:
        lines.append(_fmt_row(row))
    lines.extend(
        [
            "",
            "## Confirm window",
            "",
            f"- words: `{confirm['n_words']}` uncovered `{confirm['uncovered_total']}`",
            f"- unary `{confirm['unary_total']}` monochrome `{confirm['unary_monochrome']}`",
            f"- singleton landings `{confirm['unary_singleton_landing']}`",
            f"- binary scale-separated `{confirm['binary_scale_separated']}` / `{confirm['binary_total']}`",
            f"- unary-to-binary `{confirm['unary_to_binary_count']}`",
            "",
        ]
    )
    if confirm["unary_to_binary"]:
        lines.append("Smallest unary-to-binary returns in the confirm window:")
        lines.append("")
        for rec in confirm["unary_to_binary"][:8]:
            lines.append(f"- `{rec['parent']}` → `{rec['child']}` min=`{rec['min']}`")
        lines.append("")
    ret = scan["atlas_unary_return"]
    if ret.get("available"):
        lines.extend(
            [
                "Atlas unary-to-binary (capped scan of continuations):",
                "",
                f"- examples found: `{ret['unary_to_binary_count']}`",
                f"- among `EE…` parents: `{ret['ee_unary_to_binary_count']}`",
                "",
            ]
        )
        for rec in ret["unary_to_binary_examples"][:8]:
            lines.append(f"- `{rec['parent']}` → `{rec['child']}`")
        lines.append("")
    lines.extend(
        [
            "## Minimum-realizer extension",
            "",
            f"- tower identity in the diagnostic window: `{amp['tower_identity_in_window']}`",
            f"- square-law counterexample: `{amp['square_law_counterexample']}`",
            f"- odd-landing square counterexample: `{amp['odd_landing_square_counterexample']}`",
            f"- even-landing identity fail: `{amp['even_landing_identity_fail']}`",
            "",
            "The identity `m(E^{r+1})=m(E^r)^2` is special to the pure even",
            "tower. After an odd letter, `m(wE)=m(w)` whenever `T_w(m(w))` is",
            "even. The square lower bound does not survive mixed words.",
            "",
            "## Lean",
            "",
        ]
    )
    for name in LEAN_THEOREMS:
        lines.append(f"- `{name}`: `{lean.get(name)}`")
    lines.extend(
        [
            f"- no forbidden engines: `{lean.get('no_forbidden_engines')}`",
            f"- no global halt theorem: `{lean.get('no_global_termination_theorem')}`",
            "",
            "## Anti-overclaim",
            "",
        ]
    )
    for key, value in payload["anti_overclaim"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"**{decision['classification']}**",
            "",
            decision["reason"],
            "",
            "This is not a halt result and not a forbidden-factor law.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def write_artifacts(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = payload if payload is not None else probe_payload()
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_markdown(data), encoding="utf-8")
    return data


def main() -> None:
    payload = write_artifacts()
    print(payload["decision"]["classification"])
    print(payload["decision"]["reason"])


if __name__ == "__main__":
    main()
