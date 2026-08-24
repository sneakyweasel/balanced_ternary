"""Typed search results. A complete finite-horizon BFS is not an asymptotic theorem."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Generic, Hashable, Mapping, TypeVar

from research_engine.core.semantics import ClaimKind, SearchScope

S = TypeVar("S")
C = TypeVar("C")
P = TypeVar("P")


def _freeze_layer(layer: Mapping[Hashable, frozenset[Any]]) -> Mapping[Hashable, frozenset[Any]]:
    return MappingProxyType({key: frozenset(values) for key, values in dict(layer).items()})


@dataclass(frozen=True)
class DynamicsResult(Generic[S, C, P]):
    """Layered reachability or co-reachability with an explicit scope.

    ``layer`` is an exact-phase (or exact-depth) slice. ``union`` is the
    cumulative set of states, ignoring phase. ``terminal_image`` is the
    accepting/terminal slice. These four objects are not interchangeable.
    """

    kind: ClaimKind
    scope: SearchScope
    complete: bool
    horizon: int | None = None
    configurations: frozenset[tuple[S, P]] = field(default_factory=frozenset)
    layer: Mapping[Hashable, frozenset[S]] = field(default_factory=dict)
    union: frozenset[S] = field(default_factory=frozenset)
    terminal_image: frozenset[S] = field(default_factory=frozenset)
    live_union: frozenset[S] = field(default_factory=frozenset)
    rejected_images: int = 0
    visit_order: tuple[tuple[S, P], ...] = ()
    parents: Mapping[tuple[S, P], tuple[tuple[S, P], C]] = field(default_factory=dict)
    live_start: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "configurations", frozenset(self.configurations))
        object.__setattr__(self, "union", frozenset(self.union))
        object.__setattr__(self, "terminal_image", frozenset(self.terminal_image))
        object.__setattr__(self, "live_union", frozenset(self.live_union))
        object.__setattr__(self, "layer", _freeze_layer(self.layer))
        object.__setattr__(self, "visit_order", tuple(self.visit_order))
        object.__setattr__(self, "parents", MappingProxyType(dict(self.parents)))

    def layer_at(self, key: Hashable) -> frozenset[S]:
        return frozenset(self.layer.get(key, ()))
