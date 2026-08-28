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

/-!
# Juggler paper barrel

Review object for the math note
`docs/theory/juggler_finite_dynamics_note.md`.

This file imports only the modules named by that note. It does not
copy proofs. Laboratory satellites stay in `Problems.Juggler` and are
not the review object.

Build from `formal/`:

```text
lake build Problems.JugglerPaper
```

The note's Lean-tagged theorems are:

* 2.1 `image_monotone_of_follows`
* 2.2 `power_bound_word`
* 2.3 `power_bound_contracts`
* 2.4 `global_defect_identity`
* 2.5 `global_defect_eq_zero_iff_localsTight`,
      `global_defect_eq_zero_implies_monochrome`,
      `power_bound_eq_iff_extremal`
* 2.6 `global_defect_append`
* 3.1 `cycle_word_formally_expanding`, `odd_cell_unique`,
      `cycleMin_not_end_odd`
* 3.2 `no_cycle_word_oooeoe`, `no_cycle_word_ooooee`
* 4.1 `even_finiteProgress`, `odd_even_finiteProgress`
* 4.2 `unresolved_is_odd_odd`
* 4.3 `reachesOne_of_lt_twelve`, `even_lt_sq_twelve_reachesOne`

`FiniteProgress` is a descent certificate: a realized word with image
strictly below the start, or with image `1`. Lean packages this as
`DescentCertificate`; the note uses the two-clause English form.

This barrel does not prove that every positive integer reaches `1`,
that every orbit meets a contracting word, or that all nontrivial
cycles are impossible. Theorem 5.1 is a human proof and is not here.
`FiniteCoeffStopConjecture` is a laboratory target, not a claim of
the note.
-/
