"""Constructive hug-cylinder nonemptiness probe. Not a halt theorem.

Follow-up to the hug-cylinder realization branch (CLOSE): can
nonemptiness of the extremal hug cylinder C_L be certified at depths
far beyond the forward scan horizon (28 at 2e8), and is the parity
structure of floor(x^{3/2}) inside the budget an all-depth induction
would need?

Two measurements:

1. Backward generator chain. The hug word factors into OE / OOE
   blocks (O-runs <= 2 because 2 log2(3/2) > 1, E-runs = 1). The
   E-preimage of a single valid state y is the full interval
   [y^2, (y+1)^2), so freedom regenerates every <= 3 letters. Lazy
   generators with O-over-E and O-O-E fusions produce explicit
   witnesses n realizing the exact hug L-prefix; every witness is
   re-verified forward by exact arithmetic (word match + above
   anchor).

2. Parity-run census. The only unprovable induction steps are
   parity hits of floor(x^{3/2}) on odd-x windows of length
   ~(2/3)X^{1/4} at scale X - exactly the quadratic-crossing scale
   where the second-order term of x^{3/2} forces an extra integer
   crossing. Measure max constant-parity runs against that budget.

Not a reopen of the mechanical-lift branch (single-cell inverse
lifts for cycles; empty_ooe was death of exact cell-following, not
of the lazy tree) and not a K3 attack. All verdicts are exact
integer arithmetic.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Iterator

from research.juggler_sequence.above_anchor_walk import hug_odds_prefix
from research.juggler_sequence.hug_prefix_realization import hug_letters

try:
    from gmpy2 import iroot as _iroot
    from gmpy2 import isqrt as _isqrt
    from gmpy2 import mpz as _mpz

    HAVE_GMPY2 = True
except ImportError:  # pragma: no cover - gmpy2 is present in the lab env
    HAVE_GMPY2 = False

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "data" / "research" / "juggler" / "hug_cylinder_construction"
JSON_PATH = DATA_DIR / "summary.json"

SCIENCE_DEPTHS = (40, 56, 64)
TEST_DEPTH = 24
SEED = 10_001
NODE_BUDGET = 30_000_000
PARITY_RUN_SCALES = tuple(2**j for j in (20, 24, 28, 32, 36, 40))
PARITY_RUN_WINDOW = 250_000

CLASS_CONSTRUCTED = "HUG_CYLINDER_CONSTRUCTED"
CLASS_OBSTRUCTED = "HUG_CYLINDER_CONSTRUCTION_OBSTRUCTED"

ANTI = {
    "halt_theorem": False,
    "eventual_descent_theorem": False,
    "all_depth_nonemptiness_theorem": False,
    "k3_reopened": False,
    "mechanical_lift_reopened": False,
    "paper_a_modified": False,
    "floating_point_verdict": False,
}


def _sqrt(x: int):
    return _isqrt(x) if HAVE_GMPY2 else math.isqrt(x)


def _cbrt(x: int) -> int:
    if HAVE_GMPY2:
        r, _ = _iroot(_mpz(x), 3)
        return int(r)
    r = round(x ** (1 / 3))
    while r * r * r > x:
        r -= 1
    while (r + 1) ** 3 <= x:
        r += 1
    return r


def _root9(x: int) -> int:
    if HAVE_GMPY2:
        r, _ = _iroot(_mpz(x), 9)
        return int(r)
    r = round(x ** (1 / 9))
    while r**9 > x:
        r -= 1
    while (r + 1) ** 9 <= x:
        r += 1
    return r


def floor_power_int(x: int) -> int:
    return int(_sqrt(x * x * x)) if x % 2 == 1 else int(_sqrt(x))


class Budget:
    """Shared node budget across the generator chain."""

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.used = 0

    def spend(self, k: int = 1) -> bool:
        self.used += k
        return self.used <= self.limit


def _chain(letters: str, budget: Budget) -> list[Iterator[int]]:
    """Lazy suffix-realizer generators gen[k]: values x with the orbit of
    x realizing letters[k:]. Fusions skip through O-letters so that
    every enumeration happens against regenerated interval freedom."""

    depth = len(letters)
    gens: list[Iterator[int] | None] = [None] * (depth + 1)

    def make(k: int) -> Iterator[int]:
        if k == depth:

            def seed_gen() -> Iterator[int]:
                v = SEED
                while budget.spend():
                    yield v
                    v += 1

            return seed_gen()
        letter = letters[k]
        if letter == "E":

            def e_gen() -> Iterator[int]:
                for y in gens[k + 1]:  # type: ignore[union-attr]
                    x = y * y if (y * y) % 2 == 0 else y * y + 1
                    top = (y + 1) * (y + 1)
                    while x < top:
                        if not budget.spend():
                            return
                        yield x
                        x += 2

            return e_gen()
        # letter == "O"
        nxt = letters[k + 1] if k + 1 < depth else None
        if nxt == "E":

            def oe_gen() -> Iterator[int]:
                # anchor z two levels down; x odd with
                # x' = isqrt(x^3) even in [z^2, (z+1)^2), isqrt(x') = z
                for z in gens[k + 2]:  # type: ignore[union-attr]
                    lo = _cbrt(z * z * z * z)
                    hi = _cbrt((z + 1) ** 4) + 2
                    x = lo if lo % 2 == 1 else lo + 1
                    z_sq = z * z
                    z1_sq = (z + 1) * (z + 1)
                    while x < hi:
                        if not budget.spend():
                            return
                        x1 = int(_sqrt(x * x * x))
                        if x1 % 2 == 0 and z_sq <= x1 < z1_sq:
                            yield x
                        x += 2

            return oe_gen()
        if nxt == "O":
            # hug O-runs are <= 2: letters[k+2] must be E (or the end)
            if k + 2 < depth and letters[k + 2] != "E":
                raise AssertionError("hug O-run longer than 2")

            def ooe_gen() -> Iterator[int]:
                # anchor w three levels down; x odd, x' odd, x'' even
                # in [w^2, (w+1)^2)
                for w in gens[k + 3] if k + 3 <= depth else iter(()):  # type: ignore[union-attr]
                    lo = _root9(w**8)
                    hi = _root9((w + 1) ** 8) + 2
                    x = lo if lo % 2 == 1 else lo + 1
                    w_sq = w * w
                    w1_sq = (w + 1) * (w + 1)
                    while x < hi:
                        if not budget.spend():
                            return
                        x1 = int(_sqrt(x * x * x))
                        if x1 % 2 == 1:
                            x2 = int(_sqrt(x1 * x1 * x1))
                            if x2 % 2 == 0 and w_sq <= x2 < w1_sq:
                                yield x
                        x += 2

            def ooe_tail_gen() -> Iterator[int]:
                # word ends ...OO: any odd x with odd image works
                v = SEED if SEED % 2 == 1 else SEED + 1
                while budget.spend():
                    if int(_sqrt(v * v * v)) % 2 == 1:
                        yield v
                    v += 2

            return ooe_gen() if k + 3 <= depth else ooe_tail_gen()

        # letter O at the end of the word: any odd value
        def o_tail_gen() -> Iterator[int]:
            v = SEED if SEED % 2 == 1 else SEED + 1
            while budget.spend():
                yield v
                v += 2

        return o_tail_gen()

    for k in range(depth, -1, -1):
        gens[k] = make(k)
    return gens  # type: ignore[return-value]


def verify_witness(n: int, letters: str) -> bool:
    """Exact forward check: the orbit of n realizes `letters` and stays
    above the anchor throughout."""

    x = n
    for ch in letters:
        if (ch == "O") != (x % 2 == 1):
            return False
        x = floor_power_int(x)
        if x < n:
            return False
    return True


def construct_witness(depth: int, node_budget: int = NODE_BUDGET) -> dict[str, Any]:
    """First witness of the hug depth-L cylinder from the generator
    chain, with exact forward verification."""

    letters = hug_letters(depth)
    budget = Budget(node_budget)
    gens = _chain(letters, budget)
    try:
        witness = next(gens[0])
    except StopIteration:
        return {
            "depth": depth,
            "constructed": False,
            "nodes_used": budget.used,
        }
    ok = verify_witness(witness, letters)
    return {
        "depth": depth,
        "constructed": True,
        "witness": witness,
        "witness_bits": witness.bit_length(),
        "log2_witness": round(math.log2(witness), 2),
        "forward_verified": ok,
        "nodes_used": budget.used,
    }


def parity_run_census(
    scales: tuple[int, ...] = PARITY_RUN_SCALES, window: int = PARITY_RUN_WINDOW
) -> list[dict[str, Any]]:
    """Max constant-parity run of floor(x^{3/2}) over consecutive odd x
    near each scale X, against the induction budget (2/3) X^{1/4}."""

    rows = []
    for scale in scales:
        x = scale + 1 if scale % 2 == 0 else scale
        run = 0
        max_run = 0
        prev: int | None = None
        for _ in range(window):
            p = int(_sqrt(x * x * x)) % 2
            if p == prev:
                run += 1
            else:
                run = 1
                prev = p
            if run > max_run:
                max_run = run
            x += 2
        budget_len = (2.0 / 3.0) * scale**0.25
        rows.append(
            {
                "scale_log2": int(math.log2(scale)),
                "window": window,
                "max_parity_run": max_run,
                "budget": round(budget_len, 1),
                "run_over_budget": round(max_run / budget_len, 4),
            }
        )
    return rows


def build_summary(depths: tuple[int, ...] = SCIENCE_DEPTHS) -> dict[str, Any]:
    constructions = [construct_witness(depth) for depth in depths]
    runs = parity_run_census()
    all_built = all(
        c["constructed"] and c["forward_verified"] for c in constructions
    )
    runs_in_budget = all(r["run_over_budget"] < 1.0 for r in runs)
    summary: dict[str, Any] = {
        "experiment": "juggler_hug_cylinder_construction",
        "anti_overclaim": ANTI,
        "constructions": constructions,
        "parity_runs": runs,
        "classification": (
            CLASS_CONSTRUCTED if all_built and runs_in_budget else CLASS_OBSTRUCTED
        ),
        "notes": {
            "block_structure": "hug = OE/OOE blocks; O-runs <= 2 since 2 log2(3/2) > 1; E-preimage of one state is a full interval [y^2,(y+1)^2)",
            "budget": "an all-depth induction needs parity hits of floor(x^{3/2}) on odd-x windows of length (2/3)X^{1/4} - the quadratic-crossing scale",
            "witnesses": "every constructed witness is re-verified forward: exact word match and above-anchor",
        },
    }
    return summary


def main(depths: tuple[int, ...] = SCIENCE_DEPTHS) -> dict[str, Any]:
    summary = build_summary(depths)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "classification": summary["classification"],
                "constructions": [
                    {
                        k: v
                        for k, v in c.items()
                        if k not in ("witness",) or c["depth"] <= 40
                    }
                    for c in summary["constructions"]
                ],
                "parity_runs": summary["parity_runs"],
            },
            indent=2,
            default=str,
        )
    )
    return summary


if __name__ == "__main__":
    main()
