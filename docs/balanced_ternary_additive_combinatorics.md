# Digit-restricted additive combinatorics

Sets are integers, decoded from unique balanced expansions of bounded
length. This branch is independent of Collatz.

Let \(k\ge 0\) and \(M=(3^k-1)/2\).

\[
\begin{aligned}
A_k&=\Bigl\{\sum_{i=0}^{k-1}x_i 3^i:x_i\in\{0,1\}\Bigr\},\\
B_k&=\Bigl\{\sum_{i=0}^{k-1}x_i 3^i:x_i\in\{-1,+1\}\Bigr\},\\
C_k&=\Bigl\{\sum_{i=0}^{k-1}x_i 3^i:x_i\in\{-1,0,+1\}\Bigr\}.
\end{aligned}
\]

**PROVED** (uniqueness of balanced ternary): \(C_k=[-M,M]\cap\mathbb{Z}\)
and \(\lvert C_k\rvert=3^k\). \(\lvert A_k\rvert=\lvert B_k\rvert=2^k\).

## Sumsets (PROVED)

**\(A_k+A_k\).** Digitwise sums lie in \(\{0,1,2\}\), the complete ordinary
base-3 alphabet of length \(k\). Therefore

\[
A_k+A_k=\{0,1,\ldots,3^k-1\}.
\]

It is an interval. Cardinality \(3^k\). Representation function
\(r(n)=2^{\#\{i:d_i=1\}}\) from the unbalanced ternary digits of \(n\).
Additive energy \(E(A_k)=\sum r^2=6^k\).

**Smallest \(r\) with \(rA_k\) covering an interval of length \(\ge 2\):**
\(r=2\) for \(k\ge 1\), because \(2A_k=[0,3^k-1]\). \(A_k\) itself is
lacunary for \(k\ge 2\).

**\(A_k-A_k\).** Each digit of the difference independently realises
\(\{-1,0,1\}\), so

\[
A_k-A_k=C_k=[-M,M].
\]

Yes: \(A_k-A_k\) **is an interval**. Multiplicity
\(r(n)=2^{\#\{\text{zero digits in the \(k\)-pad}\}}\). Energy \(6^k\).

**\(B_k+B_k\).** Digitwise sums lie in \(\{-2,0,2\}=2\{-1,0,1\}\), and
\(-B_k=B_k\), hence

\[
B_k+B_k=B_k-B_k=2C_k,
\]

all even integers in \([-(3^k-1),3^k-1]\). Cardinality \(3^k\). Not a
full integer interval (odds are missing).

**\(A_k+B_k\).** Digit alphabet before carry is \(\{-1,0,1,2\}\). No
closed interval theorem is claimed. Enumeration for small \(k\) is
**VERIFIED COMPUTATIONALLY**.

These identities use uniqueness as a decoding mechanism. They are
standard digitwise arithmetic, now recorded as exact theorems of the
repository rather than as numerical sumset scans.

## Sparse weight \(W_k=\{n:w(n)\le k\}\)

**PROVED.** Squares in \(W_1\): \(w(n)\le 1\) means \(n=0\) or
\(n=\pm 3^a\). The only squares are \(0\) and \(3^{2t}=(3^t)^2\).

Cubes in \(W_1\): \(0\) and \(3^{3t}\). Primes in \(W_1\): only \(3\).

For \(k=2\), integers of the form \(\varepsilon 3^a+\delta 3^b\). Squares,
cubes, and primes in this set are a computational search
(`btlab operators sparse --k 2`). A prefix of squares is an
**OBSERVATION**, not a classification.

## Carry defect and \(d_{\mathrm{BT}}\)

\[
w(n)=\#\{i:a_i\neq 0\},\qquad
d_{\mathrm{BT}}(a,b)=w(a-b),\qquad
\mathrm{carry\_defect}(a,b)=w(a)+w(b)-w(a+b).
\]

**PROVED.** \(d_{\mathrm{BT}}\) is symmetric and definite:
\(w(-n)=w(n)\), and \(w(n)=0\) iff \(n=0\).

**PROVED.** If \(a\) and \(b\) have disjoint support then addition is
carry-free and \(\mathrm{carry\_defect}(a,b)=0\).

Triangle inequality for \(d_{\mathrm{BT}}\) is equivalent to
\(\mathrm{carry\_defect}\ge 0\) identically, i.e. subadditivity of \(w\).
That is **not** assumed. On \(\lvert a\rvert,\lvert b\rvert\le 25\) the
defect is nonnegative (**VERIFIED COMPUTATIONALLY**). Equality
\(1+1=2\) gives defect \(0\) with \(w(2)=2\). No infinite theorem is
claimed from the box scan. If a negative defect exists it is a
counterexample to the triangle inequality; none was found in that box.

## CLI

```powershell
btlab operators additive --k 6
btlab operators sparse --k 1 --bound 10000
btlab operators metrics --limit 20 1 9
```
