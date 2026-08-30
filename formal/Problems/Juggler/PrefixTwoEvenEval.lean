import Problems.Juggler.LeftoverEval

namespace Problems.Juggler

/-!
Isolated `native_decide` tables: no start `y < 256` follows a short
two-even leftover and lands in `[2, y]`. Longer leftovers are
seven-odd. Not a length-8 census and not a halt theorem.
-/

set_option maxHeartbeats 8000000

def returnsIntoB (y : ℕ) (w : List Branch) : Bool :=
  followsB y w && decide (2 ≤ image y w) && decide (image y w ≤ y)

theorem returnsIntoB_ooooee_lt256 :
    ∀ y : Fin 256, 2 ≤ y.val → returnsIntoB y.val wordOOOOEE = false := by
  native_decide

theorem returnsIntoB_oooooee_lt256 :
    ∀ y : Fin 256, 2 ≤ y.val → returnsIntoB y.val wordOOOOOEE = false := by
  native_decide

theorem returnsIntoB_two_even_ee8_lt256 :
    ∀ y : Fin 256, 2 ≤ y.val →
      returnsIntoB y.val wordTwoEvenEE8 = false := by
  native_decide

theorem returnsIntoB_oooeoe_lt256 :
    ∀ y : Fin 256, 2 ≤ y.val → returnsIntoB y.val wordOOOEOE' = false := by
  native_decide

theorem returnsIntoB_ooooeoe_lt256 :
    ∀ y : Fin 256, 2 ≤ y.val → returnsIntoB y.val wordOOOOEOE = false := by
  native_decide

theorem returnsIntoB_two_even_eoe8_lt256 :
    ∀ y : Fin 256, 2 ≤ y.val →
      returnsIntoB y.val wordTwoEvenEOE8 = false := by
  native_decide

theorem returnsIntoB_two_even_eoe9_lt256 :
    ∀ y : Fin 256, 2 ≤ y.val →
      returnsIntoB y.val wordTwoEvenEOE9 = false := by
  native_decide

end Problems.Juggler
