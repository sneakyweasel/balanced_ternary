import Problems.Juggler.LeftoverEval

namespace Problems.Juggler

/-!
Isolated `native_decide` table for the bunched leftover `O^a EOOEE`
on `4 ≤ a ≤ 6` and `n < 256`. Longer prefixes are seven-odd.
This is not a length-10 census and not the other four bunched
families.
-/

set_option maxHeartbeats 8000000

def threeEvenEOOEE (a : ℕ) : List Branch :=
  List.replicate a Branch.odd ++
    [Branch.even, Branch.odd, Branch.odd, Branch.even, Branch.even]

theorem cycleWordB_eooee_prefix_lt256 :
    ∀ n : Fin 256, ∀ a : Fin 3, 2 ≤ n.val →
      cycleWordB n.val (threeEvenEOOEE (a.val + 4)) = false := by
  native_decide

end Problems.Juggler
