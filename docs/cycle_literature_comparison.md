# Cycle literature comparison

This note places Milestone 11 against recent cycle / symbolic-language
papers. A theorem in a cited work is that paper's theorem unless its
proof has been checked here. 2026 preprints are treated as **preprints**.

## Shared affine equation

For an accelerated period of length \(p\) with total valuation \(K\) and
affine constant \(C\), a positive cycle requires

\[
n(2^K-3^p)=C,\qquad 2^K>3^p.
\]

This identity is already in the repository (Milestone 5 / 10) and in
Kramer's exponent-code formula with \(B_m=C\). It is not claimed as new.

## Kramer (2026)

Oliver Kramer,
[Adaptive Search in Collatz Exponent-Code Space via 2-adic and 3-adic Constraints](https://arxiv.org/abs/2607.10041),
preprint.

Uses the same affine constant and 2-adic / 3-adic representatives. Cycle
search in that work is a finite diagnostic, not a cycle classification.
This milestone enumerates **words**, not integers, and records exact
pruning rather than floating rates.

## Fernández–Ibáñez, Christoffel maximizers (2026)

[Christoffel Words as Extremal Structures in Collatz Dynamics](https://arxiv.org/abs/2607.24844),
preprint.

They work with **Syracuse parity words** of length \(N\) with \(r\) odd
steps. Dictionary: \(N=K\), \(r=p\), each valuation \(k_i\) is a `1`
followed by \(k_i-1\) zeros. Their functional \(C(d)\) is the Terras sum
on that binary word, related to but not identical with this repository's
\(C(\mathbf{k})\).

Claimed consequences (in their paper): no cycle with \(N>2r\); the case
\(N=2r\) is only the trivial cycle. In accelerated units this is
\(K>2p\) and \(K=2p\). Those statements are **not** adopted as theorems
here. They are independently searched on exponent words; see
[cycle_literature_replication.md](cycle_literature_replication.md).

Amplitude in that paper is not \(A_{\mathrm{add}}\). They bound the
minimum cycle element. The adapter is the slope \(K/p\), not Hamming
amplitude.

## Lebel, Christoffel modular sieving (2026)

Marc Lebel,
[Christoffel words and modular sieving for accelerated Collatz itineraries](https://doi.org/10.5281/zenodo.19070798),
preprint.

Claims: the Christoffel class never satisfies the divisibility condition;
a radius-1 exclusion reduced to \(A_s(X)=X^s-X+1\) over finite fields;
canals \(s=2\) closed; primes \(5\) and \(7\) obstruct infinite families.
These are **preprint claims**. This repository reproduces only the
exponent-code image of ceiling-Christoffel Syracuse words and the
divisor-specific walk \(\sum 2^{K_j}3^{-j}\) in \(\mathbb F_q\). Radius-1
is implemented as Hamming distance to that Christoffel word, which may
not match Lebel's canal convention.

## De Jesus, modular no-go diagnostic (2026)

Elias De Jesus,
[A Modular No-Go Diagnostic for Accelerated Collatz Cycle Closure](https://doi.org/10.5281/zenodo.20465930),
preprint.

The cycle equation is the same. The note argues that a universal
\(C\bmod 3\) pin is orthogonal to closure because \(3\mid N\). For
\(N=D=2^K-3^p\) one has \(D\equiv 2^K\not\equiv 0\pmod 3\). So \(3\nmid D\).
The orthogonality hypothesis is a **convention mismatch** with this \(D\).
The useful remaining point, which we independently use, is that modular
obstructions must be divisor-specific. That matches the finite-field walk.

## Ross, spike structures (2026)

[Spike Structures and 2-adic Transition Laws in the Accelerated Collatz Map](https://zenodo.org/records/21049703),
preprint.

Records local \(k=1\) transition laws and explicitly leaves
bounded-exponent cycle exclusion as a **conjecture**. This milestone does
not upgrade that conjecture.

## What is not claimed

No paper above is treated as a peer-reviewed exclusion of nontrivial
Collatz cycles. Finite searches here do not prove Collatz.
