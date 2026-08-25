"""Optional raw-contribution map and exact factorization check.

``F(s,c)=F̄(s,h(c))`` is a verified property when it holds, never an
assumption. Specs without ``raw_contribution`` are inapplicable.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any, Hashable, Protocol, runtime_checkable

from research_engine.core.observation import has_output, observe
from research_engine.core.problem_spec import ProblemSpec


@runtime_checkable
class ContributingSpec(Protocol):
    def raw_contribution(self, control: Any) -> Hashable:
        """Exact raw contribution of one control letter."""


class FactorizationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    REFUTED = "REFUTED"
    INAPPLICABLE = "INAPPLICABLE"


@dataclass(frozen=True)
class FactorizationResult:
    status: FactorizationStatus
    control_count: int
    contribution_count: int | None
    contributions: tuple[Hashable, ...] | None = None
    witness: tuple[Any, ...] | None = None
    claim: str = ""


def has_raw_contribution(spec: object) -> bool:
    return callable(getattr(spec, "raw_contribution", None))


def raw_image(spec: object, controls: Sequence[Any]) -> frozenset[Hashable]:
    if not has_raw_contribution(spec):
        raise TypeError(f"{type(spec).__name__} has no raw_contribution map")
    return frozenset(spec.raw_contribution(control) for control in controls)


def _stable_items(items: Iterable[Any]) -> tuple[Any, ...]:
    sequence = tuple(items)
    try:
        return tuple(sorted(sequence))
    except TypeError:
        return tuple(sorted(sequence, key=repr))


def check_control_factorization(
    spec: ProblemSpec,
    states: Sequence[Any] | None = None,
    controls: Sequence[Any] | None = None,
    phase: Any | None = None,
) -> FactorizationResult:
    """If ``h(c)=h(c')`` then transition and observation agree on ``states``."""
    if not has_raw_contribution(spec):
        return FactorizationResult(
            status=FactorizationStatus.INAPPLICABLE,
            control_count=0,
            contribution_count=None,
            claim="no raw_contribution map",
        )
    frozen_phase = phase if phase is not None else spec.initial_phase()
    if controls is None:
        start = spec.canonicalize(spec.initial_state)
        controls = spec.legal_controls(start, frozen_phase)
    letters = _stable_items(controls)
    if states is None:
        probed = (spec.canonicalize(spec.initial_state),)
    else:
        probed = tuple(spec.canonicalize(state) for state in states)
    fibers: dict[Hashable, list[Any]] = {}
    for control in letters:
        key = spec.raw_contribution(control)
        fibers.setdefault(key, []).append(control)
    contributions = _stable_items(fibers)
    observe_enabled = has_output(spec)
    for state in probed:
        for _key, group in fibers.items():
            reference = group[0]
            ref_next = spec.canonicalize(spec.transition(state, reference, frozen_phase))
            ref_out = observe(spec, state, reference, frozen_phase) if observe_enabled else None
            for other in group[1:]:
                nxt = spec.canonicalize(spec.transition(state, other, frozen_phase))
                out = observe(spec, state, other, frozen_phase) if observe_enabled else None
                if nxt != ref_next or out != ref_out:
                    return FactorizationResult(
                        status=FactorizationStatus.REFUTED,
                        control_count=len(letters),
                        contribution_count=len(contributions),
                        contributions=contributions,
                        witness=(state, reference, other, _key),
                        claim="transition or observation distinguishes equal raw contributions",
                    )
    return FactorizationResult(
        status=FactorizationStatus.VERIFIED,
        control_count=len(letters),
        contribution_count=len(contributions),
        contributions=contributions,
        claim=(
            f"transition and observation factor through {len(contributions)} "
            f"raw contributions from {len(letters)} controls"
        ),
    )
