import Problems.Juggler.Itinerary

namespace Problems.Juggler

/-! Isolated `native_decide` facts for leftover cycle exclusion. -/

set_option maxHeartbeats 8000000
set_option exponentiation.threshold 2048

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



/-!
## Bunched leftover tables

The six four-even bunched families, formerly the isolated
`Bunched*Eval` files. Isolation was for kernel timeouts, not
mathematics; one `maxHeartbeats` header covers them all.
-/

/-!
Isolated `native_decide` facts for the bunched leftover `O^a EOEE`.
The `a = 5` table is the coarse cutoff `n < 314`. The `a = 6`
table is `n < 16`. This is not a length-9 census and not the
other five bunched families.
-/


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

/-!
Isolated `native_decide` table for the bunched leftover `O^a EOOEE`
on `4 ≤ a ≤ 6` and `n < 256`. Longer prefixes are seven-odd.
This is not a length-10 census and not the other four bunched
families.
-/


def threeEvenEOOEE (a : ℕ) : List Branch :=
  List.replicate a Branch.odd ++
    [Branch.even, Branch.odd, Branch.odd, Branch.even, Branch.even]

theorem cycleWordB_eooee_prefix_lt256 :
    ∀ n : Fin 256, ∀ a : Fin 3, 2 ≤ n.val →
      cycleWordB n.val (threeEvenEOOEE (a.val + 4)) = false := by
  native_decide

/-!
Isolated `native_decide` facts for the bunched leftover `O^a EEOE`.
The `a = 5` table is the coarse cutoff `n < 314`. The `a = 6`
table is `n < 16`. This is not a length-9 census and not the
other bunched families.
-/


def wordOOOOOEEOE : List Branch :=
  List.replicate 5 Branch.odd ++
    [Branch.even, Branch.even, Branch.odd, Branch.even]

def wordOOOOOOEEOE : List Branch :=
  List.replicate 6 Branch.odd ++
    [Branch.even, Branch.even, Branch.odd, Branch.even]

theorem cycleWordB_ooooo_eeoe_lt314 :
    ∀ n : Fin 314, 2 ≤ n.val →
      cycleWordB n.val wordOOOOOEEOE = false := by
  native_decide

theorem cycleWordB_oooooo_eeoe_lt16 :
    ∀ n : Fin 16, 2 ≤ n.val →
      cycleWordB n.val wordOOOOOOEEOE = false := by
  native_decide

/-!
Isolated `native_decide` table for the bunched leftover `O^a EOEOE`
on `4 ≤ a ≤ 6` and `n < 256`. Longer prefixes are seven-odd.
This is not a length-9 census and not the other bunched families.
-/


def threeEvenEOEOE (a : ℕ) : List Branch :=
  List.replicate a Branch.odd ++
    [Branch.even, Branch.odd, Branch.even, Branch.odd, Branch.even]

theorem cycleWordB_eoeoe_prefix_lt256 :
    ∀ n : Fin 256, ∀ a : Fin 3, 2 ≤ n.val →
      cycleWordB n.val (threeEvenEOEOE (a.val + 4)) = false := by
  native_decide

/-!
Isolated `native_decide` facts for the bunched leftover `O^a EOOOEE`.
The short-prefix table is `3 ≤ a ≤ 6` and `n < 256`. The `a = 3`
tight comparison starts at `n = 197`. This is not a length-9
census and not the other bunched families.
-/

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

/-!
Isolated `native_decide` facts for the bunched leftover `O^a EOOEOE`.
The short-prefix table is `3 ≤ a ≤ 6` and `n < 256`. The `a = 3`
tight comparison starts at `n = 222`. This is not a length-9
census and not the other bunched families.
-/

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
