"""Post-run probes. Not planner hints and not adapter inputs."""

from __future__ import annotations

from research.companion_shift_order6_zero_class.spec import map_spec
from research.skolem_lrs.spec import CompanionShiftSpec, skip_attacks_for_dimension
from research.skolem_lrs.discovery import evidence_state as prefix_evidence
from research.skolem_lrs.discovery import falsify_claims as prefix_falsify


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
        "lattice_congruence": False,
        "universal_zero_free": False,
        "note": "NO ZERO FOUND is not NO ZERO EXISTS; a prefix gap is not modular exclusion",
    }


def falsify_claims(spec: CompanionShiftSpec | None = None) -> dict[str, dict[str, object]]:
    target = spec if spec is not None else map_spec()
    report = evidence_state(target)
    prefix = prefix_falsify(target)
    return {
        **prefix,
        "companion_is_the_yield": {
            "claim": "rediscovering the order-6 companion is the mathematical yield",
            "holds_on_window": True,
            "status": "REFUTED",
            "counterexample": "companion reconstruction is KNOWN infrastructure",
        },
        "prefix_means_nonexistence": {
            "claim": "no zero on the length-64 prefix means no zero exists",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": report["status"],
        },
        "matrix_word_gives_vanishing_congruence": {
            "claim": "matrix-word / lattice-gcd recovers a congruence on vanishing indices",
            "holds_on_window": not report["matrix_word_skipped"],
            "status": "REFUTED",
            "counterexample": report["skipped_attacks"],
        },
        "this_is_the_order2_competence_check": {
            "claim": "this window is the certified order-2 zero",
            "holds_on_window": False,
            "status": "REFUTED",
            "counterexample": {"dimension": report["dimension"], "zero_at": report["zero_at"]},
        },
    }
