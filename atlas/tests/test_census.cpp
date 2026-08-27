#include "test_harness.hpp"

#include "../cpp/census.hpp"
#include "../cpp/packed_word.hpp"

#include <limits>

JA_TEST(Census, OOEMinRealizer) {
    juggler_atlas::CensusTables tables;
    tables.k_max = 3;
    tables.n_begin = 1;
    tables.n_max = 5;
    juggler_atlas::cpu_census(tables);
    const uint64_t packed = 0b011;
    const int idx = juggler_atlas::dense_index(3, packed);
    JA_EXPECT(tables.min_n[static_cast<size_t>(idx)] == 5);
    JA_EXPECT(tables.min_exp[static_cast<size_t>(idx)] == 5);
    JA_EXPECT(tables.overflow_count == 0);
}

JA_TEST(Census, MissingWordStaysUnset) {
    juggler_atlas::CensusTables tables;
    tables.k_max = 4;
    tables.n_begin = 1;
    tables.n_max = 10;
    juggler_atlas::cpu_census(tables);
    const uint64_t packed = 0b0100;  // EEOE
    const int idx = juggler_atlas::dense_index(4, packed);
    JA_EXPECT(tables.min_n[static_cast<size_t>(idx)] == std::numeric_limits<uint64_t>::max());
}
