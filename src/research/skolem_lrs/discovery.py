"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.skolem_lrs.spec import CompanionShiftSpec, map_spec, next_window, observation, over_budget

MAX_INDEX = 64
MODULI = tuple(range(2, 33))
PREFIX_CAP = 24


def iterate_windows(
    spec: CompanionShiftSpec,
    *,
    max_index: int = MAX_INDEX,
) -> tuple[tuple[int, ...], ...]:
    current = spec.window
    out = [current]
    for _ in range(max_index):
        if observation(current) == 0:
            break
        if over_budget(current):
            break
        current = next_window(current, spec.last_row)
        out.append(current)
        if over_budget(current):
            break
    return tuple(out)


def observations(windows: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(observation(item) for item in windows)


def first_zero_index(values: tuple[int, ...]) -> int | None:
    for index, value in enumerate(values):
        if value == 0:
            return index
    return None


def first_negative_index(values: tuple[int, ...]) -> int | None:
    for index, value in enumerate(values):
        if value < 0:
            return index
    return None


def modular_zeros(
    values: tuple[int, ...],
    moduli: tuple[int, ...] = MODULI,
) -> dict[int, int | None]:
    found: dict[int, int | None] = {modulus: None for modulus in moduli}
    for index, value in enumerate(values):
        for modulus in moduli:
            if found[modulus] is None and value % modulus == 0:
                found[modulus] = index
    return found


def evidence_state(
    spec: CompanionShiftSpec,
    *,
    max_index: int = MAX_INDEX,
) -> dict[str, object]:
    windows = iterate_windows(spec, max_index=max_index)
    values = observations(windows)
    zero_at = first_zero_index(values)
    bit_capped = bool(windows) and over_budget(windows[-1])
    exhausted = zero_at is None and (len(values) >= max_index + 1 or bit_capped)
    mods = modular_zeros(values)
    excluding = tuple(m for m, idx in mods.items() if idx is None)
    if zero_at is not None:
        status = "ZERO_WITNESS"
    elif exhausted:
        status = "FINITE_ZERO_FREE"
    else:
        status = "FINITE_ZERO_SEARCH"
    # A modulus with no zero on a finite prefix is not integer exclusion.
    modular_status = "PREFIX_GAPS" if excluding else "NO_PREFIX_EXCLUSION"
    if excluding and zero_at is None:
        modular_status = "PREFIX_GAPS_NOT_EXCLUSION"
    return {
        "status": status,
        "values": values[:PREFIX_CAP],
        "length": len(values),
        "zero_at": zero_at,
        "first_negative": first_negative_index(values),
        "modular_zeros": mods,
        "moduli_without_zero": excluding,
        "modular_status": modular_status,
        "exhausted": exhausted,
        "computation": "COMPUTATION_EXHAUSTED" if exhausted and zero_at is None else "WITHIN_BUDGET",
        "universal_zero_free": False,
        "note": "NO ZERO FOUND is not NO ZERO EXISTS",
    }


def falsify_claims(spec: CompanionShiftSpec | None = None) -> dict[str, dict[str, object]]:
    target = spec if spec is not None else map_spec()
    report = evidence_state(target)
    values = iterate_windows(target)
    obs = observations(values)
    zero_at = report["zero_at"]
    first_neg = report["first_negative"]
    mods = report["modular_zeros"]
    asserted_exclusion = next(
        (m for m, idx in mods.items() if idx is None),
        None,
    )
    # Recheck exclusion claims against the same bounded prefix only.
    return {
        "never_vanishes": {
            "claim": "the first coordinate never vanishes on the search bound",
            "holds_on_window": zero_at is None,
            "status": "REFUTED" if zero_at is not None else "INCONCLUSIVE",
            "counterexample": zero_at,
            "quantifier": "EXISTENTIAL",
            "evidence": report["status"],
        },
        "fixed_sign": {
            "claim": "the first coordinate has constant sign",
            "holds_on_window": first_neg is None or all(v <= 0 for v in obs),
            "status": "REFUTED" if first_neg is not None and any(v > 0 for v in obs) else "INCONCLUSIVE",
            "counterexample": first_neg,
            "quantifier": "UNIVERSAL",
        },
        "eventually_positive": {
            "claim": "the first coordinate is eventually positive on the prefix",
            "holds_on_window": first_neg is None,
            "status": "REFUTED" if first_neg is not None else "INCONCLUSIVE",
            "counterexample": first_neg,
            "quantifier": "UNIVERSAL",
        },
        "modulus_excludes_zero": {
            "claim": "some m in 2..32 has no first-coordinate 0 residue on the prefix",
            "holds_on_window": asserted_exclusion is not None,
            "status": "PREFIX_GAPS_NOT_EXCLUSION" if asserted_exclusion is not None else "NO_PREFIX_EXCLUSION",
            "counterexample": None,
            "moduli_without_zero": report["moduli_without_zero"],
            "quantifier": "UNIVERSAL",
            "note": "a prefix gap is not an integer modular-exclusion theorem",
        },
        "finite_reachable_set": {
            "claim": "the window trajectory enters a finite set within the bound",
            "holds_on_window": len(set(values)) < len(values),
            "status": "REFUTED" if len(set(values)) == len(values) else "EXISTENTIAL_WITNESS",
            "counterexample": None if len(set(values)) == len(values) else "repeat",
            "quantifier": "UNIVERSAL",
        },
    }
