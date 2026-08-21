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
- direct residue and lift-digit algebra from an explicit modular inverse.

These are labelled **EXACT — LEAN VERIFIED**. The Python cylinder
implementation remains the executable instantiation; this Lean project
formalizes the exact abstract cylinder and lift interfaces and their
arithmetic consequences.
