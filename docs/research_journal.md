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

