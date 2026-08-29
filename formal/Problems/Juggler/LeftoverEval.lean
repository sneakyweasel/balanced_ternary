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

def wordOOOOOEE : List Branch :=
  [Branch.odd, Branch.odd, Branch.odd, Branch.odd, Branch.odd,
    Branch.even, Branch.even]

def wordOOOOEOE : List Branch :=
  [Branch.odd, Branch.odd, Branch.odd, Branch.odd, Branch.even,
    Branch.odd, Branch.even]

/-- Base comparison for the length-7 leftover tail: `n ≥ 14`. -/
theorem pow14_243_gt_two_pow422_pow15_128 :
    (2 : ℕ) ^ 422 * 15 ^ 128 < 14 ^ 243 := by
  native_decide

theorem cycleWordB_oooooee_lt14 :
    ∀ n : Fin 14, cycleWordB n.val wordOOOOOEE = false := by
  native_decide

theorem cycleWordB_ooooeoe_lt14 :
    ∀ n : Fin 14, cycleWordB n.val wordOOOOEOE = false := by
  native_decide

def wordOOOOOOEEE : List Branch :=
  [Branch.odd, Branch.odd, Branch.odd, Branch.odd, Branch.odd, Branch.odd,
    Branch.even, Branch.even, Branch.even]

/-- `(1 + 1/128)^{512} < 64`, used by the `n ≥ 128` tail for `OOOOOOEEE`. -/
theorem pow129_512_lt_64_mul_pow128_512 :
    (129 : ℕ) ^ 512 < 64 * 128 ^ 512 := by
  native_decide

theorem cycleWordB_ooooooeee_lt128 :
    ∀ n : Fin 128, cycleWordB n.val wordOOOOOOEEE = false := by
  native_decide

/-! Uniform two-even leftovers. Below `256` no start `n ≥ 2` realizes
seven consecutive odds, so only `k = 8` (EE) and `k = 8,9` (EOE)
need tables. -/

def sevenOdds : List Branch :=
  List.replicate 7 Branch.odd

def wordTwoEvenEE8 : List Branch :=
  List.replicate 6 Branch.odd ++ [Branch.even, Branch.even]

def wordTwoEvenEOE8 : List Branch :=
  List.replicate 5 Branch.odd ++
    [Branch.even, Branch.odd, Branch.even]

def wordTwoEvenEOE9 : List Branch :=
  List.replicate 6 Branch.odd ++
    [Branch.even, Branch.odd, Branch.even]

theorem followsB_seven_odds_of_lt256 :
    ∀ n : Fin 256, 2 ≤ n.val → followsB n.val sevenOdds = false := by
  native_decide

theorem cycleWordB_two_even_ee8_lt256 :
    ∀ n : Fin 256, cycleWordB n.val wordTwoEvenEE8 = false := by
  native_decide

theorem cycleWordB_two_even_eoe8_lt256 :
    ∀ n : Fin 256, cycleWordB n.val wordTwoEvenEOE8 = false := by
  native_decide

theorem cycleWordB_two_even_eoe9_lt256 :
    ∀ n : Fin 256, cycleWordB n.val wordTwoEvenEOE9 = false := by
  native_decide

end Problems.Juggler
