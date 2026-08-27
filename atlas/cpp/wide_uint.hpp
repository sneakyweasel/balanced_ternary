#pragma once

#include <cstdint>

#ifdef __CUDACC__
#define JA_HD __host__ __device__ inline
#else
#define JA_HD inline
#endif

namespace juggler_atlas {

struct Wide8 {
    uint64_t d[8];
};

JA_HD void w8_zero(Wide8& a) {
    for (int i = 0; i < 8; ++i) {
        a.d[i] = 0;
    }
}

JA_HD void w8_from_u64(Wide8& a, uint64_t x) {
    w8_zero(a);
    a.d[0] = x;
}

JA_HD bool w8_is_zero(const Wide8& a) {
    for (int i = 0; i < 8; ++i) {
        if (a.d[i] != 0) {
            return false;
        }
    }
    return true;
}

JA_HD int w8_cmp(const Wide8& a, const Wide8& b) {
    for (int i = 7; i >= 0; --i) {
        if (a.d[i] < b.d[i]) {
            return -1;
        }
        if (a.d[i] > b.d[i]) {
            return 1;
        }
    }
    return 0;
}

JA_HD bool w8_gt_u64(const Wide8& a, uint64_t n) {
    for (int i = 1; i < 8; ++i) {
        if (a.d[i] != 0) {
            return true;
        }
    }
    return a.d[0] > n;
}

JA_HD void w8_add(Wide8& a, const Wide8& b) {
    uint64_t carry = 0;
    for (int i = 0; i < 8; ++i) {
        uint64_t x = a.d[i];
        uint64_t s = x + b.d[i];
        uint64_t c1 = static_cast<uint64_t>(s < x);
        uint64_t s2 = s + carry;
        uint64_t c2 = static_cast<uint64_t>(s2 < s);
        a.d[i] = s2;
        carry = c1 | c2;
    }
}

JA_HD bool w8_sub(Wide8& a, const Wide8& b) {
    uint64_t borrow = 0;
    for (int i = 0; i < 8; ++i) {
        uint64_t x = a.d[i];
        uint64_t y = b.d[i];
        uint64_t s = x - y;
        uint64_t b1 = static_cast<uint64_t>(x < y);
        uint64_t s2 = s - borrow;
        uint64_t b2 = static_cast<uint64_t>(s < borrow);
        a.d[i] = s2;
        borrow = b1 | b2;
    }
    return borrow == 0;
}

JA_HD void w8_shr1(Wide8& a) {
    uint64_t carry = 0;
    for (int i = 7; i >= 0; --i) {
        uint64_t next = a.d[i] << 63;
        a.d[i] = (a.d[i] >> 1) | carry;
        carry = next;
    }
}

JA_HD void w8_shr2(Wide8& a) {
    w8_shr1(a);
    w8_shr1(a);
}

JA_HD void mul_u64(uint64_t a, uint64_t b, uint64_t& lo, uint64_t& hi) {
#if defined(__SIZEOF_INT128__)
    unsigned __int128 p = static_cast<unsigned __int128>(a) * b;
    lo = static_cast<uint64_t>(p);
    hi = static_cast<uint64_t>(p >> 64);
#else
    const uint64_t a_lo = static_cast<uint32_t>(a);
    const uint64_t a_hi = a >> 32;
    const uint64_t b_lo = static_cast<uint32_t>(b);
    const uint64_t b_hi = b >> 32;
    const uint64_t p0 = a_lo * b_lo;
    const uint64_t p1 = a_lo * b_hi;
    const uint64_t p2 = a_hi * b_lo;
    const uint64_t p3 = a_hi * b_hi;
    const uint64_t mid = (p0 >> 32) + static_cast<uint32_t>(p1) + static_cast<uint32_t>(p2);
    lo = (p0 & 0xffffffffull) | (mid << 32);
    hi = p3 + (p1 >> 32) + (p2 >> 32) + (mid >> 32);
#endif
}

JA_HD bool w8_mul(const Wide8& a, const Wide8& b, Wide8& out) {
    uint64_t acc[16];
    for (int i = 0; i < 16; ++i) {
        acc[i] = 0;
    }
    for (int i = 0; i < 8; ++i) {
        if (a.d[i] == 0) {
            continue;
        }
        uint64_t carry = 0;
        for (int j = 0; j < 8; ++j) {
            uint64_t lo = 0;
            uint64_t hi = 0;
            mul_u64(a.d[i], b.d[j], lo, hi);
            const int k = i + j;
            uint64_t s = acc[k] + lo;
            uint64_t c = static_cast<uint64_t>(s < acc[k]);
            s += carry;
            c += static_cast<uint64_t>(s < carry);
            acc[k] = s;
            uint64_t t = acc[k + 1] + hi;
            uint64_t c2 = static_cast<uint64_t>(t < acc[k + 1]);
            t += c;
            c2 += static_cast<uint64_t>(t < c);
            acc[k + 1] = t;
            carry = c2;
            int m = k + 2;
            while (carry && m < 16) {
                uint64_t u = acc[m] + carry;
                carry = static_cast<uint64_t>(u < acc[m]);
                acc[m] = u;
                ++m;
            }
            if (carry) {
                return false;
            }
        }
    }
    for (int i = 8; i < 16; ++i) {
        if (acc[i] != 0) {
            return false;
        }
    }
    for (int i = 0; i < 8; ++i) {
        out.d[i] = acc[i];
    }
    return true;
}

JA_HD Wide8 w8_isqrt(Wide8 n) {
    Wide8 res;
    Wide8 bit;
    w8_zero(res);
    w8_zero(bit);
    bit.d[7] = 1ull << 62;
    while (w8_cmp(bit, n) > 0 && !w8_is_zero(bit)) {
        w8_shr2(bit);
    }
    while (!w8_is_zero(bit)) {
        Wide8 trial = res;
        w8_add(trial, bit);
        if (w8_cmp(n, trial) >= 0) {
            w8_sub(n, trial);
            w8_shr1(res);
            w8_add(res, bit);
        } else {
            w8_shr1(res);
        }
        w8_shr2(bit);
    }
    return res;
}

JA_HD Wide8 floor_power_w8(const Wide8& n, bool& overflow) {
    overflow = false;
    if ((n.d[0] & 1ull) == 0) {
        Wide8 copy = n;
        return w8_isqrt(copy);
    }
    Wide8 sq;
    if (!w8_mul(n, n, sq)) {
        overflow = true;
        Wide8 z;
        w8_zero(z);
        return z;
    }
    Wide8 cube;
    if (!w8_mul(sq, n, cube)) {
        overflow = true;
        Wide8 z;
        w8_zero(z);
        return z;
    }
    return w8_isqrt(cube);
}

JA_HD uint64_t floor_power_u64(uint64_t n) {
    Wide8 w;
    w8_from_u64(w, n);
    bool overflow = false;
    Wide8 r = floor_power_w8(w, overflow);
    return overflow ? 0 : r.d[0];
}

}  // namespace juggler_atlas
