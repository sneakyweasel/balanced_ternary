# Theorem ledger

Machine-readable sibling: [theorem_ledger.json](theorem_ledger.json).

Tags:

- `EXACT — LEAN VERIFIED`
- `EXACT — HUMAN PROOF`
- `COMPUTATIONALLY VERIFIED`
- `CONJECTURE`
- `REFUTED`
- `REPARAMETERIZATION`

Provenance is copied from the existing mathematical record and Lean README.
This ledger does not rewrite history.

| ID | Tag | Statement (short) | Source | Lean | Tests |
|----|-----|-------------------|--------|------|-------|
| BT-encode-unique | EXACT — HUMAN PROOF | Unique canonical balanced ternary word | docs/mathematics.md | Representation/Words | test_representation |
| BT-D-S | EXACT — LEAN VERIFIED | D∘S = id | docs/balanced_ternary_operators.md | Operators/DigitDerivative | test_operators |
| BT-W-not-involution | REFUTED | W involutive on Z | docs/operator_algebra.md | Operators/Algebra W_not_involution_on_three | test_operators, regression |
| BT-Pn3 | EXACT — LEAN VERIFIED | P_n(3)=n | docs/balanced_ternary_polynomials.md | Operators/Polynomial | test_operator_branch |
| C-T-welldefined | EXACT — HUMAN PROOF | Accelerated T on positive odds | docs/collatz_mathematics.md | | test_core |
| C-append-plus | EXACT — HUMAN PROOF | BT(3n+1)=BT(n)+ | docs/collatz_mathematics.md | Representation/Words | test_theorems |
| C-odd-part-not-one-fst | EXACT — HUMAN PROOF | Unrestricted odd-part is not one rational transduction | docs/collatz_mathematics.md §12 | | test_transducers (constructive side) |
| C-affine-formula | EXACT — LEAN VERIFIED | T^m=(3^m n+C)/2^K | docs/collatz_itinerary_compatibility.md | Problems/Collatz | test_affine_formula |
| C-R-direct | EXACT — LEAN VERIFIED | Direct residue formula for R | docs/collatz_dual_coding.md | Problems/Collatz | test_dual_code |
| C-lift-zero | EXACT — LEAN VERIFIED | Realizer iff eventual zero lift | docs/collatz_zero_lift.md | Problems/Collatz/Lift,Cylinder | test_zero_lift |
| C-endpoint | EXACT — LEAN VERIFIED | Kramer endpoint / 2-adic endpoint congruences | docs/literature_comparison.md | Problems/Collatz/Endpoint | test_four_coordinate_core |
| C-center | EXACT — LEAN VERIFIED | Affine-center numerator identities | docs/collatz_affine_center.md | Problems/Collatz/Center | test_affine_center |
| C-gap | EXACT — LEAN VERIFIED | Affine gap recurrence | docs/collatz_fixed_integer_asymptotics.md | Problems/Collatz/FixedInteger | test_fixed_integer |
| C-nstar-le-n | REFUTED | n*≤n | docs/collatz_fixed_integer_asymptotics.md | | test_fixed_integer n=165 |
| C-cycles | EXACT — LEAN VERIFIED | Expanding periods excluded; D\|C; even amplitude | docs/collatz_cycle_languages.md | Problems/Collatz/Cycles | test_cycles |
| C-Nk | CONJECTURE | N_k=2^k+1 | docs/collatz_research_questions.md | | complexity tests k≤4 |
| BTC-decomp | EXACT — LEAN VERIFIED | n = lsd + 3 D(n) | docs/theory/digit_derivative.md | BTCalculus/Derivative | test_calculus_identities |
| BTC-D-I | EXACT — LEAN VERIFIED | D ∘ I_a = id | docs/theory/digit_derivative.md | BTCalculus/Integral | test_calculus_identities |
| BTC-P-band | EXACT — LEAN VERIFIED | P_a ∘ P_b = P_a | docs/theory/digit_derivative.md | BTCalculus/Integral | test_calculus_identities |
| BTC-D-mul | EXACT — LEAN VERIFIED | twisted Leibniz rule for D(xy) | docs/theory/digit_derivative.md | BTCalculus/Algebra | test_calculus_identities |
| BTC-D-add | EXACT — LEAN VERIFIED | D(x+y)=D(x)+D(y)+carry | docs/theory/digit_derivative.md | BTCalculus/Algebra | test_calculus_identities |
| BTC-trit-kleene | EXACT — LEAN VERIFIED | Trit is a 3-element Kleene algebra, not Boolean | docs/theory/trit_algebra.md | BTCalculus/Trit | test_calculus_trit |
| BTC-cmp3 | EXACT — LEAN VERIFIED | cmp3 translation / negation / antisymmetry | docs/theory/trit_control.md | BTCalculus/Comparison | test_calculus_trit |
| BTC-select3 | EXACT — LEAN VERIFIED | select3 represents Trit→ℤ; abs/min/max | docs/theory/trit_control.md | BTCalculus/Select | test_calculus_select |
| BTN-divmod | EXACT — LEAN VERIFIED | unique trit residue `c = 3q + r` | docs/theory/normalization_rewrite_system.md | BTCalculus/Normalization | test_normtheory_rewrite |
| BTN-step-value | EXACT — LEAN VERIFIED | value(P → P') = value(P) | docs/theory/normalization_rewrite_system.md | BTCalculus/Normalization | test_normtheory_rewrite |
| BTN-nf | EXACT — LEAN VERIFIED | normalize_LSD(P) = encodeZ(value(P)); all trits | docs/theory/balanced_ternary_normalization.md | BTCalculus/Normalization | test_normtheory_rewrite |
| BTN-lex | EXACT — LEAN VERIFIED | LSD step strictly decreases abs-lex rank | docs/theory/normalization_rewrite_system.md | BTCalculus/Normalization | test_normtheory_rewrite |
| BTN-carry-bound | EXACT — LEAN VERIFIED | `3\|DZ n\| ≤ \|n\|+1`; `|q| ≤ (B+1)/3` on `[-B,B]` | docs/theory/normalization_complexity.md | BTCalculus/Normalization | test_normtheory_strategies |
| BTN-confluence | EXACT — LEAN VERIFIED | stripped rewrite is locally and globally confluent; `[-5,2]` joins after `stripHigh` | docs/theory/normalization_rewrite_system.md | BTCalculus/Confluence | test_normtheory_rewrite |
| BTJ-hatD | EXACT — LEAN VERIFIED | value(hatD_raw(P))=D(value(P)); `[2]` naive drop fails | docs/theory/polynomial_jet_calculus.md | BTCalculus/NormalizedDerivative | test_hatd, test_m14_regressions |
| BTJ-section | EXACT — LEAN VERIFIED | f(a+3x)=ρ_a(f)+3 𝔇_a f(x) | docs/theory/polynomial_jet_calculus.md | BTCalculus/Polynomial | test_section |
| BTJ-product | EXACT — LEAN VERIFIED | twisted Leibniz for 𝔇_a(fg) | docs/theory/polynomial_jet_calculus.md | BTCalculus/Composition | test_section |
| BTJ-comp | EXACT — LEAN VERIFIED | 𝔇_a(f∘g)=𝔇_{ρ_a(g)}f ∘ 𝔇_a g | docs/theory/polynomial_jet_calculus.md | BTCalculus/Composition | test_section |
| BTJ-jet | EXACT — LEAN VERIFIED | finite-depth function-jet reconstruction | docs/theory/balanced_ternary_jets.md | BTCalculus/Jet | test_jets |
| BTJ-degree | EXACT — HUMAN PROOF | deg 𝔇_a f = deg f (d≥1); LC = 3^{d-1} LC(f) | docs/theory/polynomial_jet_calculus.md | | test_section |
| BTA-equiv | EXACT — LEAN VERIFIED | finite-horizon ≡_k is an equivalence; recursive iff outputs | docs/theory/residual_state_complexity.md | BTCalculus/Residual | test_myhill_nerode |
| BTA-x2-raw | EXACT — HUMAN PROOF | R_k(x^2)=(3^k-1)/2 | docs/theory/quadratic_residual_complexity.md | BTCalculus/Quadratic residualAlong_Xsq_injective | test_myhill_nerode |
| BTA-x2-mn | EXACT — HUMAN PROOF | M_k(x^2)=R_k(x^2)=(3^k-1)/2 | docs/theory/quadratic_residual_complexity.md | BTCalculus/Quadratic equivK_quad, xsq_equivK_iff_eq | test_myhill_nerode |
| BTA-x2-quad-form | EXACT — LEAN VERIFIED | f_w(x)=3^{\|w\|}x^2+2p(w)x+DZ^{\|w\|}(p(w)^2) | docs/theory/quadratic_residual_complexity.md | BTCalculus/Quadratic residualAlong_Xsq | test_myhill_nerode |
| BTA-quad-mod | EXACT — LEAN VERIFIED | deg≤2: f≡_k g iff coeffs agree mod 3^k | docs/theory/quadratic_residual_complexity.md | BTCalculus/Quadratic equivK_quad | test_myhill_nerode |
| BTA-x3-merge | EXACT — LEAN VERIFIED | first x^3 merge at k=2, delayed distinction | docs/theory/polynomial_function_congruence.md | BTCalculus/PolynomialFunctionsMod x3_first_merge_equiv_two | test_poly_congruence |
| BTA-x4-merge | EXACT — LEAN VERIFIED | first x^4 merge at k=3, delayed distinction | docs/theory/polynomial_function_congruence.md | BTCalculus/PolynomialFunctionsMod x4_first_merge_equiv_three | test_poly_congruence |
| BTA-fn-congr | EXACT — LEAN VERIFIED | f≡_k g iff 3^k divides (f-g)(n) for all n | docs/theory/polynomial_function_congruence.md | BTCalculus/PolynomialFunctionsMod equivK_iff_functionCongr | test_poly_congruence |
| BTA-Ik-newton | EXACT — HUMAN PROOF | I_k is Newton residues divisible by 3^k | docs/theory/polynomial_function_congruence.md | cubic case vanishesMod_cubic_iff | test_poly_congruence |
| BTA-quad-vanish | EXACT — LEAN VERIFIED | deg≤2: vanishes as a function iff coeffs divisible by 3^k | docs/theory/polynomial_function_congruence.md | BTCalculus/PolynomialFunctionsMod vanishesMod_quad_iff | test_poly_congruence |
| BTA-cubic-vanish | EXACT — LEAN VERIFIED | cubic vanishing iff 3^k divides D, A+B+C, 3A+B, 6A | docs/theory/polynomial_function_congruence.md | BTCalculus/PolynomialFunctionsMod vanishesMod_cubic_iff | test_poly_congruence |
| BTA-x3-x | EXACT — LEAN VERIFIED | x^3-x vanishes mod 3, leading coeff not divisible by 3 | docs/theory/polynomial_function_congruence.md | BTCalculus/PolynomialFunctionsMod X_pow_three_sub_X_vanishes_one | test_poly_congruence |
| BTA-tau | EXACT — HUMAN PROOF | τ(f,g)=1+min v_3(Δ^j (f-g)(0)) for f≠g | docs/theory/polynomial_function_congruence.md | | test_poly_congruence |
| BTA-coeffwise-nec | REFUTED | 3^k must divide every monomial coefficient for function vanishing | docs/theory/polynomial_function_congruence.md | not_three_dvd_coeff_X_pow_three_sub_X | test_poly_congruence |
| BTA-tau-minc | REFUTED | τ=1+min v_3(c_j) | docs/theory/polynomial_function_congruence.md | | test_poly_congruence |
| BTA-sample | REFUTED | sample LSD min = M_k; witness x^2 k=3 (7 vs 13) | docs/theory/residual_state_complexity.md | | test_myhill_nerode |
| BTA-cascade | EXACT — LEAN VERIFIED | outputAlong(w,f∘g)=outputAlong(outputAlong(w,g),f) | docs/theory/residual_state_complexity.md | BTCalculus/TransducerComposition | test_myhill_nerode |
| BTA-product | EXACT — HUMAN PROOF | M_k(f∘g)≤M_k(f)M_k(g) | docs/theory/residual_state_complexity.md | | test_myhill_nerode |
| BTA-locality-small | REFUTED | prefix locality ⇒ small automaton | docs/theory/residual_state_complexity.md | | test_myhill_nerode |
| BTA-hatD-B | EXACT — HUMAN PROOF | bounded-B hat D is N_B then drop; not FST on Z | docs/theory/residual_state_complexity.md | | test_myhill_nerode |
| BTA-x3-form | EXACT — LEAN VERIFIED | f_w(x)=3^{2m}x^3+3^{m+1}p x^2+3p^2 x+DZ^m(p^3) | docs/theory/cubic_residual_image.md | BTCalculus/CubicResidual residualAlong_Xcube | test_cubic_residual |
| BTA-x3-raw | EXACT — LEAN VERIFIED | R_k(x^3)=(3^k-1)/2 | docs/theory/cubic_residual_image.md | BTCalculus/CubicResidual residualAlong_Xcube_injective | test_cubic_residual |
| BTA-x3-newton | EXACT — LEAN VERIFIED | Newton coords of a cubic and of the residual family | docs/theory/cubic_residual_image.md | BTCalculus/CubicResidual newton_cubicResid | test_cubic_residual |
| BTA-x3-section | EXACT — LEAN VERIFIED | cubic Newton section step N3'=9 N3, N2'=3 N2+3(a+2)N3 | docs/theory/cubic_residual_image.md | BTCalculus/CubicResidual sectionDeriv_cubic | test_cubic_residual |
| BTA-x3-equiv-N | EXACT — LEAN VERIFIED | cubics: ≡_k iff Newton residues agree mod 3^k | docs/theory/cubic_residual_image.md | BTCalculus/CubicResidual equivK_cubic_newton | test_cubic_residual |
| BTA-x3-Fk | EXACT — HUMAN PROOF | M_k(x^3)=|Im F_k| for F_k(m,p)=Φ_k(f_{(m,p)}) | docs/theory/cubic_residual_image.md | equivK_cubic_newton | test_cubic_residual |
| BTA-x3-shallow | EXACT — HUMAN PROOF | residuals with 2m+1<k are ≡_k-separated | docs/theory/cubic_residual_image.md | | test_cubic_residual |
| BTA-x3-prefix | REFUTED | Newton classes of x^3 are congruence classes of p(w) | docs/theory/cubic_residual_image.md | | test_cubic_residual |
| BTA-x3-lift | REFUTED | M_{k+1}(x^3)=3 M_k(x^3)+1 | docs/theory/cubic_residual_image.md | | test_cubic_residual |
| BTA-x3-n2 | EXACT — LEAN VERIFIED | same-depth N2 is 3^{k-m-1}|(p-q); injective on P_m if 2m+1≤k | docs/theory/cubic_residual_fibres.md | BTCalculus/CubicFibres sameDepth_n2_injective | test_cubic_fibres |
| BTA-x3-n1fac | EXACT — LEAN VERIFIED | N1(p)-N1(q)=3(p-q)(p+q+3^m) | docs/theory/cubic_residual_fibres.md | BTCalculus/CubicFibres n1Resid_diff | test_cubic_fibres |
| BTA-x3-n2n1 | REFUTED | same-depth N2 implies N1 | docs/theory/cubic_residual_fibres.md | | test_cubic_fibres |
| BTA-x3-n21n0 | REFUTED | same-depth N2+N1 imply N0 | docs/theory/cubic_residual_fibres.md | | test_cubic_fibres |
| BTA-x3-n3gate | EXACT — LEAN VERIFIED | cross-depth N3 agrees iff k≤2 min(m,n)+1 or m=n | docs/theory/cubic_residual_fibres.md | BTCalculus/CubicFibres n3_dvd_iff | test_cubic_fibres |
| BTA-x3-sign | EXACT — LEAN VERIFIED | odd pair: N2 iff N1; N0 iff 3^k\|D^m(p^3) | docs/theory/cubic_residual_fibres.md | BTCalculus/CubicFibres sign_n0 | test_cubic_fibres |
| BTA-x3-Ckm | EXACT — HUMAN PROOF | C_{k,m}=3^m whenever 2m+1≤k | docs/theory/cubic_residual_fibres.md | sameDepth_n2_injective | test_cubic_fibres |
| BTA-x3-allsign | REFUTED | every cubic fibre is a sign pair | docs/theory/cubic_residual_fibres.md | | test_cubic_fibres |
| BTA-x3-deep-N | EXACT — LEAN VERIFIED | deepest layer: N3=N2=0, N1≡3p^2 (k≥2) | docs/theory/cubic_deepest_layer.md | BTCalculus/CubicDeepestLayer deepest_n1_mod | test_cubic_deepest |
| BTA-x3-deep-crit | EXACT — LEAN VERIFIED | deepest fibres iff p^2≡q^2 (mod 3^{k-1}) and N0 agrees | docs/theory/cubic_deepest_layer.md | BTCalculus/CubicDeepestLayer deepest_equiv_iff | test_cubic_deepest |
| BTA-x3-deep-zero | EXACT — LEAN VERIFIED | deepest 0-fibre is 3^{ceil((2k-1)/3)}|p | docs/theory/cubic_deepest_layer.md | BTCalculus/CubicDeepestLayer zero_fibre_imp | test_cubic_deepest |
| BTA-x3-deep-coset | REFUTED | every deepest fibre is a full 3-adic coset | docs/theory/cubic_deepest_layer.md | | test_cubic_deepest |
| BTA-x3-Ckk-1 | EXACT — HUMAN PROOF | C_{k,k-1}=1+Σ_s I_{k,s} with closed high-stratum J(k,s) | docs/theory/cubic_deepest_layer.md | | test_cubic_deepest |
| BTA-x3-inter-N | EXACT — LEAN VERIFIED | m=k-2: N3=0, N2≡2·3^{k-1}p (k≥3), N1≡3p^2+3^{k-1}p (k≥4) | docs/theory/cubic_intermediate_layer.md | BTCalculus/CubicIntermediateLayer inter_n2_mod | test_cubic_layer |
| BTA-x3-inter-crit | EXACT — LEAN VERIFIED | m=k-2 fibres iff p≡q (mod 3) and 3^{k-1}|(p-q)(p+q+3^{k-2}) and N0 agrees | docs/theory/cubic_intermediate_layer.md | BTCalculus/CubicIntermediateLayer inter_equiv_iff | test_cubic_layer |
| BTA-x3-inter-lift | EXACT — LEAN VERIFIED | horizon k refines k-1 at depth k-2; unit signs split | docs/theory/cubic_intermediate_layer.md | inter_horizon_refines, unit_sign_n2_splits | test_cubic_layer |
| BTA-x3-inter-n21n0 | REFUTED | at m=k-2, N2+N1 imply N0 | docs/theory/cubic_intermediate_layer.md | | test_cubic_layer |
| BTA-x3-inter-eqprev | REFUTED | C_{k,k-2}=C_{k-1,k-2} | docs/theory/cubic_intermediate_layer.md | | test_cubic_layer |
| BTA-x3-inter-renorm | REFUTED | F_k(k-2,p) renormalizes onto a deepest-layer F_{k'}(k'-1,u) | docs/theory/cubic_intermediate_layer.md | | test_cubic_layer |
| BTA-x3-vis | EXACT — LEAN VERIFIED | at m=k-1-r, N2 equality iff p≡q (mod 3^r) whenever r+1≤k | docs/theory/cubic_deficit_two.md | BTCalculus/CubicDeficitTwo depthDeficit_n2_visibility | test_cubic_deficit_two |
| BTA-x3-def2-N | EXACT — LEAN VERIFIED | m=k-3: N3=0 (k≥5), N2≡2·3^{k-2}p (k≥5), N1≡3p^2+3^{k-2}p (k≥6) | docs/theory/cubic_deficit_two.md | deficitTwo_n2_mod | test_cubic_deficit_two |
| BTA-x3-def2-crit | EXACT — LEAN VERIFIED | m=k-3 fibres iff p≡q (mod 9) and 3^{k-1}|(p-q)(p+q+3^{k-3}) and N0 agrees | docs/theory/cubic_deficit_two.md | deficitTwo_equiv_iff | test_cubic_deficit_two |
| BTA-x3-def2-n21n0 | REFUTED | at m=k-3, N2+N1 imply N0 | docs/theory/cubic_deficit_two.md | | test_cubic_deficit_two |
| BTA-x3-def2-nextdigit | REFUTED | after N2 shows p mod 9, N1 reveals the next trit | docs/theory/cubic_deficit_two.md | | test_cubic_deficit_two |
| BTA-x3-n1-diff | EXACT — LEAN VERIFIED | after N2, N1 agrees iff 3^{k-1-r} | δ(p+q+3^m) | docs/theory/cubic_n1_valuation.md | BTCalculus/CubicN1Valuation n1_after_n2_iff | test_cubic_n1_valuation |
| BTA-x3-n1-val | EXACT — LEAN VERIFIED | after N2, v3(p)<r and N1 agree imply p=q on P_m (r≥1, r+1≤k) | docs/theory/cubic_n1_valuation.md | n1_val_lt_injective | test_cubic_n1_valuation |
| BTA-x3-n1-unit | EXACT — LEAN VERIFIED | N2+N1 is injective on units of P_m for every r≥1 | docs/theory/cubic_n1_valuation.md | n1_unit_injective | test_cubic_n1_valuation |
| BTA-x3-n1-fibre | EXACT — LEAN VERIFIED | every nontrivial N2+N1 fibre on P_m lies in 3^r Z | docs/theory/cubic_n1_valuation.md | n21_fibre_in_pow | test_cubic_n1_valuation |
| BTA-x3-n1-sign | EXACT — LEAN VERIFIED | p ~ -p after N2+N1 iff 3^r | p | docs/theory/cubic_n1_valuation.md | n21_sign_iff | test_cubic_n1_valuation |
| BTA-x3-n1-scale | EXACT — LEAN VERIFIED | on p=3^r u, N1 reduces to deepest N1 at horizon k-2r when k≥2r+2 | docs/theory/cubic_n1_valuation.md | n1_high_val_scaled | test_cubic_n1_valuation |
| BTA-x3-n0-scale | EXACT — LEAN VERIFIED | D^m((3^r u)^3) is 3^{3r-m} u^3 if m≤3r, else D^{m-3r}(u^3) | docs/theory/cubic_n0_reduction.md | n0_scaled_of_le, n0_scaled_of_ge | test_cubic_n0_reduction |
| BTA-x3-n0-sign | EXACT — LEAN VERIFIED | N0(p)≡N0(-p) iff 3^k | N0(p) | docs/theory/cubic_n0_reduction.md | n0_sign_survives | test_cubic_n0_reduction |
| BTA-x3-n0-vis | EXACT — LEAN VERIFIED | D^t(u^3) mod 3^k is determined by u mod 3^{max(1,t+k-1)} | docs/theory/cubic_n0_reduction.md | n0_visible_mod | test_cubic_n0_reduction |
| BTA-x3-n0-recur | REFUTED | stripped N0 is a standard residual at the N1 horizon k-2r | docs/theory/cubic_n0_reduction.md | n0_depth_eq_n1_deepest | test_cubic_n0_reduction |
