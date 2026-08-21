# Balanced Ternary Prime Language Explorer

Research prototype for studying prime numbers in **balanced ternary**
(`-` / `0` / `+`). This is **not** a primality-testing library and does not
replace modern primality tests.

A second, separate research module studies the **accelerated Collatz map**
in balanced ternary and finite 2-adic arithmetic. It does **not** claim
progress on the Collatz conjecture and does not treat finite checks as
proofs.

**Prime core: Milestone A** — canonical encode/decode, digit statistics,
verified arithmetic invariants, a modular residue automaton, and a CLI.

**Collatz module: Milestone 5** — exact affine itineraries, minimum
realizers \(R_m\), lift coefficients \(J_m\), deterministic zero-lift
successors, and periodic-itinerary compatibility. Lyapunov search is not
included.

## Installation

Python 3.11 or newer. From this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## CLI

```powershell
btprime encode 42
btprime decode "+-0+"
btprime analyze 42
btprime residue "+-0+" --mod 7
btprime test-invariants --limit 100000

btprime collatz analyze 27
btprime collatz trajectory 27
btprime collatz inverse 1 --depth 5 --k-max 20
btprime collatz test-invariants --limit 100000
btprime collatz automaton --precision 8
btprime collatz theorems 27
btprime collatz odd-part 82
btprime collatz transducer --k 3 --limit 5000
btprime collatz valuation-shift --precision 12 --k-max 6 --length 5
btprime collatz joint --limit 500 --k-max 8
btprime collatz cylinder --ks 1,2,1
btprime collatz entropy --ks 1 --length 6
btprime collatz complexity --k-max 6
btprime collatz symbolic-graph --max-length 4 --k-max 5
btprime collatz itinerary 1,1,2,3
btprime collatz realizer 1,1,2,3
btprime collatz enumerate-itineraries --length 4 --max-k 3
btprime collatz fixed-budget --length 5 --sum-k 8
btprime collatz permutations 1,1,2,3
btprime collatz exceptional-search --length 6 --max-k 2 --epsilon 0.1
btprime collatz zero-lift --ks 1,2 --steps 8
btprime collatz periodic-itinerary 2
btprime collatz zero-lift-census --max-length 4 --max-k 4 --precision 4
```

`analyze` always prints `encode(n)`; it does not hard-code example words.
Collatz commands use the accelerated odd-only map
\(T(n)=(3n+1)/2^{v_2(3n+1)}\) on positive odd integers.

## Tests

```powershell
pytest
```

The suite includes an exhaustive round-trip, parity, and \(v_3\) check on
\([-10^6, 10^6]\). That loop is the slowest test (typically tens of seconds).

## Research UI

Interactive explorer (Streamlit). Optional extra:

```powershell
python -m pip install -e ".[ui]"
btprime collatz ui
```

Views: number explorer, trajectory, inverse tree, 2-adic automaton,
odd-part transducer, valuation prefixes, joint graph, valuation languages.
Mathematical clarity over decoration. Feature deltas are not Lyapunov
decreases; finite graphs are samples.

## Layout

```text
src/balanced_ternary/   representation, features, invariants, CLI
src/automata/           ModularAutomaton(q)
src/collatz/            accelerated Collatz research module (Milestones 1–5)
src/sieve/              stub (Phase 3+)
src/research/           stub (Phase 6+)
src/visualization/      Streamlit explorer (`btprime collatz ui`)
docs/mathematics.md     theorems implemented in Milestone A
docs/collatz_mathematics.md
docs/collatz_research_questions.md
docs/collatz_itinerary_compatibility.md
docs/collatz_zero_lift.md
```

The Collatz package reuses `balanced_ternary` and `ModularAutomaton`. It
does not change the prime-language core.

## Position convention

Displayed words are **most-significant digit first**. Every mathematical
index (weight, \(v_3\), position-class sums) counts from the
**least-significant digit** \(a_0\). See [docs/mathematics.md](docs/mathematics.md).

## Collatz claim status

See [docs/collatz_mathematics.md](docs/collatz_mathematics.md). In brief:

- \(n \equiv w(\mathrm{BT}(n))\pmod{2}\) is **PROVED**; odd Collatz states
  have odd weight, and \(3n+1\) has even weight.
- `TwoAdicDigitAutomaton(K)` residues equal \(n \bmod 2^K\) (**PROVED**).
- Valuation of \(3n+1\) from a residue modulo \(2^K\) is exact only when
  \(v_2(3n+1)<K\); otherwise the label is `AT_LEAST_K`.
- \(\mathrm{BT}(3n+1)=\mathrm{BT}(n)+\) for \(n\neq 0\) (**PROVED**).
- Division by \(2^k\) is sequential LSD-first on each valuation class
  \(L_k\); unrestricted odd-part is not a single rational transduction
  (**PROVED**). Layer C drops precision to \(2^{K-k}\).
- Finite valuation cylinders are unique residue classes of density
  \(2^{-K}\) among odds (**PROVED**).
- \(T^m(n)=(3^m n+C)/2^K\) with an explicit recurrence and closed form
  for \(C\) (**PROVED**). \(R(\mathbf{k})\) is the unique residue in
  \((0,2^{K+1})\). If \(R_m\to\infty\) along an infinite itinerary, no
  finite positive integer realises that whole itinerary (**PROVED**).
- Growth budget compares \(2^{\sum k}\) to \(3^m\) exactly. Contraction is
  not a Lyapunov function.
