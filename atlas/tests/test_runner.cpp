#include "test_harness.hpp"

int main() {
    int ran = 0;
    for (const auto& c : juggler_atlas_test::registry()) {
        ++ran;
        std::fprintf(stdout, "[ RUN      ] %s.%s\n", c.suite, c.name);
        c.fn();
        if (juggler_atlas_test::failures) {
            std::fprintf(stdout, "[  FAILED  ] %s.%s\n", c.suite, c.name);
        } else {
            std::fprintf(stdout, "[       OK ] %s.%s\n", c.suite, c.name);
        }
    }
    if (juggler_atlas_test::failures) {
        std::fprintf(stderr, "%d failure(s) in %d test(s)\n", juggler_atlas_test::failures, ran);
        return 1;
    }
    std::fprintf(stdout, "[  PASSED  ] %d test(s)\n", ran);
    return 0;
}
