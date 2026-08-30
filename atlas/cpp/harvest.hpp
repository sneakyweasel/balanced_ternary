#pragma once

#include <cstdint>
#include <vector>

namespace juggler_atlas {

struct HarvestTables {
    int k_max = 20;
    uint64_t n_begin = 2;
    uint64_t n_max = 0;
    uint64_t count_skip = 0;
    uint64_t count_e = 0;
    uint64_t count_oe = 0;
    uint64_t count_ooee = 0;
    uint64_t count_leftover = 0;
    uint64_t count_uncapped = 0;
    uint64_t count_overflow = 0;
    std::vector<uint64_t> hist;
    std::vector<uint64_t> min_n;
    std::vector<uint64_t> overflow_n;
    std::vector<uint64_t> uncapped_n;
    uint64_t overflow_cap = 16000000;
    bool overflow_truncated = false;
    bool uncapped_truncated = false;
};

void init_harvest(HarvestTables& tables);
void cpu_harvest(HarvestTables& tables);
void apply_harvest_hit(
    HarvestTables& tables,
    uint64_t n,
    int cls,
    int length,
    uint64_t packed
);

#ifdef JUGGLER_ATLAS_CUDA
bool gpu_harvest(HarvestTables& tables);
#endif

}  // namespace juggler_atlas
