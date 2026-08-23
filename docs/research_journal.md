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

