import Problems.Juggler.Itinerary

namespace Problems.Juggler

/-! Isolated `native_decide` facts for leftover cycle exclusion. -/

set_option maxHeartbeats 2000000

def wordOOOOEE : List Branch :=
  [Branch.odd, Branch.odd, Branch.odd, Branch.odd, Branch.even, Branch.even]

def wordOOOEOE' : List Branch :=
  [Branch.odd, Branch.odd, Branch.odd, Branch.even, Branch.odd, Branch.even]

def cycleWordB (n : ℕ) (w : List Branch) : Bool :=
  followsB n w && (image n w == n) && decide (1 ≤ w.length)

theorem two_mul_pow256_gt_pow257 :
    (257 : ℕ) ^ 64 < 2 * 256 ^ 64 := by
  native_decide

theorem cycleWordB_oooeoe_lt256 :
    ∀ n : Fin 256, cycleWordB n.val wordOOOEOE' = false := by
  native_decide

theorem cycleWordB_ooooee_lt256 :
    ∀ n : Fin 256, cycleWordB n.val wordOOOOEE = false := by
  native_decide

end Problems.Juggler
