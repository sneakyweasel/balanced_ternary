"""Exact bounded falsification tests for 3-adic polynomial cycle lifting.

The observable is one object only: the rooted cycle-lift tree.  A child
cycle modulo ``3^(k+1)`` reduces onto its parent modulo ``3^k``; edges
retain the child/parent period ratio.  The implementation deliberately
uses finite functional graphs and modular evaluation rather than
expanding the return polynomial ``f^q``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from math import comb
from typing import Callable, Iterable

from bt.calculus.section import IntPoly
from bt.metrics import v3
from research.padic_dynamics.families import DynamicsFamily, all_families

Cycle = tuple[int, ...]
Behaviour = tuple


def _require_positive(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError(f"{name} must be a positive integer")
    return n


def canonical_cycle(cycle: Iterable[int]) -> Cycle:
    """Canonical rotation of a nonempty directed cycle."""

    values = tuple(cycle)
    if not values:
        raise ValueError("cycle must be nonempty")
    return min(values[i:] + values[:i] for i in range(len(values)))


def _eval_mod(coeffs: tuple[int, ...], x: int, modulus: int) -> int:
    acc = 0
    for coefficient in reversed(coeffs):
        acc = (acc * x + coefficient) % modulus
    return acc


@lru_cache(maxsize=None)
def _cycles_mod(coeffs: tuple[int, ...], k: int) -> tuple[Cycle, ...]:
    modulus = 3**k
    done: set[int] = set()
    cycles: set[Cycle] = set()
    for start in range(modulus):
        if start in done:
            continue
        path: list[int] = []
        position: dict[int, int] = {}
        x = start
        while x not in position and x not in done:
            position[x] = len(path)
            path.append(x)
            x = _eval_mod(coeffs, x, modulus)
        if x in position:
            cycles.add(canonical_cycle(path[position[x] :]))
        done.update(path)
    return tuple(sorted(cycles, key=lambda cycle: (len(cycle), cycle)))


def cycles_mod(f: IntPoly, k: int) -> tuple[Cycle, ...]:
    """All directed cycles of ``f`` modulo ``3^k``."""

    return _cycles_mod(f.coeffs, _require_positive(k, "k"))


def reduce_cycle(cycle: Cycle, k: int) -> Cycle:
    """Reduce a cycle modulo ``3^k`` and remove its repeated period."""

    modulus = 3 ** _require_positive(k, "k")
    reduced = tuple(x % modulus for x in cycle)
    for period in range(1, len(reduced) + 1):
        if len(reduced) % period == 0 and all(
            reduced[i] == reduced[i % period] for i in range(len(reduced))
        ):
            return canonical_cycle(reduced[:period])
    raise RuntimeError("a finite cycle has no primitive period")


def cycle_lifts(f: IntPoly, cycle: Cycle, k: int) -> tuple[Cycle, ...]:
    """Cycles one precision higher which reduce onto ``cycle``."""

    parent = canonical_cycle(cycle)
    return tuple(child for child in cycles_mod(f, k + 1) if reduce_cycle(child, k) == parent)


def iterate_mod(f: IntPoly, x: int, steps: int, modulus: int) -> int:
    """Evaluate ``f^steps(x)`` modulo ``modulus`` without composition."""

    for _ in range(steps):
        x = _eval_mod(f.coeffs, x, modulus)
    return x


def _derivative_coeffs(f: IntPoly) -> tuple[int, ...]:
    return tuple(i * coefficient for i, coefficient in enumerate(f.coeffs))[1:] or (0,)


def _second_taylor_coeff_mod3(f: IntPoly, x: int) -> int:
    """``f''(x)/2`` modulo 3, evaluated without polynomial composition."""

    return sum(
        comb(i, 2) * coefficient * pow(x, i - 2, 3)
        for i, coefficient in enumerate(f.coeffs)
        if i >= 2
    ) % 3


def _return_second_taylor_mod3(f: IntPoly, x: int, period: int) -> int:
    """Quadratic Taylor coefficient of ``f^period`` at ``x`` modulo 3."""

    derivative = _derivative_coeffs(f)
    value = x % 3
    first = 1
    second = 0
    for _ in range(period):
        local_first = _eval_mod(derivative, value, 3)
        local_second = _second_taylor_coeff_mod3(f, value)
        second = (local_second * first * first + local_first * second) % 3
        first = local_first * first % 3
        value = _eval_mod(f.coeffs, value, 3)
    return second


def _capped_v3_residue(value: int, r: int) -> int:
    residue = value % (3**r)
    valuation = v3(residue)
    return r if valuation is None else min(valuation, r)


@dataclass(frozen=True)
class ClassicalSignature:
    """Classical local data for the return map of one cycle."""

    period: int
    lift_type: str
    multiplier_mod: int
    displacement_mod: int
    multiplier_minus_one_v3: int
    displacement_v3: int
    quadratic_correction_mod: int

    @property
    def coarse(self) -> tuple[object, ...]:
        return (
            self.period,
            self.lift_type,
            self.multiplier_minus_one_v3,
            self.displacement_v3,
        )

    @property
    def valuation_only(self) -> tuple[int, int, int]:
        return (self.period, self.multiplier_minus_one_v3, self.displacement_v3)

    @property
    def affine(self) -> tuple[object, ...]:
        return (
            self.period,
            self.multiplier_mod,
            self.displacement_mod,
            self.quadratic_correction_mod,
        )


def classical_signature(f: IntPoly, cycle: Cycle, k: int, r: int) -> ClassicalSignature:
    """Return-map multiplier/displacement data, truncated at horizon ``r``."""

    k = _require_positive(k, "k")
    r = _require_positive(r, "r")
    root = canonical_cycle(cycle)
    period = len(root)
    x = root[0]
    local_modulus = 3**r
    total_modulus = 3 ** (k + r)
    derivative = _derivative_coeffs(f)
    orbit = x
    multiplier = 1
    for _ in range(period):
        multiplier = multiplier * _eval_mod(derivative, orbit, local_modulus) % local_modulus
        orbit = _eval_mod(f.coeffs, orbit, total_modulus)
    difference = (orbit - x) % total_modulus
    if difference % (3**k):
        raise RuntimeError("cycle representative is not fixed by its return map")
    displacement = difference // (3**k) % local_modulus
    a3 = multiplier % 3
    b3 = displacement % 3
    if a3 == 1:
        lift_type = "grow" if b3 else "split"
    elif a3 == 0:
        lift_type = "grow-tails"
    else:
        lift_type = "partial-split"
    return ClassicalSignature(
        period=period,
        lift_type=lift_type,
        multiplier_mod=multiplier,
        displacement_mod=displacement,
        multiplier_minus_one_v3=_capped_v3_residue(multiplier - 1, r),
        displacement_v3=_capped_v3_residue(displacement, r),
        quadratic_correction_mod=(
            (3**k) * _return_second_taylor_mod3(f, x, period)
        )
        % local_modulus,
    )


def residual_signature(f: IntPoly, cycle: Cycle, k: int, r: int) -> tuple[int, tuple[int, ...]]:
    """Exact local return-function class on the depth-``r`` fibre.

    The table stores
    ``(f^q(x+3^k t) - (x+3^k t))/3^k mod 3^r`` for every ``t mod 3^r``.
    It is the function-congruence (hence residual ``Phi_r``) analogue,
    represented without constructing the high-degree iterate.
    """

    k = _require_positive(k, "k")
    r = _require_positive(r, "r")
    root = canonical_cycle(cycle)
    period = len(root)
    x = root[0]
    scale = 3**k
    local_modulus = 3**r
    total_modulus = scale * local_modulus
    table: list[int] = []
    for t in range(local_modulus):
        z = x + scale * t
        image = iterate_mod(f, z, period, total_modulus)
        difference = (image - z) % total_modulus
        if difference % scale:
            raise RuntimeError("return displacement is not divisible by the base precision")
        table.append(difference // scale % local_modulus)
    return period, tuple(table)


@lru_cache(maxsize=None)
def _behaviour(coeffs: tuple[int, ...], cycle: Cycle, k: int, r: int) -> Behaviour:
    root = canonical_cycle(cycle)
    if r == 0:
        return (len(root), ())
    f = IntPoly(coeffs)
    children = tuple(
        sorted(
            (
                len(child) // len(root),
                _behaviour(coeffs, child, k + 1, r - 1),
            )
            for child in cycle_lifts(f, root, k)
        )
    )
    return (len(root), children)


def behaviour_signature(f: IntPoly, cycle: Cycle, k: int, r: int) -> Behaviour:
    """Canonical rooted, period-labelled cycle-lift tree through depth ``r``."""

    return _behaviour(f.coeffs, canonical_cycle(cycle), k, _require_positive(r, "r"))


@dataclass(frozen=True)
class StateRecord:
    family: str
    polynomial: str
    coefficients: tuple[int, ...]
    level: int
    cycle: Cycle
    period: int
    classical: ClassicalSignature
    residual: tuple[int, tuple[int, ...]]
    behaviour: Behaviour

    def as_dict(self) -> dict[str, object]:
        record = asdict(self)
        record["classical"]["coarse"] = list(self.classical.coarse)
        record["classical"]["valuation_only"] = list(self.classical.valuation_only)
        record["classical"]["affine"] = list(self.classical.affine)
        return record


def state_records(
    families: Iterable[DynamicsFamily] | None = None,
    *,
    k_max: int = 4,
    r: int = 2,
) -> tuple[StateRecord, ...]:
    """All bounded cycle states used by the falsification scans."""

    k_max = _require_positive(k_max, "k_max")
    r = _require_positive(r, "r")
    if k_max + r > 7:
        raise ValueError("Phase-0 budget requires k_max + r <= 7")
    selected = tuple(all_families() if families is None else families)
    records: list[StateRecord] = []
    for family in selected:
        for k in range(1, k_max + 1):
            for cycle in cycles_mod(family.poly, k):
                classical = classical_signature(family.poly, cycle, k, r)
                records.append(
                    StateRecord(
                        family=family.id,
                        polynomial=family.poly.render(),
                        coefficients=family.poly.coeffs,
                        level=k,
                        cycle=cycle,
                        period=len(cycle),
                        classical=classical,
                        residual=residual_signature(family.poly, cycle, k, r),
                        behaviour=behaviour_signature(family.poly, cycle, k, r),
                    )
                )
    return tuple(records)


def _rank(record: StateRecord) -> tuple[int, int, int, int, Cycle]:
    return (
        record.level,
        max(len(record.coefficients) - 1, 0),
        max(abs(c) for c in record.coefficients),
        record.period,
        record.cycle,
    )


def _first_separation(
    records: Iterable[StateRecord],
    key: Callable[[StateRecord], object],
    observable: Callable[[StateRecord], object],
) -> tuple[int, dict[str, object] | None]:
    groups: dict[object, dict[object, StateRecord]] = {}
    for record in records:
        bucket = groups.setdefault(key(record), {})
        previous = bucket.get(observable(record))
        if previous is None or _rank(record) < _rank(previous):
            bucket[observable(record)] = record
    separated = [(group_key, values) for group_key, values in groups.items() if len(values) > 1]
    if not separated:
        return 0, None
    candidates: list[tuple[tuple[int, int, int, int, Cycle], object, list[StateRecord]]] = []
    for group_key, values in separated:
        pair = sorted(values.values(), key=_rank)[:2]
        candidates.append((_rank(pair[1]), group_key, pair))
    _candidate_rank, group_key, pair = min(candidates, key=lambda item: item[0])
    return len(separated), {
        "key": repr(group_key),
        "left": pair[0].as_dict(),
        "right": pair[1].as_dict(),
    }


def comparison_report(records: Iterable[StateRecord]) -> dict[str, object]:
    """Searches A--D from the Phase-0 plan."""

    states = tuple(records)
    coarse_bad, coarse_witness = _first_separation(
        states, lambda state: state.classical.coarse, lambda state: state.behaviour
    )
    residual_bad, residual_witness = _first_separation(
        states, lambda state: state.residual, lambda state: state.behaviour
    )
    compression_groups, compression_witness = _first_separation(
        states, lambda state: state.behaviour, lambda state: state.residual
    )
    valuation_bad, valuation_witness = _first_separation(
        states, lambda state: state.classical.valuation_only, lambda state: state.behaviour
    )
    affine_bad, affine_witness = _first_separation(
        states, lambda state: state.classical.affine, lambda state: state.behaviour
    )
    return {
        "states": len(states),
        "search_a": {
            "coarse_classes_with_different_futures": coarse_bad,
            "witness": coarse_witness,
        },
        "search_b": {
            "residual_classes_with_different_futures": residual_bad,
            "sufficient_on_census": residual_bad == 0,
            "witness": residual_witness,
            "classification": "REPARAMETERIZATION",
        },
        "search_c": {
            "behaviours_with_multiple_residual_classes": compression_groups,
            "witness": compression_witness,
        },
        "search_d": {
            "valuation_classes_with_different_futures": valuation_bad,
            "valuation_witness": valuation_witness,
            "affine_classes_with_different_futures": affine_bad,
            "affine_witness": affine_witness,
        },
    }


def triage_report(
    families: Iterable[DynamicsFamily] | None = None,
    *,
    k_max: int = 3,
    r: int = 2,
) -> dict[str, object]:
    """Complete bounded report, with no automatic promotion."""

    records = state_records(families, k_max=k_max, r=r)
    comparison = comparison_report(records)
    lift_types: dict[str, int] = {}
    periods: dict[int, int] = {}
    behaviours: set[Behaviour] = set()
    residuals: set[tuple[int, tuple[int, ...]]] = set()
    for record in records:
        lift_types[record.classical.lift_type] = lift_types.get(record.classical.lift_type, 0) + 1
        periods[record.period] = periods.get(record.period, 0) + 1
        behaviours.add(record.behaviour)
        residuals.add(record.residual)
    return {
        "families": len(tuple(all_families() if families is None else families)),
        "k_max": k_max,
        "r": r,
        "states": len(records),
        "periods": dict(sorted(periods.items())),
        "lift_types": dict(sorted(lift_types.items())),
        "residual_classes": len(residuals),
        "behaviour_classes": len(behaviours),
        "comparisons": comparison,
        "gate": "CLOSE",
        "classification": "REPARAMETERIZATION",
    }
