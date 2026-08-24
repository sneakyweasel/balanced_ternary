# Residual Explorer

Interactive visualization of residual prefix trees, Newton classes, and
depth-deficit visibility. This is a **tool**, not a new mathematical
development.

Launch:

```powershell
python -m pip install -e ".[ui]"
btlab ui
```

Open **Calculus research → Residual explorer**, or start the same app with
`btlab calculus explorer` (an alias of `btlab ui`).

## Architecture

```
Streamlit page
    visualization/app_pages/calculus_explorer.py
        visualization/residual_explorer.py   (view-models, no Streamlit)
            bt.calculus.*                    (closed forms, F_k)
            research.residuals.*             (fibres, layers, Q)
            visualization/theorem_ledger.py
                docs/theory/theorem_ledger.json
```

The browser never computes section derivatives, Newton coordinates, fibres,
or valuations. Those come from existing Python modules:

| Visual | Source |
|---|---|
| Residual along a prefix | `residual_along`, `cubic_residual_formula`, `quadratic_residual_formula` |
| Newton / `Φ_k` | `newton_coeffs`, `phi_k`, `F_k` |
| Equivalence / `τ` | `function_equiv`, `first_distinction_horizon`, `distinguish_pair` |
| `x^3` fibres | `deepest_fibre_of`, `inter_fibre_of`, `def2_fibre_of`, `depth_image` |
| Census | `image_profile` for `x^3`; closed `M_k=R_k` for `x^2` |
| Claim badges | `docs/theory/theorem_ledger.json` |

## Data flow

1. The top form batches polynomial, horizon `k`, and depth mode. **Run**
   commits them.
2. The adapter requests only the **visible subtree** (default first three
   levels, plus a zero-spine to the focused depth).
3. Selecting a node inspects that residual only.
4. Fibre / compare / `x^2` vs `x^3` cards run when opened.

## Controls

- **Polynomial.** Presets `x`, `x+1`, `2x+1`, `x^2`, `x^3`, `x^4`. Custom
  text uses `parse_poly` (`x^2`, not `x²`).
- **Horizon k.** Integer in `[1, 14]`. Higher `k` is finer resolution
  modulo `3^k`.
- **Depth mode.** Explicit `m`, or deficit `r` with `m = k-1-r`.
- **Explain / Research.** Explain uses short sentences derived from the
  same adapter output. Research shows raw integers, residues, Lean names,
  and ledger tags.
- **Tree navigation.** Trit-step buttons, expand selected, expand subtree
  (capped at 80 nodes), class / merge filters, Set A / Set B. Colour is
  class among **loaded** nodes; squares are visible merges; class id is
  written on the node.
- **Delayed pair.** Compare → Load delayed-distinction pair jumps to the
  first `x^3` merge at `k=2`. Raising `k` to 3 and pressing Run splits
  the class.

## Mathematical meaning of each visual

- **Tree node.** A residual `f_w` along an LSD-first prefix `w`, with
  packed `p = p(w)` and depth `m = |w|`.
- **Exact residual.** The ordinary polynomial. Distinct words give distinct
  polynomials for `x^2` and `x^3`.
- **Observable class.** `Φ_k(f)`, the Newton residues modulo `3^k`. This
  is the finite-horizon Myhill–Nerode class.
- **Depth deficit `r = k-1-m`.** For `x^3`, `N2` equality is `p ≡ q
  (mod 3^r)` (`BTA-x3-vis`, Lean verified). The labels `r=0,1,2` are the
  current research layers.
- **3-adic strip.** Fixed-width digits of `p` and residues `p mod 3^j`.
  Highlighted low-order trits are those `N2` can see.
- **Fibre.** Residuals with the same `Φ_k`. Layer APIs are used at
  `r ∈ {0,1,2}`; full cross-depth `fibre_of` is opt-in and only for
  `k ≤ 8`.
- **Compare / microscope.** `h = f-g`, Newton coefficients of `h`,
  valuations, `τ`, and a shortest distinguishing word from
  `distinguish_pair`.
- **Q invariant.** For `x^3` on the exhausted `3^r` locus, the two-scale
  split `u=a+3^t b`, `B_t(u)`, and `Q(u)`, plus a pair comparison that
  shows when `Ψ4` merges distinct `Q`-classes.

## Performance limitations

| Horizon | Tree | Census |
|---|---|---|
| `k ≤ 10` | Lazy, interactive | `x^3` Newton image is computed and cached |
| `k = 12` | Lazy | Warning; enable expensive census |
| `k = 14` | Lazy | Opt-in only; millions of residuals |

The page never renders `3^k` nodes. Default visible size is at most 120
nodes.

## What the explorer does not prove

The UI visualizes and computes. It does not add theorems.

- Lean remains the proof authority.
- A displayed integer at `k=10` is a computation, not a proof that a
  pattern continues.
- Claim badges come from the theorem ledger. Conjectures and refutations
  do not share the visual treatment of Lean-verified statements.
- Finite-horizon merges are delayed distinctions, not infinite
  equivalence.
- The explorer does not claim progress on Collatz or any other
  number-theoretic decision problem.
