#include "test_harness.hpp"

#include "../cpp/wide_uint.hpp"

JA_TEST(JugglerMap, FloorPowerSeeds) {
    JA_EXPECT(juggler_atlas::floor_power_u64(1) == 1);
    JA_EXPECT(juggler_atlas::floor_power_u64(2) == 1);
    JA_EXPECT(juggler_atlas::floor_power_u64(4) == 2);
    JA_EXPECT(juggler_atlas::floor_power_u64(6) == 2);
    JA_EXPECT(juggler_atlas::floor_power_u64(7) == 18);
    JA_EXPECT(juggler_atlas::floor_power_u64(8) == 2);
}

JA_TEST(JugglerMap, OOEAtFive) {
    uint64_t n = 5;
    JA_EXPECT((n & 1ull) == 1);
    n = juggler_atlas::floor_power_u64(n);
    JA_EXPECT(n == 11);
    JA_EXPECT((n & 1ull) == 1);
    n = juggler_atlas::floor_power_u64(n);
    JA_EXPECT(n == 36);
    JA_EXPECT((n & 1ull) == 0);
    n = juggler_atlas::floor_power_u64(n);
    JA_EXPECT(n == 6);
}

JA_TEST(JugglerMap, PE365) {
    const uint64_t a = juggler_atlas::floor_power_u64(365);
    const uint64_t b = juggler_atlas::floor_power_u64(a);
    const uint64_t c = juggler_atlas::floor_power_u64(b);
    JA_EXPECT(c == 763);
}
