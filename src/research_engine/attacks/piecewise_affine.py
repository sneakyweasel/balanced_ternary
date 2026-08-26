"""Piecewise-affine census from exact I/O. A sample-supported line is not a Z-theorem."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from math import gcd
from types import MappingProxyType
from typing import Any

from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import ClaimKind, SearchScope

MIN_SUPPORT = 3
DEFAULT_SAMPLE_WINDOW = tuple(range(-48, 49))
DEFAULT_FALSIFY_WINDOW = tuple(range(-96, 97))
COEFFICIENT_BOX = 9
K_MAX = 12
MIN_DISTINCT_K = 3
PARAM_COVERAGE = 0.6
FINITE_COVERAGE = 0.75
MAX_MODULUS = 16
BASE_BOX = (2, 3, 5, 7)


def _is_integer_state(state: object) -> bool:
    if not isinstance(state, tuple) or not state:
        return False
    return all(isinstance(part, int) and not isinstance(part, bool) for part in state)


class BranchEvidenceStatus(str, Enum):
    SUPPORTED_BY_SAMPLES = "SUPPORTED_BY_SAMPLES"
    REFUTED = "REFUTED"
    EXACTLY_CERTIFIED = "EXACTLY_CERTIFIED"
    UNDERDETERMINED = "UNDERDETERMINED"


class CensusKind(str, Enum):
    FINITE_CENSUS = "FINITE_CENSUS"
    PARAMETERIZED_CENSUS = "PARAMETERIZED_CENSUS"
    UNRESOLVED = "UNRESOLVED"


class RegionKind(str, Enum):
    INTERVAL = "interval"
    SIGN = "sign"
    CONGRUENCE = "congruence"
    VALUATION = "valuation"
    FINITE_SET = "finite_set"
    DIVISIBILITY = "divisibility"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class BranchRegion:
    """Domain descriptor inferred from support. Unknown if no pattern is complete."""

    kind: str
    parameters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))

    def as_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, **dict(self.parameters)}


@dataclass(frozen=True)
class AffineBranch:
    """Cleared relation ``q y = p x + r``. Window agreement is not a global theorem."""

    p: int
    q: int
    r: int
    support: tuple[int, ...]
    counterexamples: tuple[int, ...] = ()
    status: str = BranchEvidenceStatus.UNDERDETERMINED.value
    region: BranchRegion | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "p": self.p,
            "q": self.q,
            "r": self.r,
            "support": self.support,
            "counterexamples": self.counterexamples,
            "status": self.status,
            "region": None if self.region is None else self.region.as_dict(),
        }


@dataclass(frozen=True)
class LatentControl:
    """Derived parameter. Not an explicit problem control and not a map-specific type."""

    kind: str
    observed_values: tuple[Any, ...]
    parameters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "observed_values": self.observed_values,
            **dict(self.parameters),
        }


@dataclass(frozen=True)
class ParameterizedFamily:
    """``b^k y = p x + r`` with unbounded observed ``k``. Not a finite branch table."""

    p: int
    r: int
    observed_k: tuple[int, ...]
    support: tuple[int, ...]
    status: str
    base: int = 2
    region: BranchRegion | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "p": self.p,
            "r": self.r,
            "q_base": self.base,
            "base": self.base,
            "observed_k": self.observed_k,
            "support": self.support,
            "status": self.status,
            "region": None if self.region is None else self.region.as_dict(),
        }


@dataclass(frozen=True)
class PiecewiseAffineCensus:
    branches: tuple[AffineBranch, ...]
    family: ParameterizedFamily | None
    latent_controls: tuple[LatentControl, ...]
    census_kind: str
    coverage: float
    unresolved: tuple[int, ...]
    sample_count: int
    coefficient_box: int
    k_max: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "census_kind": self.census_kind,
            "coverage": self.coverage,
            "sample_count": self.sample_count,
            "branch_count": len(self.branches),
            "unresolved": self.unresolved,
            "coefficient_box": self.coefficient_box,
            "k_max": self.k_max,
            "branches": tuple(item.as_dict() for item in self.branches),
            "family": None if self.family is None else self.family.as_dict(),
            "latent_controls": tuple(item.as_dict() for item in self.latent_controls),
            "reconstructed_affine": None,
        }


def _reduce_line(p: int, q: int, r: int) -> tuple[int, int, int] | None:
    if q == 0:
        return None
    g = gcd(gcd(abs(p), abs(q)), abs(r))
    if g == 0:
        g = 1
    p, q, r = p // g, q // g, r // g
    if q < 0:
        p, q, r = -p, -q, -r
    return p, q, r


def _holds(p: int, q: int, r: int, x: int, y: int) -> bool:
    return q * y == p * x + r


def _line_from_points(x1: int, y1: int, x2: int, y2: int) -> tuple[int, int, int] | None:
    if x1 == x2:
        return None
    return _reduce_line(y2 - y1, x2 - x1, (x2 - x1) * y1 - (y2 - y1) * x1)


def _v2(n: int) -> int | None:
    if n == 0:
        return None
    value = abs(n)
    k = 0
    while value % 2 == 0:
        value //= 2
        k += 1
    return k


def _is_power_of_base(n: int, base: int) -> int | None:
    if n <= 0 or base < 2:
        return None
    k = 0
    value = n
    while value % base == 0:
        value //= base
        k += 1
        if k > K_MAX:
            return None
    if value == 1:
        return k
    return None


def _is_power_of_two(n: int) -> int | None:
    return _is_power_of_base(n, 2)


def _eval_map(spec: ProblemSpec, x: int, phase: object) -> int | None:
    try:
        state = spec.canonicalize((int(x),))
    except (TypeError, ValueError):
        return None
    if not _is_integer_state(state):
        return None
    try:
        controls = spec.legal_controls(state, phase)
    except (TypeError, ValueError):
        return None
    if len(controls) != 1:
        return None
    try:
        nxt = spec.canonicalize(spec.transition(state, controls[0], phase))
    except (TypeError, ValueError):
        return None
    if not _is_integer_state(nxt):
        return None
    return int(nxt[0])


def _collect_samples(
    spec: ProblemSpec,
    context: AttackContext,
    window: Sequence[int],
) -> dict[int, int]:
    phase = spec.initial_phase()
    samples: dict[int, int] = {}
    for value in window:
        image = _eval_map(spec, int(value), phase)
        if image is None:
            continue
        samples[int(value)] = image
    state = spec.canonicalize(spec.initial_state)
    orbit_phase = spec.initial_phase()
    steps = context.max_steps if context.max_steps is not None else 16
    for _ in range(max(0, steps)):
        if not _is_integer_state(state):
            break
        try:
            controls = spec.legal_controls(state, orbit_phase)
        except (TypeError, ValueError):
            break
        if len(controls) != 1:
            break
        x = int(state[0])
        try:
            nxt = spec.canonicalize(spec.transition(state, controls[0], orbit_phase))
        except (TypeError, ValueError):
            break
        if not _is_integer_state(nxt):
            break
        samples[x] = int(nxt[0])
        orbit_phase = spec.next_phase(orbit_phase, controls[0])
        state = nxt
    return samples


def _region_contains(region: BranchRegion, x: int) -> bool:
    params = region.parameters
    kind = region.kind
    if kind == RegionKind.SIGN.value:
        if params.get("sign") == "nonneg":
            return x >= 0
        if params.get("sign") == "neg":
            return x < 0
        return False
    if kind == RegionKind.INTERVAL.value:
        return int(params["lo"]) <= x <= int(params["hi"])
    if kind == RegionKind.CONGRUENCE.value:
        return x % int(params["modulus"]) == int(params["residue"])
    if kind == RegionKind.VALUATION.value:
        return x != 0 and _v2(x) == int(params["k"])
    if kind == RegionKind.DIVISIBILITY.value:
        p = int(params["p"])
        r = int(params["r"])
        k = params.get("k")
        target = p * x + r
        val = _v2(target)
        if val is None:
            return False
        if k is None:
            return True
        return val == int(k)
    if kind == RegionKind.FINITE_SET.value:
        return x in set(params.get("values", ()))
    return False


def _region_complete(region_pts: set[int], support: set[int]) -> bool:
    return bool(region_pts) and len(region_pts) >= MIN_SUPPORT and region_pts <= support


def infer_region(support: Iterable[int], domain: Iterable[int]) -> BranchRegion:
    """First descriptor whose sampled class sits inside the support.

    Accidental intersection points may lie outside that class; they do not
    block the region. Purity of the raw support is not required.
    """
    points = set(support)
    sampled = set(domain)
    if not points:
        return BranchRegion(RegionKind.UNKNOWN.value)

    nonneg = {x for x in sampled if x >= 0}
    if _region_complete(nonneg, points):
        return BranchRegion(RegionKind.SIGN.value, {"sign": "nonneg"})
    neg = {x for x in sampled if x < 0}
    if _region_complete(neg, points):
        return BranchRegion(RegionKind.SIGN.value, {"sign": "neg"})

    lo, hi = min(points), max(points)
    interval_pts = {x for x in sampled if lo <= x <= hi}
    if interval_pts == points and _region_complete(interval_pts, points):
        return BranchRegion(RegionKind.INTERVAL.value, {"lo": lo, "hi": hi})

    for modulus in range(2, MAX_MODULUS + 1):
        best: tuple[int, int] | None = None
        for residue in range(modulus):
            class_pts = {x for x in sampled if x % modulus == residue}
            if _region_complete(class_pts, points) and (
                best is None or len(class_pts) > best[0]
            ):
                best = (len(class_pts), residue)
        if best is not None:
            return BranchRegion(
                RegionKind.CONGRUENCE.value,
                {"modulus": modulus, "residue": best[1]},
            )

    for k in sorted({_v2(x) for x in points if x != 0} - {None}):
        val_pts = {x for x in sampled if x != 0 and _v2(x) == k}
        if _region_complete(val_pts, points):
            return BranchRegion(RegionKind.VALUATION.value, {"k": k})

    if len(points) <= MIN_SUPPORT:
        return BranchRegion(
            RegionKind.FINITE_SET.value,
            {"values": tuple(sorted(points))},
        )
    return BranchRegion(RegionKind.UNKNOWN.value)


def _falsify_branch(
    spec: ProblemSpec,
    p: int,
    q: int,
    r: int,
    region: BranchRegion,
    support: set[int],
    phase: object,
    window: Sequence[int],
) -> tuple[int, ...]:
    hits: list[int] = []
    for value in sorted(window, key=lambda item: (abs(item), item)):
        if value in support:
            continue
        if region.kind != RegionKind.UNKNOWN.value and not _region_contains(region, value):
            continue
        image = _eval_map(spec, value, phase)
        if image is None:
            continue
        if not _holds(p, q, r, value, image):
            hits.append(value)
            if len(hits) >= 8:
                break
    return tuple(hits)


def candidate_affine_laws(
    samples: Mapping[int, int],
) -> dict[tuple[int, int, int], set[int]]:
    """Affine identities from exact I/O. Region inference is a later step."""

    return _candidate_lines(samples)


def _candidate_lines(samples: Mapping[int, int]) -> dict[tuple[int, int, int], set[int]]:
    items = tuple(samples.items())
    supports: dict[tuple[int, int, int], set[int]] = {}
    for i, (x1, y1) in enumerate(items):
        for x2, y2 in items[i + 1 :]:
            line = _line_from_points(x1, y1, x2, y2)
            if line is None:
                continue
            bucket = supports.setdefault(line, set())
            if not bucket:
                p, q, r = line
                for x, y in items:
                    if _holds(p, q, r, x, y):
                        bucket.add(x)
    return {line: pts for line, pts in supports.items() if len(pts) >= MIN_SUPPORT}


def _parameterized_families(samples: Mapping[int, int]) -> list[ParameterizedFamily]:
    items = tuple(samples.items())
    if not items:
        return []
    families: list[ParameterizedFamily] = []
    for base in BASE_BOX:
        for p in range(-COEFFICIENT_BOX, COEFFICIENT_BOX + 1):
            for r in range(-COEFFICIENT_BOX, COEFFICIENT_BOX + 1):
                if p == 0 and r == 0:
                    continue
                if gcd(abs(p), abs(r) if r else 1) != 1 and not (p == 0 or r == 0):
                    continue
                ks: list[int] = []
                support: list[int] = []
                for x, y in items:
                    target = p * x + r
                    if y == 0:
                        continue
                    if target % y != 0:
                        continue
                    k = _is_power_of_base(target // y, base)
                    if k is None:
                        continue
                    support.append(x)
                    ks.append(k)
                if len(support) < MIN_SUPPORT:
                    continue
                coverage = len(support) / len(items)
                distinct = tuple(sorted(set(ks)))
                if coverage < PARAM_COVERAGE or len(distinct) < MIN_DISTINCT_K:
                    continue
                families.append(
                    ParameterizedFamily(
                        p=p,
                        r=r,
                        base=base,
                        observed_k=distinct,
                        support=tuple(sorted(support)),
                        status=BranchEvidenceStatus.SUPPORTED_BY_SAMPLES.value,
                        region=BranchRegion(
                            RegionKind.DIVISIBILITY.value,
                            {"p": p, "r": r, "q_base": base, "base": base},
                        ),
                    )
                )
    families.sort(
        key=lambda item: (len(item.support), len(item.observed_k), -item.base),
        reverse=True,
    )
    return families


def _finite_branches(
    spec: ProblemSpec,
    samples: Mapping[int, int],
    phase: object,
    falsify_window: Sequence[int],
) -> tuple[AffineBranch, ...]:
    domain = set(samples)
    ranked = sorted(
        _candidate_lines(samples).items(),
        key=lambda item: len(item[1]),
        reverse=True,
    )
    covered: set[int] = set()
    branches: list[AffineBranch] = []
    for (p, q, r), support in ranked:
        leftover = support - covered
        if len(leftover) < MIN_SUPPORT:
            continue
        region = infer_region(leftover if leftover == support else support, domain)
        if region.kind in {RegionKind.UNKNOWN.value, RegionKind.FINITE_SET.value}:
            continue
        counterexamples = _falsify_branch(
            spec, p, q, r, region, support, phase, falsify_window
        )
        if counterexamples:
            continue
        region_pts = {x for x in domain if _region_contains(region, x)}
        if not _region_complete(region_pts, leftover | (support & region_pts)):
            continue
        status = BranchEvidenceStatus.SUPPORTED_BY_SAMPLES.value
        branch = AffineBranch(
            p=p,
            q=q,
            r=r,
            support=tuple(sorted(region_pts)),
            counterexamples=(),
            status=status,
            region=region,
        )
        branches.append(branch)
        covered.update(region_pts)
    return tuple(branches)


def _latent_from_census(
    branches: Sequence[AffineBranch],
    family: ParameterizedFamily | None,
) -> tuple[LatentControl, ...]:
    controls: list[LatentControl] = []
    if family is not None:
        controls.append(
            LatentControl(
                kind="power_parameter",
                observed_values=family.observed_k,
                parameters={"p": family.p, "r": family.r, "q_base": family.base, "base": family.base},
            )
        )
        return tuple(controls)
    residues: dict[int, list[int]] = {}
    signs: list[str] = []
    for branch in branches:
        if branch.region is None:
            continue
        if branch.region.kind == RegionKind.CONGRUENCE.value:
            modulus = int(branch.region.parameters["modulus"])
            residue = int(branch.region.parameters["residue"])
            residues.setdefault(modulus, []).append(residue)
        elif branch.region.kind == RegionKind.SIGN.value:
            signs.append(str(branch.region.parameters.get("sign")))
    for modulus, values in residues.items():
        controls.append(
            LatentControl(
                kind="residue",
                observed_values=tuple(sorted(set(values))),
                parameters={"modulus": modulus},
            )
        )
    if signs:
        controls.append(LatentControl(kind="sign", observed_values=tuple(sorted(set(signs)))))
    return tuple(controls)


def run_piecewise_affine_census(
    spec: ProblemSpec,
    context: AttackContext | None = None,
    *,
    window: Sequence[int] = DEFAULT_SAMPLE_WINDOW,
    falsify_window: Sequence[int] = DEFAULT_FALSIFY_WINDOW,
) -> PiecewiseAffineCensus:
    """Infer affine branches from exact samples. Does not read ``spec.name``."""
    ctx = context if context is not None else AttackContext()
    samples = _collect_samples(spec, ctx, window)
    phase = spec.initial_phase()
    families = _parameterized_families(samples)
    family = families[0] if families else None
    if family is not None:
        unresolved = tuple(sorted(set(samples) - set(family.support)))
        coverage = len(family.support) / len(samples) if samples else 0.0
        return PiecewiseAffineCensus(
            branches=(),
            family=family,
            latent_controls=_latent_from_census((), family),
            census_kind=CensusKind.PARAMETERIZED_CENSUS.value,
            coverage=coverage,
            unresolved=unresolved,
            sample_count=len(samples),
            coefficient_box=COEFFICIENT_BOX,
            k_max=K_MAX,
        )

    half = tuple(value for value in window if abs(value) <= max(abs(window[0]), abs(window[-1])) // 2)
    small_samples = _collect_samples(spec, ctx, half) if half else samples
    branches = _finite_branches(spec, samples, phase, falsify_window)
    small_branches = _finite_branches(spec, small_samples, phase, falsify_window) if small_samples else ()
    explained: set[int] = set()
    for branch in branches:
        explained.update(branch.support)
    unresolved = tuple(sorted(set(samples) - explained))
    coverage = (len(explained) / len(samples)) if samples else 0.0
    grew = len(branches) > len(small_branches) and len(small_branches) > 0
    if coverage >= FINITE_COVERAGE and branches and not grew:
        kind = CensusKind.FINITE_CENSUS.value
    else:
        kind = CensusKind.UNRESOLVED.value
        if grew:
            branches = ()
            coverage = 0.0
            unresolved = tuple(sorted(samples))
    return PiecewiseAffineCensus(
        branches=branches,
        family=None,
        latent_controls=_latent_from_census(branches, None),
        census_kind=kind,
        coverage=coverage,
        unresolved=unresolved,
        sample_count=len(samples),
        coefficient_box=COEFFICIENT_BOX,
        k_max=K_MAX,
    )


def _singleton_integer(spec: ProblemSpec, context: AttackContext) -> bool:
    if spec.dimension != 1 or context.affine is not None:
        return False
    try:
        start = spec.canonicalize(spec.initial_state)
    except (TypeError, ValueError):
        return False
    if not _is_integer_state(start):
        return False
    try:
        controls = spec.legal_controls(start, spec.initial_phase())
    except (TypeError, ValueError):
        return False
    return len(controls) == 1


class PiecewiseAffineCensusAttack:
    """Recover latent affine branches from I/O. Does not install controls on the spec."""

    name = "piecewise_affine"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        return _singleton_integer(spec, context)

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        if not _singleton_integer(spec, context):
            return inapplicable(
                self.name,
                "piecewise-affine census needs a 1-D integer singleton control without AffineSystem",
                ClaimKind.REACHABLE,
            )
        census = run_piecewise_affine_census(spec, context)
        evidence = census.as_dict()
        if census.census_kind == CensusKind.PARAMETERIZED_CENSUS.value and census.family is not None:
            claim = (
                f"sample-supported parameterized family {census.family.base}^k y = "
                f"{census.family.p} x + {census.family.r} "
                f"with observed k={census.family.observed_k}; this is not a global branch theorem"
            )
            return AttackResult(
                name=self.name,
                status=AttackStatus.OBSERVATION,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim=claim,
                evidence=evidence,
                recommended_next_attacks=("parameter_domain", "closure"),
            )
        if census.census_kind == CensusKind.FINITE_CENSUS.value and census.branches:
            claim = (
                f"sample-supported finite piecewise-affine census with {len(census.branches)} "
                "branches; window agreement is not a Z-theorem"
            )
            return AttackResult(
                name=self.name,
                status=AttackStatus.OBSERVATION,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim=claim,
                evidence=evidence,
                recommended_next_attacks=("parameter_domain", "closure"),
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.INCONCLUSIVE,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.BOUNDED,
            claim=(
                "no complete finite or parameterized piecewise-affine cover on the sample window"
            ),
            evidence=evidence,
            recommended_next_attacks=("closure", "functional"),
        )


def branch_metrics(
    census: PiecewiseAffineCensus,
    expected: Sequence[tuple[int, int, int]],
) -> dict[str, float | int | str]:
    """Attack-validation scores. Not mathematical claims about the target."""
    discovered = {(item.p, item.q, item.r) for item in census.branches if item.status == BranchEvidenceStatus.SUPPORTED_BY_SAMPLES.value}
    true = set(expected)
    if census.family is not None:
        family_hit = (census.family.p, 1, census.family.r) in true or any(
            item[0] == census.family.p and item[2] == census.family.r for item in true
        )
        return {
            "census_kind": census.census_kind,
            "branch_recall": 1.0 if family_hit else 0.0,
            "branch_precision": 1.0 if family_hit else 0.0,
            "coverage": census.coverage,
            "false_branch_rate": 0.0,
            "region_precision": 1.0 if census.family.region is not None else 0.0,
        }
    recall = (len(discovered & true) / len(true)) if true else 1.0
    precision = (len(discovered & true) / len(discovered)) if discovered else 0.0
    false_rate = 1.0 - precision if discovered else 0.0
    region_hits = 0
    for branch in census.branches:
        if branch.region is not None and branch.region.kind != RegionKind.UNKNOWN.value:
            region_hits += 1
    region_precision = (region_hits / len(census.branches)) if census.branches else 0.0
    return {
        "census_kind": census.census_kind,
        "branch_recall": recall,
        "branch_precision": precision,
        "coverage": census.coverage,
        "false_branch_rate": false_rate,
        "region_precision": region_precision,
    }
