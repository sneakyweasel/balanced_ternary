"""Public API of the Collatz research module (Milestones 1–5)."""

from collatz.automata.joint_graph import JointGraph, build_joint_graph
from collatz.automata.symbolic_graph import SymbolicJointGraph, build_symbolic_graph
from collatz.automata.two_adic import TwoAdicDigitAutomaton
from collatz.automata.valuation_shift import AdmissibleValuationAutomaton
from collatz.cylinders import ValuationCylinder, precision_cost, valuation_cylinder
from collatz.dual_code import (
    CollatzDualCode,
    canonical_realizer_formula,
    reconstruct_realizer,
)
from collatz.itinerary import ValuationItinerary
from collatz.lift_tree import LiftTree, build_lift_tree
from collatz.periodic_itineraries import periodic_candidate
from collatz.zero_lift import (
    ZeroLiftState,
    finite_lift_certificate,
    lift_digit,
    lift_digits,
    zero_lift_k,
)
from collatz.bt_arithmetic import add, add_one, multiply_by_three, three_n_plus_one_word
from collatz.core import collatz_step, standard_collatz_step, three_n_plus_one
from collatz.experiments.exhaustive import run_exhaustive_experiment
from collatz.features import BalancedTernaryFeatures, extract_features
from collatz.inverse import build_inverse_tree, collatz_predecessors
from collatz.research.invariants import verify_collatz_invariants
from collatz.theorems import append_plus, predicted_features_after_append_plus
from collatz.trajectory import (
    collatz_stopping_time,
    collatz_total_stopping_time,
    collatz_trajectory,
)
from collatz.transducers import apply_even, odd_part_word
from collatz.transitions import CollatzFeatureTransition, feature_transition
from collatz.valuation import AT_LEAST_K, classify_collatz_valuation, v2

__all__ = [
    "AT_LEAST_K",
    "AdmissibleValuationAutomaton",
    "BalancedTernaryFeatures",
    "CollatzFeatureTransition",
    "CollatzDualCode",
    "JointGraph",
    "LiftTree",
    "SymbolicJointGraph",
    "TwoAdicDigitAutomaton",
    "ValuationCylinder",
    "ValuationItinerary",
    "ZeroLiftState",
    "add",
    "add_one",
    "append_plus",
    "apply_even",
    "build_inverse_tree",
    "build_joint_graph",
    "build_lift_tree",
    "build_symbolic_graph",
    "canonical_realizer_formula",
    "classify_collatz_valuation",
    "collatz_predecessors",
    "collatz_step",
    "collatz_stopping_time",
    "collatz_total_stopping_time",
    "collatz_trajectory",
    "extract_features",
    "feature_transition",
    "finite_lift_certificate",
    "lift_digit",
    "lift_digits",
    "multiply_by_three",
    "odd_part_word",
    "precision_cost",
    "periodic_candidate",
    "predicted_features_after_append_plus",
    "valuation_cylinder",
    "run_exhaustive_experiment",
    "reconstruct_realizer",
    "standard_collatz_step",
    "three_n_plus_one",
    "three_n_plus_one_word",
    "v2",
    "verify_collatz_invariants",
    "zero_lift_k",
]
