# Research journal

Compact milestone entries copied from the existing repository record.
Milestone completion calendar dates are **not** present in the docs and
are not invented here. Local experiment manifests are timestamped
2026-08-21. Milestones 7 and 8 were never numbered.

Every entry ends in a decision: `PROMOTE`, `PARK`, or `CLOSE`
([methodology.md](methodology.md)). Entries that predate the vocabulary
carry a decision derived from their own recorded next question — nothing
is restated or upgraded. The retired *Outcome A / B / C* labels map to
`PROMOTE` / `PARK` / `CLOSE`.

## Milestone 1

- **Date:** not recorded
- **Objective:** Exact accelerated Collatz, BT bridge, 2-adic automaton
- **Hypotheses:** BT features may organise the dynamics
- **Major results:** Exact `T`, inverse tree, features, `TwoAdicDigitAutomaton`; images never 0 mod 3
- **Refuted ideas:** none recorded at this layer
- **Literature:** later compared in four-coordinate work
- **Next question:** word-level Collatz structure
- **Decision:** PROMOTE (taken up by Milestone 2)

## Milestone 2

- **Date:** not recorded
- **Objective:** Append-plus, transducers, valuation graph
- **Major results:** `BT(3n+1)=BT(n)+`; LSD `/2` and `/2^k`; unrestricted odd-part is not one rational transduction
- **Refuted ideas:** “odd-part is a single FST”
- **Next question:** cylinders and complexity
- **Decision:** PROMOTE (taken up by Milestone 3)

## Milestone 3

- **Date:** not recorded
- **Objective:** Valuation cylinders, languages, complexity
- **Major results:** Unique cylinders of density `2^{-K}`; DFA/entropy computational
- **Conjecture:** `N_k=2^k+1` (held for small `k`)
- **Next question:** affine itineraries
- **Decision:** PROMOTE (taken up by Milestone 4)

## Milestone 4

- **Date:** not recorded
- **Objective:** Affine exponent codes, realizers, order sensitivity
- **Major results:** Exact `T^m` formula; unique `R`; nested `R` monotone; `C` order law
- **Open:** exceptional itinerary compatibility
- **Next question:** zero-lift
- **Decision:** PROMOTE (taken up by Milestone 5)

## Milestone 5

- **Date:** not recorded
- **Objective:** Zero-lift dynamics
- **Major results:** Realizer iff stabilization iff eventual zero lifts; unique zero-lift successor
- **Conjecture:** sustained low `K_m/m` forces infinitely many positive lifts
- **Next question:** dual coding
- **Decision:** PROMOTE (taken up by Milestone 6)

## Milestone 6

- **Date:** not recorded
- **Objective:** Dual coding (R, lift digits, mixed-radix)
- **Major results:** Direct `R` formula; lift-digit formula; BT(R) suffix counterexample at `R=3`
- **Refuted ideas:** complete `BT(R)` determines next lift/valuation
- **Next question:** literature interface
- **Decision:** PROMOTE (taken up by the four-coordinate comparison)

## Unnamed (between 6 and 9): four-coordinate compatibility

- **Date:** not recorded
- **Objective:** Compare project coordinates with 2025–2026 literature
- **Major results:** Kramer `B_m=C`, `r ≡ R (mod 2^K)`; BT not an independent entropy
- **Refuted ideas:** `H_BT` strong independence
- **Literature:** Kramer, Eliahou–Verger-Gaugry, Rozier–Terracol, Cerdá
- **Decision:** CLOSE (BT as an independent solving coordinate is refuted)

## Unnamed (between 6 and 9): affine-center geometry

- **Date:** not recorded
- **Objective:** Exact affine center `n_*`
- **Major results:** `n_*=C/D`, centered scaling identities
- **Refuted ideas:** `n_* ≤ R` as a general finite-code inequality (witness later pinned at 165)
- **Decision:** PROMOTE (taken up by Milestone 10)

## Milestone 9

- **Date:** not recorded
- **Objective:** OEIS `W` maps and commutators with `T`
- **Major results:** `W(3)=1`; `W` not globally involutive; `W∘T ≠ T∘W` at `n=3`
- **Refuted ideas:** `W` involution; `W(3n)=3W(n)`; realizer-reverse identities
- **Decision:** CLOSE (the `W` identities are refuted; no further `W` census)

## Milestone 10

- **Date:** not recorded (affine-center census artifacts 2026-08-21)
- **Objective:** Fixed-integer affine gap `G_m`
- **Major results:** `G` recurrence (Lean); **`n_* ≤ n` refuted at `n=165`, `m=17`**
- **Refuted ideas:** `n_* ≤ n` on contracting prefixes
- **Decision:** CLOSE (the inequality is refuted at `n=165`, `m=17`)

## Milestone 11

- **Date:** not recorded
- **Objective:** Primitive exponent-code cycle languages
- **Major results:** Expanding periods excluded; `D|C`; bounded census `p≤6`, `k_i≤4` finds only `(2)`
- **Literature:** 2026 cycle preprints compared, not adopted as theorems
- **Next question:** exceptional non-contracting compatibility; `N_k`; cycles beyond the census
- **Decision:** PARK (the three questions are registered conjectures; none was taken up)

## Milestone 13

- **Date:** 2026-08-22
- **Objective:** Problem-independent balanced-ternary calculus (`D`, `I_a`, trit algebra, rewrite, `cmp3`/`select3`)
- **Hypotheses:** the trit and digit decomposition might generate more than a notation for unique expansions
- **Major results:** Lean-verified decomposition, sections, left-zero projection band, twisted product rule, addition carry as a `D`-law, `cmp3`/`select3` identities; innermost terminating rewrite strategy on `{D,I_a,S,N}`; information profiles reused from existing transducers
- **Refuted ideas:** ordinary Leibniz rule for `D`; Boolean algebra of trits; `S∘D = id` (already refuted, restated)
- **Literature:** Hayes 2001, Knuth vol. 2, Malinovsky — historical Setun only
- **Next question:** not started; do not auto-open a new milestone. Open rewrite question: unique NF for open operator-fragment terms
- **Decision:** PARK

## Milestone 14

- **Date:** 2026-08-22
- **Objective:** Problem-independent balanced-ternary normalization theory on arbitrary integer coefficient vectors
- **Hypotheses:** the local carry `c = 3q + r` generates a terminating confluent rewrite whose NF is the canonical word; weighted L1 might be a rank; fused FMA is always cheaper; `D` commutes with normalize
- **Major results:** `CoeffWord` + abstract `→`; lex termination on `(|c_i|)`; Strategy A ≡ `encode(value)`; Lean value/step/NF and carry bound; FST classification by alphabet; add/mul/FMA value identities
- **Refuted ideas:** weighted `Σ |c_i|(3/2)^i` as a rank (`[2] → [-1,1]`); `D(normalize(P)) = normalize(D_coeff(P))` without a trit LSD; Strategy A/B rewrite-count equality on a small box
- **Literature:** Hayes, Knuth, Malinovsky remain the Setun fact sources; ISA normalize/FMA details stay sketches
- **Next question:** closed. Local confluence of the `i`/`i+1` critical pair is Lean-proved modulo `stripHigh` (`BTCalculus/Confluence.lean`). Do not auto-open a new milestone.
- **Decision:** CLOSE

## Milestone 15

- **Date:** 2026-08-22
- **Objective:** Normalization-aware section differential calculus on `Z[x]` and coefficient words
- **Hypotheses:** naive `D_coeff` is `D`; `𝔇_a` lowers degree and obeys classical Leibniz/chain; same-index locality
- **Major results:** `hat D` (drop plus carry) is the total semantic coefficient derivative; `𝔇_a` closes on `Z[x]` with twisted Leibniz and branch-selecting composition; function-jet reconstruction; prefix locality for polynomials
- **Refuted ideas:** `D ∘ normalize = normalize ∘ D_coeff` (`[2]`); degree-lowering; classical Leibniz; classical chain; same-index output locality
- **Literature:** 3-section / Cartier / p-kernel **REPARAMETERIZATION**; balanced residue and normalization boundary are the PROJECT-SPECIFIC layer
- **Next question:** not started; do not auto-open a new milestone. Open question: minimized residual-state growth of `x^d` as a function of `k`
- **Decision:** PARK (KNOWN section algebra with a PROJECT-SPECIFIC normalization boundary)

## Milestone 16

- **Date:** 2026-08-23
- **Objective:** Exact finite-horizon Myhill–Nerode residual automata and normalizer composition
- **Hypotheses:** sample minimization is `M_k`; prefix locality implies a small automaton; `x^2` collapses like `x^3`
- **Major results:** `≡_k` recursive characterization; `R_k(x^2)=(3^k-1)/2`; `M_k(x^2)=R_k` through `k=7` (conjecture); cascade `outputAlong` law and `M(f∘g)≤M(f)M(g)`; sample `7 ≠ 13` on `x^2` at `k=3`; bounded-`B` obstruction for `deg≥2`
- **Refuted ideas:** sample = Myhill–Nerode; locality ⇒ small automaton; bounded-`B` FST for unbounded residual coefficients
- **Literature:** residual 3-section transducers are standard automata on p-sections; the exact `M_k(x^d)` table and the sample-min counterexample are the project-specific measurements
- **Next question:** closed. Proved in Milestone 17: `M_k(x^2)=(3^k-1)/2`.
- **Decision:** PROMOTE (taken up by Milestone 17)

## Milestone 17

- **Date:** 2026-08-23
- **Objective:** Prove or refute `M_k(x^2)=(3^k-1)/2` for all `k`, with an explicit residual formula and the first higher-degree merge examples
- **Hypotheses:** every residual of `x^2` encodes its prefix injectively; distinct prefixes remain `≡_k`-separated; `x^3`/`x^4` merges are delayed distinctions rather than infinite equivalence
- **Major results:** closed form `f_w=3^{|w|}x^2+2p(w)x+DZ^{|w|}(p(w)^2)`; degree-`≤2` MN class is `(A,B,C) mod 3^k`; `M_k(x^2)=R_k(x^2)=(3^k-1)/2`; canonical probes `0^k`, `10^{k-1}`, `(-1)0^{k-1}`; first `x^3` merge at `k=2` and first `x^4` merge at `k=3`, both split at the next horizon
- **Refuted ideas:** last-layer `ρ`-triples as a complete invariant of `x^2`; `M_k(x^d)=R_k(x^d)` for `d≥3`; finite-horizon merge as infinite-state equality
- **Literature:** 3-section / Cartier residual automata remain the ambient language. The quadratic MN count and the explicit delayed-distinction pairs are project-specific.
- **Next question:** closed. Milestone 18: finite-horizon polynomial equivalence is function congruence modulo `3^k`, classified by Newton residues.
- **Decision:** PROMOTE (taken up by Milestone 18)

## Milestone 18

- **Date:** 2026-08-23
- **Objective:** Characterize polynomial function equivalence modulo `3^k`, the kernel of higher-degree residual merges
- **Hypotheses:** coefficientwise `3^k`-divisibility might still be necessary; `min v_3(c_j)` might be `τ-1`
- **Major results:** `f ≡_k g` iff `f` and `g` agree on `Z` modulo `3^k` (Lean); `I_k` is Newton-coefficientwise `3^k Z`, not `3^k Z[x]`; degree `≤2` recovers monomial residues; exact cubic criterion; first invisible polynomial `x^3-x`; `τ=1+min v_3(Δ^j h(0))`; Lean formalization of the `x^3` and `x^4` first merges
- **Refuted ideas:** coefficientwise divisibility as a necessary vanishing condition for `deg≥3`; `τ=1+min v_3(c_j)`
- **Literature:** Kempner 1921 / integer-valued polynomials are **REPARAMETERIZATION**. Project-specific layer: MN bridge, residual families, delayed-distinction formula
- **Next question:** closed. Milestone 19: image of the residual tree of `x^3` under `Φ_k` is the arithmetic map `F_k`; `M_k(x^3)=|Im F_k|`.
- **Decision:** PROMOTE (taken up by Milestone 19)

## Milestone 19

- **Date:** 2026-08-23
- **Objective:** Determine which Newton classes are reached by residuals of `x^3`, and from that `M_k(x^3)`
- **Hypotheses:** packed-prefix congruence might label the classes; `M_{k+1}=3M_k+1` might lift
- **Major results:** closed form `f_w=3^{2m}x^3+3^{m+1}p x^2+3p^2 x+DZ^m(p^3)`; Newton coordinates and section transition; `M_k(x^3)=|Im F_k|` for the explicit map `F_k(m,p)=Φ_k(f_{(m,p)})`; same-depth collision criterion; first merge is the depth-1 sign pair of `Φ_2`; shallow lower bound `(3^{r+1}-1)/2`; Lean file `CubicResidual.lean`
- **Refuted ideas:** Newton classes are congruence classes of `p(w)`; `M_{k+1}=3M_k+1`
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION. Project-specific layer: residual image of `x^3` under `Φ_k`
- **Next question:** closed. Milestone 20: fibres of `F_k` classified by the Newton hierarchy; no closed `M_k`.
- **Decision:** PROMOTE (taken up by Milestone 20)

## Milestone 20

- **Date:** 2026-08-23
- **Objective:** Classify the fibres of `F_k` and derive an exact formula or recurrence for `M_k(x^3)`
- **Hypotheses:** `N2` might imply `N1`; `N2+N1` might imply `N0`; all collisions might be sign pairs
- **Major results:** exact same-depth criterion `(N2,N1,N0)`; `N2` does not imply `N1`; `N2+N1` do not imply `N0`; `C_{k,m}=3^m` on `2m+1≤k` (Lean `N2` injection); cross-depth only when both `2m+1≥k`; sign-pair fibre theorem; deepest `0`-fibre is `3^{ceil((2k-1)/3)} | q`; zero spine for `m≥ceil(k/2)`; `M_k=sum C - spine overcount`; arithmetic image through `k=12` (`M_12=265352`)
- **Refuted ideas:** `N2 ⇒ N1`; `N2+N1 ⇒ N0`; every collision is `p ↔ -p`; `M_{k+1}=3M_k+1`
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 21: deepest-layer fibres classified; stratified `C_{k,k-1}`; no single-term formula.
- **Decision:** PROMOTE (taken up by Milestone 21)

## Milestone 21

- **Date:** 2026-08-23
- **Objective:** Exact fibre structure and count of the deepest `x^3` residual layer
- **Hypotheses:** `N2+N1` might collapse fibres to `p=±q`; every deepest fibre might be a full 3-adic coset; `C_{k,k-1}` might be a single-term formula
- **Major results:** deepest Newton simplification `N1≡3p^2`, `N2=N3=0`; fibre criterion `p^2≡q^2 (mod 3^{k-1})` and `D^{k-1}(p^3)` agreement; units collide only as sign pairs; zero fibre `3^{ceil((2k-1)/3)}|p` with Lean necessity and sufficiency; high-stratum cube-count `J(k,s)`; stratified `C_{k,k-1}=1+Σ I_{k,s}`; `C` through `k=14` (`C_{14,13}=1593644`); CLI `cubic-deepest`
- **Refuted ideas:** every deepest fibre is a full residue class (`{720,738}` at `k=8`); `p^3≡q^3 (mod 3^{2k-1})` is equivalent to the `N0` condition
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 22: first intermediate layer `m=k-2`; fibre criterion; horizon surplus; no single-term `C_{k,k-2}`.
- **Decision:** PROMOTE (taken up by Milestone 22)

## Milestone 22

- **Date:** 2026-08-23
- **Objective:** Exact fibre structure of the first intermediate `x^3` residual layer `m=k-2`, and whether it begins a depth-recursive theory
- **Hypotheses:** deepest-layer fibres might persist unchanged; `C_{k,k-2}` might equal `C_{k-1,k-2}` or `3 C_{k-1,k-3}`; `N2` alone might create the one-layer surplus; a scaling `p=3^s u` might renormalize onto a deepest-layer problem
- **Major results:** Newton simplification `N3=0`, `N2≡2·3^{k-1}p`, `N1≡3p^2+3^{k-1}p`; fibre criterion `p≡q (mod 3)` and `3^{k-1}|(p-q)(p+q+3^{k-2})` and `N0` agreement; `N2` has 3 classes; `N2+N1` do not imply `N0`; unit signs always split under horizon lift; surplus `Δ_k=C_{k,k-2}-C_{k-1,k-2}` accounted by that refinement; `C` through `k=14` (`C_{14,12}=531230`); CLI `cubic-layer`; Lean `CubicIntermediateLayer.lean`
- **Refuted ideas:** `C_{k,k-2}=C_{k-1,k-2}`; `C_{k,k-2}=3 C_{k-1,k-3}`; `N2+N1 ⇒ N0`; `N2` alone explains `Δ_k`; literal renormalization onto `F_{k'}(k'-1,u)`
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 23: general `N2` visibility `p mod 3^r`; `r=2` fibre criterion; `N1` is not the next trit.
- **Decision:** PROMOTE (taken up by Milestone 23)

## Milestone 23

- **Date:** 2026-08-23
- **Objective:** Determine what Newton coordinates expose at depth deficit `r=2` (`m=k-3`), and whether `r ↦ p mod 3^r` is a theorem
- **Hypotheses:** `N2` sees `p mod 9`; the pattern may be a general visibility law; `N1` might reveal the next trit; `r=2` might be qualitatively new
- **Major results:** `N2 ≡ 2·3^{k-2}p` (`k≥5`); visibility `N2` iff `p≡q (mod 9)` (`k≥3`); general law `N2` iff `p≡q (mod 3^r)` at `m=k-1-r` (`r+1≤k`); fibre criterion `C_{k,2}`; `N1` after `N2` is `3^{k-3}|δ(p+q+3^{k-3})`, forcing unit-residue singletons; signs require `9|p`; `N2` has 9 classes for `k≥5`; uncompressed through `k=8`; first collision at `k=9`; `C` through `k=14` (`C_{14,11}=177083`); CLI `--depth-deficit 2`; Lean `CubicDeficitTwo.lean`
- **Refuted ideas:** `N2+N1 ⇒ N0`; `N1` reveals the next trit uniformly; `r=2` is only a digit increment of the whole Newton tower
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 24: after `N2`, `N1` separates every `v3(p)<r`; nontrivial fibres lie in `3^r Z`.
- **Decision:** PROMOTE (taken up by Milestone 24)

## Milestone 24

- **Date:** 2026-08-23
- **Objective:** Prove the general `N1` refinement after the depth-deficit `N2` filter, and characterize the surviving `3^r Z` locus
- **Hypotheses:** after `N2` equality, `v3(p)<r` forces `N1` to separate `p` from every other prefix; nontrivial `N2+N1` fibres lie in `3^r Z`; the high-valuation locus may rescale
- **Major results:** exact post-`N2` law `3^{k-1-r}|δ(p+q+3^m)`; unit injectivity for every `r≥1`; valuation-stratification theorem on `P_m`; sign pairs iff `3^r|p`; partial recursion `N1(3^r u)` reduces to deepest `N1` at horizon `k-2r` when `k≥2r+2`; CLI `n1-strata` / `n1-fibre`; Lean `CubicN1Valuation.lean`
- **Refuted ideas:** unit injectivity at `r=0`; that `3^r|p` is sufficient for a merge; that the remaining locus is a full recursive copy of the original deficit-`r` problem
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 25: two-regime `N0` scaling; not a standard smaller residual.
- **Decision:** PROMOTE (taken up by Milestone 25)

## Milestone 25

- **Date:** 2026-08-23
- **Objective:** Determine the exact recursive structure of `D^m((3^r u)^3)` after the `N2+N1` locus `3^r|p`
- **Hypotheses:** `D` strips `3^{3r}`; the remainder might be a smaller cubic residual, perhaps at the Milestone-24 `N1` horizon `k-2r`
- **Major results:** two-regime identity `3^{3r-m} u^3` vs `D^{m-3r}(u^3)`; equivalent to `k≤4r+1` vs `k≥4r+1`; sign pairs survive `N0` iff `3^k|N0`; valuation threshold `3 v3(p)=m`; visibility bound `s=max(1,t+k-1)`; CLI `n0-reduction` / `n0-fibre`; Lean `CubicN0Reduction.lean`
- **Refuted ideas:** stripped `N0` is a standard residual instance; `N0` and scaled `N1` share the deepest problem at horizon `k-2r`; width `k-1-2r` equals remaining depth `k-1-4r` for `r≥1`
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 26: mismatched-width cubic quotient `Q_{t,K,W}`; exact reconstruction criterion; extra `2r` trits visible through cubic carry.
- **Decision:** PROMOTE (taken up by Milestone 26)

## Milestone 26

- **Date:** 2026-08-23
- **Objective:** Exact arithmetic of the mismatched-width cubic quotient `Q_{t,K,W}(u)=D^t(u^3) mod 3^K` on `u ∈ P_W`, the independent `N0` core after Milestones 23–25
- **Hypotheses:** equality might reduce to `u^3 ≡ v^3 (mod 3^{t+K})`; input precision might be `t+K-1` as a fibre law; the extra `2r` trits might be invisible to `D^t`; `Q` might still be a smaller residual machine
- **Major results:** reconstruction criterion `Q(u)=Q(v)` iff `3^{t+K}` divides `u^3-v^3-Δbal_t`; cube-mod sufficient not necessary unless discarded digits agree; two-regime entry `k ≶ 4r+1`; unit opposite-residue branch has no extra `3` in `v3(u^3-v^3)`; high-trit identity `D^t((a+3^t b)^3)=D^t(a^3)+3a^2b+…`; on cubic parameters `t+K-1=2W`; CLI `cubic-quotient` / `cubic-quotient-fibre` / `compare-cubic-quotient`; Lean `MismatchedCubicQuotient.lean`
- **Refuted ideas:** `Q` is an ordinary residual; extra width is invisible; `Q`-equality is a pure residue relation `u ≡ v (mod 3^s)`
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Next question:** closed. Milestone 27: no compact residue/valuation/`B_t` invariant; family `1+3^t b` forces `W-t` extra trits.
- **Decision:** PROMOTE (taken up by Milestone 27)

## Milestone 27

- **Date:** 2026-08-23
- **Objective:** Decide whether `Q_{t,K,W}` admits a compact exact invariant
- **Hypotheses:** a residue/valuation/sign/`B_t` or two-scale `(a,b)` summary might classify fibres; `B_t` itself might be the growing obstruction
- **Major results:** two-scale expansion is the working equation; `B_t` is determined by `u mod 3^{max(1,t-1)}`; on `1+3^t b`, `Q`-equality is `b ≡ c (mod 3^{K-1})`; any `Ψ` constant on that family needs `≥ W-t` extra trits; high valuation still collapses to `0`; CLI `cubic-quotient-invariant` / `cubic-quotient-compare`; Lean `MismatchedCubicInvariant.lean`; Residual Explorer Q card
- **Refuted ideas:** bounded `Ψ1`–`Ψ4` classify `Q`; `B_t` is an incompressible independent jet; `Ψ5` with `β < K-1` is sufficient on units
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Decision:** CLOSE. Stop the Q-classification line; do not invent further fibre types. Next mathematical direction is not a new Q-taxonomy.

## Consolidation (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Make the laboratory match its actual frontier: general `bt.calculus`, cubic fibres in `research.residuals`, one Newton-stratum theorem, generated ledger, CI
- **Major results:** package split; `NewtonStratum.lean`; `acceleratedT` well-defined; quadratic `M_k(x^2)` ledger rows retagged to Lean; docs reading path no longer Collatz-first
- **Deferred:** `BTA-product` (`M_k` cardinality is not a Lean object); Lake package rename; `formal/Automata/` placeholder. `BTJ-degree` was later compiled (see Lean recovery note).
- **Next question:** closed by Milestone 27. Do not auto-open a further Q-taxonomy milestone.
- **Decision:** CLOSE

## Milestone 28

- **Date:** 2026-08-23
- **Objective:** Exact Myhill–Nerode count \(M_k(x^3)\) by image cardinality, not by a further \(Q\)-taxonomy
- **Hypotheses:** same-depth \(C_{k,m}\) splits into an injective \(v_3(p)<r\) region plus a \(P_W\) core image; unexhausted cores collapse only on the zero fibre; cross-depth overlap is the zero spine plus a short list of nonzero families; a polynomial-time closed formula may exist
- **Major results:** master identity \(M_k=|\cup_m\mathrm{Im}\,F_k|\); easy count \(3^m-3^{m-r}\); core domain \(u\in P_W\); \(C=E+|\mathrm{core}|\); unexhausted formula \(C=3^m-Z+1\); unit \(G_a\) law \(b\equiv c\pmod{3^{K-1}}\); \(N_3\)-gated algorithm for \(M_k\); zero spine is not the only overlap; exact table through \(k=14\) (\(M_{14}=2390443\)); CLI `x3-states` / `x3-layer-count`; Lean `XCubeStateComplexity.lean`
- **Refuted ideas:** that \(\sum C\) minus the zero-spine overcount equals \(M_k\); that \(N_0\) determines \(N_1\) on the exhausted core; that the exact count is polynomial in \(k\) by this arithmetic (deepest layer is still \(P_{k-1}\))
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Decision:** PROMOTE (taken up by Milestone 29). Remaining obstruction: exhausted joint image \(|(N_1,Q)(P_W)|\) and the exact nonzero cross-depth families.

## Milestone 29

- **Date:** 2026-08-23
- **Objective:** Finish the exact state count \(M_k(x^3)\), or prove a rigorous obstruction and close the dedicated counting line
- **Hypotheses:** the reduced core \(H=(u^2\bmod 3^W,Q)\) might admit an exact unit/valuation image formula; every nonzero cross-depth overlap might lie in a short closed family list; a finite arithmetic sum for \(M_k\) might avoid enumerating \(P_{k-1}\)
- **Major results:** \(N_1\) on the core is the square coordinate \(A_{k,r}(u)=u^2\bmod 3^W\); units with the same square are \(\pm\); \(N_0(u)=N_0(-u)\) iff \(N_0(u)=0\); unit joint image is \(2\cdot 3^{W-1}\) minus the unit \(Q\)-zeros; non-units contribute zero-\(A\) merges and twins; cross-depth families are the zero spine, shared signs, valuation translates, one-to-cosets, high-valuation cubes, and twin translates; exact table through \(k=14\) reproduced; CLI `x3-overlaps` / `x3-image-count`
- **Refuted ideas:** that \(|\mathrm{Im}\,Q|\) determines \(|\mathrm{Im}\,H|\); that units plus the zero spine exhaust all collisions; that every nonzero overlap is a shared sign pair; that the reduced arithmetic is polynomial in \(k\)
- **Literature:** Mahler / Newton basis remains REPARAMETERIZATION
- **Decision:** CLOSE the dedicated \(x^3\) counting line. The obstruction is the vanishing locus of \(Q\) on \(P_W\) (sign surplus, twins, large unit cubes) together with classified but non-closed-form nonzero deep overlaps. Structural Newton-stratum theory is paper-worthy; the \(M_k\) table is a computational appendix. Do not open Milestone 30.

## Lean recovery (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Wrap the deferred section-derivative degree law from existing `powShift` reconstruction
- **Major results:** `sectionDeriv_natDegree` and `sectionDeriv_leadingCoeff` in `BTCalculus/Polynomial.lean`; ledger `BTJ-degree` retagged **EXACT — LEAN VERIFIED**
- **Deferred:** `BTA-Ik-newton` (Newton coefficients of \(I_k\)); `BT-encode-unique`; `M_k` as a Lean cardinality
- **Decision:** CLOSE. Not a new residual programme. Do not open Milestone 30.

## Lifting-tree triage (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Decide whether the residual-state machinery says anything about 3-adic lifting of `f(x) ≡ 0 (mod 3^k)` beyond classical Hensel and Newton-polygon theory
- **Hypotheses:** the lifting tree might be an exact sub-object of the residual Mealy machine; the residual state might carry more than the Taylor jet; the depth-`r` subtree might be determined by `v_3(f)` and `v_3(f')`; state compression might give a complexity statement
- **Major results:** iterated reconstruction `f(n_w + 3^k x) = Σ ρ_i 3^i + 3^k 𝔇_w f(x)`; balanced digits force `3^k | f(n_w)` iff every output trit vanishes, so the lifting tree **is** the zero-output subtree; residual state equals the scaled Taylor jet with linear coefficient exactly `f'(n_w)`; classical `0/1/3` trichotomy as a corollary for `k ≥ 1`; `Φ_r` determines the depth-`r` subtree and the horizon is sharp; deep linearization `𝔇_w f ≡_r f(n_w)/3^k + f'(n_w)x` for `k ≥ r` with the two residues as minimal state; `bt.calculus.lifting`; `research.lifting`; `PadicLifting.lean`; CLI `congruence`; explorer lifting view
- **Refuted ideas:** that `v_3(f(n))` and `v_3(f'(n))` determine lifting behaviour — smallest witness is the level-1 node `0` of `x^2 ± 9`, identical valuations, six surviving grandchildren versus none; that the trichotomy holds at the root — `x^2 + x` has two children with a unit derivative; that state compression is a complexity result
- **Literature:** lifting trees, singular separation, root counting, and Igusa rationality are all KNOWN (`zuniga-galindo-2003`, `cheng-gao-rojas-wan-2019`, `dwivedi-mittal-saxena-2019`, `dwivedi-saxena-2020`); the core translation is a REPARAMETERIZATION and is tagged as one
- **Open:** whether deep-regime valuation determinacy of the unordered shape is a theorem
- **Superseded** by *Unordered deep shape is valuation-determined* below. It is a theorem, and the theorem is the Newton-polygon ramification of `c + b x`.
- **Decision:** PARK, with the multivariate sub-branch CLOSEd; status `EXPLORATORY`, not a paper candidate. Multivariate systems stay closed: `dwivedi-saxena-2024-systems-non-fields` already covers `n + k` constant. Do not open a numbered milestone for this line.

## Minimal lifting state (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Is `Φ_r` minimal, or can finite-horizon lifting behaviour be compressed further?
- **Hypotheses:** the incoming plan assumed minimality was open and that the deep-regime two-residue state `(c, b) mod 3^r` was minimal; both were tested before implementing and both are false, which redirected the branch from searching for minimality to counting the true minimal state
- **Major results:** unit-scaling invariance — on a surviving branch `𝔇_a(λg) = λ 𝔇_a g` and survival is `λ`-invariant, so the whole ordered depth-`r` subtree is invariant while `Φ_r` is not, Lean-verified word-by-word in `PadicLiftingState.lean`; the linear transition law `𝔇_a(c+bx) = D(c+ab) + bx`, hence `b` invariant and `e = v_3(b)` conserved; the nonsingular row is exactly `3^r` behaviours indexed by `u = c/b`, the surviving path being the balanced digits of `-u`, which is Newton iteration in balanced digits and is tagged REPARAMETERIZATION; the row structure theorem splitting each singular row by `m = v_3(c)` into truncated trees for `m < e` and a fully ternary `e`-block for `m ≥ e`; the closed form `L_r = (3^{r+1}-1)/2 + r = 5, 15, 43, 125, 369, 1099` refining to `3^{r-e} + e`, verified exhaustively to `r = 6`, with the `C(r,2)` row overlap proved to be exactly the shared truncated trees; attainment by `f_{c,b}(x) = 3^r c + b x` and its quadratic variant, so the count is exact and not an upper bound; `bt.calculus.lifting_state`; `research.lifting.state_complexity`; `PadicLiftingState.lean`; CLI `congruence state | distinguish`; explorer minimal-state panel
- **Refuted ideas:** that `Φ_r` is minimal — smallest live witness `x` against `-x`, identical futures at every depth, `Φ_r` differing; that the deep two-residue state is minimal, so the earlier "minimal state in the deep regime" phrasing of the triage entry above was wrong and is now annotated sufficiency-only in the ledger; that unit scaling is the whole collapse — orbits number `2·3^r - 1`, strictly above `L_r` from `r = 2`; that a lower bound `L_r ≥ 3^r` was the target, when the exact value was already available
- **Literature:** Hensel lifting, the singular split, and root counting remain KNOWN; the nonsingular half of the classification is a REPARAMETERIZATION of Newton's method; the minimal-state statement itself has no located prior form, but it is a two-line consequence of the definitions and is best described as a correction to our own earlier sufficiency claim
- **Open:** the one gap in the closed form — injectivity of `d mod 3^{r-e} ↦ (B_{r-e}(d+s))_{|s| ≤ e}` for `1 < e < r`, which is all that stands between `COMPUTATIONALLY VERIFIED` and a proof of `L_r`
- **Decision:** PARK. The extreme rows, the structure theorem, the overlap, the attainment, and the reduction of the total to the rows are proved; the general row rests on exhaustion to `r = 6`, which is exactly the plan's own PARK criterion. The nonsingular half being Newton's method also keeps `CLOSE — REPARAMETERIZATION` live: the burden of showing the quotient is more than bookkeeping about Hensel lifting has not been discharged. Do not open a numbered milestone.
- **Superseded** by *Shifted-family separation closes the lifting count* below. The shift window `|s| ≤ e` above is wrong — it comes from taking the digit sum of the word instead of its balanced value — so the "gap" was our own arithmetic error, and the corrected statement is provable. The PARK is superseded by CLOSE — REPARAMETERIZATION.

## Operator-fragment unique NF (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Does every open term of `{D, I_a, S, N}` under the tree rules have a unique syntactic normal form?
- **Hypotheses:** unique NF for open terms, not just closed integer seeds; perhaps the NF is also a unique representative of the integer function
- **Major results:** all-strategy termination on the lex rank `(I0-count, N-inversion, size)`; complete critical-pair list joins; Newman gives unique syntactic NF and an explicit grammar (`N` pushed past `I±`/`S`, then an `I`/`S` spine over a `D`-safe core); size-`≤ 6` census (9331 terms) agrees with innermost `rewrite_expr`
- **Refuted ideas:** that a tree-rule irreducible is a unique representative of the integer operator — `N(D(x))` and `D(N(x))` are distinct irreducibles and agree under `evaluate` (`rewrite_N_D` is not a tree rule)
- **Literature:** Knuth–Bendix / Newman is the method. The fragment and the missing `N`–`D` commute are project-specific.
- **Next question:** does adding `N(D(x)) → D(N(x))` as a tree rule stay confluent and become a complete canonical form? Taken up immediately below.
- **Decision:** PROMOTE the unique-syntactic-NF theorem to the ledger as **EXACT — HUMAN PROOF**. Do not open a numbered milestone. Lean Newman for this fragment is deferred (no `sorry`); do not touch `BTCalculus/Confluence.lean`.

## Operator-fragment N(D) commute (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Does adding the tree rule `N(D(x)) → D(N(x))` keep termination and local confluence, and are the irreducibles unique semantic representatives?
- **Hypotheses:** the missing commute completes a canonical form for the integer operator algebra on `{D, I_a, S, N}`
- **Major results:** `D` joins the pushable class of the lex rank `(I0-count, N-inversion, size)`, so every rewrite order still terminates; five new critical pairs (`N(N(D))`, `N(D(I±))`, `N(D(I0))`, `N(D(S))`) all join; Newman gives unique syntactic NF and the grammar `I±`/`S` spine over `D^d(x)` or `D^d(N(x))`; distinct irreducibles are distinct functions by unique balanced-ternary words of fixed length plus `D(-n)=-D(n)`; size-`≤ 6` census (9331 terms) agrees
- **Refuted ideas:** none new. The old semantic-incompleteness claim stays REFUTED for the system *without* the commute (`N(D)` / `D(N)` were the witnesses and now share the NF `D(N(x))`)
- **Literature:** Knuth–Bendix / Newman; unique BT expansion. The oriented `N`–`D` tree rule is project-specific.
- **Next question:** does the same one-way `N`–`D` orientation remain locally confluent on any larger signature (`Add`, `Mul`, or `W`), or is this fragment the maximal complete unary algebra?
- **Decision:** PROMOTE termination, confluence, and semantic canonicity of the enlarged TRS to the ledger as **EXACT — HUMAN PROOF**. Do not open a numbered milestone. Lean Newman remains deferred (no `sorry`); do not touch `BTCalculus/Confluence.lean`. Taken up immediately below.

## Rewrite signature enlargement (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Does adding exact-on-ℤ `Add` / `Mul` / `W` rules to the unary tree core stay locally confluent and semantically complete, or is `{D, I_a, S, N}` maximal?
- **Hypotheses:** either the first counterexample appears as soon as `Add` or `Mul` or `W` is added, or a small oriented extension remains a complete core
- **Major results:** `D` through `Add`/`Mul` and `I_a` through `Mul` are unsound (trit carry); push-in `S(x+y)→S(x)+S(y)` overlaps `D∘S=id` in the non-joining peak `D(S(x+y)) → x+y | D(S(x)+S(y))`; the same shape is `D(S(x*y))` for `Mul`; `N`-through-`Add` alone joins its `N`-overlaps but leaves the twins `S(x+y)` / `S(x)+S(y)`; factor-out `S(x)+S(y)→S(x+y)` repairs the Add peak and stops (KNOWN AC twins, not a CAS); one-way `W` plus stock `K3` rules fails at `N∘W∘W → K3∘N | N∘K3`, repaired on a bounded CP list by exact `N∘K3→K3∘N` (not a word-table confluence claim)
- **Refuted ideas:** that unary + push-in `S` through `Add` is locally confluent; the same for `Mul`; that `N`-through-`Add` alone is semantically canonical; that one-way `N`–`D` plus stock `W`/`K3` rules is locally confluent
- **Literature:** Knuth–Bendix / Newman; AC incompleteness of sums is KNOWN. The `D∘S` / `S`-distrib overlap and the `N∘K3` gap are project-specific.
- **Next question:** does any finite exact-on-ℤ *factor-out* Add extension escape the `D∘S` obstruction and become complete even modulo AC, or is that already a computer-algebra engine? Taken up immediately below.
- **Decision:** PROMOTE the obstruction and the four refutations to the ledger. Do not open a numbered milestone. Do not install Add/Mul rules in `rewrite._step`. Do not edit `BTCalculus/Confluence.lean`.

## Factor-out Add is already a CAS (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Does any finite exact-on-ℤ factor-out Add extension of the unary tree core become a complete canonical form even modulo AC, or is that already a computer-algebra engine?
- **Hypotheses:** either a small factor-out orientation is complete modulo AC, or a named obstruction shows any such system is already AC-rewriting / unbounded
- **Major results:** the finite exact pair table is `S+S`, `N+N`, `I_a+S`, `S+I_a`, `I++I- → S` (size-decreasing; `I0` counts as `S`); same-sign `I_a+I_a` is not a rule (`3(x+y)±2` is not `I_b(x+y)`); binary matching repairs `D(S(x)+S(y))` and joins named unary overlaps, but `S(x)+(S(y)+z)` and `S(x+y)+z` are semantic twins that are not AC-equivalent; AC-matching of the same table collects non-adjacent `S` and joins opposite-sign `I++S+I-`, then fails local confluence modulo AC at `I+(x)+S(y)+I+(z) → I+(x+y)+I+(z) | I+(x)+I+(y+z)`; both failures are the balanced-trit carry of `1+1` (the same carry that made `D`-through-Add unsound). Completing either system needs constants, carry, or a polynomial NF
- **Refuted ideas:** that unary + finite binary factor-out Add is semantically complete even after identifying AC twins; that granting AC-matching of that finite table yields a complete form modulo AC
- **Literature:** AC-matching / Knuth–Bendix modulo AC is KNOWN. The same-sign `I_a` residue `±2` and the identification with the push-in `D∘S` carry are project-specific
- **Next question:** should integer sums of BT operator terms be canonicalized only as affine maps `n ↦ 3^k n + c` (evaluation / coefficient words), never by a tree TRS on `Add`? Taken up immediately below.
- **Decision:** CLOSE. Finite exact factor-out Add is AC-engine territory, not a tiny tree core. Ledger the obstruction and the two refutations. Do not install the extras in `rewrite._step`. Do not open a numbered milestone. Do not edit `BTCalculus/Confluence.lean`.

## Add is affine / coefficient-word only (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Should integer sums of BT operator terms be canonicalized only as affine maps (evaluation / coefficient words), never by a tree TRS on `Add`?
- **Hypotheses:** either a sharp architectural theorem (the only complete finite forms are affine / coefficient-word), or a small finite non-CAS Add-tree system that is complete after all
- **Major results:** the identities `U(x)+V(y)=W(x+y)` for `U,V,W ∈ {S,I_a,N}` are exactly the six known push-in / factor-out rows (`I0 = S`); same-sign `I_a` needs a non-trit constant and mixed `N` has the wrong slope; `D+D` is the same `1+1` carry. Those identities *are* the orientations already incomplete (`BTC-unary-s-distrib-obstruction`, `BTC-add-n-push-semantic`, `BTC-add-factor-cas-obstruction`). Named twins join as affine forms and as `evaluate` then coefficient-word NF (`bt.normtheory`). Production `TREE_RULES` unchanged
- **Refuted ideas:** that a third exact-on-ℤ tree orientation on `Add` escapes the existing carry / AC obstructions
- **Literature:** unique BT expansion and AC incompleteness of sums are KNOWN. The classification that those six rows exhaust the exact constructor identities, and the lab decision to canonicalize sums only as affine / coefficient-word objects, are project-specific
- **Next question:** the Add-tree program is finished. Independent of rewrite: is the full `WORD_REWRITE_RULES` table confluent on any named fragment that still excludes `Add`, or is that permanently a non-claim?
- **Decision:** PROMOTE the architectural theorem `BTC-add-affine-only` as **EXACT — HUMAN PROOF**. Do not open a numbered milestone. Do not install Add rules in `rewrite._step`. Do not edit `BTCalculus/Confluence.lean`.

## Shifted-family separation closes the lifting count (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Prove or refute the one recorded gap in `L_r`: injectivity of `d mod 3^{r-e} ↦ (B_{r-e}(d+s))_s`, the shifted family of a singular valuation row.
- **Hypotheses:** the incoming question assumed the shift window was `|s| ≤ e`, from the digit sum of the word, and asked whether so few shifts could activate enough singular branches to separate the residue `d`
- **Major results:** the shift is the **balanced value** `packWord(w)`, not the digit sum — the constant after `j` steps is `3^{e-j}(d + a_1 + 3a_2 + … + 3^{j-1}a_j)`, generalised to `𝔇_w(3^j d + 3^{j+i}x) = (d + 3^i·packWord(w)) + 3^{j+i}x` and Lean-verified as `residualAlong_linState_pow` with the fully ternary block `outputAlong_linState_pow`; consequently the window is `W_e = [-(3^e-1)/2, (3^e-1)/2]`, all `3^e` values, a complete residue system modulo `3^e`, so each block has exactly one leaf that continues; separation then holds for every `e ≥ 1` and `R ≥ 0` by induction on `R`, identifying that leaf as the unique window entry of depth `≥ min(e,R)` and descending to horizon `R - e`; hence the rows are exactly `3^{r-e} + e` and `L_r = (3^{r+1}-1)/2 + r` is proved rather than exhausted, retagged `EXACT — HUMAN PROOF`; and the count is a corollary of a **normal form** — scale `b` to `3^e`, then the behaviour is `T_{v_3(c)}` and depends on `v_3(c)` alone where `v_3(c) < e` (`r` classes), and is exactly the unit-scaling orbit with no further collapse where `v_3(c) ≥ e` (`(3^{r+1}-1)/2` classes), a bijection with behaviour classes verified for `r ≤ 4`
- **Refuted ideas:** that the shift is the digit sum of the word — our own earlier error, and the reason the row count looked unreachable; with that window the separation is genuinely **false**, since at `e = 2` every `d ≡ 3` and `d ≡ 6 (mod 9)` gives the identical tuple `(∅,∅,T_1,∅,∅)`, so the recorded "gap" was an artefact of the error rather than a real obstruction. Also refuted: that unit-orbit non-minimality is a phenomenon of the whole state space — it is entirely an artefact of the dominated stratum, and on `v_3(c) ≥ v_3(b)` the orbit *is* the minimal state.
- **Literature:** the normal form is the identification the branch was missing, and it identifies against us. "Unit orbit, degenerated to `v_3(c)` where the constant dominates" is Newton-polygon dominance plus Hensel rigidity in residual coordinates; the `3^{r-e} + e` rows and the `C(r,2)` overlap are arithmetic bookkeeping over that description. The exact count is new as a number; the object it counts is not new as an object.
- **Open:** nothing in this sub-branch. The parent dossier kept deep-regime valuation determinacy of the *unordered* shape (now closed below) and the shallow regime `k < r`.
- **Decision:** CLOSE — REPARAMETERIZATION for the minimal-state sub-branch. All four plan targets are proved and the count is attained, so the PARK criterion is gone; but promotion required the quotient not to be a standard classical object, and the normal form shows it is one. Retained as machinery: the block shift law (Lean), the separation theorem, `minimal_state_key`, and the correction of our own sufficiency-as-minimality claim. Do not open a numbered milestone.

## Unordered deep shape is valuation-determined (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** In the deep regime, is the unlabeled depth-`r` lifting shape `U_r` determined by the valuation data of the linear residual?
- **Hypotheses:** forgetting branch trits might collapse `U_r` onto the Newton-polygon pair `(v_3(c), v_3(b))`, which ordered behaviour refuses
- **Major results:** yes, as a theorem. Write `m = min(v_3(c), r)` and `e = min(v_3(b), r)`. Then `U_r = T_m` if `m < e` and `U_r = S(e, r)` if `m ≥ e`, where `T_j` is the fully ternary tree of depth `j` and `S` is the undominated recursion (a path if `e = 0`, `T_r` if `e ≥ r`, otherwise two copies of `T_{e-1}` plus one `S(e, r-1)`). The special child's exact valuation is not determined by `(m, e)` — `(9, 9)` continues to a zero constant, `(45, 9)` to a unit — but that difference is invisible to `U_r`. Checked on the complete residue system `(ℤ/3^r)^2` for `r ≤ 4`. `unordered_shape`, `valuation_unordered_shape`, `unordered_shape_census`. Ledger row `BTL-deep-valuation-shape` retagged `EXACT — HUMAN PROOF`.
- **Refuted ideas:** that the special child's unbounded valuation blocks a proof — it is real, and it is unused by `U_r`. That a bound `|c| ≤ 40` was the state space: that census never left the window `|d| ≤ (3^e-1)/2`, so it never saw the `(9, 9)` vs `(45, 9)` pair; the identity holds there anyway.
- **Literature:** this is the Newton-polygon ramification of a linear residual. The generic perturbation dies after `e-1` further steps; exactly one child continues along the slope. Not a new Hensel theorem.
- **Open:** nothing in this sub-question. The parent dossier kept the local-vs-global horizon question (now closed below) and the shallow regime.
- **Decision:** CLOSE — REPARAMETERIZATION for the unordered-shape question. The target is answered by a proof; promotion required the result not to be Hensel restated, and the closed form is exactly that restatement. Do not reopen the ordered or unordered deep-state lines. Do not open a numbered milestone.

## Local Phi_r versus global k0 (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Does the local finite-horizon state `Phi_r` give a sharper or more adaptive stabilization bound for roots modulo `3^k` than the global `k0 = O(d^2(log C+log d))`?
- **Hypotheses:** a residual/Newton state at a node could certify that `N_k(f)` has entered its closed-form regime earlier than the discriminant threshold
- **Major results:** literature gate, verified from Dwivedi–Saxena 2020 (arXiv:2006.08926): `Delta = v_p(D(rad(f)))`, `k0 = d(Delta+1)+1`, and for `k > d(Delta+1)` one has the closed form `N_k(f) = sum_i p^{k-ceil((k-nu_i)/e_i)}`; `N_k` is constant only when `D(f) != 0`. The `O(d^2(log C+log d))` figure is the Sylvester envelope of `Delta`, not a second bound. Local unique lift is Hensel / strong Hensel `v(f)>2v(f')`. Per-root contributions and the tree-of-ideals algorithm are already local. `Phi_r` is the Taylor jet (`REPARAMETERIZATION`). Witness `(x-1)(x^2-9)`: residue 1 is Hensel-unique from level 1 (`f'=-8`), residue 0 is singular, `N_k = 1,2,4,7,7,7,7`. Three different predicates — local uniqueness, global constancy, “every node nonsingular” — disagree. No CLI, UI, or Lean.
- **Refuted ideas:** that `k0` is a per-branch lift-stabilization bound; that `Phi_r` can replace `Delta` as a uniform separation certificate; that “all current nodes are Hensel-nonsingular” coincides with `N_k` constancy
- **Literature:** Hensel; Conrad strong Hensel; Zúñiga-Galindo 2003; Cheng–Gao–Rojas–Wan 2019; Dwivedi–Mittal–Saxena 2019; Dwivedi–Saxena 2020. Every precise reading is `KNOWN` or `REPARAMETERIZATION`.
- **Open:** nothing on this line
- **Decision:** CLOSE. A branch whose statements are all `KNOWN` or `REPARAMETERIZATION` is a close. Do not reopen the lifting-state line. Do not open a numbered milestone.

## 3-adic polynomial dynamics gate (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Decide whether a finite residual state gives a genuinely new minimal description of cycle lifting for polynomial iteration over `Z_3`.
- **Hypotheses:** multiplier and valuation data might miss finite futures; the complete residual return-function class should determine them; its bounded behavioural quotient might have a nonclassical normal form or consequence.
- **Major results:** the Phase-0 object was restricted to the rooted period-labelled cycle-lift tree; the local residual was represented exactly by the table `(f^q(x+3^k t)-(x+3^k t))/3^k mod 3^r`, without expanding `f^q`; on 28 prescribed maps, levels `1..3`, and horizon `r=3`, 180 cycle states gave all four Fan--Liao lift types and periods `1,2,3,6,9`; 148 residual classes collapsed to 19 bounded behaviours; equal residual classes had equal futures throughout the census; the classical return-map argument proves this sufficiency by induction on the horizon.
- **Refuted ideas:** coarse `(q,type,v_3(a-1),v_3(b))` data is complete (`x^2-3` versus `x^2+3` at the fixed cycle `(1)`); affine-plus-quadratic data is complete at horizon 3 (`x^3-x` at `(0)` on levels 1 and 2, separated by the visible cubic term `9t^3` versus the invisible `81t^3` modulo 27); the residual state is minimal (`x^2-1` versus `x^2+2` on the period-2 cycle `(0,2)` modulo 3 has equal depth-2 behaviour and unequal residual tables).
- **Literature:** cycle-lift trees, affine return maps, grow/split/tail/partial-split classification, valuation recurrences, possible periods, local interpolation, rooted-tree transducers, and finite-depth behavioural minimization are `KNOWN`; the residual table is a `REPARAMETERIZATION` of the truncated Taylor return map; the exact census is `PROJECT-SPECIFIC`.
- **Open:** none promoted. Strict bounded compression alone is ordinary behavioural quotienting and yielded no normal form, complexity theorem, or new dynamical consequence.
- **Decision:** CLOSE — REPARAMETERIZATION. Higher Taylor terms explain every failure of coarse classical signatures, while the complete residual contains exactly those classical terms. The `148 → 19` compression is real but is only standard finite-depth tree equivalence. No Phase 1, CLI, visualization, or Lean module is justified.

## Residual quotient gate for Černý-type automata (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Decide whether residual polynomials admit a natural finite transition-closed quotient that could later support synchronization / Černý analysis.
- **Hypotheses:** a non-affine arithmetic family might have a canonical finite congruence stricter than horizon truncation but coarser than raw equality; `≡_r` might already be transition-stable; residual closures of small nonlinear polynomials might be finite.
- **Major results:** `≡_r` is not a transition congruence — `x ≡_1 x+3` but `D_a x = x ≢_1 x+1 = D_a(x+3)` for every trit `a`; the coarsest transition congruence `≈_r` contained in `≡_r` is full Mealy equivalence for `r ≥ 1`, hence raw polynomial equality on `Z[x]`; affine closures are finite by the invariant slope and the intercept bound `|c| ≤ max(|b|, |c_0|)`, with exact counts `1,2,3` on the sampled linear family; every degree-`≥ 2` polynomial has infinitely many sections because `LC(D_w f) = 3^{|w|(deg f - 1)} LC(f)`; remaining-horizon clocks were excluded as manufactured DFAs. No reset words, ranks, or Černý bounds were computed.
- **Refuted ideas:** that finite-horizon `≡_r` is a transition congruence; that a non-affine residual family has a natural finite behaviour-preserving quotient; that balanced-ternary sections produce a new finite-state class beyond Ahmed–Savchuk linear polynomials.
- **Literature:** Ahmed–Savchuk 2020 (polynomial tree endomorphisms; finite-state iff linear); Anashin 2012 and Grigorchuk–Savchuk 2023 (van der Put finite-Mealy criteria). Affine residual automata are a `REPARAMETERIZATION` of that linear case. Černý bounds remain `KNOWN` background and were not opened.
- **Open:** nothing on this line. Synchronization of the affine family is an ordinary finite-DFA computation and does not reopen the gate.
- **Decision:** CLOSE — REPARAMETERIZATION. A branch whose surviving statements are the classical linear/nonlinear finite-state dichotomy is a close. Do not build CLI, visualization, Lean, or `bt.*` synchronization infrastructure. Do not open a numbered milestone.

## Operator-fragment Lean Newman (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Package the human Newman argument for the enlarged operator-fragment tree TRS as a Lean rewrite-relation proof
- **Hypotheses:** termination + local confluence of `{D, I_a, S, N}` including `N(D)→D(N)` formalize without changing the mathematics
- **Major results:** `OpFrag` inductive; `Step` with congruence; lex rank `(I0-count, N-inversion, size)` decreases on every rule; local confluence by the documented critical pairs and left-linear disjoint redexes; Newman ⇒ confluence and unique syntactic NF; NF grammar `I±`/`S` spine over `D^d(x)` or `D^d(N(x))`. Ledger `BTC-op-fragment-nd-nf` retagged **EXACT — LEAN VERIFIED**
- **Refuted ideas:** none. Integer soundness in `Rewrite.lean` is a different claim; coefficient-word `Confluence.lean` was not touched
- **Deferred:** the smaller system without the commute stays a human proof. Semantic canonicity was taken up immediately below and is now **EXACT — LEAN VERIFIED**
- **Decision:** PROMOTE the Lean Newman package. Do not open a numbered milestone. Signature enlargement (`Add`/`Mul`/`W`) is the CLOSE entry above.

## Operator-fragment Lean semantic canonicity (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Lean-prove that distinct irreducibles of the enlarged NF grammar denote distinct maps `ℤ → ℤ`
- **Hypotheses:** the human argument (fixed-length unique BT words + `D(-n)=-D(n)` + probes at `0` and `3^k`) packages on top of `OpFrag` / `OpFragNewman` without a heavy unique-expansion library
- **Major results:** `eval : OpFrag → ℤ → ℤ`; NF reconstruction as `(w, sign, d)`; closed form `sign · 3^{|w|} D^d(n) + c(w)`; pairwise disagreement of distinct triples; tree-rule soundness lifts to `eval`. Ledger `BTC-op-fragment-nd-semantic` retagged **EXACT — LEAN VERIFIED**
- **Refuted ideas:** none new. The system without `N(D)→D(N)` remains semantically incomplete
- **Decision:** PROMOTE the Lean semantic-canonicity package. Do not open a numbered milestone. Do not auto-extend to `Add`/`Mul`/`W`.

## Word-table fragments excluding Add (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Independent of `Add`, is the full `WORD_REWRITE_RULES` table confluent on any named fragment that still excludes `Add`, or is that permanently a non-claim?
- **Hypotheses:** either a clean named word-level fragment (no `Add`) is terminating and locally confluent, or every interesting fragment has a named non-joining peak / non-termination
- **Major results:** the production table itself fails local confluence at `N∘W∘W → N∘K3 | K3∘N` (`N∘K3` is not a production rule; two-way `N∘W` does not join the peak); two-way `N∘D ↔ D∘N` is a KNOWN termination obstruction; the sixteen simplifying rows (`WORD_SIMP_RULES`) terminate on `(I0-count, length)` and every string-rewriting critical pair joins, so Newman gives unique syntactic NF. The `W`/`K3` stock is the interesting kernel. Production rules were not widened
- **Refuted ideas:** that the production `WORD_REWRITE_RULES` table is locally confluent; that two-way `N∘W` repairs the already-refuted one-way `N∘W∘W` peak
- **Literature:** Knuth–Bendix / Newman for string rewriting is KNOWN. The named production peak and the simplifying fragment are project-specific
- **Next question:** does adding the exact missing commute `N∘K3`, and keeping only one-way `N`-commutes, yield a larger confluent production fragment containing both `W` and `N`, or do further named peaks appear?
- **Decision:** PROMOTE `WORD_SIMP_RULES` as **EXACT — HUMAN PROOF** and the full-table peak as **REFUTED**. Full-table confluence is a permanent non-claim inside the production table. Do not open a numbered milestone. Do not install `N∘K3`. Do not edit `BTCalculus/Confluence.lean`.

## One-way N∘K3 enlarges SIMP to a confluent W+N fragment (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Does adding the exact missing commute `N∘K3`, and keeping only one-way `N`-commutes, yield a larger confluent production fragment containing both `W` and `N`, or do further named peaks appear?
- **Hypotheses:** (A) SIMP + one-way `N∘W` / `N∘D` (oriented carefully) + `N∘K3` is terminating and locally confluent; or (B) a named new peak appears
- **Major results:** `WORD_WN_RULES` = SIMP + one-way `N∘S→S∘N`, `N∘W→W∘N`, `N∘K3→K3∘N` terminates on `(I0-count, N-inversion, length)` and every string-rewriting critical pair joins, including the old `N∘W∘W` peak (now `K3∘N`). `N∘S` is required (`N∘W∘S → W∘N∘S | W∘N` without it). The opposite orientation `K3∘N→N∘K3` fails at `N∘W∘K3`. Two-way `N∘K3` is a cycle. Production `WORD_REWRITE_RULES` was not widened
- **Refuted ideas:** that `N∘K3` is enough to add one-way `N∘D` to SIMP — peaks `N∘D∘Ip → D∘N∘Ip | N` and `N∘D∘Im → D∘N∘Im | N` (no word-level `I±` sign-flip). The earlier bounded `{N,D,S,W,K3}` check hid this by omitting `D∘I±`
- **Literature:** Knuth–Bendix / Newman for string rewriting is KNOWN. The named W+N fragment and the `N∘D∘I±` obstruction are project-specific
- **Next question:** do the tree-level `I±` sign-flips, installed as word rules, join `N∘D∘I±` without a new named peak, or is a W+N+D word fragment a different object?
- **Decision:** PROMOTE `WORD_WN_RULES` as **EXACT — HUMAN PROOF** and SIMP+`N∘D` as **REFUTED**. `N∘K3` enlarges the confluent W+N fragment and is not enough for `N∘D`. Do not open a numbered milestone. Do not install `N∘K3` or `N∘D` in default production. Do not edit `BTCalculus/Confluence.lean`.

## Word I± sign-flips close a confluent W+N+D fragment (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Do the tree-level `I±` sign-flips, installed as word rules, join `N∘D∘I±` without a new named peak, or is a W+N+D word fragment a different object?
- **Hypotheses:** (A) `WORD_WN_RULES` + one-way `N∘D` + exact word `N∘Ip → Im∘N`, `N∘Im → Ip∘N` is T+LC; or (B) a new named peak appears, or the sign-flips are not exact as pure word rules
- **Major results:** `WORD_WND_RULES` = WN + one-way `N∘D→D∘N` + `N∘Ip→Im∘N` + `N∘Im→Ip∘N` terminates on `(I0-count, N-inversion, length)` with pushable `{S,W,K3,D,Ip,Im}` and every string-rewriting critical pair joins, including the old `N∘D∘I±` peaks (`D∘N∘Ip → D∘Im∘N → N`). The identities are exact (`I_a(x)=a+3x`). Reverse `N∘D` and reverse sign-flips are cycles. Production `WORD_REWRITE_RULES` was not widened
- **Refuted ideas:** that word-level `I±` sign-flips are a different encoding than a named W+N+D fragment — they are exact pure word rules and close the fragment
- **Literature:** Knuth–Bendix / Newman for string rewriting is KNOWN. The named W+N+D fragment is project-specific
- **Next question:** do the remaining production one-way commutes (`N∘M2`, `N∘Wz`, `N∘Wt`) enlarge WND without a new named peak, or does each need a companion the way `N∘D` needed `I±`?
- **Decision:** PROMOTE `WORD_WND_RULES` as **EXACT — HUMAN PROOF**. Tree `I±` sign-flips, as one-way word rules, join `N∘D∘I±` and do not create a new peak. Do not open a numbered milestone. Do not install `N∘D` or the sign-flips in default production. Do not edit `BTCalculus/Confluence.lean`.

## Finite-context gate for misere quotients (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Decide whether finite-context signatures, distinguishing contexts, and candidate-monoid audits give a new exact method or reduction for misere quotients, beyond Plambeck–Siegel.
- **Hypotheses:** a bounded context family might certify the true quotient for a meaningful class; distinguishing-context statistics might reveal structure before the quotient is known; the laboratory pattern might help on `Q_34(0.07)`.
- **Major results:** contextual indistinguishability is already the classical congruence, so `Σ_C` is that relation restricted to a finite list; on 2116 positions of octal `0.123` the published 20-element monoid predicts every misere outcome; context refinement class counts are `2,3,3,4,5,10,15,20` at totals `0,1,2,3,4,6,8,12`, recovering all 20 published classes with 190 pairwise witnesses and no missing separator; represented products match the published table; single-heap contexts yield only 11 classes, so the heap alphabet is not a complete `C*`; Dawson’s Kayles single-heap P-positions through 33 are `2,3,7,8,12,16,17,21,22,26,30,31` and agree with published Q33 Φ-labels; a multiplicity-bounded `0.07` slice ends at 6 finite-context classes and is not `|Q_n|`; `Q_34` was not attempted. No reset-style or BT-arithmetic encoding was used.
- **Refuted ideas:** that finite-context refinement is a new quotient construction; that a short native context family (single heaps, or total size `≤ 4`) already equals the true `0.123` quotient; that class growth on a bounded slice is evidence about `Q_34`.
- **Literature:** Plambeck 2005 (20-element `0.123`); Plambeck–Siegel 2008 / 2007 supplement (partial quotients, MisereSolver, reducedness); Siegel 2007 (finite-quotient classification); Nowakowski unsolved-problem list (`|Q_33(0.07)|=638`; is `Q_34` infinite?). The `miseregames.org` Q33 heading “Complete Solution is Known” is a template artefact.
- **Open:** nothing on this line. `Q_34(0.07)` remains the literature’s open problem and does not reopen the gate.
- **Decision:** CLOSE — REPARAMETERIZATION / TOOLING ONLY. A branch whose surviving statements are the classical indistinguishability congruence plus reproduced known tables is a close. Do not build CLI, visualization, Lean, or a generic misere solver. Do not open a numbered milestone.

## Regular-output preimage gate for x^2 (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Decide whether the regular output constraint Y={0,+}^ω makes the input preimage of F(x)=x^2 sofic, despite F having infinitely many polynomial sections.
- **Hypotheses:** a regular output restriction might close a finite residual subsystem; the safety language might coincide with the zero-output lifting tree.
- **Major results:** the identity map has one live residual and a regular preimage {0,+}^*; the x^2 safety language strictly contains the lifting language, witness (+); live type counts at horizon 7 grow as 1,3,7,16,33,66,131,260 through depth 7; the residuals g_m=3^{m+1}x^2+2x of the prefixes 10^m are pairwise distinguished by w_m=(-1)^{m+1}0, by comparing 2p_k=1-3^k with the valuation-m+1 correction 3^{m+1}p_k^2. Hence L is not regular.
- **Refuted ideas:** that {0,+}^ω collapses the infinite residual tree of x^2; that the target language is the lifting tree.
- **Literature:** Ahmed–Savchuk (nonlinear ⇒ unrestricted infinite-state) remains KNOWN and does not name this pair; the packing witness is PROJECT-SPECIFIC.
- **Open:** none on this branch.
- **Decision:** PROMOTE the non-regularity theorem for (x^2,{0,+}^ω). Do not open a numbered milestone. Do not add CLI, Lean, or a ledger row in this pass.
- **Pending ideas, not opened:** exact laws for unrestricted C_F(m,r); section entropy versus dynamical entropy; solenoid / adelic packaging.

## Balanced-Monna endpoint spectra gate (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Classify balanced-Monna endpoint pairs, decide whether x^3 preserves their equivalence, and derive the exact 3-adic divergence-depth spectrum.
- **Hypotheses:** midpoint valuations might give a closed arithmetic spectrum beyond generic Monna discontinuity.
- **Major results:** endpoint pairs are the two opposite-tail expansions after a finite prefix, with u-v=4·3^n; B is the classical digit-reversal map in balanced coordinates (KNOWN / REPARAMETERIZATION); u^3-v^3=4·3^n(3ζ^2+4·3^{2n}) and t=n+min(1+2v_3(ζ),2n), or 3n when ζ=0; the spectrum at level n≥1 is 2 copies of depth 3n and 4·3^{n-s-1} copies of depth n+1+2s; x^3 preserves no pair through n≤5 and the identity forbids equality; x, -x, and constants preserve every pair; x+1 fails exactly on kind plus with prefix +^n; 2x+1 preserves none. Census: 728 pairs, 0 formula failures, 0 depth mismatches.
- **Refuted ideas:** that a valuation match is preservation; that x^3 or 2x+1 preserve a positive-density subset of fibres; that the branch should reopen M_k(x^3).
- **Literature:** Monna 1952 and real plots of 1-Lipschitz maps are KNOWN; the cubic law and the x+1 carry exception are PROJECT-SPECIFIC.
- **Open:** none on this branch.
- **Decision:** PROMOTE the cubic divergence-depth law and the stated preservation classification. Do not open a numbered milestone. Do not add CLI, Lean, cubic-count code, or a ledger row in this pass.
- **Pending ideas, not opened:** exact laws for unrestricted C_F(m,r); section entropy versus dynamical entropy; solenoid / adelic packaging.

## Balanced-Monna ledger packaging (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Record the already-promoted Monna theorems in the ledger and the theory reading path. No new mathematics.
- **Hypotheses:** none; this is documentation of existing proofs.
- **Major results:** theory page `docs/theory/monna_endpoint_spectra.md`; ledger rows `BTM-balanced-monna` (REPARAMETERIZATION), `BTM-x3-depth`, `BTM-x3-spectrum`, `BTM-x3-no-preserve` (all EXACT — HUMAN PROOF). Affine controls stay in the theory page and dossier only.
- **Refuted ideas:** none new.
- **Literature:** Monna 1952 cited on the theory page (`monna-1952-digit-reversal`), not as a ledger tag.
- **Open:** none on this branch. Lean remains deferred.
- **Decision:** PROMOTE the packaging. Do not open a numbered milestone. Do not add CLI, Lean, or any operator family. Do not reopen `M_k(x^3)`.

## Rewrite-calculus research artifact (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** After a bounded literature audit, decide whether the maximal unary tree core plus the Add/carry exclusion is a project-specific classification theorem, or only unique expansion plus routine Newman
- **Hypotheses:** the coherent package — complete `{D,I_a,S,N}` canonical form, necessity of oriented `N(D)→D(N)`, and exact exclusion of Add from a finite tree TRS — survives comparison with signed-digit arithmetic and term-rewriting literature
- **Major results:** Newman / Knuth–Bendix (`newman-1942-confluence`, `baader-nipkow-1998-term-rewriting`) and unique BT expansion (`knuth-taocp-vol2`) remain KNOWN method; Avizienis signed-digit addition and Peterson–Stickel AC completion are KNOWN and do not state the `{D,I_a,S,N}` maximality theorem or the six-identity classification `U(x)+V(y)=W(x+y)`. Two central claims stay PROJECT-SPECIFIC and form one package. Dossier `docs/problems/rewrite_calculus.md`; publication status `PAPER_CANDIDATE`. Word-table enlargement beyond `WORD_WND_RULES` is CLOSE. Production `WORD_REWRITE_RULES` was not widened. No Lean, CLI, or census in this pass
- **Refuted ideas:** that usefulness of this line depends on further named word fragments (`N∘M2`, `N∘Wz`, `N∘Wt`); that Avizienis already contains the Add-exclusion TRS theorem
- **Literature:** the four new registry records plus Knuth / Hayes / Setun. Novelty table in `docs/theory/rewrite_calculus.md`
- **Open:** Lean packaging of the two distinctive human rows (`BTC-unary-s-distrib-obstruction`, `BTC-add-affine-only`) without an AC-matching library
- **Decision:** PROMOTE the classification as a paper-candidate artifact. CLOSE further word-table enlargement. Do not open a numbered milestone. Do not install Add or extra production commutes. Cubic residuals remain the frontier.

## Rewrite-calculus formalization gate (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Can Claim A and a *restricted* Add/carry exclusion be Lean-verified without an AC-matching library?
- **Hypotheses:** unary completeness already lives in OpFrag*; the next-state output `D(x+y)` is not determined by `(D(x),D(y))`; constructor-sum identities classify by slope/const; the named carry-free S-through-Add system fails local confluence at `D∘S`
- **Major results:** `RewriteCore.unary_complete_canonical_form` packages Claim A. `RewriteAddBoundary` proves `add_not_DLocal` (witness `(0,0)` vs `(1,1)`), `exactTriple_characterization` (eight concrete triples), `not_exact_Ip_Ip` / `not_exact_Im_Im`, and `pushIn_not_locally_confluent`. Packaged exclusion: `add_requires_carry_state`. No `sorry`. No word-table enlargement. No AC library. Ledger rows `BTC-add-not-D-local`, `BTC-constructor-sum-class`, `BTC-push-in-S-peak`, `BTC-add-requires-carry-state` are **EXACT — LEAN VERIFIED**. The unrestricted “any TRS is a CAS” wording stays human
- **Refuted ideas:** that formalizing the boundary requires a generic AC-matching engine; that `D(x+y)=D(x)+D(y)` is exact
- **Literature:** Newman / Avizienis / unique expansion remain KNOWN. D-locality failure + six-row classification + named peak remain PROJECT-SPECIFIC
- **Open:** none on this gate. Drafting the note is editorial, not a rewrite milestone
- **Decision:** PROMOTE the restricted formalization. CLOSE further rewrite enlargement. Do not open another rewrite milestone.

## Rewrite-calculus reviewer packet (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Make the paper-candidate artifact sendable: one page that separates Lean from human claims and KNOWN method from PROJECT-SPECIFIC classification
- **Hypotheses:** none; this is editorial packaging of existing theorems
- **Major results:** `docs/theory/rewrite_calculus_reviewer_packet.md` states the single review question, the restricted carry-state theorem, the claim map, the five suggested falsifiers, and the files not to review
- **Refuted ideas:** none new
- **Literature:** unchanged from the formalization gate
- **Open:** none on this line. External review is the next stage
- **Decision:** PROMOTE the packet as the sendable unit with the publication draft. CLOSE further rewrite documentation. Do not open another rewrite milestone. Cubic residuals remain the frontier.

## Rewrite-calculus companion UI (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Instantiate the paper witnesses in the existing Streamlit laboratory, for local play, without a second app or repo
- **Hypotheses:** none; presentation of existing theorems
- **Major results:** one page under Calculus research with views Claim map, Unary, Carry, Constructor sums, Push-in peak. View-model `visualization.rewrite_explorer` calls `rewrite_once` / `D` / `I_a` only. Add is not installed in `_step`. Word tables stay closed
- **Refuted ideas:** none new
- **Open:** none. Isolated reviewer deploy remains deferred
- **Decision:** PROMOTE the companion page as laboratory infrastructure. CLOSE further rewrite UI (no rule editor, no word-fragment view, no second remote). Cubic residuals remain the frontier.

## Rewrite-paper refinement and maximality gate (not a numbered milestone)

- **Date:** 2026-08-23
- **Objective:** Recenter the publication note on the exact theorem that `D(x+y)` does not factor through `(D(x),D(y))`, and test whether a natural restricted carry-free maximality theorem follows without generic TRS machinery
- **Hypotheses:** output-level D-locality gives the cleanest statement; a short syntactic class might make completeness imply D-locality
- **Major results:** `DLocal H` now means `H(x,y)=G(D(x),D(y))`; `add_not_DLocal` applies it explicitly to `H(x,y)=D(x+y)`. The paper is reorganized as unary canonicality → exact locality theorem → carry explanation → named push-in peak. Constructor sums and word fragments are appendices. `add_requires_carry_state` is secondary packaging
- **Refuted ideas:** that a bounded universal maximality theorem follows naturally. Defining carry-free by D-locality assumes the contradiction; assuming the named descendants remain irreducible proves only peak persistence; deriving locality from general completeness requires the generic TRS metatheory excluded by the gate
- **Literature:** unique balanced expansion, Avizienis signed-digit arithmetic, and Newman / Knuth–Bendix remain the three concise KNOWN comparisons
- **Open:** external review of the D-locality definition, minimal witness, unary semantic canonicity, and named peak
- **Decision:** PROMOTE the tightened paper centered on `add_not_DLocal`. CLOSE the restricted maximality attempt as artificial or metatheoretically bloated. Add no maximality file or ledger row. Stop the rewrite branch after verification.

## Newton-stratum note packaging (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Extract the already-proved Newton-stratum fibre laws into a short sendable note, without new mathematics
- **Hypotheses:** none; this is editorial packaging of existing theorems
- **Major results:** `docs/theory/newton_stratum_note.md` states the unified \(N_2\) / \(N_1\) / \(N_0\) theorem, the \(Q\) boundary on the family \(1+3^tb\), the novelty table against Cahen–Chabert / Kempner / Ahmed–Savchuk, and the Lean source map. Status stays `STRUCTURAL`. No Lean, ledger row, CLI, or count
- **Refuted ideas:** none new
- **Literature:** unchanged from [residual_vs_classical.md](theory/residual_vs_classical.md)
- **Open:** none on this packaging line. The residuals dossier still asks whether the stratum says anything exact about a family other than \(x^3\); that question is not opened here
- **Decision:** PROMOTE the extract. CLOSE further Newton-stratum documentation in this pass. Do not open a numbered milestone. Do not reopen \(Q\) or \(M_k(x^3)\).

## Balanced digit sums of nonlinear polynomial values (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether \(E^{\mathbb Z}_{P,0}=\{n:s_{\mathrm{bal}}(P(n))=0\}\) for nonlinear \(P\) has a law not inherited from ordinary ternary digit sums
- **Hypotheses:** signed cancellation yields a finite-state recognizer, an unbounded predictive-state theorem, or an exact cylinder recursion
- **Major results:** translation \(s_{\mathrm{bal}}(m)=s_3(2\lvert m\rvert)-s_3(\lvert m\rvert)\) holds, so the integer target is the ordinary correlation \(s_3(2\lvert P(n)\rvert)=s_3(\lvert P(n)\rvert)\); terminal correction \(s_{\mathrm{bal}}(P(n_w))=\sum\mathrm{outputAlong}(w,P)+s_{\mathrm{bal}}(P_w(0))\); exact census through \(k=10\) on \(\{x^2,x^3,x^3-x,x^4,x^2+x\}\) (38.5s); joint states \(=3^k\); \(x^2\) exact zeros \(1,1,3,5,15,35,109,279,781,2251,6495\); prefix cylinders are not nested; ordinary \(s_3(P(n))=0\) is essentially empty on the same window
- **Refuted ideas:** a depth-independent finite-state recognizer of \(s_{\mathrm{bal}}(n^2)=0\); \(S_k=0\) equals the exact integer zero; \(E^{(k)}_{P,0}\) is a nested 3-adic inverse limit
- **Literature:** `oeis-A065363`, `ruskey-sawada-2009-digital-sum-gf`, `peter-2002-summatory-digits-polynomials`, `drmota-mauduit-rivat-2011-sum-of-digits-polynomials`, `stoll-2012-digits-polynomial-ap`, `allouche-shallit-2003-automatic-sequences`; Ahmed–Savchuk / Anashin / Avizienis / Monna remain `KNOWN`
- **Open:** none. Digital-root depth, jump-depth, and Monna plots were not opened
- **Decision:** CLOSE. The integer predicate is a reparameterization of ordinary digit sums. The census is a horizon-dependent table with no exact nonlinear invariant. Do not open Phase 1, CLI, Lean, or a theory page.

## Quartic Newton-stratum Phase 0 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether same-depth fibres of \(F_k\) for \(x^4\) admit an \(N_*\) visibility / valuation law at deficits \(r=0,1\), or whether the first obstruction appears immediately
- **Hypotheses:** some Newton coordinate of \(x^4\) sees \(p\bmod 3^r\), and after that \(v_3(p)<r\) is injective; or the cubic tower continues with \(N_2\mapsto N_3\) and \(3r\mapsto 4r\)
- **Major results:** closed form \(D^m((p+3^m x)^4)=3^{3m}x^4+4p\,3^{2m}x^3+6p^2 3^m x^2+4p^3 x+D^m(p^4)\); linear coefficient valuation \(2m\) on units, so \(N_3=N_4=0\) at \(r\in\{0,1\}\) for \(k\ge 3\); exhaustive scan \(2\le k\le 7\); no residue visibility for \(k\ge 4\) at \(r=1\); \(N_2\equiv 4p^2 3^{k-1}\pmod{3^k}\) (square filter); leftover is the two-regime fourth-power image; \(N_1\) visibility at \((3,1)\) is a width-\(3\) accident
- **Refuted ideas:** that the cubic \(N_2\) visibility law lifts by incrementing the Newton index; that every \(N_j\) fails only as a collision table without a named valuation obstruction
- **Literature:** unchanged from [residual_vs_classical.md](theory/residual_vs_classical.md); comparison object [newton_stratum_note.md](theory/newton_stratum_note.md)
- **Open:** none. Do not open \(x^5\), a quartic count, a fibre taxonomy, CLI, Lean, or a ledger row
- **Decision:** CLOSE. The first obstruction is immediate: only degree 3 has a linear residual coefficient of valuation \(m\). The leftover is another unmatched \(D^t(u^4)\) image. Not PARK — there is no sharp linear law at \(r=0,1\) waiting for general \(r\).

## Documentation index tidy (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Align the module table and reading path with the recorded decisions, without a package move
- **Hypotheses:** none; editorial
- **Major results:** `docs/architecture/research_modules.md` and the root README now list every registered module; missing dossiers (`regular_output_preimages`, `balanced_digit_sum_polynomials`) are on the documentation map; the live task is the rewrite note, and the cubic stratum is labelled as the last mathematical theory rather than a new-math frontier
- **Refuted ideas:** none
- **Open:** none. No reorganization, no deletion of parked modules, no UI change
- **Decision:** PROMOTE the index text. CLOSE further tidy work on this pass.

## Visibility class, residual sums, and Eisenstein (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Phase 0 on three candidates: a visibility class for general \(f\in\mathbb Z[x]\), the residual of a sum, and an Eisenstein translation of \(N_2\)
- **Hypotheses:** visibility is a 3-adic condition on the cubic part; residual\((f+g)\) needs a carry polynomial; \(F_k(x^3)\) is a statement about \(\operatorname{Int}(\mathbb Z[\omega])\)
- **Major results:** degree \(\le 3\), deficit 1, \(k\in\{4,5\}\): residue visibility iff \(v_3(a_3)=0\) (624 polynomials, 0 mismatches); \(x^3+x^4\) kills the law by same-valuation \(p^2\); \(x^5\) is visible via \(p^3\equiv p\pmod 3\); \(\mathrm{residual}(f+g)-\mathrm{residual}(f)-\mathrm{residual}(g)\) is always a constant trit carry; Eisenstein \(3\sim(1-\omega)^2\) and Zantema’s cyclotomic Pólya theorem are KNOWN and do not yield a new fibre law
- **Refuted ideas:** that the visibility class is \(\{x^3\}\) or a single predicate through degree 5; that addition produces a residual-valued carry of positive degree; that the cubic stratum is the Eisenstein Pólya basis
- **Literature:** `eisenstein-3-ramification`, `zantema-1982-integer-valued-number-fields`; Cahen–Chabert unchanged
- **Open:** none. Do not open an \(x^5\) taxonomy, a carry-polynomial CLI, or an \(\operatorname{Int}(\mathbb Z[\omega])\) formalization
- **Decision:** PROMOTE the degree-\(\le 3\) cubic-unit law as a corollary of the stratum. CLOSE the general-\(f\) classifier, the residual-sum candidate, and the Eisenstein probe.

## Jet-local operations and residual realization (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Phase 0 on D-locality of binary maps and on which Mealy machines are residual machines
- **Hypotheses:** addition is the unique bilinear obstruction to D-locality of \(D\circ H\); residual machines are the Mealy machines whose states are Newton tuples
- **Major results:** \(D(\max(x,y))=\max(D(x),D(y))\) and \(D(\min)=\min\circ D\) on \(\mathbb Z\); among \(axy+bx+cy+d\) with coeffs in \(\{-2,\ldots,2\}\), \(D\circ H\) is D-local only for constants and \(\pm x,\pm y\); gcd is not D-local; one-state residual machines are exactly \(ax\) for a trit (3 of 729 abstract tables); 12 two-state residual graphs in the degree-\(\le 2\) box
- **Refuted ideas:** that addition is the unique bilinear obstruction; that a length-1 jet including both \(D\) and \(\mathrm{lsd}\) is a nontrivial locality class (it reconstructs the input); that every Newton-shaped or small Mealy table is a residual machine
- **Literature:** Avizienis / carry already on the rewrite note; Kempner prefix functions already on the residual note
- **Open:** none. Do not enlarge the rewrite paper, do not enumerate 9-state machines, no Lean wrap of \(\max\)
- **Decision:** PROMOTE the lattice commutation lemma and the one-state list. CLOSE the general operation classifier and the general realization census.

## Newton-stratum note: degree-≤3 visibility sentence (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Record the degree-\(\le 3\) cubic-unit visibility corollary on the existing extract, without a new theorem file
- **Hypotheses:** none; editorial packaging of a Phase-0 corollary
- **Major results:** [newton_stratum_note.md](theory/newton_stratum_note.md), [cubic_newton_stratum.md](theory/cubic_newton_stratum.md), and [residual_vs_classical.md](theory/residual_vs_classical.md) now state that deficit-\(1\) residue visibility for \(\deg f\le 3\) is \(v_3(a_3)=0\). Status of the extract stays not-`PAPER_CANDIDATE`. No ledger row, no Lean
- **Refuted ideas:** none new
- **Open:** none. The live publication task remains the rewrite note
- **Decision:** PROMOTE the sentence. CLOSE further stratum documentation in this pass.

## General Newton kernel and residual shift (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Formalize the two missing Lean cogs that make a general \(f\in\mathbb Z[x]\) a first-class residual object: the Newton kernel of \(I_k\), and \(D^{|w|}(f(p+3^{|w|}x))\)
- **Hypotheses:** both statements are classical and compile without a new residual taxonomy
- **Major results:** `vanishesMod_iff_newtonKernel` and `equivK_iff_newtonCoeff` for every degree (`BTA-Ik-newton` retagged **EXACT — LEAN VERIFIED**); `eval_residualAlong` (`BTA-eval-residualAlong`); Python `residual_shift` is the binomial coefficient face and matches `residual_along`
- **Refuted ideas:** none. The binomial coefficient polynomial `residualShift` is named in Lean; a coefficientwise identification lemma is not required for the kernel
- **Literature:** Kempner / Cahen–Chabert unchanged; this is the formalization gap recorded in [polynomial_function_congruence.md](theory/polynomial_function_congruence.md) §12 and §16
- **Open:** none opened. Do not wrap the degree-\(\le 3\) visibility corollary, do not start an \(x^5\) taxonomy, do not add CLI
- **Decision:** PROMOTE the two cogs. CLOSE further Lean packaging in this pass. The live publication task remains the rewrite note.

## Erdős distinct subset sums Phase 0 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether canonical BT normalization, carry, or \(v_3\) of signed sums constrains sum-distinct sets beyond the elementary kernel \(R(A)=\{0\}\)
- **Hypotheses:** H1, every useful consequence is the signed-kernel definition plus size/concentration; H2, a digit-pattern or valuation obstruction is new
- **Major results:** signed-kernel equivalence is the DFX \(\varepsilon\in\{-1,0,+1\}^n\) language; \(\operatorname{encode}(s)\) is a complete invariant of the integer; magnitude–valuation hits equal \(R(A)\); exact census \(n\le 12\) on powers of 2, Conway–Guy / A276661, powers of 3; \(\{1,2,4\}\) is sum-distinct but not signed-sum-distinct; powers of 3 are signed-sum-distinct and worse than powers of 2 (\(177147\) vs \(2048\) at \(n=12\)); Conway–Guy \(R_{12}=16995\), powers of 2 \(R_{12}=8191\)
- **Refuted ideas:** high \(v_3\) forces an exact relation; a BT digit pattern is forbidden on every sum-distinct set; digit length is a sharper magnitude bound; a 3-adic method reproduces DFX
- **Literature:** `erdos-problems-1`, `erdos-moser-1956`, `dubroff-fox-xu-2021`, `steinerberger-2023-distinct-subset-sums`, `conway-guy-1968`, `lunnon-1988-distinct-subset-sums`, `bohman-1996-conway-guy`, `bohman-1998-construction`, `bae-1996-subset-sum-distinct`, `cambie-gao-kim-liu-2025-modular`, `gu-2025-generalisation`, `oeis-A276661`, `oeis-A005318`; Avizienis remains `KNOWN`
- **Open:** none. No Phase 1, CLI, UI, Lean, or ledger row
- **Decision:** CLOSE. The exact statements are `KNOWN` or `REPARAMETERIZATION`. The live publication task remains the rewrite note.

## Generalized Ostrowski order-(m) adder Phase 0 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether Baranwal’s genuine order-3 \(\Gamma\)-system has a finite unread-tail residual box, analogously to thesis Theorem 2.2
- **Hypotheses:** H1, order-\(m\) addition admits a finite-state realization with \(O(m)\) carry dimensions; H2, the state is the normalized residual \(E_i=\sum_{k=1}^{m}s_k q_{i-m+k}\); H3, the proposed §5.3 digit rules give a unique complete system
- **Major results:** residual recurrence derived and order-2 regression of Theorem 2.2; acceptance iff \(\sum w_i q_i=0\); Phase-0 \(\Gamma=([0;\overline{2}],[0;\overline{1}],[0;\overline{1}])\) is an irreducible cubic Pisot system, not disguised Ostrowski; \(\lvert t_m\rvert\le 1\) is not a sufficient box; \(\lvert t_m\rvert\le 2\) matches addition below \(q_5\) with 85 raw / 64 live minimized states; unrestricted coordinates grow
- **Refuted ideas:** proposed §5.3 rules are unique (Fibonacci and Phase-0 collisions, smallest \(5=(0,0,1)=(1,2,0)\)); naive copy of \(\{-1,0,1\}\) for the last coordinate; LSD-first with the same unread-tail formula
- **Literature:** `baranwal-2020-ostrowski-thesis`, `baranwal-schaeffer-shallit-2021-ostrowski-automatic`, `hieronymi-terry-2018-ostrowski-addition`, `frougny-solomyak-1996-linear-numeration`, `shallit-1994-numeration-regular`, `hieronymi-et-al-2024-sturmian-decidability`. The \(m\)-dimensional state was already suggested. Pisot existence of some adder is `KNOWN`
- **Open:** none opened. No Phase 1, CLI, Walnut, Lean, or order 4
- **Decision:** PARK. Computational finite box and exact residual invariant, no proved closure, and existence of some adder is a Pisot reparameterization. The live publication task remains the rewrite note.

## k-abelian residual signatures of automatic sequences (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether a laboratory residual of \(k\)-abelian factor classes explains known \(b\)-regular complexity, or whether that residual is the classical \(k\)-block-coding construction
- **Hypotheses:** \(\Sigma_k\) plus a bounded suffix might form a finite transition system distinct from Walnut / block coding; the DFAO state of an automatic sequence might already determine future \(k\)-abelian classes
- **Major results:** KSZ triple \((\mathrm{pref}_{k-1},\mathrm{suff}_{k-1},\psi_k)\) equals the class and is \(k\)-block coding plus borders; growing-factor extension of that triple is a congruence (0 conflicts on TM / period-doubling / Cantor, \(k\le 2\) and Cantor \(k=3\), \(n\le 24\)); sliding-window Rauzy is not a congruence (e.g. 1360 conflicts for TM \(k=1\), \(n=8\)); raw signatures unbounded; naive (DFAO, suffix) strictly coarser for \(k\ge 2\) (TM \(k=2\), \(n=24\): 4 naive states, 12 classes); relative class catalogues grow when \(\rho\) is unbounded; published prefixes and TM abelian \(2,3,2,3,\ldots\) recovered; empirical kernel 4-term counts are finite in the table and are not a regularity proof
- **Refuted ideas:** that raw \(\Sigma_k\) is a finite residual; that DFAO state plus suffix determines the class; that a finite \(n\)-independent class residual is the mechanism of \(b\)-regularity; that KSZ classes form a sliding transition congruence
- **Literature:** `karhumaki-saarela-zamboni-2013-k-abelian`, `parreau-rigo-rowland-vandomme-2015-2-regular`, `greinecker-2015-tm-2-abelian`, `chen-lu-wu-2017-cantor-k-abelian`, `shallit-2020-abelian-synchronization`, `couvreur-et-al-2025-pisot-k-abelian`, `allouche-shallit-2003-automatic-sequences`. The KSZ triple is a `REPARAMETERIZATION` of block coding. The general regularity conjecture remains `OPEN` in the literature and was not attacked
- **Open:** none on this line. Balanced-trit addressing of the same 3-automatic DFAO is a coordinate change and does not reopen the gate
- **Decision:** CLOSE — REPARAMETERIZATION. A branch whose surviving statements are the classical KSZ / block-coding description of \(k\)-abelian classes is a close. Do not build CLI, visualization, Lean, or `bt.*` complexity infrastructure. Do not open a numbered milestone.

## Order-3 Ostrowski residual closure (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Prove or refute a finite forward-invariant unread-tail region in \(\mathbb Z^3\) for the Phase-0 \(\Gamma=([0;\overline{2}],[0;\overline{1}],[0;\overline{1}])\)
- **Hypotheses:** H1, \(\lvert s_3\rvert\le 2\) is the invariant; H2, a coupled finite \(B_{\min}\) is the actual object; H3, live tail bounds force closure the way Theorem 2.2 does
- **Major results:** specialized map \((s_1,s_2,s_3)\mapsto(s_3,s_1+s_3,s_2+2s_3-w)\); legal \(w\in\{-4,\ldots,2\}\) (LSD \(\{-2,\ldots,1\}\)); live reachable set is an explicit 55-element \(B_{\min}\); \(\lvert s_3\rvert\le 2\) is the projection, not a sufficient box (Phase-0 85 = \(B_{\min}\) plus 30 never-live states); 108 exterior images are dead for all remaining lengths by gap recurrences \(G_i=2G_{i-1}+G_{i-2}+G_{i-3}-5\) and \(H_i=2H_{i-1}+H_{i-2}+H_{i-3}-10\); no live escape with \(\lvert s_3\rvert\ge 3\); sign-flip is not a symmetry
- **Refuted ideas:** that \(\lvert s_3\rvert\le 2\) alone is the invariant; that the 85-state table is \(B_{\min}\); that unrestricted (non-live) residuals stay bounded
- **Literature:** same BSS / Hieronymi–Terry / Frougny–Solomyak / Shallit 1994 ids. No later paper found that writes this 55-set. Pisot existence of some adder remains `KNOWN`
- **Open:** none opened here. No order 4, CLI, Walnut, or Lean
- **Decision:** PROMOTE the live invariant \(B_{\min}\) for this \(\Gamma\). Do not generalize automatically. The live publication task remains the rewrite note.

## Spectral obstruction, Pisot vs one non-Pisot order-3 \(\Gamma\) (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether finite live residual closure for the Baranwal unread-tail process is tied to Pisot-type spectral contraction, by comparing \(\Gamma_{\mathrm P}=([0;\overline{2}],[0;\overline{1}],[0;\overline{1}])\) with one genuine non-Pisot order-3 \(\Gamma\)
- **Hypotheses:** H1, Pisot contraction of the place-value recurrence implies bounded live residuals; H2, a non-Pisot conjugate with \(\lvert\mu\rvert\ge 1\) forces an unbounded live family; H3, liveness might still cut the extra expanding modes
- **Major results:** \(\Gamma_{\mathrm{NP}}=([0;\overline{2}],[0;\overline{1}],[0;\overline{3}])\) locked after an integer certificate (irreducible, \(\Delta=-439<0\), \(\lambda\in(2,3)\), conjugate modulus squared \(3/\lambda>1\)); same memoryless alphabets as the control; residual matrix \(A\) has the place-value characteristic polynomial; control still \(\lvert B_{\min}\rvert=55\); \(\Gamma_{\mathrm{NP}}\) live union strictly increasing through length 16 with all three coordinates growing; hub \((-3,-1,0)\) live at every remaining length and reached at remaining \(2m\) by the prefix \((1,-2)\); FS1996 converse not imported
- **Refuted ideas:** that changing only \(d_3\) to \(3\) accidentally stays Pisot or becomes reducible; that \(\lvert s\mapsto -s\rvert\) was needed (alphabet still asymmetric); that finite-depth growth is a theorem of infinitude
- **Literature:** `frougny-solomyak-1996-linear-numeration` (Pisot \(\Rightarrow\) some adder `KNOWN`; existential converse not this residual), `hollander-1998-greedy-regularity` (greedy languages, not this residual), BSS / Hieronymi–Terry / Shallit 1994 unchanged
- **Open:** none opened. No order 4, CLI, Walnut, or Lean
- **Decision:** PARK. Spectral distinction and live growth are visible; an exact unbounded live family (or a finite non-Pisot invariant) is not proved. Do not continue automatically. The live publication task remains the rewrite note.

## Reverse contraction of A^{-1} versus the Γ_NP adder live set (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether reverse contraction of \(A^{-1}\) proves the unread-tail live residual set of \(\Gamma_{\mathrm{NP}}\) finite
- **Hypotheses:** H1, a rational \(Q\)-norm makes \(A^{-1}\) a contraction and therefore the live set finite; H2, the live set is the co-reachable set of a bounded accepting seed; H3, depth-16 growth already means infinitude
- **Major results:** exact \(A^{-1}\) over \(\mathbb Q\) and integer reverse of \(T_w\); SPD \(Q\) with Sylvester minors \(10,101,457\) and \(\lvert A^{-1}x\rvert_Q^2\le(49/50)\lvert x\rvert_Q^2\); accepting slice \(\{s_3=0\}\) is an infinite plane; only honest finite seed is \(\{(0,0,0)\}\); basin \(C(\{0\})\) has \(9164\) states, depth \(67\), contains the hub, does not contain \((30,25,0)\); Checks A/B on that basin; \(R_{\le 16}\) has \(1351\) live states of which \(700\) lie outside \(C(\{0\})\); control \(B_{\min}\) still \(55\)
- **Refuted ideas:** that \(\{s_3=0\}\) is a finite seed; that reverse contraction bounds forward live-from-0; that \(C(\{0\})\) is the 55-set analogue; that monotone depth-16 growth is a theorem of infinitude
- **Literature:** FS1996 unchanged (Pisot \(\Rightarrow\) some adder `KNOWN`; converse not this residual). Not a reparameterization of that paper: the residual-coordinate distinction is new and parked
- **Open:** whether the adder live set itself is finite. Not taken up
- **Decision:** PARK. Contraction of \(A^{-1}\) is proved and applies only to co-reachability of a seed that is not the adder live set. Do not `PROMOTE`. Do not `CLOSE`. No order 4, CLI, Walnut, or Lean. The live publication task remains the rewrite note.

## Accepting boundary of Γ_NP (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Identify the true length-indexed accepting/live terminal set \(K_n\), without substituting \(\{(0,0,0)\}\) or claiming reverse contraction bounds \(L\)
- **Hypotheses:** H1, remaining-0 acceptance is the plane \(F=\{s_3=0\}\); H2, \(K_n\) for \(n\ge 1\) is the unread-tail slab; H3, \(K\cap F\) might still be bounded
- **Major results:** \(E_0=s_3\) so \(K_0=F\) is infinite; \(K_n=\{s:\mathrm{lo}(n)\le E_n\le\mathrm{hi}(n)\}\) is an infinite slab; kernel family \(t_n=(q_{n-1},-q_{n-2},0)\in K_n\cap F\) with \(\lvert t_n\rvert\to\infty\); \((k,0,0)\in K_0\); \((30,25,0)\) is in \(K_0\) only (gap \(25 q_{n-1}>\mathrm{hi}(n)\)) and not in \(C(\{0\})\); hub is a bounded point of \(\bigcap_n(K_n\cap F)\); Pisot \(B_{\min}\) meets \(F\) in 18 states; same terminal predicate as \(\Gamma_{\mathrm{NP}}\); boxed windows are not \(\lvert K_n\rvert\)
- **Refuted ideas:** that \(K=\{(0,0,0)\}\); that \(K_0\) is a proper finite subset of \(F\); that \(\lvert K_n\rvert\) is finite; that unbounded \(K\) is a theorem of unbounded \(L\); that Pisot vs non-Pisot changes the terminal predicate
- **Literature:** FS1996 unchanged. Residual-coordinate terminal geometry is not that paper
- **Open:** whether unbounded \(K\) forces infinitely many distinct reachable live residuals from the origin. Not taken up
- **Decision:** PROMOTE the terminal-set theorem (Outcome A). Stop. Do not claim \(L\) finite or infinite. No order 4, CLI, Walnut, or Lean. The live publication task remains the rewrite note.

## Origin-reachable live set versus the kernel family t_n (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether \(t_n\in K_n\cap F\) (or any unbounded subset of \(K\)) meets \(R(0)\) in an unbounded live family from the origin
- **Hypotheses:** H1, some bridge word from \(0\) to \(t_n\) or another unbounded \(K\)-family; H2, a forward invariant separates \(R(0)\) from large \(K\); H3, finite-depth live growth already means \(\lvert L_0\rvert=\infty\)
- **Major results:** \(T_w(s)_1=3s_3\) so \(R(0)\subseteq\{s_1\equiv 0\pmod 3\}\); \(q_n\bmod 3\) has period \(8\); \(t_n\) is residue-incompatible unless \(n\equiv 0\pmod 4\); first reverse of \(t_n\) has a unique \(s_1\not\equiv 0\pmod 3\) except \(n\equiv 0,12\pmod{24}\); those \(t_n\) are unreachable; two-step \(F\to F\) lands on \((3a,a,0)\); Pisot \(B_{\min}\) uses all \(s_1\bmod 3\); \(L_{\le 18}\) has \(2036\) states, still growing, no \(t_n\), all \(s_1\equiv 0\pmod 3\)
- **Refuted ideas:** that unbounded \(K\) implies unbounded \(L_0\); that \(t_n\) is origin-reachable for \(n\not\equiv 0,12\pmod{24}\); that repeating \(w=1\) is a live unbounded family; that Pisot has the same \(s_1\bmod 3\) trap
- **Literature:** FS1996 unchanged. The obstruction is the NP matrix first row \(d_3=3\), not Pisot theory
- **Open:** \(\lvert L_0\rvert=\infty\) and the remaining \(t_n\) for \(n\equiv 0,12\pmod{24}\). Not taken up
- **Decision:** PARK. Exact obstruction for most of \(t_n\); neither infinite \(L_0\) nor a global bound. Do not continue automatically. The live publication task remains the rewrite note.

## Lean arithmetic obstruction for Γ_NP (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Machine-check \(n\not\equiv 0,12\pmod{24}\Rightarrow t_n\notin R(0)\) for \(\Gamma_{\mathrm{NP}}\), matching Python place-value indexing
- **Hypotheses:** the already-proved residue/predecessor obstruction is a trusted Lean kernel; not a live-set theorem
- **Major results:** Lean 4.19.0 / mathlib v4.19.0, `Ostrowski.NP.kernel_unreachable_of_not_exceptional`, zero `sorry`. `T_w(s)_1=3s_3`; `q_n` mod 3 period 8; shared predecessor first coordinate; period 24 of \((q_n)\) mod 9 classifies the four non-exceptional residues with \(3\mid q_{n-1}\). Python table \(n=1..48\) matches. Exceptional classes and \(\lvert L_0\rvert\) not claimed
- **Refuted ideas:** none new; indexing mismatch with Python `q_i`/`t_n` would have killed the branch
- **Literature:** FS1996 unchanged. The obstruction is the NP matrix first row \(d_3=3\)
- **Open:** \(n\equiv 0,12\pmod{24}\) and \(\lvert L_0\rvert\). Not taken up
- **Decision:** PROMOTE the Lean obstruction kernel. \(L_0\) stays PARK. Next question (not taken up): the classes \(n\equiv 0,12\pmod{24}\)

## Exceptional kernel classes n ≡ 0, 12 (mod 24) (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether some \(t_n\) with \(n\equiv 0\) or \(12\pmod{24}\) lies in \(R_W(0)\), or prove a stronger obstruction, or exhibit any unbounded family in \(L_0\)
- **Hypotheses:** H1, a modulus or linear form stronger than \(s_1\equiv 0\pmod 3\) excludes one or both classes; H2, legal \(F\to F\) or a short control block produces an infinite live family; H3, reverse cones of \(t_{12},t_{24},\ldots\) hit the origin
- **Major results:** the two classes occupy distinct residues \((6,5,0)\) and \((3,4,0)\) modulo \(9\), both reachable on \((\mathbb Z/9\mathbb Z)^3\) (81 states) and on the scanned moduli \(4,8,9,13,18,24,27\) with \(W\) and with free \(w\); no separating affine law besides \(s_1\)-reparams on \(m\in\{8,9,13\}\); legal two-step returns to \(F\) force the ray parameter \(k\in\{-2,-1,0,1\}\) (hub on the ray, \(t_n\) not); reverse cones of \(t_{12},t_{24},t_{36},t_{48}\) miss the origin at depth \(4\) with \(\min\ell_1>\lvert C(\{0\})\rvert\) scale; no repeating block of length \(\le 2\) hits those \(t_n\). Existing Lean theorem unchanged. Zero `sorry`
- **Refuted ideas:** that a small coordinatewise modulus excludes the exceptional classes; that repeated legal \(F\to F\) is an unbounded live family; that finite reverse depth is unreachability
- **Literature:** FS1996 unchanged
- **Open:** whether exceptional \(t_n\in R_W(0)\); \(\lvert L_0\rvert\). Not taken up
- **Decision:** PARK (outcome D). Sharpest pattern: asymmetric mod-\(9\) residues, both reachable as residues; bounded two-step ray. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Origin-live geometry: time-augmented quotients and accepting slabs (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether origin-live states \(L_n=R_n\cap K_n\) are unbounded, or confined by a time-augmented / spectral / linear invariant; stop targeting only \(t_n\)
- **Hypotheses:** H1, some \(G_m=(\mathbb Z/m\mathbb Z)\times(\mathbb Z/m\mathbb Z)^3\) or affine \(\ell(r,s)\) disconnects exceptional kernel phases from the origin; H2, largest-norm live states form a symbolic family in \(K_n\); H3, a linear form stays bounded on all origin-live states
- **Major results:** canonical \(E_i=s_1 q_{i-2}+s_2 q_{i-1}+s_3 q_i\); over-approx \(G_m\) for \(m\in\{8,9,12,18,24,27,36,48\}\) hits every exceptional phase (no separator); affine \(\alpha r+\beta s_1+\gamma s_2+\delta s_3\) on \(m\in\{8,9,12,18\}\) finds none besides discarded \(s_1\)/time reparams; exact windows with prefix hit \(t_{12},t_{24},t_{36},t_{48}\) as residues; live layers from start \(N=16\) have \(\lvert L_0\rvert=379\), \(\max\lvert s\rvert_\infty=37\) at \(s=(-3,-37,0)\), no \(t_n\); start \(12\) remaining \(0\) argmax is \((-27,-6,0)\), so extrema are not a stable ray; no \(q_n\)-ansatz; \(\lvert s_3\rvert\le 12\) at \(N=16\) is not invariant (\(\max\lvert s_3\rvert=14\) at the \(N=18\) union); Method A/B agree on boxed \(n\le 6\); existing Lean theorem unchanged
- **Refuted ideas:** that remaining-phase residues exclude the exceptional classes; that \(\lvert L_{\le N}\rvert\) is \(\lvert L_n\rvert\); that a miss of \(t_{48}\) at max-length \(49\) is an obstruction (horizon artifact; hits at \(52\)); that legal-\(w\) reachability is the live slab (\(N=4\) remaining \(0\): \(\lvert R_0\rvert=1192\), \(\lvert L_0\rvert=10\))
- **Literature:** FS1996 unchanged
- **Open:** \(\lvert L_0\rvert\); exceptional \(t_n\in R_W(0)\). Not taken up
- **Decision:** PARK (outcome E). Every tested \(G_m\) collapses; no symbolic live family; layer growth is a finite path. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, Walnut, or Lean

## Length-independent energy geometry of origin-live states (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether origin-live states obey a length-independent inequality, or exhibit an explicit unbounded live family in the energy slabs
- **Hypotheses:** H1, a combination of nearby energies yields an \(i\)-independent form in \(s\); H2, some integer \(\ell(s)\) stays bounded from start remaining \(16\) to \(20\); H3, live directions concentrate in a proper cone
- **Major results:** \(u_{i-1}A=u_i\) and \(E_{i-1}(T_w s)=E_i(s)-w q_{i-1}\) Lean-verified (`Ostrowski.NP.energy_step`, ledger `OST-np-energy-step`), novelty KNOWN; no three-term energy combination is length-independent; all \(342\) nonzero forms with coeffs in \(\{-3,\ldots,3\}\) grow \(N=16\to 20\); \(\lvert s_3\rvert\) \(12\to 19\); coord max \((36,37,12)\to(57,49,19)\); live union \(1351\to 2970\); projective cloud occupies both signs in every coordinate; \(E_i/q_i\) restates \(K_n\); Method A/B agree; `kernel_unreachable_of_not_exceptional` unchanged. Zero `sorry`
- **Refuted ideas:** that \(\lvert s_3\rvert\) or any small integer linear form is a length-independent live invariant; that three nearby energies cancel to a constant covector; that the empirical live cloud is a proper coordinate cone
- **Literature:** FS1996 unchanged. The energy identity is the residual construction, not that paper
- **Open:** \(\lvert L_0\rvert\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\) (outcome D). PROMOTE only the KNOWN energy lemma. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Energy trajectory and live-set fork (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether the multi-step energy law forces a length-independent live bound, or an energy-compatible expanding family in \(K_n\)
- **Hypotheses:** H1, the telescope plus defect recurrence confines \(L_0\); H2, large-\(\lvert s_3\rvert\) slice ratios name an expanding eigen-direction that \(K_n\) still accepts; H3, a short interior block \(T_B^k(0)\) stays in \(K\) with \(\lvert s\rvert\to\infty\)
- **Major results:** Lean `Ostrowski.NP.energy_telescope` (ledger `OST-np-energy-telescope`), novelty KNOWN, zero `sorry`; origin interpretation \(E_i=-\sum\) consumed, acceptance \(\sum w_j q_j=0\); defect step \(D_{n-1}^+(T_w s)=D_n^+(s)+(w^{\max}_{n-1}-w)q_{n-1}\) restates \(K_n\) (normalized, not coordinate-bounded); ratio bounds \(-4<\mathrm{lo}/q_n\le\mathrm{hi}/q_n<2\) for \(n\ge 2\); remaining-1 form \(s_2+2s_3\in[-2,1]\) on \(\lvert L_1\rvert=958\) from start \(20\) (length-dependent); slice argmax \(\lvert s_3\rvert\) at remaining \(1,2,3\) are \((-3,-37,19)\), \((21,22,-15)\), \((9,27,-12)\), ratios \(O(1)\) off the \(A\)-eigen ray; only zero blocks of length \(\le 3\) stay in \(K\) over four repeats; expanding \(w\equiv-4\) leaves \(K_n\). `kernel_unreachable_of_not_exceptional` and `energy_step` unchanged
- **Refuted ideas:** that the defect is a live-set theorem; that remaining-1 \(s_2+2s_3\in[-2,1]\) is a global \(L_0\) bound; that large-\(\lvert s_3\rvert\) ratios stabilize to an expanding family; that a short interior repeating block is energy-compatible and unbounded
- **Literature:** FS1996 unchanged. The telescope is the residual construction, not that paper
- **Open:** \(\lvert L_0\rvert\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN telescope only. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Live control language of Γ_NP (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether an expanding residual can be sustained on co-live control prefixes of unbounded length
- **Hypotheses:** H1, a forbidden short factor cuts off long live trajectories; H2, an occurring block of length \(4\)–\(6\) stays co-live under repetition with \(\lvert s\rvert\to\infty\); H3, extension types collapse to a finite control automaton that bounds \(s\)
- **Major results:** origin-reachable live DAG with all edges, co-live = can reach remaining \(0\); at \(N=8,12,16,20\) live nodes equal co-live nodes; \(\lvert\mathcal L_k(12)\rvert\) frozen; \(\lvert\mathcal L_6(20)\rvert=361\), \(729\) remaining-\(0\) states, \(38625503\) accepting words of length \(20\); exactly \(22\) Ext sets, all consecutive windows in \(W\) of length \(\le 4\), stable \(N=8\to 20\); all \(49+343\) interior factors of length \(2,3\) occur at \(N=12\); every length-\(\le 6\) co-live prefix of \(N=20\) is co-live at \(N=16\); two length-\(6\) words fail at \(N=12\); \(14\) occurring \(k=4,5,6\) blocks stay live for three repeats from remaining \(18\) and all return to \(0\); expanding occurring blocks leave \(K\); Perron pairing grows as remaining drops (floats). No new Lean. `energy_telescope` / `energy_step` / `kernel_unreachable_of_not_exceptional` unchanged
- **Refuted ideas:** that a length-\(2\) or \(3\) interior factor is forbidden at these horizons; that occurring length-\(4\)–\(6\) prefixes yield a co-live expanding family; that finite-horizon co-liveness of a prefix is \(\lvert H(u)\rvert=\infty\); that \(22\) Ext windows bound \(\lvert s\rvert\)
- **Literature:** FS1996 unchanged
- **Open:** \(\lvert L_0\rvert\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). Census and Ext observation only. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, Walnut, or Lean

## Live Ext from energy_step (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Derive \(\operatorname{Ext}(s,n)\) from future feasibility; prove or refute interval structure and whether endpoints bound a residual functional
- **Hypotheses:** H1, \(V_n=[\mathrm{lo},\mathrm{hi}]\); H2, live Ext is \(\mathrm{lo}(n-1)\le E_n-w q_{n-1}\le\mathrm{hi}(n-1)\); H3, real width \(<4\); H4, \(u=s_2+2s_3\) is bounded on live states
- **Major results:** \(V_n\) fills for \(n\le 12\); live Ext matches `is_terminal(T_w s,n-1)`; Lean `energy_control_interval` (ledger `OST-np-energy-ext-interval`), novelty KNOWN, zero `sorry`; width \((6S_{n-2}-3)/q_{n-1}<4\) for remaining \(1..24\) (max \(\approx 3.414\)); \(22\) windows = consecutive subsets of \(W\) of size \(\le 4\) except \((-3,)\), plus empty; no singleton \((-3,)\) on origin-reachable \(N=12\) or boxed \(K_4\); boxed co-live Ext = live Ext (no holes); \(u\) and \(\lvert s_3\rvert\) grow on some windows. `energy_step` / `energy_telescope` / kernel theorem unchanged
- **Refuted ideas:** that window endpoints bound \(\lvert s\rvert\) or \(\lvert u\rvert\) at remaining \(>1\); that \(u=s_2+2s_3\) is the general Ext coordinate (it is \(E_1\)); that crude \(S_k\le 2q_k\) yields width \(<4\) (only \(<6\))
- **Literature:** FS1996 unchanged
- **Open:** \(\lvert L_0\rvert\); exact induction for width \(<4\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN live-Ext interval only. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Complementary coordinates in ker(E_n) (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** After eliminating \(E_n\), decide whether origin-live residuals can grow in \(\ker(u_n)\)
- **Hypotheses:** H1, neighboring energies \((E_n,E_{n-1},E_{n-2})\) invert \(s\); H2, homogeneous \(A^k\) is energy-neutral; H3, \(\lvert s_{\mathrm{orth}}\rvert\) is bounded on origin-live slices; H4, a short kernel-targeted block is a symbolic family
- **Major results:** \(\det(u_n,u_{n-1},u_{n-2})=3^{n-2}\) for \(n\ge 2\) (Lean `adjointDet_eq`, ledger `OST-np-adjoint-window-det`); inversion over \(\mathbb Q\); Lean `energy_homogeneous` (ledger `OST-np-energy-homogeneous`), both novelty KNOWN, zero `sorry`; Euclidean \(\lvert s_{\mathrm{orth}}\rvert\) tracks \(\lVert s\rVert_\infty\) on origin-live slices and grows \(N=12\to 16\) at remaining \(4\) (\(15\to 24\)); within-energy \(\lVert s\rVert_\infty\) also grows; local expanders from \((6,2,-3)\) at remaining \(8\), five \(2\)-repeats live at that horizon, no symbolic family. `energy_step` / `energy_telescope` / `energy_control_interval` / kernel theorem unchanged
- **Refuted ideas:** that a complementary pair \((E_{n-1},E_{n-2})\) is bounded on origin-live states; that \(\lvert s_{\mathrm{orth}}\rvert\le C\) at these horizons; that expanding \(A^k\) on \(\ker(u_n)\) itself exceeds the energy slab (homogeneous motion is energy-neutral); that a \(2\)-repeat at one horizon is \(\lvert L_0\rvert=\infty\)
- **Literature:** FS1996 unchanged
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN inversion and homogeneous identities only. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Live control of the unstable convolution (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether a \(W\)-valued word can keep the origin particular \(s_k=-\sum A^{k-1-j}e_3 w_j\) live for arbitrarily large \(k\) with \(\lvert s_k\rvert\to\infty\)
- **Hypotheses:** H1, the integer convolution matches `apply_word`; H2, companion \(z\) stays in \(\mathbb Z[\lambda]/(p)\) with \(z'=\lambda z-\lambda^2 w\); H3, unnormalized \(\lvert z_j\rvert\le C\) on origin-live remaining \(0\); H4, maximizer words at \(N=12,16\) are a symbolic family
- **Major results:** Lean `Ostrowski.NP.origin_particular` (ledger `OST-np-origin-particular`), novelty KNOWN, zero `sorry`; convolution equals `apply_word`; energy of the particular is `-consumed_sum`; all three \(\lvert\lambda_j\rvert>1\); remaining-0 live \(\lvert L_0\rvert=165\to 379\), \(\lVert s\rVert_\infty=27\to 37\), Perron \(\lvert z\rvert\approx 79\to 114\) from start remaining \(12\to 16\); maximizers share a \((2,-4,-4,\ldots)\) prefix and are not constant, not a family. `kernel_unreachable_of_not_exceptional` / `energy_step` / `energy_telescope` / `energy_control_interval` / `adjointDet_eq` / `energy_homogeneous` unchanged
- **Refuted ideas:** that a uniform unnormalized \(\lvert z_j\rvert\le C\) on origin-live remaining \(0\) bounds \(L_0\); that normalized \(\lvert\lambda\rvert^{-k}\lvert z\rvert\) bounded is residual boundedness; that finite-horizon maximizers are \(\lvert L_0\rvert=\infty\)
- **Literature:** FS1996 unchanged. The convolution is variation of constants for \(T_w\), not that paper
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN convolution only. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Impulse equals place value (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether \(A^r e_3\) is the place-value triple, so `origin_particular` is the Ostrowski convolution of \(w\) against \(q\)
- **Hypotheses:** H1, \(h_r=(3q_{r-1},3q_{r-2}+q_{r-1},q_r)\); H2, both convolution orientations match `apply_word`; H3, coordinates obey an order-3 recurrence with local forcing; H4, \(\lvert s\rvert>C\) forces unique Ext
- **Major results:** Lean `Ostrowski.NP.iterateA_e3` (ledger `OST-np-impulse-place`), novelty KNOWN, zero `sorry`; \(h_0=(0,0,1)\), \(h_1=(3,1,2)\), \(h_2=(6,5,5)\); \(s_k^{(3)}=-\sum q_r w_{k-1-r}\), \(s_k^{(1)}=-3\sum q_{r-1}w_{k-1-r}\); forcing \(F=(-3w_{k+1},-3w_k-w_{k+1},-w_{k+2})\). `origin_particular` / `energy_telescope` / `energy_control_interval` / kernel theorem unchanged
- **Refuted ideas:** that large \(\lvert s\rvert\) forces unique Ext (witness remaining \(5\), \((12,-2,-1)\), Ext \((-1,0,1)\)); that the place-value dictionary is an \(L_0\) bound
- **Literature:** FS1996 unchanged. The impulse is the companion of \(q\), not that paper
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN impulse-place dictionary only. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Recurrence as a zero-sum block (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether the place-value recurrence admits a \(W\)-valued consecutive zero-sum block that is fully live, not a reset, and expanding under iteration
- **Hypotheses:** H1, MSD \(\mathrm{val}=\texttt{consumed_sum}=-s_3\); H2, \(B_\ast=(1,-2,-1,-3)\) has \(\mathrm{val}=0\); H3, a short shift-combination is a non-reset live expander; H4, algebraic zero-sum is fully live
- **Major results:** Lean `Ostrowski.NP.recurrence_word_zero` (ledger `OST-np-recurrence-word-zero`), novelty KNOWN, zero `sorry`; \(B_\ast\) last letter \(-3\notin\) LSD; \(T_{B_\ast}(0)=0\); \(11\) length-\(\le 6\) \(W\)-valued combos, all algebraic zero-sum resets; four LSD-legal complete resets; no expander. `iterateA_e3` / `origin_particular` / `energy_telescope` unchanged
- **Refuted ideas:** that the recurrence word is an expanding live family; that algebraic zero-sum is fully live (LSD); that a reset block is \(\lvert L_0\rvert=\infty\)
- **Literature:** FS1996 unchanged. The identity is \(q_{\mathrm{rec}}\), not that paper
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN \(\mathrm{val}(B_\ast)=0\) lemma only. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Zero-value is not a reset (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether \(\mathrm{val}(B)=0\) is equivalent to \((c_B)_3=0\), and whether that forces \(c_B=0\)
- **Hypotheses:** H1, \((c_B)_3=-\mathrm{val}\); H2, identically zero-for-all-alignments is the recurrence reset lattice; H3, zero at one alignment forces a reset; H4, the shortest complete non-reset is new
- **Major results:** Lean `Ostrowski.NP.particular_s3` (ledger `OST-np-particular-s3`), novelty KNOWN, zero `sorry`; \(\mathrm{val}=0\) iff \(c_B\in F\); shortest complete non-reset is \((1,-2)\) with \(c_B=(-3,-1,0)\) (known hub), algebraic zero-sum / LSD-legal / fully live; complete \(k\le 4\) table has \(k^\ast=2\); recurrence \(11\) remain resets; \(L_0(12)\) is the live fiber on \(F\), not a new census. `recurrence_word_zero` / `iterateA_e3` / `origin_particular` / `energy_telescope` unchanged
- **Refuted ideas:** that \(\mathrm{val}(B)=0\Rightarrow c_B=0\); that a non-reset complete word is \(\lvert L_0\rvert=\infty\); that repeating the length-2 return is a new family (it is the bounded \(F\to F\) ray)
- **Literature:** FS1996 unchanged. The identity is energy at remaining \(0\), not that paper
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN \(c_3=-\mathrm{val}\) dictionary only. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Complete zero-value is not a monoid (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether \(\mathrm{val}(U)=\mathrm{val}(V)=0\) implies \(\mathrm{val}(UV)=0\), and record the exact composition law on \(F\)
- **Hypotheses:** H1, MSD `consumedSum` splits at two starts; H2, complete-word zero-value is a monoid; H3, \(\mathrm{val}(UV)=\mathrm{val}(V)-E_{\lvert V\rvert}(c_U)\); H4, live complete zeros are a new fiber
- **Major results:** Lean `Ostrowski.NP.consumedSum_append` (ledger `OST-np-consumed-sum-append`) and `val_concat_energy` (ledger `OST-np-val-concat-energy`), novelty KNOWN, zero `sorry`; \(\mathrm{val}(UV)=0\) iff \(E_{\lvert V\rvert}(c_U)=\mathrm{val}(V)\); hub square \((1,-2)(1,-2)\) has \(\mathrm{val}=5\), \(c_B=(-6,-2,-5)\); reset then hub stays zero-value; live complete remaining \(0\) is \(L_0(N)\), maximizer \((-27,-6,0)\) off the two-step ray. `particular_s3` / `particular_concat` / `foldSteps_affine` / `two_step_on_F` unchanged
- **Refuted ideas:** that complete zero-value words form a monoid (ledger `OST-np-complete-zero-monoid`); that a concatenation semigroup of complete zeros is the object of study; that \(C_N^{\mathrm{live}}\) is distinct from \(L_0(N)\)
- **Literature:** FS1996 unchanged. The split is two consumed-sum windows, not ordinary positional scaling
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN concatenation dictionary. REFUTED complete-Z monoid. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## State-dependent block value is -s3 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether \(\mathrm{Val}_s(B)=\mathrm{val}(B)-E_{\lvert B\rvert}(s)\) is a new composition law or `energy_telescope` at remaining 0
- **Hypotheses:** H1, \((T_B(s))_3=E_k(s)-\mathrm{val}(B)\) off the origin; H2, \(T_B(s)=A^k s+c_B\) already; H3, hub iterates from hub/N12 grow an unbounded live family; H4, \(\mathrm{Val}_s\) is a new transducer
- **Major results:** Lean `Ostrowski.NP.fold_s3` (ledger `OST-np-fold-s3`), novelty KNOWN, zero `sorry`; \(T_B(s)\in F\) iff \(E_k(s)=\mathrm{val}(B)\); Python `block_val` matches `-s_3` and `affine_holds` at origin, hub, and the \(N=12\) maximizer; hub word from origin is the ray, from hub leaves \(F\); legal two-step from hub stays on \((3k,k,0)\) with \(k\in\{0,1,2\}\). `energy_telescope` / `foldSteps_affine` / `val_concat_energy` unchanged
- **Refuted ideas:** that \(\mathrm{Val}_s\) is a new block-transducer calculus; that repeating the hub word from the hub is a live family; that legal two-step images from the hub escape the bounded ray
- **Literature:** FS1996 unchanged. The identity is energy at remaining 0, not that paper
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN `fold_s3` dictionary only. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Spectral cancellation is already parked (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether bounded \(W\) can keep all expanding modes bounded on infinite live trajectories, or whether a recurrent symbolic family has \(\lvert s\rvert\to\infty\)
- **Hypotheses:** H1, uniform unnormalized \(\lvert z_j\rvert\le C\) on origin-live remaining \(0\); H2, companion \(V_\lambda\) is a new eigenfunctional; H3, finite-horizon maximizers are a symbolic family; H4, extending remaining-0 BFS past \(N=16\) decides \(\lvert L_0\rvert\)
- **Major results:** ledger `OST-np-unnormalized-mode-bound` `REFUTED` (existing `compare_remaining_zero`: \(\lvert L_0\rvert=165\to 379\), Perron \(\lvert z\rvert\approx 79\to 114\), \(\lVert s\rVert_\infty=27\to 37\)); companion \(z'=\lambda z-\lambda^2 w\) is `step` in companion coordinates (`z_of_state` is the identity); N=12 maximizer is not a family; Ext at \((12,-2,-1)\) remaining 5 is not unique. No new modules. `fold_s3` / `origin_particular` / `iterateA_e3` unchanged
- **Refuted ideas:** that infinite liveness forces expanding modes bounded (finite remaining-0 slices already grow); that \(V_\lambda\) is new mathematics; that maximizer words are \(\lvert L_0\rvert=\infty\)
- **Literature:** FS1996 unchanged. The convolution is variation of constants, not that paper
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). REFUTED uniform unnormalized-mode bound. CLOSE companion/\(V_\lambda\) as reparameterization of `step`. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Arbitrarily long accepted words need not have infinitely many terminals (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether arbitrarily long origin-accepted words force infinitely many distinct remaining-0 terminals
- **Hypotheses:** H1, \(U_k=(B_\ast)^k\cdot(1,-2)\) is complete live with \(\tau=\) hub; H2, that implication holds for the full language; H3, König of \(\mathcal T_\infty\) decides \(\lvert L_0\rvert\); H4, a seven-module extendability stack is required
- **Major results:** Lean `Ostrowski.NP.recurrence_word_reset` / `reset_pow_origin` / `reset_pow_then_hub` (ledger `OST-np-reset-pow-then-hub`), novelty KNOWN, zero `sorry`; Python `U_k` fully live for \(k=0..4\), one terminal the hub; König of \((B_\ast)^\infty\) stays at the origin. No new modules. `fold_s3` / `hub_nonreset` / `recurrence_word_zero` unchanged
- **Refuted ideas:** that arbitrarily long accepted words force infinitely many terminals (ledger `OST-np-long-words-infinite-L0`); that König compactness is an \(L_0\) theorem; that finite-horizon \(\lvert L_0(N)\rvert\) growth is infinitude
- **Literature:** FS1996 unchanged. The family is the recurrence reset plus the known hub word, not that paper
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN `reset_pow_then_hub` identity. REFUTED long-words\(\Rightarrow\lvert L_0\rvert=\infty\). CLOSE König/\(\mathcal T_\infty\) as new math. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Observed remaining-0 terminals span 3Z×Z (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether origin-reachable terminals in \(F\) satisfy an extra lattice/congruence beyond \(3\mid a\), or whether the reverse formula is new mathematics
- **Hypotheses:** H1, integer reverse on \(F\) is new; H2, a second modulus (\(9\mid a\) or \(\gcd b>1\)) holds on \(L_0(N)\); H3, \(L_0(16)\subseteq L_0(12)\); H4, a seven-module reverse/pump stack is required
- **Major results:** Lean `Ostrowski.NP.unique_predecessor` / `predecessor_on_F` (ledger `OST-np-unique-predecessor`), novelty KNOWN, zero `sorry`; Python `terminal_span_report` at \(12\to 16\): \(\lvert L_0\rvert=165\to 379\), \(\gcd a=3\), \(\gcd b=1\), maximizer \((-27,-6,0)\) off the ray, all small \(\alpha a+\beta b\) grow. No new modules
- **Refuted ideas:** extra terminal congruence beyond \(3\mid a\) at these horizons (ledger `OST-np-extra-terminal-congruence`); that the \(F\)-predecessor is a new reverse calculus; that new remaining-0 states are \(\lvert L_0\rvert=\infty\)
- **Literature:** FS1996 unchanged. The reverse is inversion of \(T_w\), not that paper
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). CLOSE reverse-as-new-math. REFUTED extra congruence at recorded horizons. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Origin resets do not create new terminals (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Quotient origin-reset prefixes and decide whether primitive terminal endpoints are a new set or still \(L_0\)
- **Hypotheses:** H1, \(T_R(0)=0\) implies \(T_{RU}(0)=T_U(0)\); H2, \(P=L_0\) is a new census; H3, unbounded \(H(t)\) is primitive growth; H4, a primitive-DP / pump stack is required
- **Major results:** Lean `Ostrowski.NP.reset_prefix` (ledger `OST-np-reset-prefix`), novelty KNOWN, zero `sorry`; Python `reset_prefix_holds` on \(B_\ast\) then hub; hub \(\ell_{\min}=2\); \(C(N)\) grows through remaining \(8\). No new modules. `particular_concat` / `reset_pow_then_hub` unchanged except `reset_pow_then_hub` now uses `reset_prefix`
- **Refuted ideas:** that reset-padded length is a new terminal; that origin-primitive image \(P\) is distinct from \(L_0\); that finite-horizon \(C(N)\) is \(\lvert L_0\rvert=\infty\)
- **Literature:** FS1996 unchanged. The identity is affine composition at the origin, not that paper
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN `reset_prefix`. CLOSE \(P=L_0\) as tautology. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Suffix futures are classified by energy (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether complete-suffix acceptance at remaining \(n\) is a new Myhill–Nerode invariant, or is classified by \(E_n(s)\)
- **Hypotheses:** H1, equal \(E_{\lvert v\rvert}\) implies the same landing on \(F\); H2, claims A \(\lvert L_0\rvert=\infty\), B nonregular 3-input relation, and C this residual construction coincide; H3, a Hankel / digit-triple / triangular family is required; H4, finite future quotient implies finite \(\lvert L_0\rvert\)
- **Major results:** Lean `Ostrowski.NP.same_energy_same_OnF` (ledger `OST-np-same-energy-same-OnF`), novelty KNOWN, zero `sorry`; Python `same_energy_same_onf` on origin and \((0,-2,1)\); LSD \(0\) separates origin from hub; co-live states at remaining \(4\) in `dag_at(8)` exceed Ext types. No new modules. `fold_on_F_iff` / `energy_step` / `foldSteps_append` unchanged
- **Refuted ideas:** that suffix futures at remaining \(n\) distinguish kernel coordinates of \(s\); that Myhill–Nerode / Hankel is a new attack on \(\lvert L_0\rvert\); that A, B, and C are the same claim
- **Literature:** FS1996 unchanged. 3-input adder for one non-quadratic \(\alpha\) remains KNOWN negative. The identity is `fold_on_F_iff`, not that paper
- **Open:** \(\lvert L_0\rvert\); a contracting functional on \(\ker(u_n)\). Not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). PROMOTE the KNOWN `same_energy_same_OnF`. CLOSE MN/Hankel/digit-triple stack. Do not claim \(\lvert L_0\rvert\) finite or infinite. No order 4, CLI, or Walnut

## Ostrowski research-engine extraction R1–R2 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Freeze the Ostrowski Python/Lean baseline and extract only the demonstrated exact affine, block, phase, and trajectory primitives into a reusable engine, without changing any claim about \(\lvert L_0\rvert\)
- **Hypotheses:** H1, `transition_affine` / `apply_word` / `affine_block` already expose a problem-independent integer affine core; H2, a generic API can avoid Ostrowski recurrence, energy, and remaining-length semantics
- **Major results:** R1 baseline at git `0952da60`, ledger sha256 `7643b707…f3191`, 21 Ostrowski rows unchanged (17 Lean-verified, 4 REFUTED); `research_engine` provides `ProblemSpec`, `AffineSystem`, `BlockAction`, `Trajectory` / `LazyTrajectory`; composition law is \(T_{UV}=T_V\circ T_U\), not naive translation sum (hub word \((1,-2)\) is the witness); Ostrowski helpers delegate and keep public signatures; a one-dimensional shift spec has a strictly smaller terminal alphabet. `lake build Problems.Ostrowski.NP` green, zero `sorry`. No ledger retag
- **Refuted ideas:** none mathematical. Naive concatenation of block translations is not the affine composition law (already REFUTED as `OST-np-complete-zero-monoid`; now a generic regression)
- **Literature:** unchanged. This is infrastructure, not a numeration-system theorem
- **Open:** \(\lvert L_0\rvert\) remains PARK and was not investigated. R3 reachability/acceptance extraction is not taken up here
- **Decision:** PROMOTE the R2 `research_engine` core. PARK \(\lvert L_0\rvert\). Do not start R3, attacks, planner, CLI, or a second real problem in this cycle

## Ostrowski research-engine extraction R3 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Extract forward/reverse/live/suffix search behind `ProblemSpec` without leaking Ostrowski energy or remaining-length into `research_engine`, and without touching \(\lvert L_0\rvert\)
- **Hypotheses:** H1, Ostrowski BFS, reverse basin, and Ext-oracle are already spec-driven; H2, typed claim kinds can block the Phase-0 logical jumps (`K` unbounded \(\Rightarrow L\) infinite, union \(\Rightarrow L_n\), \(C(\{0\})\Rightarrow L\))
- **Major results:** `research_engine` now has `forward_search`, `reverse_closure`, `LIVE_SLICE` vs `LIVE` vs `CO_REACHABLE`, and `live_extensions`; every forward result is `BOUNDED`; `C({0})` remains `EXACT` co-reachability of a seed, not the adder live set; `OstrowskiSpec` is a thin adapter; `reachable_live` / `forward_layers` / `live_ext_by_oracle` / `basin_of_zero` delegate. Ledger unchanged. `lake build Problems.Ostrowski.NP` green
- **Refuted ideas:** none new. The engine encodes the existing refutations as distinct claim kinds rather than as new mathematics
- **Literature:** unchanged. Infrastructure only
- **Open:** \(\lvert L_0\rvert\) remains PARK. R4 algebra adapters, attacks, planner, CLI not taken up
- **Decision:** PROMOTE the R3 reachability/acceptance core. PARK \(\lvert L_0\rvert\). Do not start R4 in this cycle

## Ostrowski research-engine extraction R4 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Extract integer recurrences, lattice inverses, and linear forms into `research_engine.algebra` without encoding Ostrowski place values, energy, or \(B^*\)
- **Hypotheses:** H1, the companion of \(q_n=d_1 q_{n-1}+\cdots+d_m q_{n-m}\) already is the residual unread-tail matrix; H2, \(As+b=t\) over \(\mathbb Q\) with a lattice check is the reverse map; H3, \(uA\) is a generic left multiply, not an energy identity
- **Major results:** `RecurrenceSpec`, `integer_affine_preimage`, Faddeev–LeVerrier `characteristic_polynomial`, and `LinearFunctional` (`observed_bound` is a sample max, not an invariant). Fibonacci \((1,1)\) and doubling \((2)\) run on the same API. Ostrowski `integer_preimage` / `np_inverse_matrix` / `charpoly_of_matrix` / `mat_vec_left` / `triple_det` / `invert_from_energies` / `gcd_adjoint` wrap the engine. NP companion charpoly remains \((1,-2,-1,-3)\). Ledger unchanged. Fast and `--runslow` pytest green. `lake build Problems.Ostrowski.NP` green
- **Refuted ideas:** none new. A finite observed bound on \(\lvert \ell(s)\rvert\) is not a contraction on \(\ker(u_n)\)
- **Literature:** unchanged. Infrastructure only
- **Open:** \(\lvert L_0\rvert\) remains PARK. R5 attacks, planner, CLI not taken up
- **Decision:** PROMOTE the R4 algebra adapters. PARK \(\lvert L_0\rvert\). Do not start R5 in this cycle

## Ostrowski research-engine extraction R5 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Extract six typed attacks (recon, modular, affine-region, reverse, functional, block) that cannot promote a finite census or a sample max \(\lvert\ell\rvert\) to live infinitude
- **Hypotheses:** H1, `gcd` of an affine row already is the NP `s_1\equiv 0\pmod 3` law; H2, `T_B` classification needs no spectral radius; H3, `C(seed)` and `LIVE_SLICE` stay distinct claim kinds
- **Major results:** `AttackResult` carries `AttackStatus` + `ClaimKind` + `SearchScope`. Recon is always `OBSERVATION`/`BOUNDED`. Modular forcing of image coordinates is `SUPPORTED`/`EXACT` as a map law. Functional sample max is never `SUPPORTED`. Hub word `(1,-2)` is `AFFINE` with translation `(-3,-1,0)`, not an origin reset. Ledger unchanged. Fast and `--runslow` pytest green. `lake build Problems.Ostrowski.NP` green
- **Refuted ideas:** none new. A one-step leak-free region is not an invariant theorem; a bounded reverse basin is not \(L_0\)
- **Literature:** unchanged. Infrastructure only
- **Open:** \(\lvert L_0\rvert\) remains PARK. R6 planner, spectral attacks, CLI not taken up
- **Decision:** PROMOTE the R5 attack adapters. PARK \(\lvert L_0\rvert\). Do not start R6 in this cycle

## Ostrowski research-engine extraction R6 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Add hypotheses, negative knowledge, and a deterministic planner that cannot promote `TERMINAL`/`LIVE_SLICE`/`CO_REACHABLE` evidence to exact `LIVE` infinitude, without migrating `theorem_ledger.json`
- **Hypotheses:** H1, Phase-0 refutations are claim-kind non-implications; H2, a fixed cheap-attack order is enough; H3, parking \(\lvert L_0\rvert\) is a ledger decision, not a missing attack
- **Major results:** `Hypothesis` + `NegativeKnowledge` + `AttackPlanner`. `promote_if_legal` raises `LedgerError` on kind/scope mismatch. Generic schemas block `terminal_unbounded ⇒ live_unbounded` and `C(seed) ⇒ LIVE`. Ostrowski seeds `ostrowski_L0_infinite` as `PARKED` and restates existing REFUTED rows as instance schemas. Spectral/symbolic deferred. Named theorem ledger unchanged. Fast and `--runslow` pytest green. `lake build Problems.Ostrowski.NP` green
- **Refuted ideas:** none new. Bounded recon cannot `PROMOTE` \(\lvert L_0\rvert=\infty\)
- **Literature:** unchanged. Infrastructure only
- **Open:** \(\lvert L_0\rvert\) remains PARK. R7 adapter rewrite, spectral attacks, CLI not taken up
- **Decision:** PROMOTE the R6 planner/negative-knowledge core. PARK \(\lvert L_0\rvert\). Do not start R7 in this cycle

## Ostrowski research-engine extraction R7 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Make Ostrowski depend on the engine through one adapter facade (`q`, energy, digits, affine, recurrence) without moving the package or putting energy in `research_engine`
- **Hypotheses:** H1, `OstrowskiSpec` already is the `ProblemSpec`; H2, `energy_canonical` is `residual_integer`; H3, attacks/planner can take `spec.attack_context()` without new mathematics
- **Major results:** `OstrowskiSpec.q` / `energy` / `digit_realization` / `affine_system` / `recurrence` / `attack_context`. `research.ostrowski.adapter` is the facade. `energy_canonical` delegates to `residual_integer`. Attacks and `plan_np` go through the spec. Package stays `research.ostrowski`. Ledger unchanged. \(\lvert L_0\rvert\) remains PARKED. Fast and `--runslow` pytest green. `lake build Problems.Ostrowski.NP` green
- **Refuted ideas:** none new. A second `problems/ostrowski_np` tree was not created
- **Literature:** unchanged. Infrastructure only
- **Open:** \(\lvert L_0\rvert\) remains PARK. R8 synthetic benchmarks, spectral attacks, CLI not taken up
- **Decision:** PROMOTE the R7 Ostrowski adapter facade. PARK \(\lvert L_0\rvert\). Do not start R8 in this cycle

## Ostrowski research-engine extraction R8 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Add five tiny systems with known behavior and run the cheap-attack planner on all of them, fixing abstraction leaks, without touching \(\lvert L_0\rvert\)
- **Hypotheses:** H1, a collapse to 0 is a finite live closure; H2, \(x\mapsto x+1\) is an infinite live family that remains a `BOUNDED` census; H3, a reset loop has infinitely many words and one terminal; H4, \(x\mapsto 3x\) is an exact residue law; H5, \(x\mapsto 2x\) can expand out of a live box
- **Major results:** `research_engine.benchmarks` A–E. Planner default `max_steps=16`. Forward search reports actual depth, not the cap. New schema `unbounded_accepted_words ⇒ unbounded_terminals` REFUTED as kinds. None of the five emits a `LIVE` claim. Ostrowski \(\lvert L_0\rvert\) stays PARKED. Named theorem ledger unchanged. Fast and `--runslow` pytest green. `lake build Problems.Ostrowski.NP` green
- **Refuted ideas:** none new Ostrowski mathematics. The reset-loop toy is the Phase-0 word/terminal trap, not a new counterexample to \(\Gamma_{NP}\)
- **Literature:** unchanged. Infrastructure only
- **Open:** \(\lvert L_0\rvert\) remains PARK. R9 Lean export, spectral attacks, CLI not taken up
- **Decision:** PROMOTE the R8 synthetic benchmarks. PARK \(\lvert L_0\rvert\). Do not start R9 in this cycle

## Ostrowski research-engine extraction R9 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Emit minimal Lean theorem targets from exact certificates without auto-prove, without `sorry`, and without writing new `formal/` files or retagging \(\lvert L_0\rvert\)
- **Hypotheses:** H1, `SUPPORTED`+`EXACT` non-`LIVE` certificates are the only exportable targets; H2, the NP modular gcd-3 law already is Lean `step_fst_dvd_three`; H3, the hub block translation `(-3,-1,0)` already is Lean `hub_nonreset`
- **Major results:** `research_engine.verification.TheoremTarget` plus comment/YAML renderers. Bounded recon and `LIVE` claims are not exportable. Ostrowski `export_plan_targets` links modular/hub certificates to existing NP lemmas. PARKED `ostrowski_L0_infinite` is not a target. Named theorem ledger unchanged. No new Lean modules. Fast and `--runslow` pytest green. `lake build Problems.Ostrowski.NP` green
- **Refuted ideas:** none new. An exact map-law certificate is not live infinitude, and a skeleton is not a proof
- **Literature:** unchanged. Infrastructure only
- **Open:** \(\lvert L_0\rvert\) remains PARK. R10 research CLI, spectral attacks, auto-prove not taken up
- **Decision:** PROMOTE the R9 theorem-target export. PARK \(\lvert L_0\rvert\). Do not start R10 in this cycle

## Ostrowski research-engine extraction R10 (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Expose the stable engine API as `btlab research analyze|attack|reproduce|report` without a second CLI, without auto-prove, and without retagging \(\lvert L_0\rvert\)
- **Hypotheses:** H1, planner text is enough for analyze/reproduce; H2, exportable targets are enough for report; H3, a named-attack runner does not need spectral/symbolic yet
- **Major results:** `research_engine.report` plus `cli.research`. Ostrowski reproduce requires PARKED `ostrowski_L0_infinite` and Lean links `step_fst_dvd_three` / `hub_nonreset`. Benchmark B stays `BOUNDED` `LIVE_SLICE`. Deferred attacks exit 2. Named theorem ledger unchanged. No new Lean modules. Fast and `--runslow` pytest green. `lake build Problems.Ostrowski.NP` green
- **Refuted ideas:** none new. A CLI printout is not a live-set theorem
- **Literature:** unchanged. Infrastructure only
- **Open:** \(\lvert L_0\rvert\) remains PARK. Spectral attacks and auto-prove not taken up
- **Decision:** PROMOTE the R10 research CLI. PARK \(\lvert L_0\rvert\). The R1–R10 extraction is complete; do not start spectral/auto-prove in this cycle

## Ostrowski research-engine spectral plug-in (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Classify the companion of \(A\) by an integer cubic Pisot/Perron certificate without promoting expansion to live infinitude, and without symbolic-family search
- **Hypotheses:** H1, the existing integer cubic certificate already is the exact companion law; H2, float roots are labels only; H3, expanding modes do not imply \(\lvert L_0\rvert=\infty\)
- **Major results:** `research_engine.algebra.spectral` plus `SpectralClassificationAttack`. NP companion is exact Perron-non-Pisot (`SUPPORTED`/`EXACT`/`REACHABLE`). Benchmark D (1×1 tripling) is not a cubic certificate and does not emit `LIVE`. Generic schema `expanding_modes_unbounded ⇒ live_unbounded`. Symbolic stays deferred. Named theorem ledger unchanged. No new Lean modules. Fast and `--runslow` pytest green. `lake build Problems.Ostrowski.NP` green
- **Refuted ideas:** none new. Expansion is not live infinitude (already `OST-np-unnormalized-mode-bound`)
- **Literature:** unchanged. Infrastructure only
- **Open:** \(\lvert L_0\rvert\) remains PARK. Symbolic-family search and auto-prove not taken up
- **Decision:** PROMOTE the spectral plug-in. PARK \(\lvert L_0\rvert\). Do not start symbolic search or auto-prove in this cycle

## Ostrowski prefix-family search (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Test whether \(P_m=(2)\cdot(-4)^m\) plus a uniformly bounded tail is an unbounded origin-live remaining-0 family, without a generic engine attack
- **Hypotheses:** H1, N=12/16 maximizers share the prefix \((2,-4,-4,\ldots)\) so a closed tail would be the missing family; H2, live completions reuse only the two-step ray / hub / \(B_*\)-pads; H3, the prefix dies for large \(m\)
- **Major results:** `research.ostrowski.symbolic_family`. Live remaining-0 completions with tail length \(\le 6\) exist for \(m=0,1,2\) (65 other terminals, unstructured tails). For \(m\ge 3\) the prefix dies: \((2,-4,-4,-4)\) lands on \((6,2,2)\), not live. No closed-form tail. Report is `OBSERVATION` / `BOUNDED` / `LIVE_SLICE`, never `LIVE`, never infinitude. `DEFERRED_ATTACKS` stays `("symbolic",)`. Named theorem ledger unchanged. No new Lean modules
- **Refuted ideas:** \(P_m\) plus a uniformly bounded tail as an unbounded origin-live family
- **Literature:** unchanged
- **Open:** \(\lvert L_0\rvert\) remains PARK. A contracting functional on \(\ker(u_n)\) is not taken up
- **Decision:** PARK \(\lvert L_0\rvert\). CLOSE this prefix candidate. Do not open morphisms, Walnut, order 4, or a generic `SymbolicControlAttack`

## Regular-output preimage ledger packaging (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Record the already-promoted \(x^2\) safety-preimage non-regularity theorem in the ledger and the theory reading path. No new mathematics.
- **Hypotheses:** none; this is documentation of an existing proof.
- **Major results:** theory page `docs/theory/regular_output_preimages.md`; ledger row `BTR-x2-safety-nonsific` (**EXACT — HUMAN PROOF**); conjecture `x2_safety_nonsific`. Census bounds and the linear control stay in the dossier only.
- **Refuted ideas:** none new.
- **Literature:** Ahmed–Savchuk, Anashin, and Grigorchuk–Savchuk remain `KNOWN` and are cited on the theory page; the packing witness is PROJECT-SPECIFIC.
- **Open:** none on this branch. Lean remains deferred.
- **Decision:** PROMOTE the packaging. Do not open a numbered milestone. Do not add CLI, Lean, or any other output language. Do not reopen the gate.

## Unrestricted residual complexity C_F(m,r) (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether unrestricted residual complexity C_F(m,r) has an exact two-parameter law for F(x)=x and F(x)=x^2, or a proved obstruction that the census is not a remaining-horizon clock and not a closed low-degree formula.
- **Hypotheses:** for low-degree F, C_F(m,r) might be a closed two-parameter expression or short recurrence, distinct from the safety census and from M_k(x^2).
- **Major results:** C_x(m,r)=1, while the remaining-horizon clock on x grows as k. C_{x^2}(m,r)=3^m for r≥m (same-depth layer injectivity). C_{x^2}(m,m-1)=3^m-3 for m≥2, by exactly three constant-trit doubletons; the balanced expansion of ((3^r-1)/2)^2 has digit r in {0,-1}, so adding 3^r does not carry into DZ^{r+1}. Interior 0<r<m-1 is a table through m,r≤7 (not 3^{min(m,r)}, not min(3^m,3^{2r}), not the safety sequence 1,3,7,16,33,66,131,260). Ledger row `BTR-x2-C-band`. Lean deferred.
- **Refuted ideas:** that C_F is a remaining-horizon clock; that C_F=3^{min(m,r)}; that C_F is the live safety census; that the coefficient cap min(3^m,3^{2r}) is already the exact law.
- **Literature:** Ahmed–Savchuk unrestricted infinite-state remains KNOWN and is not this theorem; M_k(x^2)=(3^k-1)/2 remains the triangle m<k; cubic M_k(x^3) is not reopened.
- **Open:** the interior image size for 0<r<m-1. Section entropy and solenoid packaging stay unopened pending ideas of the safety gate.
- **Decision:** PROMOTE the band law. Do not open a numbered milestone. Do not add CLI or Lean. Do not start an interior follow-up in this phase.

## Unrestricted C_{x^2} interior (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether the OPEN interior of unrestricted C_{x^2}(m,r) saturates at 3^{2r} by an explicit m_0(r), or still requires width-Θ(m-r) enumeration
- **Hypotheses:** the m,r≤7 table suggested saturation at r=1 for m≥3 and r=2 for m≥6; the guess m_0(r)=3r was labelled non-binding
- **Major results:** Zero fibre p≡0 (mod 3^r) at m=2r is exactly the quadratic residues in Z/3^r Z, so C(2r,r)<3^{2r} (cap not attained at extra width r). The same fibre is full for every m≥3r via p=3^r+v 3^{m-r}, giving DZ^m(p^2)≡2v (mod 3^r). Ledger row `BTR-x2-C-interior`. Full C saturates computationally for r≤6 at first times 3,6,8,10,13,15 and stays at the cap; not a proved m_0(r). Exact integer image in `research.residual_complexity.triage`. Lean not opened. Band row `BTR-x2-C-band` unretagged
- **Refuted ideas:** that m_0(r)=3r is the first saturation time (C(8,3)=729 while 3r=9; C(10,4)=6561 while 3r=12); that 2r+1 or 2r+2 is a uniform first time; that a collision family blocks 3^{2r} for all large m in r≤6; that the interior count always needs width-Θ(m-r) enumeration
- **Literature:** Ahmed–Savchuk unrestricted infinite-state remains KNOWN; squares in Z/3^r Z are KNOWN; the zero-fibre identification is PROJECT-SPECIFIC. Cubic M_k(x^3) and the safety gate were not reopened
- **Open:** a proved m_0(r) for every fibre, or a fibre that never fills
- **Decision:** PARK. The zero fibre is a theorem; full interior C is a table plus that fibre, not a saturation law with explicit m_0(r)

## Unrestricted C_{x^2} every interior fibre (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether every fibre p≡α (mod 3^r) of the interior map fills, or exhibit a fibre that never fills
- **Hypotheses:** the two-parameter family (u,v) with p=α+u 3^r+v 3^{m-r} fills every fibre once m≥3r; alternatively some α has a 3-adic square/valuation obstruction that keeps the fibre incomplete for all m
- **Major results:** Every fibre is full for all m≥5r, via p=α+u 3^r+3^{m-r}, giving DZ^m(p^2)≡2u+DZ^r(2α) (mod 3^r). Ledger row `BTR-x2-C-fibre-fill`. The v=1 family is not filling at m=3r or at m=5r-1; vanishing of DZ^{m-r}(q^2) for q∈P_{2r} starts at extra width 4r. Computationally every fibre is already full at m=3r for r≤3 (not a proof). Band and zero-fibre rows unretagged. Lean not opened
- **Refuted ideas:** that some fibre stays incomplete for all m; that a single fixed high trit v=1 fills every fibre at m=3r; that 5r is the first saturation time of C_{x^2}(m,r)
- **Literature:** Ahmed–Savchuk unrestricted infinite-state remains KNOWN; the every-fibre fill at 5r is PROJECT-SPECIFIC. Cubic M_k(x^3) and the safety gate were not reopened
- **Open:** fill at m=3r for a general fibre, or the exact first filling time per fibre; a closed form for C_{x^2}(m,r)
- **Decision:** PROMOTE the every-fibre fill law at m≥5r. Do not open a numbered milestone. Do not add CLI or Lean. Do not start a 3r follow-up in this phase

## Unrestricted C_{x^2} triple-width fibre map (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Sharpen every-fibre fill from m≥5r to m≥3r, or name the exact first filling time per fibre
- **Hypotheses:** the two-parameter family p=α+u 3^r+v 3^{m-r} fills every fibre once m≥3r, even though the v=1 slice fails; alternatively some fibres first fill strictly after 3r with a fibre-dependent exact time
- **Major results:** At m=3r the two-parameter family is the entire fibre. The second coordinate is exactly 2uv+DZ^r(2αv+u^2+DZ^r(2αu+DZ^r(α^2))) (`triple_width_second`). Surjectivity of that map is not proved. A one-parameter slice does not fill a general fibre (r=2: no filling fixed-v slice; only three of nine fibres have a filling fixed-u slice). First-fill is fibre-dependent (r=2: times 5 and 6); no formula in α,r. Extreme fibres α=±(3^r-1)/2 fill by the u=0 slice. Band, zero-fibre, and 5r rows unretagged. No ledger row. Lean not opened
- **Refuted ideas:** that a single-parameter slice (fixed u or fixed v) fills every fibre at m=3r; that every fibre has the same first-filling time 2r+1
- **Literature:** Ahmed–Savchuk unrestricted infinite-state remains KNOWN; the 5r fill remains PROJECT-SPECIFIC and is not restated as this phase's theorem. Cubic M_k(x^3) and the safety gate were not reopened
- **Open:** surjectivity of the triple-width map (fill at m=3r); a first-filling time formula per fibre; a closed form for C_{x^2}(m,r)
- **Decision:** PARK. Neither a 3r fill law nor a first-fill formula was obtained. Do not open a numbered milestone. Do not add CLI or Lean. Do not start a follow-up in this phase

## Operator-dynamics {S,N,D,W} identity gate (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Decide whether the monoid generated by \(\{S,N,D,W\}\) has a composition identity that is not a consequence of the identities already recorded in `docs/operator_algebra.md`
- **Hypotheses:** the recorded list already generates every identity of word length \(\le 4\); alternatively one missing exact relation remains and is PROJECT-SPECIFIC
- **Major results:** a terminating orientation of the recorded list (auxiliary \(K_3=W\circ W\), one-way \(N\)-commutes) has joining critical pairs; 341 words of length \(\le 4\) reduce to 77 normal forms; the rewrite is sound on the probe set; no two distinct normal forms agree as maps on \(\mathbb{Z}\) probes. Already-recorded non-identities stay distinct (\(W\circ W\ne\mathrm{id}\) at \(n=3\); \(W(3n)\ne 3W(n)\) at \(n=1\); \(S\circ D\ne\mathrm{id}\) at \(n=1\); \(D\circ W\ne W\circ D\) at \(n=10\)). The production peak \(N\circ W\circ W\) joins to \(K_3\circ N\) under the recorded commute, which is not installed in `WORD_REWRITE_RULES`. No ledger row. No Lean. No CLI
- **Refuted ideas:** that a new exact identity of length \(\le 4\) remains after the recorded list; re-testing \(W\circ W=\mathrm{id}\), \(W(3n)=3W(n)\), or \(S\circ D=\mathrm{id}\)
- **Literature:** Knuth unique expansion and OEIS A134028 remain KNOWN for the maps. `WORD_SIMP` / `WORD_WN` / `WORD_WND` remain syntactic Newman certificates and were not enlarged. The recorded identities were already project facts
- **Open:** nothing on this line
- **Decision:** CLOSE. The remaining question was taxonomy. Do not enlarge the word bound or the generator set. Do not add production rules. Do not open a numbered milestone

## WORD_SIMP Lean Newman packaging (not a numbered milestone)

- **Date:** 2026-08-24
- **Objective:** Package the already-proved unique-NF claim of `BTC-word-simp-nf` as a sorry-free Lean 4 rewrite-relation proof
- **Hypotheses:** Newman on the sixteen-rule ground string TRS, analogous to `OpFragNewman` but not OpFrag (the fragment includes the W/K3 stock), covers the English unique-syntactic-NF claim without semantic canonicity
- **Major results:** `WordSimp.Letter` / `Rule` / `Step` as substring replacement; lex rank `(I0-count, length)` decreases on every rule; local confluence by disjoint commutation plus the documented overlap table; Newman ⇒ confluence and unique syntactic NF. Ledger `BTC-word-simp-nf` retagged **EXACT — LEAN VERIFIED**. `lake build BTCalculus` is green. Production `WORD_REWRITE_RULES` was not widened. `Confluence.lean` was not edited
- **Refuted ideas:** none. Semantic canonicity was not claimed
- **Literature:** Newman / Knuth–Bendix for string rewriting remains KNOWN. The named SIMP fragment is project-specific packaging of an existing human proof
- **Open:** `WORD_WN` / `WORD_WND` stay human
- **Decision:** PROMOTE the Lean packaging. Do not open a numbered milestone. Do not formalize WN/WND in this phase. Do not add semantic canonicity. Do not reopen word-table enlargement

## Balanced-ternary finite-state dynamics (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Run one exact balanced-ternary digit system through the generic research engine and identify the first finite-state / expanding boundary
- **Hypotheses:** H1, normalizing the doubled trit stream `2 d_i` has residual closure `{-1,0,1}`; H2, the mechanism is radix-3 division plus bounded forcing, witnessed by `V(c)=|c|`; H3, synthetic gain `λ=3` on the same remainder map is unbounded
- **Major results:** `research.balanced_ternary.DoubledTritSpec` delegates to `BoundedNormalizeTransducer(2)`. The step is piecewise balanced division, not one `Ax+b(d)`. Reconnaissance stays `OBSERVATION`/`BOUNDED`. The new generic `ExhaustiveClosureAttack` certifies `R_∞={-1,0,1}` by queue exhaustion. Raw states 3, sign orbits 2, minimal Mealy classes 3. Lean proves closure, Lyapunov, sign symmetry, flush, distinct output signatures, and `c_n=3n` for `λ=3`. `λ=1,2` finite; `λ=3` unbounded. Non-Pisot Ostrowski `L_0` was not reopened
- **Refuted ideas:** global nonincrease of `|c|` on the start layer; one integer-affine model of the balanced-division step
- **Literature:** unique BT expansions and bounded-alphabet transducers remain `KNOWN`. The promoted content is the engine certificate and the gain boundary
- **Open:** residual dynamics of the integer operator `D`
- **Decision:** PROMOTE the doubled-trit adapter, exact closure/Lyapunov theorems, and the `λ=3` counterexample. Do not start the `D`-operator benchmark in this cycle

## Balanced-ternary expanding `T` Phase 1 (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Discover the residual information needed to predict the LSD stream of `T(n)=3n-lsd(n)`, without assuming finite-state integer dynamics
- **Hypotheses:** H1, a bounded digit window or residue of `n` is equivalent to the full integer for future LSDs; H2, `|T(n)|` is a Lyapunov; H3, a small `λ` perturbation destroys observational finiteness
- **Major results:** `T` is the existing section `I_{-lsd(n)}(n)`, not laboratory `D`. Exact identities `lsd(T(n))=-lsd(n)`, `lsd(T^k(n))=(-1)^k lsd(n)`, `DZ(T(n))=n`, `T(I_a(x))=9x+2a`. Question A fails (`|T(n)|>|n|` for `n≠0`). Question B is a 3-state LSD quotient. Bounded reconnaissance (`|n|≤40`, length 12) is `OBSERVATION`; Lean proves the exact orbit law. `n=1` vs `n=4` shows `mod 9` is not necessary. Engine `ExpandingDResidueSpec` certifies residual closure `{-1,0,1}`; integer-state BFS hits the cap. `T_2` preserves LSD; `T_3` sends LSD to `0`. Both keep a 3-state observational residual. Non-Pisot Ostrowski `L_0` was not reopened
- **Refuted ideas:** magnitude contraction of `T`; `n mod 9` as a necessary LSD residual; observational infinitude of `T_λ` for `λ=2,3`
- **Literature:** `lsd` uniqueness is `KNOWN`. The promoted content is the observational quotient of this expanding section, not a new digit definition
- **Open:** none opened. Do not auto-start a jet-observable phase
- **Decision:** PROMOTE the expanding-`T` LSD residual, section identities, magnitude refutation, and `λ=2,3` residue maps. Stop.

## Balanced-ternary expanding `T` Phase 2 (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Decide whether the 3-state LSD quotient of `T` lifts to a finite 2-digit integer jet
- **Hypotheses:** H1, `J₂(T(n))` is a function of `J₂(n)`; H2, a third digit is needed; H3, `T_2` remains observationally identical to `T` at order 2
- **Major results:** `J₂` is existing `integer_jet(-,2)`. Exact law `J₂(T(n))=(-lsd(n), lsd(n))` from `DZ∘T=id`. Residual is the 9 trit pairs; `T`-image has size 3; full-sequence classes 9; next-output Mealy 3. `n=1` vs `n=10` same `J₂`-orbit. `T_2` sends `J₂` to `(a,0)` and is therefore visible at order 2. `T_3` collapses to `(0,0)`. Engine `ExpandingJ2Spec` certifies exact size-9 closure. Lean `jet2_expandingD`, `jet2_residue_closure`, `jet2_expandingDGain_two`, `jet2_expandingDGain_three`. Non-Pisot Ostrowski `L_0` was not reopened
- **Refuted ideas:** `J₂(T(n))` depends on the second digit; the `J₂`-orbit requires `lsd(D^2(n))`; `T_2` is invisible at order 2
- **Literature:** length-`k` integer jets are `KNOWN` (`integer_jet`, Lean `integerJet`). The promoted content is the transformation law of that jet under expanding `T`
- **Open:** none opened. Do not auto-start `J₃`
- **Decision:** PROMOTE the `J₂` jet law, the 9-state residual, and the order-2 visibility of `T_2`. Stop.

## Balanced-ternary expanding `T` Phase 3 (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Determine the memory depth of `T` on `J₃=integer_jet(-,3)`, without assuming the third digit is used or that the map factors through `J₂`
- **Hypotheses:** H₃, `T` acts on `J₃` using strictly fewer than three input digits
- **Major results:** Existing jet, LSD-first. Exact law `J₃(T(n))=(-a,a,b)=(-a)‖J₂(n)` from `lsd(T)=-a` and `DZ(T)=n`. Third digit discarded; second digit survives. Factors through `J₂`, not `J₁` (`n=1` vs `n=4`). Same `J₂` different `c` does not separate (`n=1` vs `n=10`). Raw 27, reachable 27, `T`-image 9, full-sequence 27, next-output Mealy 9. Prefix square commutes. `T_2` maps to `(a,0,b)`; `T_3` maps to `(0,0,b)` and therefore does not collapse order 3. Engine `ExpandingJ3Spec` certifies exact size-27 closure. Lean `jet3_expandingD`, `jet3_factors_through_jet2`, `jet3_residue_closure`, `jet3_expandingDGain_two`, `jet3_expandingDGain_three`. Non-Pisot Ostrowski `L_0` was not reopened
- **Refuted ideas:** `J₃(T(n))` depends only on `a`; `J₂` is insufficient for the next `J₃`; `T_3` erases all jet information by order 3
- **Literature:** length-`k` integer jets are `KNOWN`. The promoted content is the memory-depth law at order 3, not a new digit model
- **Open:** none opened. Do not auto-start `J₄`
- **Decision:** PROMOTE the `J₃` shift law, the `J₂` factorization, the `J₁` refutation, and the order-3 visibility of `T_3`. Stop.

## D/Add residual completion (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Discover the smallest residual that restores locality of `D(x+y)` after the unary rewrite calculus meets `Add`, without installing a carry table
- **Hypotheses:** a finite residual smaller than `(x,y)` repairs `D(x+y)`; the obvious `R=lsd(x+y)` might suffice
- **Major results:** Candidate search refutes `R=lsd(x+y)` with `(1,1)` vs `(0,-1)`. `(lsd x, lsd y)` is sufficient; the exact correction is `D(lsd x + lsd y) ∈ {-1,0,1}`. On `D(x)=D(y)=0` the observable takes three values, so 3 is minimal. Streaming step `s'=D(s+a+b)` using existing `D`/`lsd` has exact trit closure. Engine `DAddResidualSpec` certifies size-3 closure. Bound-2 alphabet widens the box to 5 states. The diagonal `a=b` is Phase-0 doubled-trit. Lean `dAdd_repaired`, `dAdd_not_lsd_sum_local`, `dAdd_residual_closure`, `dAdd_minimal_residual`. Did not repeat `add_not_DLocal` or `D_add`. Did not reopen Ostrowski `L_0` or the unary paper
- **Refuted ideas:** `D(x+y)` factors through `(D(x),D(y),lsd(x+y))`; the 3-state box is independent of the input alphabet bound
- **Literature:** carry of balanced addition is `KNOWN`. The promoted content is engine discovery of the minimal residual and the `lsd(x+y)` obstruction
- **Open:** none opened. Do not auto-start multiplication
- **Decision:** PROMOTE the residual `D(lsd x + lsd y)`, the `lsd(x+y)` refutation, trit closure, and bound-2 widening. Stop.

## Shortcut Collatz finite-descent residual (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Decide whether the research engine can discover a finite residual and bounded affine-block certificate that forces strict descent in the shortcut map `C` (even `n/2`, odd `(3n+1)/2`), or an exact obstruction in a natural finite-state class
- **Hypotheses:** a finite residual `R` plus blocks of length `≤ L` certifies `C^{ℓ(R(n))}(n)<n` for all large `n`; `V(n)=n` is a one-step Lyapunov; `n mod 2^L` is a closed residual of one-step `C`
- **Major results:** `ShortcutSpec` reuses the generic planner. Controls are state-determined parity. `AffineSystem` is inapplicable. Integer-state BFS from 27 hits the cap (`INCONCLUSIVE`). Forward closure from 1 is the terminal cycle `{1,2}`. Derived blocks `C^k(n)=(a_w n+b_w)/2^k` on a unique residue. `n=2^L-1` realises the all-odd word and `C^L(n)=3^L-1>n`. Lean `shortcutC`, `shortcutC_terminal_cycle`, `shortcutC_odd_increases`, `shortcutC_no_uniform_L_descent`. Perturbation `C_{5,1}` still has no uniform `L`-descent on `n mod 2^L`. Claim ladder: not B, not C. Did not modify `research.collatz` or `bt.*`
- **Refuted ideas:** one-step Lyapunov `V(n)=n`; uniform bounded-block descent determined by `n mod 2^L`
- **Literature:** unbounded stopping time of `2^L-1` is `KNOWN`. Tao logarithmic density is not a target
- **Open:** none opened. Do not auto-start a second Collatz phase
- **Decision:** CLOSE. The obstruction is exact and Lean-checked, and it is elementary. A branch whose statements are `KNOWN` is a `CLOSE`

## BTC-add-affine-only Lean packaging (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Can the unrestricted English of `BTC-add-affine-only` — the unique complete finite form of integer sums of `{S, I_a, N}` is affine / evaluate-then-BT-NF, and every finite exact-on-ℤ tree TRS on `Add` is already-incomplete or a CAS — be a short sorry-free Lean theorem covering that row, without an AC-matching library?
- **Hypotheses:** wrapping or extending `RewriteAddBoundary.lean` covers the constructor classification; the remaining hole is maximality (“every finite exact tree TRS on Add”)
- **Major results:** Restricted Claim B is already Lean: `exactTriple_characterization`, `add_not_DLocal`, `pushIn_not_locally_confluent`, `add_requires_carry_state`. Those are `BTC-constructor-sum-class`, `BTC-add-not-D-local`, `BTC-push-in-S-peak`, `BTC-add-requires-carry-state`, not the unrestricted row. Unique coefficient-word NF is already `BTN-confluence` / `BT-encode-unique`. There is no AC-matching or generic TRS library in this lab. Quantifying over every finite exact Add-tree TRS is not a short proof; it is the same hole the restricted maximality gate already closed. No new Lean module. Tag stays **EXACT — HUMAN PROOF**. Related human row `BTC-add-factor-cas-obstruction` was not retagged
- **Refuted ideas:** that wrapping `RewriteAddBoundary` covers the unrestricted unique-complete-form / every-finite-exact-Add-TRS wording; that a stub maximality module would justify a Lean retag
- **Literature:** Newman / Knuth–Bendix and Peterson–Stickel AC completion remain `KNOWN` method. No AC engine was added
- **Open:** an independently defined class of finite exact Add-tree systems that would make maximality a short Lean theorem without an AC-matching library. Not taken up
- **Decision:** PARK. Do not retag. Do not invent a stub. Do not edit `BTCalculus/Confluence.lean`. Do not widen `TREE_RULES`. CLOSE is wrong: the human proof already exists. Stop.

## Prime residual complexity (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Measure residual complexity of Prime under existing LSD-first sections `I_a`, versus the finite residual of a fixed modular sieve, without rediscovering non-automaticity
- **Hypotheses:** a length-`L` LSD jet determines Prime continuations; a finite sieve residual `gcd(n,M)=1` equals Prime; integer `n` is a finite Prime residual; the sieve DFA on trit sections is finite
- **Major results:** `SieveSpec` is `AffineSystem` `x'=3x+a` reduced mod `M`. Closure on `Z/210Z` is `EXACT` size 210. Minimized coprimality DFAs: 2, 3, 14, 94 along `S={2}⊂{2,3}⊂{2,3,5}⊂{2,3,5,7}`. Integer Prime BFS hits the cap. Separators: `1` vs `1+3^L` (same jet) and `1` vs `1+M` (same sieve class), both split by `I_0`. Lean `i0_eq_mul3`, `i0_not_prime_of_natAbs`, `iz_mod_of_congruent`, `sievePrime_I0_separator`. `R_H(L)` at `H=3` is `3,6,15,42,122,360` for `L=1..6` (`OBSERVATION`). Did not edit `bt.*` or `research.primes` objects
- **Refuted ideas:** equal jets imply equal Prime continuations; sieve residual equals Prime; `V(n)=n` is a section Lyapunov
- **Literature:** primes are not automatic (`KNOWN`); coprimality modulo `M` is regular (`KNOWN`); `I_0(x)=3x` composite for `|x|>1` is elementary
- **Open:** none opened. Do not auto-start a second prime phase
- **Decision:** CLOSE. Exact statements are `KNOWN` divisibility packaged as sections. No residual-complexity law. Stop.

## Signed-digit residual phase transitions (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Decide whether doubled-trit, `D(x+y)`, bound-2 widening, and the `λ=3` escape are one residual family `F_{λ,U}(s,u)=λ·D(s+u)`, and extract an exact finite/infinite condition
- **Hypotheses:** bounded raw forcing plus radix-3 quotient yields finite closure; the coefficient `λ/3` controls the transition; reachable set equals the invariant interval; Mealy size equals raw residual count
- **Major results:** For `λ∈{1,2,3}` and `U_m`, origin-reachable residual is finite iff `λ≤2` or `m≤1`. Sharp `λ=1` box `|s|≤⌊m/2⌋`. `(3,1)` stays at `0`; `(3,2)` is `s_n=3n` on constant `u=2`. `(2,2)` reachable `{-2,0,2}` inside invariant interval `[-2,2]`. r-way trit addition is `F_{1,U_r}` with `M(r)=2⌊r/2⌋+1` for `r=1..4`. Asymmetric `U={0,1,2}` remains finite. Engine `SignedDigitResidualSpec` certifies `U_2` size-3 closure. Lean `lambda1_reachable_box`, `finite_residual_condition`, `origin_trit_forcing`, `multi_trit_carry_bound`, wrapping `carryGain3_unbounded`. No new engine. Did not reopen T/jets, Collatz, primes, or Ostrowski `L_0`
- **Refuted ideas:** `λ=3` independently of `U` forces infinitude; the loose radius `⌈(m+1)/2⌉` is optimal; invariant interval equals reachable set
- **Literature:** Avizienis signed-digit addition remains `KNOWN`. The promoted content is the `D`-dynamics threshold and the unification of prior laboratory cases
- **Open:** none opened. Do not auto-start a general-radix theorem
- **Decision:** PROMOTE the condition `C(λ,U_m)`, the sharp `λ=1` radius, the scalar-threshold refutation, and `M(r)`. Stop.

## BTM-x3-depth Lean packaging (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Package the already-proved cubic endpoint identity and 3-adic valuation law of `BTM-x3-depth` as a sorry-free Lean 4 theorem, without enlarging to the spectrum or non-preservation rows
- **Hypotheses:** a short ring identity plus Mathlib `padicValRat` / `padicValInt` lemmas covers the English identity, the depth formula, and the opposite-parity no-tie fact
- **Major results:** `monnaEndpoint_cube_diff` is the identity `u³−v³=4·3ⁿ(3ζ²+4·3^{2n})` on `ℚ` (and the same identity on `ℤ`). `monnaEndpoint_cube_val` is `t=v₃(u³−v³)=n+min(1+2 v₃(ζ),2n)`, or `t=3n` when `ζ=0`. `monnaEndpoint_val_parity` is opposite parity of the minimum's arguments for `ζ≠0`, which feeds `padicValRat.add_eq_min` and kills a cancellation tie. Ledger `BTM-x3-depth` retagged **EXACT — LEAN VERIFIED**, Lean path `BTCalculus/MonnaEndpointCube.lean`. `lake build BTCalculus` green. `BTM-x3-spectrum` and `BTM-x3-no-preserve` stay human. `Confluence.lean` was not edited. No `bt.*` change. Not a Collatz claim and not an `M_k(x³)` count
- **Refuted ideas:** none. The cubic counting line and Add maximality were not reopened
- **Literature:** 3-adic ultrametric inequality is `KNOWN` Mathlib. The named endpoint identity remains PROJECT-SPECIFIC packaging of an existing human proof
- **Open:** `BTM-x3-spectrum` and `BTM-x3-no-preserve` stay human
- **Decision:** PROMOTE the Lean packaging. Do not open a numbered milestone. Do not formalize the spectrum or non-preservation in this phase. Stop.

## BTM-x3-no-preserve Lean packaging (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Package the already-proved non-preservation obstruction of `BTM-x3-no-preserve` as a sorry-free Lean 4 theorem, without enlarging to the spectrum or defining the Monna map `B`
- **Hypotheses:** the arithmetic core `3ζ²+4·3^{2n}` is never `±3^k`, which with the existing cube-difference identity gives `u³−v³` never `±4·3^k`; endpoint collisions of `B` are exactly pairs of that difference, so the obstruction covers the English row
- **Major results:** `monnaEndpoint_factor_ne_pm_three_pow` is the factor obstruction. `monnaEndpoint_cube_diff_ne_pm_four_three_pow` is the cube-difference obstruction, reusing `monnaEndpoint_cube_diff`. Proof is positivity plus the existing opposite-parity valuation split: the 3-free part cannot be `±1`. `B` is not defined. Ledger `BTM-x3-no-preserve` retagged **EXACT — LEAN VERIFIED**, Lean path `BTCalculus/MonnaEndpointCube.lean`. `lake build BTCalculus` green. `BTM-x3-spectrum` stays human. `Confluence.lean` was not edited. No `bt.*` change. Not a Collatz claim and not an `M_k(x³)` count
- **Refuted ideas:** none. Defining a fake `B` to force a retag was not attempted. The cubic counting line and Add maximality were not reopened
- **Literature:** positivity of sums of squares and the 3-adic ultrametric inequality are `KNOWN` Mathlib. The named endpoint obstruction remains PROJECT-SPECIFIC packaging of an existing human proof
- **Open:** `BTM-x3-spectrum` stays human
- **Decision:** PROMOTE the Lean packaging. Do not open a numbered milestone. Do not formalize the spectrum in this phase. Stop.

## Multiplicative residual universality (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Decide whether residual dynamics of `λ·D(s+u)` depend on the algebraic source of `u` or only on the attainable raw alphabet, using trit products as a single controlled extension
- **Hypotheses:** H1, the control system factors through `h(d1,d2)=d1 d2` and matches `F_{λ,U_1}`; factor count changes residual complexity; origin residual has 3 states
- **Major results:** 9 pair controls quotient to 3 raw values `{-1,0,1}` and origin residual `{0}` for `λ∈{1,2,3}`, matching `U_1`. Three-trit product is the same residual. No equal-raw separator. Doubled product `u=2 d1 d2` has image `{-2,0,2}` and follows that alphabet (`λ=1` finite 3-state, `λ=3` unbounded `s_n=3n`). Engine `ProductResidualSpec` certifies size-1 closure. Lean `product_factor_through_raw`, `product_residual_closure`, `product3_origin`, `doubled_product_factor`. No new engine. Did not reopen T/jets, Collatz, primes, Ostrowski, or a general multiplication project
- **Refuted ideas:** three origin-reachable residual states; number of multiplicative factors changes residual; product syntax determines the phase independently of `U`
- **Literature:** trit multiplication is `KNOWN`; `lsdZ_mul` already existed. The promoted content is the raw-contribution quotient against addition
- **Open:** none opened. Do not auto-start a multiplication project
- **Decision:** PROMOTE the factor-through-raw theorem and the add-vs-mul contrast. Stop.

## Exact residual-dynamics classification (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Classify `F_{λ,U}(s,u)=λ·D(s+u)` exactly for integer `λ≥1` and finite `U`, including the finite/infinite boundary, without claiming novelty for finite signed-digit adders
- **Hypotheses:** finite iff `λ≤2` or `max|u|≤1`; geometry of `U` changes the phase; `M(λ,U)` is determined by `(λ, max|u|)`; scalar `λ/3` is the whole story
- **Major results:** Origin-reachable residual is finite iff `λ≤2` or `max|u|≤1`. For `U_m` this is `λ≤2` or `m≤1` (`origin_residual_box_iff`). At `λ=3`, `s'=s+u-lsd` so constant `|u|≥2` escapes by at least 1. At `λ≥4` the same control is strictly expanding on the matching ray (`signedIterate_unbounded_of_ge_three`). Sharp `λ=2` radius `2(m-1)_+`. Geometry changes closure/Mealy, not the phase. No new engine. Did not reopen T/jets, Collatz, primes, Ostrowski, or a multiplication project
- **Refuted ideas:** geometry of `U` controls the finite/infinite phase; `M` depends only on `(λ, max|u|)`; the scalar test `λ<3`
- **Literature:** Avizienis / redundant conversion transducers are `KNOWN` for `λ=1` bounded carry. Anashin is a different 1-Lipschitz criterion. The residual-dynamics iff for synthetic gain is `NEW FORMULATION` / `PROJECT-SPECIFIC`
- **Open:** none opened. Do not auto-start a general-radix theorem
- **Decision:** PROMOTE the classification. Stop.

## Rewrite-calculus prior-art correction (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Correct the publication draft against direct balanced-ternary arithmetic-rewriting, signed-digit carry, automata, and parallel-addition prior art without adding mathematics
- **What was learned:** CMR97 already uses balanced-ternary postfix digit append \(x :_t a=3x+a\), exactly the map called \(I_a\) here, and gives terminating and confluent arithmetic rewrite systems modulo AC. \(D\) is standard least-digit removal, not a priority claim. Avižienis establishes the signed-digit carry principle; Heuberger--Prodinger establish automata for signed-digit carry including balanced ternary; Frougny and coauthors establish local/parallel addition, minimal alphabets, and block locality. The surviving paper is narrower: the exact open one-hole `OpFrag` grammar, semantic injectivity of its irreducibles, and the `DLocal` factorization obstruction. Paper B's research engine remains separate
- **Strongest theorem:** **EXACT — LEAN VERIFIED** `unary_complete_canonical_form` together with `add_not_DLocal`: the specified unary TRS is terminating, confluent, and semantically canonical, while no \(G\) satisfies \(D(x+y)=G(D(x),D(y))\) for all integers
- **Strongest refutation:** The broad claim that this project develops the first balanced-ternary arithmetic rewrite calculus is unsupported and contradicted by CMR97
- **Reusable machinery:** Eight literature-registry records, an explicit CMR97 \(\leftrightarrow\) \(I_a\) translation, a source-scoped comparison table, and `docs/theory/rewrite_calculus_prior_art.md`
- **Branch status:** `PROMOTE`
- **Why:** The arithmetic novelty was removed, but a coherent theorem/formalization distinction survives: CMR97 normalizes arithmetic terms, whereas this paper proves semantic canonicity for an explicit open unary destructor/section grammar and an exact state-factorization obstruction. No historical priority is claimed for those statements
- **Best next question:** Does external review accept this theorem-scope distinction as sufficient motivation for a short formal-methods note?

## Signed-digit residual geometry (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Characterize the origin-reachable set inside the finite envelope of `F_{λ,U}`, and whether Mealy size follows that geometry
- **Hypotheses:** `R=λℤ∩ B^*` for `U_m` and for every finite `U`; sign symmetry halves `M`
- **Major results:** `R_{1,U_m}` is the full interval, filled by `u=2,4,...,2n`. `R_{2,U_m}` is the even lattice in the sharp box, filled by `u=k+2`. Lattice-in-box fails for `U={2}` (reachable `{0,1}` inside `[-1,1]`). `M=|R|` on `U_m` and the four probes. Reused `SignedDigitResidualSpec`. Lean `lambda1_interval_reachable`, `lambda2_even_reachable`, `singleton_two_misses_neg_one`. Did not reopen the phase law, T/jets, Collatz, primes, or Ostrowski
- **Refuted ideas:** lattice-in-box for arbitrary `U`; sign symmetry forces `M=|R|/2`
- **Literature:** Avizienis conversion transducers are `KNOWN` for `λ=1` bounded carry. The fill of the envelope and the one-sided hole are `NEW FORMULATION` / `PROJECT-SPECIFIC`
- **Open:** none opened
- **Decision:** PROMOTE the `U_m` fill and the one-sided counterexample. Stop.

## Signed-digit residual minimality (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Decide whether `M=|R|` is a theorem for `F_{λ,U}` with output `lsd(s+u)`, or an artifact of previously tested alphabets
- **Hypotheses:** some sparse `U` merges distinct reachable residuals; identical 1-letter `lsd` signatures force equivalence
- **Major results:** If `λ` is not divisible by 3, distinct integers are separated by a constant word of length `v_3(s-t)+1` (`residual_separation`). Immediate signatures agree iff `s≡t (mod 3)`, and the successor difference `λ(s-t)/3` is independent of the control. Listed alphabets and `U_m` (`m≤6`) have singleton Mealy classes. At `λ=3`, `s ~ s+3k` on `ℤ` (`lambda3_trace_translate`), but that symmetry is not origin-reachable when `max|u|≤1`. Reused `SignedDigitResidualSpec` and `mealy_partition`. Did not reopen the phase law, the `U_m` fill, T/jets, Collatz, primes, or Ostrowski
- **Refuted ideas:** a listed alphabet with `M<|R|`; identical 1-letter signatures imply a merge (`0` vs `3` at `λ=1`, word `(0,0)`)
- **Literature:** unique BT expansion and carry-transducer minimization are `KNOWN`. The 3-adic distinguishing length for this residual map is `NEW FORMULATION`
- **Open:** none opened
- **Decision:** PROMOTE the coprime-gain rigidity theorem. Stop.

## Signed-digit constrained controls (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Test whether 3-adic residual rigidity survives a finite control language
- **Hypotheses:** rigidity requires a common cyclic letter; some Model A–D constraint merges distinct residuals at one control state
- **Major results:** Every word of length `v_3(s-t)+1` separates when `3∤λ` (`any_word_separation`). No-repeat `U_2` has a 10-state minimal product. Equal-parity Model D collapses `(s,0)∼(s,1)` without residual merge. `λ=3` translation holds for every word (`lambda3_constrained_symmetry`). Reused `signed_step` and `mealy_partition`. Did not reopen the phase law, Collatz, primes, T/jets, or Ostrowski
- **Refuted ideas:** a cyclic/constant letter is necessary; Models A–D produce residual merges
- **Literature:** constrained synchronization and carry transducers are `KNOWN` and answer different questions. The any-word strengthening is `NEW FORMULATION`
- **Open:** none opened
- **Decision:** PROMOTE the any-word separation theorem. Stop.

## Signed-digit short-horizon controls (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Decide whether a control language of max length strictly less than `v_3(s-t)+1` can make distinct residuals equivalent at the same control state
- **Hypotheses:** genuine short-horizon merging; some shorter word always separates; only deadlock artifacts
- **Major results:** If `3^L∣s-t` and `|w|≤L` then traces agree (`truncated_3adic_equiv`). If `3∤λ` and `|w|≥v_3(s-t)+1` then traces differ (`short_horizon_separation`). Hence `(s,q_L)∼(t,q_L)` iff `3^L∣s-t`. Smallest genuine merge `(0,q_1)∼(3,q_1)`. Horizon 0 is deadlock (`3^0=1`). Origin-reachable `U_2` horizon-2 product has 7 states and merges distinct residuals only at remaining 0. At `λ=3`, `L≥1` adds no classes beyond translation. Reused `signed_step`, `ControlAutomaton`, `mealy_partition`. Did not reopen the phase law, Collatz, primes, T/jets, or Ostrowski
- **Refuted ideas:** some shorter legal word always separates; finite horizon merges only by deadlock; `λ=3` short horizon creates new residual classes
- **Literature:** Mealy/Nerode equivalence, Anashin p-adic automata, and carry transducers are `KNOWN`. The truncated-congruence characterization is `NEW FORMULATION`
- **Open:** none opened
- **Decision:** PROMOTE the truncated-congruence theorem. Stop.

## Signed-digit finite-language max-length criterion (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Reproduce promoted residual theorems through the v2 engine API, reproduce the short-horizon theorem exactly, and decide whether a proper subset of a complete depth-L control tree can create extra residual merges
- **Hypotheses:** missing some (but not all) length-k words can merge a pair; finite L_q merges iff max|w|<v_3(s-t)+1
- **Major results:** v2 `observe` / identity factorization / envelope holes / `separate_states` / `CertificateKind` reproduce the signed-digit, geometry, minimality, product, D+Add, expanding-D, short-horizon, Collatz, and prime facts. Short-horizon `(0,q_1)∼(3,q_1)` is `EXACT_CLOSURE`; length 2 is `EXACT_COUNTEREXAMPLE`. Proper subsets with a remaining word of length k still separate. Lean `traces_eq_iff_len_le_val`. Horizon-2 U_2 profile: 5 controls = 5 contributions, 7 reachable, 5 Mealy, `EXACT_CLOSURE`. No new engine
- **Refuted ideas:** a proper subset of the complete tree can hide every separator while keeping a long word
- **Literature:** Mealy/Nerode and Anashin remain `KNOWN`. The per-word iff is `NEW FORMULATION` of the two previous 3-adic theorems
- **Open:** none opened
- **Decision:** PROMOTE the max-length / per-word criterion. Stop. Do not broaden the class of control languages

## Research engine v2 residual dynamics layers (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Encode controls ≠ raw contribution ≠ invariant envelope ≠ reachable set ≠ behavioral quotient as independently reusable engine layers with explicit exact/bounded certificates, without a second claim vocabulary
- **Hypotheses:** existing adapters already contain the distinctions; extracting them does not change known residual counts
- **Major results:** Optional `ObservableSpec`, `check_control_factorization`, envelope-vs-reachability comparison, pair-state separation BFS, engine Mealy quotient, `ComplexityProfile`, `CertificateKind` on attack results, session `PriorArtStatus` gate on `PROMOTE`. Named theorems still use the seven ledger tags. `PROVED` is not an engine status
- **Refuted ideas:** treating a depth-capped pair search as exact equivalence; promoting a hypothesis with `UNKNOWN` prior art
- **Literature:** not a mathematical claim. The prior-art field records methodology novelty (`KNOWN` / `PROJECT-SPECIFIC` / `NEW_FORMULATION`) on the session ledger only
- **Open:** none opened
- **Decision:** PROMOTE the extracted layers into `research_engine`. Stop.

```text
What was learned      Observation, raw contribution, envelope, reachable set, and Mealy size are distinct report fields. Bounded reconnaissance is CertificateKind.BOUNDED_RECONNAISSANCE. Queue exhaustion is EXACT_CLOSURE. Pair BFS reports INCONCLUSIVE when capped.
Strongest theorem     none new; the engine now states existing signed-digit / product / D+Add / Collatz / prime facts in one vocabulary
Strongest refutation  a depth cap is not exact behavioral equivalence
Reusable machinery    CertificateKind, ObservableSpec, factorization check, envelope comparison, BehavioralSeparationAttack, engine Mealy quotient, ComplexityProfile, PriorArtStatus
Branch status         PROMOTE
Why                   The signed-digit theorems already survived. This is reusable machinery after the fact, not a new residual theory
Best next question    Which new integer dynamics can be compared to signed-digit residual using only ComplexityProfile and CertificateKind?
```

## Operator-dynamics v2 benchmark N∘I₀∘D (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Test whether Research Engine v2 can diagnose a new integer map built from existing BT operators, without a problem-specific theory
- **Hypotheses:** \(F_{a,b}=I_a\circ D\circ I_b\) is a nontrivial dynamical system; \(|n|\le 2\) is invariant; \(V(n)=n\) is a Lyapunov; \(\mathbb{Z}\) is one finite residual
- **Major results:** \(F_{a,b}\) collapses to \(I_a\) by \(D\circ I_b=\mathrm{id}\). The surviving word \(F=N\circ I_0\circ D\) has \(F^2=P_0\), \(F^3=F\), and every orbit has size at most 3. Seed \(4\) closes in 3 states (`EXACT_CLOSURE`); sign Mealy quotient has 2 classes; the box \(|n|\le 2\) leaks at \(F(-2)=3\) and \(F(2)=-3\). Integer-state infinitude is the disjoint union of finite orbits, not residual infinitude. Reused generic planner only. Did not reopen signed-digit, Collatz, primes, jets, Ostrowski, or the `{S,N,D,W}` census. No new engine primitive. No ledger row
- **Refuted ideas:** \(F_{a,b}\) as a benchmark target; interval invariance; one-step Lyapunov; a single finite residual on \(\mathbb{Z}\)
- **Literature:** \(D\circ I_a=\mathrm{id}\) and \(P_a\circ P_b=P_a\) are `KNOWN`. The orbit law is a `NEW FORMULATION` of the band plus \(N\), recorded as `REPARAMETERIZATION` for the branch
- **Open:** none opened
- **Decision:** CLOSE. The map is known \(P_0\)/\(N\) algebra. The benchmark succeeded as a structural diagnosis

```text
What was learned
- I_a(D(I_b(n))) rewrites to I_a immediately; it is not a dynamics target
- N∘I_0∘D is the smallest surviving word with nontrivial iteration
- v2 reports exact per-seed closure of size 3 without being told P_0
- The interval envelope |n|≤2 leaks; V(n)=n is not a Lyapunov
- Sign observation merges 4∼3 on that orbit (M=2<|R|=3)
- Integer-state infinitude is a disjoint union of finite orbits, not residual infinitude
- Modular/spectral/block/factorization stayed inapplicable; no engine change

Strongest theorem
- F² = P_0 for F = N∘I_0∘D; every orbit has size at most 3 (Lean signedP0_sq_eq_P0, signedP0_orbit_finite)

Strongest refutation
- F(2)=-3 leaves |n|≤2; orbits of 3 and 6 are disjoint

Reusable machinery
- none; the generic v2 planner was reused as-is

Prior-art status
- NEW FORMULATION of the P-band plus N; branch CLOSE as REPARAMETERIZATION

Complexity profile
- controls 1; no raw contribution; seed reachable 3; Mealy 2; closure EXACT_CLOSURE; dominant certificate EXACT_CLOSURE

Branch status
- CLOSE

Why
- Local semantics were already the calculus. The engine correctly diagnosed finite per-orbit residual, a leaking envelope, and a sign quotient. The identities are corollaries of P_0∘P_0=P_0 and N²=id, not a new class.

Best next question
- none on this line; do not enumerate another operator word
```

## Balanced-ternary digit-sum dynamics T=s (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Test whether Research Engine v2 can diagnose T(n)=s(n) from exact local digits, without a problem-specific theory
- **Hypotheses:** V(n)=n is a Lyapunov; T²=T; identity observation merges orbit points; ℤ is one finite residual; the box |n|≤2 leaks
- **Major results:** Local fold s(n)=lsd(n)+s(D(n)) matches A065363. Seed 4 closes in 3 states (`EXACT_CLOSURE`); identity Mealy quotient has 3 classes (`M=|R|`); box |n|≤2 does not leak; reverse/block/modular/spectral/factorization/symmetry inapplicable. |s(n)|<|n| for |n|≥2 (Lean digitSumZ_natAbs_lt); every orbit reaches |n|≤1 (digitSumIterate_reaches_unit). Did not reopen signed-digit, Collatz, primes, jets, Ostrowski, N∘I₀∘D, or polynomial s_bal(P(n)). No new engine primitive. No ledger row
- **Refuted ideas:** T²=T; one-step Lyapunov; a single finite residual on ℤ; identity-observation merge
- **Literature:** s_bal is `KNOWN` (A065363). The iteration is the balanced-ternary digital root A134452 (`KNOWN`). Branch CLOSE as reparameterization of that sequence
- **Open:** none opened
- **Decision:** CLOSE. The map is known digital-root algebra. The benchmark succeeded as a structural diagnosis of a recursive digit fold

```text
What was learned
- T(n)=s(n) is the recursive fold of lsd and D, not a fixed operator word
- v2 reports exact per-seed closure of size 3 without being told a digital root
- The interval sample |n|≤2 does not leak; V(n)=n is not a Lyapunov
- Identity observation yields M=|R|; no behavioral merge
- Integer-state infinitude is a disjoint union of finite contracting orbits
- Reverse is inapplicable (infinite preimages); no engine change

Strongest theorem
- |s(n)| < |n| whenever |n|≥2; s iterated |n| times has absolute value ≤ 1 (Lean digitSumZ_natAbs_lt, digitSumIterate_reaches_unit)

Strongest refutation
- T(4)=2 and T(2)=0, so T²≠T; orbits of 4 and 5 are disjoint

Reusable machinery
- none; the generic v2 planner was reused as-is

Prior-art status
- KNOWN balanced-ternary digital root (OEIS A134452); branch CLOSE as REPARAMETERIZATION

Complexity profile
- controls 1; no raw contribution; seed reachable 3; Mealy 3; closure EXACT_CLOSURE; dominant certificate EXACT_CLOSURE

Branch status
- CLOSE

Why
- Local semantics were already the calculus. The engine correctly diagnosed finite per-orbit residual, a non-leaking sample envelope, and identity-observation equality M=|R|. The identities are the classical digital root, not a new class.

Best next question
- none on this line; do not enumerate another digit-fold map
```

## Balanced-ternary weight dynamics T=W (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Control experiment: does v2 diagnose a different regime for the nonlinear sign-erasing map W(n)=∑ d_i² than the finite-contracting digit-fold already seen for SignedP0 and s(n)?
- **Hypotheses:** |W(n)|<|n| for |n|≥2; V(n)=n is a Lyapunov; W²=W; identity observation merges orbit points; ℤ is one finite residual; the box |n|≤2 leaks; W is odd
- **Major results:** Local fold W(n)=lsd(n)²+W(D(n)) matches A005812 on ℕ. Seed 4 closes in 2 states (`EXACT_CLOSURE`); identity Mealy quotient has 2 classes (`M=|R|`); box |n|≤2 does not leak; reverse/block/modular/spectral/factorization/symmetry inapplicable. |W(n)|<|n| for |n|≥3 (Lean weightZ_natAbs_lt); W even (weightZ_even); every orbit reaches |n|≤2 (weightIterate_reaches_le_two). Recurrent set {0,1,2}. Did not reopen signed-digit, Collatz, primes, jets, Ostrowski, N∘I₀∘D, or digit-sum dynamics. No new engine primitive. No ledger row
- **Refuted ideas:** |W|<|n| for |n|≥2 (W(2)=2); W²=W; one-step Lyapunov; a single finite residual on ℤ; identity-observation merge; oddness
- **Literature:** W on ℕ is `KNOWN` (A005812). Iteration is the digital-root architecture with attractor {0,1,2} (`KNOWN` as a class). Branch CLOSE as regime-replication of the digit-sum finite-contracting pattern
- **Open:** none opened
- **Decision:** CLOSE. Same finite-contracting digit-fold regime as s(n). Sign-erasure only shifts the attractor and makes the map even. Do not enumerate another digit statistic

```text
What was learned
- W(n)=∑ d_i² is the recursive fold of squared local trits, not a new operator word
- v2 reports exact per-seed closure of size 2 without being told Hamming weight
- The |n|≥2 contraction of s(n) fails at the fixed point W(2)=2; contraction holds for |n|≥3
- Identity observation yields M=|R|; no behavioral merge
- Integer-state infinitude is a disjoint union of finite contracting orbits
- Reverse is inapplicable; no engine change

Strongest theorem
- |W(n)| < |n| whenever |n|≥3; W is even; W iterated |n| times has absolute value ≤ 2 (Lean weightZ_natAbs_lt, weightZ_even, weightIterate_reaches_le_two)

Strongest refutation
- W(2)=2, so |T(n)|<|n| for |n|≥2 is false; W(5)=3 and W(3)=1, so W²≠W

Reusable machinery
- none; the generic v2 planner was reused as-is

Prior-art status
- KNOWN OEIS A005812; iterated nonzero-count is the digital-root class; CLOSE as regime replication

Complexity profile
- controls 1; no raw contribution; seed reachable 2; Mealy 2; closure EXACT_CLOSURE; dominant certificate EXACT_CLOSURE

Branch status
- CLOSE

Why
- Replacing signed aggregation by sign-erasing aggregation did not change the v2 architecture: recursive local fold, magnitude compression, finite per-seed residual, identity observation with M=|R|, reverse inapplicable. The even image and attractor {0,1,2} are parameter changes inside the same regime.

Best next question
- none on this line; do not enumerate another digit statistic
```

## Balanced-ternary weight-drift T=n+W (not a numbered milestone)

- **Date:** 2026-08-25
- **Objective:** Test whether v2 diagnoses F(n)=n+W(n) as a different regime from the finite-contracting digit-fold of SignedP0, s(n), and W(n)
- **Hypotheses:** seed-4 orbit finite; box |n|≤2 invariant; V(n)=n decreases; one finite residual on ℤ; identity merge; F²=F; |F|<|n| for |n|≥2; F even; disjoint orbits
- **Major results:** Generic planner reports INCONCLUSIVE residual closure on seed 4, REFUTED functional |n| bound (4↦6), REFUTED box |n|≤2 (F(2)=4), INCONCLUSIVE quotient. Post-hoc: n≠0 ⇒ F(n)>n and n≤0 ⇒ F^{|n|}(n)=0 (Lean weightDriftZ_gt, weightDriftIterate_reaches_zero). Orbits of 4 and 5 meet at 8. Did not reopen signed-digit, Collatz, primes, jets, Ostrowski, N∘I₀∘D, digit-sum, or weight dynamics. No new engine primitive. No ledger row
- **Refuted ideas:** finite positive residual; interval invariance; evenness of F; disjoint orbits; contraction for |n|≥2
- **Literature:** W is A005812 (`KNOWN`). The generator n ↦ n+s(n) is Kaprekar / A062028 (`KNOWN`). Branch CLOSE as reparameterization of that class
- **Open:** none opened
- **Decision:** CLOSE. v2 correctly left the digit-fold regime. The identities are classical n+f(n) generator facts. Do not enumerate another digit-statistic perturbation

```text
What was learned
- Replacing n by W(n) contracts; adding W(n) to n produces strict increase off 0
- v2 reports INCONCLUSIVE residual closure and a REFUTED |n| bound on seed 4 without being told growth
- The nonpositive ray still contracts to 0; the split is sign-dependent
- Distinct positive seeds may merge (4 and 5 meet at 8)
- Identity observation still forbids a nontrivial Mealy quotient
- No engine change: the state cap is not infinitude, and Lean certifies the inequalities

Strongest theorem
- n ≠ 0 ⇒ n < n+W(n); n ≤ 0 ⇒ F^{|n|}(n)=0 (Lean weightDriftZ_gt, weightDriftIterate_reaches_zero)

Strongest refutation
- F(2)=4, so the box |n|≤2 leaks and |F| is not a contraction for |n|≥2; orbits of 4 and 5 meet at 8

Reusable machinery
- none; the generic v2 planner was reused as-is

Prior-art status
- KNOWN Kaprekar generator class (A062028) with increment A005812; CLOSE as REPARAMETERIZATION

Complexity profile
- controls 1; no raw contribution; seed reachable prefix hits the cap; closure INCONCLUSIVE; dominant certificate none (Lean inequalities sit outside the attack ledger)

Branch status
- CLOSE

Why
- The experiment escaped digit-fold contraction on positives, which is the intended diagnostic. The exact structure is the classical n+f(n) generator with a nonnegative digit statistic vanishing only at 0. That is not a new mathematical class.

Best next question
- none on this line; do not enumerate another digit-statistic perturbation
```

## Research Engine diagnosis loop and Syracuse stress test

- **Date:** 2026-08-25
- **Objective:** Upgrade v2 from attack executor to a diagnose → compare → decide loop, then stress-test it on the accelerated odd-only map without Collatz hints
- **Hypotheses:** SignedP0 / digit-sum / weight share a finite-contracting regime that saturates; Syracuse is a different class; the engine may hit a representation boundary on hidden \(2\)-adic branching
- **Major results:** `research_engine.diagnosis` (`RegimeFingerprint`, family saturation, `ResearchDecision`, `ExpectedResearchValue`). Digit-fold family `SATURATED` from evidence, not from names. WeightDrift stays a non-member expanding control. Syracuse adapter in `research.syracuse` (no `research.collatz` import): mixed magnitude, truncated closure, `ENGINE_LIMITATION`. Lean `syracuseS_one` packages `acceleratedT`. No ledger row
- **Refuted ideas:** one-step Lyapunov; odd interval [1,15]; contraction for odd \(n\ge 3\); idempotence
- **Literature:** Lagarias survey, Terras stopping times, Tao logarithmic density (`KNOWN`); cycle preprints not treated as theorems; parked Collatz module not reopened
- **Open:** generic piecewise-affine / prime-power-clearing census
- **Decision:** PARK (engine `ENGINE_LIMITATION`). Do not auto-continue; do not claim a Collatz result

```text
What was learned
- Diagnosis classifies the three closed digit maps as one finite-contracting family
- Family saturation discourages another contracting scalar fold without a hard-coded ban
- Syracuse is not that family: mixed growth and truncated residuals under dummy control
- v2 can refute naive descent, but cannot name the hidden 2-adic partition as a control alphabet
- S(1)=1 is exact and KNOWN; a bounded seed-27 census is not convergence

Strongest theorem
- S(1)=1 (Lean syracuseS_one); well-definedness is acceleratedT (KNOWN)

Strongest refutation
- S(3)=5 and S(11)=17 kill one-step contraction and a small odd interval

Reusable machinery
- research_engine.diagnosis (fingerprints, family status, coverage, research decision, scorer)

Prior-art status
- KNOWN 3x+1 map; engine rediscovery of well-definedness and the 1-cycle; ENGINE_LIMITATION on implicit valuation control

Complexity profile
- seed 27: 1 control; closure INCONCLUSIVE; |n| functional REFUTED; no profile-schema fork

Branch status
- PARK

Why
- The upgrade succeeded: v2 now decides what kind of mathematics to attempt next. Syracuse shows a new regime and a precise engine boundary. That is not a Collatz solution and does not reopen research.collatz.

Best next question
- Can a generic piecewise-affine census from I/O samples become a reusable v2 attack?
```

## Generic piecewise-affine census

- **Date:** 2026-08-25
- **Objective:** Turn the Syracuse `ENGINE_LIMITATION` into a generic I/O census that recovers latent affine branches without map-specific hints
- **Hypotheses:** Hidden congruence/sign/nested maps admit a finite census; an unbounded \(2^k\) family must not collapse to a finite table; Syracuse may then show a parameterized family from samples
- **Major results:** `PiecewiseAffineCensus` (`AffineBranch`, `BranchRegion`, `LatentControl`). Synthetics A–C recover hidden finite branches; D is `PARAMETERIZED_CENSUS` for \((x+1)/2^{v_2(x+1)}\). Digit-fold core family stays `SATURATED`. Syracuse adapter still hint-free: sample-supported family \(2^k y=3x+1\), engine `CONTINUE` (not `ENGINE_LIMITATION`). Lean `hiddenCongruenceA` residue identities; no ledger row
- **Refuted ideas:** two-point lines as branches; finite affine tables for unbounded \(2^k\) families; promoting window agreement to a \(\mathbb{Z}\)-theorem
- **Literature:** `acceleratedT_mul` **KNOWN**; census rediscovery is **OBSERVATION**
- **Open:** exact certification of a reconstructed \(2^k\)-divisibility region
- **Decision:** PARK (engine `CONTINUE` on Syracuse). Do not auto-continue; do not claim a Collatz result

```text
What was learned
- A generic I/O census can recover hidden finite affine partitions
- Parameterized 2^k families are a distinct census kind, not a growing finite table
- Digit-fold cores are unchanged; SignedP0 has only a secondary mod-3 census
- Syracuse yields 2^k y = 3x+1 from samples, which is KNOWN as acceleratedT_mul
- Same-run modular/cycle attacks stay inapplicable without AffineSystem injection

Strongest theorem
- hiddenCongruenceA residue identities (Lean); elementary KNOWN arithmetic

Strongest refutation
- Synthetic D and Syracuse refuse a finite branch table

Reusable machinery
- research_engine.attacks.piecewise_affine and hidden_piecewise benchmarks

Prior-art status
- KNOWN clearing identity; engine rediscovery from I/O; no new Collatz theorem

Complexity profile
- census metrics on AttackResult.evidence; profile schema not forked

Branch status
- PARK

Why
- The missing generic capability now exists and moved the Syracuse engine boundary. The recovered family is already known mathematics. Remaining work is exact domain certification, not a Collatz solver.

Best next question
- Can a reconstructed 2^k-divisibility region become an exact generic certificate without map-specific hints?
```

## Exact domain certificates

- **Date:** 2026-08-25
- **Objective:** Certify arithmetic predicates of a reconstructed parameterized family without map-specific hints, distinguishing mere divisibility from maximal selection
- **Hypotheses:** Maximal conjunction \(b^k\mid q \land b^{k+1}\nmid q\) is exact parameter selection; \(b^k\mid q\) alone is necessary-only when higher \(k\) exist; the integer iff with \(v_b(q)\) is reusable, not a Collatz identity
- **Major results:** `ParameterDomainAttack` after `piecewise_affine` via `prior_results`. Synthetics: trap B is `NECESSARY_ONLY`; maximal A and odd-prime C are `EXACT`; mixed D uses residue AND maximal. Syracuse hint-free: conjunction \(2^k\mid(3x+1)\land 2^{k+1}\nmid(3x+1)\), presentation \(k=v_2(3x+1)\) only after certification. Engine `CONTINUE`. Lean `mul_pow_eq_iff_padicValInt`. No ledger row
- **Refuted ideas:** billing mere divisibility as exact parameter selection; treating window-exact map realization as a \(\mathbb{Z}\)-theorem; seeding \(v_2(3x+1)\)
- **Literature:** `acceleratedT_mul` and padic valuation iff **KNOWN**; engine rediscovery is **OBSERVATION**
- **Open:** generic certificates beyond KNOWN clearing, still without map-specific hints
- **Decision:** PARK (engine `CONTINUE` on Syracuse). Do not auto-continue; do not claim a Collatz result

```text
What was learned
- A reconstructed family can be certified without seeding a valuation formula
- Mere divisibility is necessary-only when several exponents appear
- The integer iff (b^k y = q and b does not divide y) iff v_b(q)=k is KNOWN arithmetic
- Digit-fold cores and WeightDrift exclusion are unchanged
- Syracuse domain EXACT is the known clearing identity, not a new Collatz theorem

Strongest theorem
- mul_pow_eq_iff_padicValInt (Lean); elementary KNOWN arithmetic

Strongest refutation
- Trap B: 2^k | q does not select the exact parameter when higher k exist

Reusable machinery
- research_engine.attacks.parameter_domain; BASE_BOX {2,3,5,7}; prior_results chaining

Prior-art status
- KNOWN clearing and KNOWN valuation iff; engine rediscovery from I/O; no new Collatz theorem

Complexity profile
- domain metrics on AttackResult.evidence; profile schema not forked

Branch status
- PARK

Why
- The missing generic domain-certificate layer exists and classified Syracuse as KNOWN clearing with an exact arithmetic relation. Map globality on Z remains empirical. That is not a Collatz solver.

Best next question
- Is there a generic certificate beyond KNOWN clearing that still does not require map-specific hints?
```

## End-to-end Syracuse domain certification

- **Date:** 2026-08-25
- **Objective:** Run the existing census plus domain pipeline hint-free on Syracuse and decide whether the old domain-certification limitation is gone
- **Hypotheses:** v2 can reconstruct maximal-divisibility domains generically; mere divisibility is not exact; odd-prime synthetics confirm the mechanism is not base-2
- **Major results:** Hint-free family \(2^k y=3x+1\), \(k\in\{1,2,3,4,6\}\). Maximal conjunction `EXACT`/`LEAN_CERTIFIED` for the relation; mere divisibility `NECESSARY_ONLY`. Engine `CONTINUE` (PARTIALLY_CERTIFIED: map globality empirical). Lean `syracuseS_parameter_iff` applies the generic Engine lemma. Digit-fold `SATURATED`. No `research.collatz` reopen
- **Refuted ideas:** \(2^k\mid(3x+1)\) as exact parameter selection; treating window agreement as a \(\mathbb{Z}\)-theorem; `ENGINE_LIMITATION` as the current Syracuse status
- **Literature:** `acceleratedT_mul` **KNOWN**; engine rediscovery **OBSERVATION**
- **Open:** consume certified latent control in generic modular/cycle/quotient attacks, without Collatz escalation
- **Decision:** PARK (engine `CONTINUE`). Do not auto-continue

```text
What was learned
- v2 crossed observe → infer → parameterize → identify domain → certify for the arithmetic relation
- Maximal divisibility is exact; mere divisibility is necessary-only
- Odd-prime v3 synthetic certifies the same pipeline off base 2
- Map globality, cycles, and boundedness remain unproved
- Digit-fold cores and WeightDrift exclusion are unchanged

Strongest theorem
- mul_pow_eq_iff_padicValInt, specialized as syracuseS_parameter_iff; KNOWN arithmetic

Strongest refutation
- Mere 2^k | (3x+1) does not select k when higher exponents exist

Reusable machinery
- none added; existing parameter_domain and census were sufficient

Prior-art status
- KNOWN clearing identity; NEW GENERIC ENGINE CAPABILITY is the pipeline, not the identity

Complexity profile
- unchanged schema; domain costs on evidence (predicate_count=5, queries=1994)

Branch status
- PARK

Why
- The missing domain-certification limitation is gone for the reconstructed relation. Remaining gaps are Collatz-scale and explicitly out of scope.

Best next question
- Can exact reconstructed latent control be consumed by generic control-word, cycle, modular, quotient, or residual attacks?
```

## Control-word composition of certified latent families

- **Date:** 2026-08-25
- **Objective:** Consume a certified one-step affine family as an abstract certificate and derive exact multi-step constraints without map-specific composition laws
- **Hypotheses:** Cleared affine steps compose symbolically; algebraic composition is not realizability; later-step domain obstructions and necessary cycle constraints are generic; Syracuse is only a consumer
- **Major results:** Attack `control_word` after `parameter_domain`. Synthetics A–F validate composition, impossible suffixes, involution cycles, and off-domain algebraic candidates. Syracuse derives \(2^{\sum k}x_m=3^m x_0+C(\mathbf{k})\) and \((2^K-3^m)x=C\) from the certificate. Fingerprint `latent_control_algebra=EXPLOITABLE`. Engine `CONTINUE`. Lean `compose_two_affine` / `cycle_of_composed`. Block/modular/spectral stay inapplicable (no `AffineSystem` injection). No ledger row
- **Refuted ideas:** treating a composed equation as a realized trajectory; treating a cycle constraint as a cycle; injecting affine systems to force block dynamics; hard-coding the Syracuse product formula
- **Literature:** composed clearing and Collatz cycle equations **KNOWN**; generic engine consumption is the capability
- **Open:** map-agnostic obstruction from composed constraints, still without Collatz escalation
- **Decision:** PARK (engine `CONTINUE`). Do not auto-continue; do not claim a Collatz result

```text
What was learned
- A certified family can be composed without rediscovering or hard-coding its law
- FORMALLY_COMPOSED is not REALIZABLE; later k=0 on coprime images is IMPOSSIBLE
- Hypothetical periods produce exact (A-B)x=C constraints, not orbits
- Previously inapplicable AffineSystem attacks stay inapplicable; control_word is the newly applicable layer
- Digit-fold cores and WeightDrift exclusion are unchanged

Strongest theorem
- compose_two_affine and cycle_of_composed (Lean); elementary KNOWN algebra

Strongest refutation
- Power-clear words (*,0) are algebraically composable and arithmetically impossible

Reusable machinery
- research_engine.attacks.control_word; cleared-form composition; latent_control_algebra fingerprint

Prior-art status
- KNOWN cycle/composition identities; NEW GENERIC ENGINE CAPABILITY is reasoning with certified controls

Complexity profile
- unchanged schema; word_count / queries / quotient_size on evidence

Branch status
- PARK

Why
- Certified latent control is now a reasoning layer. The Syracuse identities it produces are already known. Map globality remains empirical. That is not a Collatz solver.

Best next question
- Can exact multi-step control-word constraints feed a generic obstruction attack that remains map-agnostic?
```

## Control-word obstruction calculus

- **Date:** 2026-08-25
- **Objective:** Consume exact control-word constraints and derive class-level arithmetic obstructions without map-specific logic
- **Hypotheses:** Length-1 cycle solvability is a finite divisor class; search failure is not impossibility; the same calculus applies off Syracuse
- **Major results:** Attack `control_obstruction` after `control_word`. Synthetics A–F: divisor class, modular class, empty odd-prime class, later-k domain class, sign off-domain, large-candidate not impossible. Syracuse length-1 possible \(k\in\{1,2\}\) as divisor class (KNOWN). Odd-prime clear is the non-Syracuse reuse. Engine `CONTINUE`. Lean `exists_mul_eq_iff_dvd` / `not_dvd_of_abs_gt` / `cycle_constraint_dvd`. No ledger row
- **Refuted ideas:** treating a window miss as IMPOSSIBLE; collapsing WORD and CLASS; seeding Collatz moduli
- **Literature:** integer divisibility and length-one Syracuse candidates **KNOWN**
- **Open:** symbolic class emptiness for composed remainders when \(m\ge 2\)
- **Decision:** PARK (engine `CONTINUE`). Do not auto-continue; do not claim a Collatz result

```text
What was learned
- Exact (A-B)x=C constraints can exclude infinite exponent classes via divisors
- WORD impossibility is not CLASS emptiness; a search miss is UNKNOWN
- Odd-prime clear shows the calculus is not secretly base 2
- Longer words still mostly yield modular conditions on enumerated C
- Digit-fold cores and WeightDrift exclusion are unchanged

Strongest theorem
- exists_mul_eq_iff_dvd and not_dvd_of_abs_gt (Lean); elementary KNOWN arithmetic

Strongest refutation
- y=2x-100 has candidate x=100; absence from the sample window is not an obstruction

Reusable machinery
- research_engine.attacks.control_obstruction; WORD vs CLASS certificates

Prior-art status
- KNOWN length-one cycle divisor lists; NEW GENERIC ENGINE CAPABILITY is class obstruction from certificates

Complexity profile
- unchanged schema; class_count / word_count / certificate_count on evidence

Branch status
- PARK

Why
- The missing constraint-to-obstruction layer exists and proved class-level length-one emptiness where the arithmetic forces it. Syracuse instances are KNOWN. That is not a Collatz solver.

Best next question
- Can class-level obstructions for m≥2 be proved symbolically in the remainder C(k)?
```

## Symbolic multi-step control-word obstructions

- **Date:** 2026-08-25
- **Objective:** Prove infinite class-level impossibility from the symbolic remainder of a multi-step control word, without enumerating words
- **Hypotheses:** Last-control independence of C plus |D|>|C| yields a symbolic class; total length-m emptiness is false on power-clear; r=0 must not be obstructed; Syracuse is only a consumer
- **Major results:** `SYMBOLIC_CLASS` last-k bound (k_min=2 on 2^k y=x+1; k_min=4 on Syracuse m=2). Remainder C=p C_prefix+r A_prefix independent of last k (Lean `last_step_remainder`). Counterexample-first: all length-2 impossible is REFUTED by (1,1). Zero remainder (2^k y=x) is not obstructed. Fingerprint `SYMBOLIC_CLASS`. Engine `CONTINUE`. No ledger row
- **Refuted ideas:** enumerative emptiness billed as symbolic; total m=2 impossibility; last-k class including C=0
- **Literature:** last-step remainder and |D|>|C| divisibility **KNOWN**; generic engine consumption is the capability
- **Open:** recursive remainder / gcd(D,C) when |D| does not dominate
- **Decision:** PARK (engine `CONTINUE`). Do not auto-continue; do not claim a Collatz result

```text
What was learned
- C of a certified power family is independent of the last control
- An infinite last-k class is obstructed by |D|>|C| without enumerating words
- Total length-m emptiness is false whenever a small dividing word exists
- Zero remainder is algebraically consistent, not an obstruction
- Digit-fold cores and WeightDrift exclusion are unchanged; Syracuse is PARK

Strongest theorem
- last_step_remainder and cycle_abs_obstruction (Lean); elementary KNOWN arithmetic

Strongest refutation
- All length-2 words impossible on 2^k y=x+1: witness (1,1)

Reusable machinery
- SYMBOLIC_CLASS certificates; last_k_threshold; ControlWordSummary remainder_independent_of_last

Prior-art status
- KNOWN growth/divisibility; NEW GENERIC ENGINE CAPABILITY is symbolic class obstruction from remainders

Complexity profile
- unchanged schema; symbolic_count / k_min on evidence

Branch status
- PARK

Why
- The engine can now eliminate an infinite multi-step class from a symbolic remainder. The Syracuse instance is known growth. That is not a Collatz solver.

Best next question
- Can a recursive remainder invariant obstruct a class where |D| does not dominate |C|?
```

## Recursive remainder invariants

- **Date:** 2026-08-25
- **Objective:** Discover a recursive remainder invariant that obstructs an infinite class when |D|≤|C|
- **Hypotheses:** Fixed-last elimination D|C ⇒ D|K is generic; magnitude last-k does not apply on last=0; false seed residues are refuted; Syracuse is only a consumer
- **Major results:** RemainderInvariant + RECURSIVE_INVARIANT. Identity b^{k1}C - r D = r p (b^{k1}+p). Synthetics A–F: residue, gcd, odd-prime valuation on five-clear, exceptions (1,0), REFUTED C≡0 mod 4, mixed predicates. Syracuse last-0 with K=12. Fingerprint RECURSIVE_INVARIANT. Engine CONTINUE. Lean two_step_elimination / dvd_constant_of_dvd_remainder. No ledger row
- **Refuted ideas:** seed C≡0 (mod 4) from one prefix; total length-2 emptiness; using |D|>|C| as the proof of these classes
- **Literature:** remainder elimination and D|C ⇒ D|K **KNOWN**; generic engine consumption is the capability
- **Open:** higher-length recurrences that are not a fixed-last constant
- **Decision:** PARK (engine CONTINUE). Do not auto-continue; do not claim a Collatz result

```text
What was learned
- Last k=0 has |D|≤|C| infinitely often, so magnitude last-k does not apply
- The two-step recurrence yields D|C ⇒ D|K with K independent of the prefix
- That class is infinite and not an enumeration
- Seed residue candidates can be false; exceptions such as (1,0) survive
- Digit-fold cores and WeightDrift exclusion are unchanged; Syracuse is PARK

Strongest theorem
- dvd_constant_of_dvd_remainder (Lean); elementary KNOWN arithmetic

Strongest refutation
- C≡0 (mod 4) from prefix k0=1 on 3^k y=x+1 fails at k0=2

Reusable machinery
- RemainderInvariant; RECURSIVE_INVARIANT scope; elimination_constant

Prior-art status
- KNOWN elimination identities; NEW GENERIC ENGINE CAPABILITY is using them when |D|≤|C|

Complexity profile
- unchanged schema; recursive_count on evidence

Branch status
- PARK

Why
- The engine can obstruct an infinite class without magnitude domination. The identity is known. That is not a Collatz solver.

Best next question
- Can a higher-length remainder recurrence yield an invariant that is not a fixed-last constant?
```

## Research Engine v2 first real-problem campaign

- **Date:** 2026-08-25
- **Objective:** Run unmodified v2 against mx+r, 5x+1, Euclidean remainder dynamics, then a score_candidate Target D
- **Hypotheses:** Latent affine-control generalizes across \(T_{m,r}\); same local language need not be the same global regime; valuation-control may transfer to quotient-control
- **Major results:** Every tested odd \((m,r)\) recovers \(2^k y=mx+r\) with EXACT domain and WORD/CLASS/SYMBOLIC_CLASS/RECURSIVE_INVARIANT. \(T_{3,1}\) CLOSE to Syracuse. Seed 27 is a 3-cycle of \(T_5\) (FINITE-HORIZON EXACT) while the odd window still shows net growth (EMPIRICAL). Euclidean 2-D remainder: piecewise_affine inapplicable; exact seed closure size 4; engine CLOSE not ENGINE_LIMITATION; C.1 not built. Target D selected from the scored pool with no override. Lean `mxPlusR_parameter_iff`. No ledger. Digit-fold remains a comparison cluster, except seed-closed mx+r maps are billed as FINITE_CONTRACTING
- **Refuted ideas:** seed 27 is a long mixed trajectory for every \(T_{m,r}\); C.0 Euclidean is ENGINE_LIMITATION as an enum; same local family implies the same core fingerprint
- **Literature:** Crandall 1978, Chamberland 2003, Lagarias 2010, Vallée 2006, Knuth vol. 2. All recovered identities KNOWN
- **Open:** vector census of \(y=A_u x+b_u\)
- **Decision:** PARK

```text
What was learned
- The existing 1-D census chain generalizes across a parameterized mx+r family without map-specific attacks
- Seed-orbit finiteness is treated as numerical contraction, so T_5 at 27 clusters with digit-fold cores
- Euclidean remainder dynamics do not enter the latent-control chain (dimension gate); engine CLOSE from seed gcd closure
- Restricted claimed_capabilities make ExpectedResearchValue identically zero; the default capability list restores ranking
- No new mathematics; the campaign is a multi-domain consumption test

Strongest theorem
- mxPlusR_parameter_iff (Lean); KNOWN padic arithmetic, not a map theorem

Strongest refutation
- 27 is a 3-cycle of T_5; default seed is not a Syracuse-like transient

Reusable machinery
- Hint-free MxPlusRSpec and EuclideanSpec; in-process campaign corpus runner; no new engine attack

Prior-art status
- KNOWN mx+r / 5x+1 / Euclidean algorithm; ENGINE REDISCOVERY of families, domains, and one seed cycle

Complexity profile
- unchanged schema; census/word/obstruction counts on attack evidence

Branch status
- PARK

Why
- The same engine recovered certified affine control on a family of arithmetic maps and failed, for a named generic reason, to transfer that language to Euclidean quotients. That is a capability result, not a theorem program.

Best next question
- Can a reusable vector affine census express control-dependent A_u on Euclidean remainder dynamics and on an unrelated 2-D linear synthetic?
```

## Research Engine v2 generic vector-affine latent control

- **Date:** 2026-08-25
- **Objective:** Smallest generic \(y=A_u x+b_u\) capability; synthetics A–D; Euclidean and unrelated 2-D consumers; Lean compose/cycle/obstruction
- **Hypotheses:** Latent-control methodology transfers from 1-D valuation-controlled affine maps to multi-D matrix-controlled affine maps without Euclidean-specific attacks
- **Major results:** `vector_affine` recovers finite and parameterized matrix branches from I/O; domains EXACT (congruence / valuation / quotient); matrix words compose; class obstruction on shear synthetics; Euclidean recovers \(A_k=((0,1),(1,0))+k((0,0),(0,1))\) with quotient \(k=-\lfloor a/b\rfloor\); parity shear consumes the same attack; Lean `compose_two_vector_affine` / `cycle_of_vector_affine` / `vector_cycle_impossible`; decision treats VECTOR/MATRIX_PARAMETERIZED recovery as novel under MEDIUM delta. No ledger. Identities **KNOWN**
- **Refuted ideas:** global identity on the false-affine trap; tiny-support matrices as family generators; billing `%` rediscovery as new Euclidean mathematics
- **Literature:** Vallée 2006, Knuth vol. 2; matrix affine algebra standard
- **Open:** matrix-word recursive invariants when entrywise magnitude domination fails
- **Decision:** PARK

```text
What was learned
- Scalar piecewise_affine stays 1-D; vector I/O needs a thin sibling attack, not EuclideanControl
- Parameterized matrix families reuse DomainCertificate directions (EXACT after falsify survival)
- Euclidean is a consumer, not a representation boundary once vector census exists
- Generality is evidenced by an unrelated parity-shear map sharing the attack
- No new number theory; the result is an engine-language transfer

Strongest theorem
- compose_two_vector_affine / cycle_of_vector_affine / vector_cycle_impossible (Lean); KNOWN algebra

Strongest refutation
- Trap identity fails outside the sample box; fitted matrices are not Z-theorems

Reusable machinery
- VectorAffineCensus attack; hidden_vector_affine synthetics; affine_control_type fingerprint; Problems.Engine.VectorAffine

Prior-art status
- KNOWN Euclidean / matrix composition; ENGINE REDISCOVERY of A_q and synthetic shears; NEW GENERIC ENGINE CAPABILITY vector_affine

Complexity profile
- unchanged schema

Branch status
- PARK

Why
- Latent control generalizes to vector affine dynamics; Euclid and an unrelated lattice map both consume it; mathematics remains KNOWN. Do not open an Euclidean theorem program.

Best next question
- Can matrix-word recursive invariants obstruct infinite control classes when entrywise magnitude domination fails?
```

## Research Engine v2 matrix-word recursive invariants

- **Date:** 2026-08-25
- **Objective:** Discover recursive \((M_i,c_i)\) invariants that eliminate infinite vector control classes when magnitude is INAPPLICABLE; freeze the attack architecture
- **Hypotheses:** Image-kernel / entry-gcd predicates on composed matrix words transfer the scalar remainder-invariant method without Euclidean-specific code
- **Major results:** `matrix_word_invariant` proves non-magnitude `RECURSIVE_INVARIANT` on shear+vertical-offset classes; gcd/det class obstructions with exceptions; false all-\(k\) invariant REFUTED; zero-offset family UNKNOWN; Euclid and parity-shear consume the attack with no cycle class (zero offset); unrelated lattice walk consumes it. Lean `recursive_matrix_word_step` / `kernel_row_cycle_impossible` / `entry_gcd_divides_translation` / `shear_word_class_impossible`. Attack architecture **FROZEN**. No ledger. Identities **KNOWN**
- **Refuted ideas:** all-parameter lattice candidate on the in-window even-\(k\) trap; “all words impossible” when \(k=\pm 1\) is realizable; magnitude domination as the success criterion
- **Literature:** integer \(Ax=b\) / invariant factors; Knuth / Vallée Euclidean (consumer only)
- **Open:** none at the engine layer
- **Decision:** PARK

```text
What was learned
- Rank-deficient Q-consistent systems need an integer-image test, not only det≠0
- Recurrence must stay inside the control class (odd-length prefixes, not every append)
- Zero-offset Euclidean/parity-shear families have x=0 as a cycle solution; UNKNOWN is correct
- Magnitude INAPPLICABLE is a required label, not an afterthought
- This is the last planned attack; further extensions need a real mathematical failure

Strongest theorem
- shear_word_class_impossible / kernel_row_cycle_impossible / entry_gcd_divides_translation (Lean); KNOWN algebra

Strongest refutation
- False all-k invariant; exception family is not ALL WORDS IMPOSSIBLE

Reusable machinery
- MatrixWordInvariantAttack; hidden_matrix_invariants A–G; Problems.Engine.MatrixWord; capability matrix_word_recursive_invariant

Prior-art status
- KNOWN integer linear algebra; NEW GENERIC ENGINE CAPABILITY matrix_word_invariant; ATTACK ARCHITECTURE FROZEN

Complexity profile
- unchanged schema

Branch status
- PARK

Why
- Recursive non-magnitude class elimination works and is Lean-certified. Mathematics is KNOWN. Freeze the engine and consume a real target next.

Best next question
- Which real mathematical target should the frozen Research Engine v2 consume next?
```

## Frozen Engine campaign: one-variable linear-constraint loops

- **Date:** 2026-08-25
- **Objective:** Run frozen Research Engine v2 against Carelli 2026 one-variable SLCs without adding attacks
- **Hypotheses:** Blind adapters can yield DISCOVERED affine/residue structure; control-word obstructions; the engine stops at the Reachability barrier
- **Major results:** Decrement: adapter-given \(y=x-1\), WORD cycle obstruction, Lean termination. Negation: census UNRESOLVED (sign truncation of \(y=-x\)); control-word stack skipped; 2-cycles only post-run. \(R^+\): DISCOVERED \(3y=4x-1\) and \(3y=4x-2\) on residues 1 and 2 mod 3; CLASS obstructions; empirical halt, not a theorem. Seeded corpus bills all three `FAMILY_SATURATED` against digit-fold cores. ResearchLoop selected `hidden_vector_parity_shear` (`ExpectedResearchValue=0.027`), no override. Lean `rplusRel_*` / `decrement_reaches_zero` / `negation_period2`. Quotient deadlock fix (partial `legal_controls`). No ledger. No new attack
- **Refuted ideas:** monotone descent / one-step contraction on \(R^+\); complete census of the involution \(x\mapsto -x\); seed closure as map contraction
- **Literature:** Carelli 2026; Matthews–Watts 1984; Möller 1978; Braverman 2006; Tiwari 2004; Hosseini–Ouaknine–Worrell 2019; Ben-Amram et al. 2025 survey. All recovered identities KNOWN
- **Open:** Reachability for \(\lfloor 4x/3\rfloor\); named census limitation not implemented
- **Decision:** PARK

```text
What was learned
- From the inequalities of Carelli's R+ alone, v2 reconstructed two residue-selected affine branches and class cycle obstructions
- That is reconstruction of generalized-Collatz language, not a termination theorem
- Sign-first census truncation blocks the obvious involution x'=-x, so Carelli's length-(<=2) theorem is not an engine rediscovery
- Seed-orbit finiteness again bills expanding maps as FINITE_CONTRACTING
- One correctness fix: Mealy quotient respects deadlock; no new attack

Strongest theorem
- rplusRel_unique / rplusRel_clear / rplusRel_ediv and decrement_reaches_zero (Lean); KNOWN

Strongest refutation
- R+ is not monotone; y=-x is not a complete engine census

Reusable machinery
- Hint-free OneVariableLoopSpec; in-process frozen campaign runner; scout kept off the adapter

Prior-art status
- KNOWN Carelli / Matthews–Watts / affine SLC decidability; ENGINE REDISCOVERY of the R+ integer graph; ENGINE_LIMITATION on the involution census

Complexity profile
- unchanged schema

Branch status
- PARK

Why
- The frozen stack recovered conceptually relevant intermediate structure on a 2026 SLC target and failed, for a named generic reason, to certify a global involution. Mathematics remains KNOWN. Do not implement the census fix; do not attack Reachability.

Best next question
- Can the frozen 1-D census consume a genuinely nondeterministic one-variable SLC, where legal_controls is not a singleton?
```

## Frozen Engine campaign phase 2: nondeterministic one-variable SLC

- **Date:** 2026-08-25
- **Objective:** Test whether frozen v2 can reason about a one-variable linear-constraint loop when several transitions are legal from the same state, without adding nondeterministic machinery
- **Hypotheses:** Fingerprint/closure already see branching; PiecewiseAffineCensus and ControlWord may not; ∃ vs ∀ must not collapse
- **Major results:** Synthetics A–E: census inapplicable, `BRANCHING` fingerprint, quantifier probes distinguish `EXISTENTIAL_WITNESS` / `REFUTED` / `CERTIFIED_ON_WINDOW` / `UNKNOWN`. Real target `slc_sum_strip` (\(-1\le x+x'\le 1\)): census/word/obstruction skipped; closure truncated; ∃ cycle witnessed; ∀ termination `REFUTED`; ∀ paths cycle `UNKNOWN`; ResearchLoop `CONTINUE` (trivial identity separation). Lean `sumStripRel_*` / cycle witnesses. No new attack. No census fix
- **Refuted ideas:** overlapping-domain census as a frozen capability; silent promotion of truncation to a universal refutation; collapsing ∃ cycle into ∀ paths cycle
- **Literature:** Carelli 2026 Lemma 5.33 / Theorem 3.20. Affine slices and length-(\(\le 2\)) cyclic-trace theorem remain **KNOWN**, not engine rediscovery
- **Open:** parked singleton-census gate; start-local Mealy alphabet; spanning-tree closure witnesses; Phase-1 involution census
- **Decision:** PARK

```text
What was learned
- legal_controls with cardinality >1 is visible to fingerprint, magnitude probes, and closure BFS
- The frozen 1-D census requires a singleton at the start state, so overlapping affine branches are never recovered and never falsely partitioned
- ControlWord and control_obstruction never run; there is no legal-word language L_m(x)
- Post-run probes can keep EXISTENTIAL_WITNESS distinct from universal claims; truncation is UNKNOWN, not a refutation
- Carelli's three-slice strip and length-(<=2) theorem were not rediscovered by the engine

Strongest theorem
- sumStripRel_all / sumStrip_cycle_zero_one (Lean); KNOWN existential facts about the adapter relation

Strongest refutation
- Universal termination of the sum strip; the claim that the frozen census can represent overlapping legal domains

Reusable machinery
- RelationLoopSpec (successor-as-control); hidden synthetics A–E; quantifier_report (campaign probe, not an attack)

Prior-art status
- KNOWN Carelli Lemma 5.33; ENGINE_LIMITATION on singleton census / start-local Mealy alphabet; no new mathematics

Complexity profile
- unchanged schema

Branch status
- PARK

Why
- The experiment answered how far deterministic latent-control machinery already reaches into nondeterminism: diagnosis yes, 1-D control language no. Do not thaw the architecture.

Best next question
- Which other frozen-engine mathematical target should be consumed next, leaving the parked SLC limitations untouched?
```

## Frozen Engine campaign: BB-5 generalized Collatz map

- **Date:** 2026-08-25
- **Objective:** Run frozen Research Engine v2 on Michel's BB-5 map B without adding attacks, without proving BB(5) or Collatz
- **Hypotheses:** Blind adapter yields DISCOVERED residue-selected affine branches; control-word CLASS obstructions; engine stops short of universal convergence
- **Major results:** DISCOVERED \(3y=5x+18\) on \(x\equiv 0\pmod{3}\) and \(3y=5x+22\) on \(x\equiv 1\pmod{3}\); domains EXACT; 14 control words; mixed length-2/3 CLASS obstructions; length-1 candidates \(x=-9,-11\) outside \(n\ge 0\); exact seed-0 closure of size 15 ending at 12284. Isolated decision CONTINUE; seeded FAMILY_SATURATED. Lean `bRel_*`. No ledger. No new attack
- **Refuted ideas:** monotone descent; one-step contraction; seed closure as map contraction; identifying seed-0 halt with BB(5) or with \(\forall n\,B\) terminates
- **Literature:** Michel 1993/2015; Yolcu–Aaronson–Heule 2023; Aaronson 2020; bbchallenge 2025. All recovered identities KNOWN
- **Open:** universal convergence of B on N; parked fingerprint coarseness
- **Decision:** PARK

```text
What was learned
- From the exact partial relation 3y in {5n+18, 5n+22} alone, v2 reconstructed two residue-selected affine branches and class cycle obstructions
- That is reconstruction of Michel's language, not a BB-5 or Collatz theorem
- Mixed control words can be realizable as paths and impossible as cycles; the engine kept that distinction
- Seed-0 finite closure is the published champion trajectory and is not universal termination
- Seed-orbit finiteness again bills an expanding 5/3 map as FINITE_CONTRACTING

Strongest theorem
- bRel_unique / bRel_undefined_two / bRel_not_fixed (Lean); KNOWN

Strongest refutation
- B is not monotone; finite seed closure is not contraction

Reusable machinery
- Hint-free PartialFiveThreeSpec; in-process frozen campaign runner; scout kept off the adapter

Prior-art status
- KNOWN Michel / Yolcu–Aaronson–Heule / bbchallenge; ENGINE REDISCOVERY of the integer graph of B; no new mathematics

Complexity profile
- unchanged schema

Branch status
- PARK

Why
- The frozen stack recovered conceptually relevant intermediate structure on a contemporary Collatz-adjacent target and correctly stopped at the known convergence barrier. Do not prove totality of B.

Best next question
- Which other frozen-engine mathematical target should be consumed next, leaving parked fingerprint coarseness and the open convergence of B untouched?
```

## Frozen Engine campaign: aliquot dynamics

- **Date:** 2026-08-25
- **Objective:** Stress-test frozen v2 on A(n)=sigma(n)-n, including open seed 276, without new attacks
- **Hypotheses:** Affine census will fail; known small cycles/termination appear as exact closures; 276 remains unresolved; ENGINE_LIMITATION is the honest diagnosis
- **Major results:** Census UNRESOLVED on all seeds. 12: exact halt to 0. 6: 1-state closure. 220: 2-state closure. 276: ENGINE_LIMITATION, mixed magnitude, closure cap 32, prefix 276,396,696,1104,1872,3770 matches A008892; no fate claimed. Descent REFUTED at 12. Lean properDivisorSum_*. No new attack. ResearchLoop next un-overridden
- **Refuted ideas:** global A(n)<n; seed closure as contraction; treating 276 truncation as infinitude or termination
- **Literature:** Guy–Selfridge 1975; Erdős 1976; te Riele 1999; OEIS A008892. All identities KNOWN
- **Open:** fate of 276; Catalan–Dickson; parked affine-language limitation
- **Decision:** PARK (engine: ENGINE_LIMITATION on 276)

```text
What was learned
- Factorization-dependent A(n) is outside the frozen affine/valuation attack language
- Known small recurrent seeds still appear as exact finite closures
- 276's opening trajectory is recomputed exactly within budget; its fate is not
- ENGINE_LIMITATION is the correct flagship diagnosis, not a failed experiment

Strongest theorem
- properDivisorSum_prime / properDivisorSum_six / properDivisorSum_220_284 (Lean); KNOWN

Strongest refutation
- A(12)=16; finite seed closure is not contraction

Reusable machinery
- Budgeted SigmaMinusNSpec with TRANSITION_UNRESOLVED; scout kept off the adapter

Prior-art status
- KNOWN aliquot lore; ENGINE_LIMITATION on piecewise-affine cover; no new mathematics

Complexity profile
- unchanged schema

Branch status
- PARK

Why
- The experiment answered the boundary question: existing machinery diagnoses and closes tiny known orbits, and cannot consume divisor-sum dynamics. Do not add an aliquot attack.

Best next question
- Which frozen-engine target still lies inside the existing attack language, now that this arithmetic boundary is recorded?
```

## Frozen Engine campaign: open order-6 Skolem instance

- **Date:** 2026-08-25
- **Objective:** Test whether frozen v2 can make progress on the 2026 survey's unresolved order-6 integer LRS using only existing vector/matrix/reachability machinery
- **Hypotheses:** Companion matrices are recovered in dimension 2; easy zeros are certified; the order-6 instance remains UNKNOWN; the frozen 3-point census cannot consume dimension ≥ 3
- **Major results:** Dim-2 recovered exact companions \(((0,1),(-2,3))\), \(((0,1),(1,1))\), \(((0,1),(-1,0))\). Zeros at indices 3 and 1. Order-3 census UNRESOLVED. Order-6 vector census COMPUTATION_EXHAUSTED (\(25^6\)). Prefix 12,49,374,6003,21520,150773; first negative \(u_{11}\); no zero on \(\{0,\ldots,64\}\). No modular exclusion. Lean companion_shift_*. No new attack. ResearchLoop next un-overridden
- **Refuted ideas:** flagship fixed sign (counterexample \(n=11\)); finite zero-search as non-existence; seed-zero closure as contraction
- **Literature:** Bacik et al. 2026 survey sequence (13); Lipton et al. 2022; Luca–Ouaknine–Worrell 2026; Kenison et al. 2025 order 4. All identities KNOWN
- **Open:** whether survey (13) vanishes; parked vector-census dimensional barrier
- **Decision:** PARK (flagship ResearchDecision CLOSE; engineering ENGINE_LIMITATION of the census)

```text
What was learned
- Frozen vector_affine recovers exact 2-D companions from I/O, including the easy Skolem calibrations
- The same census cannot determine a 3x3 matrix (3-point fit) and cannot even be run in dimension 6 (25^d cube)
- Representation fit is not research leverage: the order-6 instance stays UNKNOWN
- NO ZERO FOUND on {0,...,64} is a finite-range check, not the literature 10^1000 certificate and not non-existence
- Stopping at a zero is again billed FINITE_CONTRACTING

Strongest theorem
- companion_shift_positive_step / companion_shift_zero_small_third / companion_shift_order6_eleventh_negative (Lean); KNOWN

Strongest refutation
- flagship first coordinate is not of fixed sign (u_11 < 0); 3-point vector census is not a Z^d theorem for d>=3

Reusable machinery
- Hint-free CompanionShiftSpec; budgeted skip of the exponential census cube; scout kept off the adapter

Prior-art status
- KNOWN Skolem lore; ENGINE REDISCOVERY of 2-D companions; no new mathematics

Complexity profile
- unchanged schema

Branch status
- PARK

Why
- The experiment answered the yield question: the affine/matrix language already fits, but frozen v2 does not produce a new invariant, exclusion, or decision on the open order-6 instance. Do not add a Skolem attack.

Best next question
- Which frozen-engine target still lies inside the existing low-dimensional affine language, now that this high-dimensional census barrier is recorded?
```

## Research Engine v2.2: research memory

- **Date:** 2026-08-25
- **Objective:** Persist accumulated experiment history as classified research knowledge without adding attacks or contaminating blind discovery
- **Hypotheses:** Failures cluster by mathematical signature; known rediscoveries stay non-novel; `score_candidate` is unchanged unless memory is passed
- **Major results:** `research_engine.memory` (`MemoryExperiment`, `FailureRecord`, `GreyLoot`, `MathematicalYield`, `ResearchMemory`). Historical seed covers digit-fold, Syracuse, Euclidean/vector, matrix-word, nondeterministic SLC, involution census (not implemented), Carelli \(R^+\), BB-5, aliquot, Skolem order 6, and the `skolem_lrs` identifier hygiene false positive. Global-reachability cluster emits `PROMOTE_TO_NEXT_VERSION` as guidance only. No new attack. No Lean. Package 0.2.2
- **Refuted ideas:** treating `skolem_lrs` as a literature leak; a single failure justifying a new attack; silent grey-loot injection into `BlindPacket`
- **Literature:** none new; historical campaigns remain KNOWN / PARK as in their dossiers
- **Open:** which cluster, if any, later justifies a v2.3 abstraction from evidence rather than intuition
- **Decision:** PROMOTE (memory layer enters the platform; attack stack stays frozen)

```text
What was learned
- Failed attacks are reusable evidence about the boundary of the current language
- Representation novelty and mathematical novelty must be scored independently
- Grey loot survives finalization; scout knowledge stays off the attack lane
- Recurring GLOBAL_REASONING failures (Skolem, R+, BB-5) are the leading v2.3 candidate and were not implemented
- ExpectedResearchValue is unchanged when no memory store is supplied

Strongest theorem
- none; this is engine methodology

Strongest refutation
- identifier token skolem_lrs is not a literature leak (EXPERIMENT_HYGIENE, resolved)

Reusable machinery
- research_engine.memory; optional ResearchLoop(memory=...); FailureLearningValue

Prior-art status
- KNOWN historical campaigns; no new mathematics

Branch status
- PROMOTE

Why
- The layer answers the v2.2 question: history can be persistent research intelligence without expanding the attack surface or contaminating blind discovery.

Best next question
- Which frozen-engine target still teaches something new about an unresolved high-value failure cluster?
```

## Research Engine v2.2: research target board

- **Date:** 2026-08-25
- **Objective:** Turn experimental history into research memory, grey loot, a ranked target portfolio, and a prior-art map without new attacks
- **Hypotheses:** Recurring failures cluster by mathematical meaning; ExpectedResearchValue with FailureLearningValue can rank a mixed portfolio; blind packets can stay free of scout conclusions
- **Major results:** `ResearchTarget` board (~17 candidates, three pools), enriched historical `GreyLoot`, named failure clusters, engineering candidates as guidance only, prior-art dossiers, hint-free `BlindPacket`s, protocol campaign order known → frontier → wildcard → ResearchLoop pick. No new attack. No adapters for unrun targets. No Lean.
- **Refuted ideas:** inventing EV scores to force an order; treating a single failure as an implementation instruction; injecting scout conclusions into attack-lane packets
- **Literature:** existing campaign sources plus `oeis-A037274`, `oeis-A007320`; no novelty claimed from keywords
- **Open:** the first computed frontier target after calibration
- **Decision:** PROMOTE (board enters the platform as intelligence, not as theorems)

```text
What was learned
- Historical lessons can be stored as grey loot with transfer targets and status
- Global reachability, quantifier mismatch, and non-affine arithmetic recur across distinct names
- Representation novelty and mathematical novelty stay independent
- Calibration targets should run first even when EV is tiny
- A ResearchLoop pick is computed from leftovers, not chosen by taste

Strongest theorem
- none; this is engine methodology

Strongest refutation
- none new; historical counterexamples preserved as loot

Reusable machinery
- ResearchTarget, PriorArtDossier, NamedFailureCluster, assemble_board, recommend_campaign_order

Prior-art status
- KNOWN historical campaigns; frontier open questions cited, not claimed

Branch status
- PROMOTE

Why
- v2.2 can now start a frozen-engine campaign from a ranked map of what failed and what remains open, without another scouting round and without expanding the attack surface.

Best next question
- What exact intermediate theorem or obstruction can frozen v2 produce on the first frontier target in the computed campaign order?
```

## Frozen Engine campaign: open order-10 LRS Positivity instance

- **Date:** 2026-08-25
- **Objective:** Test whether frozen v2 + v2.2 memory can make progress on the 2026 survey's unresolved order-10 integer LRS Positivity instance, and whether that failure is the same `GLOBAL_REASONING` cluster as Skolem
- **Hypotheses:** Companion matrices are recovered in dimension 2; easy negatives are certified; a finite negative prefix is distinguished from nonnegativity from \(n=0\); the order-10 instance remains UNKNOWN; Positivity half-space safety fails for the same finite-to-infinite gap as Skolem hyperplane reachability
- **Major results:** Dim-2 recovered exact companions \(((0,1),(1,1))\), \(((0,1),(-1,0))\). Negatives at indices 1 and 2. Order-3 census UNRESOLVED. Order-10 vector census COMPUTATION_EXHAUSTED (\(25^{10}\)). Prefix 35,574,34592,...; no negative on \(\{0,\ldots,64\}\). Orthant invariance holds on A and fails on the flagship last row. Lean companion_obs_*. Memory ingest joins the existing `GLOBAL_REASONING` cluster. ResearchLoop next un-overridden (`hidden_congruence_a`). No new attack
- **Refuted ideas:** flagship nonnegative orthant invariant; finite nonnegative window as universal Positivity; eventual nonnegative tail as Positivity from \(n=0\); a new `ORDERED_VECTOR_INVARIANTS` capability merely because the property is a half-space
- **Literature:** Bacik et al. 2026 survey sequence (16); Ouaknine–Worrell 2014 order \(\le 5\) and simple order \(\le 9\). All identities KNOWN
- **Open:** whether survey (16) is nonnegative for every \(n\); parked vector-census dimensional barrier
- **Decision:** PARK (campaign label ENGINE_LIMITATION; flagship ResearchDecision CLOSE)

```text
What was learned
- Frozen vector_affine recovers exact 2-D companions from I/O, including easy sign calibrations
- Accepting at a negative observation certifies NEGATIVE_WITNESS and distinguishes D from A
- The same census cannot determine a 3x3 matrix and cannot be run in dimension 10
- CERTIFIED_ON_WINDOW on {0,...,64} is not the literature 10^6 bound and not universal nonnegativity
- Skolem GLOBAL_REASONING and Positivity GLOBAL_REASONING share the cluster key finite_to_infinite_certificate

Strongest theorem
- companion_obs_nonneg_small_step / companion_obs_early_negative_first / companion_obs_order10_step (Lean); KNOWN

Strongest refutation
- nonnegative orthant is not invariant for the flagship last row; a later nonnegative tail is not positivity from n=0

Reusable machinery
- Hint-free CompanionObsSpec; v2.2 ingest of the flagship into the existing global-reachability cluster; scout kept off the adapter

Prior-art status
- KNOWN Positivity lore; ENGINE REDISCOVERY of 2-D companions; no new mathematics

Complexity profile
- unchanged schema

Branch status
- PARK

Why
- Representation fits. The infinite half-space safety property does not. Changing existential hyperplane reachability into universal half-space safety did not create a new frozen-engine capability. Do not add a Positivity attack.

Best next question
- Which frozen-engine target still lies inside the existing low-dimensional affine language, now that both Skolem and Positivity have recorded the same finite-to-infinite gap?
```

## Frozen Engine campaign: switching affine Z^2 origin

- **Date:** 2026-08-25
- **Objective:** Test whether frozen v2 + v2.2 memory can cash out existing low-dimensional affine attacks on the stored two-path integer loop, without re-entering the `GLOBAL_REASONING` cluster
- **Hypotheses:** Vector census recovers the two declared pieces; origin from \((3,2)\) is not a finite witness; a class obstruction on \(\mathbb N_0^2\) is elementary from preimages; this is not Skolem/Positivity
- **Major results:** `FINITE_CENSUS` of \((x+y,y-1)\) and \((x-1,x+y)\). Image-kernel matrix-word CLASS cycle obstruction on a 2-letter alphabet. Closure incomplete (cap 32). Origin absent from the truncated union. Lean `two_path_nonneg_never_origin`: nonnegative non-origin states never reach \((0,0)\). Planner unchanged with memory. Next leftover pick `cyclic_tag_bit` (un-overridden). No new attack
- **Refuted ideas:** \((3,2)\) reaches the origin on the bound; every small nonnegative seed reaches the origin; no period-2 orbit; truncated BFS is a global basin; this failure belongs in `GLOBAL_REASONING`
- **Literature:** Ben-Amram–Genaim–Ouaknine–Worrell 2025 survey; Hosseini–Ouaknine–Worrell 2019 affine SLC. All identities KNOWN
- **Open:** termination on all of \(\mathbb Z^2\); origin on \(\mathbb N_0^2\) is classified
- **Decision:** CLOSE (engine `CONTINUE` on the finite census; statements are all KNOWN)

```text
What was learned
- Frozen vector_affine recovers the two stored switching pieces as a FINITE_CENSUS
- matrix_word_invariant emits an image-kernel cycle obstruction; that is not an origin theorem
- Scalar control_word / control_obstruction stay inapplicable on this dummy-control packet
- N^2 origin-avoidance is a finite preimage fact, certified in Lean, not an infinite-time barrier
- Truncated residual BFS (size 33, incomplete) is not a basin and not infinitude

Strongest theorem
- two_path_nonneg_never_origin (Lean); KNOWN

Strongest refutation
- (3,2) does not reach (0,0); (1,0)<->(0,1) is a 2-cycle disjoint from the origin

Reusable machinery
- Hint-free TwoPathZ2Spec; v2.2 ingest that does not join GLOBAL_REASONING; scout kept off the adapter

Prior-art status
- KNOWN two-path arithmetic; ENGINE REDISCOVERY of the two affine pieces; no new mathematics

Complexity profile
- unchanged schema

Branch status
- CLOSE

Why
- The existing stack cashed the representation and an elementary class obstruction. Every statement is KNOWN. Do not add a switching-affine attack.

Best next question
- What representation mismatch, if any, does the un-overridden leftover pick cyclic_tag_bit still teach?
```

## Frozen Engine campaign: order-2 companion known zero

- **Date:** 2026-08-25
- **Objective:** Execute `CampaignOrder.research_loop_pick` without override: the leftover competence check `skolem_order2_known_zero`
- **Hypotheses:** Frozen v2 still recovers the 2-D companion and the index-3 zero; ingest must not dump a `ZERO_WITNESS` into `GLOBAL_REASONING`
- **Major results:** Board pick confirmed. `FINITE_CENSUS` recovers \(M=((0,1),(-2,3))\). Closure complete, size 4. First coordinate vanishes at index 3. Lean `companion_shift_zero_small_third` reused. Planner unchanged with memory. Next leftover pick `cyclic_tag_bit` (un-overridden). No new attack. No new Lean
- **Refuted ideas:** the first coordinate never vanishes on the bound; this calibration belongs in `GLOBAL_REASONING`; the board pick should be replaced by a frontier target
- **Literature:** Kenison et al. 2025 order-4 completeness; Bacik et al. 2026 survey. All identities KNOWN
- **Open:** none for this window; order-6 vanishing remains parked
- **Decision:** CLOSE (engine `CONTINUE` on the finite census; statements are all KNOWN)

```text
What was learned
- assemble_board leftover pick can be an already-run calibration; the protocol still runs it
- Frozen vector_affine recovers the declared order-2 companion as a one-branch FINITE_CENSUS
- Exact residual closure of size 4 is a ZERO_WITNESS, not an infinite-time theorem
- Memory-aware EV may boost this target because it resembles GLOBAL_REASONING; ingest must not follow that resemblance
- Planner output is unchanged with memory=ResearchMemory()

Strongest theorem
- companion_shift_zero_small_third (existing Lean); KNOWN

Strongest refutation
- first coordinate vanishes at index 3; this is not the order-6 global cluster

Reusable machinery
- Hint-free companion_shift_order2 wrapper around CompanionShiftSpec; v2.2 ingest that does not join GLOBAL_REASONING

Prior-art status
- KNOWN order-2 zero; ENGINE REDISCOVERY of the companion; no new mathematics

Complexity profile
- unchanged schema

Branch status
- CLOSE

Why
- The board asked for a competence check. Frozen v2 still finds the companion and the finite zero. Every statement is KNOWN. Do not add a Skolem attack.

Best next question
- What representation mismatch, if any, does the un-overridden leftover pick cyclic_tag_bit still teach?
```

## Research Engine v2.3 Phase 1: research strategy

- **Date:** 2026-08-26
- **Objective:** Turn frozen v2.2 memory and the 0.2.1 attack stack into ranked falsifiable hypotheses and opt-in attack chains, without new attacks
- **Hypotheses:** Evidence-backed `ResearchHypothesis` records plus a capability graph can replace flood-order planning on stated research goals; known rediscoveries stay tagged known
- **Major results:** Historical memory regenerates Syracuse / Carelli \(R^+\) / switching-affine / matrix-word statements as known hypotheses. `StrategyPlanner` rediscovers `piecewise_affine → parameter_domain → control_word → control_obstruction` and runs fewer attacks than flood order. Default `AttackPlanner` / `ResearchLoop` unchanged. Hypotheses do not cross `BlindPacket`s. Phases 2–4 gated
- **Refuted ideas:** a planted singleton invariant on the hidden sign map; flood-order as the only orchestration; known loot billed as novel
- **Literature:** engine methodology; historical campaigns remain KNOWN as in their dossiers
- **Open:** whether a replayed real target yields a `PROOF_READY` inductive or ranking obligation (Phase 2 gate)
- **Decision:** PROMOTE Phase 1 as laboratory intelligence. Do not add attacks. Do not open Phases 2–4

```text
What was learned
- Grey loot and exact artifacts already contain ranked, falsifiable research statements
- The historically successful census→domain→control-word→obstruction chain can be selected, not merely encoded as named-run prerequisites
- Counterexample-first leak attacks refute false invariants without a new solver
- Blindness extends from grey loot to hypotheses: source_target A is not a predicate for B
- Global reasoning, law/domain split, and quantifiers remain gated

Strongest theorem
- none; engine methodology only

Strongest refutation
- S={(0,)} is not invariant for the hidden sign map

Reusable machinery
- research_engine.strategy (ResearchHypothesis, AttackChain, StrategyPlanner); optional ResearchMemory.hypotheses

Prior-art status
- KNOWN rediscoveries regenerated; no new mathematics

Complexity profile
- unchanged schema

Branch status
- PROMOTE (Phase 1 only)

Why
- The engine can now ask which chain to run and which evidence-backed hypothesis to falsify, without thawing the attack stack.

Best next question
- Does a replayed real target produce a PROOF_READY obligation T(S)⊆S or V(T(x))<V(x)?
```

## Research Engine v2.3 Phase 2: global reasoning

- **Date:** 2026-08-26
- **Objective:** Add a generic inductive/ranking layer that wraps existing envelope and leak attacks, producing intermediate T(S)⊆S / V(T(x))<V(x) certificates on the GLOBAL_REASONING cluster without becoming a Skolem, Positivity, or Collatz solver
- **Hypotheses:** Bounded CEGIS over a four-form region catalog plus a fixed ranking catalog can certify known calibrations and refuse to bill finite closure as a universal theorem
- **Major results:** `research_engine.reasoning` (`EvidenceState`, `InvariantCertificate`, `RankingCertificate`, bounded CEGIS, ranking reconnaissance). Two-path Z^2 nonnegative orthant is `INDUCTIVE_CERTIFIED` (known). Decrement ranking is `RANKING_CERTIFIED` (known). Carelli / Skolem order-2 / positivity small companion stay below `UNIVERSAL_THEOREM`. Opt-in chain `global_inductive`; `DEFAULT_ATTACK_ORDER` unchanged; `ENGINE_STRATEGY_VERSION` stays 0.2.3; `ENGINE_REASONING_VERSION = 0.2.4`. Phases 3–4 gated
- **Refuted ideas:** finite complete closure as `UNIVERSAL_THEOREM`; Phase 1 `PROOF_READY` control-obstruction as an inductive certificate; flood-order mutation as the vehicle for global reasoning
- **Literature:** engine methodology; Two-path N^2 and decrement ranking remain KNOWN rediscoveries
- **Open:** whether law candidates can be separated from domain partition without touching `infer_region` (Phase 3 gate)
- **Decision:** PROMOTE Phase 2 as laboratory intelligence. Do not add flood attacks. Do not open Phases 3–4

```text
What was learned
- True T(S)⊆S is distinct from AffineInvariantAttack live-slice leak search
- A four-form catalog plus four CEGIS rounds is enough to rediscover N^2 invariance and decrement ranking
- Evidence states stop finite BFS from being billed as a universal theorem
- Carelli / Skolem / positivity calibrations can be replayed as diagnostics without becoming solvers
- global_inductive can sit on StrategyPlanner without mutating DEFAULT_ATTACK_ORDER

Strongest theorem
- none; engine methodology only (known calibrations tagged KNOWN_REDISCOVERY)

Strongest refutation
- complete finite closure is not UNIVERSAL_THEOREM; cluster replays are not solvers

Reusable machinery
- research_engine.reasoning (analyze, InvariantCertificate, RankingCertificate, EvidenceState); opt-in global_inductive chain

Prior-art status
- KNOWN rediscoveries on TwoPathZ2 and slc_decrement; no new mathematics

Complexity profile
- unchanged schema

Branch status
- PROMOTE (Phase 2 only)

Why
- The engine now has an intermediate certificate between finite exact structure and a universal theorem, without thawing the attack stack or opening a target-specific solver.

Best next question
- Can law candidates be separated from domain partition without touching infer_region?
```

## Research Engine v2.3 Phase 3: law ⊥ domain

- **Date:** 2026-08-26
- **Objective:** Certify affine laws independently of region partition, so LAW_CERTIFIED may precede DOMAIN_CERTIFIED, without mutating infer_region or completing the parked involution census
- **Hypotheses:** `_candidate_lines` already contains the law; sign-first `infer_region` is a later, possibly truncated, domain attachment
- **Major results:** `research_engine.law` (`AffineLaw`, `DomainAttachment`, `LawEvidence`, `DomainEvidence`). Negation \(y=-x\) is `LAW_CERTIFIED` (known) with `DOMAIN_TRUNCATED`; flood census stays `UNRESOLVED`. Decrement \(y=x-1\) may certify law and sample domain together; flood `FINITE_CENSUS` unchanged. Opt-in chain `law_domain` only when memory carries `DOMAIN_INFERENCE`. `infer_region` sign-first order unchanged. `ENGINE_LAW_VERSION = 0.2.5`. Phase 4 gated
- **Refuted ideas:** completing the involution census as the Phase-3 vehicle; `LAW_CERTIFIED` as `FINITE_CENSUS`; truncated sign region as `DOMAIN_CERTIFIED`; Carelli length-≤2 as an engine rediscovery from \(y=-x\)
- **Literature:** engine methodology; affine involution and decrement remain KNOWN rediscoveries
- **Open:** overlapping nondeterministic branches / quantifier semantics (Phase 4 gate)
- **Decision:** PROMOTE Phase 3 as laboratory intelligence. Do not add flood attacks. Do not implement the involution census. Do not open Phase 4

```text
What was learned
- Affine laws can be extracted from exact I/O before infer_region attaches a domain
- Sign-first truncation is a domain failure, not a missing law
- LAW_CERTIFIED must not rewrite an UNRESOLVED flood census
- law_domain can sit on StrategyPlanner without stealing census_obstruction when memory is absent
- The parked involution regression remains a calibration, not a census-fix ticket

Strongest theorem
- none; engine methodology only (known calibrations tagged KNOWN_REDISCOVERY)

Strongest refutation
- y=-x on a truncated sign region is not a complete finite census and not Carelli length-≤2

Reusable machinery
- research_engine.law (analyze, AffineLaw, DomainAttachment); opt-in law_domain chain; candidate_affine_laws export

Prior-art status
- KNOWN rediscoveries on slc_negation and slc_decrement; no new mathematics

Complexity profile
- unchanged schema

Branch status
- PROMOTE (Phase 3 only)

Why
- The engine can now state a sample-certified affine law when the region partition is incomplete, without thawing infer_region or claiming a Z-cover.

Best next question
- Can overlapping nondeterministic branches be consumed without a new deterministic control language?
```

## Research Engine v2.3 Phase 4: EXISTS_PATH ≠ ALL_PATHS

- **Date:** 2026-08-26
- **Objective:** Treat legal_controls × transition as R ⊆ X×X and keep EXISTS_PATH ≠ ALL_PATHS as engine evidence, without a new flood attack, overlapping-domain census, or nondeterministic SLC solver
- **Hypotheses:** successor-as-control already is a relation; campaign quantifier_report already distinguishes ∃/∀; lifting that discipline into research_engine is methodology, not a number-theory theorem
- **Major results:** `research_engine.quantifiers` (`PathQuantifier`, `PathStatus`, `RelationEdge`, `PathClaim`, `QuantifierReport`). Stay-or-decrement: ∃ cycle `EXISTENTIAL_WITNESS`, ∀ paths cycle `UNKNOWN`, ∀ terminate `REFUTED`. Two-affine replays the same split; census still skipped. Dual-decrement window-certifies termination; truncation stays `UNKNOWN`. Sum-strip is a parked diagnostic, not Carelli length-≤2. Opt-in chain `quantifier_probe` only when memory carries `QUANTIFIER`. `ENGINE_QUANTIFIER_VERSION = 0.2.6`. Phases 1–3 versions unchanged. v2.3 complete
- **Refuted ideas:** ∃ cycle as ∀ paths cycle; `NO_PATH_FOUND` as nonexistence; `CERTIFIED_ON_WINDOW` as a Z-theorem; overlapping-domain census as the Phase-4 vehicle; Carelli length-≤2 as an engine rediscovery
- **Literature:** engine methodology; stay-or-decrement, two-affine, and sum-strip remain KNOWN rediscoveries
- **Open:** none for a Phase 5; overlapping-domain census and a nondeterministic control-word solver stay PARK
- **Decision:** PROMOTE Phase 4 as laboratory intelligence. Do not add flood attacks. Do not implement overlapping-domain census. Do not thaw branching_quantifier. Do not open Phase 5

```text
What was learned
- legal_controls × transition is already R ⊆ X×X; the missing piece was engine-owned ∃/∀ status
- An existential cycle does not certify all_paths_cycle; Phase 0 leaves the latter UNKNOWN
- NO_PATH_FOUND is a search report, not a nonexistence theorem
- CERTIFIED_ON_WINDOW is not a Z-theorem; shrinking the cap must yield UNKNOWN, not REFUTED
- quantifier_probe can sit on StrategyPlanner without stealing census_obstruction, global_inductive, or law_domain when QUANTIFIER memory is absent

Strongest theorem
- none; engine methodology only (known calibrations tagged KNOWN_REDISCOVERY)

Strongest refutation
- stay-or-decrement has a stay cycle and does not universally terminate; that is not ∀ paths cycle

Reusable machinery
- research_engine.quantifiers (analyze, relation_edges, bounded probes); opt-in quantifier_probe chain

Prior-art status
- KNOWN rediscoveries on stay-or-decrement, two-affine, and sum-strip; no new mathematics

Complexity profile
- unchanged schema

Branch status
- PROMOTE (Phase 4; v2.3 program complete)

Why
- The engine can now state EXISTS_PATH ≠ ALL_PATHS on branching specs without teaching the census to accept overlapping domains or adding a nondeterministic solver.

Best next question
- none from this program; parked clusters stay parked
```

## Research Campaign 01: mx_plus_r_7x1_class_obstruction

- **Date:** 2026-08-26
- **Objective:** Extract a nontrivial class obstruction for \(T(x)=(7x+1)/2^{v_2(7x+1)}\) relevant to reaching 1, using frozen Research Engine v2.3 without new attacks
- **Hypotheses:** residue/valuation control might exclude an infinite family from the basin of 1; family rediscovery is not the yield
- **Major results:** Blind `StrategyPlanner(CYCLE_EXCLUSION)` selected `census_obstruction` and recovered \(2^k y=7x+1\). Exact image theorem: \(T(n)\equiv 1,2,\) or \(4\pmod 7\). Complementary classes are not basin-excluded: \(T(73)=1\) and \(T(299593)=1\). Only positive length-one cycle is \(1\). Seed \(3\) misses \(1\) on horizons 16 and 32 (not divergence). Lean in `Problems.Engine.MxPlusR`. No new attacks
- **Refuted ideas:** rediscovery of the family as yield; seed 3 reaches 1 on the bound; \(n\equiv 3,5,6\pmod 7\) cannot reach 1; odd multiples of 7 cannot reach 1; the 7x+1 image class fills all units as in 3x+1 / 5x+1
- **Literature:** Crandall 1978; Chamberland 2003; laboratory `mxPlusR_parameter_iff`
- **Open:** which odd \(n\) reach 1; not decided by the image class
- **Decision:** CLOSE. The surviving statement is KNOWN elementary arithmetic. No class excludes an infinite family from reaching 1

```text
What was learned
- Frozen v2.3 rediscovers 2^k y = 7x+1; that is infrastructure, not yield
- T(n) lands in <2> = {1,2,4} inside (Z/7Z)*; 3x+1 and 5x+1 fill all units
- C_out is transient, not basin-excluded: T(73)=1 and T(299593)=1
- Generic cycle-word obstructions classify 1-cycles (only x=1), they do not block reaching 1
- Finite non-visit of 1 from seed 3 is not divergence and not a class obstruction

Strongest theorem
- If 2^k y = 7x+1 then y ≡ 1, 2, or 4 (mod 7)

Strongest refutation
- T(73)=1 with 73 ≡ 3 (mod 7); T(299593)=1 with 299593 ≡ 0 (mod 7)

Reusable machinery
- none added; existing MxPlusRSpec, StrategyPlanner, and MxPlusR.lean lemmas

Prior-art status
- KNOWN elementary congruence; 7-specific because 2 has order 3 mod 7

Complexity profile
- unchanged schema

Branch status
- CLOSE

Why
- No class excludes an infinite family from reaching 1. The image statement is exact, Lean-certified, and KNOWN. Further census expansion would not change that.

Best next question
- What exact obstruction, if any, can frozen v2.3 produce on the next unrun leftover target without new attacks?
```

## Research Campaign 02: weak_collatz_floor_5x4_rplus

- **Date:** 2026-08-26
- **Objective:** Extract a class or branch obstruction for the closed strip \(5x-4\le 4x'\le 5x-1\) (\(x\ge 2\)) relevant to losing the successor, using frozen Research Engine v2.3 without new attacks
- **Hypotheses:** residue-affine control might force loss of the successor; 4/3 reconstruction is not the yield; a universal halt claim is forbidden
- **Major results:** Blind `StrategyPlanner(CYCLE_EXCLUSION)` selected `census_obstruction` and recovered four branches \(4y=5x-r\) (`FINITE_CENSUS`). Exact definedness: unique successor for every \(x\ge 2\), and the successor stays in the domain. Fixed points \(2,3,4\). Seed \(5\) grows on horizons 16 and 32. The map is not \(R^+\) (\(8\mapsto 9\) vs \(10\)). Lean in `Problems.Engine.LinearConstraintLoops`. No new attacks
- **Refuted ideas:** rediscovery of the 4/3 language as yield; this is the 4/3 loop; every orbit loses its successor; finite halt is a \(\mathbb Z\)-theorem; a residue image class excludes a losing-successor basin; \(R^+\) is likewise total on its domain
- **Literature:** Carelli 2026; Matthews–Watts 1984; Ben-Amram–Genaim–Ouaknine–Worrell 2025; laboratory `rplusRel_*`
- **Open:** weak-map halt when hitting a multiple of 4 is a different spec, not this closed strip
- **Decision:** CLOSE. The surviving statements are KNOWN elementary arithmetic or a REPARAMETERIZATION of the 4/3 SLC campaign. Losing the successor is false on this spec

```text
What was learned
- Frozen v2.3 recovers 4y=5x-r as a FINITE_CENSUS; that is 4/3 language, not yield
- Interval length equals the modulus, so the successor is total on x>=2 and stays there
- R+ can be undefined (length 2, modulus 3); this strip cannot
- Fixed points 2,3,4 and growing seed 5 refute “every orbit loses its successor”
- The board’s weak-map halt question is a different spec from the stored inequality

Strongest theorem
- For every integer x>=2 there is a unique y with 5x-4 <= 4y <= 5x-1, and that y satisfies y>=2

Strongest refutation
- 2,3,4 are fixed points; seed 5 grows on horizons 16 and 32; strip(8)=9 while R+(8)=10

Reusable machinery
- none added; existing OneVariableLoopSpec, integer_images, StrategyPlanner, and LinearConstraintLoops.lean lemmas

Prior-art status
- KNOWN elementary interval arithmetic; 5/4-specific because length equals modulus, unlike R+

Complexity profile
- unchanged schema

Branch status
- CLOSE

Why
- Losing the successor is false on the stored closed strip. The branch census is a REPARAMETERIZATION of the 4/3 campaign. Further census expansion would not change that.

Best next question
- What exact obstruction, if any, can frozen v2.3 produce on the next unrun leftover target without new attacks?
```

## Research Campaign 03: matthews_prize_mod3_avoider

- **Date:** 2026-08-26
- **Objective:** Extract a class obstruction forcing ±1 (mod 3) avoiders of the three-branch map into the known cycles, using frozen Research Engine v2.3 without new attacks
- **Hypotheses:** residue-affine control might force avoiders into -1 or {-2,-4}; branch reconstruction and 0 (mod 3) divergence are not the yield; totality is forbidden
- **Major results:** Blind `StrategyPlanner(CYCLE_EXCLUSION)` selected `census_obstruction` and recovered the three given branches (`FINITE_CENSUS`). Exact: 0 (mod 3) is invariant and expanding; cycles at -1 and {-2,-4}. Packet seeds 1 and 5 enter 0 (mod 3). Window avoiders in [-40,40] are {-28,-10,-4,-2,-1}, i.e. the cycles and two preimages. Lean in `Problems.Engine.MatthewsMod3`. No new attacks
- **Refuted ideas:** rediscovery of the three formulas as yield; seeds 1 and 5 are avoiders; {1,2} (mod 3) is a basin; finite cycle visit is a Z-theorem; this is the 4/3 strip or the BB5 map; every window avoider is a cycle point
- **Literature:** Matthews–Watts 1984; laboratory BB-5 / R+ residue-affine reconstruction
- **Open:** whether every Z-avoider enters -1 or {-2,-4}; not decided by the window
- **Decision:** CLOSE. The surviving statements are KNOWN elementary arithmetic. No avoider-class obstruction

```text
What was learned
- Frozen v2.3 recovers the three given branches as a FINITE_CENSUS; that is the problem definition, not yield
- 0 (mod 3) is invariant and expanding; {1,2} (mod 3) is not a basin (T(1)=3)
- Packet seeds 1 and 5 are not avoiders
- Window avoiders include preimages -28 and -10 of {-2,-4}; that is not a Z-theorem
- Named cycles at -1 and {-2,-4} are elementary from the definition

Strongest theorem
- If 3|x then T(x)=2x, 3|T(x), and |T(x)|=2|x|

Strongest refutation
- T(1)=3 and T(5)=1; {1,2} (mod 3) is not a basin; -28 and -10 are avoider preimages, not only cycle points

Reusable machinery
- none added; existing OneVariableLoopSpec, StrategyPlanner, and new KNOWN lemmas in MatthewsMod3.lean

Prior-art status
- KNOWN elementary residue arithmetic; Matthews–Watts supply the map, not an avoider obstruction

Complexity profile
- unchanged schema

Branch status
- CLOSE

Why
- No class forces avoiders into the known cycles. The invariant and cycles are exact, Lean-certified, and KNOWN. Further census expansion would not change that.

Best next question
- What exact obstruction, if any, can frozen v2.3 produce on the next unrun leftover target without new attacks?
```

## Research Campaign 04: companion_shift_order6_zero_class

- **Date:** 2026-08-26
- **Objective:** Recover a lattice/gcd or matrix-word congruence on vanishing indices of the declared order-6 companion window, using frozen Research Engine v2.3 without interpolants, without a new attack, and without claiming non-existence
- **Hypotheses:** an intermediate vanishing-index class constraint might exist that is not the companion definition; prefix gaps and companion rediscovery are not the yield
- **Major results:** Blind `StrategyPlanner(ORIGIN_AVOIDANCE)` selected `vector_matrix` with empty results. Live `ResearchLoop` decision CONTINUE. Prefix length 65 is `FINITE_ZERO_FREE` (`zero_at=None`); `u_11<0`; every modulus 2..32 hits a 0 residue (`NO_PREFIX_EXCLUSION`); `vector_affine` and `matrix_word_invariant` skipped (`COMPUTATION_EXHAUSTED`). Lean reused in `Problems.Engine.CompanionShift`. No new attacks
- **Refuted ideas:** companion-as-yield; prefix ⇒ non-existence; matrix-word gives a vanishing congruence; this is the order-2 competence check; fixed sign
- **Literature:** Bacik et al. 2026; Kenison et al. 2025; Lipton et al. 2022
- **Open:** whether the first coordinate vanishes on Z; not decided by the prefix or the skip
- **Decision:** CLOSE. The surviving statements are KNOWN. No vanishing-index class constraint

```text
What was learned
- Frozen skip at dimension 6 blocks vector census and matrix-word; that is COMPUTATION_EXHAUSTED, not a congruence
- No first-coordinate zero on indices 0..64 is FINITE_ZERO_FREE, not non-existence
- Every modulus 2..32 hits a 0 residue on the prefix; prefix modular zeros are not integer vanishing
- u_11 < 0 is already Lean-certified and KNOWN
- Companion reconstruction is the problem definition, not yield

Strongest theorem
- The observation at index 11 is negative (companion_shift_order6_eleventh_negative)

Strongest refutation
- matrix_word_invariant is skipped at d=6; no zero on 0..64 does not mean no zero exists

Reusable machinery
- none added; existing CompanionShiftSpec, StrategyPlanner, and CompanionShift.lean

Prior-art status
- KNOWN companion window and prefix facts; literature-open vanishing is out of this campaign's target

Complexity profile
- unchanged schema

Branch status
- CLOSE

Why
- No lattice/gcd vanishing congruence was recovered. The skip, the prefix, and the companion window are KNOWN. Further census expansion or interpolants would violate the frozen contract.

Best next question
- What exact obstruction, if any, can frozen v2.3 produce on the next unrun leftover target without new attacks?
```

## Research Campaign 05: skolem_order5_unconditional

- **Date:** 2026-08-26
- **Objective:** On a declared order-5 companion window, see whether frozen v2.3 can do more than a finite prefix, without interpolants, without un-skipping matrix-word, and without claiming an unconditional order-5 decision
- **Hypotheses:** dimension 5 might be a new computational cluster; a finite zero might be billed as an order-5 procedure; uniqueness might fall out of the prefix
- **Major results:** Blind `StrategyPlanner(ORIGIN_AVOIDANCE)` selected `vector_matrix` with empty results. Prefix is `ZERO_WITNESS` at index 2. Skip pair at d=5 equals skip pair at d=6 (`COMPUTATION_EXHAUSTED`). Lean `companion_shift_order5_zero_second`. No new attacks
- **Refuted ideas:** census runs at d=5; d=5 skip is a new cluster; ZERO_WITNESS is an unconditional order-5 procedure; prefix recovers uniqueness; this is the order-6 flagship or the order-2 window
- **Literature:** Lipton et al. 2022 Example 2.4; Kenison et al. 2025; Bacik et al. 2026
- **Open:** unconditional vanishing for general order-5 LRS; not decided by this window
- **Decision:** CLOSE. The surviving statements are KNOWN. Finite zero plus the same skip cluster as dimension 6

```text
What was learned
- Frozen skip at dimension 5 is identical to dimension 6; not a new cluster
- The declared window has a first-coordinate zero at index 2 (ZERO_WITNESS)
- A finite zero is not uniqueness and not an unconditional order-5 procedure
- Companion reconstruction remains the problem definition, not yield
- StrategyPlanner(ORIGIN_AVOIDANCE) still selects vector_matrix with empty results

Strongest theorem
- The observation at index 2 vanishes (companion_shift_order5_zero_second)

Strongest refutation
- 25^5 census is skipped with the same attack pair as 25^6; a ZERO_WITNESS does not decide all order-5 LRS

Reusable machinery
- none added; existing CompanionShiftSpec, StrategyPlanner, and a KNOWN identity in CompanionShift.lean

Prior-art status
- KNOWN finite zero of Lipton et al. 2022 Example 2.4; literature uniqueness and the conditional procedure are out of scope

Complexity profile
- unchanged schema

Branch status
- CLOSE

Why
- The finite zero is KNOWN. The skip is the same computational cluster as dimension 6. No uniqueness certificate and no unconditional procedure. Further census expansion or interpolants would violate the frozen contract.

Best next question
- What exact obstruction, if any, can frozen v2.3 produce on the next unrun leftover target without new attacks?
```

## Research Campaign 06: juggler_sequence

- **Date:** 2026-08-26
- **Objective:** Diagnose the stored even/odd floor-power map as distinct from residue-affine control and from divisor-sum, using frozen v2.3 without a radical attack and without a halt theorem on all positive integers
- **Hypotheses:** the fingerprint might match aliquot truncation, or seed-13 halt might be billed as a Z-theorem, or census might fake an affine cover
- **Major results:** Blind `StrategyPlanner(TERMINATION)` selected `global_inductive` with empty results. Live `ResearchLoop` CONTINUE with exact residual closure of size 5 on seed 13 and piecewise-affine INCONCLUSIVE. Exact: T(1)=1; 13→46→6→2→1. Odd 3 grows. T(8)=2 is not the 5x/4 strip; T(13)=46 is not σ(13)−13. Lean in `Problems.Engine.FloorPower`. No new attacks
- **Refuted ideas:** residue-affine cover; seed-13 halt is a Z-theorem; this is aliquot; this is the 5x/4 strip; global descent; a new radical attack is required
- **Literature:** OEIS A007320; laboratory aliquot comparison
- **Open:** whether every positive integer reaches 1; not decided by seed 13
- **Decision:** CLOSE. The surviving statements are KNOWN. Finite seed closure plus a missing affine cover; fingerprint distinct from aliquot truncation

```text
What was learned
- Packet seed 13 reaches 1 in four steps; T(1)=1; that is not a halt theorem
- Piecewise-affine census is INCONCLUSIVE; floor powers sit outside residue-affine language
- StrategyPlanner(TERMINATION) selects global_inductive with no implemented ranking attack
- The seed-13 fingerprint is FINITE_SEED_CLOSURE, distinct from aliquot factorization truncation
- Odd 3 grows; T(8)=2 is not floor(5n/4)

Strongest theorem
- The packet seed 13 reaches 1 in four steps (floorPower_thirteen_reaches_one)

Strongest refutation
- T(3)=5 (not descent); T(13)=46 (not aliquot); T(8)=2 (not the 5x/4 strip)

Reusable machinery
- none added; FloorPowerSpec follows the existing one-variable dummy-control pattern; KNOWN lemmas in FloorPower.lean

Prior-art status
- KNOWN computational orbit; OEIS A007320 records step counts, not a class obstruction

Complexity profile
- unchanged schema

Branch status
- CLOSE

Why
- The finite orbit is KNOWN. There is no affine cover and no class forcing all seeds to 1. A radical attack would violate the frozen contract.

Best next question
- What exact obstruction, if any, can frozen v2.3 produce on the next unrun leftover target without new attacks?
```

## Research Campaign 07: reverse_and_add_base3

- **Date:** 2026-08-26
- **Objective:** Diagnose the stored balanced-ternary reverse-plus-add map as distinct from digit-fold saturation and from factorization or floor-power maps, using frozen v2.3 without a reverse-add attack, without a palindrome theorem, and without importing base-10 folklore
- **Hypotheses:** the fingerprint might match digit-fold or aliquot/juggler, or seed-196 halt might be billed as a Z-theorem, or census might fake an affine cover, or the adapter might leak palindrome conjectures
- **Major results:** Blind `StrategyPlanner(TERMINATION)` selected `global_inductive` with empty results. Live `ResearchLoop` CONTINUE with exact residual closure of size 9 on seed 196 and piecewise-affine INCONCLUSIVE. Exact: T(0)=0; W(196)=196 so T(196)=392; 196 reaches 0 in eight steps. T(8)=0 is not the floor-power image; T(196)=392 is not digit-sum or σ(196)−196. Lean in `Problems.Engine.ReverseAdd`. No new attacks
- **Refuted ideas:** residue-affine cover; seed-196 halt is a Z-theorem; this is digit-fold; this is aliquot; this is the floor-power map; every seed is reverse-fixed; a new reverse-add attack is required
- **Literature:** OEIS A134028 (the reverse W); laboratory digit-fold / aliquot / floor-power comparison
- **Open:** whether every integer seed hits a reverse-fixed point; not decided by seed 196
- **Decision:** CLOSE. The surviving statements are KNOWN. Finite seed closure plus a missing affine cover; fingerprint distinct from digit-fold, aliquot, and floor-power

```text
What was learned
- Packet seed 196 is reverse-fixed and reaches 0 in eight steps; T(0)=0; that is not a reverse-fixed theorem on Z
- Piecewise-affine census is INCONCLUSIVE; digit reverse sits outside residue-affine language
- StrategyPlanner(TERMINATION) selects global_inductive with no implemented ranking attack
- The seed-196 fingerprint is FINITE_SEED_CLOSURE, distinct from digit-fold saturation, aliquot truncation, and floor-power closure
- T(8)=0 is not the floor-power image 2; T(196)=392 is not digit-sum 2 and not aliquot 203; W(2)=-2

Strongest theorem
- The packet seed 196 reaches 0 in eight steps (reverseAdd_one_ninety_six_reaches_zero)

Strongest refutation
- T(196)=392 (not digit-sum or aliquot); T(8)=0 (not floor-power); W(2)=-2 (not every seed reverse-fixed)

Reusable machinery
- none added; ReverseAddSpec follows the existing one-variable dummy-control pattern; KNOWN lemmas in ReverseAdd.lean wrapping core encodeZ

Prior-art status
- KNOWN computational orbit; OEIS A134028 is the reverse W, not a class obstruction

Complexity profile
- unchanged schema

Branch status
- CLOSE

Why
- The finite orbit is KNOWN. There is no affine cover and no class forcing all seeds to a reverse-fixed point. A reverse-add attack or palindrome totality claim would violate the frozen contract.

Best next question
- What exact obstruction, if any, can frozen v2.3 produce on the next unrun leftover target without new attacks?
```

## Research Campaign 08: home_prime_49

- **Date:** 2026-08-26
- **Objective:** Diagnose the stored factorization-concatenation map as recurring the non-affine arithmetic cluster, using frozen v2.3 without a concatenation attack and without claiming that seed 49 reaches a prime
- **Hypotheses:** the fingerprint might match aliquot unbounded truncation, or seed-49 prefix might be billed as a Z-theorem, or census might fake an affine cover, or the adapter might leak unfinished-seed folklore
- **Major results:** Blind `StrategyPlanner(TERMINATION)` selected `global_inductive` with empty results. Live `ResearchLoop` CONTINUE with exact residual closure of size 13 on the truncated seed-49 prefix and piecewise-affine INCONCLUSIVE. Exact: T(7)=7; 49=7·7 concatenates to 77; 4→22→211. Seed 49 grows until the factorization cap. T(49)=77 is not aliquot or floor-power; T(8)=222 is not reverse-add. Lean in `Problems.Engine.FactorConcat`. No new attacks
- **Refuted ideas:** residue-affine cover; seed-49 prefix is a Z-theorem; this is aliquot; this is the floor-power map; this is reverse-plus-add; a new concatenation attack is required
- **Literature:** OEIS A037274; laboratory aliquot comparison
- **Open:** whether seed 49 reaches a prime; not decided by the truncated prefix
- **Decision:** CLOSE. The surviving statements are KNOWN. Budget-truncated prefix plus a missing affine cover; engine EXACT_CLOSURE is a cap artefact, distinct from aliquot UNBOUNDED_SAMPLE and from attractor closures

```text
What was learned
- Packet seed 49 maps to 77 then grows until the factorization cap; T(7)=7; that is not a prime-reachability theorem
- Piecewise-affine census is INCONCLUSIVE; factor concatenation sits outside residue-affine language
- StrategyPlanner(TERMINATION) selects global_inductive with no implemented ranking attack
- Engine FINITE_SEED_CLOSURE of size 13 is a budget artefact, distinct from aliquot UNBOUNDED_SAMPLE and from reverse-add/juggler attractor closures
- T(49)=77 is not aliquot 8 and not floor-power 343; T(8)=222 is not reverse-add 0; seed 4 reaches 211

Strongest theorem
- Seed 4 reaches the prime 211 in two steps (four_reaches_two_eleven)

Strongest refutation
- T(49)=77 (not aliquot or floor-power); T(8)=222 (not reverse-add)

Reusable machinery
- none added; FactorConcatSpec follows the existing factorization-capped one-variable pattern; KNOWN lemmas in FactorConcat.lean

Prior-art status
- KNOWN computational prefix; OEIS A037274 records home-prime iteration, not a class obstruction

Complexity profile
- unchanged schema

Branch status
- CLOSE

Why
- The finite prefix is KNOWN. There is no affine cover and no class forcing seed 49 to a prime. A concatenation attack or unfinished-seed claim would violate the frozen contract.

Best next question
- What exact obstruction, if any, can frozen v2.3 produce on the next unrun leftover target without new attacks?
```

## Research Campaign 09: cyclic_tag_bit

- **Date:** 2026-08-26
- **Objective:** Diagnose the stored 0|->0, 1|->11 rewrite (halt on empty) as an integer-encoded word map, using frozen v2.3 without a tag-system attack and without a universality claim
- **Hypotheses:** census might fake an affine cover; seed-101 halt might be billed as an integer Z-theorem; the mismatch might require a new tag attack
- **Major results:** Blind `StrategyPlanner(TERMINATION)` selected `global_inductive` with empty results. Live `ResearchLoop` CONTINUE with EXPANDING / UNBOUNDED_SAMPLE, piecewise-affine INCONCLUSIVE, closure INCONCLUSIVE at cap 32. Exact: empty has no successor; [0] is fixed; 101 maps to 0111; length is nondecreasing. Lean in `Problems.Engine.CyclicTag`. No new attacks
- **Refuted ideas:** residue-affine cover; seed-101 halt is an integer Z-theorem; the successor is affine on the encoding; nonempty words map to empty in one step; a new tag attack is required
- **Literature:** Baader–Nipkow 1998
- **Open:** none on this production; nonempty length never drops
- **Decision:** CLOSE. The surviving statements are KNOWN. Predicted word/integer mismatch; low-value obvious incompatibility; board has no remaining unrun names

```text
What was learned
- Empty has no successor; [0] is fixed; 101 maps to 0111 and grows; length is nondecreasing
- Piecewise-affine census is INCONCLUSIVE; residual BFS hits cap 32
- StrategyPlanner(TERMINATION) selects global_inductive with no implemented ranking attack
- Fingerprint is EXPANDING / UNBOUNDED_SAMPLE / COARSE_OBSERVATION: the predicted word/integer mismatch
- Failure-learning is low-value obvious incompatibility, as the protocol already said

Strongest theorem
- Length never decreases when a successor exists (tagStep_length_ge)

Strongest refutation
- Nonempty window words do not map to empty in one step; [0] is fixed

Reusable machinery
- none added; WordRewriteSpec is a sentinel encoding of the existing one-variable dummy-control pattern; KNOWN lemmas in CyclicTag.lean

Prior-art status
- KNOWN rewrite identities; Baader–Nipkow is a textbook, not a class obstruction

Complexity profile
- unchanged schema

Branch status
- CLOSE

Why
- The identities are the productions. The mismatch was predicted. A tag-system attack or universality claim would violate the frozen contract. The stored board is now fully run.

Best next question
- none on the stored board; every named target is now run
```

## Research Engine v2.4: research-control layer

- **Date:** 2026-08-26
- **Objective:** Turn the nine frozen v2.3 campaigns into an immutable baseline, an explicit CLOSE taxonomy, a non-executable Top-3 attack-proposal layer, and a controlled v2.2 replay protocol, without adding attacks
- **Hypotheses:** laboratory CLOSE is too coarse; the engine loses the mathematical frontier when the executable attack vocabulary is exhausted; v2.2 history can be replayed without contaminating the blind track
- **Major results:** `research_engine.control` (`ENGINE_CONTROL_VERSION = 0.2.7`). Immutable `RESEARCH_ENGINE_V2_3_BASELINE`. Primary close tags independent of `mathematical_status`. Every campaign emits exactly three non-executable proposals. Phase-0 replays of `skolem_order2_known_zero` and `switching_affine_z2_origin`. Retrospective: ranking synthesis, nonlinear composition, and proof-guided refinement are the recurring missing capabilities. `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** CLOSE implies mathematical resolution; finite census upgrades to RESOLVED; proposal names may be registry attacks; historical v2.2 yield may seed the blind track
- **Literature:** engine methodology; campaign prior art unchanged
- **Open:** which missing-capability family is the first executable v2.4 attack
- **Decision:** PROMOTE the control layer. Do not implement ranking, basin, or symbolic composition in this branch

```text
What was learned
- v2.3 repeatedly stopped at an unimplemented mathematical frontier, not at a lack of search volume
- CLOSE_SKIP_BOUNDARY + FRONTIER is the honest status of the order-5/6 companion campaigns
- CLOSE_FALSE_OBSTRUCTION + STRONG_NEGATIVE captures the 7x+1 and Matthews class/avoider refutations without claiming the map theorems
- Top-3 proposals from the nine campaigns recur on ranking, nonlinear composition, and predecessor/basin language
- v2.2 replays recover the historical maps independently; added information is control classification, not a new theorem

Strongest theorem
- none; this is engine methodology

Strongest refutation
- Finite/prefix/budget evidence must not infer mathematical_status = RESOLVED

Reusable machinery
- research_engine.control: baseline freeze, CLOSE taxonomy, AttackProposalDossier, v2.2 replay protocol, retrospective extractor

Prior-art status
- engine diagnosis; no new number-theory claim

Complexity profile
- unchanged schema; no new attack

Branch status
- PROMOTE

Why
- The frontier is now explicit. Implementing another attack before evaluating the proposal layer would repeat the v2.3 mistake of expanding machinery without a new mathematical consequence.

Best next question
- What is the cheapest falsifier for ranking-function synthesis as the first executable v2.4 attack family?
```

## Research Engine v2.4: ranking-function Phase-0 falsifier

- **Date:** 2026-08-26
- **Objective:** Decide PROMOTE / REFINE / ABANDON for ranking-function synthesis as the first executable v2.4 attack, using only frozen v2.3 transitions and a tiny exact template family
- **Hypotheses:** a scalar ranking `V = a·log_bit + b·digit + c·residue` already decreases outside a finite core on the three TERMINATION campaigns that stalled at unimplemented `global_inductive`
- **Major results:** 145 canonical templates, exact integer comparison, `K≤8` known cores. All three primary targets are `RANKING_NEEDS_RICHER_STATE`. Cyclic tag negative control is `RANKING_IMPLAUSIBLE` (length nondecrease). Family decision **REFINE**. Formalization `not_yet_formalization_ready`. Records: `docs/research/ranking_phase0.md`, `docs/research/ranking_phase0.json`. Frozen v2.3 seeds and `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** a simple size ranking on `(log_bit, digit, residue)` is already a termination certificate on these bounded samples; naive word-length ranking for cyclic tag
- **Literature:** engine methodology; campaign prior art unchanged
- **Open:** whether a small richer family (odd-even composition, reverse-gap/palindrome defect, composite-versus-prime piecewise) survives the same exact tables
- **Decision:** PARK the ranking synthesizer. REFINE the attack family. Do not enlarge the coefficient grid and do not thaw `DEFAULT_ATTACK_ORDER`

```text
What was learned
- Juggler odd-to-odd floor-power (3→5) increases every available size statistic at constant parity, so no positive-tilt scalar V on (log_bit, digit, parity) can descend
- Reverse-plus-add typically grows; bt_length is not a descent coordinate on the observed window
- Home-prime factor concatenation increases decimal length; primes are an infinite halt set, not a finite ranking core
- Cyclic tag length is nondecreasing: the prototype does discriminate a known obstruction
- Expansion anti-rankings (net negative size tilt) can survive inequalities and must be rejected as termination candidates

Strongest theorem
- none; this is a bounded exact falsifier, not a ranking theorem

Strongest refutation
- Odd juggler 3→5: every coherent scalar template in the Phase-0 family fails on an exact transition outside E={1}

Reusable machinery
- research_engine.control.ranking: canonical 7³ grid, exact integer V, structured failure classes, AttackProposalDossier overlay for Phase-0 only

Prior-art status
- engine diagnosis; no new number-theory claim

Complexity profile
- unchanged schema; no new attack

Branch status
- PARK

Why
- Scalar ranking is not ready to become an executable attack, but the failures share a coherent richer language. Building a general synthesizer now would be machinery gravity. The named Phase-1 family is the next cheapest falsifier.

Best next question
- Can odd-even composition, reverse-gap/palindrome defect, and composite-versus-prime piecewise ranking be falsified on the same exact transition tables without enlarging the coefficient grid?
```

## Research Engine v2.4: ranking-function Phase-1 enriched falsifier

- **Date:** 2026-08-26
- **Objective:** Test the three Phase-0 enrichments — odd-even `T^2`, reverse_gap, piecewise composite `V_C` — as cheap exact falsifiers
- **Hypotheses:** one-step scalar failure can be repaired by composition, representation defect, or piecewise regime without a general synthesizer
- **Major results:** Juggler `COMPOSED_RANKING_PROMISING` (`BOUNDED_SURVIVOR`, 72 coherent templates, 11 odd-to-even macros; strongest `V=log_bit` on `T^2`; 9 odd-to-odd steps including `3→5` remain outside). Reverse-add `REVERSE_GAP_IMPLAUSIBLE` (`1→2` sends a palindrome to `reverse_gap=4`). Home-prime `PIECEWISE_RANKING_NEEDS_RICHER_STATE` (`4→22` concat length growth; `10→25` factor_count nondecrease). Family decision **MIXED**. Records: `docs/research/ranking_phase1.md`, `docs/research/ranking_phase1.json`. Frozen v2.3 seeds and `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** palindrome defect as a termination ranking for reverse-plus-add; a single `V_C` on `(decimal_length, Omega, omega)` as composite-to-composite descent
- **Literature:** engine methodology; campaign prior art unchanged
- **Open:** whether the restricted juggler `T^2` subfamily should become an attack, or reverse-add/home-prime should move to symbolic composition first
- **Decision:** PARK implementing a ranking attack. MIXED for the family. Do not thaw `DEFAULT_ATTACK_ORDER`

```text
What was learned
- On the observed odd-to-even juggler macros, k=2 size ranking is a bounded survivor; it does not address odd-to-odd 3→5
- reverse_gap of the canonical BT word is well-defined, but palindromes are not an attractor of reverse-plus-add
- Composite-to-composite home-prime concatenation can grow decimal length while Omega stays put or omega falls (10→25)
- The three enrichments do not share one next ranking language

Strongest theorem
- none; juggler T^2 decrease is a BOUNDED_SURVIVOR, not a global ranking

Strongest refutation
- Reverse-add 1→2: reverse_gap 0→4, so palindrome-defect ranking fails on the same seed that killed scalar ranking

Reusable machinery
- research_engine.control.ranking_phase1: k=2 composed evaluation, tiny reverse_gap grid, piecewise V_C on factor_trial features

Prior-art status
- engine diagnosis; no new number-theory claim

Complexity profile
- unchanged schema; no new attack

Branch status
- PARK

Why
- One restricted composed ranking survived a bounded sample, but reverse-gap is the wrong Lyapunov direction and piecewise V_C does not descend on concat. Specifying a general ranking attack now would ignore two of three targets.

Best next question
- Should the restricted juggler T^2 ranking be specified as an attack, or should reverse-add and home-prime move to symbolic composition first?
```

## Research Engine v2.4: symbolic-composition Phase-2 falsifier

- **Date:** 2026-08-26
- **Objective:** Decide whether the Phase-1 juggler `T^2` ranking signal is an exact two-step law, and whether the same k=2 probe helps reverse-add and home-prime
- **Hypotheses:** for some nonlinear maps, `T^2` has a simpler exact inequality than one-step ranking; that mechanism need not be shared
- **Major results:** Juggler `SYMBOLIC_COMPOSITION_PROMISING`: on odd `n` with `T(n)` even, `T^2(n)=isqrt(isqrt(n^3))<n` by `k^4 ≤ n^3` (Lean `floorPower_odd_even_two_step_lt`, `PROVED`; 43 odd-even samples, no counterexample; odd-to-odd `3→5` remains outside). Reverse-add `REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE`: neither two-step descent nor ascent (`3→4→8` grows; `1→2→0` collapses; `2→0→0` drops `bt_length`). Home-prime `HOME_COMPOSITION_NEEDS_RICHER_STRUCTURE`: `10→25→55` keeps decimal length; `16→2222→211101` drops `Ω` from 4 to 3; two-step length nondecrease is a `BOUNDED_SYMBOLIC_SURVIVOR`. Family **MIXED**. Promoted concept (not executable): `odd_even_symbolic_composition`. Records: `docs/research/symbolic_composition_phase2.md`, `docs/research/symbolic_composition_phase2.json`. Frozen v2.3 seeds and `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** two-step reverse-plus-add as a magnitude Lyapunov law; one-step concat always lengthening composites; two-step `Ω` nondecrease on home-prime
- **Literature:** engine methodology; campaign prior art unchanged
- **Open:** whether odd-even `T^2 < n` should be specified as a tiny juggler attack, while reverse-add/home-prime move to target-specific rewrite composition
- **Decision:** PARK specifying a symbolic-composition attack. MIXED for the family. Do not thaw `DEFAULT_ATTACK_ORDER`

```text
What was learned
- The Phase-1 juggler ranking survivor is a downstream size consequence of an exact T^2(n) < n lemma on the odd-to-even domain
- Evenness of T(n) identifies T^2 with iterated isqrt of n^3; the size obstruction itself does not use parity
- Reverse-add T^2 both collapses palindromes (1→2→0) and expands other seeds (3→4→8); composition adds complexity
- Home-prime composition remains a factor-word rewrite: 10→25 keeps decimal length, 16→2222→211101 drops Omega
- Symbolic composition is the right language for juggler and the wrong shared theory for the three-target family

Strongest theorem
- For n ≥ 2 odd with isqrt(n^3) even, T^2(n) = isqrt(isqrt(n^3)) < n (Lean: floorPower_odd_even_two_step_lt). Not a halt theorem

Strongest refutation
- Reverse-add 1→2→0: two-step magnitude can drop to 0, so T^2 is not a uniform expansion; 3→4→8 shows it is not a uniform descent either

Reusable machinery
- research_engine.control.symbolic_composition: k=2 sample checks, integer two-step obstruction, Top-3 overlay for Phase-2 only
- Problems.Engine.FloorPower: sqrt_sqrt_n_cubed_lt and floorPower_odd_even_two_step_lt

Prior-art status
- engine diagnosis plus a map-specific integer lemma; no new ranking/composition engine

Complexity profile
- unchanged schema; no new attack

Branch status
- PARK

Why
- The smallest demonstrated concept is odd-even T^2 < n for juggler. Promoting a universal composition family would ignore reverse-add and home-prime, where composition does not simplify. Specifying even the juggler attack now would auto-continue past the decide step.

Best next question
- Should odd-even T^2 < n be specified as a tiny juggler attack, while reverse-add and home-prime move to target-specific rewrite composition?
```

## Research Engine v2.4: restricted symbolic-composition Phase-3 attack

- **Date:** 2026-08-26
- **Objective:** Convert the proved Juggler odd-even `T^2 < n` lemma into a gated executable primitive without a general composition engine
- **Hypotheses:** map-identity matching plus a two-candidate vocabulary plus Lean association recovers Juggler and rejects unrelated maps
- **Major results:** Family **PROMOTE_RESTRICTED**. Juggler `APPLICABLE`: candidate `T^2(x) < x`, Lean `PROVED` (`floorPower_odd_even_two_step_lt`), `mathematical_status = NEW_STRUCTURAL_LEMMA`, `global_consequence = NONE`. Reverse-add, Home Prime, and cyclic tag `NOT_APPLICABLE` / `MAP_MISMATCH`. Attack names are not in `DEFAULT_ATTACK_ORDER`; opt-in is `enable_restricted_symbolic_composition`. Records: `docs/research/symbolic_composition_phase3.md`, `docs/research/symbolic_composition_phase3.json`. Frozen v2.3 seeds, Phase-0/1/2 records, and `DEFERRED_ATTACKS = ("symbolic",)` unchanged
- **Refuted ideas:** treating restricted composition as a generic two-step check on every target; promoting a local lemma to termination
- **Literature:** engine methodology; campaign prior art unchanged
- **Open:** whether another stored map has a natural depth-2 branch that would justify a Phase-4 falsifier
- **Decision:** PROMOTE the gated `odd_even_two_step_decrease` primitive for controlled research use. Do not thaw `DEFAULT_ATTACK_ORDER`

```text
What was learned
- The Phase-2 Juggler lemma can be recovered by matching the floor-power successor, not by campaign name
- Reverse-add, home-prime, and cyclic tag reject as MAP_MISMATCH without alternative-composition search
- Lean certification is an association with floorPower_odd_even_two_step_lt; bounded checks are not the proof
- A local exact lemma stays local: global_consequence is NONE
- Gating keeps the v2.3 flood order intact

Strongest theorem
- For n ≥ 2 odd with T(n) even, T^2(n) < n (Lean: floorPower_odd_even_two_step_lt). Not a halt theorem

Strongest refutation
- Reverse-add, home-prime, and cyclic tag are not floor-power maps; the rule does not apply

Reusable machinery
- research_engine.attacks.restricted_symbolic_composition: one CompositionRule, depth 2, experimental gate
- EXPERIMENTAL_ATTACKS outside DEFAULT_ATTACK_ORDER

Prior-art status
- engine primitive packaging a map-specific integer lemma

Complexity profile
- unchanged flood order; gated opt-in only

Branch status
- PROMOTE

Why
- The smallest executable concept works: Juggler is recovered, negatives reject, freeze holds. Widening depth or adding a composition engine would ignore the measurement.

Best next question
- Does any other stored map have a natural depth-2 branch with an exact inequality that would justify a Phase-4 falsifier, rather than widening this primitive now?
```

## Research Engine v2.4: reverse-add two-step composition Phase-4 falsifier

- **Date:** 2026-08-26
- **Objective:** Test whether k=2 reverse-plus-add exposes an exact structural relation that one-step ranking and reverse_gap could not see
- **Hypotheses:** W(x)+W(T(x))=0, or sign(T²)=sign(x), or bt_length(T²) ≤ bt_length(x)+1
- **Major results:** Candidate 1 `CANCELLATION_FAILURE` at `1→2→0` (`W(1)=1`, `W(2)=-2`). Candidate 2 `SIGN_REVERSAL` at the same sample. Candidate 3 length+1 is a bounded survivor on 49 frozen two-step samples, not a theorem. Classification **REVERSE_COMPOSITION_NEEDS_RICHER_STRUCTURE**. Green loot `NO_NEW_LOOT`. Lean `NOT_YET_FORMALIZATION_READY`. Top-3 #1 stays `symbolic_nonlinear_composition`; `reverse_add_symbolic_composition` is not registered. Records: `docs/research/reverse_add_composition_phase4.md`, `docs/research/reverse_add_composition_phase4.json`. Frozen v2.3 seeds, Phase-0–3 records, and `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** two-step reverse cancellation as a Juggler-style identity; two-step sign preservation; reverse_gap reopening
- **Literature:** engine methodology; campaign prior art unchanged
- **Open:** whether the missing coordinate is the balanced-ternary carry of `x+W(x)`
- **Decision:** PARK a reverse-add composition attack. The Juggler composition method did not transfer

```text
What was learned
- T^2(x)=x+W(x)+W(T(x)) does not cancel: W(1)+W(2)=-1 and T^2(1)=0
- Two-step reverse-plus-add can leave the positive cone at the smallest seed
- A +1 two-step length bound survived the frozen window but has no symbolic proof and is not green loot
- Two-step composition is target-specific: Juggler produced a Lean lemma, reverse-add did not
- reverse_gap stays closed; the missing structure is carry of x+W(x), not a larger census

Strongest theorem
- none; the length+1 bound is a BOUNDED observation, not a lemma

Strongest refutation
- 1→2→0: W(1)=1, W(2)=-2, so the second reverse expands rather than cancelling, and T^2 hits 0

Reusable machinery
- research_engine.control.reverse_add_composition: three pre-ranked k=2 candidates on frozen reverse-add samples

Prior-art status
- engine diagnosis; no new number-theory claim

Complexity profile
- unchanged flood order; no new attack

Branch status
- PARK

Why
- The three natural two-step identities do not produce a Lean-ready reverse lemma. Building a palindrome engine or thawing DEFAULT_ATTACK_ORDER would be machinery gravity.

Best next question
- Is the missing reverse-add coordinate the balanced-ternary carry of x+W(x), and should that be a separate falsifier rather than a composition engine?
```

## Research Engine v2.4: reverse-add carry Phase-5 falsifier

- **Date:** 2026-08-26
- **Objective:** Test whether the existing balanced-ternary addition trace of T(x)=x+W(x) exposes a one-dimensional carry coordinate invisible to magnitude, length, reverse_gap, and two-step composition
- **Hypotheses:** C ≥ max(0, ΔL); C=0 ⇒ ΔL=0; C>0 ⇒ ΔL=1, with C = carry-chain length of add_with_trace
- **Major results:** Candidate 1 survived on 49 frozen one-step samples but is near-definitional. Candidate 2 `REVERSAL_DEPENDENCE` at `2→0` (`W(2)=-2`, length 2→1). Candidate 3 `LENGTH_DECOUPLING` at `5→-6` (`C=2`, length 3→3). Classification **CARRY_NEEDS_RICHER_STATE**. Green loot `NO_NEW_LOOT`. Lean `FORMALIZATION_BLOCKED`. Top-3 #1 stays `symbolic_nonlinear_composition`; carry is supporting but insufficient; `balanced_ternary_carry_attack` is not registered. Records: `docs/research/reverse_add_carry_phase5.md`, `docs/research/reverse_add_carry_phase5.json`. Frozen v2.3 seeds, Phase-0–4 records, and `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** zero-carry preserves canonical length; positive carry forces +1 length; one-dimensional carry as a successor oracle
- **Literature:** engine methodology; campaign prior art unchanged
- **Open:** what exact word-level interaction of x and W(x) should be named instead of a single carry number
- **Decision:** PARK the one-dimensional carry coordinate. Do not register a carry attack

```text
What was learned
- Carry-chain length can be read from add_with_trace without a new arithmetic engine
- C(x) ≥ max(0, ΔL) holds on the frozen sample and is essentially the addition mechanism
- C=0 does not preserve length: 2→0 has W(2)=-2 and collapses by opposite-trit cancellation
- C>0 does not force length +1: 5→-6 has an internal chain of length 2 and ΔL=0
- Special probes respond to the arithmetic: palindrome 1 grows with C=2; seed 196 grows with C=7; W<0 at 2 and successor 0 at 8 have C=0

Strongest theorem
- none; the growth bound is a restatement of how a word sum creates an extra MSD

Strongest refutation
- 5→-6: C=2 with bt_length 3→3, so carry is not the same coordinate as length change

Reusable machinery
- research_engine.control.reverse_add_carry: three pre-ranked k=1 carry/length candidates on frozen reverse-add samples

Prior-art status
- engine diagnosis; no new number-theory claim

Complexity profile
- unchanged flood order; no new attack

Branch status
- PARK

Why
- A one-dimensional carry statistic is related to x+W(x) but does not determine successor length. Building a digit-dynamics engine or thawing DEFAULT_ATTACK_ORDER would be machinery gravity.

Best next question
- If carry is not a sufficient one-dimensional coordinate, what exact word-level interaction of x and W(x) should be named instead?
```

## Research Engine v2.4: reverse-add pair-interaction Phase-6 falsifier

- **Date:** 2026-08-26
- **Objective:** Test whether LSD-aligned pair sums of encode(x) and encode(W(x)) expose an exact successor coordinate invisible to magnitude, length, reverse_gap, T², and carry-chain length
- **Hypotheses:** P0>P2 ⇒ ΔL≤0; P+≠P- ⇒ sign(T)=sign(P+-P-); ΔL≥1 ⇒ s_{n-1}≠0
- **Major results:** Candidates 1 and 3 survived on their frozen domains (19 and 17 samples) but are finite/near-positional, not loot. Candidate 2 `SIGN_IMBALANCE_MISMATCH` at `-672→-448` (P+=4, P-=3, T<0; counts ignore 3^i). Classification **REVERSE_PAIR_NEEDS_RICHER_STRUCTURE**. Green loot `NO_NEW_LOOT`. Lean `FORMALIZATION_BLOCKED`. Top-3 #1 stays `symbolic_nonlinear_composition`; pair interaction is supporting but insufficient; `reverse_pair_interaction` is not registered. Records: `docs/research/reverse_add_pair_interaction_phase6.md`, `docs/research/reverse_add_pair_interaction_phase6.json`. Frozen v2.3 seeds, Phase-0–5 records, and `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** pair-sign majority determines sign(T); one-dimensional pair counts as a successor oracle
- **Literature:** engine methodology; campaign prior art unchanged
- **Open:** what exact remaining interaction of x and W(x) is still not a digit-language engine
- **Decision:** PARK simple reverse-pair aggregates. Do not register a pair-interaction attack

```text
What was learned
- Raw pair sums s_i = left_i + right_i are exactly the add_with_trace digit pairs, with no new arithmetic engine
- P0>P2 ⇒ ΔL≤0 survived on 19 frozen domain samples and is not a definition of s_i
- Pair-sign majority does not determine sign(T): -672→-448 has P+>P- but T<0 because counts ignore place value
- ΔL≥1 ⇒ s_{n-1}≠0 survived on 17 growth samples; it is a weak positional restatement, not loot
- Special probes match the arithmetic: palindrome 1 has s=(2,); reverse-as-negation 2 and 8 have all-zero pairs; 5 has an internal |s|=2; seed 196 is all |s|=2

Strongest theorem
- none; the two length survivors are finite-sample observations, not lemmas

Strongest refutation
- -672→-448: P+=4, P-=3, sign(T)=-1

Reusable machinery
- research_engine.control.reverse_add_pair_interaction: three pre-ranked k=1 pair/successor candidates on frozen reverse-add samples

Prior-art status
- engine diagnosis; no new number-theory claim

Complexity profile
- unchanged flood order; no new attack

Branch status
- PARK

Why
- Pairwise reverse interaction is visible and related to length, but simple counts and the top position do not determine T. A digit-language engine would be machinery gravity.

Best next question
- If simple pair counts and the top aligned position do not determine T, what exact remaining interaction of x and W(x) is still not a digit-language engine?
```

## Research Engine v2.4: reverse-add weighted-pair Phase-7 falsifier

- **Date:** 2026-08-26
- **Objective:** Test whether a low-information positional summary of reverse-pair sums determines sign(T) without reconstructing T=sum s_i 3^i
- **Hypotheses:** sign(T)=sign(s_h); m+>m- ⇒ T>0 (and symmetric); sign(T)=sign(s_{h2})
- **Major results:** Candidates 1 and 2 survived on 42 nonzero-pair samples and repair Phase-6 `-672→-448` (h=6, s_h<0, m->m+). Candidate 3 `MULTI_POSITION_INTERFERENCE` at `6→4` (`s=(1,-2,1)`, h2=1 negative, h=2 positive). Classification **WEIGHTED_PAIR_PROMISING**. Green loot `NO_NEW_LOOT`. Lean `FORMALIZATION_READY` (bound |sum_{i<h} s_i 3^i| ≤ 3^h-1; not proved here). Top-3 #1 stays `symbolic_nonlinear_composition`; highest-pair sign is supporting; `weighted_reverse_pair_interaction` is not registered. Records: `docs/research/reverse_add_weighted_pair_phase7.md`, `docs/research/reverse_add_weighted_pair_phase7.json`. Frozen v2.3 seeds, Phase-0–6 records, and `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** highest |s|=2 collision determines sign(T); further unweighted or collision-only scalars as successor oracles
- **Literature:** engine methodology; campaign prior art unchanged
- **Open:** whether reverse-and-add still needs a target-specific nonlinear identity once sign is a place-value fact
- **Decision:** PARK a production weighted-pair attack. Do not register weighted_reverse_pair_interaction

```text
What was learned
- Highest nonzero pair sign determines sign(T) on the frozen sample and is strictly coarser than the full weighted sum
- The same law repairs -672: P+>P- but m-=6 > m+=5, so T<0
- Candidate 2 is the mixed-sign unpacking of Candidate 1, not an independent law
- Highest |s|=2 does not determine sign: 6→4 has an internal -2 dominated by a higher +1
- The sign law is the base-3 bound |lower| ≤ 3^h-1, not reverse-add loot; no Lean proof in this phase

Strongest theorem
- none proved here; the candidate sign law is FORMALIZATION_READY as a place-value bound

Strongest refutation
- 6→4: h2=1, s_{h2}=-2, h=2, s_h=+1, T=4

Reusable machinery
- research_engine.control.reverse_add_weighted_pair: three pre-ranked positional summaries on frozen reverse-add samples

Prior-art status
- engine diagnosis; no new number-theory claim

Complexity profile
- unchanged flood order; no new attack

Branch status
- PARK

Why
- Positional dominance explains sign(T) without reconstructing T, but it is a general leading-term bound and the collision summary fails. A digit-language engine would be machinery gravity.

Best next question
- If highest-pair sign is an exact but general place-value fact, does reverse-and-add still need a target-specific nonlinear identity?
```

## Research Engine v2.4: reverse-add involution Phase-8 falsifier

- **Date:** 2026-08-26
- **Objective:** Test whether \(W(W(x))=x\) creates a reverse-specific exact law among \(x\), \(W(x)\), \(T(x)\), and \(W(T(x))\) that is not generic place-value arithmetic and not a tautology
- **Hypotheses:** \(|W(T)-W(x)|\le|W(x)|\); \(\operatorname{reverse\_gap}(T)\le\operatorname{reverse\_gap}(x)+\operatorname{bt\_length}(x)\); MSD(\(T\)) lies in the operand MSD set
- **Major results:** Candidates 1 and 2 fail at the palindrome \(1\to 2\) (\(R=-3\); gap \(0\to 4\)). Candidate 3 survives 42 nonzero successors but is assessed `GENERAL_ARITHMETIC`. Classification **REVERSE_INVOLUTION_REFUTED**. Green loot `NO_NEW_LOOT`. Lean `FORMALIZATION_BLOCKED`. Top-3 #1 stays `symbolic_nonlinear_composition`; `reverse_involution_not_sufficient_at_this_level`; `reverse_involution_structure` is not registered. Records: `docs/research/reverse_add_involution_phase8.md`, `docs/research/reverse_add_involution_phase8.json`. Frozen v2.3 seeds, Phase-0–7 records, and `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** reverse-sum residual bound; successor reverse-gap length bound; compressed involution summaries as reverse-and-add loot
- **Literature:** engine methodology; campaign prior art unchanged
- **Open:** return to the existing symbolic-nonlinear frontier without a digit-language engine
- **Decision:** CLOSE the compressed involution falsifier. Do not register reverse_involution_structure. Stop inventing scalar descriptors of reverse-and-add

```text
What was learned
- Canonical W is involutive iff x=0 or 3 does not divide x; 6 and -672 are not involutive, and that fact is not loot
- |W(T)-W(x)| is not controlled by |W(x)|: palindrome 1 maps to 2 with residual -3
- reverse_gap of the successor is not controlled by gap(x)+length(x): the same 1→2 step jumps 0 to 4
- MSD inheritance of T from {MSD(x), MSD(W), negatives} survived the frozen sample but is generic leading-digit arithmetic
- W(W(x))=x and T=x+W(x) remain definitional and were not counted as yield

Strongest theorem
- none; the only survivor is GENERAL_ARITHMETIC, not a reverse-add lemma

Strongest refutation
- 1→2: R=-3 and reverse_gap 0→4 on a reversal-fixed palindrome

Reusable machinery
- research_engine.control.reverse_add_involution: three pre-ranked k=1 involution-interaction candidates on frozen reverse-add samples; gated name reverse_involution_phase8 is not in DEFAULT_ATTACK_ORDER

Prior-art status
- engine diagnosis; no new number-theory claim

Complexity profile
- unchanged flood order; no new attack

Branch status
- CLOSE

Why
- The defining involution does not produce a compressed reverse-specific law among x, W(x), T(x), W(T(x)). Remaining survivors are generic arithmetic. A digit-language engine would be machinery gravity.

Best next question
- If compressed involution summaries fail, should reverse-and-add return to the existing symbolic-nonlinear frontier without a digit-language engine?
```

## Research Engine v2.4: frontier re-ranking Phase-9 selection

- **Date:** 2026-08-26
- **Objective:** Rank remaining `(target, attack)` pairs for expected new mathematics per unit of attack effort, without implementing or executing a winner
- **Hypotheses:** Accumulated Phase 0–8 evidence plus frozen v2.3 Top-3 dossiers suffice to select a high-information next experiment; reverse-add must stay closed
- **Major results:** **SELECTED_FRONTIER** `(juggler_sequence, odd_odd_branch_composition)` expected loot `GREEN`, Lean `PLAUSIBLE`. Backups: `(mx_plus_r_7x1_class_obstruction, basin_preimage_grammar)` and `(matthews_prize_mod3_avoider, basin_preimage_grammar)`, both `GREY`. Reverse-add excluded. Score is qualitative, not calibrated. Records: `docs/research/phase9_frontier_ranking.md`, `docs/research/phase9_frontier_ranking.json`. Frozen v2.3 seeds, Phase-0–8 records, and `DEFAULT_ATTACK_ORDER` unchanged. No new board. No new attack registration
- **Refuted ideas:** reopening reverse-add because it has stored observations; treating a successful Juggler lemma as a universal composition attack; ranking synthesizer / digit-language / generic symbolic engine as the next battle
- **Literature:** engine methodology; campaign prior art unchanged
- **Open:** exact k=2 law on the Juggler odd-odd cylinder, if any
- **Decision:** PROMOTE the frontier map as laboratory intelligence. Do not execute the selected pair in this phase

```text
What was learned
- The ranking unit is (target, attack), not a leftover board ordering
- Reverse-add is CLOSED: many observations are not a reason to reopen it
- The Juggler odd-even lemma is exhausted; the complementary odd-odd cylinder is the highest-yield unused pair
- Image-as-basin remains a recurring limitation and supplies the two GREY backups
- Replays of known zeros or reproduced orthant theorems are unattractive

Strongest theorem
- none; this phase selects, it does not prove

Strongest refutation
- none new; reverse-add remains excluded by Phase-8

Reusable machinery
- research_engine.control.frontier_ranking: frozen candidate pool, qualitative score, Top-3 AttackProposalDossier; gated name phase9_frontier_ranking is not in DEFAULT_ATTACK_ORDER

Prior-art status
- engine diagnosis; no new number-theory claim

Complexity profile
- unchanged flood order; no new attack

Branch status
- PROMOTE (selection intelligence only)

Why
- The next battle should be the cheapest high-yield falsifier on a named complementary Juggler cylinder, not another reverse-add scalar or a new attack family.

Best next question
- Run a k=2 odd-odd composition falsifier on the existing frozen Juggler transitions without generalizing odd_even_two_step_decrease.
```

## Research Engine v2.4: Juggler odd-odd composition Phase-10 falsifier

- **Date:** 2026-08-26
- **Objective:** Determine whether the complementary odd→odd floor-power cylinder admits a simple exact k=2 law that is not definitional restatement and not a halt theorem
- **Hypotheses:** `T^2(x)>x` on all `D_OO`; `T^2(n)>n` on `D_OO` with exact threshold `n≥3`; `T^2(x)` remains odd
- **Major results:** Candidate 1 `THRESHOLD_FAILURE` at `1→1→1`. Candidate 2 survived 8 frozen samples and is Lean **PROVED** as `floorPower_odd_odd_two_step_gt`. Candidate 3 `PARITY_DOMAIN_LEAK` at `5→11→36`. Classification **JUGGLER_ODD_ODD_GREEN_LOOT**. Scope `LOCAL_BRANCH_LAW`, not `GLOBAL_TERMINATION`. Top-3 #1 is `odd_odd_symbolic_composition` (proposed, not registered). `odd_even_two_step_decrease` unchanged. Records: `docs/research/juggler_odd_odd_phase10.md`, `docs/research/juggler_odd_odd_phase10.json`. Frozen v2.3 seeds, Phase-0–9 records, and `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** strict two-step growth on the whole cylinder including 1; odd-cylinder invariance under `T^2`; k>2 to hide `5→11→36`
- **Literature:** engine methodology; Juggler totality remains open and unclaimed
- **Open:** whether leakage into an even image reuses the odd-even lemma at depth 2
- **Decision:** PROMOTE the local odd-odd growth lemma. Do not register a production odd-odd attack. Do not claim termination or divergence

```text
What was learned
- D_OO and D_OE are complementary odd cylinders; the existing odd-even theorem is unchanged
- T^2(x)>x fails on D_OO at the fixed point 1
- For n≥3 in D_OO, T^2(n)>n follows from (n+1)^2 ≤ n^3 plus odd-branch monotonicity
- T^2 does not preserve oddness: 5→11→36 leaves the cylinder
- The growth law is LOCAL_BRANCH_LAW, the dual of odd-even descent, not a divergence theorem

Strongest theorem
- For odd n≥3 with T(n) odd, T^2(n)>n (floorPower_odd_odd_two_step_gt)

Strongest refutation
- 5→11→36: two odd steps can land even

Reusable machinery
- research_engine.control.juggler_odd_odd: three pre-ranked k=2 odd-odd candidates; gated name juggler_odd_odd_phase10 is not in DEFAULT_ATTACK_ORDER

Prior-art status
- engine diagnosis; local floor-power lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack

Branch status
- PROMOTE

Why
- The complementary cylinder has an exact dual inequality with a derived threshold and a Lean proof. Cylinder invariance fails, so stop at k=2.

Best next question
- Does odd-cylinder leakage into an even image reuse floorPower_odd_even_two_step_lt without raising composition depth?
```

## Lychrel / Reverse-and-Add problem registration

- **Date:** 2026-08-26
- **Objective:** Register the Lychrel / Reverse-and-Add family \(R_b(n)=n+\operatorname{rev}_b(n)\) as a pipeline candidate (decimal canonical, base-\(b\) generalization, base-3 instance, exploratory balanced-ternary branch) without executing an attack
- **Hypotheses:** A digit-transducer / residual / PalReach formulation might be new relative to computational Lychrel lore; this is registration, not a test of that hypothesis
- **Major results:** Problem `lychrel_dynamics` registered. Five candidate attack families recorded and not placed in `DEFAULT_ATTACK_ORDER`. Novelty review required and incomplete. Distinct from closed `reverse_and_add_base3` (\(n+W(n)\)). Records: `docs/problems/lychrel_dynamics.md`, `research.lychrel_dynamics`. Literature ids `oeis-A023108`, `oeis-A006960`, `oeis-A056964`, `oeis-A077408`, `oeis-A060382`, `prosper-veigneau-2001-palindromic-reversal`, `weisstein-196-algorithm`
- **Refuted ideas:** identifying this problem with the closed BT reverse-plus-add campaign; billing 196 or 103 as proved Lychrel numbers
- **Literature:** known computational candidate lists and the palindromic-reversal paper; automata/transducer prior art still required before any attack
- **Open:** existence of a non-palindromizing seed in base 10 (literature-open, not a project conjecture)
- **Decision:** PARK. Do not execute. Do not thaw the flood order. Do not reopen reverse-and-add

```text
What was learned
- Unsigned R_b is a different map from closed T(n)=n+W(n)
- Decimal 196 and ternary 103 are computational candidates, not theorems
- Five attack families can be named without becoming flood-order attacks
- Novelty risk is very high; qualitative labels are not a numeric rank
- Lean targets are definitional objects, not the conjecture

Strongest theorem
- none; this phase registers

Strongest refutation
- identification with reverse_and_add_base3

Reusable machinery
- research.lychrel_dynamics pipeline record and candidate family metadata; not an attack

Prior-art status
- known; novelty review mandatory before selection-to-execution

Complexity profile
- unchanged flood order; no new production attack

Branch status
- PARK

Why
- The family is a serious candidate with a clear attack surface, but novelty risk is very high and no novelty review has finished. Registration is not an attack.

Best next question
- Complete the novelty-review searches before any promotion from selection to execution.
```

## Research Engine v2.4: Juggler macro-dynamics Phase-11 falsifier

- **Date:** 2026-08-26
- **Objective:** Determine whether the paired odd-even contraction and odd-odd expansion lemmas induce an exact macro-transition grammar for odd Juggler states
- **Hypotheses:** combined direction on odd `n≥3`; `B` determines `parity(T^2)`; contraction exits the odd macro
- **Major results:** Candidate 1 survived as `COMPOSITION_OF_KNOWN_FACTS` (`floorPower_odd_macro_direction`). Candidate 2 `MACRO_PARITY_NOT_DETERMINISTIC` at `5→11→36`. Candidate 3 `DIRECTION_SURVIVAL_DECOUPLING` at `15→58→7`. Classification **MACRO_GRAMMAR_NEEDS_RICHER_STRUCTURE**. Loot `NO_NEW_LOOT`. Macro-state `M(n)=(parity(n), B(n), parity(T^2(n)))` is `MACRO_STATE_INSUFFICIENT`. Records: `docs/research/juggler_macro_phase11.md`, `docs/research/juggler_macro_phase11.json`. Frozen v2.3 seeds, Phase-0–10 records, and `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** `B` as a next-parity grammar; contraction as deterministic exit from the odd macro; billing the combined direction lemma as new loot; a parity automaton or `k>2` rescue
- **Literature:** engine methodology; Juggler totality remains open and unclaimed
- **Open:** basin/preimage grammar on `mx_plus_r_7x1_class_obstruction`
- **Decision:** PARK the macro-grammar branch. Keep the two local Juggler lemmas. Do not register `juggler_macro_grammar`. Do not invent another Juggler micro-attack

```text
What was learned
- D_OE and D_OO remain complementary on odd n>=3; n=1 is the exceptional fixed point
- Pairing the two proved lemmas yields a combined direction statement, not a new consequence
- B(n)=O does not determine parity(T^2): 3→5→11 stays odd, 5→11→36 leaves even
- B(n)=E does not force exit: 7→18→4 is even, 15→58→7 is odd
- The three-bit macro-state loses the information that would couple direction to survival

Strongest theorem
- For odd n>=3, B=E => T^2<n and B=O => T^2>n (floorPower_odd_macro_direction; COMPOSITION_OF_KNOWN_FACTS)

Strongest refutation
- 5→11→36 and 15→58→7: branch label does not determine T^2 parity or odd-macro survival

Reusable machinery
- research_engine.control.juggler_macro: three pre-ranked k=2 macro candidates; gated name juggler_macro_phase11 is not in DEFAULT_ATTACK_ORDER

Prior-art status
- engine diagnosis; combined known lemmas, not a Juggler halt or divergence result

Complexity profile
- unchanged flood order; no new production attack

Branch status
- PARK

Why
- The paired branch laws do not induce a next-bit transition grammar. A richer state has not been justified. Stop rather than manufacture a macro theory.

Best next question
- Run a basin/preimage falsifier on mx_plus_r_7x1_class_obstruction without adding another Juggler micro-attack.
```

## Research Engine v2.4: Juggler parity-drift Phase-12 falsifier

- **Date:** 2026-08-26
- **Objective:** Determine whether log-log parity drift yields an exact finite-block inequality without predicting the next parity bit
- **Hypotheses:** exact one-step power bounds; `OOOEE` implies `T^5(n)<n`; shortest negative-drift word `EE` implies `T^2(n)<n`
- **Major results:** Candidate 1 survived as `DEFINITIONAL_RESTATEMENT`. Candidate 2 survived on frozen `OOOEE` states `3,25,39` and is Lean **PROVED** as `floorPower_oooee_five_step_lt` via `n5^32 ≤ n^27`. Candidate 3 (`EE`) survived as even-branch contraction, not loot. Classification **PARITY_DRIFT_GREEN_LOOT**. Scope `LOCAL_BRANCH_LAW`, Level B only. Records: `docs/research/juggler_parity_drift_phase12.md`, `docs/research/juggler_parity_drift_phase12.json`. Frozen v2.3 seeds, Phase-0–11 records, and `DEFAULT_ATTACK_ORDER` unchanged
- **Refuted ideas:** treating one-step `T ≤ n^{3/2}` as new loot; treating `EE` as mixed-energy loot; promoting a contractive block to a global frequency/termination theorem
- **Literature:** engine methodology; Juggler totality remains open and unclaimed
- **Open:** whether every long trajectory contains `OOOEE` (Level C, out of scope)
- **Decision:** PROMOTE the local `OOOEE` five-step contraction. Do not register `parity_drift_block`. Do not claim termination or divergence

```text
What was learned
- Additive log-log costs are exactly the floor-power inequalities; that restatement is not loot
- The shortest negative-drift word in the frozen list is EE, which is ordinary even contraction
- OOOEE is realized on the frozen window and satisfies T^5(n)<n
- Floors preserve the heuristic sign: n5^32 ≤ n^27 forces T^5(n)<n for n≥2
- A contractive block is not a theorem that every orbit contains that block

Strongest theorem
- If n≥2 follows the parity word OOOEE, then T^5(n)<n (floorPower_oooee_five_step_lt)

Strongest refutation
- One-step additive costs are definitional; EE is not mixed-branch energy loot

Reusable machinery
- research_engine.control.juggler_parity_drift: three pre-ranked k≤5 candidates; gated name juggler_parity_drift_phase12 is not in DEFAULT_ATTACK_ORDER

Prior-art status
- engine diagnosis; local floor-power block lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack

Branch status
- PROMOTE

Why
- The mixed block OOOEE has an exact contraction inequality that is not a restatement of the k=2 lemmas and is Lean-proved. Level C remains untouched.

Best next question
- Other k≤5 mixed blocks as Level B conditionals, without a parity-frequency theorem.
```

## Juggler fixed-word power inequalities

- **Date:** 2026-08-26
- **Objective:** Falsify the exponent-only hypothesis that a Juggler parity word \(w\) obeys \(T^{|w|}(n)^{2^{|w|}}\lessgtr n^{3^{\#O(w)}}\) with the sign of \(3^{\#O}\) versus \(2^{|w|}\), independently of letter order
- **Hypotheses:** two-sided canonical comparison; one-sided floor composition \(T^k(n)^{2^k}\le n^{3^o}\); same-count permutations agree; near-critical words \(27/32\), \(243/256\), \(729/512\) are the strongest floor-error tests
- **Major results:** Exhaustive \(|w|\le 8\) on \(1\le n\le 10^6\) plus targeted \(k=9\), \(o=6\). Two-sided exponent-only law **REFUTED** (expanding reverse fails at `O`/\(n=3\); strict even contraction equals on perfect squares). One-sided composition held on the whole domain (H1, including `OE` vs `EO` and all realized \(243/256\) words). Lean **PROVED** `floorPower_oooeeeoo_eight_step_lt`: `OOOEEEOO` implies \(T^8(n)^{256}\le n^{243}\) and \(T^8(n)<n\) for \(n\ge 2\). Classification **POWER_WORD_COUNTEREXAMPLE**. Records: `docs/research/juggler_power_words.md`, `docs/problems/juggler_power_words.md`. Research Engine control layer unchanged
- **Refuted ideas:** expanding reverse inequality \(T_w(n)^{2^k}>n^{3^o}\); strict \(T(n)^2<n\) on all even \(n\ge 2\); treating `OOOEE` as an isolated lucky word rather than one-sided composition
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** a word-indexed one-sided composition lemma without a general-word tactic or frequency theorem
- **Decision:** PROMOTE the one-sided composition and the `OOOEEEOO` theorem. Record the two-sided law as COUNTEREXAMPLE. Do not register an attack

```text
What was learned
- Floor steps give only upper bounds, so T_w(n)^{2^k} <= n^{3^o} is the composition principle
- The expanding reverse inequality is false at the first odd n>=3
- Pure-even strict contraction fails with equality on the infinite square-tower family
- Same (k,o) permutations agreed on both comparisons (H1); ordering was not a discriminator
- Near-critical 243/256 mixed words survived; OOOEE is the (5,3) calibration of the same mechanism

Strongest theorem
- If n>=2 follows the parity word OOOEEEOO, then T^8(n)<n (floorPower_oooeeeoo_eight_step_lt)

Strongest refutation
- OO at n=3: 11^4 = 14641 < 3^9 = 19683, against the expanding reverse inequality

Reusable machinery
- research.juggler_sequence.power_words: exact cmp_pow and fixed-word sweep
- FloorPower primitives pow_sq_le / pow_sq_le_cube / floorPower_even_sq_le / floorPower_odd_sq_le_cube

Prior-art status
- local floor-power block lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The two-sided exponent-only law is false, but the one-sided OOOEE mechanism is not an isolated word: a near-critical 243/256 block is Lean-proved. Stop before a general-word tactic.

Best next question
- Can the one-sided floor-power chain be packaged as a composition lemma indexed by a finite word, without a general-word tactic and without a parity-frequency theorem?
```

## Juggler one-sided floor-power composition

- **Date:** 2026-08-26
- **Objective:** Decide whether the surviving one-sided envelope \(T_w(n)^{2^k}\le n^{3^o}\) is a compositional theorem of realized finite words
- **Hypotheses:** `PowerBound` is preserved by append-even and append-odd; the exponent gap \(3^o<2^k\) at \(n\ge 2\) yields strict contraction; mixed-word equality is not required for the weak theorem
- **Major results:** Near-equality scan found no one-sided failure. Mixed words had no equality in the focus set. Lean API `power_bound_empty` / `power_bound_append_even` / `power_bound_append_odd` / `power_bound_follows` / `power_bound_contracts` **PROVED**. `OOOEE` and `OOOEEEOO` are instances via `floorPower_oooee_of_follows` and `floorPower_oooeeeoo_of_follows`. Classification **POWER_COMPOSITION_GREEN**. Records: `docs/research/juggler_power_composition.md`, `docs/problems/juggler_power_composition.md`. Control layer unchanged
- **Refuted ideas:** requiring a strict floor inequality in the composition theorem; treating OOOEE as an isolated chain rather than an instance of `PowerBound`
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** mixed-word equality classification (secondary)
- **Decision:** PROMOTE the finite-word power calculus. Do not register an attack. Do not claim termination

```text
What was learned
- The weak bound is inductive: empty word, append even (k,o)->(k+1,o), append odd (k,o)->(k+1,o+1)
- Realization is a finite itinerary hypothesis `follows`, not a second engine
- Strict contraction is the exponent gap at n>=2, not a strict floor inequality
- Equality is structural (square towers, n=1), so the weak theorem is correctly non-strict
- OOOEE and OOOEEEOO are ordinary instances of the same corollary

Strongest theorem
- Every realized finite word w obeys T_w(n)^{2^{|w|}} <= n^{3^{#O(w)}}; if 3^o < 2^k and n>=2 then T_w(n)<n

Strongest refutation
- none for the weak bound; the two-sided expanding reverse remains false at OO, n=3

Reusable machinery
- FloorPower.PowerBound / follows / power_bound_append_even / power_bound_append_odd / power_bound_contracts
- research.juggler_sequence.power_composition near-equality probe

Prior-art status
- local floor-power composition lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The one-sided envelope is a finite-word theorem, not a word-specific accident. Stop rather than classify mixed equality or add a tactic.

Best next question
- Is mixed-word equality possible, or is equality generated only by even perfect-power towers and the odd fixed point n=1?
```

## Juggler mixed-word floor-power equality

- **Date:** 2026-08-26
- **Objective:** Decide whether every odd Juggler step forces the composed one-sided envelope to be strict for \(n\ge 2\)
- **Hypotheses:** mixed-word equality does not occur for \(n\ge 2\); equivalently \(T(n)^2<n^3\) for every odd \(n\ge 3\) because \(n^{3/2}\) is never an integer
- **Major results:** Mixed-word equality **exists**. Smallest witness: word `O`, \(n=9\), \(T(9)=27\), \(27^2=9^3\). Mechanism: odd squares have integer \(n^{3/2}\). Lean **PROVED** `floorPower_odd_sq_eq_cube_of_sq` and `floorPower_nine_odd_eq`. No both-letter (`O` and `E`) equality on the searched domain. Classification **MIXED_EQUALITY_FOUND**. Records: `docs/research/juggler_equality_rigidity.md`, `docs/problems/juggler_equality_rigidity.md`. Control layer unchanged
- **Refuted ideas:** mixed-word strictness `mixed_word_power_lt`; universal `T(n)^2<n^3` for odd \(n\ge 3\); `floorPower_odd_sq_lt_cube` as a lemma for all odd \(n\ge 3\)
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether a word containing `E` can attain equality for \(n\ge 2\); whether all-odd equality is exactly the odd \(b^{2^j}\) family
- **Decision:** PROMOTE the witness and the odd-square mechanism. Stop mixed-strictness. Do not register an attack

```text
What was learned
- An odd step need not be strict: T(n)^2 = n^3 whenever n is an odd square
- The smallest mixed equality is O at n=9, not a deep or exotic word
- All-odd tight chains continue on odd high even powers such as 81 = 3^4
- A tight odd step has odd image, so E cannot follow it immediately
- Floor strictness is not the same as the exponent-gap contraction 3^o < 2^k

Strongest theorem
- If m is odd, then T(m^2)^2 = (m^2)^3 (floorPower_odd_sq_eq_cube_of_sq); in particular T(9)^2 = 9^3

Strongest refutation
- Mixed-word equality at O, n=9: 27^2 = 9^3 = 729

Reusable machinery
- research.juggler_sequence.equality_rigidity: mixed-equality search reusing power_words cmp_pow
- FloorPower lemmas floorPower_odd_sq_eq_cube_of_sq and floorPower_nine_odd_eq

Prior-art status
- local floor-power equality witness, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The mixed-strictness hypothesis is false, with a minimized arithmetic source. Stop rather than add PowerBoundStrict or a mixed_word_power_lt theorem.

Best next question
- Is equality for words containing E impossible for n>=2, and is all-odd equality exactly the odd b^{2^j} family?
```

## Juggler finite-word power algebra and equality rigidity

- **Date:** 2026-08-26
- **Objective:** Decide whether global envelope equality for a realized finite word forces every local branch inequality to be tight, and whether each local tightness is equivalent to a perfect square
- **Hypotheses:** even `T(n)^2=n` iff square; odd `T(n)^2=n^3` iff square; composite envelope equality implies every local inequality is tight, hence every relevant state is square
- **Major results:** Local iff-square theorems **PROVED**. Equality propagation **PROVED** (`power_bound_eq_implies_local_eq`). Square-state consequence **PROVED** (`power_bound_eq_implies_square`). Unfolded word theorem `power_bound_word`. Computational search: 0 `LOCAL_SQUARE_EQ_FALSE`, 0 `GLOBAL_EQ_PROPAGATION_FALSE`; 118 predicted equalities on \(n\le 10^4\), depth 8, none both-letter. Classification **EQUALITY_RIGIDITY_GREEN**. Records: `docs/research/juggler_power_algebra.md`, `docs/problems/juggler_power_algebra.md`. Control layer unchanged
- **Refuted ideas:** mixed-word strictness remains refuted (prior phase); huge `cmp_pow` equality search; `PowerBoundStrict` / `PowerHeight` certificates
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** how `O` and `E` act on successive perfect powers; not an equality-word census
- **Decision:** PROMOTE the rigidity chain. Do not register an attack. Do not claim termination

```text
What was learned
- Local even and odd envelope equalities are exactly the perfect-square states
- Global T_w(n)^{2^k} = n^{3^o} forces every local inequality in the chain to be tight
- Therefore every relevant itinerary state is a square; images such as 27 and 2 need not be
- 9→27 and 16→4→2 are instances of that chain, not exceptional words
- Contraction from 3^o < 2^k is a separate comparison from floor equality

Strongest theorem
- If a realized finite word attains the envelope with equality, then every local branch is exact and every relevant state is a perfect square

Strongest refutation
- none for the rigidity chain; mixed-word strictness remains false at O, n=9

Reusable machinery
- FloorPower PowerBoundEq / power_bound_eq_implies_local_eq / power_bound_eq_implies_square
- research.juggler_sequence.power_algebra local-tightness probe

Prior-art status
- local floor-power rigidity lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Equality is controlled by the same local inequalities that built the finite-word envelope, with an exact square condition at each step. Stop rather than census equality words or add PowerHeight.

Best next question
- How do O and E act on successive perfect powers (the descending s^2 ↦ s^3 / s^2 ↦ s dynamics)?
```

## Juggler exact perfect-power dynamics and saturation budget

- **Date:** 2026-08-26
- **Objective:** Decide whether a realized word of length \(k\) can attain the finite-word floor-power envelope with equality only if the start is a \(2^k\)-th power
- **Hypotheses:** if \(n=a^{2^r}\) then exact \(E\) is \(a^{2^{r-1}}\) and exact \(O\) is \(a^{3\cdot 2^{r-1}}\); each exact branch drops one factor of \(2\); equality of length \(k\) forces \(HasPowTwoDepth(n,k)\)
- **Major results:** Exact even/odd transitions **PROVED**. Depth-drop lemmas **PROVED**. Cube-depth pullback `hasPowTwoDepth_of_cube` **PROVED**. Budget theorem `power_bound_eq_implies_pow_two_depth` **PROVED**. For \(n\ge 2\), equality of length \(k\) implies \(2^{2^k}\le n\). Computational search: 0 `POWER_TWO_DEPTH_COUNTEREXAMPLE` on \(n\le 10^4\), depth 8, prescribed words to length 6, and square towers of bases \(2..30\); 99 saturating starts, 0 mixed saturations. Classification **SATURATION_BUDGET_GREEN**. Records: `docs/research/juggler_saturation_budget.md`, `docs/problems/juggler_saturation_budget.md`. Control layer unchanged
- **Refuted ideas:** mixed-word strictness remains refuted (prior phase); `PowerHeight` hierarchy; huge `cmp_pow` equality search; equality-word census
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** which words arise as traces of the even exponent maps \(e\mapsto e/2\) and \(e\mapsto 3e/2\)
- **Decision:** PROMOTE the finite saturation-budget theorem. Do not register an attack. Do not claim termination

```text
What was learned
- Exact E on a^{2^r} is a^{2^{r-1}}; exact O is a^{3·2^{r-1}} = (a^3)^{2^{r-1}}
- Both transitions drop one factor of 2 from the exponent; the image stays square iff r ≥ 2 (or the remaining base is square)
- Envelope equality of length k forces HasPowTwoDepth(n, k), hence n ≥ 2^{2^k} for n ≥ 2
- Exact steps preserve parity, so mixed words cannot saturate; all-even equality is the contracting case and is tight at 2^{2^k}
- The simple 2-adic depth invariant was not falsified; no PowerHeight datatype was required

Strongest theorem
- If a realized finite word of length k attains the floor-power envelope with equality, then the start is a 2^k-th power

Strongest refutation
- none for the budget; mixed-word strictness remains false at O, n=9

Reusable machinery
- FloorPower HasPowTwoDepth / hasPowTwoDepth_even_exact / hasPowTwoDepth_odd_exact / power_bound_eq_implies_pow_two_depth
- research.juggler_sequence.saturation_budget square-depth probe

Prior-art status
- local perfect-power budget lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Equality saturation is a finite 2-adic resource. Each exact branch spends one unit, so a k-step equality word cannot start below a 2^k-th power. Stop rather than classify equality words or add PowerHeight.

Best next question
- Which words can appear as traces of the even exponent maps e ↦ e/2 and e ↦ 3e/2, once every pre-branch exponent is required to stay even?
```

## Juggler equality-word language and parity rigidity

- **Date:** 2026-08-26
- **Objective:** Decide whether a realized finite word attaining the floor-power envelope with equality must be monochrome, \(E^k\) or \(O^k\), and whether those families are exactly the even and odd perfect-power towers
- **Hypotheses:** exact perfect-power states keep the parity of the base; therefore an equality itinerary cannot switch letters; the reverse towers realize \(E^k\) and \(O^k\)
- **Major results:** Parity of \(a^e\) **PROVED**. Exact-step parity preservation **PROVED**. Monochrome theorem `power_bound_eq_implies_monochrome` **PROVED**. Extremal iff `power_bound_eq_iff_extremal` **PROVED**: equality is exactly \(a^{2^k}\xrightarrow{E^k}a\) or \(a^{2^k}\xrightarrow{O^k}a^{3^k}\). Even minimum \(2^{2^k}\) for \(n\ge 2\); odd minimum \(3^{2^k}\) for \(n\ge 3\). Computational search: 0 `MIXED_EQUALITY_WORD_FOUND` on \(n\le 10^4\), depth 8, square towers, and prescribed mixed words. Classification **EXTREMAL_FAMILY_GREEN**. Records: `docs/research/juggler_equality_language.md`, `docs/problems/juggler_equality_language.md`. Control layer unchanged
- **Refuted ideas:** mixed-word strictness remains refuted (prior phase; one-letter equality at `O`, \(n=9\), not a both-letter word); equality-word census; `PowerHeight`; a second exponent automaton
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** exact deficit of a non-monochrome realized word relative to the weak envelope
- **Decision:** PROMOTE the monochrome language and the two extremal families. Do not register an attack. Do not claim termination

```text
What was learned
- For e ≥ 1 the parity of a^e is the parity of a, so an exact tower never changes letter
- Envelope equality forces w = E^k or w = O^k; no mixed equality word exists
- The two families are exactly a^{2^k} --E^k--> a (even a) and a^{2^k} --O^k--> a^{3^k} (odd a)
- All-even equality contracts; all-odd equality expands; both saturate the same one-sided envelope
- The simple parity invariant was not falsified; no PowerHeight or word automaton was required

Strongest theorem
- A realized finite word attains the floor-power envelope with equality if and only if it is an exact even tower or an exact odd tower

Strongest refutation
- none for the language; mixed-word strictness remains false at O, n=9

Reusable machinery
- FloorPower power_bound_eq_implies_monochrome / power_bound_eq_iff_extremal / iterate even/odd towers
- research.juggler_sequence.equality_language mixed-word probe

Prior-art status
- local equality-language lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Equality is not a free language over {E,O}. It collapses to two monochrome arithmetic extremals, which are the boundary of the existing finite-word envelope. Stop rather than census words or return to termination.

Best next question
- What exact deficit does a non-monochrome realized word have relative to the one-sided envelope?
```

## Juggler finite-word envelope defect and strictness

- **Date:** 2026-08-26
- **Objective:** Decide whether a realized non-monochrome finite word has a compositional algebraic deficit relative to the one-sided floor-power envelope, traced from the first non-exact branch
- **Hypotheses:** a positive local defect \(\delta_E\) or \(\delta_O\) persists through every suffix; the weakest useful quantitative law is \(\Delta_w(n)\ge\delta_j\); unit positivity \(\Delta\ge 1\) is only the baseline
- **Major results:** Local defects **PROVED**. `StrictPowerBound` append and suffix persistence **PROVED**. Non-monochrome \(\Rightarrow\Delta\ge 1\) **PROVED**. Deficit is monotone under even/odd continuation **PROVED**. First-defect bound \(\Delta\ge\delta_j\) through an arbitrary realized suffix **PROVED**. Probe on \(n\le 400\), depth 6: 0 unit falsifiers, 0 \(\Delta<\delta_j\), 0 suffix decreases. Classification **DEFECT_QUANTITATIVE_GREEN**. Records: `docs/research/juggler_envelope_defect.md`, `docs/problems/juggler_envelope_defect.md`. Control layer unchanged
- **Refuted ideas:** mixed-word local strictness remains refuted (prior phase; `O`, \(n=9\)); a first-defect-position order on same-count words; `PowerHeight`; a suffix-length closed form; contraction-margin upgrade
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** exact recursive \(\mathcal{D}(x,\mathrm{branch},v)\) strictly stronger than \(\delta_j\)
- **Decision:** PROMOTE the local-defect calculus and the first-defect lower bound. Do not register an attack. Do not claim termination

```text
What was learned
- δ_E(x) is the even square remainder; δ_O(x) is the isqrt remainder of x^3
- StrictPowerBound appends, so a first positive defect cannot be repaired by any suffix
- Non-monochrome realized words satisfy Δ ≥ 1, the integer complement of the extremal families
- powerDeficit is nondecreasing along every realized continuation
- The first local defect is a certified lower bound: Δ_w(n) ≥ δ_j

Strongest theorem
- If a realized word leaves an equality prefix at the first non-exact even or odd branch, then the final envelope deficit is at least that local defect

Strongest refutation
- none for the defect law; mixed-word local strictness remains false at O, n=9

Reusable machinery
- FloorPower localDefectEven/Odd, StrictPowerBound, powerDeficit, suffix deficit monotonicity
- research.juggler_sequence.envelope_defect first-defect probe

Prior-art status
- local defect lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The envelope now has a distance: equality is the two monochrome towers, and the first inexact floor step supplies a positive integer defect that every later branch preserves. Stop rather than chase a suffix-length closed form or a contraction margin.

Best next question
- Is there an exact recursive suffix defect D(x, branch, v) strictly stronger than the first local defect?
```

## Juggler first-defect bound sharpness

- **Date:** 2026-08-26
- **Objective:** Decide whether \(\Delta_w(n)\ge\delta_j\) is sharp for a nonempty suffix, or whether every later branch strictly amplifies the deficit
- **Hypotheses:** either \(|v|>0\Rightarrow\Delta>\delta_j\), or equality is a rigid exact-even suffix on \(T(n)\)
- **Major results:** Empty-prefix first step \(\Delta=\delta\) **PROVED**. Exact even continuation preserves \(\Delta\) **PROVED**. Any odd letter after a defect strictly increases \(\Delta\) **PROVED**. Nonempty exact prefix already forces \(\Delta>\delta_j\) **PROVED**. Iff characterization `power_deficit_eq_local_even_iff` / `_odd_iff` **PROVED**. Universal \(|v|>0\Rightarrow\Delta>\delta_j\) **REFUTED** at `OE`, \(n=11\) and `EE`, \(n=18\). Constructed even towers remain sharp through suffix length 3. Classification **DEFECT_SHARP_GREEN**. Records: `docs/research/juggler_defect_sharpness.md`, `docs/problems/juggler_defect_sharpness.md`. Control layer unchanged
- **Refuted ideas:** universal one-step amplification; empty suffix automatically sharp (false at `OO`, \(n=9\)); recursive suffix-defect object; `PowerHeight`; contraction-margin upgrade
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether odd starts admit arbitrarily long sharp suffixes \(OE^s\)
- **Decision:** PROMOTE the sharpness characterization. Do not register an attack. Do not claim termination. Do not add a recursive defect calculus

```text
What was learned
- The first-defect bound is already optimal: Δ = δ_j on a rigid family
- After a first defect at the start, equality holds iff the suffix is an exact even tower on T(n)
- Any odd letter, or any inexact even letter, strictly increases the deficit
- A nonempty exact prefix already makes Δ > δ_j, so |v|=0 is not automatically sharp
- Universal |v|>0 ⇒ Δ > δ_j is false; 11 OE and 18 EE are the smallest witnesses

Strongest theorem
- After a first defect at the start, the final envelope deficit equals the local defect if and only if the remaining word is an exact even tower on T(n)

Strongest refutation
- |v|>0 ⇒ Δ > δ_j fails at word OE, n=11 and word EE, n=18

Reusable machinery
- FloorPower power_deficit_eq_local_even_iff / power_deficit_eq_local_odd_iff / append equality and strictness
- research.juggler_sequence.defect_sharpness sharpness probe

Prior-art status
- local sharpness lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The first floor defect is exactly the irrecoverable global lower bound, and it is attained precisely on exact even suffixes of T(n). That is the sharp statement. Stop rather than invent a recursive defect calculus.

Best next question
- Does an odd start admit arbitrarily long exact-even sharp suffixes OE^s, or is the unbounded sharp family only the even monochrome towers?
```

## Juggler odd-start sharp even-tower suffixes

- **Date:** 2026-08-26
- **Objective:** Decide whether an odd first defect can feed an arbitrarily deep exact even tower, i.e. whether \(T(n)=a^{2^s}\) occurs for odd \(n\) and unbounded \(s\ge 2\)
- **Hypotheses:** `ODD_SHARP_SUFFIX_UNBOUNDED`, `ODD_SHARP_SUFFIX_FINITE`, or `ODD_SHARP_SUFFIX_IMPOSSIBLE`
- **Major results:** Inverse-floor `T(n)=M` iff \(M^2\le n^3<(M+1)^2\) for odd \(n\) **PROVED**. Specialization \(M=a^{2^s}\) **PROVED**. Odd first-defect scan \(n\le 50000\): 13 depth-1 hits, 0 depth \(\ge 2\). Fourth-power scan \(b\le 2500\): no odd cube; one even cube at \(b=97\), \(n=198636\). Even-start family remains unbounded. Classification **ODD_SHARP_SUFFIX_INCOMPLETE**. Records: `docs/research/juggler_odd_sharp_suffix.md`, `docs/problems/juggler_odd_sharp_suffix.md`. Control layer unchanged
- **Refuted ideas:** treating a finite empty search as impossibility; importing monochromatic equality onto the odd start (the tower is on \(T(n)\)); real `n^{3/2}` / `cmp_pow` attack; `PowerHeight`
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether a cube in a fourth-power square interval must be even
- **Decision:** PARK the depth classification. Keep the inverse-floor lemmas. Do not register an attack. Do not claim termination. Do not add a recursive defect calculus

```text
What was learned
- For odd n, T(n)=M is exactly the integer interval M^2 ≤ n^3 < (M+1)^2
- Sharp OE^s is exactly T(n)=a^{2^s} on a first-defect odd start
- Every odd first-defect hit through n=50000 has square_depth(T(n))=1
- A cube can sit in a fourth-power square interval, but the only hit found is even
- Even first defects still admit arbitrarily long exact even towers

Strongest theorem
- For odd n, T(n)=a^{2^s} if and only if a^{2^{s+1}} ≤ n^3 < (a^{2^s}+1)^2

Strongest refutation
- none for s≥2; the empty search is not a theorem. The even b=97 cube shows the interval is not automatically empty

Reusable machinery
- FloorPower floor_sqrt_eq_iff_sq_interval / floorPower_odd_eq_iff_cube_interval / floorPower_odd_eq_pow_two_depth_iff
- research.juggler_sequence.odd_sharp_suffix integer-root probe

Prior-art status
- inverse-floor packaging of Nat.sqrt, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PARK

Why
- The odd-start sharp family is reduced to a clean Diophantine interval, and every cheap integer-root search is consistent with only OE, but no obstruction was proved and no s≥2 witness appeared. Stop rather than build a number-theory framework around an unproved gap.

Best next question
- Must a cube in [b^8,(b^4+1)^2) be even, or is there an odd witness?
```

## Juggler FloorPower paper-ready packaging

- **Date:** 2026-08-26
- **Objective:** Make `Problems.Engine.FloorPower` paper-ready (unique proofs, glue, section order) and retry the parked odd-start \(s\ge 2\) question
- **Hypotheses:** specialized OOOEE/OOOEEEOO proofs are instances of `power_bound_contracts`; cubes in \([b^8,(b^4+1)^2)\) are even unless exact
- **Major results:** `floorPower` now uses `n^3`. Shared exponent rewrites (`two_pow_succ`, `three_pow_succ`, `pow_three_succ_right`). `follows_wordOOOEE_iff` / `follows_wordOOOEEEOO_iff`; nested-hyp block lemmas are wrappers. Glue: `floorPower_even_eq_iff_sq_interval`, `localTight_*_iff_square`, `even_word_contracts`, `odd_word_expands`. No `sorry`. Extended search: fourth powers \(b\le 20000\) still one inexact cube (`b=97`, even \(n=198636\)); odd starts \(n\le 200000\) still max depth 1. No elementary \(s\ge 2\) obstruction. Reserved `floorPower_odd_pow_two_depth_ge_two_false` remains absent. Classification still **ODD_SHARP_SUFFIX_INCOMPLETE**. No ledger row. Control layer unchanged
- **Refuted ideas:** treating the still-empty odd search as impossibility; adding `PowerHeight`; expanding `lean_export.py` beyond the seed-13 trio; reopening Phase 11 as a macro grammar
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether a cube in a fourth-power square interval must be even
- **Decision:** PROMOTE the packaging and glue. PARK the \(s\ge 2\) depth classification again. Do not register an attack. Do not claim termination

```text
What was learned
- OOOEE / OOOEEEOO nested-hyp theorems are definitionally the follows predicates
- The one-step map is cleaner as Nat.sqrt / Nat.sqrt (n^3)
- Even equality words of length k≥1 contract; odd equality words of length k≥1 expand for n≥3
- b=97 remains the only inexact fourth-power cube through b=20000
- No odd s≥2 hit through n=200000; no short integer obstruction appeared

Strongest theorem
- power_bound_eq_iff_extremal and the first-defect sharpness iff remain the headline results; the new statements are glue

Strongest refutation
- none for s≥2; the even b=97 cube is still the only inexact interval hit

Reusable machinery
- FloorPower paper sections; follows_word iff wrappers; even/odd inverse-floor pair
- even_word_contracts / odd_word_expands

Prior-art status
- local floor-power envelope, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE the Lean packaging; PARK the odd-start Diophantine

Why
- The existing theory is now a single narrative with unique proofs. The parked interval question is unchanged: empty search is not a theorem, and no elementary evenness law was found.

Best next question
- Must a cube in [b^8,(b^4+1)^2) be even, or is there an odd witness?
```

## Juggler defect-compensated contraction

- **Date:** 2026-08-26
- **Objective:** Decide whether a mixed realized word with \(3^o>2^k\) can still contract because floor defect exceeds the formal gap \(n^{3^o}-n^{2^k}\)
- **Hypotheses:** `COMPENSATED_CONTRACTION_FOUND`, `COMPENSATION_FIRST_DEFECT_SUFFICIENT`, `POSITIVE_DRIFT_NONCONTRACTION`, or `NO_USEFUL_COMPENSATION`
- **Major results:** Certificate `power_bound_compensated_contracts` **PROVED**. `EOO` contracts iff \(n\in\{2,12,14\}\) **PROVED**. First local defect never exceeds the \((k,o)=(3,2)\) formal gap **PROVED**. `OOE`/`OEO` produced no contraction on the scanned odd window. Classification **COMPENSATED_CONTRACTION_FOUND**. Records: `docs/research/juggler_compensated_contraction.md`, `docs/problems/juggler_compensated_contraction.md`. Control layer unchanged
- **Refuted ideas:** first-defect-only compensation \(\delta_j>G\) on the shortest mixed positive-drift family; treating \(\Delta>G\) as new arithmetic rather than a packaging of contraction; opening a lower-envelope theory; reopening parked \(OE^s\)
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether `OOE`/`OEO` never contract, or whether an infinite mixed positive-drift contraction family exists
- **Decision:** PROMOTE the certificate and the finite `EOO` classification. Do not register an attack. Do not claim termination. Do not add a lower envelope

```text
What was learned
- Formal drift 3^o > 2^k is not a complete predictor of block direction
- Δ > G is equivalent to contraction for n ≥ 2 and packages a reusable certificate
- The first local defect never supplies G for (k,o)=(3,2)
- EOO contracts exactly at 2, 12, 14; n=10 realizes EOO and expands
- OOE and OEO did not contract on the scanned window

Strongest theorem
- follows n EOO implies (T^3(n) < n ↔ n = 2 ∨ n = 12 ∨ n = 14)

Strongest refutation
- first-defect sufficiency δ_j > G fails at every EOO witness (n=2: δ=1 < 256=G)

Reusable machinery
- FloorPower power_bound_compensated_contracts / floorPower_eoo_contracts_iff
- research.juggler_sequence.compensated_contraction bounded exact probe

Prior-art status
- local finite-word direction, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The shortest mixed positive-drift word yields a finite compensated-contraction family and a reusable deficit-versus-gap certificate. First-defect-only compensation is false here, so the phase stops rather than building a suffix-amplification calculus.

Best next question
- Do OOE and OEO never contract, or is there an infinite mixed positive-drift contraction family?
```

## Juggler EOO square-root cell mechanism

- **Date:** 2026-08-26
- **Objective:** Replace the enumerated `EOO` contraction set \(\{2,12,14\}\) by an exact square-root cell threshold on \(q=\lfloor\sqrt n\rfloor\)
- **Hypotheses:** `EOO_CELL_MECHANISM_GREEN`, `EOO_CELL_COUNTEREXAMPLE`, `COMPENSATED_PATTERN_FOUND`, `COMPENSATED_EOO_ISOLATED`, or `POSITIVE_DRIFT_CONTRACTION_FAMILY`
- **Major results:** On a realized `EOO` start, \(T^3(n)=\mathrm{eooCellOutput}\,q\) and contracts iff \(n>c(q)\) **PROVED**. Only \(q=1,3\) have \(c<(q+1)^2\). `OOE`/`OEO` vary on n-sqrt cells. `EOOO` uses the same first-even freeze but contracts only at \(n=2\). Classification **EOO_CELL_MECHANISM_GREEN**. Records: `docs/research/juggler_eoo_cell_mechanism.md`, `docs/problems/juggler_eoo_cell_mechanism.md`. Control layer unchanged
- **Refuted ideas:** `OOE`/`OEO` freeze on the start square-root cell; a three-point residue pattern beyond “same cell, \(n>c\)”; an infinite length-4 mixed contraction family on the scanned window; turning the generic \(\Delta>G\) certificate into a word-specific tactic
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether `OOE`/`OEO` never contract, or whether a first-even positive-drift word has \(c(q)\) strictly inside \((q^2,(q+1)^2)\) for infinitely many odd \(q\)
- **Decision:** PROMOTE the cell/threshold classification. Do not register an attack. Do not claim termination. Do not add a generic cell calculus

```text
What was learned
- EOO output is constant on each square-root cell [q^2, (q+1)^2)
- Contraction is the threshold n > eooCellOutput q, not a huge power comparison
- Only q=1 (c=1 → n=2) and q=3 (c=11 → n=12,14) intersect that threshold
- OOE and OEO do not freeze on n-sqrt cells; the first even step is the specializer
- EOOO has the same first-even freeze, but the extra odd step pushes q=3 to 36 > 16

Strongest theorem
- follows n EOO implies (T^3(n) < n ↔ eooCellOutput ⌊√n⌋ < n)

Strongest refutation
- OOE/OEO constancy on the start square-root cell is false; first-odd words vary inside the cell

Reusable machinery
- FloorPower eooCellOutput / eoo_contracts_on_cell / follows_eoo_sqrt_iff
- research.juggler_sequence.eoo_cell_mechanism cell scan

Prior-art status
- local finite-word cell classification, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The enumerated set {2,12,14} is the overlap of EOO-realizable even integers in the cells q=1,3 with the threshold n>c(q). For q≥5 the cell output already meets or exceeds the next square, so no further EOO start contracts.

Best next question
- Prove OOE/OEO never contract, or find a first-even positive-drift word whose cell output sits strictly inside (q^2,(q+1)^2) for infinitely many odd q
```

## Juggler floor-cell geometry

- **Date:** 2026-08-26
- **Objective:** Decide whether EOO is an isolated cell trick or the first-even freeze \(T_{Ev}(n)=T_v(\lfloor\sqrt n\rfloor)\) is a reusable geometric law
- **Hypotheses:** `FIRST_E_FREEZE_GREEN`, `CELL_CALCULUS_GREEN`, `CELL_FAMILY_FOUND`, `CELL_GEOMETRY_TOO_EXPENSIVE`, or `CELL_DUALITY_COUNTEREXAMPLE`
- **Major results:** First-even freeze and first-even contraction threshold **PROVED**. Odd floor cells contain at most one integer **PROVED**. `EOO` is the mixed-cell case; `EEOOOO` is an entire-cell case at \(n\in\{4,6,8\}\). No parametrized positive-drift family on the scanned window. Classification **FIRST_E_FREEZE_GREEN**. Records: `docs/research/juggler_floor_cells.md`, `docs/problems/juggler_floor_cells.md`. Control layer unchanged
- **Refuted ideas:** a useful odd-start freeze on a wide cell; a recursive cell tree as the next necessary object; an infinite first-even positive-drift contraction family in length \(\le6\)
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether only finitely many first-even positive-drift cells can mix or all-contract; whether `OOE`/`OEO` never contract
- **Decision:** PROMOTE the freeze and odd-cell uniqueness. Do not add a cell tree. Do not register an attack. Do not claim termination

```text
What was learned
- Every realized Ev word satisfies T_Ev(n)=T_v(⌊√n⌋) on the square-root cell
- Contraction is the threshold T_v(q)<n, with a trichotomy all-contract / mixed / all-expand
- Odd cells contain at most one n, so an initial O does not freeze a range
- EOO is mixed at q=1,3; EEOOOO is entire-cell at q=2 (n=4,6,8)
- A recursive partition is not justified: one E already freezes, and O refines to singletons

Strongest theorem
- follows n (even :: v) implies (T^{|v|+1}(n) < n ↔ T^{|v|}(⌊√n⌋) < n)

Strongest refutation
- odd floor cells are never wider than one integer, so the anticipated E/O duality holds exactly

Reusable machinery
- FloorPower first_even_freeze / first_even_contracts_iff / odd_cell_unique
- research.juggler_sequence.floor_cells

Prior-art status
- local finite-word cell identity, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The EOO list is the mixed-cell case of a generic first-even identity. Odd-start words fail to freeze because their primitive cells are singletons, not because the freeze formula is false. No cell tree is required.

Best next question
- Prove there are only finitely many first-even positive-drift contraction cells, or find a suffix that stays below the next square for infinitely many q
```

## Juggler first-even thresholds

- **Date:** 2026-08-26
- **Objective:** Decide whether \(Q_v=\{q:T_v(q)<(q+1)^2\}\) is finite for positive-drift first-even suffixes
- **Hypotheses:** `FIRST_E_FINITE_GREEN`, `FIRST_E_THRESHOLD_GREEN`, `FIRST_E_INFINITE_FAMILY`, `FIRST_E_THRESHOLD_COUNTEREXAMPLE`, or `FIRST_E_MECHANISM_TOO_LOCAL`
- **Major results:** Exact any-contraction is \(c+1<(q+1)^2\) **PROVED**. Whole-cell contraction is \(c<q^2\) **PROVED**. \(Q_{OO}=\{1,3\}\) with threshold \(q\ge5\) **PROVED**. \(Q_{OOO}=\{1\}\) with threshold \(q\ge3\) **PROVED**. \(Q_O\) is all odd \(q\), but \(\alpha=3/2\le2\). Classification **FIRST_E_FINITE_GREEN**. Records: `docs/research/juggler_first_even_thresholds.md`, `docs/problems/juggler_first_even_thresholds.md`. Control layer unchanged
- **Refuted ideas:** deriving finiteness from the one-sided upper envelope; treating \(c<(q+1)^2\) as the exact integer any-contraction test; reading \(Q_O=\mathbb{N}_{\mathrm{odd}}\) as a compensated positive-drift family
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether every suffix with \(\alpha_v>2\) is eventually above \((q+1)^2\)
- **Decision:** PROMOTE the interval law and the OO/OOO finiteness theorems. Do not open a generic lower envelope. Do not claim termination

```text
What was learned
- Any contraction on [q^2,(q+1)^2) is c+1<(q+1)^2; whole-cell is c<q^2
- Ev is formally expanding iff the suffix satisfies α_v>2
- Q_OO={1,3} and Q_OOO={1} by eventual thresholds, not by census
- A later odd step is nondecreasing, so OOO inherits the OO bound
- Q_O is infinite because α=3/2<2; that is formal contraction of EO

Strongest theorem
- follows q OO and q≥5 imply T^2(q) ≥ (q+1)^2; follows q OOO and q≥3 imply T^3(q) ≥ (q+1)^2

Strongest refutation
- the one-sided power envelope cannot prove these lower bounds; Q_O infinite is not a positive-drift family

Reusable machinery
- FloorPower cell_any_contracts_iff / oo_suffix_threshold / ooo_suffix_threshold
- research.juggler_sequence.first_even_thresholds

Prior-art status
- local finite-word threshold, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The EOO and EOOO contraction starts are the realized points of two finite Q_v, now with explicit eventual bounds. Suffixes with α≤2 can have large Q_v, but those words are not formally expanding.

Best next question
- Prove eventual non-contraction for every suffix with α_v>2, or find one such suffix with unbounded Q_v
```

## Juggler superquadratic suffixes

- **Date:** 2026-08-26
- **Objective:** Prove or refute that every fixed suffix \(v\) with \(\alpha_v>2\) has finite first-even contraction set \(Q_v\)
- **Hypotheses:** `FIRST_E_EVENTUAL_NONCONTRACTION_GREEN`, `LOWER_GROWTH_COMPOSITION_GREEN`, `SUPERQUADRATIC_COUNTEREXAMPLE`, or `LOWER_BOUND_TECHNIQUE_TOO_WEAK`
- **Major results:** Coarse bound \(n<4\cdot n.\mathrm{sqrt}^2\) **PROVED**. `LowerPowerBound` composes along any realized word **PROVED**. Eventual \(T_v(q)\ge(q+1)^2\) for each fixed \(v\) with \(3^{\#O(v)}>2^{|v|+1}\) **PROVED**. No finite word has \(\alpha_v=2\) **PROVED**. Scan of superquadratic words of length \(\le5\) found only \(Q_v\subseteq\{1,2,3\}\). Classification **FIRST_E_EVENTUAL_NONCONTRACTION_GREEN**. Records: `docs/research/juggler_superquadratic_suffixes.md`, `docs/problems/juggler_superquadratic_suffixes.md`. Control layer unchanged
- **Refuted ideas:** deriving the threshold from the one-sided upper envelope; a critical \(\alpha_v=2\) regime for finite words; a uniform-in-\(v\) threshold
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether changing superquadratic suffixes can still produce infinitely many first-even contraction cells; whether a uniform bound exists for \(\alpha_v\ge2+\varepsilon\)
- **Decision:** PROMOTE the fixed-word lower-growth theorem. Keep exact OO/OOO classifications. Do not open a generic lower-envelope theory. Do not claim termination

```text
What was learned
- 4 T^2 beats n (even) and n^3 (odd) for every n≥1
- These compose to q^{3^o} ≤ D_v T_v(q)^{2^r} for a word-dependent D_v
- The integer gap 3^o > 2^{r+1} then beats (q+1)^2 for large q
- No finite word has α_v=2, because 3^o is odd
- Exact OO/OOO bounds remain much sharper than the coarse Q0(v)

Strongest theorem
- 2^{|v|+1} < 3^{#O(v)} implies ∃ Q0(v) ∀ q≥Q0(v), follows q v → T_v(q) ≥ (q+1)^2

Strongest refutation
- the upper envelope cannot prove this; α_v=2 never occurs

Reusable machinery
- FloorPower LowerPowerBound / lower_growth_word / eventually_no_first_even_contraction
- research.juggler_sequence.superquadratic_suffixes

Prior-art status
- local fixed-word threshold, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Compensated contraction for any one formally expanding first-even word Ev is a finite-cell phenomenon. The proof is a coarse integer lower bound, not a new envelope theory.

Best next question
- Can changing superquadratic suffixes still produce infinitely many first-even contraction cells, or is there a uniform threshold for α_v≥2+ε?
```

## Juggler uniform superquadratic thresholds

- **Date:** 2026-08-26
- **Objective:** Prove or refute a threshold \(Q(\varepsilon)\) for all suffixes with \(\alpha_v\ge 2+\varepsilon\)
- **Hypotheses:** `UNIFORM_MARGIN_GREEN`, `UNIFORM_LENGTH_MARGIN_GREEN`, `UNIFORM_CONSTANT_ARTIFACT`, `CHANGING_SUFFIX_COUNTEREXAMPLE`, or `NO_USEFUL_UNIFORMITY`
- **Major results:** Short-word \(q_{\max}\) is not controlled by \(\varepsilon_v\) alone **COMPUTATIONALLY VERIFIED**. `lowerDenom` depends on letter order **OBSERVATION**. Discrete gap \(3^o-2^{r+1}\ge 1\) **PROVED**. Family \(v_k=E^kO^{3k}\) at \(q_k=2^{2^{k-1}}\) collapses onto \(1\) and contracts for arbitrarily large \(q\) **PROVED**. Classification **CHANGING_SUFFIX_COUNTEREXAMPLE**. Records: `docs/research/juggler_uniform_thresholds.md`, `docs/problems/juggler_uniform_thresholds.md`. Control layer unchanged
- **Refuted ideas:** a threshold depending only on the exponent margin \(\varepsilon\); restoring uniformity by improving the coarse \(4T^2\) constants; treating \(D_v\) as the essential obstruction
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether a residual uniform bound survives after excluding even-tower collapses onto a small state
- **Decision:** PROMOTE the changing-suffix family theorem. Close \(\varepsilon\)-only uniformity as REFUTED. Keep the fixed-word theorem. Do not open a lower-envelope theory. Do not claim termination

```text
What was learned
- q_max on short superquadratic words stays in {1,2,3} and is not monotone in ε
- D_v depends on letter order (late odds cube a larger D), but that is not why Q(ε) fails
- An even tower maps 2^{2^{k-1}} onto 1; any odd tail then stays at 1
- The family E^k O^{3k} is superquadratic for k≥2 and contracts at arbitrarily large q
- Q(ε,r) is true by finiteness of length-r words, but must be at least 2^{2^{k-1}}

Strongest theorem
- ∀ N ∃ k o q v: N≤q, 2^{|v|+1}<3^{#O(v)}, v=E^k O^o, follows q v, and T_v(q)+1<(q+1)^2

Strongest refutation
- no Q(ε) exists; even α=(27/16)^k→∞ fails on the even-tower collapse family

Reusable machinery
- FloorPower even_tower_odd_tail_contracts / changing_suffix_unbounded_contraction
- research.juggler_sequence.uniform_superquadratic

Prior-art status
- local family counterexample, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The remaining loophole of the fixed-word theorem was a changing suffix v=v_q. A uniform superquadratic margin does not close it: a long even prefix can collapse a huge perfect power of two onto 1.

Best next question
- If suffixes that collapse a large even tower onto a small state are excluded, does any residual uniform bound remain?
```

## Juggler collapse normalization

- **Date:** 2026-08-26
- **Objective:** Formalize \(T_{E^r u}(a^{2^r})=T_u(a)\) and test whether bounded initial even-run depth restores family non-contraction
- **Hypotheses:** `COLLAPSE_NORMALIZATION_GREEN`, `COLLAPSE_DEPTH_SUFFICIENT`, `COLLAPSE_DEPTH_TOO_WEAK`, `COLLAPSE_COUNTEREXAMPLE`, or `COLLAPSE_NORMALIZATION_INSUFFICIENT`
- **Major results:** Decomposition \(v=E^{r(v)}u(v)\) **PROVED**. Residual identity and exact-tower evaluation at \(a\) **PROVED**. \(E^kO^{3k}\) is \(O^{3k}\) on residual \(1\) **PROVED**. Bounded initial even-run **REFUTED**: `OEEE` plus nine odds at \(q=7\) **PROVED**; scanned \(OE^kO^{3k}\) contracts at \(q=345\) (\(k=4\)) and \(q=19955\) (\(k=5\)). Classification **COLLAPSE_DEPTH_TOO_WEAK**. Records: `docs/research/juggler_collapse_normalization.md`, `docs/problems/juggler_collapse_normalization.md`. Control layer unchanged
- **Refuted ideas:** initial even-run length as a sufficient collapse complexity; restoring \(Q(R)\) from a bound on the leading `E`s alone
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether a bound on the longest even run anywhere restores a family threshold
- **Decision:** PROMOTE the residual identity and the initial-run refutation. Do not add a collapse algebra. Do not claim termination

```text
What was learned
- E^r u on a^{2^r} is exactly u on a, for even a that realize u
- First-even contraction on that tower cell is T_u(a)+1 < (a^{2^r}+1)^2
- The E^k O^{3k} family is residual evaluation at 1 after k square roots
- An odd letter followed by a long even run can collapse large q onto 1
- Initial even-run length 0 is not a family bound; the extra parameter is the longest even run

Strongest theorem
- even a and follows a u imply T_{E^r u}(a^{2^r}) = T_u(a)

Strongest refutation
- q=7 follows OEEE plus nine odds, is superquadratic, has initial even-run 0, and contracts

Reusable machinery
- FloorPower initialEvenRun / collapse_on_pow_two / odd_even_tower_seven
- research.juggler_sequence.collapse_normalization

Prior-art status
- local collapse identity, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The missing state for changing families is scale collapse, but the collapse need not sit at the start of the word. Bounding only the leading E-run leaves an internal even basin that still feeds 1.

Best next question
- Does a bound on the longest even run restore family-level first-even non-contraction for superquadratic suffixes?
```

## Juggler internal even-run collapse

- **Date:** 2026-08-27
- **Objective:** Explain changing-family contraction by internal even-run collapse, and test whether bounded `maxEvenRun` restores a useful family bound
- **Hypotheses:** `INTERNAL_COLLAPSE_NORMALIZATION_GREEN`, `BOUNDED_RUN_COUNTEREXAMPLE`, `NUMERIC_COLLAPSE_COUNTEREXAMPLE`, `COLLAPSE_COMPRESSION_GREEN`, or `GLOBAL_COLLAPSE_OBSTRUCTION_GREEN`
- **Major results:** Medial identity \(T_{uE^rv}=T_v\circ T_{E^r}\circ T_u\) **PROVED**. Basin \(T_{O^s}(1)=1\) **PROVED**. Nested `maxEvenRun=3` word at \(q=2500\) lands on \(1\) **PROVED**. Further nests at \(q=6250000\) and a 121-bit \(q\) **COMPUTATIONALLY VERIFIED**. Short \(T>1\) contraction only `OO` at \(q=3\). Classification **BOUNDED_RUN_COUNTEREXAMPLE**. Records: `docs/research/juggler_internal_collapse.md`, `docs/problems/juggler_internal_collapse.md`. Control layer unchanged
- **Refuted ideas:** a useful \(Q(R)\) from syntactic `maxEvenRun ≤ R`; treating initial-run length and max-run length as interchangeable family bounds
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether every large superquadratic contraction requires an even run into an inert basin with unbounded entry/exit ratio
- **Decision:** PROMOTE the internal-run identity and the nested R=3 family. Do not add a collapse tree. Do not claim termination

```text
What was learned
- A medial even run is residual evaluation at its exit state
- 1 is inert under any odd tail; 3 grows under odds
- Nested E^3 O blocks keep maxEvenRun=3 while lifting q from 7 to 2500 to 6.25e6 to 121 bits
- Short-word q_max for maxE≤2 stays small only because a second stacked run is absent
- Large changing-family contractions on the scan are collapse-to-1, not generic α-growth

Strongest theorem
- follows 2500 (EE ++ OEEE ++ O^12), the word is superquadratic with maxEvenRun=3, and T=1

Strongest refutation
- maxEvenRun=3 does not give a useful family threshold; q can have 121 bits

Reusable machinery
- FloorPower maxEvenRun / internal_even_collapse / nested_even_collapse_2500
- research.juggler_sequence.internal_collapse

Prior-art status
- local collapse mechanism, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Changing families defeat fixed-word bounds by feeding a large state into an even run that exits at 1. Bounding the length of those runs does not bound the entry state, because an extra even run can be stacked in front.

Best next question
- Must every large superquadratic first-even contraction contain an even run that lands in an inert basin with unbounded entry/exit ratio?
```

## Juggler descent and capture certificates

- **Date:** 2026-08-27
- **Objective:** Normalize changing-family collapses as capture into \(\{1\}\) and pair them with descent as a local progress calculus
- **Hypotheses:** `CAPTURE_NORMALIZATION_GREEN`, `CAPTURE_BASIN_ONE_GREEN`, `ESCAPE_NOT_CAPTURED`, `DESCENT_CAPTURE_FRAMEWORK_GREEN`, or `ESCAPE_FAMILY_FOUND`
- **Major results:** `Capture`/`Descent`/`ReachesOne` **PROVED**. Capture composes through an arbitrary prefix **PROVED**. \(E^kO^{3k}\), `OEEE` at \(q=7\), and the nested \(q=2500\) word are capture **PROVED**. First-even cell capture when \(T_v(q)=1\) **PROVED**. A minimal non-1 value admits neither certificate **PROVED**. Short `EOO` at \(12,14\) is descent, not capture. Classification **DESCENT_CAPTURE_FRAMEWORK_GREEN**. Records: `docs/research/juggler_capture_certificates.md`, `docs/problems/juggler_capture_certificates.md`. Control layer unchanged
- **Refuted ideas:** treating large changing-family contractions as generic compensated descent; enlarging the basin beyond \(\{1\}\) for the known families
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** structural constraints on a hypothetical infinite `NO_CERTIFICATE` path
- **Decision:** PROMOTE the descent/capture calculus. Keep \(S=\{1\}\). Do not claim every trajectory contains a certificate. Do not claim termination

```text
What was learned
- Large changing-family collapses are capture into {1}, not mere contraction
- Capture composes: a prefix plus a residual capture is a capture
- Short EOO at 12 and 14 is descent to 11; small is not inert (3→5→11→36)
- On a first-even cell, T_v(q)=1 is cell capture
- A hypothetical minimal n that never reaches 1 admits no descent and no capture

Strongest theorem
- Capture n u and Capture (T_u n) v imply Capture n (u++v); a minimal non-1 n admits neither Descent nor Capture

Strongest refutation
- none of the large collapse families escape {1}; EOO 12/14 are descent, which the framework already names

Reusable machinery
- FloorPower Capture / Descent / capture_of_suffix / minimal_avoids_progress
- research.juggler_sequence.capture_certificates

Prior-art status
- local certificate calculus, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The scale-collapse loophole is a machine-checkable capture certificate. Together with descent, that is the first exact vocabulary for what a hypothetical minimal counterexample must avoid.

Best next question
- What structural constraints would an infinite NO_CERTIFICATE path have to satisfy?
```

## Juggler no-progress path structure

- **Date:** 2026-08-27
- **Objective:** Derive necessary structure for a hypothetical infinite `NO_CERTIFICATE` Juggler prefix from existing descent/capture certificates
- **Hypotheses:** `NO_PROGRESS_STRUCTURE_GREEN`, `COLLAPSE_WITHOUT_CAPTURE_COUNTEREXAMPLE`, or `DEFECT_RESET_COUNTEREXAMPLE`
- **Major results:** `ReachesOne` closed backward along images **EXACT — LEAN VERIFIED**. \(2,4,6,8\) are `ReachesOne` **EXACT — LEAN VERIFIED**. A non-1 value cannot visit any `ReachesOne` image, even one \(\ge n\) **EXACT — LEAN VERIFIED**. A nonempty even prefix at \(n\ge 2\) is `Descent` **EXACT — LEAN VERIFIED**. A minimal non-1 \(n\ge 3\) is odd **EXACT — LEAN VERIFIED**. `OOOE` at \(3\) and `OOE` at \(5\) land at \(6\) (`NO_CERTIFICATE` as blocks, `ReachesOne`-implied). `OOE` at \(9\) lands at uncertified \(11\); no defect reset on \(n\le 80\). Classification **NO_PROGRESS_STRUCTURE_GREEN**. Records: `docs/research/juggler_no_progress_paths.md`, `docs/problems/juggler_no_progress_paths.md`. Control layer unchanged
- **Refuted ideas:** treating Phase A as the full obstruction; enlarging `Capture` beyond \(\{1\}\); a new coinductive path type
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** after an uncertified collapse to \(y\ge n\), must a later residual become descent, capture, or cheap-`ReachesOne` implied?
- **Decision:** PROMOTE the extra constraint \(C\). Keep \(S=\{1\}\). Do not claim every uncertified collapse has a bounded sequel. Do not claim termination

```text
What was learned
- ReachesOne is closed backward: visiting any certified state, not only [1, n), is fatal
- Landing at 2, 4, 6, or 8 is already ReachesOne; the capture basin stays {1}
- OOE at 5 lands at 6: not Descent, not Capture, still forbidden
- Even prefixes at n>=2 are Descent; a minimal non-1 n>=3 starts odd
- Uncertified y>=n collapses exist (OOE at 9 to 11) and can be large (OOOOE at 37 to 9317); no defect reset on the scan

Strongest theorem
- If not ReachesOne n, then not ReachesOne (image n w); a nonempty even word at n>=2 is Descent

Strongest refutation
- the claim that every even collapse to m>1 is already Descent, Capture, or cheap ReachesOne; OOE at 9 lands at 11

Reusable machinery
- FloorPower two_reachesOne / reachesOne_of_image / minimal_avoids_reachesOne_image / even_word_descent
- research.juggler_sequence.no_progress_paths

Prior-art status
- local obstruction refinement, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- C is strictly stronger than minimal_avoids_progress. A prefix can stay at or above n and still be fatal if its image is a certified ReachesOne state.

Best next question
- After an uncertified collapse to y>=n, must a later residual become Descent, Capture, or cheap-ReachesOne implied, with any bound depending only on y?
```

## Juggler residual progress

- **Date:** 2026-08-27
- **Objective:** Identify a useful residual class \(R\) such that a bounded prefix from \(y\in R\) is Descent or `ReachesOne`, starting from known uncertified collapses
- **Hypotheses:** `RESIDUAL_PROGRESS_GREEN`, `RESIDUAL_ESCAPE_FOUND`, or `SMALL_RESIDUAL_CORE_FOUND`
- **Major results:** \(1\le y<12\) is `ReachesOne` **EXACT — LEAN VERIFIED**. Even \(1\le y<144\) is `ReachesOne` **EXACT — LEAN VERIFIED**. Image in \(\{1,\ldots,11\}\) is fatal **EXACT — LEAN VERIFIED**. A positive non-1 value is at least \(12\). Calibration residuals `11` and `9317` locally descend from \(y\). \(9\to 11\) is now `ReachesOne`-implied. No uniform \(L\) on all of \(\mathbb{N}\) (`193` needs \(70\) steps). Classification **RESIDUAL_PROGRESS_GREEN**. Records: `docs/research/juggler_residual_progress.md`, `docs/problems/juggler_residual_progress.md`. Control layer unchanged
- **Refuted ideas:** a uniform `ProgressWithin` bound for every positive integer; enlarging `Capture` beyond \(\{1\}\); a new residual-path datatype
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** must a residual \(y\ge 144\) eventually land in an even state below \(144\)?
- **Decision:** PROMOTE the finite class \(R=\{1,\ldots,11\}\) and the even-below-\(144\) corollary. Keep \(S=\{1\}\). Do not claim a uniform bound for every \(y\). Do not claim termination

```text
What was learned
- The useful R is the initial segment {1,...,11}, not all of N
- Even residuals below 144 are ReachesOne by one even step into that segment
- 9→11 is now ReachesOne-implied; 11 and 9317 locally descend from y
- No uniform L: 193 first hits R at step 70
- Renewal T^r(y)<n held on the n≤80 uncertified list; that is not a theorem

Strongest theorem
- If 1 ≤ y < 12 then ReachesOne y; if y is even and 1 ≤ y < 144 then ReachesOne y

Strongest refutation
- ProgressWithin(y,L) for a single L and every y; 193 requires 70 steps to hit R

Reusable machinery
- FloorPower reachesOne_of_lt_twelve / image_lt_twelve_reachesOne / even_lt_sq_twelve_reachesOne
- research.juggler_sequence.residual_progress

Prior-art status
- finite residual-class certificate, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- R strictly enlarges the cheap {2,4,6,8} set and swallows the minimized uncertified residual 11. Capture still means image 1.

Best next question
- Must a residual y≥144 eventually land in an even state below 144, with any bound depending only on y?
```

## Juggler even-run scale barriers

- **Date:** 2026-08-27
- **Objective:** Convert minimality into an exact scale lower bound on even runs, without claiming the orbit is all-odd
- **Hypotheses:** `EVEN_SCALE_BARRIER_GREEN`, `MINIMAL_NORMAL_FORM_GREEN`, or `INTERNAL_COLLAPSE_BELOW_MINIMAL`
- **Major results:** `MinimalNonTerm` **EXACT — LEAN VERIFIED**. An \(E^r\) run on a minimal non-1 orbit has entry \(\ge n^{2^r}\) **EXACT — LEAN VERIFIED**. The start is odd, at least \(12\), and its first image is odd **EXACT — LEAN VERIFIED**. Finite-prefix normal form **EXACT — LEAN VERIFIED**. Changing-family towers cannot lie on the orbit. Classification **MINIMAL_NORMAL_FORM_GREEN**. Records: `docs/research/juggler_even_scale_barrier.md`, `docs/problems/juggler_even_scale_barrier.md`. Control layer unchanged
- **Refuted ideas:** “minimal counterexample orbit is all-odd”; enlarging `Capture`; a halt theorem
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** after the first odd run grows past \(n^2\), must the first even residual fall below \(n\), or can it land in \([n,\infty)\)?
- **Decision:** PROMOTE the scale barrier and the finite-prefix normal form. Do not claim an all-odd orbit. Do not claim termination

```text
What was learned
- Minimality is a scale constraint, not an all-odd constraint
- E^r on a minimal non-1 orbit forces entry >= n^{2^r}; the exit stays >= n
- The start is odd and the first image is odd; later even states are allowed at scale >= n^2
- OE at the start is descent; changing-family collapses to 1 cannot occur on the orbit
- Ordinary orbits do visit even states above the start (e.g. 3→36)

Strongest theorem
- If MinimalNonTerm n and an E^r run occurs at a later state m, then n^{2^r} <= m

Strongest refutation
- the claim that a minimal non-1 orbit must be all-odd

Reusable machinery
- Problems.Engine.MinimalNonTerm even_run_scale_barrier / minimal_counterexample_normal_form
- research.juggler_sequence.even_scale_barrier

Prior-art status
- conditional scale obstruction, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The even branch plus minimality gives an exact numerical barrier. That is the first global restriction on how a hypothetical counterexample may collapse.

Best next question
- After the first odd run has grown past n^2, must the first even residual fall below n, or can it land in [n, ∞)?
```

## Juggler repeated OE scale budget

- **Date:** 2026-08-27
- **Objective:** Quantify the scale cost of consecutive `OE` blocks on a hypothetical minimal non-1 orbit
- **Hypotheses:** `REPEATED_OE_SCALE_GREEN`, `OE_RUN_FORBIDDEN_GREEN`, or `BLOCK_SCALE_COUNTEREXAMPLE`
- **Major results:** `T^2(x)^4 ≤ x^3` and \(T^{2r}(x)^{4^r}\le x^{3^r}\) **EXACT — LEAN VERIFIED**. On a `MinimalNonTerm` orbit, \(n^{4^r}\le x^{3^r}\) **EXACT — LEAN VERIFIED**. \((\texttt{OE})^r\) cannot start at \(n_*\) **EXACT — LEAN VERIFIED**. No envelope or scale failure on \(n\le 80\). Longest stay-\(\ge n\) consecutive run is \(r=2\) at \(x=17537\) on the orbit of \(77\). Classification **REPEATED_OE_SCALE_GREEN**. Records: `docs/research/juggler_repeated_oe.md`, `docs/problems/juggler_repeated_oe.md`. Control layer unchanged
- **Refuted ideas:** an `OE` frequency theorem; a uniform \(r\) independent of \(x\); a halt theorem
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** what lower bound on the odd-run length \(a\) in \(O^aE\) does minimality impose before the first legal even residual?
- **Decision:** PROMOTE the repeated-`OE` scale barrier. Do not claim every orbit contains many `OE` blocks. Do not claim termination

```text
What was learned
- One OE block is the word envelope T^2(x)^4 ≤ x^3; (OE)^r is T^{2r}(x)^{4^r} ≤ x^{3^r}
- Minimality converts that into n^{4^r} ≤ x^{3^r}
- (OE)^r cannot start at n_* because the first image is odd
- Consecutive OE can stay above n (77: 17537 --(OE)^2--> 243); r is not uniformly bounded
- This is a scale budget, not a frequency theorem

Strongest theorem
- If MinimalNonTerm n and (OE)^r occurs at a later state x, then n^{4^r} ≤ x^{3^r}

Strongest refutation
- a uniform bound on consecutive OE length independent of x; r=2 stays above 77

Reusable machinery
- Problems.Engine.RepeatedOE repeated_oe_scale_barrier / oe_requires_scale
- research.juggler_sequence.repeated_oe

Prior-art status
- conditional block-scale obstruction, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Repeated OE is now an exact scale inequality on a hypothetical counterexample, obtained from the existing word envelope plus minimality.

Best next question
- For a block O^a E, what exact lower bound on a does minimality impose before the first legal even residual?
```

## Juggler odd-run financing

- **Date:** 2026-08-27
- **Objective:** Convert minimality plus the word envelope into an exact odd-run financing law for the first legal even residual
- **Hypotheses:** `ODD_RUN_FINANCING_GREEN`, `ODD_RUN_MINIMUM_GREEN`, `BLOCK_FINANCING_GREEN`, or `SCALE_FINANCING_COUNTEREXAMPLE`
- **Major results:** \(O^aE\) on a `MinimalNonTerm` orbit requires \(n^{2^{a+1}}\le x^{3^a}\) **EXACT — LEAN VERIFIED**. \(O^aE^b\) requires \(n^{2^{a+b}}\le x^{3^a}\) **EXACT — LEAN VERIFIED**. At the start, \(2^{a+1}\le 3^a\) iff \(a\ge 2\), so the first even residual cannot occur before `OOE` **EXACT — LEAN VERIFIED**. No envelope or financing failure on \(n\le 80\). Later \(a=1\) occurs (\(77\): \(1523\xrightarrow{\mathrm{OE}}243\)). Classification **ODD_RUN_FINANCING_GREEN**. Records: `docs/research/juggler_odd_run_financing.md`, `docs/problems/juggler_odd_run_financing.md`. Control layer unchanged
- **Refuted ideas:** an absolute later odd-run lower bound \(a\ge 2\); an odd-run frequency theorem; a halt theorem; a lower-envelope theory
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** for a fixed pair \((a,b)\), can repeated \(O^aE^b\) stay \(\ge n_*\) indefinitely, or does the required scale eventually become impossible?
- **Decision:** PROMOTE the financing law and the \(O^aE^b\) block theorem. Do not claim a later absolute bound on \(a\). Do not claim termination

```text
What was learned
- Odd growth must finance the next allowed even collapse: n^{2^{a+1}} <= x^{3^a}
- The same accounting for O^a E^b is n^{2^{a+b}} <= x^{3^a}
- At the start this is 2^{a+1} <= 3^a, whose first solution is a=2, so no even residual before OOE
- Later a=1 is possible after growth (77: 1523 --OE--> 243); the inequality stays, the absolute bound on a does not
- A coarse xa >= x0 lower bound does not tighten the start window; no extra modulus programme

Strongest theorem
- If MinimalNonTerm n and O^a E^b occurs at a later state x, then n^{2^{a+b}} <= x^{3^a}

Strongest refutation
- every later odd run has length at least 2; 1523 finances OE above 77

Reusable machinery
- Problems.Engine.OddRunFinancing odd_run_financing_scale_barrier / odd_even_block_scale_barrier / initial_even_not_before_ooe
- research.juggler_sequence.odd_run_financing

Prior-art status
- conditional growth-pays-for-collapse accounting, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Minimality plus the word envelope is now an exact integer-power balance between odd expansion and even collapse, including a finite start constraint.

Best next question
- For a fixed pair (a,b), can repeated O^a E^b stay >= n_* indefinitely, or does financing eventually fail?
```

## Juggler repeated O^a E^b blocks

- **Date:** 2026-08-27
- **Objective:** Decide whether a fixed \(O^aE^b\) can repeat on a hypothetical minimal non-1 orbit without violating the scale budget
- **Hypotheses:** `REPEATED_BLOCK_SCALE_GREEN`, `REPEATED_CONTRACTION_FORBIDDEN`, `REPEATED_EXPANSION_SURVIVES`, or `REPETITION_GLOBAL_OBSTRUCTION_GREEN`
- **Major results:** \((O^aE^b)^r\) requires \(n^{2^{r(a+b)}}\le x^{3^{ar}}\) **EXACT — LEAN VERIFIED**. \(3^a\neq 2^{a+b}\) for nonempty blocks **EXACT — LEAN VERIFIED**. Formally contracting blocks contract the entry and cannot start at \(n_*\) **EXACT — LEAN VERIFIED**. Later contracting copies may stay (\(\mathrm{OE}\) from \(17537\) to \(243\ge 77\)). Expanding \((OOE)^2\) from \(69\) stays at \(212>69\). Classification **REPEATED_BLOCK_SCALE_GREEN**. Records: `docs/research/juggler_repeated_block.md`, `docs/problems/juggler_repeated_block.md`. Control layer unchanged
- **Refuted ideas:** a contracting block is always a descent below \(n_*\); repeated expansion contradicts the scale budget; a repetition-global obstruction; a frequency theorem; a halt theorem
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** can a long expanding repetition avoid every current certificate, or does some already-proved certificate eventually apply?
- **Decision:** PROMOTE the repeated-block scale law and the regime split. Accept that repetition alone is not a global obstruction. Do not claim termination

```text
What was learned
- (O^a E^b)^r on a minimal non-1 orbit requires n^{2^{r(a+b)}} <= x^{3^{a r}}
- 3^a != 2^{a+b} for nonempty blocks; contracting is 3^a < 2^{a+b}, expanding is the rest
- Contracting blocks contract the entry and cannot start at n_*; later copies may stay above n
- Expanding (OOE)^2 from 69 stays at 212>69; repetition finances later even runs more easily
- Repetition alone is not a global obstruction

Strongest theorem
- If MinimalNonTerm n and (O^a E^b)^r occurs at a later state x, then n^{2^{r(a+b)}} <= x^{3^{a r}}

Strongest refutation
- repeated expansion contradicts the scale budget; 69 --(OOE)^2--> 212

Reusable machinery
- Problems.Engine.RepeatedBlock repeated_odd_even_scale_barrier / initial_contracting_repeated_forbidden
- research.juggler_sequence.repeated_block

Prior-art status
- conditional repeated-block scale theorem plus a useful negative, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The r-fold envelope plus minimality unifies the OE and odd-run theorems, and the expanding census kills repetition as a standalone contradiction.

Best next question
- Can a long expanding repetition avoid every current certificate, or does some already-proved certificate eventually apply?
```

## Juggler finite-progress coverage

- **Date:** 2026-08-27
- **Objective:** Make the strong-induction spine formal and isolate the leftover class after even and `OE` coverage
- **Hypotheses:** `INDUCTION_SPINE_GREEN`, `ODD_ODD_FRONTIER_GREEN`, `RESIDUAL_CLASS_IDENTIFIED`, or `FINITE_PROGRESS_GREEN`
- **Major results:** `(∀ n>1 FiniteProgress n) ⇒ (∀ n≥1 ReachesOne n)` **EXACT — LEAN VERIFIED**. Even `n≥2` and odd-to-even `n≥2` have `FiniteProgress` **EXACT — LEAN VERIFIED**. Any uncovered `n≥2` is odd-to-odd **EXACT — LEAN VERIFIED**. On `2≤n≤80` every odd-to-odd start has first-even image `≥n`. Classification **ODD_ODD_FRONTIER_GREEN**. Records: `docs/research/juggler_progress_coverage.md`, `docs/problems/juggler_progress_coverage.md`. Control layer unchanged
- **Refuted ideas:** the leftover class is empty; the first even residual of an odd-to-odd start descends; a halt theorem; an all-odd minimal orbit
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** after an odd-to-odd start whose first even residual stays `≥n`, which already-proved certificate can still supply `FiniteProgress`?
- **Decision:** PROMOTE the spine and the odd-to-odd gap. Do not prove `FiniteProgress` for all `n`. Do not claim termination

```text
What was learned
- FiniteProgress is Descent or Capture; strong induction turns a universal hypothesis into ReachesOne
- Even n>=2 and odd-to-even n>=2 have FiniteProgress automatically
- Any n>=2 without FiniteProgress must be odd-to-odd; the first odd-to-odd image expands
- In 2..80 every odd-to-odd start has first-even image >= n, so induction does not fire there
- This is a coverage gap, not a halt theorem and not an all-odd orbit claim

Strongest theorem
- If every n>1 has FiniteProgress, then every n>=1 is ReachesOne; every n>=2 that is not odd-to-odd has FiniteProgress

Strongest refutation
- the first even residual of an odd-to-odd start is a descent; all 18 such starts in 2..80 stay above n

Reusable machinery
- Problems.Engine.Progress FiniteProgress / reachesOne_of_all_finiteProgress / unresolved_is_odd_odd
- research.juggler_sequence.progress_coverage

Prior-art status
- organizing coverage theorem, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The induction spine is now a machine-visible implication, and Lean isolates odd-to-odd as the only automatic gap.

Best next question
- After an odd-to-odd start whose first even residual stays >= n, which already-proved certificate can still supply FiniteProgress?
```

## Juggler odd-to-odd first-even residual

- **Date:** 2026-08-27
- **Objective:** Classify the first even residual of an odd-to-odd start under minimality
- **Hypotheses:** `FIRST_EVEN_RESIDUAL_CLASSIFIED`, `BOUNDARY_CYCLE_GREEN`, `RESIDUAL_OVERSHOOT_GREEN`, or `ODD_ODD_COUNTEREXAMPLE_CLASS`
- **Major results:** Even residual trichotomy \(z<n^2\), return cell, or overshoot **EXACT — LEAN VERIFIED**. \(z=n^2\) is impossible for odd \(n\) **EXACT — LEAN VERIFIED**. First `O^a E` descends iff \(z<n^2\), and that case is `FiniteProgress` **EXACT — LEAN VERIFIED**. On `MinimalNonTerm`, first `O^a E` is neither `Descent` nor `Capture`; leftover is return-to-\(n\) or overshoot **EXACT — LEAN VERIFIED**. Window \(2\le n\le 80\) is all overshoot. Classification **FIRST_EVEN_RESIDUAL_CLASSIFIED**. Records: `docs/research/juggler_odd_odd_frontier.md`, `docs/problems/juggler_odd_odd_frontier.md`. Control layer unchanged
- **Refuted ideas:** first even residual of an odd-odd start descends; \(z=n_*^2\) as a possible even residual; overshoot is already `FiniteProgress`; a halt theorem
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** answered in the post-overshoot residual phase
- **Decision:** PROMOTE the trichotomy and the CE dichotomy. Do not exclude cycles. Do not claim termination

```text
What was learned
- An even residual vs an odd n is below n^2, in (n^2,(n+1)^2), or at least (n+1)^2; n^2 cannot be even
- O^a E descends iff z<n^2; that subclass has FiniteProgress
- A MinimalNonTerm start cannot Descent or Capture on the first O^a E
- The CE leftover is T(z)=n (cycle) or T(z)>n (overshoot)
- In 2..80 every odd-odd first residual overshoots; some later even runs still stay above n

Strongest theorem
- If MinimalNonTerm n and O^a E occurs at n, then either T(z)=n and z<(n+1)^2, or (n+1)^2≤z and T(z)>n

Strongest refutation
- the first even residual of an odd-odd start descends; all 18 such starts in 2..80 overshoot

Reusable machinery
- Problems.Engine.OddOddFrontier minimal_first_even_dichotomy / finiteProgress_of_first_even_below
- research.juggler_sequence.odd_odd_frontier

Prior-art status
- residual classification, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The odd-odd induction obligation is now an exact cell split, and the first O^a E is proved not to close a minimal counterexample.

Best next question
- After the first overshoot T(z)>n, can the post-even odd state still carry a known FiniteProgress certificate, or is a later excursion required?
```

## Juggler post-overshoot residual

- **Date:** 2026-08-27
- **Objective:** Classify the first state after a first-even overshoot and test whether one or two later excursions force a return below the original start
- **Hypotheses:** `POST_OVERSHOOT_PROGRESS_GREEN`, `RETURN_BELOW_START_GREEN`, `TWO_EXCURSION_GREEN`, or `PERSISTENT_OVERSHOOT_COUNTEREXAMPLE`
- **Major results:** \(z\ge(n+1)^2\iff T(z)>n\) **EXACT — LEAN VERIFIED**. Post-overshoot \(y\) may be even or odd **EXACT — LEAN VERIFIED**. `ReturnBelow` plus a prefix is `FiniteProgress`; a CE never returns below its start **EXACT — LEAN VERIFIED**. Even \(y\) after the first `O^a E` on a CE forces \(n^2\le y\) and \(n^4\le z\) **EXACT — LEAN VERIFIED**. Two excursions do not always return below \(n\): \(37\) and \(77\) stay **COMPUTATIONALLY VERIFIED**. Classification **PERSISTENT_OVERSHOOT_COUNTEREXAMPLE**. Records: `docs/research/juggler_post_overshoot.md`, `docs/problems/juggler_post_overshoot.md`. Control layer unchanged
- **Refuted ideas:** the first post-overshoot state is odd; two excursions force return below \(n\); every overshoot is already `FiniteProgress`; a halt theorem
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** answered in the residual-chain certificate phase
- **Decision:** PROMOTE the classification, the even-\(y\) fourth-power barrier, and the two-excursion negative. Do not claim a general return-below theorem. Do not claim termination

```text
What was learned
- After overshoot, y=T(z)>n and may be even or odd
- ReturnBelow is a finite-prefix certificate, distinct from Descent and Capture; a CE never has it
- Even y after the first O^a E on a CE already overshoots and forces n^4 ≤ z
- In 2..80, 13 of 18 odd-odd overshoots have even T(z); the odd leftovers are 9, 37, 49, 69, 77
- Two excursions close 9, 49, 69 and fail on 37 and 77

Strongest theorem
- If MinimalNonTerm n and the first O^a E image y is even, then n^2 ≤ y and n^4 ≤ z

Strongest refutation
- two consecutive O^a E^b excursions force a return below n; 37 and 77 stay

Reusable machinery
- Problems.Engine.OddOddFrontier ReturnBelow / minimal_post_even_even_z_ge_fourth
- research.juggler_sequence.post_overshoot

Prior-art status
- leftover classification, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The overshoot branch now has an exact residual split and a CE scale law, and the hoped-for two-excursion return is computationally false.

Best next question
- After two persistent overshoots with odd residual states, what existing certificate can still fire without assuming a return law?
```

## Juggler residual-chain certificate propagation

- **Date:** 2026-08-27
- **Objective:** Formalize residual-step certificate propagation and isolate the recursive odd-odd leftover
- **Hypotheses:** `RESIDUAL_CHAIN_GREEN`, `RESIDUAL_CERTIFICATE_CLOSURE_GREEN`, `PERSISTENT_ODD_RESIDUAL_COUNTEREXAMPLE`, or `RESIDUAL_CHAIN_REDUCES_NO_FURTHER`
- **Major results:** `ResidualStep` composes `ReachesOne`, `Capture`, and `ReturnBelow` **EXACT — LEAN VERIFIED**. Residual `Descent` that stays \(\ge x\) is not `Descent` at \(x\) **EXACT — LEAN VERIFIED**. `PersistentOddResidual` stays on the odd-odd frontier **EXACT — LEAN VERIFIED**. CE residual scale: odd exit \(\ge n\), even exit \(\ge n^2\) **EXACT — LEAN VERIFIED**. First residuals in \(2\le n\le 80\): 13 propagate, 3 automatic-`FiniteProgress` stay (\(9,49,77\)), 2 persistent odd-odd (\(37,69\)). Classification **RESIDUAL_CHAIN_GREEN**. Records: `docs/research/juggler_residual_chain.md`, `docs/problems/juggler_residual_chain.md`. Control layer unchanged
- **Refuted ideas:** `FiniteProgress(y)` implies `FiniteProgress(n)`; every stay residual is odd-odd; a uniform residual horizon; a halt theorem
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** answered in the residual-path regime phase
- **Decision:** PROMOTE the residual relation and the compose/non-compose split. Do not claim that chains terminate. Do not claim that `FiniteProgress` propagates. Do not claim termination

```text
What was learned
- ReachesOne, Capture, and ReturnBelow propagate backward along a residual excursion
- Descent at y with image ≥ n is not Descent at n; FiniteProgress does not propagate
- Stay-odd splits: 9, 49, 77 have automatic FiniteProgress; 37, 69 are persistent odd-odd
- 37 → 9317 → 2233 stays above 37; the middle step is Descent at 9317
- A CE residual is ≥ n if odd and ≥ n^2 if even

Strongest theorem
- ResidualStep x y and ReachesOne y imply ReachesOne x; residual Descent staying ≥ x is not Descent at x

Strongest refutation
- FiniteProgress at the residual is FiniteProgress at the start; 9→11, 77→1523, and 37→9317→2233 stay above the original n

Reusable machinery
- Problems.Engine.ResidualChain ResidualStep / residual_descent_not_below / ResidualChain
- research.juggler_sequence.residual_chain

Prior-art status
- composition lemmas, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The odd-odd leftover is now a composable residual relation with an exact certificate split, and stay-odd is no longer one class.

Best next question
- For a persistent odd-odd residual of a hypothetical minimal counterexample, does the existing scale budget on the intervening even run force a later ReturnBelow or a later even residual that violates the barrier?
```

## Juggler residual-path regimes

- **Date:** 2026-08-27
- **Objective:** Split a hypothetical residual path into a bounded cycle-candidate regime and an unbounded scale-budget regime
- **Hypotheses:** `BOUNDED_RESIDUAL_CYCLE_GREEN`, `CYCLE_OBSTRUCTION_GREEN`, `UNBOUNDED_RESIDUAL_SCALE_GREEN`, or `NO_RESIDUAL_CONSTRAINT`
- **Major results:** A repeated orbit state is a finite Juggler cycle **EXACT — LEAN VERIFIED**. A bounded prefix longer than its window is not nodup **EXACT — LEAN VERIFIED**. Every nonempty cycle word has \(2^r<3^o\); contracting words and \(2^r=3^o\) are impossible **EXACT — LEAN VERIFIED**. Residual returns need \(a\ge 2\) **EXACT — LEAN VERIFIED**. Scan \(2\le n\le 400\): only fixed point is \(1\); no residual period-1. Classification **BOUNDED_RESIDUAL_CYCLE_GREEN**. Records: `docs/research/juggler_residual_path.md`, `docs/problems/juggler_residual_path.md`. Control layer unchanged
- **Refuted ideas:** residual return with \(a\le 1\); contracting cycle words; a halt theorem; an infinite-path type
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed or found here
- **Open:** answered in the fixed cycle-word bound phase
- **Decision:** PROMOTE the bounded-path reduction and the strict cycle envelope. Do not claim that cycles are impossible. Do not close the unbounded branch. Do not claim termination

```text
What was learned
- A repeated iterate is a finite cycle; a bounded residual prefix must repeat
- Every nonempty cycle word satisfies 2^r < 3^o
- Residual period-1 needs a ≥ 2; a ≤ 1 and contracting words are excluded
- In 2..400 the only fixed point is 1; no residual period-1 appears
- The unbounded branch still only has the existing per-step financing

Strongest theorem
- If a realized word returns to x ≥ 2, then 2^r < 3^o; a residual return therefore has a ≥ 2

Strongest refutation
- residual return with a ≤ 1; 2^{1+b} ≤ 3 is impossible for b ≥ 1

Reusable machinery
- Problems.Engine.ResidualPath cycle_strict_envelope / residual_return_a_ge_two / bounded_prefix_not_nodup
- research.juggler_sequence.residual_path

Prior-art status
- case split, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The bounded residual regime is now an exact cycle candidate with a strict exponent gap, and a meaningful class of returns is excluded without a cycle engine.

Best next question
- Can a mixed residual word with a ≥ 2 return exactly to its start, or does the existing strict defect already forbid PowerBoundEq on that return?
```

## Juggler fixed cycle-word size bounds

- **Date:** 2026-08-27
- **Objective:** Turn exact cycle return into a finite size bound via lower growth, then exclude short words
- **Hypotheses:** `CYCLE_BOUND_GREEN`, `CYCLE_WORD_EXCLUDED`, `CYCLE_SMALL_SEARCH_GREEN`, `CYCLE_BOUND_TOO_WEAK`, or `CYCLE_REALIZATION_COUNTEREXAMPLE`
- **Major results:** `CycleWord n w` implies \(n^{3^o-2^k}\le D_w\) and \(n\le D_w\) **EXACT — LEAN VERIFIED**. Contracting words cannot cycle **EXACT — LEAN VERIFIED**. No `O` or `OO` cycle for \(n\ge 2\) **EXACT — LEAN VERIFIED**. No `EOO` cycle **EXACT — LEAN VERIFIED**. `OOE` has \(n\le 262144\). Classification **CYCLE_BOUND_GREEN**. Records: `docs/research/juggler_cycle_word.md`, `docs/problems/juggler_cycle_word.md`. Control layer unchanged
- **Refuted ideas:** cycle return is envelope equality / `PowerBoundEq`; \(D_w\) is tight for every mixed word; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** answered in the cycle-word arithmetic phase
- **Decision:** PROMOTE the cycle size inequality and the short-word exclusions. Do not claim that all cycles are impossible. Do not claim termination

```text
What was learned
- Cycle return is compatible with a positive envelope defect
- Lower growth still gives n^{3^o-2^k} ≤ D_w and the crude bound n ≤ D_w
- O and OO collapse to n ≤ 4 and are excluded
- EOO is excluded by existing square-root cells, not by its huge D_w
- OOE is finite-bounded by 262144; OEO still has a weak D_w

Strongest theorem
- If CycleWord n w and n ≥ 2, then n^{3^o-2^k} ≤ lowerDenom w

Strongest refutation
- cycle return contradicts PowerBoundEq; the cycle defect is n^{3^o}-n^{2^k} > 0

Reusable machinery
- Problems.Engine.CycleWord CycleWord / cycle_pow_le_lowerDenom / no_cycle_word_eoo
- research.juggler_sequence.cycle_word

Prior-art status
- finite reduction, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Each fixed cycle word is now a finite arithmetic problem, and several short expanding words are already excluded without a cycle engine.

Best next question
- Can OEO be reduced below its crude D_w bound by unfolding the even square cell, the way EOO was reduced?
```

## Juggler cycle-word arithmetic

- **Date:** 2026-08-27
- **Objective:** Exclude `OOE` and `OEO` by exact last-branch cells and rotation, without tightening \(D_w\)
- **Hypotheses:** `OOE_CYCLE_EXCLUDED`, `OEO_CYCLE_EXCLUDED`, `CYCLE_STRUCTURE_GREEN`, `CYCLE_BOUND_TOO_WEAK`, or `MIXED_CYCLE_COUNTEREXAMPLE`
- **Major results:** last-even cycle return is the cell \(n^2\le z<(n+1)^2\), not \(z=n^2\) **EXACT — LEAN VERIFIED**. Cycle minimum is odd **EXACT — LEAN VERIFIED**. No `OOE` or `OEO` cycle for \(n\ge 2\) **EXACT — LEAN VERIFIED**. Classification **OOE_CYCLE_EXCLUDED**. Records: `docs/research/juggler_cycle_arith.md`, `docs/problems/juggler_cycle_arith.md`. Control layer unchanged
- **Refuted ideas:** last-even return is \(z=n^2\); `OOE`/`OEO` require a smaller \(D_w\); cycle return is envelope equality; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** answered in the E-terminating suffix-threshold phase
- **Decision:** PROMOTE the cell/rotation exclusions. Do not claim that all cycles are impossible. Do not claim termination

```text
What was learned
- Last-even cycle return is the square cell, not z = n^2
- For odd n the pre-final even state cannot be n^2
- OOE contradicts the existing OO suffix threshold for n ≥ 5
- OEO is a one-letter rotation of EOO
- The minimum state of a nontrivial cycle is odd

Strongest theorem
- There is no CycleWord n wordOOE or CycleWord n wordOEO for n ≥ 2

Strongest refutation
- last-even return is the exact square z = n^2

Reusable machinery
- Problems.Engine.CycleWord cycle_last_even_interval / exists_cycle_min_odd / no_cycle_word_ooe
- research.juggler_sequence.cycle_arith

Prior-art status
- finite-word exclusion, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The first mixed expanding words are now closed by exact cells and rotation, without a cycle engine and without touching the unbounded residual branch.

Best next question
- Can a cycle word of length at least 4 that ends in E be excluded by the same last-even cell against an existing superquadratic prefix, without a cycle engine?
```

## Juggler E-terminating suffix thresholds

- **Date:** 2026-08-27
- **Objective:** Lift the `OOE` cell argument to a generic suffix threshold and close length-4 E-terminating words
- **Hypotheses:** `LAST_EVEN_CLASS_GREEN`, `E_TERMINATING_LENGTH4_GREEN`, `E_SUFFIX_COUNTEREXAMPLE`, `CELL_THRESHOLD_TOO_WEAK`, or `CYCLE_E_BRANCH_PARK`
- **Major results:** if \(T_v(n)\ge(n+1)^2\) for \(n\ge N\), then no cycle \(vE\) at \(n\ge N\) **EXACT — LEAN VERIFIED**. No `OOOE` cycle **EXACT — LEAN VERIFIED**. No length-4 E-terminating cycle **EXACT — LEAN VERIFIED**. Classification **LAST_EVEN_CLASS_GREEN**. Records: `docs/research/juggler_cycle_e_term.md`, `docs/problems/juggler_cycle_e_term.md`. Control layer unchanged
- **Refuted ideas:** every length-4 E-word needs a separate cell analysis; last-even return is \(z=n^2\); O-terminating cycles are included; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** answered in the E-terminating threshold-inventory phase
- **Decision:** PROMOTE the generic threshold theorem and the length-4 E-terminating exclusion. Do not claim that all cycles are impossible. Do not treat cycles ending in `O`

```text
What was learned
- The reusable condition is a suffix threshold T_v ≥ (n+1)^2, not word length
- The only expanding length-4 E-terminating word is OOOE
- Every other length-4 E-word is formally contracting
- OOOE is excluded by the existing OOO threshold
- Cycles ending in O are a separate branch

Strongest theorem
- If T_v(m) ≥ (m+1)^2 whenever m ≥ N follows v, then there is no CycleWord n (vE) for n ≥ N

Strongest refutation
- length-4 E-terminating words other than OOOE require a new cell argument; they are contracting

Reusable machinery
- Problems.Engine.CycleWord no_cycle_append_even_of_suffix_threshold / no_cycle_word_length_four_ends_even
- research.juggler_sequence.cycle_e_term

Prior-art status
- reusable cell-versus-threshold lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The OOE argument is now a generic interface, and every length-4 E-terminating cycle word is excluded without a cycle engine.

Best next question
- Which existing suffix thresholds already sit above the next square for words longer than OOO, and do they exclude the corresponding E-terminating cycles without a new census?
```

## Juggler E-terminating threshold inventory

- **Date:** 2026-08-27
- **Objective:** Inventory existing next-square thresholds and close length-5 E-terminating words by odd-append inheritance
- **Hypotheses:** `LAST_E_THRESHOLD_COVERAGE_GREEN`, `THRESHOLD_INHERITANCE_GREEN`, `E_TERMINATING_LENGTH5_GREEN`, `E_TERMINATING_THRESHOLD_GAP`, or `LAST_E_METHOD_PARK`
- **Major results:** `O^a` for \(a\ge 3\) has next-square threshold \(N=3\) **EXACT — LEAN VERIFIED**. No `O^a E` cycle for \(a\ge 3\) **EXACT — LEAN VERIFIED**. No length-5 E-terminating cycle **EXACT — LEAN VERIFIED**. Every expanding \(vE\) is excluded above a huge \(Q_0(v)\) **EXACT — LEAN VERIFIED**. Classification **LAST_E_THRESHOLD_COVERAGE_GREEN**. Records: `docs/research/juggler_cycle_e_threshold.md`, `docs/problems/juggler_cycle_e_threshold.md`. Control layer unchanged
- **Refuted ideas:** every expanding \(vE\) needs a new exact threshold; the eventual \(Q_0\) is a useful uniform bound; O-terminating cycles are included; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** what is the smallest expanding E-terminating suffix that is not all-odd?
- **Decision:** PROMOTE the inventory, inheritance, and length-5 exclusion. Do not claim that all cycles are impossible. Do not treat cycles ending in `O`

```text
What was learned
- Exact next-square thresholds already exist for OO and OOO
- Odd-append inherits a next-square bound, so O^a has N=3 for a≥3
- The only expanding length-5 E-word is OOOOE
- Every expanding vE is already superquadratic and has a huge eventual Q0
- The first mixed expanding E-suffix appears at length 6

Strongest theorem
- There is no CycleWord n (v ++ [E]) for |v|=4 and n≥2

Strongest refutation
- the eventual Q0 is a practical uniform bound; it is D_v · 4^{2^|v|}

Reusable machinery
- Problems.Engine.CycleWord threshold_inherits_odd_append / odd_run_suffix_threshold / no_cycle_word_length_five_ends_even
- research.juggler_sequence.cycle_e_threshold

Prior-art status
- threshold reuse, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Existing thresholds plus one inheritance lemma close every length-5 E-terminating cycle without a census or a cycle engine.

Best next question
- What is the smallest expanding E-terminating suffix that is not all-odd, and can it be excluded without a new census?
```

## Juggler internal-E scale barriers

- **Date:** 2026-08-27
- **Objective:** Use the cycle-minimum even-scale barrier to bootstrap existing next-square suffixes across an internal even step
- **Hypotheses:** `INTERNAL_E_BOOTSTRAP_GREEN`, `E_TERMINATING_LENGTH6_GREEN`, `OOOEOE_EXCEPTION`, `INTERNAL_E_COUNTEREXAMPLE`, or `LAST_E_METHOD_LIMITED`
- **Major results:** even cycle states on a cycle minimum satisfy \(z\ge n^2\) **EXACT — LEAN VERIFIED**. If the suffix after an internal `E` has a next-square threshold at \(N\), there is no such `CycleMin` for \(n\ge N\) **EXACT — LEAN VERIFIED**. No `CycleMin` for `OEOOOE` **EXACT — LEAN VERIFIED**. No `CycleWord` for `OOEOOE` **EXACT — LEAN VERIFIED**. Classification **INTERNAL_E_BOOTSTRAP_GREEN**. Records: `docs/research/juggler_cycle_internal_e.md`, `docs/problems/juggler_cycle_internal_e.md`. Control layer unchanged
- **Refuted ideas:** \(y>n\) is required for the bootstrap; `OOOOEE` dies through the `OOOOE` threshold; `¬CycleMin` is `¬CycleWord`; every mixed length-6 E-word is excluded; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** what exact extra scale does the prefix `OOO` give before the internal `E` of `OOOEOE`?
- **Decision:** PROMOTE the cycle-minimum barrier and the internal-E bootstrap. Do not claim that all length-6 E-cycles are impossible. Do not treat cycles ending in `O`

```text
What was learned
- Cycle-min even states satisfy z ≥ n^2 by parity on the realized cycle
- y ≥ n is enough: a next-square suffix then overshoots the last-even cell
- OEOOOE is impossible as a cycle minimum via suffix OOO
- OOEOOE is impossible as a CycleWord: every rotation dies
- OOOEOE and OOOOEE are not covered by existing next-square suffixes

Strongest theorem
- If v has a next-square threshold at N, then there is no CycleMin n (u E v E) for n ≥ N

Strongest refutation
- OOOOEE is free from the OOOOE threshold; T_OOOO ≥ (n+1)^2 does not lift across an extra E

Reusable machinery
- Problems.Engine.CycleWord CycleMin / no_cycleMin_internal_even_threshold / no_cycle_word_ooeooe
- research.juggler_sequence.cycle_internal_e

Prior-art status
- threshold transport across an internal even step, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Minimality on the realized cycle amplifies existing OO / OOO thresholds far enough to kill the first mixed E-words that have those suffixes, without a census or a D_w improvement.

Best next question
- What exact extra scale does the prefix OOO give before the internal E of OOOEOE?
```

## Juggler cycle extrema

- **Date:** 2026-08-27
- **Objective:** Package word-independent cycle extrema and test whether square-scale growth forces a superquadratic prefix
- **Hypotheses:** `CYCLE_EXTREMES_GREEN`, `ASCENDING_SUPERQUADRATIC_GREEN`, `MAX_RETURN_CELL_GREEN`, `EXTREMAL_CYCLE_COUNTEREXAMPLE`, or `EXTREMES_NOT_ENOUGH`
- **Major results:** cycle maximum is even **EXACT — LEAN VERIFIED**. On a cycle minimum, \(M>m^2\) **EXACT — LEAN VERIFIED**. Any realized path from \(n\ge 2\) to a state \(\ge n^2\) is superquadratic **EXACT — LEAN VERIFIED**. Min-to-even prefixes on a cycle minimum are superquadratic **EXACT — LEAN VERIFIED**. Classification **CYCLE_EXTREMES_GREEN**. Records: `docs/research/juggler_cycle_extrema.md`, `docs/problems/juggler_cycle_extrema.md`. Control layer unchanged
- **Refuted ideas:** \(M=m^2\) is possible; the full-cycle envelope already forces the prefix law; every odd start hits \(m^2\) before dropping; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** does the superquadratic min-to-max prefix plus the exact maximum return cell force a forbidden transition without a word census?
- **Decision:** PROMOTE the extrema package and the square-scale prefix law. Do not claim that growth and collapse cannot coexist. Do not exclude first-cell maxima

```text
What was learned
- A nontrivial cycle has odd min, even max, and M > m^2
- Reaching square scale requires 3^o ≥ 2^{k+1}, which is strictly stronger than 2^k < 3^o
- OOE is expanding but cannot carry m to m^2
- Ordinary stay-above-min transients often drop before m^2, so the cycle demand is not vacuous
- The maximum return cell does not force T(M) = m

Strongest theorem
- If follows n w, n ≥ 2, and n^2 ≤ T_w(n), then 3^{#O(w)} ≥ 2^{|w|+1}

Strongest refutation
- every odd start hits m^2 before dropping; 7 walks OE and falls to 4

Reusable machinery
- Problems.Engine.CycleWord CycleMax / cycleMin_max_gt_sq / square_scale_superquadratic
- research.juggler_sequence.cycle_extrema

Prior-art status
- word-independent extrema and prefix law, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Stopping the length programme produced a reusable constraint that applies to every cycle word at once: the path from the minimum to any even cycle state is superquadratic.

Best next question
- Does the superquadratic min-to-max prefix plus the exact maximum return cell force a forbidden transition without a word census?
```

## Juggler top excursions

- **Date:** 2026-08-27
- **Objective:** Normalize every nontrivial cycle at the odd landing after the maximum even run, and record the two-sided scale window
- **Hypotheses:** `TOP_EXCURSION_GREEN`, `TOP_SCALE_WINDOW_GREEN`, `TOP_ASCENT_CONTRADICTION_GREEN`, `TOP_WINDOW_SURVIVES`, or `TOP_EXCURSION_COUNTEREXAMPLE`
- **Major results:** `r` even iterates give \(T^r(x)^{2^r}\le x<(T^r(x)+1)^{2^r}\) **EXACT — LEAN VERIFIED**. Every cycle maximum has a finite even run onto an odd landing **EXACT — LEAN VERIFIED**. The cycle rotates to \(p\to M\to E^r\to p\) with \(3^{\#O(u)}\ge 2^{|u|+r}\) **EXACT — LEAN VERIFIED**. Classification **TOP_EXCURSION_GREEN**. Records: `docs/research/juggler_cycle_top_excursion.md`, `docs/problems/juggler_cycle_top_excursion.md`. Control layer unchanged
- **Refuted ideas:** the top window is empty; every top run has length 1; \(T(M)\) is the cycle minimum; ordinary overshoots close a top excursion; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** does any existing exact threshold force the ascent \(p\to M\) out of the top window for a scalable family of \(r\)?
- **Decision:** PROMOTE the top even-run, the two-sided window, and the landing normal form. Do not claim that the ascent is impossible. Do not claim that \(T(M)=m\)

```text
What was learned
- Every cycle maximum begins a finite E^r onto an odd landing p
- The exact window is p^{2^r} ≤ M < (p+1)^{2^r}; it is nonempty
- The ascent p → M is scale-superquadratic: 3^o ≥ 2^{k+r}
- Direct return p = m is the last-even first-cell family; it is not forced
- Transient maxima sit in the window and do not return to p

Strongest theorem
- A CycleMax rotates to p → M → E^r → p with p^{2^r} ≤ M < (p+1)^{2^r}

Strongest refutation
- the top window is empty; it is a nonempty integer interval

Reusable machinery
- Problems.Engine.CycleWord even_iter_pow_le / cycleMax_top_normal_form / power_scale_superquadratic
- research.juggler_sequence.cycle_top_excursion

Prior-art status
- maximum-normalization lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The maximum is now a turning point with a sharp two-sided cell. That is the strongest word-independent structure currently available. The ascent is not shown to overshoot the cell.

Best next question
- Answered in the maximum-predecessor branch: the odd predecessor forces p < x < M inside nested cells, without emptying a top-run length.
```

## Juggler maximum predecessors

- **Date:** 2026-08-27
- **Objective:** Exploit that the global maximum is reached from an odd predecessor, and test whether the nested top cells restrict or empty a cycle
- **Hypotheses:** `TOP_NESTED_CELL_GREEN`, `TOP_SCALE_GAP_GREEN`, `TOP_RUN_OBSTRUCTION_GREEN`, `TOP_NESTED_CELL_SURVIVES`, or `TOP_COUNTEREXAMPLE_PATTERN`
- **Major results:** the predecessor of a cycle maximum is odd **EXACT — LEAN VERIFIED**. The top is three-level \(p<x<M\) **EXACT — LEAN VERIFIED**. Nested cells \(p^{2^r}\le M<(p+1)^{2^r}\) and \(M^2\le x^3<(M+1)^2\) **EXACT — LEAN VERIFIED**. Scale \(x^3\ge p^{2^{r+1}}\) and \(M<x^2\) **EXACT — LEAN VERIFIED**. Classification **TOP_NESTED_CELL_GREEN**. Records: `docs/research/juggler_cycle_top_pred.md`, `docs/problems/juggler_cycle_top_pred.md`. Control layer unchanged
- **Refuted ideas:** \(x=p\) on a cycle; \(x\ge p^2\) is forced; the nested cells empty every top-run length; \(T(M)=p\) for \(r>1\); a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** does any further exact cell force the nested triple \((p,x,M)\) out of both windows at once, without naming the ascent word?
- **Decision:** PROMOTE the odd predecessor, the three-level top, and the nested cells. Do not claim that a top-run length is impossible. Do not claim that \(x\ge p^2\)

```text
What was learned
- The maximum is reached by an odd step; an even predecessor would descend
- The odd-to-even two-step plus even descent force p < x < M for every r ≥ 1
- T(M)=p only when r=1; the conclusion p<x still holds for longer top runs
- Nested cells give x^3 ≥ p^{2^{r+1}} and M < x^2, but the integer region stays nonempty
- Transient r=1 maxima can have x < p^2 (9 and 77), so that strengthening is false

Strongest theorem
- A CycleMax has an odd predecessor x with p < x < M, p^{2^r} ≤ M < (p+1)^{2^r}, and M^2 ≤ x^3 < (M+1)^2

Strongest refutation
- x ≥ p^2; start 9 has p=11, x=27, M=140

Reusable machinery
- Problems.Engine.CycleWord cycle_top_three_level / cycle_top_nested_cell / cycle_top_pred_scale
- research.juggler_sequence.cycle_top_pred

Prior-art status
- maximum-predecessor nested-cell lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The global maximum is now a three-level exact cell, not merely a two-sided window. That is a word-independent restriction. It is not an r-obstruction.

Best next question
- Answered in the peak-descent branch: the maximum determines a canonical contracting OE^r block, and financing it recovers the existing ascent scale.
```

## Juggler canonical peak descent

- **Date:** 2026-08-27
- **Objective:** Name the canonical peak block \(x\xrightarrow{OE^r}p<x\) and test whether financing it from \(p\) to \(x\) is stronger than the existing top-ascent envelope
- **Hypotheses:** `PEAK_DESCENT_GREEN`, `ODD_MILESTONE_GREEN`, `PEAK_SCALE_GAP_GREEN`, `PEAK_MILESTONE_COUNTEREXAMPLE`, or `MILESTONE_REPACKAGING`
- **Major results:** every cycle maximum has a canonical `OE^r` descent **EXACT — LEAN VERIFIED**. The block is formally contracting **EXACT — LEAN VERIFIED**. Peak-ascent finance \(3^{o+1}\ge 2^{k+r+1}\) **EXACT — LEAN VERIFIED** and is a **REPARAMETERIZATION** of the top ascent. Classification **PEAK_DESCENT_GREEN**. Records: `docs/research/juggler_cycle_peak_descent.md`, `docs/problems/juggler_cycle_peak_descent.md`. Control layer unchanged
- **Refuted ideas:** peak finance is a stronger scale gap; transients close \(p\to x\); \(T(p)\) has one parity; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** answered in the extremal-composition branch: composing landings and extrema is envelope repackaging
- **Decision:** PROMOTE the canonical peak descent and the finance identity. Do not claim a stronger scale gap. Do not build an odd-milestone engine

```text
What was learned
- Every cycle maximum determines a peak block OE^r with T(x)=p<x
- OE^r is formally contracting: 3 < 2^{r+1}
- Combining p^{2^{r+1}} ≤ x^3 with the ascent envelope recovers 3^{o+1} ≥ 2^{k+r+1}
- That inequality is the existing top-ascent law after appending the final O
- Transient peaks realise the descent only; they do not close p → x

Strongest theorem
- A CycleMax has a canonical descent x --OE^r--> p < x, and OE^r is formally contracting

Strongest refutation
- peak finance is stronger than the top ascent; it is the same exponent comparison

Reusable machinery
- Problems.Engine.CycleWord cycle_peak_descent / peak_ascent_scale / cycle_peak_finance
- research.juggler_sequence.cycle_peak_descent

Prior-art status
- canonical peak-block lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- The maximum now names a contracting subword without a census. The financing question is answered: it does not beat the existing ascent law. Stop before a milestone graph.

Best next question
- Answered in the extremal-composition branch: composing the existing min / first-even / top-cell / peak constraints is envelope repackaging.
```

## Juggler extremal composition

- **Date:** 2026-08-27
- **Objective:** Compose existing cycle constraints (minimum scale, first-even financing, top cell, peak descent) and test whether they yield a word-independent contradiction or only the ordinary envelope
- **Hypotheses:** `GLOBAL_EXTREMAL_COMPOSITION_GREEN`, `FIRST_TO_TOP_SCALE_GREEN`, `TOP_TO_RETURN_GREEN`, `DEFECT_EXTREMAL_GREEN`, `COMPOSITION_REPACKAGING`, or `EXTREMAL_COUNTEREXAMPLE`
- **Major results:** distinguished order \(m\le p<x<M\) **EXACT — LEAN VERIFIED**. Strict top window \(p^{2^r}<M\) **EXACT — LEAN VERIFIED**. Derived \(m^4<x^3\) **EXACT — LEAN VERIFIED** and a **REPARAMETERIZATION** of \(M>m^2\) plus the cube cell. Every attempted stronger scale law reduces to `power_bound_word` or an existing extremal theorem. Classification **COMPOSITION_REPACKAGING**. Records: `docs/research/juggler_cycle_extremal_composition.md`, `docs/problems/juggler_cycle_extremal_composition.md`. Control layer unchanged
- **Refuted ideas:** first-even versus top is a new scale gap; \(p=m\); \(z<p\) or \(z>x\) as universal; split min-to-max is stronger than the envelope; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** answered in the cyclic-rounding branch: return of the exact floor remainders is a non-envelope identity
- **Decision:** CLOSE the compose-for-contradiction branch. Record the compatible normal form. Do not open odd-landings, a residual graph, or an energy

```text
What was learned
- A CycleMax packages as m ≤ p < x < M with a strict top window p^{2^r} < M
- The fourth-power comparison m^4 < x^3 is M > m^2 plus the cube cell
- Split paths m → z → M and p → x → M recover the ordinary word envelope
- Transient starts already forbid treating p = m, z = M, or z ≷ x as universal
- Location-sensitive packaging exists; it does not produce a cycle contradiction

Strongest theorem
- A CycleMax has distinguished states m ≤ p < x < M with p^{2^r} < M < (p+1)^{2^r} and m^4 < x^3

Strongest refutation
- composing scale laws beats the envelope; every such composition is power_bound_word or an existing extremal theorem

Reusable machinery
- Problems.Engine.CycleWord cycle_distinguished_order / cycle_top_window_strict / cycleMax_min_sq_lt
- research.juggler_sequence.cycle_extremal_composition

Prior-art status
- negative composition result, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- CLOSE

Why
- The existing cells coexist around one closed trajectory. Their scale content is the ordinary envelope. A further abstraction layer would be machinery gravity.

Best next question
- Answered in the cyclic-rounding branch: return of the exact floor remainders is a non-envelope identity.
```

## Juggler cyclic rounding

- **Date:** 2026-08-27
- **Objective:** Keep the exact local floor remainders the envelope discards and test whether cyclic closure of those equations yields a non-envelope constraint or a cycle obstruction
- **Hypotheses:** `CYCLIC_ROUNDING_GREEN`, `CYCLIC_ROUNDING_NEW_CONSTRAINT`, `CYCLE_REMAINDER_RIGIDITY_GREEN`, `CYCLE_ROUNDING_REPACKAGING`, or `ROUNDING_COUNTEREXAMPLE`
- **Major results:** every cycle branch satisfies \(x^e=T(x)^2+\rho\) with \(0\le\rho<2T(x)+1\) **EXACT — LEAN VERIFIED**. Cyclic return balances \(\sum\rho+\sum_{\mathrm{even}}x(x-1)=\sum_{\mathrm{odd}}x^2(x-1)\) **EXACT — LEAN VERIFIED**. All-zero remainders are impossible for \(n\ge 2\) **EXACT — LEAN VERIFIED**. Peak odd remainder is positive, equivalently \(M^2<x^3\) **EXACT — LEAN VERIFIED**. Dropping remainders recovers `power_bound_word`. Universal remainder amplification is **REFUTED** at start 9. Classification **CYCLIC_ROUNDING_GREEN**. Records: `docs/research/juggler_cycle_rounding.md`, `docs/problems/juggler_cycle_rounding.md`. Control layer unchanged
- **Refuted ideas:** a positive remainder forces the next remainder to grow; remainder composition is only the exponent envelope; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** is there a sequential, non-sum remainder identity that uses \(T_w(n)=n\) and cannot be rewritten as the path-power / path-square balance?
- **Decision:** PROMOTE the remainder API, the cyclic balance, and the all-zero rigidity. Do not claim a cycle obstruction. Do not build remainder dynamics

```text
What was learned
- The envelope remainder is the existing localDefect, now with a uniform successor window
- Cyclic return keeps the remainders as ∑ρ + even gaps = odd gaps
- That identity is not power_bound_word: it uses the states, not only 2^k vs 3^o
- All-zero remainders are impossible on a nontrivial cycle; peak ρ_O is odd and positive
- A later remainder need not grow; start 9 has 0, 83, 19

Strongest theorem
- On a CycleWord, ∑ρ + ∑_{even} x(x-1) = ∑_{odd} x^2(x-1), and some ρ is positive for n ≥ 2

Strongest refutation
- remainder amplification; start 9 has remainders 0, 83, 19

Reusable machinery
- Problems.Engine.FloorPower branchDefect / localDefectOdd_lt_succ
- Problems.Engine.CycleWord cycle_remainder_balance / cycle_exists_pos_remainder
- research.juggler_sequence.cycle_rounding

Prior-art status
- remainder-refinement lemma, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Keeping the remainders around a cycle is the first identity that uses T_w(n)=n without collapsing to the exponent envelope. It is not an obstruction. Stop before a remainder-dynamics object.

Best next question
- Is there a sequential, non-sum remainder identity that uses T_w(n)=n and cannot be rewritten as the path-power / path-square balance?
```

## Juggler cycle Diophantine defects

- **Date:** 2026-08-27
- **Objective:** Test whether the sequential peak defects \(\delta=x^3-M^2\) and \(\varepsilon=M-p^{2^r}\) impose a congruence or residual-class restriction that the existing power envelope cannot see
- **Hypotheses:** `DIOPHANTINE_NEW_CONGRUENCE`, `CYCLE_R_AVOIDANCE_GREEN`, `DIOPHANTINE_REPACKAGING`, or `DIOPHANTINE_COUNTEREXAMPLE`
- **Major results:** \(x^3=(p^{2^r}+\varepsilon)^2+\delta\) **EXACT — LEAN VERIFIED** and **REPARAMETERIZATION** of the nested cells. The slack identity \(x^3-p^{2^{r+1}}=2\varepsilon p^{2^r}+\varepsilon^2+\delta\) is `cycle_top_pred_scale` made exact. \(\delta\) and \(\varepsilon\) odd is existing peak/top parity. A nontrivial cycle avoids \(R=\{1,\ldots,11\}\), hence \(p\ge 13\) **EXACT — LEAN VERIFIED**, a named corollary of `reachesOne_of_lt_twelve`. Residue census on 38 transient peaks: 13 pairs mod 8, 24 pairs mod 16, all odd/odd. Classification **DIOPHANTINE_REPACKAGING**. Records: `docs/research/juggler_cycle_diophantine.md`, `docs/problems/juggler_cycle_diophantine.md`. Control layer unchanged
- **Refuted ideas:** the sequential identity is stronger than the envelope slack; \((\delta,\varepsilon)\) is modularly rigid beyond odd/odd; \(R\) forbids a residue class of \(p\) already on transients; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** answered in the odd-odd residual branch: non-extremal continuation is `ODD_ODD_RESIDUAL_COMPLEX`
- **Decision:** CLOSE the Diophantine peak-pair branch as `DIOPHANTINE_REPACKAGING`. Record the named defects and the cycle \(R\)-avoidance corollary. Do not claim a cycle obstruction

```text
What was learned
- The sequential peak identity exists and is not a path-sum remainder balance
- Its arithmetic content is the known slack of x^3 ≥ p^{2^{r+1}}
- δ and ε are odd by the existing peak/top parity; transients realise many residues mod 8 and 16
- R-avoidance is cycle-only and only upgrades 2 ≤ p to 13 ≤ p
- Transient landings in R are common and do not refute the cycle bound

Strongest theorem
- On a CycleMax, x^3 = (p^{2^r} + ε)^2 + δ, equivalently x^3 − p^{2^{r+1}} = 2ε p^{2^r} + ε^2 + δ

Strongest refutation
- a modular restriction stronger than odd/odd; 13 distinct (δ,ε) pairs mod 8 on transients

Reusable machinery
- Problems.Engine.CycleDiophantine peakOddDefect / topEvenDefect / peak_diophantine_slack
- cycleWord_iterate_not_lt_twelve / cycle_top_landing_ge_thirteen
- research.juggler_sequence.cycle_diophantine

Prior-art status
- negative sequential-identity result, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- CLOSE

Why
- The peak pair rewrites the nested cells. Residues do not beat the envelope. Stop before another defect layer.

Best next question
- Answered in the odd-odd residual branch: non-extremal continuation is `ODD_ODD_RESIDUAL_COMPLEX`.
```

## Juggler odd fourth-power heavy search

- **Date:** 2026-08-27
- **Objective:** Search the exact interval \(a^8\le n^3<(a^4+1)^2\) for an odd non-square \(n\) with \(T(n)=a^4\), persist the range, and look for an obstruction
- **Hypotheses:** `ODD_FOURTH_POWER_COUNTEREXAMPLE`, `ODD_FOURTH_POWER_NO_WITNESS`, `ODD_FOURTH_POWER_STRUCTURE_DISCOVERED`, `ODD_FOURTH_POWER_PROOF_READY`
- **Major results:** Resumable exact \(a\)-parameter search (`odd-fourth-v1-cbrt`, `python-int`). Persisted range \(1\le a<10^8\): \(99\,999\,999\) candidates, \(465\) interval cubes, \(0\) odd non-squares. Cubes are exactly \(a=k^3\), \(n=k^8\) for \(1\le k\le 464\), plus the inexact even hit \(a=97\), \(n=198636\). Occupancy at most one. Dataset: `data/research/juggler/odd_sharp_suffix/`. Tool: `tools/odd_fourth_power_search.py`. Control layer unchanged. Classification still **ODD_SHARP_SUFFIX_INCOMPLETE**
- **Refuted ideas:** interval emptiness as the obstruction (`a=97`); scanning \(n\) instead of \(a\); treating the empty odd-non-square range as a theorem; incrementing the cube index \(m\) by \(1\) (jumps of size \(a^{5/3}\))
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** whether \(T(n)=a^4\) and \(n\) odd forces \(n\) to be a square
- **Decision:** PARK. Record `ODD_FOURTH_POWER_NO_WITNESS` and `ODD_FOURTH_POWER_STRUCTURE_DISCOVERED`. Do not start Lean. Do not claim termination

```text
What was learned
- T(n)=a^4 is the exact interval a^8 <= n^3 < (a^4+1)^2
- The interval holds at most one cube
- Even a forces even n; odd squares occur only for a=k^3
- Through a<10^8 the only inexact cube is a=97, n=198636 even
- No odd non-square witness; emptiness is evidence, not a theorem

Strongest theorem
- none new; the inverse-floor iff remains the Lean fact

Strongest refutation
- "the fourth-power square interval never contains a cube" fails at a=97

Reusable machinery
- tools/odd_fourth_power_search.py and the SQLite dataset under
  data/research/juggler/odd_sharp_suffix/

Prior-art status
- finite exact search, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PARK

Why
- The search left a persistent range and a clean hit list: exact eighth
  powers plus one even exception. That is enough to park. It is not a
  proof, and it does not justify a number-theory framework.

Best next question
- Prove that T(n)=a^4 and n odd implies n is a square, or find an odd
  non-square witness
```

## Juggler odd fourth-power nearest-cube obstruction

- **Date:** 2026-08-27
- **Objective:** Name the arithmetic obstruction in \(T(n)=a^4\) with \(n\) odd, from the persisted \(a<10^8\) hits, and Lean only the cheapest surviving route
- **Hypotheses:** `NONCUBE_CUBE_EVEN_GREEN`, `ODD_FOURTH_POWER_GREEN`, `ODD_SHARP_SUFFIX_GREEN`, `ODD_FOURTH_POWER_COUNTEREXAMPLE`
- **Major results:** Occupancy \(\le 1\), exact family \(a=k^3\Rightarrow n=k^8\), and non-cube \(\Rightarrow n=m+1\) are **EXACT — LEAN VERIFIED**. Odd \(m\) forces the candidate even, so \(T(n)=a^4\) and \(n\) odd implies \(n\) is a square when \(m\) is odd. Restricted Phase-G corollary: an odd first defect cannot have a sharp exact-even suffix of length \(\ge 2\) when that cube root is odd. The preferred “odd \(a\) forces \(m\) odd” guess is false (\(a=3\), \(m=18\)). Corpus still 465 hits, 0 odd non-squares, unique inexact hit \(a=97\). Classification still **ODD_SHARP_SUFFIX_INCOMPLETE**. No ledger row. Control layer unchanged
- **Refuted ideas:** odd \(a\) forces \(m\) odd; treating hit-set “even \(a\) forces even \(n\)” as a theorem; interval emptiness; replacing the reserved impossibility name by the restricted corollary
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** a non-cube with even \(m\) never satisfies \((m+1)^3-a^8\le 2a^4\)
- **Decision:** PARK. Record the restricted odd-\(m\) Lean. Do not claim `ODD_FOURTH_POWER_GREEN` or `ODD_SHARP_SUFFIX_GREEN`. Do not start Routes C/D. Do not claim termination

```text
What was learned
- The fourth-power window holds at most one cube
- A cube a sits at n=k^8; a non-cube leaves only n=m+1
- That candidate is even exactly when m is odd (a=97)
- Odd a need not make m odd (a=3, m=18, empty window)
- The leftover counterexample shape is even m with gap ≤ 2a^4

Strongest theorem
- If T(n)=a^4, n is odd, and floor_cbrt(a^8) is odd, then n is a square

Strongest refutation
- “odd a forces m odd” fails at a=3; interval emptiness still fails at a=97

Reusable machinery
- FloorPower nearest-cube block (occupancy, exact family, successor candidate, odd-cbrt parity)
- odd_sharp_suffix nearest-cube analysis of persisted hits

Prior-art status
- restricted inverse-floor packaging, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PARK

Why
- Route B names a real obstruction only when m is odd. The even-m
  emptiness is not elementary after the focused hit analysis. Stop
  rather than open a modulus sweep or enlarge the search.

Best next question
- Prove that a non-cube with even m never places m+1 in the window,
  or exhibit such an a
```

## Juggler even cube-root fourth-power obstruction

- **Date:** 2026-08-27
- **Objective:** Prove or refute that a non-cube \(a\) with even \(m=\lfloor\sqrt[3]{a^8}\rfloor\) satisfies \((m+1)^3-a^8>2a^4\)
- **Hypotheses:** `FOURTH_POWER_ODD_GREEN`, `ODD_SHARP_SUFFIX_GREEN`, `NONCUBE_EVEN_CANDIDATE_SURVIVES`
- **Major results:** Even-\(m\) discovery \(a\le 20000\): 0 window hits; closest near-misses \(a=3,6,79,2\). \(a=97\) remains an odd-\(m\) hit. \(a=37840\) has even \(m\) with \(a^8\) at the top of its cube cell, so a uniform remaining-fraction lemma is false. The trivial bound \(m\ge a^{8/3}-1\) is sharp and cannot produce an \(A_0\). No small-modulus obstruction on the surviving candidate. Classification still **ODD_SHARP_SUFFIX_INCOMPLETE**. No new Lean. No ledger row. Control layer unchanged
- **Refuted ideas:** uniform remaining-fraction bound for even \(m\); cube-root bracketing threshold \(A_0\); treating the \(10^8\) empty even-\(m\) range as a theorem
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** a non-cube with even \(m\) never satisfies \((m+1)^3-a^8\le 2a^4\)
- **Decision:** PARK. Do not start Baker/Thue/Mordell. Do not rerun \(10^8\). Do not claim `FOURTH_POWER_ODD_GREEN` or `ODD_SHARP_SUFFIX_GREEN`

```text
What was learned
- Even-m non-cubes did not hit the window on a<=20000
- Closest even-m near-misses are small a (3, 6, 79, 2)
- a=97 stays legal: m odd, surplus negative
- Eighth powers can sit at the top of a cube cell (a=37840)
- m >= a^{8/3}-1 cannot yield a finite threshold for any A0

Strongest theorem
- none new; the odd-m nearest-cube lemmas remain the Lean facts

Strongest refutation
- a uniform remaining-fraction bound for even m fails at a=37840

Reusable machinery
- even_cbrt_surplus_record / even_cbrt discovery notes under
  data/research/juggler/odd_sharp_suffix/analysis/

Prior-art status
- local gap comparison, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PARK

Why
- The even-m gap inequality is not elementary after the focused surplus
  analysis. Stop rather than open Baker/Thue or enlarge the search.

Best next question
- Prove that a non-cube with even m never places m+1 in the window,
  or exhibit such an a
```

## Juggler even cube-root modular obstruction

- **Date:** 2026-08-27
- **Objective:** Decide whether parity or a small exact modulus rules out even \(m\) with \((m+1)^3-a^8\le 2a^4\)
- **Hypotheses:** `MOD2_OBSTRUCTION_GREEN`, `MODULAR_OBSTRUCTION_GREEN`, `MODULAR_PLUS_SIZE_GREEN`, `EVEN_M_OBSTRUCTION_COUNTEREXAMPLE`, `OBSTRUCTION_NOT_MODULAR`
- **Major results:** Candidate A fails: even \(a\) makes \(D\) odd, odd \(a\) makes \(D\) even, and both occur. Candidates B/C fail: no \(q\in\{2,4,8,16,32,64,128,3,5,7,9,13,15,24\}\) empties even-\(m\) classes; \(a=3\) is a live even-\(m\) pair. Candidate D fails for a fixed modulus once \(2a^4\ge q\). For odd \(a\), \(a^8\equiv 1\pmod{32}\) and \(2a^4\equiv 2\pmod{32}\). \(a=97\) stays an odd-\(m\) window hit. Classification **OBSTRUCTION_NOT_MODULAR**. No new Lean. No ledger row. Control layer unchanged
- **Refuted ideas:** pure parity obstruction; some \(2^k\) forbids even \(m\); a small mixed modulus forbids even \(m\)
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** a non-cube with even \(m\) never satisfies \((m+1)^3-a^8\le 2a^4\)
- **Decision:** PARK. Record `OBSTRUCTION_NOT_MODULAR`. Do not start Baker/Thue/Mordell. Do not enlarge the modulus. Do not rerun \(10^8\). Do not claim `FOURTH_POWER_ODD_GREEN`

```text
What was learned
- Even m occurs (a=3); no modulus can forbid even m itself
- D is odd for even a and even for odd a; both fit 0<D<=2a^4
- Odd eighth powers are 1 mod 32 and 2a^4 is 2 mod 32
- 2^k and small odd/mixed q leave many even-m residue classes
- a=97 remains the odd-m window regression

Strongest theorem
- none new; the odd-m nearest-cube lemmas remain the Lean facts

Strongest refutation
- Candidates A-D fail; the obstruction is not modular

Reusable machinery
- even_cbrt_moduli analysis under
  data/research/juggler/odd_sharp_suffix/analysis/

Prior-art status
- local residue comparison, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PARK

Why
- The even-m window inequality is not a small-modulus fact. Stop rather
  than start Baker/Thue or enlarge q.

Best next question
- Prove the even-m gap inequality by a non-modular argument, or exhibit
  a non-cube a with even m and D <= 2a^4
```

## Juggler even cube-root near-power gap

- **Date:** 2026-08-27
- **Objective:** Decide whether an elementary near-square / near-cube gap closes even \(m\) with \((m+1)^3-a^8\le 2a^4\)
- **Hypotheses:** `NEAR_POWER_GAP_GREEN`, `FOURTH_POWER_RIGIDITY_GREEN`, `ODD_FOURTH_POWER_GREEN`, `NONCUBE_GAP_COUNTEREXAMPLE`, `DIOPHANTINE_ESCALATION_REQUIRED`
- **Major results:** Route A is false at \(a=97\) (\(k=5\), \(u=-28\), odd \(m\), window hit). The exact-family cell of \(k^8\) holds \(a^8\) only for \(a=k^3\); every checked \(u\neq 0\) leaves that cell, but leaving it does not force a miss. Closest even-\(m\) failures are \(a=3,6,79,2\), not near-cubes. Neighborhood \(1\le k\le 30\), \(1\le|u|\le 6\): 0 window hits. Discovery \(a\le 20000\): 0 even-\(m\) hits; sign of \(v\) matched sign of \(u\). No elementary \(D\) bound stronger than \(1\) produces a threshold. Classification **DIOPHANTINE_ESCALATION_REQUIRED**. No new Lean. No ledger row. Control layer unchanged
- **Refuted ideas:** unrestricted non-cube gap; leaving the exact-family cell implies a miss; \(|a-k^3|\) is the quantity that separates hits from misses
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** a non-cube with even \(m\) never satisfies \((m+1)^3-a^8\le 2a^4\)
- **Decision:** PARK. Record `DIOPHANTINE_ESCALATION_REQUIRED`. Do not start Baker/Thue/Mordell. Do not enlarge the modulus. Do not rerun \(10^8\). Do not claim `NEAR_POWER_GAP_GREEN` or `ODD_FOURTH_POWER_GREEN`

```text
What was learned
- Route A fails: a=97 is a non-cube window hit (m odd)
- Exact-family cells are exclusive to a=k^3; nonzero u jumps cells
- Jumping cells does not bound D; a=97 left its nearest cell and hit
- Closest even-m failures are small a (3, 6, 79, 2), not near-cubes
- |u|=1 through k<=30 never hits the window
- No elementary gap stronger than D>=1 yields a finite threshold

Strongest theorem
- none new; the odd-m nearest-cube lemmas remain the Lean facts

Strongest refutation
- Route A, and "leave the exact-family cell => miss", both fail at a=97

Reusable machinery
- near_power analysis under
  data/research/juggler/odd_sharp_suffix/analysis/

Prior-art status
- local gap comparison, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PARK

Why
- Elementary near-common-power expansions identify the exact family
  and then stop. The leftover even-m inequality is a genuine
  Diophantine gap. Record it and do not introduce Baker/Thue.

Best next question
- Name a concrete method for X=a^4, Y even, X^2-Y^3=r before
  introducing it, or exhibit the smallest even-m window hit
```

## Juggler fourth-power Diophantine gap survey

- **Date:** 2026-08-27
- **Objective:** Decide whether a known \(|x^3-y^4|\) or Hall-scale theorem proves \(0<n^3-b^4\le 2b^2\) impossible for odd non-square \(n\) and \(b=a^2\)
- **Hypotheses:** `GAP_THEOREM_SUFFICIENT`, `ODDNESS_GAP_SUFFICIENT`, `DIOPHANTINE_THEOREM_IDENTIFIED`, `FOURTH_POWER_DIOPHANTINE_COUNTEREXAMPLE`, `DIOPHANTINE_ESCALATION_REQUIRED`
- **Major results:** No mapped theorem beats \(2b^2\). Mihăilescu gives \(\ge 2\); Liouville gives \(\ge 1\); Roth loses to the height of \(b^{4/3}\); Hall (even as a conjecture) gives \(X^{1/2}\) against a window of size \(2Y\sim 2X^{3/2}\); Danilov forbids raising the Hall exponent; Bennett equal-exponent and fixed-base results do not apply; superelliptic solvers need fixed \(k\). The only persisted positive-\(r\) hit is \(a=97\), \(r=165506495\le 2b^2=177058562\), \(n\) even. The weakest sufficient bound would be \(|x^3-y^8|>2y^4\) for non-cube \(y\) and odd \(x\); that is stronger than Hall and is not published. Classification **DIOPHANTINE_ESCALATION_REQUIRED**. No new Lean. No ledger row. Control layer unchanged
- **Refuted ideas:** treating Hall or Mihăilescu as a closing theorem; applying equal-exponent or fixed-base Bennett results to \(n^3-b^4\)
- **Literature:** Mihăilescu 2004; Hall 1971; Danilov 1982; Bennett CMB 2008 and Crelle/LMS; Bugeaud 1996; Waldschmidt arXiv:0908.4031; Pillai 1945. Juggler totality remains open and unclaimed
- **Open:** \(0<n^3-b^4\le 2b^2\) with \(b=a^2\) not a cube and \(n\) odd
- **Decision:** PARK. Record `DIOPHANTINE_ESCALATION_REQUIRED`. Do not start Baker/Thue. Do not claim `GAP_THEOREM_SUFFICIENT` or `ODD_FOURTH_POWER_GREEN`

```text
What was learned
- The window is |X^3-Y^2| <= 2Y with Y=a^4; Hall-scale is X^{1/2}
- Mihailescu and Liouville give constants, not 2b^2
- Roth-type bounds fail because b^{4/3} has height growing with b
- a=97 shows |X^3-Y^2| > 2Y is false without oddness / fourth-power extra structure
- No published theorem specializes to the required bound

Strongest theorem
- none new; the odd-m nearest-cube lemmas remain the Lean facts

Strongest refutation
- Hall, even if proved, does not close the window; Danilov blocks any stronger uniform Hall exponent

Reusable machinery
- diophantine_gap analysis under
  data/research/juggler/odd_sharp_suffix/analysis/

Prior-art status
- literature comparison, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PARK

Why
- The remaining inequality is stronger than the best standard
  square-cube gap statements. Record the exact missing bound
  and do not import Baker/Thue.

Best next question
- Prove |x^3-y^8| > 2y^4 for non-cube y and odd x, after naming
  a method, or exhibit the smallest odd non-square window hit
```

## Juggler near-extremal non-contracting prefixes

- **Date:** 2026-08-27
- **Objective:** Decide whether realized non-monochrome prefixes can keep \(G_j=2^j-3^{o_j}\le 0\) with \(\Delta\) too small to force contraction
- **Hypotheses:** `NEAR_EXTREMAL_STRUCTURE_GREEN`, `DEFECT_DRIVEN_CONTRACTION_GREEN`, `BAD_PREFIX_BOUNDED_GREEN`, `BAD_PREFIX_ARBITRARY`, `NEAR_EXTREMAL_COUNTEREXAMPLE`
- **Major results:** Prefix-NC words start with \(O\); length \(\ge 2\) starts with \(OO\); the mixed family \(O^k E\) (\(k\ge 2\)) is already Lean. The language also contains other mixed patterns (`OOEO`, …). `EOO` has \(\tau=1\) and is not a bad prefix. Scan \(n\le 2000\), \(k\le 10\): 1541 mixed prefix-NC rows, 0 defect-driven certificates, mixed words of length 10 that expand (`n=37`, `n=173`). Closest computed \(\Delta/G\) is on short `OOE` and still far below the formal gap. Classification **NEAR_EXTREMAL_STRUCTURE_GREEN**. No new Lean. No ledger row. Control layer unchanged
- **Refuted ideas:** treating `EOO` block contraction as a prefix-NC escape; treating a horizon hit as an infinite realized family
- **Literature:** `oeis-A007320`; Juggler totality remains open and unclaimed
- **Open:** answered in the prefix-NC admissibility branch as `PREFIX_NC_ARITHMETIC_COMPLEX`; an explicit infinite family remains open
- **Decision:** PARK. Record the prefix-NC language. Do not claim `BAD_PREFIX_BOUNDED_GREEN` or termination

```text
What was learned
- Every prefix-NC word starts with O; length >= 2 starts with OO
- O^k E for k>=2 is prefix-NC (already Lean); other mixed patterns exist
- EOO has tau=1, so it is not a bad prefix
- n=3 realizes OOOE, not OOE
- 1541 mixed prefix-NC rows on n<=2000, k<=10; 0 defect certificates
- Mixed prefix-NC words of length 10 expand (n=37, n=173)

Strongest theorem
- none new; compensated contraction and 2^{k+1}<=3^k remain the Lean facts

Strongest refutation
- EOO is not a prefix-noncontracting escape route

Reusable machinery
- near_extremal_prefixes probe and records under
  docs/research/juggler_near_extremal_prefixes.md

Prior-art status
- finite-prefix language, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PARK

Why
- The combinatorial language is described and the scan shows
  expanding mixed prefixes through the horizon. That is not a
  bound and not a new contraction theorem. Stop.

Best next question
- Answered in the prefix-NC admissibility branch: backward
  floor-cell pullback is `PREFIX_NC_ARITHMETIC_COMPLEX`.
```

## Juggler odd-odd residual admissibility

- **Date:** 2026-08-27
- **Objective:** Test whether a non-extremal `ResidualStep` chain remains finitely admissible, or whether successor constraints tighten until the next odd-odd step is impossible
- **Hypotheses:** `ODD_ODD_ADMISSIBILITY_GREEN`, `ODD_ODD_BOUNDED_GREEN`, `ODD_ODD_VALUATION_GREEN`, `ODD_ODD_MONOTONE_GREEN`, `ODD_ODD_COUNTEREXAMPLE`, or `ODD_ODD_RESIDUAL_COMPLEX`
- **Major results:** `HARD_PROBES` reproduce \(37\to 9317\) (`O^4E^1`), \(9317\to 2233\) (`O^3E^2`), \(69\to 117\), \(77\to 1523\to 243\), \(9\to 11\). Every odd-odd start in \(2\le n\le 80\) has a non-extremal first residual. Interval widths grow on both length-2 continuations. \(v_2(z)\) on the \(37\)-chain is \(2,5,1\). \(y>x\) fails at \(53\to 9\) and after persistence at \(69\to 117\to 3\). Window max non-extremal odd-odd depth is \(2\), a horizon count, not \(L\). No Lean file. Classification **ODD_ODD_RESIDUAL_COMPLEX**. Records: `docs/research/juggler_odd_odd_residual.md`, `docs/problems/juggler_odd_odd_residual.md`, `data/research/juggler/odd_odd_residuals/`. Control layer unchanged
- **Refuted ideas:** successor cells tighten; \(y>x\) is necessary; \(v_2/v_3\) is monotone; exact \(O^k\) towers are the unbounded residual branch; a search-horizon depth is \(L\); a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** answered in the prefix-NC admissibility branch as `PREFIX_NC_ARITHMETIC_COMPLEX`
- **Decision:** CLOSE the non-extremal odd-odd continuation branch as `ODD_ODD_RESIDUAL_COMPLEX`. Do not add Lean. Do not infer a bound from the window

```text
What was learned
- ResidualStep stays the successor; another odd-odd step is ResidualStep plus is_odd_odd plus a positive odd defect
- Those conditions do not tighten: even-run widths grow on 37 and 69
- y>x fails at 53→9 and after persistence at 69→117→3 and 9317→2233
- No first residual in n≤80 is an exact O^k tower
- Depth 2 is a search-horizon count, not a bound L

Strongest theorem
- none new; ResidualStep and PersistentOddResidual remain the Lean facts

Strongest refutation
- interval tightening and y>x; 37→9317→2233 has even-run width 18635→44567460015 and y<x at the second step

Reusable machinery
- research.juggler_sequence.odd_odd_residuals
- data/research/juggler/odd_odd_residuals/

Prior-art status
- negative admissibility result, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- CLOSE

Why
- Every proposed I(S) dies on the known traces. The leftover is ResidualStep rewritten. Stop before a new recurrence object.

Best next question
- Answered in the prefix-NC admissibility branch: backward
  floor-cell pullback is `PREFIX_NC_ARITHMETIC_COMPLEX`.
```

## Juggler prefix-NC arithmetic admissibility

- **Date:** 2026-08-27
- **Objective:** Test whether backward even/odd floor-cell constraints empty the realizing set of a mixed prefix-noncontracting word
- **Hypotheses:** `PREFIX_NC_ADMISSIBILITY_GREEN`, `PREFIX_NC_ESCAPE_SET_SHRINKS`, `PREFIX_NC_NEAR_EXTREMAL_GREEN`, `PREFIX_NC_COUNTEREXAMPLE`, or `PREFIX_NC_ARITHMETIC_COMPLEX`
- **Major results:** \(A(\mathtt{OOE},6)=\{5\}\) **COMPUTATIONALLY VERIFIED**. All \(43\) mixed prefix-NC words of length \(\le 8\) are realized with \(n\le 800\). Empty fiber over images \(1..24\) does not mean unrealizable (`OOEOOOOOOO` at \(173\)). Horizon witnesses: \(37\) realizes `OOOOEOOOEE`, \(173\) realizes `OOEOOOOOOO`, \(2127\) realizes `OOOOEOOOOEE`. Backward constraints are the existing even cell and `odd_cell_unique`. No Lean file. Classification **PREFIX_NC_ARITHMETIC_COMPLEX**. Records: `docs/research/juggler_prefix_nc_admissibility.md`, `docs/problems/juggler_prefix_nc_admissibility.md`, `data/research/juggler/prefix_nc_admissibility/`. Control layer unchanged. `ResidualStep` not extended
- **Refuted ideas:** long mixed prefix-NC words are arithmetically empty; empty-over-image-cap is unrealizable; a search-horizon word is an infinite family; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** answered in the escape-state branch as `ESCAPE_STATE_COMPLEX`
- **Decision:** CLOSE the backward-admissibility branch as `PREFIX_NC_ARITHMETIC_COMPLEX`. Do not add Lean. Do not infer a bound from the window

```text
What was learned
- Backward admissibility is the existing even cell and odd_cell_unique, composed along the word
- A(OOE, 6) = {5}
- Every mixed prefix-NC word of length <= 8 has a realizing start n <= 800
- Empty fiber over images 1..24 is not A(w)=empty; OOEOOOOOOO is realized at 173
- A dangerous finite word is not a dangerous infinite trajectory

Strongest theorem
- none new; inverse-floor cells and odd_cell_unique remain the Lean facts

Strongest refutation
- H1/H2 in the window; all 43 mixed k<=8 words are realized, and OOE at 5 avoids compensated contraction

Reusable machinery
- research.juggler_sequence.prefix_nc_admissibility
- data/research/juggler/prefix_nc_admissibility/

Prior-art status
- negative admissibility result, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- CLOSE

Why
- The combinatorial escape language and the arithmetic language agree through length 8. The leftover is ResidualStep-style cell composition, not a new obstruction. Stop before a cell-tree engine.

Best next question
- Answered in the escape-state branch: the combined escape margin is `ESCAPE_STATE_COMPLEX`.
```

## Juggler escape-state margin

- **Date:** 2026-08-27
- **Objective:** Test whether \(M=\mathrm{formal\_gap}-\Delta\), or a small tuple, is a progress measure on mixed prefix-NC non-contracting prefixes
- **Hypotheses:** `ESCAPE_STATE_INVARIANT_GREEN`, `ESCAPE_MARGIN_GREEN`, `ESCAPE_REGIME_GREEN`, `ESCAPE_COUNTEREXAMPLE`, or `ESCAPE_STATE_COMPLEX`
- **Major results:** On \(G\le 0\), \(M=T_w(n)^{2^k}-n^{2^k}\) **COMPUTATIONALLY VERIFIED**, a **REPARAMETERIZATION** of \(T\ge n\). Sign identity has \(0\) failures. Overshoot \(T-n\) grows on \(9\), \(37\), \(173\). No \(M=0\) return for \(n\ge 2\) in \(n\le 200\), \(k\le 8\). \(187\) escape prefixes; longest \(8\) is the horizon, not \(L\). No Lean file. Classification **ESCAPE_STATE_COMPLEX**. Records: `docs/research/juggler_escape_state.md`, `docs/problems/juggler_escape_state.md`, `data/research/juggler/escape_state/`. Control layer unchanged. `ResidualStep` not extended
- **Refuted ideas:** \(M\) is a new progress law; escape overshoot shrinks; \(M=0\) is a second envelope boundary; a history certificate creates a new future state; a halt theorem
- **Literature:** `oeis-A007320`; no nontrivial Juggler cycle is claimed
- **Open:** not another local rewrite of \(T\ge n\); a global well-founded measure remains the global problem
- **Decision:** CLOSE the escape-state branch as `ESCAPE_STATE_COMPLEX`. Do not add Lean. Do not infer a bound from the window

```text
What was learned
- On G<=0, M = T^{2^k}-n^{2^k}, so M>=0 iff the prefix does not contract
- That is compensated-contraction / actual contraction rewritten, not a new state
- Escape overshoot grows: 9 goes 11→36; 37 goes 9317→24906114455136
- The future orbit is determined by the current integer; history is only a past certificate
- Indefinite escape is non-termination

Strongest theorem
- none new; the envelope and compensated contraction remain the Lean facts

Strongest refutation
- M is a progress measure; it is T>=n, and overshoot grows on known expanders

Reusable machinery
- research.juggler_sequence.escape_state
- data/research/juggler/escape_state/

Prior-art status
- negative progress-measure result, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- CLOSE

Why
- The escape predicate is prefix-NC plus T>=n. No compact I with I_{j+1}<I_j survived. Stop before a state machine.

Best next question
- Not another local rewrite of T>=n. A global well-founded measure, if it exists, is not this margin.
```

## Juggler excursions and first-return induction

- **Date:** 2026-08-27
- **Objective:** Test whether first-return-below words can be certified by the existing finite-word envelope and defect calculus, without a new engine
- **Hypotheses:** `EXCURSION_ENVELOPE_GREEN`, `FIRST_RETURN_DEFECT_GREEN`, `MINIMAL_COUNTEREXAMPLE_ROUTE_GREEN`, `EXCURSION_STRUCTURE_GREEN`, `EXCURSION_COUNTEREXAMPLE`, or `EXCURSION_INDUCTION_COMPLEX`
- **Major results:** On \(2\le n\le 2000\), all 1999 starts return below \(n\) before horizon \(10^4\). Every first-return word has \(2^k>3^o\) **COMPUTATIONALLY VERIFIED**. First-defect and peak-suffix never certify a return the exponent gap misses. `COMPUTED_ONLY` count \(0\). Lemma A universal **REFUTED** (even \(n\) has word \(E\)). Lemma A for odd starts and Lemma B hold on the window. No measure \(M\) other than the defined return. Classification **EXCURSION_ENVELOPE_GREEN**. Records: `docs/research/juggler_excursions.md`, `docs/problems/juggler_excursions.md`, `data/research/juggler/excursions/`. Control layer unchanged. `ResidualStep` not extended. No Lean file
- **Refuted ideas:** first-return words must be non-extremal for every start; full-word \(\Delta\) as a certificate on a completed return; return value \(<n\) as a new canonical measure
- **Literature:** `oeis-A007320`; escape-state / odd-odd residual / prefix-NC admissibility / CycleDiophantine remain closed
- **Open:** does every \(n\ge 2\) realize a finite prefix with \(3^o<2^k\)? That would give `FiniteProgress` from `power_bound_contracts`. An infinite prefix-NC itinerary would be a non-terminator
- **Decision:** PARK the excursion branch as `EXCURSION_ENVELOPE_GREEN`. Do not add Lean. Do not infer a bound from the window. Do not claim termination

```text
What was learned
- τ_<, τ_≤, and the peak/return split are distinct; the primary object is first return strictly below the start
- On n=2..2000 every first-return word is formally contracting, so power_bound_contracts already certifies the completed return
- First-defect and peak-suffix are extra, not independent certificates
- A MinimalNonTerm has no finite excursion; the census cannot produce a smaller MNT
- The missing theorem is existence of a contracting prefix, not another local residual

Strongest theorem
- none new; power_bound_contracts remains the Lean fact applied post hoc to w(n)

Strongest refutation
- Lemma A for every start: even n returns by the extremal word E

Reusable machinery
- research.juggler_sequence.excursions
- data/research/juggler/excursions/

Prior-art status
- window-level envelope observation, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PARK

Why
- The window is clean enough to name a candidate theorem, not complete enough to prove it. Stop before Lean and before a new global state engine.

Best next question
- Does every n>=2 realize a finite prefix with 3^o<2^k?
```

## Juggler two-sided minimal-counterexample corridor

- **Date:** 2026-08-27
- **Objective:** Test whether a pivot corridor \(x^{2^r}\le n^{3^o}\) and \(n^{2^s}\le x^{3^q}\) constrains \(x\) beyond the concatenated-word test, using stay-above prefixes of actual first-return paths
- **Hypotheses:** `CORRIDOR_REPACKAGING`, `CORRIDOR_RIGIDITY_GREEN`, `CORRIDOR_DEFECT_GREEN`, `CORRIDOR_COUNTEREXAMPLE`
- **Major results:** On \(2\le n\le 2000\), 45948 corridors; 39137 stay-above. Available exact comparisons satisfy forward, reverse, and compat. Reverse never fires unless \(2^{r+s}>3^{o+q}\). Mixed equality 0. Both-sides equality 0. Defect-over-gap 0. Extremal equality hits are monochrome towers. Classification **CORRIDOR_REPACKAGING**. Records: `docs/research/juggler_corridor.md`, `docs/problems/juggler_corridor.md`, `data/research/juggler/corridor/`. Control layer unchanged. `ResidualStep` not extended. No Lean file
- **Refuted ideas:** the corridor is a new opposite inequality; reverse-without-fullword on stay-above or at return; mixed saturation; even stay-above corridors
- **Literature:** `oeis-A007320`; this is not the REFUTED two-sided exponent-only law; excursion / escape-state / prefix-NC / CycleDiophantine remain closed
- **Open:** does every \(n\ge 2\) realize a finite prefix with \(3^o<2^k\)? The corridor does not replace that existence statement
- **Decision:** CLOSE the corridor branch as `CORRIDOR_REPACKAGING`. Do not add Lean. Do not claim termination

```text
What was learned
- The future lower bound T^j(n)>=n is already minimal_nonterm_image_ge
- On stay-above segments, forward, reverse, and compat are power_bound_word plus image>=n
- Composition 2^{r+s}<=3^{o+q} is contraposed power_bound_contracts on the concatenated word
- Reverse never certified a return the exponent gap missed, including at non-peak pivots
- Closest slack is the trivial single-odd gap 3-2=1; 2^a=3^b has no positive solutions, so the corridor never algebraically closes

Strongest theorem
- none new; power_bound_word, power_bound_contracts, and minimal_nonterm_image_ge remain the Lean facts

Strongest refutation
- the corridor supplies a pivot-specific contraction or rigidity not implied by the concatenated word

Reusable machinery
- research.juggler_sequence.corridor
- data/research/juggler/corridor/

Prior-art status
- negative corridor result, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- CLOSE

Why
- Every exact corridor predicate collapsed to the existing envelope plus stay-above. Stop before Lean and before a corridor automaton.

Best next question
- Does every n>=2 realize a finite prefix with 3^o<2^k?
```

## Juggler first positive-drift crossing and endpoint arithmetic

- **Date:** 2026-08-27
- **Objective:** Test whether a long actual prefix-NC orbit forces new arithmetic on the endpoint \(x_k=T^k(n)\), and characterize the first \(G_k>0\) crossing
- **Hypotheses:** `DRIFT_ENDPOINT_GREEN`, `DRIFT_FIRST_CROSSING_GREEN`, `DRIFT_ENDPOINT_FILTRATION_GREEN`, `DRIFT_INDUCTION_GREEN`, `DRIFT_ENDPOINT_COUNTEREXAMPLE`, `DRIFT_ENDPOINT_COMPLEX`
- **Major results:** On \(2\le n\le 2000\), all 1999 starts cross; absorbed-at-1 still NC is 0. Every crossing is an even letter with \(2^{\tau-1}\le 3^o<2^\tau\) **COMPUTATIONALLY VERIFIED**, a **REPARAMETERIZATION** of the \(G\)-recurrence. Mixed NC prefixes 2797; endpoints split on parity (1428/1369), square (8/2789), and \(\gcd\) (493/2304). Only universal mixed predicate is \(T^k\ge n\), the old non-contraction identity. Longest \(\tau_+=70\) at \(n=193\). Classification **DRIFT_ENDPOINT_COMPLEX**. Records: `docs/research/juggler_drift_crossing.md`, `docs/problems/juggler_drift_crossing.md`, `data/research/juggler/drift_crossing/`. Control layer unchanged. `ResidualStep` not extended. No Lean file
- **Refuted ideas:** long prefix-NC survival forces even/odd/square/\(v_2\)/\(v_3\)/large gcd/fixed residue; crossing predecessor is a square; \(\tau_+<\infty\) from a finite window
- **Literature:** `oeis-A007320`; corridor / escape-state / prefix-NC / CycleDiophantine remain closed; odd-fourth-power remains parked
- **Open:** does every \(n\ge 2\) realize a finite prefix with \(3^o<2^k\)? Endpoint arithmetic does not supply the obstruction
- **Decision:** CLOSE the drift-crossing branch as `DRIFT_ENDPOINT_COMPLEX`. Do not add Lean. Do not claim termination

```text
What was learned
- tau_+ exists on n=2..2000; no start reaches 1 still prefix-NC
- First positive G is always an even letter; that is the G-recurrence, not a Juggler endpoint law
- Mixed prefix-NC endpoints keep both parities, both gcd regimes, and both square statuses
- T^k >= n on every mixed NC prefix in the window is tau_+=tau_< rewritten
- Longest actual postponement is n=193 with tau_+=70; the last NC state 6498 has gcd 1 and is not a square

Strongest theorem
- none new; power_bound_contracts remains the Lean fact that G>0 implies T^k<n

Strongest refutation
- long prefix-NC survival forces a shrinking endpoint class

Reusable machinery
- research.juggler_sequence.drift_crossing
- data/research/juggler/drift_crossing/

Prior-art status
- negative endpoint-filtration result, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- CLOSE

Why
- The only exact crossing law is the G-recurrence. Mixed endpoints stay arithmetically free. Stop before Lean and before another endpoint state machine.

Best next question
- A genuine existence argument that every n>=2 eventually takes an even step with 2^{k-1} <= 3^{o} < 2^k, not another endpoint laboratory.
```

## Juggler drift-first-passage tree

- **Date:** 2026-08-27
- **Objective:** Test whether nested realizing sets \(A_w^{NC}\) of actual prefix-NC words acquire a named arithmetic constraint that forbids indefinite continuation
- **Hypotheses:** `DRIFT_TREE_PRUNING_GREEN`, `DRIFT_FIRST_PASSAGE_UNBOUNDED`, `DRIFT_FIRST_PASSAGE_COMPLEX`, `DRIFT_FIRST_PASSAGE_INCOMPLETE`, `DRIFT_FIRST_PASSAGE_COUNTEREXAMPLE`
- **Major results:** Nested window \(n=2..2000\): \(1318\) prefix-NC words, compression \(\approx 1\) after length \(4\); tags empty \(1072\), same \(1048\), tautological subset \(10\), named-thinner \(259\) (residue/modulus artefacts, not a rule). Hunt \(n\le 10^5\): max \(\tau_+=253\) at \(n=78901\); \(n=193\), \(\tau_+=70\), last NC \(6498\) still holds; leftover \(n=48443\) at the bit cap. Classification **DRIFT_FIRST_PASSAGE_COMPLEX**. Records: `docs/research/juggler_drift_first_passage.md`, `docs/problems/juggler_drift_first_passage.md`, `data/research/juggler/drift_first_passage/`. Control layer unchanged. `ResidualStep` not extended. No Lean file
- **Refuted ideas:** nested start-set signatures compress below the words; a cardinality drop is a pruning rule; \(\tau_+\le 70\); late first-passage starts occupy a thin residue class; a larger record is an unbounded family
- **Literature:** `oeis-A007320`; Terras stopping-time is methodological only (`terras-1976-stopping-time`); prefix-NC / endpoint / corridor / CycleDiophantine remain closed; odd-fourth-power remains parked
- **Open:** does every \(n\ge 2\) realize a finite prefix with \(3^o<2^k\)? Nested start-sets do not supply the obstruction
- **Decision:** CLOSE the drift-first-passage branch as `DRIFT_FIRST_PASSAGE_COMPLEX`. Do not add Lean. Do not claim termination

```text
What was learned
- A_w as part of the node is the right object; window-exact nested sets still do not prune
- After length 4, distinct arithmetic signatures track the words (compression near 1)
- Named-thinner hits are residue death or modulus artefacts of longer prefixes, not a rule
- Least-constrained mixed prefixes are the short words OOE / OOEO / OOOE
- Hunt record is n=78901 with tau_+=253; n=193 / tau_+=70 remains the nested-window regression
- One hunt start (n=48443) hit the bit cap still prefix-NC; that cutoff is not L

Strongest theorem
- none new; power_bound_contracts remains the Lean fact that G>0 implies T^k<n

Strongest refutation
- nested A_w signatures compress, or tau_+ <= 70

Reusable machinery
- research.juggler_sequence.drift_first_passage
- data/research/juggler/drift_first_passage/

Prior-art status
- negative nested-set result plus a larger delay record, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- CLOSE

Why
- The nested start-set does not acquire a named pruning rule. Isolated larger tau_+ records change the known delay, not the induction. Stop before Lean and before a formal prefix tree.

Best next question
- A genuine existence argument that every n>=2 eventually takes an even step with 2^{k-1} <= 3^{o} < 2^k, not another start-set census.
```

## Juggler layer architecture rewrite

- **Date:** 2026-08-27
- **Objective:** Rewrite the Juggler Lean stack as one-way layers under `Problems.Juggler` so the only unproved global arrow is finite coefficient stopping time
- **Hypotheses:** the missing object is a first-passage / certificate separation, not another word identity; fused `FloorPower` caused recent CLOSE loops
- **Major results:** Live Lean is `formal/Problems/Juggler/` with barrel `formal/Problems/Juggler.lean`. Engine copies of FloorPower, Progress, MinimalNonTerm, RepeatedOE, OddRunFinancing, OddOddFrontier, ResidualChain, ResidualPath, RepeatedBlock, CycleWord, and CycleDiophantine are deleted; no export shims. `follows ↔ word`, `HasFiniteCoeffStop → HasFiniteStop`, `DescentCertificate → HasFiniteStop ∨ ReachesOne`, and `HasFiniteCoeffStop → ¬MinimalNonTerm` are proved. `∀ n ≥ 2, HasFiniteCoeffStop n` and `MinimalNonTerm n → HasFiniteCoeffStop n` are first-class unproved Props. Python paths go through `research.juggler_sequence.lean_paths`. No new hunt. No halt theorem. No ledger row (reparameterization / packaging)
- **Refuted ideas:** dual Engine/Juggler namespaces; leftover FloorPower as a compatibility layer
- **Literature:** `oeis-A007320`; Terras stopping-time is methodological only (`terras-1976-stopping-time`); drift-crossing / drift-first-passage remain closed
- **Open:** does every \(n\ge 2\) have finite coefficient / drift stopping time?
- **Decision:** PROMOTE the architecture. Do not claim termination

```text
What was learned
- The fused FloorPower stack mixed orbit, word, envelope, stopping time, and certificates
- follows ↔ word is the itinerary bridge; G(w) is a property of the word alone
- Finite coefficient stop already implies a strict smaller iterate
- One inductive DescentCertificate replaces Descent/Capture/FiniteProgress as parallel defs
- MinimalNonTerm is incompatible with a realized coefficient stop
- Scale, residuals, and cycles are downward-only leaves

Strongest theorem
- HasFiniteCoeffStop n → HasFiniteStop n, wrapping power_bound_contracts

Strongest refutation
- none new; the rewrite does not settle τ_G(n)<∞

Reusable machinery
- formal/Problems/Juggler/
- research.juggler_sequence.lean_paths

Prior-art status
- architectural reparameterization of existing local lemmas, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack; control layer not modified

Branch status
- PROMOTE

Why
- Engine Juggler files are gone, layers compile one-way, and the missing implication is a first-class Lean statement.

Best next question
- Does every n >= 2 have finite coefficient / drift stopping time?
```

## Juggler global accumulated defect

- **Date:** 2026-08-27
- **Objective:** Assemble local Juggler floor remainders into one exact compositional global defect
- **Hypotheses:** the correct recurrence is a weighted lift through later exponents, not `Δ_{i+1}=Δ_i+ρ_i`; the envelope slack is a theorem, not the definition
- **Major results:** `powGap a ρ e = (a+ρ)^e-a^e`. Even step keeps the old slack and lifts `ρ` through `2^k`. Odd step cubes the running slack and then lifts `ρ`. Lean `global_defect_identity`: `n^{3^o}=T_w(n)^{2^k}+Δ_w(n)`. Envelope is the corollary `Δ≥0`. `Δ=0` iff every local remainder vanishes iff `localsTight` iff `PowerBoundEq`. Mixed realized words have `Δ>0`. First-defect bound `ρ_i^{2^i}≤Δ`. Composition is the two-term lift `powGap(mid^{2^{|u|}},Δ_u,3^{#O(v)})+powGap(T_v^{2^{|v|}},Δ_v,2^{|u|})`. A `ResidualStep` carries the same identity. On a CE, `Δ+n^{2^k}≤n^{3^o}`. Short-word census `n≤80`, length `≤5` matches the slack exactly. No halt theorem
- **Refuted ideas:** additive accumulation `Δ_{i+1}=Δ_i+ρ_i`; treating `Δ` as a prior subtraction of `PowerBound`; `Δ` larger than the formal surplus forbids `OOE`/`OOEO`/`OOOE` on a CE (that inequality is `T_w(n)<n`)
- **Literature:** OEIS A007320; existing envelope / equality / local-defect layers
- **Open:** can a first-defect lower bound beat `n^{3^o}-n^{2^k}` on a mixed expanding class?
- **Decision:** PROMOTE the global defect layer. Do not claim termination

```text
What was learned
- Local remainders must be lifted through later 2^k and 3^{#O} exponents
- The envelope slack is exactly this lifted accumulation
- Zero global defect is the existing rigid equality tower
- Composition is polynomial, not additive
- The CE surplus inequality restates T_w(n)≥n and does not kill expanding mixed prefixes

Strongest theorem
- n^{3^{#O(w)}} = T_w(n)^{2^{|w|}} + Δ_w(n) for every realized finite word

Strongest refutation
- Δ > n^{3^o}-n^{2^k} on an expanding mixed CE prefix: equivalent to T_w(n)<n

Reusable machinery
- formal/Problems/Juggler/GlobalDefect.lean
- research.juggler_sequence.global_defect

Prior-art status
- constructive strengthening of PowerBound / powerDeficit, not a Juggler halt result

Complexity profile
- unchanged flood order; no new production attack

Branch status
- PROMOTE

Why
- The recurrence, identity, equality characterization, and composition law are new exact statements. They do not prove termination.

Best next question
- Can a quantitative lower bound on Δ beat the formal surplus on some mixed expanding class?
```

