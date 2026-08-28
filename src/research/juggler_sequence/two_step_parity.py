"""Multi-step itinerary-parity census on odd Juggler starts.

Phase-0 falsifier for the two-step parity discrepancy branch. Exact
integer counting only: does the joint parity word of the first four
itinerary letters on odd starts converge to the product densities,
and with what empirical discrepancy exponent?

Not a Research Engine control-layer experiment. Not a frequency
theorem, not a predictive-state claim (theta bins and residue states
stay REFUTED/CLOSE), and not a termination theorem. The census decides
only whether the depth-2 analytic lemma is worth attempting.
"""

from __future__ import annotations

import json
from math import isqrt, log
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
JSON_PATH = REPO_ROOT / "docs" / "research" / "juggler_two_step_parity.json"
DOC_PATH = REPO_ROOT / "docs" / "research" / "juggler_two_step_parity.md"

N_MAX = 10_000_000
DEPTH = 4
COARSE_GRID = (
    10_000,
    100_000,
    1_000_000,
    *(1 << k for k in range(14, 24)),
    N_MAX,
)
ENVELOPE_RATIO = 1.06

WORDS4 = tuple(
    "O" + "".join(w)
    for w in (
        (a, b, c)
        for a in "EO"
        for b in "EO"
        for c in "EO"
    )
)

# The only length-4 contracting continuation of an odd-to-odd start:
# 3^2 < 2^4 forces image^16 <= n^9, hence a four-step certificate.
CONTRACTING_TARGET = "OOEE"

ANTI_OVERCLAIM = {
    "global_termination": False,
    "parity_frequency_theorem": False,
    "predictive_state_claim": False,
    "reopen_landing_theta": False,
    "reopen_2adic_bridge": False,
    "depth2_analytic_lemma_proved": False,
}


def juggler_step(x: int) -> int:
    if x % 2 == 1:
        return isqrt(x * x * x)
    return isqrt(x)


# --- Phase 1: exact validation of the linearization and gap structure ---

SCALE = 10**30


def _sqrt_scaled(x: int, scale: int = SCALE) -> int:
    """floor(sqrt(x) * scale) in exact integer arithmetic."""
    return isqrt(x * scale * scale)


def _quartic_scaled(x: int, scale: int = SCALE) -> int:
    """floor(x^{1/4} * scale) in exact integer arithmetic."""
    return isqrt(isqrt(x * scale**4))


def identity_error_scaled(n: int, scale: int = SCALE) -> tuple[int, int]:
    """(E(n)*scale, bound*scale) for the exact linearization at odd n.

    Lemma A: m^{3/2} = (3/2) m n^{3/4} - (1/2) n^{9/4} + E(n) with
    0 <= E(n) <= (3/8) (n^{3/2}-1)^{-1/2} <= (1/2) n^{-3/4}, where
    m = floor(n^{3/2}). Returned values carry integer-rounding slack of
    a few units times m, negligible at this scale.
    """
    if n < 3 or n % 2 == 0:
        raise ValueError("odd n >= 3 required")
    m = isqrt(n**3)
    m32 = _sqrt_scaled(m**3, scale)
    n94 = _quartic_scaled(n**9, scale)
    n34 = _quartic_scaled(n**3, scale)
    err = m32 + n94 // 2 - (3 * m * n34) // 2
    bound = (scale * scale) // (2 * n34)
    return err, bound


def identity_scan(samples: tuple[int, ...]) -> dict[str, Any]:
    """Check 0 <= E(n) <= (1/2) n^{-3/4} on the given odd samples."""
    slack_units = 8
    worst_ratio = 0.0
    for n in samples:
        err, bound = identity_error_scaled(n)
        m = isqrt(n**3)
        slack = slack_units * max(m, 1)
        if err < -slack or err > bound + slack:
            return {"holds": False, "witness": n}
        if bound > 0:
            worst_ratio = max(worst_ratio, err / bound)
    return {"holds": True, "count": len(samples), "worst_ratio": round(worst_ratio, 6)}


def gap_decomposition_check(start: int, count: int, h: int) -> dict[str, Any]:
    """Verify g(n) = floor(delta) + kappa on `count` consecutive odd n.

    g(n) = m(n+2h) - m(n), delta(n) = (n+2h)^{3/2} - n^{3/2}, and
    kappa = [ {n^{3/2}} >= 1 - {delta(n)} ]. Exact scaled integers;
    samples within a tiny window of a cell boundary are skipped and
    counted separately.
    """
    scale = SCALE
    tol = 10
    matches = skipped = 0
    for i in range(count):
        n = start + 2 * i
        m0 = isqrt(n**3)
        m1 = isqrt((n + 2 * h) ** 3)
        g = m1 - m0
        s0 = _sqrt_scaled(n**3, scale)
        s1 = _sqrt_scaled((n + 2 * h) ** 3, scale)
        delta_scaled = s1 - s0
        floor_delta = delta_scaled // scale
        frac_delta = delta_scaled % scale
        frac_n = s0 - m0 * scale
        threshold = scale - frac_delta
        if abs(frac_n - threshold) <= tol:
            skipped += 1
            continue
        kappa = 1 if frac_n >= threshold else 0
        if g != floor_delta + kappa:
            return {"holds": False, "witness": n}
        matches += 1
    return {"holds": True, "matches": matches, "skipped": skipped}


def itinerary_word(n: int, depth: int = DEPTH) -> str:
    """Parity letters of n, J(n), ..., J^{depth-1}(n). Exact isqrt only."""
    letters = []
    x = n
    for _ in range(depth):
        letters.append("O" if x % 2 == 1 else "E")
        x = juggler_step(x)
    return "".join(letters)


def word_counts(n_max: int, depth: int = DEPTH) -> dict[str, int]:
    """Exact counts of depth-letter itinerary words over odd n in [3, n_max]."""
    counts = {w: 0 for w in WORDS4} if depth == 4 else {}
    for n in range(3, n_max + 1, 2):
        w = itinerary_word(n, depth)
        counts[w] = counts.get(w, 0) + 1
    return counts


def _prefix_counts(counts4: dict[str, int], depth: int) -> dict[str, int]:
    out: dict[str, int] = {}
    for w, c in counts4.items():
        key = w[:depth]
        out[key] = out.get(key, 0) + c
    return out


def _discrepancies(counts4: dict[str, int], odds: int) -> dict[str, float]:
    """D_w = count_w - odds * 2^{-(|w|-1)} for every word of length 2..4."""
    out: dict[str, float] = {}
    for depth in (2, 3, 4):
        expected = odds / (1 << (depth - 1))
        for w, c in _prefix_counts(counts4, depth).items():
            out[w] = c - expected
    return out


def _fit_exponent(points: list[tuple[int, float]]) -> float | None:
    """Least-squares slope of log max|D| vs log N on the top half of points."""
    usable = [(n, v) for n, v in points if v > 0]
    if len(usable) < 8:
        return None
    tail = usable[len(usable) // 2:]
    xs = [log(n) for n, _ in tail]
    ys = [log(v) for _, v in tail]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return None
    return round(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den, 4)


def scan(n_max: int = N_MAX) -> dict[str, Any]:
    """One exact pass over odd starts with a geometric discrepancy envelope."""
    counts4 = {w: 0 for w in WORDS4}
    odds = 0
    ooee_descent_violations = 0
    max_abs: dict[int, float] = {2: 0.0, 3: 0.0, 4: 0.0}
    envelope: dict[int, list[tuple[int, float]]] = {2: [], 3: [], 4: []}
    rows: list[dict[str, Any]] = []
    coarse = {n for n in COARSE_GRID if n <= n_max} | {n_max}
    next_sample = 1024

    for n in range(3, n_max + 1, 2):
        letters = []
        x = n
        for _ in range(DEPTH):
            letters.append("O" if x % 2 == 1 else "E")
            x = juggler_step(x)
        w = "".join(letters)
        counts4[w] += 1
        odds += 1
        if w == CONTRACTING_TARGET and x >= n:
            ooee_descent_violations += 1
        boundary = n + 1
        if boundary >= next_sample or boundary >= n_max - 1:
            disc = _discrepancies(counts4, odds)
            for depth in (2, 3, 4):
                depth_max = max(abs(v) for k, v in disc.items() if len(k) == depth)
                if depth_max > max_abs[depth]:
                    max_abs[depth] = depth_max
                envelope[depth].append((boundary, max_abs[depth]))
            if boundary in coarse or boundary - 1 in coarse:
                rows.append(
                    {
                        "n": boundary,
                        "odds": odds,
                        "counts4": dict(counts4),
                        "D": {k: round(v, 4) for k, v in disc.items()},
                        "max_abs_D": {str(d): round(max_abs[d], 4) for d in (2, 3, 4)},
                        "max_over_n12": {
                            str(d): round(max_abs[d] / boundary**0.5, 6)
                            for d in (2, 3, 4)
                        },
                        "max_over_n13": {
                            str(d): round(max_abs[d] / boundary ** (1 / 3), 6)
                            for d in (2, 3, 4)
                        },
                    }
                )
            while next_sample <= boundary:
                next_sample = int(next_sample * ENVELOPE_RATIO) + 1

    final = rows[-1]
    fitted = {str(d): _fit_exponent(envelope[d]) for d in (2, 3, 4)}
    ooee_count = counts4[CONTRACTING_TARGET]
    return {
        "n_max": n_max,
        "depth": DEPTH,
        "checkpoints": rows,
        "final": final,
        "max_abs_D": {str(d): round(max_abs[d], 4) for d in (2, 3, 4)},
        "fitted_exponent": fitted,
        "ooee": {
            "count": ooee_count,
            "fraction_of_odds": round(ooee_count / final["odds"], 6),
            "expected_fraction": 0.125,
            "descent_violations": ooee_descent_violations,
        },
        "anti_overclaim": dict(ANTI_OVERCLAIM),
    }


def write_json(row: dict[str, Any], path: Path = JSON_PATH) -> None:
    path.write_text(json.dumps(row, indent=2) + "\n", encoding="utf-8")


def write_docs(row: dict[str, Any], path: Path = DOC_PATH) -> None:
    final = row["final"]
    fit = row["fitted_exponent"]
    ooee = row["ooee"]
    lines = [
        "# Juggler multi-step itinerary-parity census",
        "",
        "Status: **OBSERVATION** (exact counting; no analytic lemma claimed)",
        "",
        "Exact census of the joint parity word of the first four itinerary",
        "letters on odd starts. Phase-0 falsifier for iterating the one-step",
        "discrepancy bound (Theorem 5.1 in the finite-dynamics note) to",
        "depth two and beyond. Not a frequency theorem, not a predictive",
        "state, not a termination claim.",
        "",
        f"Window: odd `n <= {row['n_max']}`. Expected class fraction of a",
        "depth-`d` word within odd starts is `2^{-(d-1)}`.",
        "",
        "| depth | max|D_w| on window | max|D|/N^{1/2} | max|D|/N^{1/3} | fitted exponent |",
        "| --- | --- | --- | --- | --- |",
    ]
    for d in ("2", "3", "4"):
        lines.append(
            f"| {d} | {row['max_abs_D'][d]} | "
            f"{final['max_over_n12'][d]} | {final['max_over_n13'][d]} | "
            f"{fit[d]} |"
        )
    lines += [
        "",
        f"Depth-4 counts at `N = {final['n']}` (odds = {final['odds']}):",
        "",
        "| word | count | D_w |",
        "| --- | --- | --- |",
    ]
    for w in sorted(final["counts4"]):
        lines.append(f"| {w} | {final['counts4'][w]} | {final['D'][w]} |")
    lines += [
        "",
        "## OOEE class",
        "",
        f"`OOEE` count {ooee['count']} = {ooee['fraction_of_odds']} of odd",
        f"starts (product density {ooee['expected_fraction']}). Every census",
        "OOEE start satisfied the four-step descent `T^4(n) < n`",
        f"(violations: {ooee['descent_violations']}); this instantiates the",
        "contraction `3^2 < 2^4` and is a guard, not a new theorem.",
        "",
        "## Reading",
        "",
        "The fitted exponents are envelope slopes on a geometric sample,",
        "label **OBSERVATION**. A depth-2 analytic lemma (discrepancy of",
        "the nested parity pair over odd n) is a separate, unproved step.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    row = scan()
    write_json(row)
    write_docs(row)
    print(
        "fitted exponents",
        row["fitted_exponent"],
        "ooee fraction",
        row["ooee"]["fraction_of_odds"],
    )


if __name__ == "__main__":
    main()
