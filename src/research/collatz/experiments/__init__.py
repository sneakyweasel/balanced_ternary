"""Reproducible Collatz experiments."""

from research.collatz.experiments.bt_warp import run_bt_warp_census
from research.collatz.experiments.complexity_spectrum import (
    ComplexitySpectrumResult,
    run_complexity_spectrum,
)
from research.collatz.experiments.cycle_census import run_cycle_census
from research.collatz.experiments.affine_center import run_affine_center_census
from research.collatz.experiments.exhaustive import ExhaustiveExperimentResult, run_exhaustive_experiment
from research.collatz.experiments.noncontracting_dual import run_noncontracting_dual
from research.collatz.experiments.information_content import run_information_content
from research.collatz.experiments.near_critical import run_near_critical
from research.collatz.asymptotic import run_fixed_integer_census
from research.collatz.experiments.periodic_dual import periodic_dual_trace
from research.collatz.experiments.schema import ExperimentManifest
from research.collatz.experiments.suffix_determination import suffix_determination_census

__all__ = [
    "ComplexitySpectrumResult",
    "ExhaustiveExperimentResult",
    "ExperimentManifest",
    "periodic_dual_trace",
    "run_affine_center_census",
    "run_bt_warp_census",
    "run_complexity_spectrum",
    "run_cycle_census",
    "run_exhaustive_experiment",
    "run_fixed_integer_census",
    "run_information_content",
    "run_near_critical",
    "run_noncontracting_dual",
    "suffix_determination_census",
]
