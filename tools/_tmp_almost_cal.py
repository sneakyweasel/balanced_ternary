"""Time the L=25781 primitives before the science run."""

import time

from research.juggler_sequence.cycle_almost_search import (
    PHASE1_L,
    backward_run_walk,
    distinguished_words,
    follow_word,
    forward_scan,
    word_bundle,
    word_follow_scan,
)
from research.juggler_sequence.cycle_finance import o_min_and_theta


def main() -> None:
    started = time.perf_counter()
    odd, theta = o_min_and_theta(PHASE1_L)
    print("o_min", odd, theta, "t", time.perf_counter() - started)
    started = time.perf_counter()
    words = distinguished_words(PHASE1_L, odd)
    print("words", {k: len(v) for k, v in words.items()}, "t", time.perf_counter() - started)
    started = time.perf_counter()
    bundle = word_bundle(PHASE1_L, odd)
    print(
        "bundle",
        {k: (v.get("two_type"), v.get("n_ooe"), v.get("n_oe")) for k, v in bundle.items() if isinstance(v, dict) and "n_ooe" in v},
        "t",
        time.perf_counter() - started,
    )
    started = time.perf_counter()
    rec = follow_word(1_000_001, words["christoffel"])
    print("follow one", rec["depth"], rec["complete"], "t", time.perf_counter() - started)
    started = time.perf_counter()
    back = backward_run_walk(words["christoffel"], 1_000_001, beam=8)
    print("backward one", back, "t", time.perf_counter() - started)
    started = time.perf_counter()
    follow = word_follow_scan(words["christoffel"], 1_000_001, 1_002_001, stride=34)
    print("follow window", follow, "t", time.perf_counter() - started)
    started = time.perf_counter()
    fwd = forward_scan(2_000_001, 2_020_001, target_l=PHASE1_L, workers=1, chunk=50_000)
    print(
        "forward 10k",
        fwd["n_seen"],
        fwd["max_steps"],
        fwd["hardest"],
        fwd["max_bits"],
        fwd["hist"],
        fwd["elapsed_s"],
    )


if __name__ == "__main__":
    main()
