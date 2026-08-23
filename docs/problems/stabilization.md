# Local residual horizon versus global root-count bounds

## Problem

Whether the finite-horizon residual \(\Phi_r\) gives a sharper or more
adaptive stabilization bound for \(f(x)\equiv 0\pmod{3^k}\) than the
known global threshold on \(N_k(f)\).

## Exact statement

Let \(N_k(f)=\#\{x\bmod 3^k:f(x)\equiv 0\}\). Dwivedi–Saxena 2020 give a
closed form for \(N_k(f)\) once \(k\ge k_0:=d(\Delta+1)+1\), where
\(\Delta=v_p(D(\mathrm{rad}(f)))\). The laboratory has a local object
\(\Phi_r(\mathfrak{D}_w f)\) that determines the next \(r\) lifting
levels at a node. Question: does that local object improve \(k_0\), or
predict the same stabilization earlier?

## Current literature

Verified from the papers, not from dossier wording. Full quotations and
the A–E classification:
[docs/theory/local_vs_global_stabilization.md](../theory/local_vs_global_stabilization.md).

| claim | novelty |
|---|---|
| \(k_0=d(\Delta+1)+1\) is a closed form for the *global* \(N_k(f)\); constancy only if \(D(f)\ne 0\) | `KNOWN` (`dwivedi-saxena-2020-igusa-univariate`) |
| worst-case envelope \(O(d^2(\log C+\log d))\) is the Sylvester bound on \(\Delta\) | `KNOWN` (same) |
| unique lift of a simple root; strong Hensel \(v(f)>2v(f')\) | `KNOWN` |
| per-root contribution \(p^{k-\lceil(k-\nu_i)/e_i\rceil}\) after separation | `KNOWN` (same, Thm 19) |
| tree of lifts / tree of ideals / poly-time counting | `KNOWN` (Zúñiga-Galindo 2003; Cheng–Gao–Rojas–Wan 2019; Dwivedi–Mittal–Saxena 2019) |
| \(\Phi_r\) determines the next \(r\) levels | `REPARAMETERIZATION` of the Taylor jet (`BTL-phi-determinacy`) |

`extended` / `independent`: none. `refuted`: the novelty hypothesis that
\(\Phi_r\) is a sharper \(k_0\).

## Branch budget

```text
Mathematical target     does Phi_r improve the global k0, or predict
                        N_k-stabilization earlier / more adaptively?
Novelty hypothesis      a local residual/Newton state could certify
                        global count-stability before d(Delta+1)
Falsifier               every precise reading is already Hensel,
                        Newton-polygon, or Dwivedi–Saxena 2020
Existing machinery      LiftNode, level_counts, Phi_r, the closed
                        lifting-state theory
Maximum Phase-0 scope   literature gate; one mixed-cluster witness;
                        no CLI, UI, or Lean
Promotion criterion     a bound or certificate that is not k0, not
                        Hensel, and not the 2019/2020 algorithms
Stop criterion          literature already has the local and the
                        global objects, and they answer different
                        questions
```

## Balanced-ternary formulation

A level-\(k\) root is a trit word \(w\) with every residual output zero.
\(\Phi_r(\mathfrak{D}_w f)\) is the \(r\)-jet at that node. \(N_k(f)\) is
the number of such words of length \(k\).

## Why BT may be relevant

Only as a reading of objects the laboratory already has. The
identification of the lifting tree with the residual machine is itself a
reparameterization and is not reused here as a source of novelty.

## Candidate operations / invariants

- \(\Phi_r\) at a node — `REPARAMETERIZATION` of the Taylor jet.
- first level at which a given node has unit derivative — `KNOWN` (Hensel).
- \(\Delta=v_3(D(\mathrm{rad}(f)))\) — `KNOWN` (Dwivedi–Saxena).
- \(N_k(f)\) — `KNOWN`.

## Experiments

`research.stabilization.triage.witness_mixed_clusters`: the polynomial
\((x-1)(x^2-9)\). Residue \(1\) is Hensel-unique from level 1; residue
\(0\) is the singular \(\pm 3\) cluster; \(N_k\) is not constant from
level 1. That is the expected multi-cluster picture, not a new bound.

## Conjectures

None. Nothing was open.

## Counterexamples

Novelty hypothesis, not a mathematical statement: \(\Phi_r\) as a
sharper \(k_0\). Witness above.

## Formalization

None. No `sorry`. Lean is not opened on a closed literature gate.

## Results

- \(k_0\) is a closed form for \(N_k(f)\), not a per-branch lift bound.
- Local unique lift is Hensel / strong Hensel, already adaptive.
- \(\Phi_r\) is the Taylor jet.
- A node can be locally unique forever while \(N_k\) is still moving.

## Open questions

None on this line.

## Decision

`CLOSE`. Every precise reading is `KNOWN` or `REPARAMETERIZATION`. The
lifting-state line stays closed and is not reopened.

Best next question: none here. Pick a problem whose statements are not
already in Hensel / Newton-polygon / Igusa / Dwivedi–Saxena.

## Publication assessment

Status: `ARCHIVED`.

Not a `PAPER_CANDIDATE`. The comparison is a literature clarification.
