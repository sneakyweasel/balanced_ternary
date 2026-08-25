"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.positivity_lrs.spec import CompanionObsSpec, map_spec, next_window, observation, over_budget

MAX_INDEX = 64
MODULI = tuple(range(2, 33))
PREFIX_CAP = 24


def iterate_windows(
    spec: CompanionObsSpec,
    *,
    max_index: int = MAX_INDEX,
) -> tuple[tuple[int, ...], ...]:
    current = spec.window
    out = [current]
    for _ in range(max_index):
        if over_budget(current):
            break
        current = next_window(current, spec.last_row)
        out.append(current)
        if over_budget(current):
            break
    return tuple(out)


def observations(windows: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(observation(item) for item in windows)


def first_negative_index(values: tuple[int, ...]) -> int | None:
    for index, value in enumerate(values):
        if value < 0:
            return index
    return None


def last_negative_index(values: tuple[int, ...]) -> int | None:
    found = None
    for index, value in enumerate(values):
        if value < 0:
            found = index
    return found


def orthant_invariant(spec: CompanionObsSpec) -> bool:
    return all(coeff >= 0 for coeff in spec.last_row)


def modular_negative_residues(
    values: tuple[int, ...],
    moduli: tuple[int, ...] = MODULI,
) -> dict[int, tuple[int, ...]]:
    found: dict[int, set[int]] = {modulus: set() for modulus in moduli}
    for value in values:
        for modulus in moduli:
            found[modulus].add(value % modulus)
    return {modulus: tuple(sorted(residues)) for modulus, residues in found.items()}


def evidence_state(
    spec: CompanionObsSpec,
    *,
    max_index: int = MAX_INDEX,
) -> dict[str, object]:
    windows = iterate_windows(spec, max_index=max_index)
    values = observations(windows)
    neg = first_negative_index(values)
    last_neg = last_negative_index(values)
    bit_capped = bool(windows) and over_budget(windows[-1])
    window_nonneg = neg is None
    exhausted = window_nonneg and (len(values) >= max_index + 1 or bit_capped)
    after_last = () if last_neg is None else values[last_neg + 1 :]
    eventual_candidate = last_neg is not None and bool(after_last) and all(v >= 0 for v in after_last)
    if neg is not None:
        status = "NEGATIVE_WITNESS"
    elif window_nonneg:
        status = "CERTIFIED_ON_WINDOW"
    else:
        status = "NO_NEGATIVE_FOUND"
    return {
        "status": status,
        "universal": "UNKNOWN",
        "values": values[:PREFIX_CAP],
        "length": len(values),
        "first_negative": neg,
        "last_negative": last_neg,
        "min_on_window": min(values) if values else None,
        "window_nonneg": window_nonneg,
        "eventual_nonneg_candidate": eventual_candidate,
        "orthant_invariant": orthant_invariant(spec),
        "modular_residues": modular_negative_residues(values),
        "exhausted": exhausted,
        "computation": "COMPUTATION_EXHAUSTED" if exhausted else "WITHIN_BUDGET",
        "universal_nonneg": False,
        "note": "CERTIFIED_ON_WINDOW is not universal nonnegativity",
    }


def falsify_claims(spec: CompanionObsSpec | None = None) -> dict[str, dict[str, object]]:
    target = spec if spec is not None else map_spec()
    report = evidence_state(target)
    windows = iterate_windows(target)
    obs = observations(windows)
    neg = report["first_negative"]
    last_neg = report["last_negative"]
    unique = len(set(windows)) < len(windows)
    signs = tuple(1 if v > 0 else (-1 if v < 0 else 0) for v in obs)
    period = None
    for length in range(1, min(8, len(signs) // 2) + 1):
        if signs[:length] * (len(signs) // length) == signs[: length * (len(signs) // length)]:
            if signs[:length] * 2 != signs[:length]:
                period = length
                break
            if length > 1:
                period = length
                break
    return {
        "all_terms_nonneg": {
            "claim": "every first-coordinate observation on the search bound is nonnegative",
            "holds_on_window": neg is None,
            "status": "REFUTED" if neg is not None else "INCONCLUSIVE",
            "counterexample": neg,
            "quantifier": "UNIVERSAL",
            "evidence": report["status"],
        },
        "all_terms_positive": {
            "claim": "every first-coordinate observation on the search bound is strictly positive",
            "holds_on_window": all(v > 0 for v in obs),
            "status": "REFUTED" if any(v <= 0 for v in obs) else "INCONCLUSIVE",
            "counterexample": next((i for i, v in enumerate(obs) if v <= 0), None),
            "quantifier": "UNIVERSAL",
        },
        "signs_periodic": {
            "claim": "the observed sign sequence is purely periodic of small period",
            "holds_on_window": period is not None,
            "status": "SUPPORTED" if period is not None else "INCONCLUSIVE",
            "counterexample": None,
            "period": period,
            "quantifier": "UNIVERSAL",
        },
        "positive_orthant_invariant": {
            "claim": "nonnegative last-row coefficients preserve the nonnegative orthant",
            "holds_on_window": orthant_invariant(target) and all(v >= 0 for v in target.window),
            "status": (
                "EXACT"
                if orthant_invariant(target) and all(v >= 0 for v in target.window)
                else "REFUTED"
            ),
            "counterexample": None if orthant_invariant(target) else "mixed last_row signs",
            "quantifier": "UNIVERSAL",
        },
        "residue_quotient_proves_nonneg": {
            "claim": "a modulus in 2..32 excludes negative observations",
            "holds_on_window": False,
            "status": "REFUTED" if neg is not None else "INCONCLUSIVE",
            "counterexample": neg,
            "note": "a residue class is not a sign theorem",
            "quantifier": "UNIVERSAL",
        },
        "bounded_orbit_implies_nonneg": {
            "claim": "the window trajectory is finite within the bound, hence nonnegative",
            "holds_on_window": unique,
            "status": "REFUTED" if (not unique) or neg is not None else "INCONCLUSIVE",
            "counterexample": neg,
            "quantifier": "UNIVERSAL",
        },
        "eventual_nonneg_from_n0": {
            "claim": "nonnegativity from the first index follows from a finite negative prefix",
            "holds_on_window": neg is None,
            "status": "REFUTED" if neg is not None else "INCONCLUSIVE",
            "counterexample": neg,
            "last_negative": last_neg,
            "quantifier": "UNIVERSAL",
            "note": "a later nonnegative tail is not nonnegativity from n=0",
        },
        "large_terms_positive": {
            "claim": "all sufficiently large terms on the prefix are positive",
            "holds_on_window": last_neg is None or (
                last_neg < len(obs) - 1 and all(v > 0 for v in obs[last_neg + 1 :])
            ),
            "status": (
                "REFUTED"
                if last_neg is not None and last_neg >= len(obs) - 1
                else ("INCONCLUSIVE" if last_neg is None else "WINDOW_ONLY")
            ),
            "counterexample": last_neg,
            "quantifier": "UNIVERSAL",
        },
    }
