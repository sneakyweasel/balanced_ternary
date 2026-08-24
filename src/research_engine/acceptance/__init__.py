"""Acceptance package: terminal predicates, live slices, suffix feasibility."""

from research_engine.acceptance.live import (
    filter_terminal,
    forward_live_layers,
    live_from_spec,
    live_intersection,
)
from research_engine.acceptance.suffix import (
    co_live_extensions,
    extension_set,
    is_co_live,
    is_suffix_accepted,
    live_extensions,
)
from research_engine.acceptance.terminal import TerminalSpec

__all__ = [
    "TerminalSpec",
    "co_live_extensions",
    "extension_set",
    "filter_terminal",
    "forward_live_layers",
    "is_co_live",
    "is_suffix_accepted",
    "live_extensions",
    "live_from_spec",
    "live_intersection",
]
