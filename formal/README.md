# Collatz dual-code formalization

Lean 4.19 + Mathlib. Build from this directory:

```powershell
lake build
```

The project contains no `sorry` or `admit`.

Compiled theorem groups:

- bounded monotone natural sequences are eventually constant;
- exact lift equations imply monotonicity;
- eventual stabilization iff lift digits are eventually zero;
- boundedness iff eventual zero lift;
- mixed-radix reconstruction;
- positive-integer nested-cylinder realization iff stabilization;
- realization iff eventual zero lift;
- unique zero-lift child from the exact zero-lift law;
- direct residue and lift-digit algebra from an explicit modular inverse;
- odd-endpoint congruence modulo `2^(K+1)`, including a `ZMod` form;
- Kramer's endpoint congruence `2^K x = C` in `ZMod (3^m)`;
- affine-center start/endpoint numerators and cross-multiplied scaling;
- `M ≤ X` from the nonnegative `3^m` endpoint lift;
- the fixed-integer affine gap `G = 2^K (n - x)`, its exact recurrence,
  the periodic-code identity `n(2^K - 3^p) = C`, and `2^K ≠ 3^m` for `m ≥ 1`;
- primitive lists, expanding-period exclusion, rotation of an affine block,
  and even additive amplitude of odd states;
- exact endpoint change under refinement and signed successor drift;
- lift blocks as the mixed-radix expansion of `(R_m - 1) / 2`;
- boundedness iff the mixed-radix lift blocks are eventually zero;
- balanced-ternary digit lists: MSD evaluation, digit-sum after append-plus,
  `W(-n) = -W(n)`, `W(3^m n) = W(n)` after canonicalization, and
  `W(W(n)) = n` when the LSD is nonzero.

These are labelled **EXACT — LEAN VERIFIED**. The Python cylinder
implementation remains the executable instantiation; this Lean project
formalizes the exact abstract cylinder and lift interfaces and their
arithmetic consequences, together with the digit-list algebra of OEIS
reversal. Orbit statistics of `W` and `T` are not formalized.
