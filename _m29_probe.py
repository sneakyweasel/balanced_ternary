"""Milestone 29: joint-image collisions and cross-depth families."""

from collections import defaultdict

from bt.calculus.cubic import F_k, prefixes_at
from research.residuals.cubic_fibres import n3_vanishes, zero_spine_depths
from research.residuals.cubic_n0_reduction import n0_mod, n0_regime
from research.residuals.x3_state_complexity import (
    C_layer,
    core_n0,
    core_phi,
    core_u_range,
    core_width,
    easy_count,
    layer_depth,
)


def A_coord(u: int, k: int, r: int) -> int:
    exp = k - 2 * r - 1
    if exp <= 0:
        return 0
    return (u * u) % (3**exp)


def H_coord(u: int, k: int, r: int) -> tuple[int, int]:
    return (A_coord(u, k, r), core_n0(u, k, r))


def classify_core_collisions(k: int, r: int) -> None:
    buckets: dict[tuple, list[int]] = defaultdict(list)
    for u in core_u_range(k, r):
        buckets[H_coord(u, k, r)].append(u)
    W = core_width(k, r)
    m = layer_depth(k, r)
    fibs = {phi: us for phi, us in buckets.items() if len(us) > 1}
    print(
        f"k={k} r={r} W={W} regime={n0_regime(k, r)} "
        f"|H|={len(buckets)} |P|={3**max(W, 0)} C={C_layer(k, r)}"
    )
    kinds = defaultdict(int)
    for us in fibs.values():
        xs = sorted(us)
        if len(xs) == 2 and xs[0] == -xs[1]:
            kinds["sign"] += 1
        elif all(u == 0 or u % 3 == 0 for u in xs) and A_coord(xs[0], k, r) == 0:
            kinds["zero-A"] += 1
        else:
            kinds["other"] += 1
            if kinds["other"] <= 6:
                print("  other", xs, "A", A_coord(xs[0], k, r), "Q", core_n0(xs[0], k, r))
    print("  multi-fibres", dict(kinds), "n_multi", len(fibs))
    # check C = easy + |H|
    if r <= m:
        pred = easy_count(m, r) + len(buckets)
        print("  easy+|H|", pred, "C", C_layer(k, r), "ok", pred == C_layer(k, r))


def units_only_signs(k: int, r: int) -> None:
    W = core_width(k, r)
    if W < 1:
        return
    units = [u for u in core_u_range(k, r) if u % 3 != 0]
    sq: dict[int, list[int]] = defaultdict(list)
    exp = k - 2 * r - 1
    mod = 3**exp if exp > 0 else 1
    for u in units:
        sq[(u * u) % mod].append(u)
    bad = 0
    for us in sq.values():
        xs = sorted(set(us))
        if len(xs) == 1:
            continue
        if len(xs) == 2 and xs[0] == -xs[1]:
            continue
        bad += 1
        print("  unit square fibre not ±", xs)
    print(f"  unit square fibres extra={bad} (k={k} r={r})")


print("=== core H collisions ===")
for k in range(4, 12):
    for r in range(0, (k + 1) // 2):
        if k - 1 - r < 0:
            continue
        classify_core_collisions(k, r)
        if k >= 4 * r + 1:
            units_only_signs(k, r)

print()
print("=== cross-depth family dump ===")


def family_label(ps, qs, m, n, k):
    if all(p == 0 for p in ps) or F_k(m, 0, k) == F_k(n, 0, k) == F_k(m, ps[0], k):
        # check if this phi is the zero class
        if F_k(m, ps[0], k) == F_k(m, 0, k) and F_k(n, 0, k) == F_k(m, 0, k):
            return "zero-spine"
    same = set(ps) & set(qs)
    if same and all(abs(p) == abs(next(iter(same))) or p in same for p in ps + qs):
        if same == set(ps) == set(qs) or (len(ps) <= 2 and set(ps) <= set(qs) | set(ps)):
            if all(x == -y or x == y for x in ps for y in ps) and 0 not in same:
                return f"same-p-sign {sorted(same)}"
    if len(ps) == 1 and len(qs) == 1 and ps[0] != qs[0] and ps[0] == -qs[0]:
        return "cross-sign"
    if len(ps) == 1 and len(qs) >= 1:
        p = ps[0]
        if all((q - p) % (3 ** max(n - m, 1)) == 0 or (q + p) % 3 == 0 for q in qs[:1]):
            return f"translate p={p} -> {qs[:4]}..."
    return "UNCLASSIFIED"


for k in range(6, 11):
    start = k // 2
    images = []
    for m in range(k):
        buckets = defaultdict(list)
        for p in prefixes_at(m):
            buckets[F_k(m, p, k)].append(p)
        images.append(buckets)
    print(f"--- k={k} spine={zero_spine_depths(k)} ---")
    for m in range(start, k):
        for n in range(m + 1, k):
            inter = set(images[m]) & set(images[n])
            zero = F_k(m, 0, k)
            for phi in inter:
                ps, qs = images[m][phi], images[n][phi]
                if phi == zero == F_k(n, 0, k):
                    lab = "zero-spine"
                else:
                    lab = family_label(ps, qs, m, n, k)
                if lab.startswith("UNCLASS") or True:
                    print(f"  ({m},{n}) {lab} p={ps} q={qs[:8]}{'...' if len(qs)>8 else ''}")
