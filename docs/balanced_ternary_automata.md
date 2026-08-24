# Finite-state maps on balanced ternary

Classification of integer maps \(f:\mathbb{Z}\to\mathbb{Z}\) (possibly
partial) according to whether \(\mathrm{BT}(f(n))\) is obtained from
\(\mathrm{BT}(n)\) by a sequential finite-state transduction. Details:
`src/bt/transducers/zoo.py`. Existing machines in
`src/research/collatz/transducers/` are reused.

## Zoo (summary)

| Function | Finite-state? | Type | States | Status |
| --- | --- | --- | --- | --- |
| \(S(n)=3n\) | yes | append LSD 0 | 1 | PROVED |
| \(N(n)=-n\) | yes | letter-to-letter | 1 | PROVED |
| \(D\), \(D^k\) (\(k\) fixed) | yes | drop \(k\) LSDs | 1 | PROVED |
| \(H_3\) on \(3\mathbb{Z}\) | yes | \(D\) on \(a_0=0\) | 1 | PROVED |
| \(I_{\pm}(n)=3n\pm 1\) | yes | append LSD \(\pm\) | 1 | PROVED |
| \(K_3=n/3^{v_3(n)}\) | yes | skip trailing zeros | 2 | PROVED |
| \(M_2=2n\) | yes | LSD Mealy | 3 | PROVED |
| \(H_2\) on \(2\mathbb{Z}\) | yes | LSD Mealy | 3 | PROVED |
| \(M_2^k\), \(H_2^k\) | yes | product of \(k\) copies | see below | existence PROVED; sizes computational |
| \(W,W_z,W_t\) | no (one-way sequential) | global reverse | — | PROVED obstruction |
| odd-part \(n/2^{v_2(n)}\) | no | not one rational transduction | — | PROVED (existing argument) |
| Collatz \(T\) | no | \(3n+1\) FST then unrestricted odd-part | — | PROVED as a composition |

Reversal is not a one-way sequential function: the transducer would have to
buffer an unbounded prefix before seeing the MSD. No claim is made about
two-way machines. Unrestricted odd-part remains the project's example of a
natural arithmetic map that is a countable union of finite-state branches
but not one rational transduction.

The contrast between \(K_3\) and odd-part is exact: \(v_3\) is the number of
trailing zeros of \(\mathrm{BT}(n)\), hence locally readable LSD-first;
\(v_2\) is not a bounded-state function of balanced-ternary digits.

## State complexity of \(M_2^k\) and \(H_2^k\)

Naive product bound \(3^k\). Reachable and (for \(H_2^k\)) minimized sizes
are **VERIFIED COMPUTATIONALLY** by BFS / Mealy partition refinement. They
are not theorems. CLI:

```powershell
btlab operators states --max-k 6
btlab operators zoo
```

If a prefix equals \(3^k\), that is OEIS A000244 (the bound), not a new
sequence. Strict inequality for some \(k\) is reported as a computation,
not as a closed form.

## Compositions with reverse

\(W\circ D^k\) and \(D\circ W\) still require both ends of the word.
Composing a non-sequential map with a sequential one does not restore
one-way finite-state structure.

## Operator complexity (honest boundary)

No exact formula for \(\lvert\mathrm{states}(M_2^k)\rvert\) is claimed.
Transition entropy of the 3-state doubling machine is a finite-alphabet
Mealy quantity and is not developed into a theorem here.
