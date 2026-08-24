"""Registry wrapping existing experiment runners. Runners are not rewritten."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class ExperimentSpec:
    id: str
    name: str
    problem: str
    runner: Callable[..., Any]
    notes: str


def _specs() -> tuple[ExperimentSpec, ...]:
    from research.collatz.asymptotic import run_fixed_integer_census
    from research.collatz.experiments.affine_center import run_affine_center_census
    from research.collatz.experiments.bt_warp import run_bt_warp_census
    from research.collatz.experiments.complexity_spectrum import run_complexity_spectrum
    from research.collatz.experiments.cycle_census import run_cycle_census
    from research.collatz.experiments.exhaustive import run_exhaustive_experiment
    from research.collatz.experiments.information_content import run_information_content
    from research.collatz.experiments.near_critical import run_near_critical
    from research.collatz.experiments.suffix_determination import suffix_determination_census

    return (
        ExperimentSpec(
            "collatz.exhaustive",
            "Odd-n feature-transition scan",
            "collatz",
            run_exhaustive_experiment,
            "Existing runner; prefer btlab collatz experiment",
        ),
        ExperimentSpec(
            "collatz.information",
            "Compatibility information-content census",
            "collatz",
            run_information_content,
            "Existing runner; prefer btlab collatz information-test",
        ),
        ExperimentSpec(
            "collatz.near_critical",
            "Near-critical drift census",
            "collatz",
            run_near_critical,
            "Existing runner; prefer btlab collatz near-critical",
        ),
        ExperimentSpec(
            "collatz.affine_center",
            "Affine-center census",
            "collatz",
            run_affine_center_census,
            "Existing runner; prefer btlab collatz affine-center-census",
        ),
        ExperimentSpec(
            "collatz.fixed_integer",
            "Fixed-integer affine-gap census",
            "collatz",
            run_fixed_integer_census,
            "Existing runner; prefer btlab collatz fixed-integer-census",
        ),
        ExperimentSpec(
            "collatz.warp",
            "BT warp commutator census",
            "collatz",
            run_bt_warp_census,
            "Existing runner; prefer btlab collatz warp-census",
        ),
        ExperimentSpec(
            "collatz.cycles",
            "Bounded primitive-cycle census",
            "collatz",
            run_cycle_census,
            "Existing runner; prefer btlab collatz cycle-census",
        ),
        ExperimentSpec(
            "collatz.complexity",
            "/2^k complexity spectrum",
            "collatz",
            run_complexity_spectrum,
            "Existing runner; prefer btlab collatz complexity",
        ),
        ExperimentSpec(
            "collatz.suffix",
            "BT(R) suffix-determination census",
            "collatz",
            suffix_determination_census,
            "Existing runner; prefer btlab collatz suffix-test",
        ),
    )


def list_experiments() -> tuple[ExperimentSpec, ...]:
    return _specs()


def get_experiment(experiment_id: str) -> ExperimentSpec:
    for spec in _specs():
        if spec.id == experiment_id:
            return spec
    raise KeyError(experiment_id)


def inspect_artifact(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text if len(text) < 8000 else text[:8000] + "\n... [truncated]\n"
