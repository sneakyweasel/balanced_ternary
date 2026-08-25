"""Compare fingerprints by certified fields, not by formula text."""

from __future__ import annotations

from research_engine.diagnosis.types import (
    CORE_DIMENSIONS,
    UNOBSERVED,
    DeltaLevel,
    RegimeFingerprint,
    RegimeSimilarity,
    StructuralDelta,
)


def compare_fingerprints(
    left: RegimeFingerprint,
    right: RegimeFingerprint,
) -> tuple[RegimeSimilarity, StructuralDelta]:
    left_pop = left.populated()
    right_pop = right.populated()
    keys = tuple(sorted(set(left_pop) | set(right_pop)))
    matching: list[str] = []
    differing: list[tuple[str, str, str]] = []
    for key in keys:
        a = left_pop.get(key, UNOBSERVED)
        b = right_pop.get(key, UNOBSERVED)
        if a == b:
            matching.append(key)
        else:
            differing.append((key, a, b))
    score = (len(matching) / len(keys)) if keys else 0.0
    similarity = RegimeSimilarity(
        score=score,
        compared_dimensions=keys,
        matching_dimensions=tuple(matching),
    )
    core_diffs = tuple(item for item in differing if item[0] in CORE_DIMENSIONS)
    gap = 1.0 - score
    if len(core_diffs) >= 2 or gap >= 0.45:
        level = DeltaLevel.HIGH
    elif len(core_diffs) == 1 or gap >= 0.2:
        level = DeltaLevel.MEDIUM
    else:
        level = DeltaLevel.LOW
    delta = StructuralDelta(
        level=level,
        differing_dimensions=tuple(differing),
        similarity=similarity,
    )
    return similarity, delta


def core_match(left: RegimeFingerprint, right: RegimeFingerprint) -> bool:
    a = left.core_key()
    b = right.core_key()
    return a is not None and a == b
