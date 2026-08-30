import Problems.Juggler.LeftoverEval

namespace Problems.Juggler

/-!
Isolated `native_decide` facts for the bunched leftover `O^a EOEE`.
The `a = 5` table is the coarse cutoff `n < 314`. The `a = 6`
table is `n < 16`. This is not a length-9 census and not the
other five bunched families.
-/

set_option maxHeartbeats 8000000

def wordOOOOOEOEE : List Branch :=
  List.replicate 5 Branch.odd ++
    [Branch.even, Branch.odd, Branch.even, Branch.even]

def wordOOOOOOEOEE : List Branch :=
  List.replicate 6 Branch.odd ++
    [Branch.even, Branch.odd, Branch.even, Branch.even]

theorem cycleWordB_ooooo_eoee_lt314 :
    ∀ n : Fin 314, 2 ≤ n.val →
      cycleWordB n.val wordOOOOOEOEE = false := by
  native_decide

theorem cycleWordB_oooooo_eoee_lt16 :
    ∀ n : Fin 16, 2 ≤ n.val →
      cycleWordB n.val wordOOOOOOEOEE = false := by
  native_decide

theorem pow314_243_gt_two_pow422_succ_pow192 :
    (2 : ℕ) ^ 422 * 315 ^ 192 < 314 ^ 243 := by
  native_decide

theorem pow16_729_gt_two_pow1330_succ_pow384 :
    (2 : ℕ) ^ 1330 * 17 ^ 384 < 16 ^ 729 := by
  native_decide

end Problems.Juggler
