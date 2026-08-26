"""Region membership, probes, and candidate constructors from a finite sample."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from itertools import product

from research_engine.core.semantics import State
from research_engine.reasoning.types import Region, RegionForm

ORTHANT_GRID = 6
MODULAR_WINDOW = 24
FINITE_SET_CAP = 48
INTERVAL_ENUM_CAP = 256


def _as_ints(state: State) -> tuple[int, ...]:
    return tuple(int(part) for part in state)


def contains(region: Region, state: State) -> bool:
    coords = _as_ints(state)
    params = region.parameters
    if region.form is RegionForm.FINITE_SET:
        members = {tuple(item) for item in params.get("states", ())}
        return coords in members
    if region.form is RegionForm.INTERVAL:
        if len(coords) != 1:
            return False
        return int(params["lo"]) <= coords[0] <= int(params["hi"])
    if region.form is RegionForm.SIGN_ORTHANT:
        sign = str(params.get("sign") or "nonneg")
        if sign == "nonneg":
            return all(value >= 0 for value in coords)
        if sign == "nonpos":
            return all(value <= 0 for value in coords)
        return False
    if region.form is RegionForm.MODULAR_CLASS:
        if len(coords) != 1:
            return False
        modulus = int(params["modulus"])
        residue = int(params["residue"])
        if modulus <= 0:
            return False
        return coords[0] % modulus == residue % modulus
    return False


def probe_states(region: Region, extra: Sequence[State] = ()) -> tuple[State, ...]:
    """Finite probe of S. Exhaustive for small finite/interval regions."""

    found: list[State] = []
    seen: set[State] = set()

    def _add(state: State) -> None:
        coords = _as_ints(state)
        if coords in seen:
            return
        if not contains(region, coords):
            return
        seen.add(coords)
        found.append(coords)

    params = region.parameters
    if region.form is RegionForm.FINITE_SET:
        for item in params.get("states", ()):
            _add(tuple(int(part) for part in item))
    elif region.form is RegionForm.INTERVAL:
        lo, hi = int(params["lo"]), int(params["hi"])
        if hi - lo <= INTERVAL_ENUM_CAP:
            for value in range(lo, hi + 1):
                _add((value,))
        else:
            for value in (lo, hi, (lo + hi) // 2):
                _add((value,))
    elif region.form is RegionForm.SIGN_ORTHANT:
        dim = max(1, region.dimension)
        for combo in product(range(ORTHANT_GRID + 1), repeat=dim):
            coords = combo if str(params.get("sign") or "nonneg") == "nonneg" else tuple(-x for x in combo)
            _add(coords)
        for axis in range(dim):
            point = [0] * dim
            point[axis] = ORTHANT_GRID * 3
            if str(params.get("sign") or "nonneg") == "nonpos":
                point[axis] = -point[axis]
            _add(tuple(point))
    elif region.form is RegionForm.MODULAR_CLASS:
        modulus = int(params["modulus"])
        residue = int(params["residue"])
        for value in range(-MODULAR_WINDOW, MODULAR_WINDOW + 1):
            if value % modulus == residue % modulus:
                _add((value,))
    for state in extra:
        _add(state)
    return tuple(found)


def candidates_from_sample(
    sample: Sequence[State],
    *,
    dimension: int,
    complete: bool,
) -> tuple[Region, ...]:
    """Ordered catalog. Does not invent a region for an empty sample."""

    points = tuple(_as_ints(state) for state in sample)
    if not points:
        return ()
    dim = max(dimension, max(len(item) for item in points))
    found: list[Region] = []

    unique = tuple(dict.fromkeys(points))
    if complete or len(unique) <= FINITE_SET_CAP:
        found.append(
            Region(
                form=RegionForm.FINITE_SET,
                parameters={"states": unique},
                dimension=dim,
            )
        )

    if dim == 1:
        values = tuple(item[0] for item in unique)
        found.append(
            Region(
                form=RegionForm.INTERVAL,
                parameters={"lo": min(values), "hi": max(values)},
                dimension=1,
            )
        )
        if len(unique) >= 3:
            for modulus in range(2, 9):
                residues = {value % modulus for value in values}
                if len(residues) == 1:
                    found.append(
                        Region(
                            form=RegionForm.MODULAR_CLASS,
                            parameters={"modulus": modulus, "residue": next(iter(residues))},
                            dimension=1,
                        )
                    )
                    break

    if unique and all(all(part >= 0 for part in item) for item in unique):
        found.append(
            Region(
                form=RegionForm.SIGN_ORTHANT,
                parameters={"sign": "nonneg"},
                dimension=dim,
            )
        )
    elif unique and all(all(part <= 0 for part in item) for item in unique):
        found.append(
            Region(
                form=RegionForm.SIGN_ORTHANT,
                parameters={"sign": "nonpos"},
                dimension=dim,
            )
        )
    return tuple(found)


def enlarge_finite(region: Region, extra: Iterable[State]) -> Region:
    if region.form is not RegionForm.FINITE_SET:
        return region
    members = list(region.parameters.get("states", ()))
    seen = {tuple(item) for item in members}
    for state in extra:
        coords = _as_ints(state)
        if coords not in seen:
            seen.add(coords)
            members.append(coords)
    return Region(
        form=RegionForm.FINITE_SET,
        parameters={"states": tuple(members)},
        dimension=region.dimension,
    )
