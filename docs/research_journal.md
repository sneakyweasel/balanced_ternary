# Research journal

Compact milestone entries copied from the existing repository record.
Milestone completion calendar dates are **not** present in the docs and
are not invented here. Local experiment manifests are timestamped
2026-08-21. Milestones 7 and 8 were never numbered.

## Milestone 1

- **Date:** not recorded
- **Objective:** Exact accelerated Collatz, BT bridge, 2-adic automaton
- **Hypotheses:** BT features may organise the dynamics
- **Major results:** Exact `T`, inverse tree, features, `TwoAdicDigitAutomaton`; images never 0 mod 3
- **Refuted ideas:** none recorded at this layer
- **Literature:** later compared in four-coordinate work
- **Next question:** word-level Collatz structure

## Milestone 2

- **Date:** not recorded
- **Objective:** Append-plus, transducers, valuation graph
- **Major results:** `BT(3n+1)=BT(n)+`; LSD `/2` and `/2^k`; unrestricted odd-part is not one rational transduction
- **Refuted ideas:** “odd-part is a single FST”
- **Next question:** cylinders and complexity

## Milestone 3

- **Date:** not recorded
- **Objective:** Valuation cylinders, languages, complexity
- **Major results:** Unique cylinders of density `2^{-K}`; DFA/entropy computational
- **Conjecture:** `N_k=2^k+1` (held for small `k`)
- **Next question:** affine itineraries

## Milestone 4

- **Date:** not recorded
- **Objective:** Affine exponent codes, realizers, order sensitivity
- **Major results:** Exact `T^m` formula; unique `R`; nested `R` monotone; `C` order law
- **Open:** exceptional itinerary compatibility
- **Next question:** zero-lift

## Milestone 5

- **Date:** not recorded
- **Objective:** Zero-lift dynamics
- **Major results:** Realizer iff stabilization iff eventual zero lifts; unique zero-lift successor
- **Conjecture:** sustained low `K_m/m` forces infinitely many positive lifts
- **Next question:** dual coding

## Milestone 6

- **Date:** not recorded
- **Objective:** Dual coding (R, lift digits, mixed-radix)
- **Major results:** Direct `R` formula; lift-digit formula; BT(R) suffix counterexample at `R=3`
- **Refuted ideas:** complete `BT(R)` determines next lift/valuation
- **Next question:** literature interface

## Unnamed (between 6 and 9): four-coordinate compatibility

- **Date:** not recorded
- **Objective:** Compare project coordinates with 2025–2026 literature
- **Major results:** Kramer `B_m=C`, `r ≡ R (mod 2^K)`; BT not an independent entropy
- **Refuted ideas:** `H_BT` strong independence
- **Literature:** Kramer, Eliahou–Verger-Gaugry, Rozier–Terracol, Cerdá

## Unnamed (between 6 and 9): affine-center geometry

- **Date:** not recorded
- **Objective:** Exact affine center `n_*`
- **Major results:** `n_*=C/D`, centered scaling identities
- **Refuted ideas:** `n_* ≤ R` as a general finite-code inequality (witness later pinned at 165)

## Milestone 9

- **Date:** not recorded
- **Objective:** OEIS `W` maps and commutators with `T`
- **Major results:** `W(3)=1`; `W` not globally involutive; `W∘T ≠ T∘W` at `n=3`
- **Refuted ideas:** `W` involution; `W(3n)=3W(n)`; realizer-reverse identities

## Milestone 10

- **Date:** not recorded (affine-center census artifacts 2026-08-21)
- **Objective:** Fixed-integer affine gap `G_m`
- **Major results:** `G` recurrence (Lean); **`n_* ≤ n` refuted at `n=165`, `m=17`**
- **Refuted ideas:** `n_* ≤ n` on contracting prefixes

## Milestone 11

- **Date:** not recorded
- **Objective:** Primitive exponent-code cycle languages
- **Major results:** Expanding periods excluded; `D|C`; bounded census `p≤6`, `k_i≤4` finds only `(2)`
- **Literature:** 2026 cycle preprints compared, not adopted as theorems
- **Next question:** exceptional non-contracting compatibility; `N_k`; cycles beyond the census

## Milestone 13

- **Date:** 2026-08-22
- **Objective:** Problem-independent balanced-ternary calculus (`D`, `I_a`, trit algebra, rewrite, `cmp3`/`select3`)
- **Hypotheses:** the trit and digit decomposition might generate more than a notation for unique expansions
- **Major results:** Lean-verified decomposition, sections, left-zero projection band, twisted product rule, addition carry as a `D`-law, `cmp3`/`select3` identities; innermost terminating rewrite strategy on `{D,I_a,S,N}`; information profiles reused from existing transducers
- **Refuted ideas:** ordinary Leibniz rule for `D`; Boolean algebra of trits; `S∘D = id` (already refuted, restated)
- **Literature:** Hayes 2001, Knuth vol. 2, Malinovsky — historical Setun only
- **Next question:** not started; do not auto-open a new milestone. Open rewrite question: unique NF for open operator-fragment terms

## Milestone 14

- **Date:** 2026-08-22
- **Objective:** Problem-independent balanced-ternary normalization theory on arbitrary integer coefficient vectors
- **Hypotheses:** the local carry `c = 3q + r` generates a terminating confluent rewrite whose NF is the canonical word; weighted L1 might be a rank; fused FMA is always cheaper; `D` commutes with normalize
- **Major results:** `CoeffWord` + abstract `→`; lex termination on `(|c_i|)`; Strategy A ≡ `encode(value)`; Lean value/step/NF and carry bound; FST classification by alphabet; add/mul/FMA value identities
- **Refuted ideas:** weighted `Σ |c_i|(3/2)^i` as a rank (`[2] → [-1,1]`); `D(normalize(P)) = normalize(D_coeff(P))` without a trit LSD; Strategy A/B rewrite-count equality on a small box
- **Literature:** Hayes, Knuth, Malinovsky remain the Setun fact sources; ISA normalize/FMA details stay sketches
- **Next question:** closed. Local confluence of the `i`/`i+1` critical pair is Lean-proved modulo `stripHigh` (`BTCalculus/Confluence.lean`). Do not auto-open a new milestone.

## Milestone 15

- **Date:** 2026-08-22
- **Objective:** Normalization-aware section differential calculus on `Z[x]` and coefficient words
- **Hypotheses:** naive `D_coeff` is `D`; `𝔇_a` lowers degree and obeys classical Leibniz/chain; same-index locality
- **Major results:** `hat D` (drop plus carry) is the total semantic coefficient derivative; `𝔇_a` closes on `Z[x]` with twisted Leibniz and branch-selecting composition; function-jet reconstruction; prefix locality for polynomials
- **Refuted ideas:** `D ∘ normalize = normalize ∘ D_coeff` (`[2]`); degree-lowering; classical Leibniz; classical chain; same-index output locality
- **Literature:** 3-section / Cartier / p-kernel **REPARAMETERIZATION**; balanced residue and normalization boundary are the project-specific layer. Outcome B with a C-layer.
- **Next question:** not started; do not auto-open a new milestone. Open question: minimized residual-state growth of `x^d` as a function of `k`

## Milestone 16

- **Date:** 2026-08-23
- **Objective:** Exact finite-horizon Myhill–Nerode residual automata and normalizer composition
- **Hypotheses:** sample minimization is `M_k`; prefix locality implies a small automaton; `x^2` collapses like `x^3`
- **Major results:** `≡_k` recursive characterization; `R_k(x^2)=(3^k-1)/2`; `M_k(x^2)=R_k` through `k=7` (conjecture); cascade `outputAlong` law and `M(f∘g)≤M(f)M(g)`; sample `7 ≠ 13` on `x^2` at `k=3`; bounded-`B` obstruction for `deg≥2`
- **Refuted ideas:** sample = Myhill–Nerode; locality ⇒ small automaton; bounded-`B` FST for unbounded residual coefficients
- **Literature:** residual 3-section transducers are standard automata on p-sections; the exact `M_k(x^d)` table and the sample-min counterexample are the project-specific measurements
- **Next question:** closed. Proved in Milestone 17: `M_k(x^2)=(3^k-1)/2`.

## Milestone 17

- **Date:** 2026-08-23
- **Objective:** Prove or refute `M_k(x^2)=(3^k-1)/2` for all `k`, with an explicit residual formula and the first higher-degree merge examples
- **Hypotheses:** every residual of `x^2` encodes its prefix injectively; distinct prefixes remain `≡_k`-separated; `x^3`/`x^4` merges are delayed distinctions rather than infinite equivalence
- **Major results:** closed form `f_w=3^{|w|}x^2+2p(w)x+DZ^{|w|}(p(w)^2)`; degree-`≤2` MN class is `(A,B,C) mod 3^k`; `M_k(x^2)=R_k(x^2)=(3^k-1)/2`; canonical probes `0^k`, `10^{k-1}`, `(-1)0^{k-1}`; first `x^3` merge at `k=2` and first `x^4` merge at `k=3`, both split at the next horizon
- **Refuted ideas:** last-layer `ρ`-triples as a complete invariant of `x^2`; `M_k(x^d)=R_k(x^d)` for `d≥3`; finite-horizon merge as infinite-state equality
- **Literature:** 3-section / Cartier residual automata remain the ambient language. The quadratic MN count and the explicit delayed-distinction pairs are project-specific.
- **Next question:** closed. Milestone 18: finite-horizon polynomial equivalence is function congruence modulo `3^k`, classified by Newton residues.

## Milestone 18

- **Date:** 2026-08-23
- **Objective:** Characterize polynomial function equivalence modulo `3^k`, the kernel of higher-degree residual merges
- **Hypotheses:** coefficientwise `3^k`-divisibility might still be necessary; `min v_3(c_j)` might be `τ-1`
- **Major results:** `f ≡_k g` iff `f` and `g` agree on `Z` modulo `3^k` (Lean); `I_k` is Newton-coefficientwise `3^k Z`, not `3^k Z[x]`; degree `≤2` recovers monomial residues; exact cubic criterion; first invisible polynomial `x^3-x`; `τ=1+min v_3(Δ^j h(0))`; Lean formalization of the `x^3` and `x^4` first merges
- **Refuted ideas:** coefficientwise divisibility as a necessary vanishing condition for `deg≥3`; `τ=1+min v_3(c_j)`
- **Literature:** Kempner 1921 / integer-valued polynomials are **REPARAMETERIZATION**. Project-specific layer: MN bridge, residual families, delayed-distinction formula
- **Next question:** closed. Milestone 19: image of the residual tree of `x^3` under `Φ_k` is the arithmetic map `F_k`; `M_k(x^3)=|Im F_k|`.

## Milestone 19

- **Date:** 2026-08-23
- **Objective:** Determine which Newton classes are reached by residuals of `x^3`, and from that `M_k(x^3)`
- **Hypotheses:** packed-prefix congruence might label the classes; `M_{k+1}=3M_k+1` might lift
- **Major results:** closed form `f_w=3^{2m}x^3+3^{m+1}p x^2+3p^2 x+DZ^m(p^3)`; Newton coordinates and section transition; `M_k(x^3)=|Im F_k|` for the explicit map `F_k(m,p)=Φ_k(f_{(m,p)})`; same-depth collision criterion; first merge is the depth-1 sign pair of `Φ_2`; shallow lower bound `(3^{r+1}-1)/2`; Lean file `CubicResidual.lean`
- **Refuted ideas:** Newton classes are congruence classes of `p(w)`; `M_{k+1}=3M_k+1`
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION. Project-specific layer: residual image of `x^3` under `Φ_k`
- **Next question:** closed. Milestone 20: fibres of `F_k` classified by the Newton hierarchy; no closed `M_k`.

## Milestone 20

- **Date:** 2026-08-23
- **Objective:** Classify the fibres of `F_k` and derive an exact formula or recurrence for `M_k(x^3)`
- **Hypotheses:** `N2` might imply `N1`; `N2+N1` might imply `N0`; all collisions might be sign pairs
- **Major results:** exact same-depth criterion `(N2,N1,N0)`; `N2` does not imply `N1`; `N2+N1` do not imply `N0`; `C_{k,m}=3^m` on `2m+1≤k` (Lean `N2` injection); cross-depth only when both `2m+1≥k`; sign-pair fibre theorem; deepest `0`-fibre is `3^{ceil((2k-1)/3)} | q`; zero spine for `m≥ceil(k/2)`; `M_k=sum C - spine overcount`; arithmetic image through `k=12` (`M_12=265352`)
- **Refuted ideas:** `N2 ⇒ N1`; `N2+N1 ⇒ N0`; every collision is `p ↔ -p`; `M_{k+1}=3M_k+1`
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 21: deepest-layer fibres classified; stratified `C_{k,k-1}`; no single-term formula.

## Milestone 21

- **Date:** 2026-08-23
- **Objective:** Exact fibre structure and count of the deepest `x^3` residual layer
- **Hypotheses:** `N2+N1` might collapse fibres to `p=±q`; every deepest fibre might be a full 3-adic coset; `C_{k,k-1}` might be a single-term formula
- **Major results:** deepest Newton simplification `N1≡3p^2`, `N2=N3=0`; fibre criterion `p^2≡q^2 (mod 3^{k-1})` and `D^{k-1}(p^3)` agreement; units collide only as sign pairs; zero fibre `3^{ceil((2k-1)/3)}|p` with Lean necessity and sufficiency; high-stratum cube-count `J(k,s)`; stratified `C_{k,k-1}=1+Σ I_{k,s}`; `C` through `k=14` (`C_{14,13}=1593644`); CLI `cubic-deepest`
- **Refuted ideas:** every deepest fibre is a full residue class (`{720,738}` at `k=8`); `p^3≡q^3 (mod 3^{2k-1})` is equivalent to the `N0` condition
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 22: first intermediate layer `m=k-2`; fibre criterion; horizon surplus; no single-term `C_{k,k-2}`.

## Milestone 22

- **Date:** 2026-08-23
- **Objective:** Exact fibre structure of the first intermediate `x^3` residual layer `m=k-2`, and whether it begins a depth-recursive theory
- **Hypotheses:** deepest-layer fibres might persist unchanged; `C_{k,k-2}` might equal `C_{k-1,k-2}` or `3 C_{k-1,k-3}`; `N2` alone might create the one-layer surplus; a scaling `p=3^s u` might renormalize onto a deepest-layer problem
- **Major results:** Newton simplification `N3=0`, `N2≡2·3^{k-1}p`, `N1≡3p^2+3^{k-1}p`; fibre criterion `p≡q (mod 3)` and `3^{k-1}|(p-q)(p+q+3^{k-2})` and `N0` agreement; `N2` has 3 classes; `N2+N1` do not imply `N0`; unit signs always split under horizon lift; surplus `Δ_k=C_{k,k-2}-C_{k-1,k-2}` accounted by that refinement; `C` through `k=14` (`C_{14,12}=531230`); CLI `cubic-layer`; Lean `CubicIntermediateLayer.lean`
- **Refuted ideas:** `C_{k,k-2}=C_{k-1,k-2}`; `C_{k,k-2}=3 C_{k-1,k-3}`; `N2+N1 ⇒ N0`; `N2` alone explains `Δ_k`; literal renormalization onto `F_{k'}(k'-1,u)`
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 23: general `N2` visibility `p mod 3^r`; `r=2` fibre criterion; `N1` is not the next trit.

## Milestone 23

- **Date:** 2026-08-23
- **Objective:** Determine what Newton coordinates expose at depth deficit `r=2` (`m=k-3`), and whether `r ↦ p mod 3^r` is a theorem
- **Hypotheses:** `N2` sees `p mod 9`; the pattern may be a general visibility law; `N1` might reveal the next trit; `r=2` might be qualitatively new
- **Major results:** `N2 ≡ 2·3^{k-2}p` (`k≥5`); visibility `N2` iff `p≡q (mod 9)` (`k≥3`); general law `N2` iff `p≡q (mod 3^r)` at `m=k-1-r` (`r+1≤k`); fibre criterion `C_{k,2}`; `N1` after `N2` is `3^{k-3}|δ(p+q+3^{k-3})`, forcing unit-residue singletons; signs require `9|p`; `N2` has 9 classes for `k≥5`; uncompressed through `k=8`; first collision at `k=9`; `C` through `k=14` (`C_{14,11}=177083`); CLI `--depth-deficit 2`; Lean `CubicDeficitTwo.lean`
- **Refuted ideas:** `N2+N1 ⇒ N0`; `N1` reveals the next trit uniformly; `r=2` is only a digit increment of the whole Newton tower
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 24: after `N2`, `N1` separates every `v3(p)<r`; nontrivial fibres lie in `3^r Z`.

## Milestone 24

- **Date:** 2026-08-23
- **Objective:** Prove the general `N1` refinement after the depth-deficit `N2` filter, and characterize the surviving `3^r Z` locus
- **Hypotheses:** after `N2` equality, `v3(p)<r` forces `N1` to separate `p` from every other prefix; nontrivial `N2+N1` fibres lie in `3^r Z`; the high-valuation locus may rescale
- **Major results:** exact post-`N2` law `3^{k-1-r}|δ(p+q+3^m)`; unit injectivity for every `r≥1`; valuation-stratification theorem on `P_m`; sign pairs iff `3^r|p`; partial recursion `N1(3^r u)` reduces to deepest `N1` at horizon `k-2r` when `k≥2r+2`; CLI `n1-strata` / `n1-fibre`; Lean `CubicN1Valuation.lean`
- **Refuted ideas:** unit injectivity at `r=0`; that `3^r|p` is sufficient for a merge; that the remaining locus is a full recursive copy of the original deficit-`r` problem
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 25: two-regime `N0` scaling; not a standard smaller residual.

## Milestone 25

- **Date:** 2026-08-23
- **Objective:** Determine the exact recursive structure of `D^m((3^r u)^3)` after the `N2+N1` locus `3^r|p`
- **Hypotheses:** `D` strips `3^{3r}`; the remainder might be a smaller cubic residual, perhaps at the Milestone-24 `N1` horizon `k-2r`
- **Major results:** two-regime identity `3^{3r-m} u^3` vs `D^{m-3r}(u^3)`; equivalent to `k≤4r+1` vs `k≥4r+1`; sign pairs survive `N0` iff `3^k|N0`; valuation threshold `3 v3(p)=m`; visibility bound `s=max(1,t+k-1)`; CLI `n0-reduction` / `n0-fibre`; Lean `CubicN0Reduction.lean`
- **Refuted ideas:** stripped `N0` is a standard residual instance; `N0` and scaled `N1` share the deepest problem at horizon `k-2r`; width `k-1-2r` equals remaining depth `k-1-4r` for `r≥1`
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 26: mismatched-width cubic quotient `Q_{t,K,W}`; exact reconstruction criterion; extra `2r` trits visible through cubic carry.

## Milestone 26

- **Date:** 2026-08-23
- **Objective:** Exact arithmetic of the mismatched-width cubic quotient `Q_{t,K,W}(u)=D^t(u^3) mod 3^K` on `u ∈ P_W`, the independent `N0` core after Milestones 23–25
- **Hypotheses:** equality might reduce to `u^3 ≡ v^3 (mod 3^{t+K})`; input precision might be `t+K-1` as a fibre law; the extra `2r` trits might be invisible to `D^t`; `Q` might still be a smaller residual machine
- **Major results:** reconstruction criterion `Q(u)=Q(v)` iff `3^{t+K}` divides `u^3-v^3-Δbal_t`; cube-mod sufficient not necessary unless discarded digits agree; two-regime entry `k ≶ 4r+1`; unit opposite-residue branch has no extra `3` in `v3(u^3-v^3)`; high-trit identity `D^t((a+3^t b)^3)=D^t(a^3)+3a^2b+…`; on cubic parameters `t+K-1=2W`; CLI `cubic-quotient` / `cubic-quotient-fibre` / `compare-cubic-quotient`; Lean `MismatchedCubicQuotient.lean`
- **Refuted ideas:** `Q` is an ordinary residual; extra width is invisible; `Q`-equality is a pure residue relation `u ≡ v (mod 3^s)`
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 27: no compact residue/valuation/`B_t` invariant; family `1+3^t b` forces `W-t` extra trits.

## Milestone 27

- **Date:** 2026-08-23
- **Objective:** Decide whether `Q_{t,K,W}` admits a compact exact invariant
- **Hypotheses:** a residue/valuation/sign/`B_t` or two-scale `(a,b)` summary might classify fibres; `B_t` itself might be the growing obstruction
- **Major results:** two-scale expansion is the working equation; `B_t` is determined by `u mod 3^{max(1,t-1)}`; on `1+3^t b`, `Q`-equality is `b ≡ c (mod 3^{K-1})`; any `Ψ` constant on that family needs `≥ W-t` extra trits; high valuation still collapses to `0`; CLI `cubic-quotient-invariant` / `cubic-quotient-compare`; Lean `MismatchedCubicInvariant.lean`; Residual Explorer Q card
- **Refuted ideas:** bounded `Ψ1`–`Ψ4` classify `Q`; `B_t` is an incompressible independent jet; `Ψ5` with `β < K-1` is sufficient on units
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Decision:** Outcome C. Stop the Q-classification line; do not invent further fibre types. Next mathematical direction is not a new Q-taxonomy.

## Consolidation (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Make the laboratory match its actual frontier: general `bt.calculus`, cubic fibres in `research.residuals`, one Newton-stratum theorem, generated ledger, CI
- **Major results:** package split; `NewtonStratum.lean`; `acceleratedT` well-defined; quadratic `M_k(x^2)` ledger rows retagged to Lean; docs reading path no longer Collatz-first
- **Deferred:** `BTA-product` (`M_k` cardinality is not a Lean object); `BTJ-degree` (Mathlib 4.19 degree lemmas were not a short proof); Lake package rename; `formal/Automata/` placeholder
- **Next question:** closed by Milestone 27. Do not auto-open a further Q-taxonomy milestone.

## Milestone 28

- **Date:** 2026-08-23
- **Objective:** Exact Myhill–Nerode count \(M_k(x^3)\) by image cardinality, not by a further \(Q\)-taxonomy
- **Hypotheses:** same-depth \(C_{k,m}\) splits into an injective \(v_3(p)<r\) region plus a \(P_W\) core image; unexhausted cores collapse only on the zero fibre; cross-depth overlap is the zero spine plus a short list of nonzero families; a polynomial-time closed formula may exist
- **Major results:** master identity \(M_k=|\cup_m\mathrm{Im}\,F_k|\); easy count \(3^m-3^{m-r}\); core domain \(u\in P_W\); \(C=E+|\mathrm{core}|\); unexhausted formula \(C=3^m-Z+1\); unit \(G_a\) law \(b\equiv c\pmod{3^{K-1}}\); \(N_3\)-gated algorithm for \(M_k\); zero spine is not the only overlap; exact table through \(k=14\) (\(M_{14}=2390443\)); CLI `x3-states` / `x3-layer-count`; Lean `XCubeStateComplexity.lean`
- **Refuted ideas:** that \(\sum C\) minus the zero-spine overcount equals \(M_k\); that \(N_0\) determines \(N_1\) on the exhausted core; that the exact count is polynomial in \(k\) by this arithmetic (deepest layer is still \(P_{k-1}\))
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Decision:** not closed. Remaining obstruction: exhausted joint image \(|(N_1,Q)(P_W)|\) and the exact nonzero cross-depth families.

