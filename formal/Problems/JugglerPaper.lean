import Problems.Juggler.Dynamics
import Problems.Juggler.Iteration
import Problems.Juggler.Termination
import Problems.Juggler.Itinerary
import Problems.Juggler.WordStats
import Problems.Juggler.Envelope
import Problems.Juggler.Equality
import Problems.Juggler.Defect
import Problems.Juggler.GlobalDefect
import Problems.Juggler.Cells
import Problems.Juggler.Certificates
import Problems.Juggler.Progress
import Problems.Juggler.Cycles
import Problems.Juggler.LeftoverEval
import Problems.Juggler.LeftoverCycles
import Problems.Juggler.SmallCycleCensus
import Problems.Juggler.NormalizedDefect
import Problems.Juggler.ExpansionSlack
import Problems.Juggler.NearTightScale

/-!
# Juggler paper barrel (Paper A)

Review object for the finite-dynamics note
`docs/theory/juggler_finite_dynamics_note.md`.

This file imports only the modules named by that note. It does not
copy proofs. Laboratory satellites stay in `Problems.Juggler` and are
not the review object. Certificates and Cycles still compile their
existing dependencies (`FirstPassage`, `Collapse`, `Residuals`); those
files are not imported here as review targets.

The exact floor reductions used by the companion discrepancy
manuscript (`GapCells.lean`) are not part of this review object.

Build from `formal/`:

```text
lake build Problems.JugglerPaper
```

The note's Lean-tagged theorems are listed in its Appendix A:

* 2.1 `image_monotone_of_follows`
* 2.2 `power_bound_word`
* 2.3 `power_bound_contracts`
* 2.4 `global_defect_identity`
* 2.5 `global_defect_eq_zero_iff_localsTight`,
      `global_defect_eq_zero_implies_monochrome`,
      `power_bound_eq_iff_extremal`
* 2.6 `global_defect_append`
* 2.7 `image_eq_start_defectRatio`, with the per-step scale bound
      `one_plus_eta_lt_succ_sq`
* 3.1 `odd_cell_unique`
* 3.2 `cycle_word_formally_expanding`, `cycleMin_not_end_odd`,
      `square_scale_superquadratic`, `cycleMin_to_even_superquadratic`
* 3.3 `lower_growth_word`
* 3.4 `oo_suffix_threshold`, `ooo_suffix_threshold`,
      `threshold_inherits_odd_append`
* 3.5 `no_cycle_word_oooeoe`, `no_cycle_word_ooooee`
* 3.6 `no_cycle_word_length_le_six`, with components
      `no_cycle_word_replicate_odd`, `cycleWord_exists_even_terminating`,
      `no_cycle_word_len_six_ends_even`, `no_cycle_word_oooeoe`,
      `no_cycle_word_ooooee`
* 3.7 `no_cycle_word_ooooeoe`, `no_cycle_word_oooooee`
* 3.8 `no_cycle_word_length_le_seven`, with components
      `no_cycle_word_len_seven_ends_even`, `no_cycle_word_ooeoooe`,
      `no_cycle_word_oooeooe`
* 4.1 `even_finiteProgress`, `odd_even_finiteProgress`
* no certificate implies odd-to-odd:
      `no_finiteProgress_implies_odd_odd`
* §4  `four_block_pe_1999` (certified four-block expanding chain)

`FiniteProgress` is a descent certificate: a realized word with image
strictly below the start. Lean packages this as `DescentCertificate`.

This barrel does not prove that every positive integer reaches `1`,
that every orbit meets a contracting word, or that all nontrivial
cycles are impossible. The cycle census stops at length seven;
length eight and beyond is open.
`FiniteCoeffStopConjecture` is a laboratory target, not a claim of
the note.
-/
