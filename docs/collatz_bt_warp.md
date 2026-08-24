# Balanced-ternary word maps and accelerated Collatz

This note records Milestone 9. Claim labels are **PROVED**, **VERIFIED
COMPUTATIONALLY**, **CONJECTURE**, and **OBSERVATION**. Finite checks are
not theorems. Nothing here is a Collatz proof.

The objects are OEIS-style transformations of canonical balanced-ternary
words, composed with the accelerated odd-only map

\[
T(n)=\frac{3n+1}{2^{v_2(3n+1)}}
\]

defined only on positive odd integers. Strong BT-independence of the
canonical realizer \(R\) was already **REFUTED**. The question here is
whether a *permutation of BT words* interacts with \(T\).

## Maps

All maps reuse the existing encoder. Display is MSD-first with alphabet
`+/-/0`. The LSD is \(a_0\).

- \(W\): OEIS [A134028](https://oeis.org/A134028). Reverse the canonical
  word, then decode (leading zeros after reverse are stripped).
- \(W_z\): OEIS [A160652](https://oeis.org/A160652). Reverse leaving
  trailing zeros. \(W_z(n)=W(n)\,3^{v_3(n)}\) for \(n\neq 0\).
- \(W_{\mathrm{tail}}\): OEIS [A351702](https://oeis.org/A351702). Reverse
  every digit except the MSD. \(W_{\mathrm{tail}}(-n)=-W_{\mathrm{tail}}(n)\).
- Palindromes: OEIS [A134027](https://oeis.org/A134027), the canonical word
  equals its reverse.
- \(s_3\): OEIS [A065363](https://oeis.org/A065363), signed digit sum.
- Alternating sum: OEIS [A065364](https://oeis.org/A065364),
  \(\sum_i a_i(-1)^i\).
- \(L_3\): OEIS [A134021](https://oeis.org/A134021), canonical length.

Published prefixes are locked in `tests/unit/test_oeis_maps.py`. They are not
invented examples.

## Exact word algebra

**PROVED** (and Lean-verified at the digit-list level):

1. Digitwise negation reverses evaluation, and reverse commutes with
   negation, so \(W(-n)=-W(n)\) and \(W(0)=0\).
2. Appending LSD \(+1\) realises \(3n+1\) for a nonzero word:
   \(s_3(3n+1)=s_3(n)+1\) and \(L_3(3n+1)=L_3(n)+1\) when \(n\neq 0\).
   This is the Layer A append-plus theorem.
3. Appending \(m\) trailing zeros multiplies the value by \(3^m\) and
   does not change \(W\) after canonicalization: \(W(3^m n)=W(n)\).
4. If the LSD is nonzero, reverse has no leading zero, so
   \(W(W(n))=n\). Equivalently, for integers,
   \(W(W(n))=n\) if and only if \(n=0\) or \(3\nmid n\).

**PROVED**, not involutive: \(W\) is A134028, not A160652. Trailing zeros
become leading zeros after reverse and are stripped. The smallest
positive witness is \(W(3)=1\), \(W(W(3))=1\neq 3\). \(W_z\) and
\(W_{\mathrm{tail}}\) are involutions on \(\mathbb{Z}\).

**REFUTED EXACTLY:** \(W(3n)=3W(n)\). Witness \(n=1\): \(W(3)=1\neq 3\).

**PROVED:** for odd \(n\), weight is odd and reverse preserves weight, so
\(W(n)\) is odd. For \(3\nmid n\), the LSD is the sign of \(W(n)\):
\(n\equiv 1\pmod 3\) implies \(W(n)>0\), and \(n\equiv -1\pmod 3\) implies
\(W(n)<0\). Therefore \(T(W(n))\) is defined, for odd \(n\) not divisible
by 3, if and only if \(n\equiv 1\pmod 3\). Positive integers whose LSD is
`-` have \(W(n)<0\), so \(T(W(n))\) is undefined.

The 2-adic valuation \(k=v_2(3n+1)\) is not a function of \(W(n)\). Reverse
exchanges LSD and MSD; it does not predict \(k\).

## Commutator with \(T\)

\[
\mathrm{Comm}_{WT}(n)=W(T(n))-T(W(n))
\]

is defined only when \(n\) is positive odd and \(W(n)\) is positive odd.
No signed extension of \(T\) is used.

**REFUTED EXACTLY** on that domain: \(W\circ T=T\circ W\). Smallest
witness \(n=3\): \(W(3)=1\), \(T(3)=5\), \(W(5)=-11\), \(T(1)=1\), so
\(\mathrm{Comm}_{WT}(3)=-12\).

On odd \(n\le 20000\) (**VERIFIED COMPUTATIONALLY**):

- the commutator is defined for 5004 of 10000 odds (density \(0.5004\)),
  matching the exact count of odd \(n\equiv 1\pmod 3\) plus four
  multiples of 3 with positive \(W(n)\);
- \(\mathrm{Comm}_{WT}(n)=0\) for exactly four values:
  \(1,121,5461,9841\), all palindromes;
- palindromes need not commute: \(n=7\) has \(W(7)=7\) and
  \(\mathrm{Comm}_{WT}(7)=-16\);
- \(\Delta_L=L_3(T(n))-L_3(n)\) ranged in \(\{-8,\ldots,1\}\). This is an
  integer length change from append-plus followed by odd-part, not an
  identity \(\log_3 2\).

On every positive odd \(n\le 10^6\), \(\Delta_s(n)=s_3(T(n))-s_3(n)-1\)
equals \(s_3(T(n))-s_3(3n+1)\), so it measures only the odd-part step
(**VERIFIED COMPUTATIONALLY**; the identity \(s_3(3n+1)=s_3(n)+1\) is
**PROVED**). Zero commutators in that range were palindromes
(**VERIFIED COMPUTATIONALLY**, not a theorem).

## Special classes and palindromes

No named class — palindromes, fixed length, sparse words, A351702 fixed
points, trailing-digit families — forces commutation with \(T\). Length-1
is the singleton \(\{1\}\) on positive odds. Trailing `-` never enters the
commutator domain, by the sign lemma above.

Along ordinary \(T\)-orbits, palindromes appear as an **OBSERVATION**
(for example four palindromes on the truncated orbit of 27). This is not
a statement about A224502 primes.

## Canonical realizers

For a valuation word \(\mathbf{k}\), compare \(W(R(\mathbf{k}))\) with
\(R(\mathrm{reverse}(\mathbf{k}))\) and \(R(\mathrm{tail\text{-}reverse}(\mathbf{k}))\).
Both candidate identities fail already at \(\mathbf{k}=(1)\):
\(R((1))=3\) and \(W(3)=1\neq 3\). Bounded censuses preserve these
counterexamples. Reverse of a BT word is not reverse of an exponent code.

## Composition semigroup

On generator words in \(\{T,W,W_{\mathrm{tail}}\}\) of length at most 6,
with \(T\) undefined off positive odds:

- \(W_{\mathrm{tail}}W_{\mathrm{tail}}=\mathrm{id}\) holds on the scanned
  integers (**PROVED** as an involution; the scan is a check);
- \(WW=\mathrm{id}\) fails at \(n=3\);
- \(WT=TW\) fails at \(n=3\);
- \(W_{\mathrm{tail}}T=TW_{\mathrm{tail}}\) fails at \(n=7\).

Sample agreement of longer words is **VERIFIED COMPUTATIONALLY** only.

## Classification

**A. Exact new theorems.** Involution criterion for \(W\); sign of \(W(n)\)
from the LSD; \(W(3^m n)=W(n)\); \(W(-n)=-W(n)\); domain of \(T\circ W\)
for odd \(n\) not divisible by 3; \(\Delta_s\) isolates the odd-part step.

**B. Known OEIS structure reproduced.** A134028, A160652, A351702, A065363,
A065364, A134021, A134027.

**C. Computational observations.** Extreme rarity of \(\mathrm{Comm}_{WT}=0\);
the four zeros through \(20000\) are palindromes; \(\Delta_L\) range;
palindromes on named \(T\)-orbits.

**D. Refuted hypotheses.** \(W\) involutive on all of \(\mathbb{Z}\);
\(W(3n)=3W(n)\); \(W\circ T=T\circ W\); \(W(R(\mathbf{k}))=R(f(\mathbf{k}))\)
for reverse or tail-reverse of the valuation word.

**E. Open questions.** Is \(\{n:\mathrm{Comm}_{WT}(n)=0\}\) exactly the
positive odd palindromes \(p\) with \(W(T(p))=T(p)\)? The inclusion one way
is tautological for palindromes; the converse is only computationally
supported. No relation constraining near-critical exponent codes was found.

## Q1–Q7

1. Reversal interacts with \(T\) only through a sparse, domain-restricted
   commutator. The interaction is real and exactly describable, but it is
   not a hidden Collatz coordinate.
2. The only meaningful exact commutation class found is the trivial
   length-1 point \(\{1\}\). Palindromes do not commute in general.
3. Palindrome class \(P_{BT}\) is closed under \(W\) and is a thin subset
   of odds. Its \(T\)-behaviour is an observation, not a descent law.
4. Digit sums add no Collatz transition beyond append-plus:
   \(s_3(3n+1)=s_3(n)+1\) was already known. \(\Delta_s\) is the odd-part
   remainder.
5. \(W(R(\mathbf{k}))\) does not equal \(R\) of the reversed or
   tail-reversed itinerary.
6. No constraint on near-critical exponent codes was obtained.
7. The exact statements are genuine (involution criterion, sign/domain
   lemmas, OEIS identifications). They are a permutation of BT words, not
   a new arithmetic coordinate for Collatz.

## Assessment

The direction is **computationally interesting** and records several
exact word-level theorems. It is not a Collatz obstruction and is not
claimed as publishable Collatz progress. Novelty relative to the
2-adic / 3-adic / rational-base \(3/2\) literature is the OEIS reversal
layer; no exact relation identifying \(W\) with those coordinates was
found.

## Commands

```powershell
btlab reverse 21
btlab reverse-tail 224
btlab collatz warp 27
btlab collatz warp-census --limit 20000
btlab collatz warp-realizer 1,4,2
btlab collatz warp-semigroup --length 6
btlab collatz warp-counterexamples
```

Lean statements live in `formal/Representation/Words.lean`. Experiment rows
use schema `collatz-bt-warp/v1`.
