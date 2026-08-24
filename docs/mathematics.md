# Balanced-ternary mathematics

Units of the representation are ordinary integers. Balanced ternary is a
numeral system, not a change of physical units.

All identities below are implemented as executable tests. Claims not proved
here are not stated as theorems.

## Representation

Every integer \(n\) has a unique expansion

\[
n=\sum_{i=0}^{k-1}a_i3^i,\qquad a_i\in\{-1,0,+1\},
\]

with no leading zeros except for \(n=0\), whose word is `0`. The display
alphabet is `-` \(= -1\), `0` \(= 0\), `+` \(= +1\), written
**most-significant digit first**.

Positive integers have leading `+`. Negative integers have leading `-`,
equal to digitwise negation of the encoding of \(|n|\).

### Position convention (LSD)

Internally, **mathematical positions are indexed from the least-significant
digit**:

\[
a_0,a_1,a_2,\ldots
\]

so \(a_0\) is the **last** character of the displayed word. Position-class
sums \(S_j^{(t)}=\sum_{i\equiv j\pmod t}a_i\) use this indexing.

Encode uses only integer remainder and division. Remainder `2` is rewritten
as digit \(-1\) with carry \(+1\), because \(2=3-1\).

## Invariant 1 — uniqueness / round trip

**Status: proved theorem** (standard balanced ternary; verified exhaustively
on \([-10^6,10^6]\)).

\[
\operatorname{decode}(\operatorname{encode}(n))=n.
\]

`normalize` strips leading zeros and is a left inverse of display: the
canonical word is unique.

## Invariant 2 — parity of weight

**Status: proved theorem.**

Let \(w(n)=\sum_i|a_i|\). Since \(3^i\equiv 1\pmod 2\) and
\(-1\equiv 1\pmod 2\),

\[
n=\sum_i a_i3^i\equiv\sum_i|a_i|\equiv w(n)\pmod 2.
\]

Hence \(n\) is odd if and only if \(w(n)\) is odd. In particular every
prime \(p>2\) has odd weight.

## Invariant 3 — \(3\)-adic valuation

**Status: proved theorem.**

The least-significant nonzero digit sits at index \(v_3(n)\):

\[
v_3(n)=\min\{i:a_i\neq 0\}
\]

for \(n\neq 0\). For \(n=0\) we take \(v_3(0)=\infty\) (returned as
`None` in code). Consequently a prime \(p\neq 3\) cannot end with digit
`0`.

## Invariant 4 — modular recurrence

**Status: proved theorem.**

Reading digits most-significant to least-significant, if the current prefix
has residue \(r\pmod q\), appending digit \(a\) yields

\[
r'\equiv 3r+a\pmod q.
\]

This is exactly Horner's rule for the polynomial \(\sum a_i3^i\). The
automaton `ModularAutomaton(q)` implements it, so

\[
\texttt{automaton\_residue}(w,q)=\operatorname{decode}(w)\bmod q
\]

for every word and every modulus \(q\ge 2\) (including \(q=3\), where the
transition collapses to \(r'\equiv a\pmod 3\)).

Python's remainder for negative integers is in \(\{0,\ldots,q-1\}\), matching
the automaton states.

## Out of scope for this note

Finite sieve languages \(\mathcal S_B\), forbidden patterns, growth rates
\(\lambda_B\), and statistical metric comparisons are **not** implemented
here and must not be described as theorems until proved or
refuted with an explicit counterexample search.

## Operator algebra

The first-class maps \(S,N,D,W\) and their compositions are recorded in
[balanced_ternary_operators.md](balanced_ternary_operators.md) and
[operator_algebra.md](operator_algebra.md). The digit derivative identity
\(n=a_0+3D(n)\) is the LSD form of uniqueness. Collatz is an application
of this algebra, not a source of operator identities.
