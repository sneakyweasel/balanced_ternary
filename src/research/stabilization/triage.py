"""One witness that local Hensel uniqueness is not global N_k constancy.

No new bound is computed. The function records the already-classical
split between a simple root and a singular cluster on the same f.
"""

from __future__ import annotations

from bt.calculus.lifting import level_counts, lift_tree, node_at
from bt.calculus.section import parse_poly

WITNESS = "x^3 - x^2 - 9x + 9"


def _require_nat(n: int, name: str) -> int:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError(f"{name} must be a natural number")
    return n


def witness_mixed_clusters(k_max: int = 5) -> dict[str, object]:
    """The polynomial (x-1)(x^2-9).

    Residue 1 is Hensel-unique from level 1. Residue 0 carries the
    singular cluster of ±3, so N_k is not constant from level 1.
    """
    k_max = _require_nat(k_max, "k_max")
    if k_max < 2:
        raise ValueError("k_max must be at least 2")
    f = parse_poly(WITNESS)
    counts = level_counts(f, k_max)
    simple = node_at(f, (1,))
    cluster = node_at(f, (0,))
    simple_path = all(
        len(node_at(f, (1,) + (0,) * extra).children) == 1
        for extra in range(k_max - 1)
    )
    return {
        "poly": f.render(),
        "N_k": list(counts),
        "simple_node": {
            "word": "1",
            "singular": simple.singular,
            "f_prime": simple.f_prime,
            "children": len(simple.children),
            "unique_lift_thereafter": simple_path,
        },
        "cluster_node": {
            "word": "0",
            "singular": cluster.singular,
            "f_prime": cluster.f_prime,
            "children": len(cluster.children),
        },
        "N_k_constant_from_level_1": len(set(counts[1:])) == 1,
        "local_unique_but_global_moving": (
            not simple.singular
            and simple_path
            and len(set(counts[1:])) > 1
        ),
    }


def first_all_nonsingular(f, k_max: int) -> int | None:
    """Least k>=1 at which every surviving node has unit derivative, or None."""
    nodes = lift_tree(f, k_max)
    for k in range(1, k_max + 1):
        layer = [n for n in nodes if n.level == k]
        if layer and all(not n.singular for n in layer):
            return k
    return None


def local_vs_global_report(k_max: int = 5) -> dict[str, object]:
    """Triage payload: the mixed-cluster witness plus the literature verdict."""
    mixed = witness_mixed_clusters(k_max)
    f = parse_poly(WITNESS)
    return {
        "witness": mixed,
        "first_all_nonsingular": first_all_nonsingular(f, k_max),
        "verdict": {
            "k0_is_a_closed_form_for_N_k": True,
            "k0_is_not_a_per_branch_lift_bound": True,
            "phi_r_is_the_taylor_jet": True,
            "local_hensel_already_adaptive": True,
            "witness_splits_local_from_global": mixed["local_unique_but_global_moving"],
            "novelty": "NONE",
        },
    }
