"""Public API of the Collatz research module."""

from research.collatz.automata.joint_graph import JointGraph, build_joint_graph
from research.collatz.automata.symbolic_graph import SymbolicJointGraph, build_symbolic_graph
from research.collatz.automata.two_adic import TwoAdicDigitAutomaton
from research.collatz.automata.valuation_shift import AdmissibleValuationAutomaton
from research.collatz.affine_center import AffineCenterState, AffineRegime
from research.collatz.affine_gap import affine_gap
from research.collatz.cycles import PeriodicExponentCode, candidate_cycle
from research.collatz.cylinders import ValuationCylinder, precision_cost, valuation_cylinder
from research.collatz.compatibility import (
    CompatibilityGraph,
    CompatibilityState,
    ExponentCodeDiagnostic,
    build_compatibility_graph,
)
from research.collatz.dual_code import (
    CollatzDualCode,
    canonical_realizer_formula,
    reconstruct_realizer,
)
from research.collatz.fixed_integer import InfiniteTrajectoryAffineState
from research.collatz.itinerary import ValuationItinerary
from research.collatz.endpoint_3adic import KramerEndpoint, kramer_endpoint_residue
from research.collatz.lift_tree import LiftTree, build_lift_tree
from research.collatz.periodic_itineraries import periodic_candidate
from research.collatz.rational_base import (
    RationalBaseThreeHalves,
    decode_base_3_2,
    encode_base_3_2,
)
from research.collatz.zero_lift import (
    ZeroLiftState,
    finite_lift_certificate,
    lift_digit,
    lift_digits,
    zero_lift_k,
)
from research.collatz.core import collatz_step, standard_collatz_step, three_n_plus_one
from research.collatz.experiments.exhaustive import run_exhaustive_experiment
from research.collatz.features import BalancedTernaryFeatures, extract_features
from research.collatz.inverse import build_inverse_tree, collatz_predecessors
from research.collatz.invariants import verify_collatz_invariants
from research.collatz.theorems import append_plus, predicted_features_after_append_plus
from research.collatz.trajectory import (
    collatz_stopping_time,
    collatz_total_stopping_time,
    collatz_trajectory,
)
from research.collatz.transducers.odd_part import odd_part_word
from research.collatz.transitions import CollatzFeatureTransition, feature_transition
from research.collatz.valuation import AT_LEAST_K, classify_collatz_valuation, v2
from research.collatz.warp import WarpState, warp_state

__all__ = [
    "AT_LEAST_K",
    "AdmissibleValuationAutomaton",
    "AffineCenterState",
    "AffineRegime",
    "BalancedTernaryFeatures",
    "CollatzFeatureTransition",
    "CollatzDualCode",
    "CompatibilityGraph",
    "CompatibilityState",
    "ExponentCodeDiagnostic",
    "InfiniteTrajectoryAffineState",
    "PeriodicExponentCode",
    "JointGraph",
    "KramerEndpoint",
    "LiftTree",
    "SymbolicJointGraph",
    "TwoAdicDigitAutomaton",
    "RationalBaseThreeHalves",
    "ValuationCylinder",
    "ValuationItinerary",
    "WarpState",
    "ZeroLiftState",
    "append_plus",
    "build_inverse_tree",
    "build_joint_graph",
    "build_lift_tree",
    "build_compatibility_graph",
    "build_symbolic_graph",
    "canonical_realizer_formula",
    "candidate_cycle",
    "classify_collatz_valuation",
    "collatz_predecessors",
    "collatz_step",
    "collatz_stopping_time",
    "collatz_total_stopping_time",
    "collatz_trajectory",
    "extract_features",
    "encode_base_3_2",
    "decode_base_3_2",
    "feature_transition",
    "finite_lift_certificate",
    "affine_gap",
    "lift_digit",
    "lift_digits",
    "kramer_endpoint_residue",
    "odd_part_word",
    "precision_cost",
    "periodic_candidate",
    "predicted_features_after_append_plus",
    "valuation_cylinder",
    "run_exhaustive_experiment",
    "reconstruct_realizer",
    "standard_collatz_step",
    "three_n_plus_one",
    "v2",
    "verify_collatz_invariants",
    "warp_state",
    "zero_lift_k",
]
