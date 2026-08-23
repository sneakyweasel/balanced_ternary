# Balanced Ternary Mathematical Laboratory

An exact-arithmetic **research platform**. Balanced ternary mathematics is
the core. Research problems — Collatz, sparse powers, additive
combinatorics, operator dynamics — are independent applications.

This repository does **not** claim a solution of the Collatz conjecture or
of any other open problem. Finite checks are never presented as proofs.
Claims are labelled **PROVED** (human), **PROVED — LEAN**,
**COMPUTATIONALLY VERIFIED**, **CONJECTURE**, **OBSERVATION**,
**REFUTED**, or **REPARAMETERIZATION**. See
[docs/README.md](docs/README.md) for the mapping to ledger tags.

## What balanced ternary is

Every integer has a unique canonical expansion

\[
n = \sum_i a_i 3^i,\qquad a_i \in \{-1,0,+1\}
\]

with no leading zeros (except \(n=0\)). Display uses `-`, `0`, `+`
(most-significant digit first). Mathematical positions are indexed from
the least-significant digit \(a_0\).

## Why this repository exists

To keep a **problem-independent** encoder, arithmetic, operators,
polynomials, automata, and transducers, and to attach new open problems
as modules that import `bt` but never the reverse.

## How research is done here

Each direction runs the loop **explore → distill → prove/refute →
decide**, under a written budget that fixes the target, the novelty
hypothesis, and the falsifier before implementation starts. Every branch
ends in exactly one decision — `PROMOTE`, `PARK`, or `CLOSE` — and a
closed branch stays documented so it is not rediscovered. Machinery is a
means: reusable primitives are welcome, taxonomies without a
theorem-level payoff are not.

See [docs/methodology.md](docs/methodology.md).

## Core (`bt`)

Representation, arithmetic, normalization, operators (`S`, `N`, `D`,
`W`, `M2`, `H2`, …), the trit calculus (`D`, `I_a`, `cmp3`, `select3`,
rewrite), metrics, support, polynomials \(P_n\) with
\(P_n(3)=n\), generic automata, and generic transducers.

```python
from bt import decode, encode

word = encode(42)
assert decode(word) == 42
```

The compatibility façade `from balanced_ternary import encode` remains
supported.

## Research applications (`research`)

| Module | Status |
|--------|--------|
| `research.collatz` | STRUCTURAL |
| `research.residuals` | STRUCTURAL |
| `research.lifting` | EXPLORATORY |
| `research.additive_combinatorics` | EXPLORATORY |
| `research.perfect_powers` | EXPLORATORY |
| `research.primes` | EXPLORATORY |
| `research.sparse_polynomials` | EXPLORATORY |
| `research.operator_dynamics` | EXPLORATORY |

```python
from collatz import AffineCenterState, CompatibilityState, collatz_step
```

still works; the implementation lives under `research.collatz`.

## Formal verification

Lean 4 + Mathlib under `formal/`. No `sorry` or `admit`.

```powershell
cd formal
lake build
```

See [formal/README.md](formal/README.md) and
[docs/architecture/formalization.md](docs/architecture/formalization.md).

## Current open problems and conjectures

Active / computationally supported registry entries include `N_k=2^k+1`,
low-\(K_m/m\) lift conjectures, and non-contraction compatibility.
Refuted hypotheses (including `W(3)=1` and `n_*=165` at step 17) are
kept under `conjectures/refuted/`.

```powershell
btprime conjectures list
btprime status
```

## Quick start

Python 3.11 or newer:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,ui]"
pytest
```

Optional Parquet experiment I/O: `pip install -e ".[experiments]"`.

## CLI

The command is `btprime`. Existing commands are aliases; namespaces are
also available.

```powershell
btprime encode 42
btprime bt encode 42
btprime operators apply S 42
btprime calculus eval 42
btprime collatz analyze 27
btprime status
```

Research UI (optional). The Streamlit app is centered on balanced ternary,
with a calculator, encode/analyze, operators, and the Residual explorer;
Collatz pages remain as one application:

```powershell
btprime ui
btprime collatz ui
btprime calculus explorer
```

## Tests and Lean

```powershell
pytest
pytest --runslow
cd formal
lake build
```

`pytest` skips the slow marker (k>10 residual censuses, million-range identities, Streamlit AppTests) and runs in parallel. Full suite: `pytest --runslow`. Serial: `pytest -n 0`.

## How to add a new research problem

1. Copy [docs/problems/TEMPLATE.md](docs/problems/TEMPLATE.md) to
   `docs/problems/<id>.md`.
2. Copy `src/research/template/` to `src/research/<id>/` and fill
   `problem.py`.
3. Import only `bt.*` plus shared experiment/registry utilities.
4. Register conjectures in `conjectures/` and literature in `literature/`.
5. Add tests under `tests/research/` and witnesses under `tests/regression/`.
6. Do not edit core arithmetic to introduce the problem.

Every new problem starts from a branch budget and ends in a decision:
[docs/methodology.md](docs/methodology.md).

Architecture: [docs/architecture/overview.md](docs/architecture/overview.md).
Documentation map: [docs/README.md](docs/README.md).
Journal: [docs/research_journal.md](docs/research_journal.md).
