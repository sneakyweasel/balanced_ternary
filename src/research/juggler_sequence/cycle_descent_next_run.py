"""Next-run type after a cheap-band descent.

Not a halt theorem, not a leftover-word census, not a floor raise,
and not a reopen of return-cost coupling or ordered pairs.

Section 5 needs a coupling that forbids o-e independent n-valleys.
The remaining untested local slogan is: a descending even run onto
the cheap band [n, 19n] cannot start a=2, so N_cheap is O(1).
This probe asks that, and only that.

Dossier: docs/problems/juggler_cycle_descent_next_run.md.
"""

from __future__ import annotations

import json
from collections import Counter
from math import isqrt
from typing import Any

from research.juggler_sequence.block_map_q import a_of, block_map
from research.juggler_sequence.cycle_finance import (
    DATA_DIR,
    PUBLISHED_FLOOR,
    sha256_int_list,
)
from research.juggler_sequence.cycle_ordered_excursion import (
    excursion_map,
    first_a2,
    next_run,
)

CHEAP_LIFT = 19
START = PUBLISHED_FLOOR + 1
NEAR_WINDOW = 20_000
SPOTLIGHT_6187 = 6187
DESCENT_DIR = DATA_DIR / "descent_next_run"


def cheap_band_hi(n: int, lift: int = CHEAP_LIFT) -> int:
    return lift * n


def in_cheap_band(p: int, n: int, lift: int = CHEAP_LIFT) -> bool:
    return n <= p <= cheap_band_hi(n, lift)


def one_even_peak(p: int) -> int:
    """Minimal even predecessor of odd p: the left edge of the even cell."""

    return p * p


def even_iter_to_odd(peak: int, n: int) -> tuple[int, int] | None:
    """Even-iterate from an even peak until an odd landing, or drop below n."""

    if peak < 2 or peak % 2 == 1:
        return None
    steps = 0
    current = peak
    while current % 2 == 0:
        nxt = isqrt(current)
        steps += 1
        if nxt < n:
            return None
        current = nxt
    return current, steps


def one_even_witness(n: int = START) -> dict[str, Any] | None:
    """First a=2 start in the cheap band, as a one-even descent."""

    seed = first_a2(n)
    if seed is None or not in_cheap_band(seed, n):
        return None
    peak = one_even_peak(seed)
    return {
        "n": n,
        "p": seed,
        "a": 2,
        "peak": peak,
        "peak_ge_n2": peak >= n * n,
        "in_band": True,
    }


def post_ooe_census(
    n: int,
    window: int = NEAR_WINDOW,
    *,
    lift: int = CHEAP_LIFT,
) -> dict[str, Any]:
    """a=2 starts on [n, n+window): OOE descent landings in the cheap band."""

    hi = n + window
    a_counts: Counter[int] = Counter()
    n_a2 = 0
    n_in_band = 0
    n_a2_after = 0
    n_even_land = 0
    witnesses: list[dict[str, int]] = []
    current = n if n % 2 == 1 else n + 1
    while current < hi:
        if next_run(current) == 2:
            n_a2 += 1
            rec = excursion_map(current, 2)
            if rec is None:
                current += 2
                continue
            peak, landing = rec
            if landing % 2 == 0:
                n_even_land += 1
                stepped = even_iter_to_odd(landing, n)
                if stepped is None:
                    current += 2
                    continue
                landing, _extra = stepped
            if landing % 2 == 1 and in_cheap_band(landing, n, lift):
                n_in_band += 1
                run = a_of(landing)
                a_counts[run] += 1
                if run == 2:
                    n_a2_after += 1
                    if len(witnesses) < 5:
                        witnesses.append(
                            {
                                "v": current,
                                "peak": peak,
                                "p": landing,
                                "a": run,
                            }
                        )
        current += 2
    return {
        "n": n,
        "lo": n,
        "hi": hi,
        "band_hi": cheap_band_hi(n, lift),
        "a2_starts": n_a2,
        "landings_in_band": n_in_band,
        "a2_after_descent": n_a2_after,
        "even_first_landing": n_even_land,
        "a_counts": {str(k): v for k, v in sorted(a_counts.items())},
        "witnesses": witnesses,
        "slogan_false": n_a2_after > 0,
    }


def spotlight_6187() -> dict[str, Any]:
    """Named open-orbit Q-descent 11189 → 1087 → 189 on the 6187 path.

    This is not a CycleMin witness: both landings sit below 6187.
    It is recorded only so the ordered-excursion descent is not
    mistaken for a cheap-band a=2 return.
    """

    start = SPOTLIGHT_6187
    x = 11189
    mid = block_map(x)
    end = block_map(mid)
    return {
        "start": start,
        "x": x,
        "mid": mid,
        "end": end,
        "a_x": a_of(x),
        "a_mid": a_of(mid) if mid % 2 == 1 else "even",
        "a_end": a_of(end) if end % 2 == 1 else "even",
        "matches_named": mid == 1087 and end == 189,
        "cyclemin_legal": min(x, mid, end) >= start,
        "end_in_cheap_band": in_cheap_band(end, start),
        "is_falsifier": False,
    }


def build_summary(
    *,
    n: int = START,
    window: int = NEAR_WINDOW,
) -> dict[str, Any]:
    one = one_even_witness(n)
    post = post_ooe_census(n, window)
    drop = spotlight_6187()
    first_pair = post["witnesses"][0] if post["witnesses"] else None
    return {
        "n": n,
        "lift": CHEAP_LIFT,
        "band_hi": cheap_band_hi(n),
        "window": window,
        "one_even": one,
        "post_ooe": post,
        "spotlight_6187": drop,
        "one_even_a2": one is not None,
        "post_ooe_a2": post["slogan_false"],
        "slogan_false": bool(one is not None or post["slogan_false"]),
        "first_post_ooe_pair": first_pair,
        "sha256_a2_starts": sha256_int_list(
            [row["v"] for row in post["witnesses"]]
        ),
    }


def write_summary(path=DESCENT_DIR / "summary.json", **kwargs: Any) -> dict[str, Any]:
    payload = build_summary(**kwargs)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    out = write_summary()
    print(json.dumps(
        {
            "slogan_false": out["slogan_false"],
            "one_even": out["one_even"],
            "a2_after_descent": out["post_ooe"]["a2_after_descent"],
            "a_counts": out["post_ooe"]["a_counts"],
            "first_pair": out["first_post_ooe_pair"],
            "spotlight_6187": out["spotlight_6187"],
        },
        indent=2,
    ))
