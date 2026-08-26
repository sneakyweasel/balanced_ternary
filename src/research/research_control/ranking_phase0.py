"""Load existing v2.3 campaign transitions for the ranking Phase-0 falsifier."""

from __future__ import annotations

import json
from pathlib import Path

from bt.sequences import bt_length
from research.cyclic_tag_bit.discovery import WINDOW_WORDS as TAG_WINDOW
from research.cyclic_tag_bit.discovery import orbit_words, step_word
from research.cyclic_tag_bit.spec import encode_word
from research.home_prime_49.discovery import WINDOW as HOME_WINDOW
from research.home_prime_49.discovery import orbit as home_orbit
from research.home_prime_49.discovery import step as home_step
from research.juggler_sequence.discovery import WINDOW as JUGGLER_WINDOW
from research.juggler_sequence.discovery import orbit as juggler_orbit
from research.juggler_sequence.discovery import step as juggler_step
from research.reverse_and_add_base3.discovery import WINDOW as REVERSE_WINDOW
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.discovery import step as reverse_step
from research_engine.control.ranking import (
    NEGATIVE_CONTROL,
    ObservedTransition,
    TargetRankingReport,
    decide_phase0,
    falsify_target,
    integer_features,
    phase0_payload,
    render_phase0_markdown,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "ranking_phase0.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "ranking_phase0.md"


def _unique_pairs(pairs: list[tuple[int, int, str]]) -> tuple[ObservedTransition, ...]:
    seen: set[tuple[int, int]] = set()
    items: list[ObservedTransition] = []
    for source, image, note in pairs:
        key = (source, image)
        if key in seen:
            continue
        seen.add(key)
        items.append(
            ObservedTransition(
                source=source,
                image=image,
                source_features=_features_for(note, source),
                image_features=_features_for(note, image),
                note=note,
            )
        )
    return tuple(items)


def _features_for(kind: str, n: int):
    if kind.startswith("juggler"):
        return integer_features(n, digit=abs(n).bit_length() or 1, residue=n % 2)
    if kind.startswith("reverse"):
        return integer_features(n, digit=bt_length(n), residue=n % 2)
    digit = len(str(abs(n))) if n != 0 else 1
    return integer_features(n, digit=digit, residue=n % 2)


def juggler_transitions() -> tuple[ObservedTransition, ...]:
    pairs: list[tuple[int, int, str]] = []
    for seed in JUGGLER_WINDOW:
        image = juggler_step(seed)
        if image is None:
            continue
        note = "juggler odd floor-power" if seed % 2 else "juggler even square-root"
        pairs.append((seed, image, note))
    path = juggler_orbit(13)["path"]
    for src, dst in zip(path, path[1:]):
        note = "juggler odd floor-power" if src % 2 else "juggler even square-root"
        pairs.append((int(src), int(dst), note))
    return _unique_pairs(pairs)


def reverse_transitions() -> tuple[ObservedTransition, ...]:
    pairs: list[tuple[int, int, str]] = []
    for seed in REVERSE_WINDOW:
        image = reverse_step(seed)
        if image is None:
            continue
        pairs.append((seed, image, "reverse digit_reversal"))
    path = reverse_orbit(196)["path"]
    for src, dst in zip(path, path[1:]):
        pairs.append((int(src), int(dst), "reverse digit_reversal"))
    return _unique_pairs(pairs)


def home_transitions() -> tuple[ObservedTransition, ...]:
    pairs: list[tuple[int, int, str]] = []
    for seed in HOME_WINDOW:
        image = home_step(seed)
        if image is None:
            continue
        pairs.append((seed, image, "home factor concat"))
    for start in (49, 4, 10):
        path = home_orbit(start, max_steps=8)["path"]
        for src, dst in zip(path, path[1:]):
            pairs.append((int(src), int(dst), "home factor concat"))
    return _unique_pairs(pairs)


def _tag_items() -> tuple[ObservedTransition, ...]:
    items: list[ObservedTransition] = []
    seen: set[tuple[int, int]] = set()
    for word in TAG_WINDOW:
        nxt = step_word(word)
        if nxt is None:
            continue
        src_n = encode_word(word)
        dst_n = encode_word(nxt)
        if (src_n, dst_n) in seen:
            continue
        seen.add((src_n, dst_n))
        items.append(
            ObservedTransition(
                source=src_n,
                image=dst_n,
                source_features=integer_features(src_n, digit=len(word), residue=int(word[0])),
                image_features=integer_features(
                    dst_n, digit=len(nxt), residue=int(nxt[0]) if nxt else 0
                ),
                note="rewrite length",
            )
        )
    path = orbit_words("101")["path"]
    for src, dst in zip(path, path[1:]):
        src_word = str(src)
        dst_word = str(dst)
        src_n = encode_word(src_word)
        dst_n = encode_word(dst_word)
        if (src_n, dst_n) in seen:
            continue
        seen.add((src_n, dst_n))
        items.append(
            ObservedTransition(
                source=src_n,
                image=dst_n,
                source_features=integer_features(
                    src_n, digit=len(src_word), residue=int(src_word[0])
                ),
                image_features=integer_features(
                    dst_n, digit=len(dst_word), residue=int(dst_word[0]) if dst_word else 0
                ),
                note="rewrite length",
            )
        )
    return tuple(items)


def run_phase0() -> tuple[TargetRankingReport, ...]:
    juggler = falsify_target(
        "juggler_sequence",
        juggler_transitions(),
        available_features=("log_bit=bit_length(1+|x|)", "digit=bit_length(|x|)", "residue=n mod 2"),
        exceptional=(1,),
        notes=("E={1} is the observed fixed point; T(x)=x already excludes it.",),
    )
    reverse = falsify_target(
        "reverse_and_add_base3",
        reverse_transitions(),
        available_features=("log_bit=bit_length(1+|x|)", "digit=bt_length", "residue=n mod 2"),
        exceptional=(0,),
        notes=("E={0} is the reverse-fixed halt; T(0)=0.",),
    )
    home = falsify_target(
        "home_prime_49",
        home_transitions(),
        available_features=("log_bit=bit_length(1+|x|)", "digit=decimal_length", "residue=n mod 2"),
        exceptional=(),
        notes=("Fixed primes already excluded by T(x)!=x; no extra exceptional states.",),
    )
    tag = falsify_target(
        NEGATIVE_CONTROL,
        _tag_items(),
        available_features=(
            "log_bit=bit_length(1+|encoding|)",
            "digit=word_length",
            "residue=leading bit",
        ),
        exceptional=(encode_word("0"),),
        is_negative_control=True,
        notes=("Negative control: |T(w)| >= |w| whenever a successor exists.",),
    )
    return (juggler, reverse, home, tag)


def write_artifacts(reports: tuple[TargetRankingReport, ...] | None = None) -> dict:
    items = reports if reports is not None else run_phase0()
    decision, reason = decide_phase0(items)
    payload = phase0_payload(items, decision=decision, decision_reason=reason)
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase0_markdown(payload), encoding="utf-8")
    return payload


def load_payload() -> dict:
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


if __name__ == "__main__":
    result = write_artifacts()
    print(result["decision"], result["decision_reason"])
    for row in result["target_matrix"]:
        print(row["target"], row["classification"], row["best_result"])
