"""Reproducible Collatz experiments."""

from collatz.experiments.complexity_spectrum import (
    ComplexitySpectrumResult,
    run_complexity_spectrum,
)
from collatz.experiments.affine_center import run_affine_center_census
from collatz.experiments.exhaustive import ExhaustiveExperimentResult, run_exhaustive_experiment
from collatz.experiments.noncontracting_dual import run_noncontracting_dual
from collatz.experiments.information_content import run_information_content
from collatz.experiments.near_critical import run_near_critical
from collatz.experiments.periodic_dual import periodic_dual_trace
from collatz.experiments.schema import ExperimentManifest
from collatz.experiments.suffix_determination import suffix_determination_census

__all__ = [
    "ComplexitySpectrumResult",
    "ExhaustiveExperimentResult",
    "ExperimentManifest",
    "periodic_dual_trace",
    "run_affine_center_census",
    "run_complexity_spectrum",
    "run_exhaustive_experiment",
    "run_information_content",
    "run_near_critical",
    "run_noncontracting_dual",
    "suffix_determination_census",
]
