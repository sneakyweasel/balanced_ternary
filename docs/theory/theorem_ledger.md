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
