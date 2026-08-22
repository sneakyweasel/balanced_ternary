# Cycle literature replication

Exact scope of independent checks against 2026 cycle preprints. Claim
labels: **reproduced**, **partially reproduced**, **convention mismatch**,
**unresolved**, **counterexample found**. Preprints are not assumed true.

## Fernández–Ibáñez, \(N>2r\)

Source: arXiv:2607.24844, Theorem 8.1(2), Syracuse parity words.

Accelerated dictionary: \(N=K\), \(r=p\). Search: every primitive word
with \(1\le p\le 6\), \(1\le k_i\le 4\), and \(K>2p\).

Result: **0** exact cycles. Classification: **partially reproduced** as
**COMPUTATIONALLY VERIFIED** inside that bound. Not a global theorem.
Hidden convention: Syracuse bits, not accelerated letters.

## Fernández–Ibáñez, \(N=2r\) is the trivial cycle

Same paper, Theorem 8.1(1). In the same bound the only integral exact
periods with \(K=2p\) were \((2)^p\). Classification: **partially
reproduced** / **COMPUTATIONALLY VERIFIED**. Words such as \((1,3)\) have
\(K=2p\) and were not cycles.

## Lebel, Christoffel class never has \(D\mid C\)

Source: Zenodo 10.5281/zenodo.19070798, Theorem 1 (preprint).

Independent test: ceiling-Christoffel Syracuse words of parameters
\((K,p)\) mapped to exponent codes, contracting \(K\), \(p\le 6\).
Integral hits were only \((2)^p\), i.e. the trivial cycle and its
non-primitive repetitions. Classification: **partially reproduced** for
this Christoffel encoding. The resultant proof is **unresolved** here.
Radius-1 canals \(A_s(X)=X^s-X+1\) were **not** rebuilt; Hamming radius
is an adapter, not Lebel's object.

## De Jesus, \(3\mid N\) implies \(C\bmod 3\) is orthogonal

Source: Zenodo 10.5281/zenodo.20465930.

For \(D=2^K-3^p\), **PROVED** \(3\nmid D\). Sampled \(C\bmod 3\) on
\(p\le 4\), \(k_i\le 3\) took values \(\{1,2\}\), never \(0\), and
`three_divides_D=0`. Classification: **convention mismatch**. The
divisor-specific walk is **reproduced** as an independent exact lemma:
if \(q\mid D\) and \(q\neq 3\), then \(q\mid C\) iff
\(\sum_j 2^{K_j}3^{-j}=0\) in \(\mathbb F_q\).

## Kramer cycle searches

Finite exponent-code diagnostics. Not replicated as a cycle theorem.
Classification: **unresolved** as a uniqueness statement; **reproduced**
as the shared affine constant \(B=C\).

## Ross bounded-exponent exclusion

Stated as a conjecture in that preprint. Classification: **unresolved**.
No counterexample and no proof here.

No counterexample to Collatz was found. No preprint was upgraded to a
repository theorem without an independent proof.
