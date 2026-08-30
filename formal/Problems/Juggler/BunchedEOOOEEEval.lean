import Problems.Juggler.LeftoverEval

namespace Problems.Juggler

/-!
Isolated `native_decide` facts for the bunched leftover `O^a EOOOEE`.
The short-prefix table is `3 ≤ a ≤ 6` and `n < 256`. The `a = 3`
tight comparison starts at `n = 197`. This is not a length-9
census and not the other bunched families.
-/

set_option maxHeartbeats 8000000
set_option exponentiation.threshold 2048

def threeEvenEOOOEE (a : ℕ) : List Branch :=
  List.replicate a Branch.odd ++
    [Branch.even, Branch.odd, Branch.odd, Branch.odd,
      Branch.even, Branch.even]

theorem cycleWordB_eoooee_prefix_lt256 :
    ∀ n : Fin 256, ∀ a : Fin 4, 2 ≤ n.val →
      cycleWordB n.val (threeEvenEOOOEE (a.val + 3)) = false := by
  native_decide

theorem pow40_27_lt_two_mul_pow39_27 :
    (40 : ℕ) ^ 27 < 2 * 39 ^ 27 := by
  native_decide

theorem two_pow38_mul_pow39_16_lt_pow24_27 :
    (2 : ℕ) ^ 38 * 39 ^ 16 < 24 ^ 27 := by
  native_decide

theorem pow197_729_gt_two_pow1650_succ_pow512 :
    (2 : ℕ) ^ 1650 * 198 ^ 512 < 197 ^ 729 := by
  native_decide

end Problems.Juggler
