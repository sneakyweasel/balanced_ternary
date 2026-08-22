# Balanced ternary and Collatz research

An exact-arithmetic research platform with two connected components:

- canonical balanced-ternary representation, arithmetic, features, invariants,
  and modular residue automata;
- the accelerated odd-only Collatz map studied through exponent codes,
  2-adic cylinders, lift digits, 3-adic endpoints, balanced ternary, and
  affine-center geometry.

This is not a primality-testing library and does not claim a proof or
disproof of the Collatz conjecture. Claims are labelled **PROVED**,
**VERIFIED COMPUTATIONALLY**, **CONJECTURE**, or **OBSERVATION**. Finite
checks are never presented as proofs.

## Current research surface

For a finite valuation code \(\mathbf{k}=(k_0,\ldots,k_{m-1})\), the
project computes

\[
T^m(n)=\frac{3^m n+C}{2^K},\qquad K=\sum_i k_i,
\]

together with:

- the refined 2-adic start representative \(R\);
- Kramer's 2-adic representative \(r\) and 3-adic endpoint representative
  \(M\);
- the canonical endpoint \(X=T^m(R)\);
- the balanced-ternary word \(\operatorname{BT}(R)\);
- mixed-radix lift digits \(t_i\);
- exact drift \(3^m/2^K\);
- the affine center \(n_*=C/(2^K-3^m)\) and centered inequalities;
- OEIS balanced-ternary word maps, especially reversal \(W\), composed
  with \(T\) on an explicit domain.

Balanced ternary is tested as a representation of \(R\), not asserted to be
an independent arithmetic coordinate. The current exact result is that
\(\operatorname{BT}(R)\) is determined by \(R\); lossy balanced-ternary
features can still be useful observables.

## Quick start

Python 3.11 or newer:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,ui]"
pytest
```

The slowest Python test exhaustively checks balanced-ternary identities on
\([-10^6,10^6]\).

## Representative CLI workflows

The stable command is `btprime`. Use `--help` on either command group for
the complete research surface.

```powershell
# Balanced ternary
btprime encode 42
btprime analyze 42
btprime residue "+-0+" --mod 7

# Accelerated Collatz dynamics
btprime collatz analyze 27
btprime collatz trajectory 27
btprime collatz inverse 1 --depth 5 --k-max 20

# Exponent codes and exact geometry
btprime collatz dual-code 1,4,2
btprime collatz compatibility 1,4,2
btprime collatz affine-center 1,4,2
btprime reverse 21
btprime collatz warp 27
btprime collatz warp-census --limit 20000

# Bounded experiments
btprime collatz information-test --max-length 4 --max-k 4
btprime collatz near-critical --max-length 4 --max-k 4 --seed 17
btprime collatz affine-center-census --max-length 6 --max-k 4 --critical-gap 10
```

Collatz commands use
\(T(n)=(3n+1)/2^{v_2(3n+1)}\) on positive odd integers.

## Python API

The package roots expose commonly used exact objects:

```python
from balanced_ternary import decode, encode
from collatz import AffineCenterState, CompatibilityState, collatz_step

word = encode(42)
assert decode(word) == 42

state = CompatibilityState.from_valuations((1, 4, 2))
center = AffineCenterState.from_valuations((1, 4, 2))
assert state.R == center.R
```

The root imports are the supported convenience façade. Experiment runners,
schemas, and specialized automata remain research APIs in their submodules.

## Research UI

Install the optional UI dependencies and launch the Streamlit explorer:

```powershell
python -m pip install -e ".[ui]"
btprime collatz ui
```

The UI covers integer dynamics, finite-state models, exponent-code
compatibility, lift coding, affine-center geometry, and BT word maps. Expensive bounded
searches run only after explicit submission and are labelled as computational
experiments.

## Reproducible experiments

Experiment runners use exact integer/rational records and versioned manifests
where supported. Generated JSONL, Parquet, CSV, and report artifacts live
under `experiments/` and are intentionally ignored by Git.

For example:

```powershell
btprime collatz affine-center-census `
  --max-length 6 --max-k 4 --critical-gap 10 `
  --output-dir experiments/collatz/raw/affine-center
```

Parquet output is optional; JSONL plus a manifest is the portable baseline.

## Formal verification

Lean 4 + Mathlib proofs live under `formal/`.

```powershell
cd formal
lake build
```

The formal layer includes the affine exponent-code formula, cylinders,
lift/stabilization statements, 3-adic endpoint congruences, and affine-center
numerator identities. See [formal/README.md](formal/README.md).

## Repository layout

```text
src/balanced_ternary/       canonical representation, arithmetic, features
src/automata/               shared modular residue automaton
src/collatz/
  automata/                 2-adic and symbolic finite-state models
  languages/                cylinder languages and DFA minimization
  transducers/              division and odd-part transducers
  experiments/              reproducible bounded computations
  research/                 executable Collatz invariant checks
src/visualization/          Streamlit research explorer
tests/                      balanced-ternary, Collatz, CLI, and UI tests
docs/                       mathematics, milestones, literature, open questions
formal/                     Lean 4 formalization
experiments/                ignored generated artifacts
```

## Documentation

Start with [docs/README.md](docs/README.md). The main records are:

- [Collatz mathematics](docs/collatz_mathematics.md)
- [Research questions and claim status](docs/collatz_research_questions.md)
- [Dual coding and lift digits](docs/collatz_dual_coding.md)
- [Four-coordinate literature comparison](docs/literature_comparison.md)
- [Affine-center geometry](docs/collatz_affine_center.md)
- [BT word maps and Collatz commutators](docs/collatz_bt_warp.md)

Displayed balanced-ternary words are most-significant digit first.
Mathematical positions are indexed from the least-significant digit \(a_0\).
