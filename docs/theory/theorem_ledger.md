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
| BTA-x2-raw | EXACT — HUMAN PROOF | R_k(x^2)=(3^k-1)/2 | docs/theory/residual_state_complexity.md | | test_myhill_nerode |
| BTA-x2-mn | CONJECTURE | M_k(x^2)=R_k(x^2) for all k (verified k≤7) | docs/theory/residual_state_complexity.md | BTCalculus/MyhillNerode x_sq_not_equiv_one_three | test_myhill_nerode |
| BTA-sample | REFUTED | sample LSD min = M_k; witness x^2 k=3 (7 vs 13) | docs/theory/residual_state_complexity.md | | test_myhill_nerode |
| BTA-cascade | EXACT — LEAN VERIFIED | outputAlong(w,f∘g)=outputAlong(outputAlong(w,g),f) | docs/theory/residual_state_complexity.md | BTCalculus/TransducerComposition | test_myhill_nerode |
| BTA-product | EXACT — HUMAN PROOF | M_k(f∘g)≤M_k(f)M_k(g) | docs/theory/residual_state_complexity.md | | test_myhill_nerode |
| BTA-locality-small | REFUTED | prefix locality ⇒ small automaton | docs/theory/residual_state_complexity.md | | test_myhill_nerode |
| BTA-hatD-B | EXACT — HUMAN PROOF | bounded-B hat D is N_B then drop; not FST on Z | docs/theory/residual_state_complexity.md | | test_myhill_nerode |
