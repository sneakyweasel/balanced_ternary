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

## Still open

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

The research question of the module remains:

> Which balanced ternary languages correspond to prescribed future
> Collatz valuation paths?

Milestone 3 answers that question for every *finite* valuation prefix by
an exact residue class and a residue DFA. It does not answer the question
by solving Collatz.
