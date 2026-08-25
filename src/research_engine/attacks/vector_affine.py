"""Vector-affine census from exact I/O. A fitted matrix is not a Z-theorem."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from typing import Any

from research_engine.algebra.lattices import (
    adjugate,
    integer_affine_preimage,
    matrix_det,
    subtract_vectors,
    vector_gcd,
)
from research_engine.attacks.result import AttackContext, AttackResult, AttackStatus, inapplicable
from research_engine.core.affine_system import (
    add_vectors,
    apply_matrix,
    identity_matrix,
    matrix_dimension,
    multiply_matrices,
    zero_vector,
)
from research_engine.core.problem_spec import ProblemSpec
from research_engine.core.semantics import CertificateKind, ClaimKind, Matrix, SearchScope, State, Vector

MIN_SUPPORT = 3
SAMPLE_RANGE = 8
FALSIFY_RANGE = 12
DIFF_CAP = 12
MIN_DISTINCT_K = 3
PARAM_COVERAGE = 0.55
FINITE_COVERAGE = 0.7
MAX_WORDS = 16
LEAN_COMPOSE = "Problems.Engine.compose_two_vector_affine"
LEAN_CYCLE = "Problems.Engine.cycle_of_vector_affine"
LEAN_OBSTRUCT = "Problems.Engine.vector_cycle_impossible"


def _is_integer_state(state: object) -> bool:
    if not isinstance(state, tuple) or not state:
        return False
    return all(isinstance(part, int) and not isinstance(part, bool) for part in state)


def add_matrix_k(base: Matrix, direction: Matrix, k: int) -> Matrix:
    n = matrix_dimension(base)
    return tuple(
        tuple(base[i][j] + k * direction[i][j] for j in range(n)) for i in range(n)
    )


def subtract_matrices(left: Matrix, right: Matrix) -> Matrix:
    n = matrix_dimension(left)
    if matrix_dimension(right) != n:
        raise ValueError("matrix dimensions must match")
    return tuple(tuple(left[i][j] - right[i][j] for j in range(n)) for i in range(n))


def _v2(n: int) -> int | None:
    if n == 0:
        return None
    value = abs(n)
    k = 0
    while value % 2 == 0:
        value //= 2
        k += 1
    return k


def _eval_vector(spec: ProblemSpec, state: State, phase: object) -> State | None:
    try:
        canonical = spec.canonicalize(state)
    except (TypeError, ValueError):
        return None
    if not _is_integer_state(canonical) or len(canonical) != spec.dimension:
        return None
    try:
        controls = spec.legal_controls(canonical, phase)
    except (TypeError, ValueError):
        return None
    if len(controls) != 1:
        return None
    try:
        nxt = spec.canonicalize(spec.transition(canonical, controls[0], phase))
    except (TypeError, ValueError):
        return None
    if not _is_integer_state(nxt) or len(nxt) != spec.dimension:
        return None
    return tuple(int(part) for part in nxt)


def _grid(dimension: int, bound: int) -> tuple[State, ...]:
    values = tuple(range(-bound, bound + 1))
    if dimension == 1:
        return tuple((int(value),) for value in values)
    return tuple(tuple(int(part) for part in point) for point in product(values, repeat=dimension))


def collect_vector_samples(
    spec: ProblemSpec,
    context: AttackContext,
    bound: int,
) -> dict[State, State]:
    phase = spec.initial_phase()
    samples: dict[State, State] = {}
    for raw in _grid(spec.dimension, bound):
        image = _eval_vector(spec, raw, phase)
        if image is None:
            continue
        samples[tuple(int(part) for part in spec.canonicalize(raw))] = image
    state = spec.canonicalize(spec.initial_state)
    orbit_phase = spec.initial_phase()
    steps = context.max_steps if context.max_steps is not None else 16
    for _ in range(max(0, steps)):
        if not _is_integer_state(state) or len(state) != spec.dimension:
            break
        image = _eval_vector(spec, state, orbit_phase)
        if image is None:
            break
        samples[tuple(int(part) for part in state)] = image
        try:
            controls = spec.legal_controls(state, orbit_phase)
        except (TypeError, ValueError):
            break
        if len(controls) != 1:
            break
        orbit_phase = spec.next_phase(orbit_phase, controls[0])
        state = image
    return samples


def _matrix_from_bases(dxs: Sequence[Vector], dys: Sequence[Vector]) -> Matrix | None:
    d = len(dxs)
    if d < 1 or len(dys) != d:
        return None
    columns_x = tuple(tuple(dxs[j][i] for j in range(d)) for i in range(d))
    columns_y = tuple(tuple(dys[j][i] for j in range(d)) for i in range(d))
    det = matrix_det(columns_x)
    if det == 0:
        return None
    prod = multiply_matrices(columns_y, adjugate(columns_x))
    rows: list[tuple[int, ...]] = []
    for i in range(d):
        row: list[int] = []
        for j in range(d):
            if prod[i][j] % det != 0:
                return None
            row.append(prod[i][j] // det)
        rows.append(tuple(row))
    return tuple(rows)


def _holds(matrix: Matrix, offset: Vector, src: Vector, dst: Vector) -> bool:
    return add_vectors(apply_matrix(matrix, src), offset) == dst


def _fit_affine(points: Sequence[tuple[Vector, Vector]]) -> tuple[Matrix, Vector] | None:
    if len(points) < MIN_SUPPORT:
        return None
    dimension = len(points[0][0])
    diffs: list[tuple[Vector, Vector]] = []
    origin, origin_image = points[0]
    for src, dst in points[1:]:
        dx = subtract_vectors(src, origin)
        dy = subtract_vectors(dst, origin_image)
        if any(dx):
            diffs.append((dx, dy))
    if len(diffs) < dimension:
        return None
    for chosen in combinations(diffs, dimension):
        matrix = _matrix_from_bases(
            tuple(item[0] for item in chosen),
            tuple(item[1] for item in chosen),
        )
        if matrix is None:
            continue
        offset = subtract_vectors(origin_image, apply_matrix(matrix, origin))
        if all(_holds(matrix, offset, src, dst) for src, dst in points):
            return matrix, offset
    return None


@dataclass(frozen=True)
class VectorAffineBranch:
    matrix: Matrix
    offset: Vector
    support: tuple[State, ...]
    counterexamples: tuple[State, ...] = ()
    status: str = "UNDERDETERMINED"
    region: Mapping[str, Any] | None = None
    parameter: int | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "matrix": self.matrix,
            "offset": self.offset,
            "support": self.support,
            "counterexamples": self.counterexamples,
            "status": self.status,
            "region": None if self.region is None else dict(self.region),
            "parameter": self.parameter,
        }


@dataclass(frozen=True)
class VectorAffineFamily:
    base: Matrix
    direction: Matrix
    offset: Vector
    observed_k: tuple[int, ...]
    support: tuple[State, ...]
    status: str
    region: Mapping[str, Any] | None = None

    def matrix_at(self, k: int) -> Matrix:
        return add_matrix_k(self.base, self.direction, k)

    def as_dict(self) -> dict[str, Any]:
        return {
            "base": self.base,
            "direction": self.direction,
            "offset": self.offset,
            "observed_k": self.observed_k,
            "support": self.support,
            "status": self.status,
            "region": None if self.region is None else dict(self.region),
        }


@dataclass(frozen=True)
class VectorAffineCensus:
    branches: tuple[VectorAffineBranch, ...]
    family: VectorAffineFamily | None
    census_kind: str
    coverage: float
    sample_count: int
    unresolved: tuple[State, ...]
    relations: tuple[Mapping[str, Any], ...]
    certificates: tuple[Mapping[str, Any], ...]
    domains: tuple[Mapping[str, Any], ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "census_kind": self.census_kind,
            "coverage": self.coverage,
            "sample_count": self.sample_count,
            "branch_count": len(self.branches),
            "unresolved": self.unresolved,
            "branches": tuple(item.as_dict() for item in self.branches),
            "family": None if self.family is None else self.family.as_dict(),
            "relations": self.relations,
            "certificates": self.certificates,
            "domains": self.domains,
            "reconstructed_affine": None,
        }


def _generator_points(keys: Sequence[State]) -> tuple[State, ...]:
    box = tuple(point for point in keys if all(abs(part) <= 4 for part in point))
    step = max(1, len(keys) // 20)
    spread = tuple(keys[index] for index in range(0, len(keys), step))
    return tuple(dict.fromkeys(box + spread))


def _candidate_maps(samples: Mapping[State, State]) -> dict[tuple[Matrix, Vector], tuple[State, ...]]:
    keys = tuple(samples)
    found: dict[tuple[Matrix, Vector], tuple[State, ...]] = {}
    if len(keys) < MIN_SUPPORT:
        return found
    generators = _generator_points(keys)
    for index, origin in enumerate(generators):
        others = generators[index + 1 :] + generators[:index]
        stride = max(1, len(others) // 12)
        sampled = tuple(others[pos] for pos in range(0, len(others), stride))[:12]
        for first, second in combinations(sampled, 2):
            fitted = _fit_affine(
                (
                    (origin, samples[origin]),
                    (first, samples[first]),
                    (second, samples[second]),
                )
            )
            if fitted is None:
                continue
            matrix, offset = fitted
            support = tuple(
                point for point in keys if _holds(matrix, offset, point, samples[point])
            )
            if len(support) < MIN_SUPPORT:
                continue
            key = (matrix, offset)
            previous = found.get(key)
            if previous is None or len(support) > len(previous):
                found[key] = support
    return found


def _all_candidate_branches(
    samples: Mapping[State, State],
    falsify: Mapping[State, State],
) -> tuple[VectorAffineBranch, ...]:
    branches: list[VectorAffineBranch] = []
    for (matrix, offset), support in _candidate_maps(samples).items():
        counters = tuple(
            point
            for point, image in falsify.items()
            if not _holds(matrix, offset, point, image)
        )
        status = "EXACTLY_CERTIFIED" if not counters else "SUPPORTED_BY_SAMPLES"
        branches.append(
            VectorAffineBranch(
                matrix=matrix,
                offset=offset,
                support=support,
                counterexamples=counters,
                status=status,
            )
        )
    branches.sort(key=lambda item: (-len(item.support), item.matrix, item.offset))
    return tuple(branches)


def _cluster_branches(
    samples: Mapping[State, State],
    falsify: Mapping[State, State],
) -> tuple[VectorAffineBranch, ...]:
    candidates = _candidate_maps(samples)
    ranked = sorted(candidates.items(), key=lambda item: (-len(item[1]), item[0][0], item[0][1]))
    remaining = set(samples)
    branches: list[VectorAffineBranch] = []
    for (matrix, offset), support in ranked:
        live = tuple(point for point in support if point in remaining)
        if len(live) < MIN_SUPPORT:
            continue
        counters = tuple(
            point
            for point, image in falsify.items()
            if not _holds(matrix, offset, point, image)
        )
        status = "EXACTLY_CERTIFIED" if not counters else "SUPPORTED_BY_SAMPLES"
        branches.append(
            VectorAffineBranch(
                matrix=matrix,
                offset=offset,
                support=live,
                counterexamples=counters,
                status=status,
            )
        )
        remaining.difference_update(live)
        if len(remaining) < MIN_SUPPORT:
            break
    return tuple(branches)


def _scalar_multiple(delta: Matrix, direction: Matrix) -> int | None:
    n = matrix_dimension(direction)
    k = None
    for i in range(n):
        for j in range(n):
            step = direction[i][j]
            left = delta[i][j]
            if step == 0:
                if left != 0:
                    return None
                continue
            if left % step != 0:
                return None
            value = left // step
            if k is None:
                k = value
            elif k != value:
                return None
    return 0 if k is None else k


def _parameter_family(branches: Sequence[VectorAffineBranch]) -> VectorAffineFamily | None:
    """Form A_k = A0 + k D only from large-support branches.

    Tiny accidental fits must not define the family direction.
    """
    if not branches:
        return None
    ranked = sorted(branches, key=lambda item: (-len(item.support), item.matrix, item.offset))
    largest = len(ranked[0].support)
    floor = max(MIN_SUPPORT, largest // 4)
    live = [item for item in ranked if len(item.support) >= floor]
    if len(live) < MIN_DISTINCT_K:
        return None
    # Prefer the offset of the heaviest branches, not the most frequent tiny ones.
    offset_weight: dict[Vector, int] = {}
    for item in live:
        offset_weight[item.offset] = offset_weight.get(item.offset, 0) + len(item.support)
    offset = max(offset_weight, key=lambda item: (offset_weight[item], item))
    live = [item for item in live if item.offset == offset]
    distinct: list[Matrix] = []
    support_of: dict[Matrix, int] = {}
    for item in live:
        support_of[item.matrix] = max(support_of.get(item.matrix, 0), len(item.support))
        if item.matrix not in distinct:
            distinct.append(item.matrix)
    if len(distinct) < MIN_DISTINCT_K:
        return None
    best: tuple[Matrix, Matrix, dict[Matrix, int], int] | None = None
    for index, base in enumerate(distinct):
        for other in distinct[index + 1 :]:
            delta = subtract_matrices(other, base)
            g = vector_gcd([entry for row in delta for entry in row])
            if g == 0:
                continue
            direction = tuple(tuple(entry // g for entry in row) for row in delta)
            if not any(entry for row in direction for entry in row):
                continue
            ks: dict[Matrix, int] = {}
            for matrix in distinct:
                multiple = _scalar_multiple(subtract_matrices(matrix, base), direction)
                if multiple is None:
                    continue
                ks[matrix] = multiple
            if len(ks) < MIN_DISTINCT_K:
                continue
            weight = sum(support_of[matrix] for matrix in ks)
            if best is None or weight > best[3] or (weight == best[3] and len(ks) > len(best[2])):
                best = (base, direction, ks, weight)
    if best is None:
        return None
    base, direction, ks, _weight = best
    observed = tuple(sorted(set(ks.values())))
    if len(observed) < MIN_DISTINCT_K:
        return None
    members = {item.matrix for item in live if item.matrix in ks}
    support = tuple(point for item in live if item.matrix in members for point in item.support)
    return VectorAffineFamily(
        base=base,
        direction=direction,
        offset=offset,
        observed_k=observed,
        support=support,
        status="SUPPORTED_BY_SAMPLES",
    )


def _k_from_family(family: VectorAffineFamily, src: Vector, dst: Vector) -> int | None:
    delta = subtract_vectors(dst, add_vectors(apply_matrix(family.base, src), family.offset))
    step = apply_matrix(family.direction, src)
    if not any(step):
        return None
    k = None
    for left, right in zip(delta, step, strict=True):
        if right == 0:
            if left != 0:
                return None
            continue
        if left % right != 0:
            return None
        value = left // right
        if k is None:
            k = value
        elif k != value:
            return None
    return k


def _family_pairs(
    family: VectorAffineFamily,
    samples: Mapping[State, State],
) -> list[tuple[State, int]]:
    pairs: list[tuple[State, int]] = []
    for src, dst in samples.items():
        k = _k_from_family(family, src, dst)
        if k is None:
            continue
        if _holds(family.matrix_at(k), family.offset, src, dst):
            pairs.append((src, k))
    return pairs


def _infer_region(
    family: VectorAffineFamily | None,
    branches: Sequence[VectorAffineBranch],
    samples: Mapping[State, State],
) -> Mapping[str, Any] | None:
    if family is not None:
        pairs = _family_pairs(family, samples)
        if len({k for _, k in pairs}) < MIN_DISTINCT_K:
            return None
        valuation = _valuation_region(pairs)
        if valuation is not None:
            return valuation
        quotient = _quotient_region(pairs)
        if quotient is not None:
            return quotient
        return {"kind": "latent_parameter", "observed_k": family.observed_k}
    if len(branches) >= 2:
        residues = _residue_region(branches)
        if residues is not None:
            return residues
    return None


def _valuation_region(pairs: Sequence[tuple[State, int]]) -> dict[str, Any] | None:
    dimension = len(pairs[0][0])
    for index in range(dimension):
        for shift in (0, 1, -1):
            offsets: set[int] = set()
            ok = True
            for src, k in pairs:
                observed = _v2(src[index] + shift)
                if observed is None:
                    continue
                offsets.add(k - observed)
            if ok and len(offsets) == 1:
                return {
                    "kind": "valuation",
                    "coordinate": index,
                    "shift": shift,
                    "base": 2,
                    "k_offset": next(iter(offsets)),
                    "direction": "EXACT",
                }
            offsets = set()
            ok = True
            for src, k in pairs:
                observed = _v2(abs(src[index]) + shift)
                if observed is None:
                    continue
                offsets.add(k - observed)
            if ok and len(offsets) == 1:
                return {
                    "kind": "valuation",
                    "coordinate": index,
                    "shift": shift,
                    "base": 2,
                    "abs": True,
                    "k_offset": next(iter(offsets)),
                    "direction": "EXACT",
                }
    if dimension >= 2:
        offsets = set()
        ok = True
        for src, k in pairs:
            observed = _v2(src[0] - src[1])
            if observed is None:
                observed = 0
            offsets.add(k - observed)
        if ok and len(offsets) == 1:
            return {
                "kind": "valuation",
                "form": "x0-x1",
                "base": 2,
                "k_offset": next(iter(offsets)) if offsets else 0,
                "direction": "EXACT",
            }
    return None


def _quotient_region(pairs: Sequence[tuple[State, int]]) -> dict[str, Any] | None:
    dimension = len(pairs[0][0])
    for num in range(dimension):
        for den in range(dimension):
            if num == den:
                continue
            for scale in (1, -1):
                offsets: set[int] = set()
                ok = True
                for src, k in pairs:
                    divisor = src[den]
                    if divisor == 0:
                        continue
                    offsets.add(k - scale * (src[num] // divisor))
                if ok and len(offsets) == 1:
                    return {
                        "kind": "quotient",
                        "numerator": num,
                        "denominator": den,
                        "k_scale": scale,
                        "k_offset": next(iter(offsets)),
                        "direction": "EXACT",
                    }
    return None


def _majority_residue(values: Sequence[int], threshold: float = 0.9) -> int | None:
    if not values:
        return None
    counts: dict[int, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    residue, count = max(counts.items(), key=lambda item: item[1])
    if count / len(values) >= threshold:
        return residue
    return None


def _residue_region(branches: Sequence[VectorAffineBranch]) -> dict[str, Any] | None:
    live = [item for item in branches if len(item.support) >= MIN_SUPPORT]
    live = sorted(live, key=lambda item: -len(item.support))
    if len(live) < 2:
        return None
    subsets = [live]
    if len(live) > 2:
        subsets.append(live[:2])
    dimension = len(live[0].support[0])
    for group in subsets:
        for modulus in range(2, 9):
            for index in range(dimension):
                mapping: dict[int, Matrix] = {}
                ok = True
                for branch in group:
                    residue = _majority_residue(tuple(point[index] % modulus for point in branch.support))
                    if residue is None:
                        ok = False
                        break
                    if residue in mapping and mapping[residue] != branch.matrix:
                        ok = False
                        break
                    mapping[residue] = branch.matrix
                if ok and len(mapping) == len(group):
                    return {
                        "kind": "congruence",
                        "coordinate": index,
                        "modulus": modulus,
                        "direction": "EXACT",
                    }
            if dimension >= 2:
                mapping = {}
                ok = True
                for branch in group:
                    residue = _majority_residue(
                        tuple((point[0] + point[1]) % modulus for point in branch.support)
                    )
                    if residue is None:
                        ok = False
                        break
                    if residue in mapping and mapping[residue] != branch.matrix:
                        ok = False
                        break
                    mapping[residue] = branch.matrix
                if ok and len(mapping) == len(group):
                    return {
                        "kind": "congruence",
                        "form": "x0+x1",
                        "modulus": modulus,
                        "direction": "EXACT",
                    }
    return None


def _predicate_k(region: Mapping[str, Any], src: State) -> int | None:
    kind = region.get("kind")
    k_offset = int(region.get("k_offset") or 0)
    if kind == "valuation":
        if region.get("form") == "x0-x1":
            observed = _v2(src[0] - src[1])
            return k_offset if observed is None else observed + k_offset
        index = int(region.get("coordinate") or 0)
        shift = int(region.get("shift") or 0)
        value = abs(src[index]) + shift if region.get("abs") else src[index] + shift
        observed = _v2(value)
        if observed is None:
            return None
        return observed + k_offset
    if kind == "quotient":
        den = src[int(region["denominator"])]
        if den == 0:
            return None
        scale = int(region.get("k_scale") or 1)
        return scale * (src[int(region["numerator"])] // den) + k_offset
    return None


def _certify_domain(
    region: Mapping[str, Any] | None,
    family: VectorAffineFamily | None,
    branches: Sequence[VectorAffineBranch],
    falsify: Mapping[State, State],
) -> tuple[Mapping[str, Any], ...]:
    if region is None:
        return ()
    if family is not None and region.get("kind") in {"valuation", "quotient"}:
        necessary = True
        sufficient = True
        for src, dst in falsify.items():
            predicted = _predicate_k(region, src)
            actual = _k_from_family(family, src, dst)
            if predicted is not None and not _holds(
                family.matrix_at(predicted), family.offset, src, dst
            ):
                sufficient = False
            if actual is None:
                continue
            if predicted != actual:
                necessary = False
        if sufficient and necessary:
            direction = "EXACT"
        elif sufficient:
            direction = "SUFFICIENT_ONLY"
        elif necessary:
            direction = "NECESSARY_ONLY"
        else:
            direction = "NONE"
        return (
            {
                "direction": direction,
                "evidence": "COUNTEREXAMPLE_SURVIVED" if direction == "EXACT" else "SAMPLE_WINDOW",
                "domain": dict(region),
            },
        )
    if region.get("kind") == "congruence":
        return (
            {
                "direction": "EXACT" if region.get("direction") == "EXACT" else "NONE",
                "evidence": "COUNTEREXAMPLE_SURVIVED",
                "domain": dict(region),
            },
        )
    del branches
    return (
        {
            "direction": "NECESSARY_ONLY",
            "evidence": "SAMPLE_WINDOW",
            "domain": dict(region),
        },
    )


def compose_vector_steps(steps: Sequence[tuple[Matrix, Vector]]) -> tuple[Matrix, Vector]:
    if not steps:
        raise ValueError("steps must be nonempty")
    dimension = matrix_dimension(steps[0][0])
    matrix = identity_matrix(dimension)
    offset = zero_vector(dimension)
    for item_matrix, item_offset in steps:
        offset = add_vectors(apply_matrix(item_matrix, offset), item_offset)
        matrix = multiply_matrices(item_matrix, matrix)
    return matrix, offset


def cycle_matrix_constraint(matrix: Matrix, offset: Vector) -> tuple[Matrix, Vector]:
    dimension = matrix_dimension(matrix)
    return subtract_matrices(matrix, identity_matrix(dimension)), tuple(-part for part in offset)


def _inconsistent_over_q(matrix: Matrix, rhs: Vector) -> bool:
    n = matrix_dimension(matrix)
    aug = [
        [Fraction(matrix[i][j]) for j in range(n)] + [Fraction(rhs[i])]
        for i in range(n)
    ]
    row = 0
    for col in range(n):
        pivot = next((i for i in range(row, n) if aug[i][col] != 0), None)
        if pivot is None:
            continue
        aug[row], aug[pivot] = aug[pivot], aug[row]
        scale = aug[row][col]
        aug[row] = [value / scale for value in aug[row]]
        for i in range(n):
            if i == row:
                continue
            factor = aug[i][col]
            aug[i] = [left - factor * right for left, right in zip(aug[i], aug[row], strict=True)]
        row += 1
    return any(all(row[j] == 0 for j in range(n)) and row[n] != 0 for row in aug)


def linear_system_status(matrix: Matrix, rhs: Vector) -> str:
    det = matrix_det(matrix)
    n = matrix_dimension(matrix)
    if det != 0:
        solution = integer_affine_preimage(matrix, zero_vector(n), rhs)
        if solution is None:
            return "UNIQUE_NONINTEGRAL"
        return "UNIQUE_INTEGER"
    if _inconsistent_over_q(matrix, rhs):
        return "INCONSISTENT"
    return "UNDERDETERMINED"


def _compose_and_obstruct(
    family: VectorAffineFamily | None,
    branches: Sequence[VectorAffineBranch],
) -> tuple[tuple[Mapping[str, Any], ...], tuple[Mapping[str, Any], ...]]:
    relations: list[dict[str, Any]] = []
    certificates: list[dict[str, Any]] = []
    if family is not None:
        ks = family.observed_k[:4]
        words = [(k,) for k in ks] + [(a, b) for a in ks[:3] for b in ks[:3]]
        length_one_blocked = True
        observed_len1 = 0
        for word in words[:MAX_WORDS]:
            steps = [(family.matrix_at(k), family.offset) for k in word]
            composed, translation = compose_vector_steps(steps)
            relations.append(
                {
                    "word": word,
                    "matrix": composed,
                    "offset": translation,
                    "evidence": "ALGEBRAICALLY_COMPOSED",
                    "lean": LEAN_COMPOSE,
                }
            )
            left, rhs = cycle_matrix_constraint(composed, translation)
            status = linear_system_status(left, rhs)
            if status in {"UNIQUE_NONINTEGRAL", "INCONSISTENT"}:
                certificates.append(
                    {
                        "scope": "WORD",
                        "kind": "determinant" if status == "UNIQUE_NONINTEGRAL" else "inconsistent",
                        "word": word,
                        "det": matrix_det(left),
                        "status": "PROVED",
                        "lean": LEAN_OBSTRUCT if status == "UNIQUE_NONINTEGRAL" else LEAN_CYCLE,
                    }
                )
            elif len(word) == 1:
                length_one_blocked = False
            if len(word) == 1:
                observed_len1 += 1
                if status not in {"UNIQUE_NONINTEGRAL", "INCONSISTENT"}:
                    length_one_blocked = False
        if length_one_blocked and observed_len1 >= 1 and certificates:
            certificates.append(
                {
                    "scope": "CLASS",
                    "kind": "linear_system",
                    "status": "PROVED",
                    "observed_k": family.observed_k,
                    "lean": LEAN_CYCLE,
                }
            )
        return tuple(relations), tuple(certificates)
    live = [item for item in branches if item.status != "REFUTED"][:4]
    if not live:
        live = list(branches[:4])
    for left, right in list(product(live, live))[:MAX_WORDS]:
        composed, translation = compose_vector_steps(
            ((left.matrix, left.offset), (right.matrix, right.offset))
        )
        relations.append(
            {
                "word": (left.matrix, right.matrix),
                "matrix": composed,
                "offset": translation,
                "evidence": "ALGEBRAICALLY_COMPOSED",
                "lean": LEAN_COMPOSE,
            }
        )
        constraint, rhs = cycle_matrix_constraint(composed, translation)
        status = linear_system_status(constraint, rhs)
        if status in {"UNIQUE_NONINTEGRAL", "INCONSISTENT"}:
            certificates.append(
                {
                    "scope": "WORD",
                    "kind": "determinant" if status == "UNIQUE_NONINTEGRAL" else "inconsistent",
                    "det": matrix_det(constraint),
                    "status": "PROVED",
                    "lean": LEAN_OBSTRUCT if status == "UNIQUE_NONINTEGRAL" else LEAN_CYCLE,
                }
            )
    return tuple(relations), tuple(certificates)


def _reclassify_branches(
    branches: Sequence[VectorAffineBranch],
    region: Mapping[str, Any] | None,
    falsify: Mapping[State, State],
) -> tuple[VectorAffineBranch, ...]:
    if region is None:
        return tuple(branches)
    out: list[VectorAffineBranch] = []
    for branch in branches:
        if region.get("kind") == "congruence":
            counters = []
            for point, image in falsify.items():
                if not _point_in_congruence(region, point, branch):
                    continue
                if not _holds(branch.matrix, branch.offset, point, image):
                    counters.append(point)
            status = "EXACTLY_CERTIFIED" if not counters else "SUPPORTED_BY_SAMPLES"
            out.append(
                VectorAffineBranch(
                    matrix=branch.matrix,
                    offset=branch.offset,
                    support=branch.support,
                    counterexamples=tuple(counters),
                    status=status,
                    region=region,
                    parameter=branch.parameter,
                )
            )
            continue
        out.append(branch)
    return tuple(out)


def _point_in_congruence(region: Mapping[str, Any], point: State, branch: VectorAffineBranch) -> bool:
    modulus = int(region.get("modulus") or 2)
    if region.get("form") == "x0+x1":
        residue = (point[0] + point[1]) % modulus
        support_res = {(item[0] + item[1]) % modulus for item in branch.support}
        return residue in support_res
    index = int(region.get("coordinate") or 0)
    residue = point[index] % modulus
    support_res = {item[index] % modulus for item in branch.support}
    return residue in support_res


def run_vector_affine_census(spec: ProblemSpec, context: AttackContext) -> VectorAffineCensus:
    samples = collect_vector_samples(spec, context, SAMPLE_RANGE)
    falsify = collect_vector_samples(spec, context, FALSIFY_RANGE)
    candidate_branches = _all_candidate_branches(samples, falsify)
    family = _parameter_family(candidate_branches)
    branches = _cluster_branches(samples, falsify)
    if family is not None:
        pairs = _family_pairs(family, samples)
        support = tuple(src for src, _ in pairs)
        observed = tuple(sorted({k for _, k in pairs}))
        family = VectorAffineFamily(
            base=family.base,
            direction=family.direction,
            offset=family.offset,
            observed_k=observed,
            support=support,
            status=family.status,
        )
        covered = set(family.support)
        kind = "PARAMETERIZED_CENSUS"
        coverage = (len(covered) / len(samples)) if samples else 0.0
        if coverage < PARAM_COVERAGE or len(family.observed_k) < MIN_DISTINCT_K:
            family = None
    if family is None:
        covered = {point for item in branches for point in item.support}
        coverage = (len(covered) / len(samples)) if samples else 0.0
        kind = "FINITE_CENSUS" if branches and coverage >= FINITE_COVERAGE else "UNRESOLVED"
    # Infer region only after the family decision, so a discarded spurious
    # family cannot leave a latent_parameter residue on a finite census.
    region = _infer_region(family, branches, samples)
    if family is not None:
        family = VectorAffineFamily(
            base=family.base,
            direction=family.direction,
            offset=family.offset,
            observed_k=family.observed_k,
            support=family.support,
            status=family.status,
            region=region,
        )
    if family is None:
        branches = _reclassify_branches(branches, region, falsify)
    domains = _certify_domain(region, family, branches, falsify)
    relations, certificates = _compose_and_obstruct(family, branches)
    unresolved = tuple(point for point in samples if point not in covered) if samples else ()
    return VectorAffineCensus(
        branches=branches,
        family=family,
        census_kind=kind,
        coverage=coverage,
        sample_count=len(samples),
        unresolved=unresolved,
        relations=relations,
        certificates=certificates,
        domains=domains,
    )


def _vector_singleton(spec: ProblemSpec, context: AttackContext) -> bool:
    if spec.dimension < 2 or context.affine is not None:
        return False
    try:
        start = spec.canonicalize(spec.initial_state)
    except (TypeError, ValueError):
        return False
    if not _is_integer_state(start) or len(start) != spec.dimension:
        return False
    try:
        controls = spec.legal_controls(start, spec.initial_phase())
    except (TypeError, ValueError):
        return False
    return len(controls) == 1


class VectorAffineCensusAttack:
    """Recover latent y = A_u x + b_u. Does not install AffineSystem on the spec."""

    name = "vector_affine"

    def applicable(self, spec: ProblemSpec, context: AttackContext) -> bool:
        return _vector_singleton(spec, context)

    def run(self, spec: ProblemSpec, context: AttackContext) -> AttackResult:
        if not _vector_singleton(spec, context):
            return inapplicable(
                self.name,
                "vector-affine census needs dimension>=2 singleton control without AffineSystem",
                ClaimKind.REACHABLE,
            )
        census = run_vector_affine_census(spec, context)
        evidence = census.as_dict()
        if census.census_kind == "PARAMETERIZED_CENSUS" and census.family is not None:
            return AttackResult(
                name=self.name,
                status=AttackStatus.OBSERVATION,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim=(
                    "sample-supported parameterized vector family A_k = A0 + k D; "
                    "window agreement is not a global branch theorem"
                ),
                evidence=evidence,
                certificate_kind=CertificateKind.BOUNDED_RECONNAISSANCE,
            )
        if census.census_kind == "FINITE_CENSUS" and census.branches:
            return AttackResult(
                name=self.name,
                status=AttackStatus.OBSERVATION,
                kind=ClaimKind.REACHABLE,
                scope=SearchScope.BOUNDED,
                claim=(
                    f"sample-supported finite vector-affine census with {len(census.branches)} "
                    "branches; window agreement is not a Z-theorem"
                ),
                evidence=evidence,
            )
        return AttackResult(
            name=self.name,
            status=AttackStatus.INCONCLUSIVE,
            kind=ClaimKind.REACHABLE,
            scope=SearchScope.BOUNDED,
            claim="vector-affine census unresolved on the stated window",
            evidence=evidence,
        )
