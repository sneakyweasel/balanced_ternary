import Problems.Juggler.LeftoverEval

namespace Problems.Juggler

/-!
Isolated `native_decide` table for the bunched leftover `O^a EOEOE`
on `4 ≤ a ≤ 6` and `n < 256`. Longer prefixes are seven-odd.
This is not a length-9 census and not the other bunched families.
-/

set_option maxHeartbeats 8000000

def threeEvenEOEOE (a : ℕ) : List Branch :=
  List.replicate a Branch.odd ++
    [Branch.even, Branch.odd, Branch.even, Branch.odd, Branch.even]

theorem cycleWordB_eoeoe_prefix_lt256 :
    ∀ n : Fin 256, ∀ a : Fin 3, 2 ≤ n.val →
      cycleWordB n.val (threeEvenEOEOE (a.val + 4)) = false := by
  native_decide

end Problems.Juggler
