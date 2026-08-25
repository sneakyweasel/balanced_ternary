"""Failure-learning term for ExpectedResearchValue. Default is 1.0."""

from __future__ import annotations

from research_engine.diagnosis.types import CandidateSketch
from research_engine.memory.types import FailureCluster, ImportanceLevel


def _exercises(sketch: CandidateSketch, cluster: FailureCluster) -> bool:
    family = cluster.key[3]
    bottleneck = cluster.key[2]
    claimed = set(sketch.claimed_capabilities)
    if family == "global_reachability" and (
        not claimed or "infinite_reachable_trajectories" in claimed or "latent_vector_affine_control" in claimed
    ):
        fp = sketch.fingerprint
        if fp is None:
            return True
        if fp.eventual_region in {"UNBOUNDED_SAMPLE", "UNOBSERVED"}:
            return True
        if fp.affine_control_type in {"VECTOR", "MATRIX_PARAMETERIZED"}:
            return True
    if family == "deterministic_control" and (
        "branching_controls" in claimed or "nontrivial_control_alphabet" in claimed or not claimed
    ):
        return True
    if family == "latent_affine" and (
        "latent_piecewise_affine_control" in claimed or not claimed
    ):
        fp = sketch.fingerprint
        if fp is not None and fp.piecewise_affine_structure in {"NONE", "UNCERTAIN", "UNOBSERVED"}:
            return True
        if fp is None:
            return True
    if bottleneck == "saturated_finite_contracting_regime":
        return False
    return False


def _reproduces_saturated(sketch: CandidateSketch, cluster: FailureCluster) -> bool:
    if cluster.key[2] != "saturated_finite_contracting_regime":
        return False
    fp = sketch.fingerprint
    if fp is None:
        return False
    return (
        fp.numerical_contraction == "FINITE_CONTRACTING"
        and fp.eventual_region == "FINITE_SEED_CLOSURE"
        and fp.control_structure == "SINGLETON"
    )


def failure_learning_value(
    sketch: CandidateSketch,
    memory: object,
) -> tuple[float, str]:
    """Return (multiplier, note). Absent or empty memory yields (1.0, '')."""

    clusters_fn = getattr(memory, "clusters", None)
    if clusters_fn is None:
        return 1.0, ""
    clusters = tuple(clusters_fn())
    if not clusters:
        return 1.0, ""

    matching: list[FailureCluster] = []
    saturated: list[FailureCluster] = []
    for cluster in clusters:
        if _reproduces_saturated(sketch, cluster):
            saturated.append(cluster)
        elif _exercises(sketch, cluster) and cluster.mathematical_importance is ImportanceLevel.HIGH:
            matching.append(cluster)

    if matching:
        best = max(matching, key=lambda item: item.recurrence_count)
        value = 1.0 + min(1.0, 0.25 * best.recurrence_count)
        note = (
            f"resembles {best.recurrence_count} previous "
            f"{best.key[0]} failures"
        )
        return value, note
    if saturated:
        return 0.5, "likely to reproduce a saturated regime"
    return 1.0, ""
