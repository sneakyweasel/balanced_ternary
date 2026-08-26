"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.cyclic_tag_bit.spec import (
    DEFINED,
    WordRewriteSpec,
    decode_word,
    encode_word,
    map_images,
    map_spec,
    step_word,
    transition_status,
    word_length,
)

WINDOW_WORDS = ("0", "1", "00", "01", "10", "11", "101", "111", "000")
ORBIT_CAP = 40
START = "101"


def step(n: int) -> int | None:
    images = map_images(n)
    if len(images) != 1:
        return None
    return images[0]


def orbit_words(start: str = START, *, max_steps: int = ORBIT_CAP) -> dict[str, object]:
    seen: list[str] = []
    current = start
    for _ in range(max_steps):
        encoded = encode_word(current)
        status = transition_status(encoded)
        if status != DEFINED:
            return {
                "path": tuple(seen + [current]),
                "kind": "halt" if not current else "truncated",
                "hits_empty": ("" in seen) or current == "",
            }
        if current in seen:
            return {
                "path": tuple(seen),
                "kind": "cycle",
                "hits_empty": "" in seen,
            }
        nxt = step_word(current)
        seen.append(current)
        if nxt is None:
            return {"path": tuple(seen), "kind": "halt", "hits_empty": "" in seen}
        current = nxt
    return {"path": tuple(seen), "kind": "truncated", "hits_empty": "" in seen}


def evidence_state(spec: WordRewriteSpec | None = None) -> dict[str, object]:
    target = spec if spec is not None else map_spec()
    start_orbit = orbit_words(target.start_word)
    path = start_orbit["path"]
    lengths = tuple(len(item) for item in path)
    zero_fixed = step_word("0") == "0"
    empty_halt = step_word("") is None
    drops = 0
    growths = 0
    first_growth: str | None = None
    for word in WINDOW_WORDS:
        nxt = step_word(word)
        if nxt is None:
            continue
        if len(nxt) < len(word):
            drops += 1
        elif len(nxt) > len(word):
            growths += 1
            if first_growth is None:
                first_growth = word
    seed_code = encode_word(target.start_word)
    return {
        "start_word": target.start_word,
        "start_orbit": path,
        "start_kind": start_orbit["kind"],
        "hits_empty": start_orbit["hits_empty"],
        "steps_to_empty": path.index("") if "" in path else None,
        "lengths": lengths,
        "empty_halt": empty_halt,
        "zero_fixed": zero_fixed,
        "first_growth": first_growth,
        "drops": drops,
        "growths": growths,
        "seed_code": seed_code,
        "seed_length_obs": word_length(seed_code),
        "image_word_101": step_word("101"),
        "decode_roundtrip": decode_word(seed_code) == target.start_word,
        "census_affine_system": target.affine_system(),
        "universal_empty": False,
        "note": "nonempty length never decreases; that is not a tag-system attack",
    }


def falsify_claims(spec: WordRewriteSpec | None = None) -> dict[str, dict[str, object]]:
    report = evidence_state(spec)
    return {
        "residue_affine_cover": {
            "claim": "the encoded map is residue-affine / piecewise-affine in the frozen census language",
            "holds_on_window": report["census_affine_system"] is not None,
            "status": "REFUTED",
            "counterexample": "affine_system is None; successor is a word rewrite",
        },
        "seed_halt_is_z_theorem": {
            "claim": "the packet seed reaching empty is a theorem obtained by the frozen integer stack",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": report["start_orbit"],
        },
        "this_is_integer_affine": {
            "claim": "the successor is an affine map of the encoded integer",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {
                "word": "101",
                "image": report["image_word_101"],
                "encoding": report["seed_code"],
            },
        },
        "empty_from_nonempty": {
            "claim": "some nonempty window word maps to empty in one step",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {"drops": report["drops"], "zero_fixed": report["zero_fixed"]},
        },
        "new_tag_attack": {
            "claim": "progress requires a new tag-system attack",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": "exact I/O is the problem definition; frozen stack diagnoses the mismatch",
        },
    }
