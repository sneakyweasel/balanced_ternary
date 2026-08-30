#pragma once

#include "packed_word.hpp"
#include "wide_uint.hpp"

#ifdef __CUDACC__
#define JA_HD_HARVEST __host__ __device__ inline
#else
#define JA_HD_HARVEST inline
#endif

namespace juggler_atlas {

enum class HarvestClass : int {
    Skip = 0,
    E = 1,
    OE = 2,
    OOEE = 3,
    Leftover = 4,
    Uncapped = 5,
    Overflow = 6,
};

struct HarvestHit {
    HarvestClass cls = HarvestClass::Uncapped;
    int length = 0;
    uint64_t packed = 0;
};

JA_HD_HARVEST HarvestHit classify_contracting_word(int depth, uint64_t packed) {
    HarvestHit hit;
    hit.length = depth;
    hit.packed = packed;
    if (depth == 1 && packed == 0ull) {
        hit.cls = HarvestClass::E;
        return hit;
    }
    if (depth == 2 && packed == 1ull) {
        hit.cls = HarvestClass::OE;
        return hit;
    }
    if (depth == 4 && packed == 3ull) {
        hit.cls = HarvestClass::OOEE;
        return hit;
    }
    hit.cls = HarvestClass::Leftover;
    return hit;
}

JA_HD_HARVEST HarvestHit walk_certificate(uint64_t n, int k_max, bool& overflow) {
    overflow = false;
    HarvestHit hit;
    hit.cls = HarvestClass::Uncapped;
    if (n < 2) {
        hit.cls = HarvestClass::Skip;
        return hit;
    }
    uint64_t packed = 0;
    uint64_t state64 = n;
    bool wide = false;
    Wide8 state8;
    w8_zero(state8);

    for (int depth = 1; depth <= k_max; ++depth) {
        const uint64_t bit = wide ? (state8.d[0] & 1ull) : (state64 & 1ull);
        packed |= bit << (depth - 1);

        if (!wide) {
            uint64_t nxt64 = 0;
            if (floor_power_u64_ok(state64, nxt64)) {
                if (nxt64 < n) {
                    return classify_contracting_word(depth, packed);
                }
                state64 = nxt64;
                continue;
            }
            w8_from_u64(state8, state64);
            wide = true;
        }
        bool ov = false;
        Wide8 nxt = floor_power_w8(state8, ov);
        if (ov) {
            overflow = true;
            hit.cls = HarvestClass::Overflow;
            hit.length = depth;
            hit.packed = packed;
            return hit;
        }
        if (w8_lt_u64(nxt, n)) {
            return classify_contracting_word(depth, packed);
        }
        state8 = nxt;
    }
    hit.length = k_max;
    hit.packed = packed;
    return hit;
}

}  // namespace juggler_atlas
