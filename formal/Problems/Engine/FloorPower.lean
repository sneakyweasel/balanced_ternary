import Mathlib.Data.Nat.Sqrt
import Mathlib.Tactic

namespace Problems.Engine

/-!
Exact identities for the even/odd floor-power map.
These statements are the problem definition and a finite seed orbit.
They are KNOWN. They are not a halt theorem on all positive integers.
-/

/-- Even `n` maps to `Nat.sqrt n`; odd `n` maps to `Nat.sqrt (n^3)`. -/
def floorPower (n : ℕ) : ℕ :=
  if n % 2 = 0 then n.sqrt else (n * n * n).sqrt

theorem floorPower_one : floorPower 1 = 1 := by
  native_decide

theorem floorPower_thirteen_step : floorPower 13 = 46 := by
  native_decide

/-- Packet seed `13` reaches `1` in four steps. Not a map theorem. -/
theorem floorPower_thirteen_reaches_one :
    (floorPower^[4] 13) = 1 := by
  native_decide

end Problems.Engine
