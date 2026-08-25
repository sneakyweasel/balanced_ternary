"""Comparable complexity fields. Unsupported fields stay unset."""

from __future__ import annotations

from dataclasses import dataclass

from research_engine.attacks.result import AttackStatus
from research_engine.core.semantics import CertificateKind, SearchScope


@dataclass(frozen=True)
class ComplexityProfile:
    control_count: int | None = None
    raw_contribution_count: int | None = None
    invariant_state_count: int | None = None
    reachable_state_count: int | None = None
    behavioral_state_count: int | None = None
    minimal_machine_count: int | None = None
    graph_diameter: int | None = None
    max_separation_depth: int | None = None
    symmetry_count: int | None = None
    closure_status: str | None = None

    def populated_fields(self) -> dict[str, int | str]:
        mapping = {
            "control_count": self.control_count,
            "raw_contribution_count": self.raw_contribution_count,
            "invariant_state_count": self.invariant_state_count,
            "reachable_state_count": self.reachable_state_count,
            "behavioral_state_count": self.behavioral_state_count,
            "minimal_machine_count": self.minimal_machine_count,
            "graph_diameter": self.graph_diameter,
            "max_separation_depth": self.max_separation_depth,
            "symmetry_count": self.symmetry_count,
            "closure_status": self.closure_status,
        }
        return {key: value for key, value in mapping.items() if value is not None}

    def format_report(self) -> str:
        labels = (
            ("raw controls", self.control_count),
            ("raw contribution values", self.raw_contribution_count),
            ("raw residual states", self.invariant_state_count),
            ("reachable residual states", self.reachable_state_count),
            ("behavioral states", self.behavioral_state_count),
            ("minimal Mealy states", self.minimal_machine_count),
            ("graph diameter", self.graph_diameter),
            ("max separation depth", self.max_separation_depth),
            ("symmetry count", self.symmetry_count),
            ("closure status", self.closure_status),
        )
        lines = [f"{label}: {value}" for label, value in labels if value is not None]
        return "\n".join(lines)


def closure_status_label(
    *,
    complete: bool | None = None,
    status: AttackStatus | None = None,
    scope: SearchScope | None = None,
    certificate_kind: CertificateKind | None = None,
) -> str | None:
    if certificate_kind is not None:
        return certificate_kind.value
    if complete is True:
        return CertificateKind.EXACT_CLOSURE.value
    if status is AttackStatus.INCONCLUSIVE or complete is False:
        return AttackStatus.INCONCLUSIVE.value
    if scope is not None:
        return scope.value
    return None
