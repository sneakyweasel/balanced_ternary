#include "census.hpp"

#include "packed_word.hpp"
#include "wide_uint.hpp"

#include <limits>

namespace juggler_atlas {
namespace {

void init_tables(CensusTables& tables) {
    const int size = dense_size(tables.k_max);
    tables.min_n.assign(static_cast<size_t>(size), std::numeric_limits<uint64_t>::max());
    tables.min_exp.assign(static_cast<size_t>(size), std::numeric_limits<uint64_t>::max());
    tables.overflow_count = 0;
}

}  // namespace

void cpu_census(CensusTables& tables) {
    init_tables(tables);
    const uint64_t n_lo = tables.n_begin;
    const uint64_t n_hi = tables.n_max;
    const int k_max = tables.k_max;
    for (uint64_t n = n_lo; n <= n_hi; ++n) {
        Wide8 state;
        w8_from_u64(state, n);
        uint64_t packed = 0;
        for (int depth = 1; depth <= k_max; ++depth) {
            packed |= (state.d[0] & 1ull) << (depth - 1);
            bool overflow = false;
            Wide8 nxt = floor_power_w8(state, overflow);
            if (overflow) {
                ++tables.overflow_count;
                break;
            }
            const int idx = dense_index(depth, packed);
            if (n < tables.min_n[static_cast<size_t>(idx)]) {
                tables.min_n[static_cast<size_t>(idx)] = n;
            }
            if (w8_gt_u64(nxt, n) && n < tables.min_exp[static_cast<size_t>(idx)]) {
                tables.min_exp[static_cast<size_t>(idx)] = n;
            }
            state = nxt;
        }
    }
}

}  // namespace juggler_atlas
