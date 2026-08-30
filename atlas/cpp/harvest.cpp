#include "harvest.hpp"

#include "harvest_walk.hpp"
#include "packed_word.hpp"

#include <limits>

namespace juggler_atlas {

void init_harvest(HarvestTables& tables) {
    const int size = dense_size(tables.k_max);
    tables.hist.assign(static_cast<size_t>(size), 0);
    tables.min_n.assign(static_cast<size_t>(size), std::numeric_limits<uint64_t>::max());
    tables.overflow_n.clear();
    tables.uncapped_n.clear();
    tables.count_skip = 0;
    tables.count_e = 0;
    tables.count_oe = 0;
    tables.count_ooee = 0;
    tables.count_leftover = 0;
    tables.count_uncapped = 0;
    tables.count_overflow = 0;
    tables.overflow_truncated = false;
    tables.uncapped_truncated = false;
}

void apply_harvest_hit(
    HarvestTables& tables,
    uint64_t n,
    int cls,
    int length,
    uint64_t packed
) {
    switch (static_cast<HarvestClass>(cls)) {
        case HarvestClass::Skip:
            ++tables.count_skip;
            return;
        case HarvestClass::E:
            ++tables.count_e;
            return;
        case HarvestClass::OE:
            ++tables.count_oe;
            return;
        case HarvestClass::OOEE:
            ++tables.count_ooee;
            return;
        case HarvestClass::Leftover: {
            ++tables.count_leftover;
            const int idx = dense_index(length, packed);
            ++tables.hist[static_cast<size_t>(idx)];
            if (n < tables.min_n[static_cast<size_t>(idx)]) {
                tables.min_n[static_cast<size_t>(idx)] = n;
            }
            return;
        }
        case HarvestClass::Uncapped:
            ++tables.count_uncapped;
            if (tables.uncapped_n.size() < static_cast<size_t>(tables.overflow_cap)) {
                tables.uncapped_n.push_back(n);
            } else {
                tables.uncapped_truncated = true;
            }
            return;
        case HarvestClass::Overflow:
            ++tables.count_overflow;
            if (tables.overflow_n.size() < static_cast<size_t>(tables.overflow_cap)) {
                tables.overflow_n.push_back(n);
            } else {
                tables.overflow_truncated = true;
            }
            return;
    }
}

void cpu_harvest(HarvestTables& tables) {
    init_harvest(tables);
    const int k_max = tables.k_max;
    for (uint64_t n = tables.n_begin; n <= tables.n_max; ++n) {
        bool overflow = false;
        const HarvestHit hit = walk_certificate(n, k_max, overflow);
        apply_harvest_hit(
            tables,
            n,
            static_cast<int>(hit.cls),
            hit.length,
            hit.packed
        );
    }
}

}  // namespace juggler_atlas
