#include "test_harness.hpp"

#include "../cpp/packed_word.hpp"

JA_TEST(PackedWord, DenseSize) {
    JA_EXPECT(juggler_atlas::dense_size(0) == 0);
    JA_EXPECT(juggler_atlas::dense_size(1) == 2);
    JA_EXPECT(juggler_atlas::dense_size(2) == 6);
    JA_EXPECT(juggler_atlas::dense_size(3) == 14);
    JA_EXPECT(juggler_atlas::dense_index(1, 0) == 0);
    JA_EXPECT(juggler_atlas::dense_index(1, 1) == 1);
    JA_EXPECT(juggler_atlas::dense_index(2, 0) == 2);
}

JA_TEST(PackedWord, UnpackAndRuns) {
    JA_EXPECT(juggler_atlas::unpack_word(3, 0b011) == "OOE");
    JA_EXPECT(juggler_atlas::odd_count(3, 0b011) == 2);
    JA_EXPECT(juggler_atlas::run_signature(3, 0b011) == "O2,E1");
    JA_EXPECT(juggler_atlas::unpack_word(4, 0b0100) == "EEOE");
}

JA_TEST(PackedWord, WordId) {
    JA_EXPECT(juggler_atlas::word_id(3, 3) == ((3ull << 32) | 3ull));
}
