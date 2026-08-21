# Collatz research questions

Every claim is labelled PROVED, VERIFIED COMPUTATIONALLY, CONJECTURE, or
OBSERVATION. A conjecture requires automated counterexample search.
Statistical drift is not deterministic descent. Lyapunov functions are
not pursued.

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
   \(J_m\) are eventually zero. **PROVED**.
2. Every finite prefix has exactly one zero-lift extension. It is
   \(v_2(3T^m(R_m)+1)\). **PROVED**.
3. The deterministic zero-lift successor is the accelerated Collatz
   orbit of the canonical realizer. **PROVED**. This identifies the
   limitation rather than solving it.
4. Purely periodic and eventually periodic valuation itineraries have
   exact affine compatibility candidates and exact cylinder checks.
   **PROVED**. The bounded cycle census is **VERIFIED COMPUTATIONALLY**.
5. Finite precision in the canonical current state certifies many
   immediate \(J>0\) extensions; unbounded valuations leave some cases
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
2. Does sustained low \(K_m/m\) force infinitely many \(J_m>0\)?
   **CONJECTURE**; no implication is assumed.
3. Can periodic-pattern compatibility be classified beyond the exact
   candidate calculation without repackaging the positive-cycle problem?

See [docs/collatz_zero_lift.md](collatz_zero_lift.md). Nothing in
Milestone 5 proves or disproves the Collatz conjecture.
