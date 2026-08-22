# Collatz research questions

Every claim is labelled PROVED, VERIFIED COMPUTATIONALLY, CONJECTURE, or
OBSERVATION. A conjecture requires automated counterexample search.
Statistical drift is not deterministic descent. Lyapunov functions are
not pursued.

This file is the active claim register. Separate placeholder result and
hypothesis logs were retired; experimental tables live under
`experiments/` when a runner writes them.

## Answered in Milestone 2 (with the stated status)

1. \(\mathrm{BT}(3n+1)=\mathrm{BT}(n)+\) for \(n\neq 0\), with closed-form
   feature deltas. **PROVED** (Layer A).
2. Division by 2 (and by \(2^k\)) is finite-state LSD-first on even
   integers / on \(L_k\). The unrestricted odd-part map is not a single
   rational transduction (Mealy / subsequential / rational-function
   model, regularity of preimages, non-regularity of \(\{\mathrm{BT}(2^j)\}\)
   by pumping, contradiction). **PROVED** (Layer B).
3. Admissible finite valuation prefixes via the precision-drop residue
   graph, classified by the exact budget \(2^{\sum k}\) vs \(3^m\).
   **PROVED** as a congruence / comparison; enumeration at finite \(P\)
   is computational (Layer C). Layer C `FORBIDDEN` is relative to a fixed
   starting \(P\), not a global prohibition.
4. The word graph \(w\xrightarrow{k}w'\) is `odd_part(append_plus(w))`.
   Truncations and synchronizing-string searches are samples
   (Layer D).

## Answered in Milestone 3

1. Valuation cylinders \(C_{\mathbf{k}}\) are unique residue classes
   modulo \(2^{1+K}\) of density exactly \(2^{-K}\) among odd residues.
   Every finite positive valuation word is admissible at that minimum
   precision. **PROVED**.
2. The BT language of a cylinder is the residue DFA at modulus \(2^{1+K}\).
   Length-\(L\) padded counts and \(H_L\) are **VERIFIED COMPUTATIONALLY**.
3. Precision cost \(P=Q+K\) is the 2-adic information consumed by a
   valuation word. Identifying this with the homogeneous factor \(2^K\)
   versus \(3^m\) is a dictionary, not a Lyapunov proof.
4. The graph of nodes \((\mathbf{k}, r \bmod 2^P, P)\) is a graph of
   symbolic futures, distinct from the sampled integer graph.

## Answered in Milestone 4

1. Exact affine formula \(T^m(n)=(3^m n+C)/2^K\) with
   \(C_{\mathrm{append}\,k}=3C+2^{K}\) and closed form
   \(\sum_j 3^{m-1-j}2^{K_j}\). **PROVED**.
2. Positivity of intermediates for positive odd \(n\) is automatic
   (\(C\ge 0\)). **PROVED**.
3. \(R(\mathbf{k})\) is the unique residue modulo \(2^{K+1}\); nested
   \(R\) is nondecreasing; \(R_m\to\infty\) excludes a positive integer
   realizer of that entire infinite itinerary. **PROVED**.
   \(R((1)^m)=2^{m+1}-1\). **PROVED**.
4. Adjacent swap formula for \(C\); descending order maximises \(C\).
   **PROVED**. \(R\) can change at equal \((m,K)\). **VERIFIED
   COMPUTATIONALLY**.
5. The exceptional itinerary compatibility problem is formulated, not
   solved. No finite certificate of \(R_m\to\infty\) for all
   non-contracting itineraries was found.

## Answered in Milestone 5

1. An infinite itinerary has a positive integer realizer iff its nested
   minima \(R_m\) eventually stabilize iff its exact lift coefficients
   lift digits \(t_m\) are eventually zero. **PROVED**.
2. Every finite prefix has exactly one zero-lift extension. It is
   \(v_2(3T^m(R_m)+1)\). **PROVED**.
3. The deterministic zero-lift successor is the accelerated Collatz
   orbit of the canonical realizer. **PROVED**. This identifies the
   limitation rather than solving it.
4. Purely periodic and eventually periodic valuation itineraries have
   exact affine compatibility candidates and exact cylinder checks.
   **PROVED**. The bounded cycle census is **VERIFIED COMPUTATIONALLY**.
5. Finite precision in the canonical current state certifies many
   immediate positive-lift extensions; unbounded valuations leave some cases
   unresolved at every fixed precision. **PROVED**.

## Other still-open questions

1. Closed form for minimized `/2^k` state complexity \(N_k\). The pattern
   \(N_k=2^k+1\) is a **CONJECTURE** with counterexample search
   (`btprime collatz complexity`).
2. Closed form for \(A_k\), the minimized DFA size of \(L_k\).
3. A complete description of the sofic / regular language of *infinite*
   admissible valuation sequences on odd 2-adics (finite prefixes are
   now completely described).
4. Whether interesting synchronizing digit contexts have a structural
   characterisation beyond finite search.
5. Inverse-language structure of predecessor BT words.
6. Lyapunov / drift questions — explicitly deferred.
7. Optional product experiments with prime-sieve moduli remain
   exploratory. They must not be described as constraining or solving
   Collatz.

The research question of the module is now:

> What distinguishes infinite or arbitrarily long positive integer
> trajectories from arbitrary finite 2-adically admissible valuation
> itineraries?

## Milestone 5 open questions

1. Can a finite abstraction certify infinitely many positive lifts for
   a nontrivial infinite class of future valuation patterns?
2. Does sustained low \(K_m/m\) force infinitely many \(t_m>0\)?
   **CONJECTURE**; no implication is assumed.
3. Can periodic-pattern compatibility be classified beyond the exact
   candidate calculation without repackaging the positive-cycle problem?

See [docs/collatz_zero_lift.md](collatz_zero_lift.md). Nothing in
Milestone 5 proves or disproves the Collatz conjecture.

## Answered in Milestone 6

1. \(R\) has the direct residue formula
   \(R\equiv(2^K-C)3^{-m}\pmod {2^{K+1}}\). **PROVED**.
2. The lift digit has an exact modular formula from the state
   \((m,T^m(R))\), and the endpoint has a closed successor recurrence.
   **PROVED**.
3. For fixed valuations, lift digits form a unique mixed-radix expansion
   of \((R-1)/2\). **PROVED** and **EXACT — LEAN VERIFIED**.
4. Even the complete \(\operatorname{BT}(R)\) does not determine the next
   zero-lift valuation or a proposed lift digit. **EXACT COUNTEREXAMPLE**.
5. Adjacent swaps satisfy an exact residue law for \(R\), but modular
   wraparound prevents the sorted \(C\) order from inducing a sorted
   \(R\) order. **PROVED**.

See [docs/collatz_dual_coding.md](collatz_dual_coding.md).

## Answered in the four-coordinate compatibility milestone

1. Kramer's affine constant is exactly this repository's \(C\), his
   2-adic representative is \(r=R\bmod2^K\), and his least-positive
   endpoint representative is \(M\equiv C2^{-K}\pmod{3^m}\).
   **PROVED** by direct congruence reduction and exhaustive regression.
2. The canonical endpoint always satisfies \(x_m\equiv M\pmod{3^m}\).
   This adds an exact 3-adic compatibility view, but it is still a
   deterministic function of the exponent code. **PROVED; LEAN VERIFIED**
   at the endpoint-congruence interface.
3. \(\operatorname{BT}(R)\) is not an information-theoretically independent
   coordinate once exact \(R\), or the complete exponent code, is retained.
   **PROVED** by determinism of canonical encoding.
4. Even the complete word \(\operatorname{BT}(R)\) does not determine the
   next zero-lift valuation or proposed lift behavior. The exact witness
   \((1)\) versus \((1,4)\), both with \(R=3\), is preserved in the
   information-content experiment. **EXACT COUNTEREXAMPLE**.
5. Rational base \(3/2\) makes the odd parity-map branch
   \(n\mapsto(3n+1)/2\) an append-\(1\) operation. Balanced ternary makes
   \(n\mapsto3n+1\) append-\(+\). Neither identity alone localizes all
   halvings of the accelerated map. **PROVED identities; no superiority
   claim**.
6. Lift digits are unique mixed-radix blocks of the refined 2-adic
   representative, so they expose existing exact 2-adic information rather
   than add an independent coordinate. **PROVED; LEAN VERIFIED**.
7. Fixed-depth and fixed-valuation observables retain finite-state models.
   Dhiman--Pandey's undefinability result applies to the full arbitrary-step
   relation in \(BA_2\), not these bounded objects. No unrestricted finite
   compatibility automaton was obtained.

The strong candidate hypothesis \(H_{\mathrm{BT}}\), interpreted as an
additional exact obstruction not implied by the code and exact \(R\), is
**REFUTED EXACTLY**. Balanced ternary remains useful as an exposed
representation and as a partition of deliberately lossy finite states.
See [literature_comparison.md](literature_comparison.md) and
[balanced_ternary_vs_collatz_literature.md](balanced_ternary_vs_collatz_literature.md).

## Affine-center milestone

1. Every nonempty code has the exact rational affine center
   \(n_*=C/(2^K-3^m)\). **PROVED**.
2. The centered start and endpoint satisfy
   \(X-n_*=(3^m/2^K)(R-n_*)\), with explicit unreduced and reduced
   numerator/denominator pairs. **PROVED; LEAN VERIFIED** in
   cross-multiplied form.
3. Expanding codes satisfy \(n_*<0<M,R<X\). Contracting codes move toward
   a positive center, with equality only at a fixed point. **PROVED**.
4. The 3-adic coordinate obeys \(X=M+q3^m\), \(q\ge0\), hence \(M\le X\).
   **PROVED; LEAN VERIFIED**.
5. No universal total order was found between \(R\) and \(M\), or between
   \(C\) and \(R\); exact bounded witnesses occur in both directions.
   **VERIFIED COMPUTATIONALLY**.
6. The candidate inequality \(n_*\le R\) survived 5,460 recorded rows and
   a separate 2,015,539-prefix streamed search. It remains a
   **CONJECTURE**; in the contracting regime it is equivalent to \(X\le R\).

See [collatz_affine_center.md](collatz_affine_center.md).

## Answered in Milestone 9

1. Canonical BT reversal \(W\) is OEIS A134028. It is an involution if and
   only if \(n=0\) or \(3\nmid n\). **PROVED; LEAN VERIFIED** at the
   digit-list level. \(W(3n)=3W(n)\) is **REFUTED EXACTLY** at \(n=1\).
2. \(T(W(n))\) is defined, for odd \(n\) not divisible by 3, iff
   \(n\equiv 1\pmod 3\). **PROVED**.
3. \(W\circ T=T\circ W\) on that domain is **REFUTED EXACTLY** at \(n=3\).
   Zero commutators through odd \(n\le 20000\) are
   \(\{1,121,5461,9841\}\). **VERIFIED COMPUTATIONALLY**.
4. \(s_3(3n+1)=s_3(n)+1\) remains the only exact digit-sum Collatz
   transition; \(\Delta_s\) isolates the odd-part step. **PROVED**.
5. \(W(R(\mathbf{k}))\) is not \(R\) of the reversed or tail-reversed
   itinerary. Smallest witness \(\mathbf{k}=(1)\). **REFUTED EXACTLY**.
6. No constraint on near-critical exponent codes was found.
   **OBSERVATION**.

See [collatz_bt_warp.md](collatz_bt_warp.md).
