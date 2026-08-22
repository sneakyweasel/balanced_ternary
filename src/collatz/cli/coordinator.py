"""Dispatch parsed Collatz commands to their family handlers."""

from __future__ import annotations

import argparse

from .foundations import (
    _analyze,
    _trajectory,
    _inverse,
    _invariants,
    _automaton,
    _experiment,
    _theorems,
    _odd_part,
    _transducer,
    _valuation_shift,
    _joint,
    _cylinder,
    _entropy,
    _complexity,
    _symbolic_graph,
)
from .itineraries import (
    _itinerary,
    _realizer,
    _enumerate_itineraries,
    _fixed_budget,
    _permutations,
    _exceptional_search,
    _zero_lift,
    _periodic_itinerary,
    _zero_lift_census,
    _dual_code,
    _lift_tree,
    _periodic_dual,
    _suffix_test,
    _dual_dataset,
)
from .compatibility import (
    _compatibility,
    _compatibility_graph,
    _rational_base,
    _information_test,
    _near_critical,
    _affine_center,
    _affine_center_census,
)

def run_collatz(args: argparse.Namespace) -> int:
    cmd = args.collatz_cmd
    if cmd == "analyze":
        return _analyze(args.n)
    if cmd == "trajectory":
        return _trajectory(args.n, args.max_steps)
    if cmd == "inverse":
        return _inverse(args.m, args.depth, args.k_max, args.max_nodes)
    if cmd == "test-invariants":
        return _invariants(args.limit)
    if cmd == "automaton":
        return _automaton(args.precision, args.word)
    if cmd == "experiment":
        return _experiment(args.limit, args.write)
    if cmd == "theorems":
        return _theorems(args.n)
    if cmd == "odd-part":
        return _odd_part(args.x)
    if cmd == "transducer":
        return _transducer(args.k, args.limit)
    if cmd == "valuation-shift":
        return _valuation_shift(args.precision, args.k_max, args.length)
    if cmd == "joint":
        return _joint(
            args.limit,
            args.k_max,
            args.precision,
            args.pattern_length,
            args.sync_length,
        )
    if cmd == "cylinder":
        return _cylinder(args.ks, args.leftover)
    if cmd == "entropy":
        return _entropy(args.ks, args.length, args.leftover)
    if cmd == "complexity":
        return _complexity(args.k_max, args.write)
    if cmd == "symbolic-graph":
        return _symbolic_graph(args.max_length, args.k_max, args.leftover)
    if cmd == "itinerary":
        return _itinerary(args.ks)
    if cmd == "realizer":
        return _realizer(args.ks)
    if cmd == "enumerate-itineraries":
        return _enumerate_itineraries(args.length, args.max_k, args.write)
    if cmd == "fixed-budget":
        return _fixed_budget(args.length, args.sum_k, args.write)
    if cmd == "permutations":
        return _permutations(args.ks, args.write)
    if cmd == "exceptional-search":
        return _exceptional_search(args.length, args.max_k, args.epsilon)
    if cmd == "zero-lift":
        return _zero_lift(args.ks, args.steps, args.candidate_k, args.precision)
    if cmd == "periodic-itinerary":
        return _periodic_itinerary(args.ks)
    if cmd == "zero-lift-census":
        return _zero_lift_census(args.max_length, args.max_k, args.precision)
    if cmd == "dual-code":
        return _dual_code(args.ks)
    if cmd == "lift-tree":
        return _lift_tree(args.max_depth, args.max_k, args.max_nodes)
    if cmd == "periodic-dual":
        return _periodic_dual(args.ks, args.repeats)
    if cmd == "suffix-test":
        return _suffix_test(args.max_length, args.max_k, args.suffix_max)
    if cmd == "dual-dataset":
        return _dual_dataset(args.length, args.max_k, args.write)
    if cmd == "compatibility":
        return _compatibility(args.ks)
    if cmd == "compatibility-graph":
        return _compatibility_graph(args.max_depth, args.max_k, args.root)
    if cmd == "rational-base":
        return _rational_base(args.n)
    if cmd == "information-test":
        return _information_test(
            args.max_length, args.max_k, args.precision_max, args.write
        )
    if cmd == "near-critical":
        return _near_critical(
            args.max_length,
            args.max_k,
            args.random_length,
            args.random_count,
            args.seed,
            args.write,
        )
    if cmd == "affine-center":
        return _affine_center(args.ks, args.critical_gap)
    if cmd == "affine-center-census":
        return _affine_center_census(
            args.max_length,
            args.max_k,
            args.critical_gap,
            args.closest_count,
            args.write,
        )
    if cmd == "ui":
        from visualization.app import launch

        return launch()
    raise SystemExit(f"unknown collatz command {cmd!r}")
