"""Optional observation map for a ``ProblemSpec``.

Observation is not part of the required protocol. Specs without
``output`` stay valid; attacks that need it return inapplicable.
"""

from __future__ import annotations

from typing import Any, Hashable, Protocol, runtime_checkable


def _phase_key(phase: Any) -> Any:
    return getattr(phase, "value", phase)


@runtime_checkable
class ObservableSpec(Protocol):
    """Mealy-style output. The value must be hashable and exactly comparable."""

    def output(self, state: Any, control: Any, phase: Any) -> Hashable:
        """Deterministic observation of one transition."""


def has_output(spec: object) -> bool:
    return callable(getattr(spec, "output", None))


def observe(spec: object, state: Any, control: Any, phase: Any) -> Hashable:
    """Call ``output(state, control, phase)``, falling back to two-argument ``output``."""
    output = getattr(spec, "output", None)
    if not callable(output):
        raise TypeError(f"{type(spec).__name__} has no output map")
    try:
        return output(state, control, phase)
    except TypeError:
        return output(state, control)


class ObservationCache:
    """Memoize observations for a frozen spec. Unsafe if ``output`` is not pure."""

    def __init__(self, spec: object) -> None:
        self._spec = spec
        self._cache: dict[tuple[Any, Any, Any], Hashable] = {}

    def __call__(self, state: Any, control: Any, phase: Any) -> Hashable:
        key = (state, control, _phase_key(phase))
        if key not in self._cache:
            self._cache[key] = observe(self._spec, state, control, phase)
        return self._cache[key]
