#pragma once

#include <cstdint>
#include <string>

#ifdef __CUDACC__
#define JA_HD_PACKED __host__ __device__
#else
#define JA_HD_PACKED
#endif

namespace juggler_atlas {

JA_HD_PACKED inline constexpr uint64_t word_id(uint32_t length, uint32_t packed) {
    return (static_cast<uint64_t>(length) << 32) | packed;
}

JA_HD_PACKED inline constexpr int dense_index(int length, uint64_t packed) {
    return ((1 << length) - 2) + static_cast<int>(packed);
}

JA_HD_PACKED inline constexpr int dense_size(int k_max) {
    if (k_max <= 0) {
        return 0;
    }
    return (1 << (k_max + 1)) - 2;
}

inline constexpr int odd_count(int length, uint64_t packed) {
    uint64_t mask = length ? ((1ull << length) - 1ull) : 0ull;
    uint64_t bits = packed & mask;
    int count = 0;
    while (bits) {
        count += static_cast<int>(bits & 1ull);
        bits >>= 1;
    }
    return count;
}

inline std::string unpack_word(int length, uint64_t packed) {
    std::string out;
    out.resize(static_cast<size_t>(length));
    for (int i = 0; i < length; ++i) {
        out[static_cast<size_t>(i)] = ((packed >> i) & 1ull) ? 'O' : 'E';
    }
    return out;
}

inline std::string run_signature(int length, uint64_t packed) {
    if (length <= 0) {
        return {};
    }
    std::string out;
    uint64_t bit = packed & 1ull;
    int run = 1;
    for (int i = 1; i < length; ++i) {
        uint64_t nxt = (packed >> i) & 1ull;
        if (nxt == bit) {
            ++run;
        } else {
            out += (bit ? 'O' : 'E');
            out += std::to_string(run);
            out += ',';
            bit = nxt;
            run = 1;
        }
    }
    out += (bit ? 'O' : 'E');
    out += std::to_string(run);
    return out;
}

}  // namespace juggler_atlas
