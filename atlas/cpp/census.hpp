#pragma once

#include <cstdint>
#include <vector>

namespace juggler_atlas {

struct CensusTables {
    int k_max = 0;
    uint64_t n_begin = 1;
    uint64_t n_max = 0;
    std::vector<uint64_t> min_n;
    std::vector<uint64_t> min_exp;
    uint64_t overflow_count = 0;
};

void cpu_census(CensusTables& tables);

#ifdef JUGGLER_ATLAS_CUDA
bool gpu_census(CensusTables& tables);
#endif

}  // namespace juggler_atlas
