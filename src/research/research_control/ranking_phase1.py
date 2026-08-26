"""Load frozen v2.3 transitions for the ranking Phase-1 enriched falsifier."""

from __future__ import annotations

import json
from pathlib import Path

from bt.representation import encode
from bt.sequences import bt_length
from research.home_prime_49.discovery import WINDOW as HOME_WINDOW
from research.home_prime_49.discovery import is_fixed_prime
from research.home_prime_49.discovery import orbit as home_orbit
from research.home_prime_49.discovery import step as home_step
from research.home_prime_49.spec import factor_trial
from research.juggler_sequence.discovery import WINDOW as JUGGLER_WINDOW
from research.juggler_sequence.discovery import orbit as juggler_orbit
from research.juggler_sequence.discovery import step as juggler_step
from research.reverse_and_add_base3.discovery import WINDOW as REVERSE_WINDOW
from research.reverse_and_add_base3.discovery import orbit as reverse_orbit
from research.reverse_and_add_base3.discovery import step as reverse_step
from research_engine.control.ranking import ObservedTransition, integer_features
from research_engine.control.ranking_phase1 import (
    Phase1TargetReport,
    decide_phase1,
    falsify_home_piecewise,
    falsify_juggler_composed,
    falsify_reverse_gap,
    phase1_payload,
    render_phase1_markdown,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "ranking_phase1.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "ranking_phase1.md"


def reverse_gap(n: int) -> int:
    """L1 discrepancy between the canonical MSD word and its reverse.

    Uses existing ``encode``. Canonical words have no leading zeros except
    ``n = 0``. Negatives are handled by ``encode``. This is not a palindrome
    language engine.
    """

    msd = encode(n).digits_msd
    rev = tuple(reversed(msd))
    return sum(abs(left - right) for left, right in zip(msd, rev))


def _juggler_features(n: int):
    return integer_features(n, digit=abs(n).bit_length() or 1, residue=n % 2)


def _unique_juggler_seeds() -> tuple[int, ...]:
    seeds = list(JUGGLER_WINDOW)
    path = juggler_orbit(13)["path"]
    for item in path:
        seeds.append(int(item))
    seen: set[int] = set()
    ordered: list[int] = []
    for seed in seeds:
        if seed in seen:
            continue
        seen.add(seed)
        ordered.append(seed)
    return tuple(ordered)


def juggler_composed_transitions() -> tuple[tuple[ObservedTransition, ...], int]:
    items: list[ObservedTransition] = []
    odd_odd = 0
    seen: set[tuple[int, int]] = set()
    for seed in _unique_juggler_seeds():
        if seed % 2 == 0:
            continue
        mid = juggler_step(seed)
        if mid is None:
            continue
        if mid % 2 == 1:
            odd_odd += 1
            continue
        image = juggler_step(mid)
        if image is None:
            continue
        key = (seed, image)
        if key in seen:
            continue
        seen.add(key)
        items.append(
            ObservedTransition(
                source=seed,
                image=image,
                source_features=_juggler_features(seed),
                image_features=_juggler_features(image),
                note="juggler odd-even composed k=2",
            )
        )
    return tuple(items), odd_odd


def reverse_transitions() -> tuple[ObservedTransition, ...]:
    pairs: list[tuple[int, int]] = []
    for seed in REVERSE_WINDOW:
        image = reverse_step(seed)
        if image is None:
            continue
        pairs.append((seed, image))
    path = reverse_orbit(196)["path"]
    for src, dst in zip(path, path[1:]):
        pairs.append((int(src), int(dst)))
    seen: set[tuple[int, int]] = set()
    items: list[ObservedTransition] = []
    for source, image in pairs:
        if (source, image) in seen:
            continue
        seen.add((source, image))
        items.append(
            ObservedTransition(
                source=source,
                image=image,
                source_features=integer_features(
                    source,
                    digit=bt_length(source),
                    residue=source % 2,
                    extra={"reverse_gap": reverse_gap(source)},
                ),
                image_features=integer_features(
                    image,
                    digit=bt_length(image),
                    residue=image % 2,
                    extra={"reverse_gap": reverse_gap(image)},
                ),
                note="reverse digit_reversal",
            )
        )
    return tuple(items)


def _home_features(n: int):
    factors = factor_trial(n) or {}
    omega = len(factors)
    omega_total = sum(factors.values())
    digit = len(str(abs(n))) if n != 0 else 1
    return integer_features(
        n,
        digit=digit,
        residue=omega,
        extra={"factor_count": omega_total, "omega": omega},
    )


def _unique_home_seeds() -> tuple[int, ...]:
    seeds = list(HOME_WINDOW)
    for start in (49, 4, 10):
        for item in home_orbit(start, max_steps=8)["path"]:
            seeds.append(int(item))
    seen: set[int] = set()
    ordered: list[int] = []
    for seed in seeds:
        if seed in seen:
            continue
        seen.add(seed)
        ordered.append(seed)
    return tuple(ordered)


def home_piecewise_transitions() -> tuple[tuple[ObservedTransition, ...], tuple[ObservedTransition, ...]]:
    composite: list[ObservedTransition] = []
    terminal: list[ObservedTransition] = []
    seen: set[tuple[int, int]] = set()
    for seed in _unique_home_seeds():
        image = home_step(seed)
        if image is None or seed == image:
            continue
        if is_fixed_prime(seed):
            continue
        key = (seed, image)
        if key in seen:
            continue
        seen.add(key)
        item = ObservedTransition(
            source=seed,
            image=image,
            source_features=_home_features(seed),
            image_features=_home_features(image),
            note="home factor concat",
        )
        if is_fixed_prime(image):
            terminal.append(item)
        else:
            composite.append(item)
    return tuple(composite), tuple(terminal)


def run_phase1() -> tuple[Phase1TargetReport, ...]:
    composed, odd_odd = juggler_composed_transitions()
    juggler = falsify_juggler_composed(composed, exceptional=(1,), odd_odd_count=odd_odd)
    reverse = falsify_reverse_gap(reverse_transitions(), exceptional=(0,))
    composite, terminal = home_piecewise_transitions()
    home = falsify_home_piecewise(composite, terminal_entries=terminal)
    return (juggler, reverse, home)


def write_artifacts(reports: tuple[Phase1TargetReport, ...] | None = None) -> dict:
    items = reports if reports is not None else run_phase1()
    decision, reason = decide_phase1(items)
    payload = phase1_payload(items, decision=decision, decision_reason=reason)
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    DOC_PATH.write_text(render_phase1_markdown(payload), encoding="utf-8")
    return payload


if __name__ == "__main__":
    result = write_artifacts()
    print(result["ranking_phase1_decision"], result["decision_reason"])
    for row in result["target_matrix"]:
        print(row["target"], row["classification"], "survivors", row["survivors"], row["first_failure"])
