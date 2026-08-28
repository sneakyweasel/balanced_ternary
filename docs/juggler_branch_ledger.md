# Juggler finite-dynamics branch ledger

This appendix curates the branches used in the
[Juggler finite-dynamics paper](theory/juggler_finite_dynamics_note.md).
It is not a replacement for the theorem ledger. `Decision` reproduces the
terminal `PROMOTE | PARK | CLOSE` decision in each source dossier; combining
the branches into a paper does not retroactively change those decisions.

Evidence labels describe the strongest paper-relevant result, not every
statement in the branch.

| Theme | Branch and dossier | Decision | Strongest evidence | Strongest defensible outcome | Role in paper |
|---|---|---|---|---|---|
| Formal contraction | [Power composition](problems/juggler_power_composition.md) | PROMOTE | **EXACT — LEAN VERIFIED** | Every realized word obeys the one-sided power envelope; negative exponent gap forces contraction | Central theorem |
| Exact slack | [Global defect](problems/juggler_global_defect.md) | PROMOTE | **EXACT — LEAN VERIFIED** | Local floor remainders lift to the exact global-defect identity | Central theorem |
| Symbolic language | [Word language](problems/juggler_word_language.md) | CLOSE | **EXACT — LEAN VERIFIED** plus bounded census | Realizable-language factor closure survives; no extra PE grammar survives beyond the known block description in the tested families | Structural elimination |
| Computational apparatus | [Word Atlas](problems/juggler_word_atlas.md) | PARK | **COMPUTATIONALLY VERIFIED** | Exact-reference/native validated census with witnesses, continuations, factors, PE records, and manifests | Methodological centerpiece |
| Realization geometry | [Realization geometry](problems/juggler_realization_geometry.md) | CLOSE | **REFUTED** / **REPARAMETERIZATION** | Unary corridors and prefix holes are explained by scale and landing parity, not a new interval law | Geometric elimination |
| Residual state | [Residual-state sufficiency](problems/juggler_residual_state.md) | CLOSE | **REFUTED** within the stated finite family | Intrinsic future needs the current landing \(y\); incoming history does not supply a useful proper quotient | State elimination |
| Residual equivalence | [Residual minimization](problems/juggler_residual_minimize.md) | CLOSE | **COMPUTATIONALLY VERIFIED** / **REPARAMETERIZATION** | Finite-horizon class collapse is a shared halt word or finite-sample effect, not a new residual state | State elimination |
| Future quotient | [Future quotient](problems/juggler_future_quotient.md) | CLOSE | **REFUTED** within the stated signatures | Listed arithmetic projections do not predict bounded residual futures | State elimination |
| Defect aggregation | [Sum-rho](problems/juggler_sum_rho.md) | CLOSE | **REFUTED** | Naive accumulated remainders remain state-dependent; exact surviving laws are global-defect reparameterizations | State/global elimination |
| Persistent blocks | [Two-block residual](problems/juggler_two_block_residual.md) | PROMOTE | **REFUTED**, Lean-certified witness | \(365\to763\to1749\) via two `OOE` persistent expanding blocks refutes forced contraction after one block | Certified counterexample |
| Inverse geometry | [Backward geometry](problems/juggler_backward_geometry.md) | CLOSE | **EXACT — LEAN VERIFIED** cells plus finite tests | Repeated inversion adds no tested rank beyond nested exact cells and the reversed itinerary | Inverse elimination |
| Local cell quotient | [Cell hut](problems/juggler_cell_hut.md) | CLOSE | **REFUTED** within tested signatures | Wide-even/singleton-odd asymmetry is exact but does not define a simpler forward quotient | Inverse elimination |
| Word cylinders | [Preimage cylinders](problems/juggler_preimage_cylinders.md) | CLOSE | **EXACT — LEAN VERIFIED** counterexample | Exact cylinders are itinerary semantics; `OOE` cylinders can have opposite next parity | Inverse separator |
| Scale barrier | [Even scale barrier](problems/juggler_even_scale_barrier.md) | PROMOTE | **EXACT — LEAN VERIFIED** | Even runs obey a conditional scale barrier and finite-prefix normal form | Surviving exact structure |
| Progress coverage | [Progress coverage](problems/juggler_progress_coverage.md) | PROMOTE | **EXACT — LEAN VERIFIED** | Even and odd-to-even starts have automatic finite progress; any automatically unresolved start is odd-to-odd | Exact induction boundary |
| Finite residual progress | [Residual progress](problems/juggler_residual_progress.md) | PROMOTE | **EXACT — LEAN VERIFIED** | The residual class \(\{1,\ldots,11\}\) reaches \(1\), and even residuals below \(144\) are fatal | Certified finite landing class |
| First return | [First-return excursions](problems/juggler_first_return_excursions.md) | CLOSE | **REPARAMETERIZATION** | First-return maximality adds no law beyond first descent and the power envelope | Finite-path elimination |
| Adversarial paths | [Adversarial paths](problems/juggler_adversarial_paths.md) | CLOSE | **REPARAMETERIZATION** | Adversarial optimization recovers the known first-return boundary | Extremal elimination |
| Information complexity | [Information complexity](problems/juggler_information_complexity.md) | CLOSE | **REFUTED** as a growing-state law | Fixed-sample future precision does not grow after the short itinerary separates the sample | State elimination |
| Extremal control | [Extremal control](problems/juggler_extremal_control.md) | PARK | **EXACT — HUMAN PROOF** for the ideal model; **OBSERVATION** for realization | Ideal bang-bang maximizers are not uniformly realized by exact Juggler paths | Extremal boundary |
| Cycle extrema | [Cycle extrema](problems/juggler_cycle_extrema.md) | PROMOTE | **EXACT — LEAN VERIFIED** | Cycle minimum/maximum parity, square-scale demand, and superquadratic min-to-even prefixes | Partial cycle structure |
| Cycle scale closure | [Prefix-OOO extra scale](problems/juggler_cycle_ooo_scale.md) | CLOSE | **EXACT — LEAN VERIFIED** reparameterizations plus **REFUTED** scale claim | Minimum cannot end odd, but `OOOEOE` and `OOOOEE` remain unexcluded | Cycle boundary |
| Statistics | [Probabilistic drift](problems/juggler_probabilistic.md) | PARK | **OBSERVATION** | Mixed ensembles have negative log-log drift; hard paths are odd-rich; no pointwise exceptional-family theorem | Descriptive layer |
| Ambient discrepancy | [Odd-image discrepancy](problems/juggler_odd_image_discrepancy.md) | PARK | **EXACT — HUMAN PROOF** | The ambient odd-input sign sum satisfies \(|S_O(N)|\ll N^{5/6}\) | Analytic theorem |
| Dynamical transfer | [Parity discrepancy transfer](problems/juggler_parity_discrepancy_transfer.md) | CLOSE | **REFUTED** | Translation-uniform short-interval laws and automatic transfer to sparse generated images fail in the tested form | Analytic boundary |
| Acceleration | [Odd-to-odd acceleration](problems/juggler_accelerated.md) | CLOSE | **REPARAMETERIZATION** | Acceleration shortens notation but retains the same state-dependent blocks | Global elimination |

## Synthesis

The promoted branches provide exact finite structure: the power envelope,
global defect, certified persistent-block counterexample, scale barriers, and
cycle extrema. The parked Atlas, discrepancy, probabilistic, and extremal
branches remain reusable evidence or descriptive mathematics. The closed
branches supply negative knowledge: specified reductions either fail on
explicit witnesses, reproduce exact cell/itinerary semantics, or collapse only
on a bounded sample.

The common conclusion is deliberately limited:

> No pointwise termination mechanism was obtained from the tested finite
> compressions.

The ledger does not claim that all possible compressions fail.
