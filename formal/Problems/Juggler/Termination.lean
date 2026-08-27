import Problems.Juggler.Iteration

namespace Problems.Juggler

/-!
# Hitting 1

`ReachesOne` is the orbit predicate `∃ k, T^[k] n = 1`. This file does
not mention words or certificates. Finite seed identities live here as
examples, not as a map theorem.
-/

def ReachesOne (n : ℕ) : Prop :=
  ∃ k, floorPower^[k] n = 1

theorem reachesOne_one : ReachesOne 1 :=
  ⟨0, rfl⟩

theorem reachesOne_of_iterate {n m k : ℕ}
    (h : floorPower^[k] n = m) (hm : ReachesOne m) : ReachesOne n := by
  obtain ⟨j, hj⟩ := hm
  refine ⟨k + j, ?_⟩
  rw [Nat.add_comm, Function.iterate_add_apply, h, hj]

theorem floorPower_thirteen_reaches_one :
    (floorPower^[4] 13) = 1 := by
  native_decide

theorem two_reachesOne : ReachesOne 2 :=
  ⟨1, by
    change floorPower 2 = 1
    exact floorPower_two⟩

theorem four_reachesOne : ReachesOne 4 :=
  reachesOne_of_iterate (k := 1) (by
    change floorPower 4 = 2
    exact floorPower_four) two_reachesOne

theorem six_reachesOne : ReachesOne 6 :=
  reachesOne_of_iterate (k := 1) (by
    change floorPower 6 = 2
    exact floorPower_six) two_reachesOne

theorem eight_reachesOne : ReachesOne 8 :=
  reachesOne_of_iterate (k := 1) (by
    change floorPower 8 = 2
    exact floorPower_eight) two_reachesOne

theorem three_reachesOne : ReachesOne 3 :=
  ⟨6, by native_decide⟩

theorem five_reachesOne : ReachesOne 5 :=
  ⟨5, by native_decide⟩

theorem seven_reachesOne : ReachesOne 7 :=
  ⟨4, by native_decide⟩

theorem nine_reachesOne : ReachesOne 9 :=
  ⟨7, by native_decide⟩

theorem ten_reachesOne : ReachesOne 10 :=
  reachesOne_of_iterate (k := 1) (by
    change floorPower 10 = 3
    native_decide) three_reachesOne

theorem eleven_reachesOne : ReachesOne 11 :=
  ⟨4, by native_decide⟩

/-- Every positive residual strictly below `12` is `ReachesOne`.
This is a finite certificate, not a halt theorem. -/
theorem reachesOne_of_lt_twelve {y : ℕ} (hpos : 1 ≤ y) (hy : y < 12) :
    ReachesOne y := by
  match y with
  | 0 => omega
  | 1 => exact reachesOne_one
  | 2 => exact two_reachesOne
  | 3 => exact three_reachesOne
  | 4 => exact four_reachesOne
  | 5 => exact five_reachesOne
  | 6 => exact six_reachesOne
  | 7 => exact seven_reachesOne
  | 8 => exact eight_reachesOne
  | 9 => exact nine_reachesOne
  | 10 => exact ten_reachesOne
  | 11 => exact eleven_reachesOne
  | _ + 12 => omega

/-- A positive non-`ReachesOne` value cannot lie in `{1,…,11}`. -/
theorem non_reachesOne_ge_twelve {n : ℕ} (hn : 1 ≤ n) (hfail : ¬ReachesOne n) :
    12 ≤ n := by
  by_contra h
  exact hfail (reachesOne_of_lt_twelve hn (Nat.not_le.mp h))

/-- One even step into `{1,…,11}`: every even `n` with `1 ≤ n < 144`
is `ReachesOne`. Not a halt theorem. -/
theorem even_lt_sq_twelve_reachesOne {n : ℕ} (heven : n % 2 = 0)
    (hpos : 1 ≤ n) (hn : n < 144) : ReachesOne n := by
  have hsqrt : n.sqrt < 12 := by
    rw [Nat.sqrt_lt]
    simpa using hn
  have himg : floorPower n < 12 := by
    rw [floorPower_even_eq heven]
    exact hsqrt
  exact reachesOne_of_iterate (k := 1) rfl
    (reachesOne_of_lt_twelve (floorPower_pos hpos) himg)

end Problems.Juggler
