"""Synthetic integer-dynamics benchmarks for the experimental engine."""

from research_engine.benchmarks.pipeline import (
    live_infinite_hypothesis,
    load_benchmark,
    reproduce_checks,
    run_all_benchmarks,
    run_benchmark,
)
from research_engine.benchmarks.hidden_piecewise import (
    HiddenCongruenceASpec,
    HiddenNestedCSpec,
    HiddenPowerClearDSpec,
    HiddenSignBSpec,
)
from research_engine.benchmarks.systems import (
    ExpandingEscapeSpec,
    FiniteClosureSpec,
    InfiniteTranslateSpec,
    ModularTripleSpec,
    ResetLoopSpec,
)

__all__ = [
    "ExpandingEscapeSpec",
    "FiniteClosureSpec",
    "HiddenCongruenceASpec",
    "HiddenNestedCSpec",
    "HiddenPowerClearDSpec",
    "HiddenSignBSpec",
    "InfiniteTranslateSpec",
    "ModularTripleSpec",
    "ResetLoopSpec",
    "live_infinite_hypothesis",
    "load_benchmark",
    "reproduce_checks",
    "run_all_benchmarks",
    "run_benchmark",
]
