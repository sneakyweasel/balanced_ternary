"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.skolem_lrs.discovery import evidence_state as prefix_evidence
from research.skolem_lrs.discovery import falsify_claims as prefix_falsify
from research.skolem_lrs.spec import CompanionShiftSpec, skip_attacks_for_dimension
from research.skolem_order5_unconditional.spec import map_spec


def evidence_state(spec: CompanionShiftSpec | None = None) -> dict[str, object]:
    target = spec if spec is not None else map_spec()
    report = prefix_evidence(target, max_index=64)
    skipped = skip_attacks_for_dimension(target.dimension)
    ctx = target.attack_context()
    return {
        **report,
        "dimension": target.dimension,
        "skipped_attacks": skipped,
        "context_skip_attacks": tuple(ctx.skip_attacks),
        "matrix_word_skipped": "matrix_word_invariant" in skipped,
        "vector_census_skipped": "vector_affine" in skipped,
        "same_skip_as_dimension_6": skipped == skip_attacks_for_dimension(6),
        "lattice_congruence": False,
        "uniqueness_from_prefix": False,
        "unconditional_decision": False,
        "note": "a ZERO_WITNESS is not an order-5 decision procedure; skip is not uniqueness",
    }


def falsify_claims(spec: CompanionShiftSpec | None = None) -> dict[str, dict[str, object]]:
    target = spec if spec is not None else map_spec()
    report = evidence_state(target)
    prefix = prefix_falsify(target)
    return {
        **prefix,
        "companion_is_the_yield": {
            "claim": "rediscovering the order-5 companion is the mathematical yield",
            "holds_on_window": True,
            "status": "REFUTED",
            "counterexample": "companion reconstruction is KNOWN infrastructure",
        },
        "census_runs_at_dimension_5": {
            "claim": "vector census and matrix-word run at dimension 5",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": report["skipped_attacks"],
        },
        "this_is_the_order6_flagship": {
            "claim": "this window is the order-6 survey instance",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {"dimension": report["dimension"], "zero_at": report["zero_at"]},
        },
        "this_is_the_order2_competence_check": {
            "claim": "this window is the certified order-2 zero",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {"dimension": report["dimension"], "zero_at": report["zero_at"]},
        },
        "zero_witness_is_unconditional_decision": {
            "claim": "a finite first-coordinate zero decides vanishing for all order-5 LRS",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": report["status"],
        },
        "prefix_gives_uniqueness": {
            "claim": "the frozen prefix recovers uniqueness of the zero",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": "uniqueness_from_prefix is False; moduli 2..32 are not a certificate",
        },
        "same_skip_is_a_new_cluster": {
            "claim": "dimension-5 census skip is a new computational cluster",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": report["same_skip_as_dimension_6"],
        },
    }
