import Problems.Juggler.LeftoverEval

namespace Problems.Juggler

/-!
Isolated `native_decide` facts for the bunched leftover `O^a EOOEOE`.
The short-prefix table is `3 ≤ a ≤ 6` and `n < 256`. The `a = 3`
tight comparison starts at `n = 222`. This is not a length-9
census and not the other bunched families.
-/

set_option maxHeartbeats 8000000
set_option exponentiation.threshold 2048

def threeEvenEOOEOE (a : ℕ) : List Branch :=
  List.replicate a Branch.odd ++
    [Branch.even, Branch.odd, Branch.odd, Branch.even,
      Branch.odd, Branch.even]

theorem cycleWordB_eooeoe_prefix_lt256 :
    ∀ n : Fin 256, ∀ a : Fin 4, 2 ≤ n.val →
      cycleWordB n.val (threeEvenEOOEOE (a.val + 3)) = false := by
  native_decide

theorem pow40_9_lt_two_mul_pow39_9 :
    (40 : ℕ) ^ 9 < 2 * 39 ^ 9 := by
  native_decide

theorem pow222_243_gt_two_pow560_succ_pow171 :
    (2 : ℕ) ^ 560 * 223 ^ 171 < 222 ^ 243 := by
  native_decide

end Problems.Juggler
