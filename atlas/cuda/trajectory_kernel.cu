#include "trajectory_kernel.cuh"

#include "../cpp/packed_word.hpp"
#include "../cpp/wide_uint.hpp"

#include <cuda_runtime.h>

#include <limits>
#include <vector>

namespace juggler_atlas {
namespace {

__global__ void trajectory_kernel(
    uint64_t n_begin,
    uint64_t n_end_inclusive,
    int k_max,
    unsigned long long* min_n,
    unsigned long long* min_exp,
    unsigned long long* overflow_count,
    unsigned long long* overflow_n,
    unsigned long long overflow_cap
) {
    const uint64_t n = n_begin + static_cast<uint64_t>(blockIdx.x) * blockDim.x + threadIdx.x;
    if (n < n_begin || n > n_end_inclusive) {
        return;
    }
    Wide8 state;
    w8_from_u64(state, n);
    uint64_t packed = 0;
    for (int depth = 1; depth <= k_max; ++depth) {
        packed |= (state.d[0] & 1ull) << (depth - 1);
        bool overflow = false;
        Wide8 nxt = floor_power_w8(state, overflow);
        if (overflow) {
            const unsigned long long slot = atomicAdd(overflow_count, 1ull);
            if (slot < overflow_cap) {
                overflow_n[slot] = n;
            }
            return;
        }
        const int idx = dense_index(depth, packed);
        atomicMin(min_n + idx, static_cast<unsigned long long>(n));
        if (w8_gt_u64(nxt, n)) {
            atomicMin(min_exp + idx, static_cast<unsigned long long>(n));
        }
        state = nxt;
    }
}

}  // namespace

bool gpu_census(CensusTables& tables) {
    const int size = dense_size(tables.k_max);
    tables.min_n.assign(static_cast<size_t>(size), std::numeric_limits<uint64_t>::max());
    tables.min_exp.assign(static_cast<size_t>(size), std::numeric_limits<uint64_t>::max());
    tables.overflow_count = 0;
    tables.overflow_truncated = false;
    tables.overflow_n.clear();

    unsigned long long* d_min = nullptr;
    unsigned long long* d_exp = nullptr;
    unsigned long long* d_ov = nullptr;
    unsigned long long* d_ov_n = nullptr;
    const size_t bytes = static_cast<size_t>(size) * sizeof(unsigned long long);
    const unsigned long long cap = tables.overflow_cap;
    const size_t ov_bytes = static_cast<size_t>(cap) * sizeof(unsigned long long);
    if (cudaMalloc(&d_min, bytes) != cudaSuccess) {
        return false;
    }
    if (cudaMalloc(&d_exp, bytes) != cudaSuccess) {
        cudaFree(d_min);
        return false;
    }
    if (cudaMalloc(&d_ov, sizeof(unsigned long long)) != cudaSuccess) {
        cudaFree(d_min);
        cudaFree(d_exp);
        return false;
    }
    if (cudaMalloc(&d_ov_n, ov_bytes) != cudaSuccess) {
        cudaFree(d_min);
        cudaFree(d_exp);
        cudaFree(d_ov);
        return false;
    }
    cudaMemcpy(d_min, tables.min_n.data(), bytes, cudaMemcpyHostToDevice);
    cudaMemcpy(d_exp, tables.min_exp.data(), bytes, cudaMemcpyHostToDevice);
    unsigned long long zero = 0;
    cudaMemcpy(d_ov, &zero, sizeof(zero), cudaMemcpyHostToDevice);

    const uint64_t count = tables.n_max - tables.n_begin + 1;
    const int threads = 256;
    const int blocks = static_cast<int>((count + static_cast<uint64_t>(threads) - 1) / threads);
    trajectory_kernel<<<blocks, threads>>>(
        tables.n_begin,
        tables.n_max,
        tables.k_max,
        d_min,
        d_exp,
        d_ov,
        d_ov_n,
        cap
    );
    const cudaError_t err = cudaDeviceSynchronize();
    bool ok = err == cudaSuccess;
    if (ok) {
        cudaMemcpy(tables.min_n.data(), d_min, bytes, cudaMemcpyDeviceToHost);
        cudaMemcpy(tables.min_exp.data(), d_exp, bytes, cudaMemcpyDeviceToHost);
        cudaMemcpy(&tables.overflow_count, d_ov, sizeof(unsigned long long), cudaMemcpyDeviceToHost);
        const uint64_t stored = tables.overflow_count < cap ? tables.overflow_count : cap;
        tables.overflow_truncated = tables.overflow_count > cap;
        tables.overflow_n.resize(static_cast<size_t>(stored));
        if (stored > 0) {
            cudaMemcpy(
                tables.overflow_n.data(),
                d_ov_n,
                static_cast<size_t>(stored) * sizeof(unsigned long long),
                cudaMemcpyDeviceToHost
            );
        }
    }
    cudaFree(d_min);
    cudaFree(d_exp);
    cudaFree(d_ov);
    cudaFree(d_ov_n);
    return ok;
}

}  // namespace juggler_atlas
