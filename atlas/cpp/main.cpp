#include "census.hpp"
#include "harvest.hpp"
#include "packed_word.hpp"

#ifdef JUGGLER_ATLAS_CUDA
#include "../cuda/harvest_kernel.cuh"
#endif

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <limits>
#include <string>

namespace {

struct Args {
    std::string mode = "census";
    int k_max = 12;
    uint64_t n_max = 1000000;
    uint64_t n_begin = 1;
    std::string backend = "cpu";
    std::string output = "census.tsv";
    uint64_t list_cap = 16000000;
};

void usage() {
    std::cerr
        << "juggler-atlas-census --mode census|harvest --k-max 12 "
           "--n-max 1000000 --n-begin 1 --backend cpu|cuda --output out.tsv\n";
}

bool parse_args(int argc, char** argv, Args& args) {
    for (int i = 1; i < argc; ++i) {
        const std::string key = argv[i];
        if (i + 1 >= argc) {
            return false;
        }
        const std::string val = argv[++i];
        if (key == "--mode") {
            args.mode = val;
        } else if (key == "--k-max") {
            args.k_max = std::atoi(val.c_str());
        } else if (key == "--n-max") {
            args.n_max = static_cast<uint64_t>(std::strtoull(val.c_str(), nullptr, 10));
        } else if (key == "--n-begin") {
            args.n_begin = static_cast<uint64_t>(std::strtoull(val.c_str(), nullptr, 10));
        } else if (key == "--backend") {
            args.backend = val;
        } else if (key == "--output") {
            args.output = val;
        } else if (key == "--list-cap") {
            args.list_cap = static_cast<uint64_t>(std::strtoull(val.c_str(), nullptr, 10));
        } else {
            return false;
        }
    }
    return (args.mode == "census" || args.mode == "harvest")
        && args.k_max > 0
        && args.k_max <= 24
        && args.n_max >= args.n_begin
        && args.n_begin >= 1;
}

void write_census_tsv(
    const std::string& path,
    const juggler_atlas::CensusTables& tables,
    const std::string& backend
) {
    std::ofstream out(path);
    out << "# schema=juggler-word-atlas/v1\n";
    out << "# k_max=" << tables.k_max << "\n";
    out << "# n_max=" << tables.n_max << "\n";
    out << "# n_begin=" << tables.n_begin << "\n";
    out << "# backend=" << backend << "\n";
    out << "# overflow_count=" << tables.overflow_count << "\n";
    out << "length\tpacked\tmin_n\tmin_expanding_n\n";
    const uint64_t missing = std::numeric_limits<uint64_t>::max();
    for (int length = 1; length <= tables.k_max; ++length) {
        const int count = 1 << length;
        for (int packed = 0; packed < count; ++packed) {
            const int idx = juggler_atlas::dense_index(length, static_cast<uint64_t>(packed));
            const uint64_t mn = tables.min_n[static_cast<size_t>(idx)];
            const uint64_t me = tables.min_exp[static_cast<size_t>(idx)];
            out << length << '\t' << packed << '\t';
            if (mn == missing) {
                out << '\t';
            } else {
                out << mn << '\t';
            }
            if (me == missing) {
                out << '\n';
            } else {
                out << me << '\n';
            }
        }
    }
}

void write_list(const std::string& path, uint64_t count, bool truncated, const std::vector<uint64_t>& ns) {
    std::ofstream ov(path);
    ov << "# overflow_count=" << count << "\n";
    ov << "# overflow_truncated=" << (truncated ? 1 : 0) << "\n";
    for (uint64_t n : ns) {
        ov << n << "\n";
    }
}

void write_harvest_tsv(
    const std::string& path,
    const juggler_atlas::HarvestTables& tables,
    const std::string& backend
) {
    std::ofstream out(path);
    out << "# schema=juggler-certificate-harvest/v1\n";
    out << "# k_max=" << tables.k_max << "\n";
    out << "# n_max=" << tables.n_max << "\n";
    out << "# n_begin=" << tables.n_begin << "\n";
    out << "# backend=" << backend << "\n";
    out << "# count_skip=" << tables.count_skip << "\n";
    out << "# count_e=" << tables.count_e << "\n";
    out << "# count_oe=" << tables.count_oe << "\n";
    out << "# count_ooee=" << tables.count_ooee << "\n";
    out << "# count_leftover=" << tables.count_leftover << "\n";
    out << "# count_uncapped=" << tables.count_uncapped << "\n";
    out << "# count_overflow=" << tables.count_overflow << "\n";
    out << "# overflow_truncated=" << (tables.overflow_truncated ? 1 : 0) << "\n";
    out << "# uncapped_truncated=" << (tables.uncapped_truncated ? 1 : 0) << "\n";
    out << "length\tpacked\tcount\tmin_n\n";
    const uint64_t missing = std::numeric_limits<uint64_t>::max();
    for (int length = 1; length <= tables.k_max; ++length) {
        const int count = 1 << length;
        for (int packed = 0; packed < count; ++packed) {
            const int idx = juggler_atlas::dense_index(length, static_cast<uint64_t>(packed));
            const uint64_t c = tables.hist[static_cast<size_t>(idx)];
            if (c == 0) {
                continue;
            }
            const uint64_t mn = tables.min_n[static_cast<size_t>(idx)];
            out << length << '\t' << packed << '\t' << c << '\t';
            if (mn == missing) {
                out << '\n';
            } else {
                out << mn << '\n';
            }
        }
    }
}

int run_census(const Args& args) {
    juggler_atlas::CensusTables tables;
    tables.k_max = args.k_max;
    tables.n_begin = args.n_begin;
    tables.n_max = args.n_max;
    std::string used = args.backend;
    if (args.backend == "cuda") {
#ifdef JUGGLER_ATLAS_CUDA
        if (!juggler_atlas::gpu_census(tables)) {
            std::cerr << "CUDA census failed\n";
            return 1;
        }
#else
        std::cerr << "juggler-atlas-census was built without CUDA\n";
        return 2;
#endif
    } else {
        used = "cpu";
        juggler_atlas::cpu_census(tables);
    }
    write_census_tsv(args.output, tables, used);
    write_list(args.output + ".overflow", tables.overflow_count, tables.overflow_truncated, tables.overflow_n);
    std::cout << "experiment_id=\n";
    std::cout << "configuration=k_max=" << args.k_max << ",backend=" << used << ",mode=census\n";
    std::cout << "input_range=" << args.n_begin << ".." << args.n_max << "\n";
    std::cout << "output_location=" << args.output << "\n";
    std::cout << "record_counts=table_size=" << tables.min_n.size()
              << ",overflow=" << tables.overflow_count
              << ",overflow_stored=" << tables.overflow_n.size()
              << ",overflow_truncated=" << (tables.overflow_truncated ? 1 : 0) << "\n";
    std::cout << "checksum=\n";
    return 0;
}

int run_harvest(const Args& args) {
    juggler_atlas::HarvestTables tables;
    tables.k_max = args.k_max;
    tables.n_begin = args.n_begin;
    tables.n_max = args.n_max;
    tables.overflow_cap = args.list_cap;
    std::string used = args.backend;
    if (args.backend == "cuda") {
#ifdef JUGGLER_ATLAS_CUDA
        if (!juggler_atlas::gpu_harvest(tables)) {
            std::cerr << "CUDA harvest failed\n";
            return 1;
        }
#else
        std::cerr << "juggler-atlas-census was built without CUDA\n";
        return 2;
#endif
    } else {
        used = "cpu";
        juggler_atlas::cpu_harvest(tables);
    }
    write_harvest_tsv(args.output, tables, used);
    write_list(args.output + ".overflow", tables.count_overflow, tables.overflow_truncated, tables.overflow_n);
    write_list(args.output + ".uncapped", tables.count_uncapped, tables.uncapped_truncated, tables.uncapped_n);
    std::cout << "experiment_id=\n";
    std::cout << "configuration=k_max=" << args.k_max << ",backend=" << used << ",mode=harvest\n";
    std::cout << "input_range=" << args.n_begin << ".." << args.n_max << "\n";
    std::cout << "output_location=" << args.output << "\n";
    std::cout << "record_counts=leftover=" << tables.count_leftover
              << ",e=" << tables.count_e
              << ",oe=" << tables.count_oe
              << ",ooee=" << tables.count_ooee
              << ",uncapped=" << tables.count_uncapped
              << ",overflow=" << tables.count_overflow
              << ",overflow_truncated=" << (tables.overflow_truncated ? 1 : 0)
              << ",uncapped_truncated=" << (tables.uncapped_truncated ? 1 : 0) << "\n";
    std::cout << "checksum=\n";
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    Args args;
    if (!parse_args(argc, argv, args)) {
        usage();
        return 2;
    }
    if (args.mode == "harvest") {
        return run_harvest(args);
    }
    return run_census(args);
}
