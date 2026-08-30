#include "test_harness.hpp"

#include "../cpp/harvest.hpp"
#include "../cpp/harvest_walk.hpp"
#include "../cpp/packed_word.hpp"
#include "../cpp/wide_uint.hpp"

JA_TEST(Harvest, FastPathSeeds) {
    uint64_t out = 0;
    JA_EXPECT(juggler_atlas::floor_power_u64_ok(1, out) && out == 1);
    JA_EXPECT(juggler_atlas::floor_power_u64_ok(2, out) && out == 1);
    JA_EXPECT(juggler_atlas::floor_power_u64_ok(4, out) && out == 2);
    JA_EXPECT(juggler_atlas::floor_power_u64_ok(5, out) && out == 11);
    JA_EXPECT(juggler_atlas::floor_power_u64_ok(7, out) && out == 18);
    JA_EXPECT(juggler_atlas::isqrt_u64(9) == 3);
    JA_EXPECT(juggler_atlas::isqrt_u128(81, 0) == 9);
}

JA_TEST(Harvest, ClassifyFixtures) {
    bool overflow = false;
    const auto even = juggler_atlas::walk_certificate(6, 20, overflow);
    JA_EXPECT(!overflow);
    JA_EXPECT(even.cls == juggler_atlas::HarvestClass::E);
    JA_EXPECT(even.length == 1);

    const auto oe = juggler_atlas::walk_certificate(7, 20, overflow);
    JA_EXPECT(oe.cls == juggler_atlas::HarvestClass::OE);
    JA_EXPECT(oe.length == 2);
    JA_EXPECT(oe.packed == 1ull);

    const auto ooee = juggler_atlas::walk_certificate(5, 20, overflow);
    JA_EXPECT(ooee.cls == juggler_atlas::HarvestClass::OOEE);
    JA_EXPECT(ooee.length == 4);
    JA_EXPECT(juggler_atlas::unpack_word(ooee.length, ooee.packed) == "OOEE");

    const auto leftover = juggler_atlas::walk_certificate(9, 20, overflow);
    JA_EXPECT(leftover.cls == juggler_atlas::HarvestClass::Leftover);
    JA_EXPECT(juggler_atlas::unpack_word(leftover.length, leftover.packed) == "OOEOE");
}

JA_TEST(Harvest, CpuWindow) {
    juggler_atlas::HarvestTables tables;
    tables.k_max = 20;
    tables.n_begin = 2;
    tables.n_max = 20;
    juggler_atlas::cpu_harvest(tables);
    JA_EXPECT(tables.count_e == 10);
    JA_EXPECT(tables.count_oe + tables.count_ooee + tables.count_leftover + tables.count_uncapped + tables.count_overflow == 9);
    JA_EXPECT(tables.count_skip == 0);
    const int idx = juggler_atlas::dense_index(5, 0b01011ull);
    JA_EXPECT(tables.hist[static_cast<size_t>(idx)] >= 1);
    JA_EXPECT(tables.min_n[static_cast<size_t>(idx)] == 9);
}
