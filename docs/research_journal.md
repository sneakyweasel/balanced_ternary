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


