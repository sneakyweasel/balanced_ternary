#pragma once

#include <cstdio>
#include <vector>

namespace juggler_atlas_test {

struct Case {
    const char* suite;
    const char* name;
    void (*fn)();
};

inline std::vector<Case>& registry() {
    static std::vector<Case> cases;
    return cases;
}

struct Register {
    Register(const char* suite, const char* name, void (*fn)()) {
        registry().push_back({suite, name, fn});
    }
};

inline int failures = 0;

inline void expect(bool cond, const char* expr, const char* file, int line) {
    if (!cond) {
        std::fprintf(stderr, "FAIL %s:%d  %s\n", file, line, expr);
        ++failures;
    }
}

}  // namespace juggler_atlas_test

#define JA_EXPECT(cond) \
    ::juggler_atlas_test::expect(static_cast<bool>(cond), #cond, __FILE__, __LINE__)

#define JA_TEST(suite, name)                                    \
    static void suite##_##name();                               \
    static ::juggler_atlas_test::Register suite##_##name##_reg{ \
        #suite, #name, suite##_##name};                         \
    static void suite##_##name()
