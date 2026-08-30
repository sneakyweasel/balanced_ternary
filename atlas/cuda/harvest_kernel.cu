#include "harvest_kernel.cuh"

#include "../cpp/harvest_walk.hpp"
#include "../cpp/packed_word.hpp"

#include <cuda_runtime.h>

#include <limits>
#include <vector>

namespace juggler_atlas {
namespace {

constexpr uint64_t SLAB = 1ull << 28;

__global__ void harvest_kernel(
    uint64_t n_begin,
    uint64_t n_end_inclusive,
    int k_max,
    unsigned long long* coarse,
    unsigned long long* hist,
    unsigned long long* min_n,
    unsigned long long* overflow_count,
    unsigned long long* overflow_n,
    unsigned long long* uncapped_count_stored,
    unsigned long long* uncapped_n,
    unsigned long long list_cap
) {
    const uint64_t n = n_begin + static_cast<uint64_t>(blockIdx.x) * blockDim.x + threadIdx.x;
    if (n < n_begin || n > n_end_inclusive) {
        return;
    }
    bool overflow = false;
    const HarvestHit hit = walk_certificate(n, k_max, overflow);
    const int cls = static_cast<int>(hit.cls);
    atomicAdd(coarse + cls, 1ull);
    if (hit.cls == HarvestClass::Leftover) {
        const int idx = dense_index(hit.length, hit.packed);
        atomicAdd(hist + idx, 1ull);
        atomicMin(min_n + idx, static_cast<unsigned long long>(n));
        return;
    }
    if (hit.cls == HarvestClass::Overflow) {
        const unsigned long long slot = atomicAdd(overflow_count, 1ull);
        if (slot < list_cap) {
            overflow_n[slot] = n;
        }
        return;
    }
    if (hit.cls == HarvestClass::Uncapped) {
        const unsigned long long slot = atomicAdd(uncapped_count_stored, 1ull);
        if (slot < list_cap) {
            uncapped_n[slot] = n;
        }
    }
}

}  // namespace

bool gpu_harvest(HarvestTables& tables) {
    init_harvest(tables);
    const int size = dense_size(tables.k_max);
    const size_t hist_bytes = static_cast<size_t>(size) * sizeof(unsigned long long);
    const unsigned long long cap = tables.overflow_cap;
    const size_t list_bytes = static_cast<size_t>(cap) * sizeof(unsigned long long);

    unsigned long long* d_coarse = nullptr;
    unsigned long long* d_hist = nullptr;
    unsigned long long* d_min = nullptr;
    unsigned long long* d_ov = nullptr;
    unsigned long long* d_ov_n = nullptr;
    unsigned long long* d_un = nullptr;
    unsigned long long* d_un_n = nullptr;

    auto cleanup = [&]() {
        if (d_coarse) cudaFree(d_coarse);
        if (d_hist) cudaFree(d_hist);
        if (d_min) cudaFree(d_min);
        if (d_ov) cudaFree(d_ov);
        if (d_ov_n) cudaFree(d_ov_n);
        if (d_un) cudaFree(d_un);
        if (d_un_n) cudaFree(d_un_n);
    };

    if (cudaMalloc(&d_coarse, 8 * sizeof(unsigned long long)) != cudaSuccess) {
        return false;
    }
    if (cudaMalloc(&d_hist, hist_bytes) != cudaSuccess) {
        cleanup();
        return false;
    }
    if (cudaMalloc(&d_min, hist_bytes) != cudaSuccess) {
        cleanup();
        return false;
    }
    if (cudaMalloc(&d_ov, sizeof(unsigned long long)) != cudaSuccess) {
        cleanup();
        return false;
    }
    if (cudaMalloc(&d_un, sizeof(unsigned long long)) != cudaSuccess) {
        cleanup();
        return false;
    }
    if (cudaMalloc(&d_ov_n, list_bytes) != cudaSuccess) {
        cleanup();
        return false;
    }
    if (cudaMalloc(&d_un_n, list_bytes) != cudaSuccess) {
        cleanup();
        return false;
    }

    std::vector<unsigned long long> host_min(
        static_cast<size_t>(size),
        std::numeric_limits<unsigned long long>::max()
    );
    cudaMemset(d_coarse, 0, 8 * sizeof(unsigned long long));
    cudaMemset(d_hist, 0, hist_bytes);
    cudaMemcpy(d_min, host_min.data(), hist_bytes, cudaMemcpyHostToDevice);
    unsigned long long zero = 0;
    cudaMemcpy(d_ov, &zero, sizeof(zero), cudaMemcpyHostToDevice);
    cudaMemcpy(d_un, &zero, sizeof(zero), cudaMemcpyHostToDevice);

    const int threads = 256;
    for (uint64_t begin = tables.n_begin; begin <= tables.n_max; ) {
        uint64_t last = begin + SLAB - 1ull;
        if (last < begin || last > tables.n_max) {
            last = tables.n_max;
        }
        const uint64_t count = last - begin + 1ull;
        const int blocks = static_cast<int>(
            (count + static_cast<uint64_t>(threads) - 1ull) / static_cast<uint64_t>(threads)
        );
        harvest_kernel<<<blocks, threads>>>(
            begin,
            last,
            tables.k_max,
            d_coarse,
            d_hist,
            d_min,
            d_ov,
            d_ov_n,
            d_un,
            d_un_n,
            cap
        );
        if (cudaDeviceSynchronize() != cudaSuccess) {
            cleanup();
            return false;
        }
        if (last == tables.n_max) {
            break;
        }
        begin = last + 1ull;
    }

    unsigned long long coarse[8] = {};
    cudaMemcpy(coarse, d_coarse, sizeof(coarse), cudaMemcpyDeviceToHost);
    cudaMemcpy(tables.hist.data(), d_hist, hist_bytes, cudaMemcpyDeviceToHost);
    cudaMemcpy(tables.min_n.data(), d_min, hist_bytes, cudaMemcpyDeviceToHost);
    unsigned long long ov_stored = 0;
    unsigned long long un_stored = 0;
    cudaMemcpy(&ov_stored, d_ov, sizeof(ov_stored), cudaMemcpyDeviceToHost);
    cudaMemcpy(&un_stored, d_un, sizeof(un_stored), cudaMemcpyDeviceToHost);

    tables.count_skip = coarse[static_cast<int>(HarvestClass::Skip)];
    tables.count_e = coarse[static_cast<int>(HarvestClass::E)];
    tables.count_oe = coarse[static_cast<int>(HarvestClass::OE)];
    tables.count_ooee = coarse[static_cast<int>(HarvestClass::OOEE)];
    tables.count_leftover = coarse[static_cast<int>(HarvestClass::Leftover)];
    tables.count_uncapped = coarse[static_cast<int>(HarvestClass::Uncapped)];
    tables.count_overflow = coarse[static_cast<int>(HarvestClass::Overflow)];
    tables.overflow_truncated = ov_stored > cap;
    tables.uncapped_truncated = un_stored > cap;

    const uint64_t ov_keep = ov_stored < cap ? ov_stored : cap;
    const uint64_t un_keep = un_stored < cap ? un_stored : cap;
    tables.overflow_n.resize(static_cast<size_t>(ov_keep));
    tables.uncapped_n.resize(static_cast<size_t>(un_keep));
    if (ov_keep > 0) {
        cudaMemcpy(
            tables.overflow_n.data(),
            d_ov_n,
            static_cast<size_t>(ov_keep) * sizeof(unsigned long long),
            cudaMemcpyDeviceToHost
        );
    }
    if (un_keep > 0) {
        cudaMemcpy(
            tables.uncapped_n.data(),
            d_un_n,
            static_cast<size_t>(un_keep) * sizeof(unsigned long long),
            cudaMemcpyDeviceToHost
        );
    }
    cleanup();
    return true;
}

}  // namespace juggler_atlas
