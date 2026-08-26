"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.mx_plus_r.spec import mx_plus_r_step
from research.mx_plus_r_7x1_class_obstruction.spec import map_spec

WINDOW = tuple(n for n in range(1, 81) if n % 2 == 1)
IMAGE_CLASS = frozenset({1, 2, 4})
OUT_CLASS = frozenset({0, 3, 5, 6})


def step(n: int) -> int:
    return mx_plus_r_step(n, 7, 1)


def valuation(n: int) -> int:
    y = 7 * n + 1
    k = 0
    while y % 2 == 0:
        y //= 2
        k += 1
    return k


def orbit_of(n: int, *, max_steps: int = 16) -> tuple[int, ...]:
    seen: list[int] = []
    current = n
    for _ in range(max_steps):
        if current in seen:
            break
        seen.append(current)
        current = step(current)
    return tuple(seen)


def image_residues(window: tuple[int, ...] = WINDOW) -> frozenset[int]:
    return frozenset(step(n) % 7 for n in window)


def image_divisible_by_seven(window: tuple[int, ...] = WINDOW) -> bool:
    return any(step(n) % 7 == 0 for n in window)


def valuation_residue_pairs(window: tuple[int, ...] = WINDOW) -> frozenset[tuple[int, int]]:
    return frozenset((valuation(n) % 3, step(n) % 7) for n in window)


def one_preimage(m: int) -> int:
    if isinstance(m, bool) or not isinstance(m, int) or m < 1:
        raise ValueError(f"m must be a positive int, got {m!r}")
    return (pow(2, 3 * m) - 1) // 7


def contrast_units(m: int, r: int, modulus: int, window: tuple[int, ...] = WINDOW) -> frozenset[int]:
    return frozenset(mx_plus_r_step(n, m, r) % modulus for n in window)


def evidence_state(spec=None) -> dict[str, object]:
    target = spec if spec is not None else map_spec()
    path = orbit_of(target.start, max_steps=target.start_remaining)
    path32 = orbit_of(target.start, max_steps=32)
    residues = image_residues()
    pairs = valuation_residue_pairs()
    preimages = tuple((m, one_preimage(m), one_preimage(m) % 7) for m in range(1, 8))
    return {
        "start": target.start,
        "path": path,
        "hits_one_horizon_16": 1 in path,
        "hits_one_horizon_32": 1 in path32,
        "t_one": step(1),
        "image_residues_mod7": tuple(sorted(residues)),
        "image_in_units_subgroup": residues <= IMAGE_CLASS,
        "image_divisible_by_seven": image_divisible_by_seven(),
        "valuation_pairs": tuple(sorted(pairs)),
        "valuation_determines_image_class": pairs == {(0, 1), (1, 4), (2, 2)},
        "preimages_of_one": preimages,
        "seventy_three": (73, 73 % 7, step(73)),
        "multiple_of_seven_preimage": (299593, 299593 % 7, step(299593)),
        "contrast_3x1_mod3": tuple(sorted(contrast_units(3, 1, 3))),
        "contrast_5x1_mod5": tuple(sorted(contrast_units(5, 1, 5))),
        "horizon_class_stable": image_residues(WINDOW) == image_residues(
            tuple(n for n in range(1, 33) if n % 2 == 1)
        ),
        "note": "image class is not a basin exclusion; finite non-visit of 1 is not divergence",
    }


def falsify_claims(spec=None) -> dict[str, dict[str, object]]:
    target = spec if spec is not None else map_spec()
    report = evidence_state(target)
    return {
        "family_is_the_yield": {
            "claim": "rediscovering 2^k y = 7x+1 is the mathematical yield",
            "holds_on_window": True,
            "status": "REFUTED",
            "counterexample": "family is KNOWN infrastructure",
        },
        "start_reaches_one_on_bound": {
            "claim": "seed 3 reaches 1 within 16 steps",
            "holds_on_window": report["hits_one_horizon_16"],
            "status": "REFUTED",
            "counterexample": report["path"],
        },
        "out_class_cannot_reach_one": {
            "claim": "odd n ≡ 3,5,6 (mod 7) cannot reach 1",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": report["seventy_three"],
        },
        "multiples_of_seven_cannot_reach_one": {
            "claim": "odd multiples of 7 cannot reach 1",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": report["multiple_of_seven_preimage"],
        },
        "image_avoids_zero_mod_seven": {
            "claim": "T(n) is never 0 (mod 7) on the odd window",
            "holds_on_window": not report["image_divisible_by_seven"],
            "status": "EXACT",
            "counterexample": None,
        },
        "image_in_two_subgroup": {
            "claim": "T(n) ≡ 1,2, or 4 (mod 7) on the odd window",
            "holds_on_window": report["image_in_units_subgroup"],
            "status": "EXACT",
            "counterexample": None,
        },
        "same_obstruction_as_3x1": {
            "claim": "the 7x+1 image class is the same as filling all units, as in 3x+1 / 5x+1",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {
                "7x1": report["image_residues_mod7"],
                "3x1": report["contrast_3x1_mod3"],
                "5x1": report["contrast_5x1_mod5"],
            },
        },
        "horizon_changes_image_class": {
            "claim": "widening the odd window inside the budget changes the image class",
            "holds_on_window": not report["horizon_class_stable"],
            "status": "REFUTED",
            "counterexample": report["image_residues_mod7"],
        },
    }
