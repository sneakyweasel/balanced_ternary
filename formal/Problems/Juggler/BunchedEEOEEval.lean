import Problems.Juggler.LeftoverEval

namespace Problems.Juggler

/-!
Isolated `native_decide` facts for the bunched leftover `O^a EEOE`.
The `a = 5` table is the coarse cutoff `n < 314`. The `a = 6`
table is `n < 16`. This is not a length-9 census and not the
other bunched families.
-/

set_option maxHeartbeats 8000000

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

end Problems.Juggler
