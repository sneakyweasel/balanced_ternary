#include "census.hpp"
#include "packed_word.hpp"

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
    int k_max = 12;
    uint64_t n_max = 1000000;
    uint64_t n_begin = 1;
    std::string backend = "cpu";
    std::string output = "census.tsv";
};

void usage() {
    std::cerr
        << "juggler-atlas-census --k-max 12 --n-max 1000000 --n-begin 1 "
           "--backend cpu|cuda --output census.tsv\n";
}

bool parse_args(int argc, char** argv, Args& args) {
    for (int i = 1; i < argc; ++i) {
        const std::string key = argv[i];
        if (i + 1 >= argc) {
            return false;
        }
        const std::string val = argv[++i];
        if (key == "--k-max") {
            args.k_max = std::atoi(val.c_str());
        } else if (key == "--n-max") {
            args.n_max = static_cast<uint64_t>(std::strtoull(val.c_str(), nullptr, 10));
        } else if (key == "--n-begin") {
            args.n_begin = static_cast<uint64_t>(std::strtoull(val.c_str(), nullptr, 10));
        } else if (key == "--backend") {
            args.backend = val;
        } else if (key == "--output") {
            args.output = val;
        } else {
            return false;
        }
    }
    return args.k_max > 0 && args.n_max >= args.n_begin && args.n_begin >= 1;
}

void write_tsv(
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

}  // namespace

int main(int argc, char** argv) {
    Args args;
    if (!parse_args(argc, argv, args)) {
        usage();
        return 2;
    }
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
    write_tsv(args.output, tables, used);
    {
        std::ofstream ov(args.output + ".overflow");
        ov << "# overflow_count=" << tables.overflow_count << "\n";
        ov << "# overflow_truncated=" << (tables.overflow_truncated ? 1 : 0) << "\n";
        for (uint64_t n : tables.overflow_n) {
            ov << n << "\n";
        }
    }
    std::cout << "experiment_id=\n";
    std::cout << "configuration=k_max=" << args.k_max << ",backend=" << used << "\n";
    std::cout << "input_range=" << args.n_begin << ".." << args.n_max << "\n";
    std::cout << "output_location=" << args.output << "\n";
    std::cout << "record_counts=table_size=" << tables.min_n.size()
              << ",overflow=" << tables.overflow_count
              << ",overflow_stored=" << tables.overflow_n.size()
              << ",overflow_truncated=" << (tables.overflow_truncated ? 1 : 0) << "\n";
    std::cout << "checksum=\n";
    return 0;
}
