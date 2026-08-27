# Diophantine gap survey for n^3 - b^4

Whether a known perfect-power gap rules out
`0 < n^3 - b^4 <= 2 b^2` for odd non-square `n` and `b = a^2`.
This is not a `10^8` rerun, not Baker/Thue code, and not a theorem.

- persisted hits: `465`
- exact family `r = 0`: `464`
- positive-`r` hits: `1`
- odd non-square hits: `0`
- any published bound beats `2b^2`: `False`
- classification: **DIOPHANTINE_ESCALATION_REQUIRED**

## Scale a theorem must reach

The window is `0 <= n^3 - b^4 <= 2 b^2` with `b = a^2`.
A useful lower bound must exceed `2 b^2` after excluding the
exact family `r = 0` and after remaining legal at `a = 97`.

Rewritten as a square-cube gap: `Y = b^2 = a^4`, `X = n`,
`|X^3 - Y^2| <= 2 Y`. Hall-type bounds give about `X^{1/2}`,
while `2 Y` is about `X^{3/2}`.

## a = 97 must survive

- `b = 9409`, `n = 198636` even
- `r = 165506495`
- `2 b^2 = 177058562`
- `r <= 2 b^2`: `True`

Any bound `|X^3 - Y^2| > 2 Y` without extra hypotheses is false.
Oddness, or `Y` being a fourth power together with odd `X`, is
required.

## Persisted positive-`r` hits

- a `97`, n `198636`: r `165506495`, 2b^2 `177058562`, odd `False`

## Adversarial regressions

- a `2`: cube `False`, n `7`, r `87`, r<=2b^2 `False`, odd `True`
- a `3`: cube `False`, n `19`, r `298`, r<=2b^2 `False`, odd `True`
- a `6`: cube `False`, n `119`, r `5543`, r<=2b^2 `False`, odd `True`
- a `8`: cube `True`, n `256`, r `0`, r<=2b^2 `True`, odd `False`
- a `27`: cube `True`, n `6561`, r `0`, r<=2b^2 `True`, odd `True`
- a `79`: cube `False`, n `114905`, r `177861064`, r<=2b^2 `False`, odd `True`
- a `97`: cube `False`, n `198636`, r `165506495`, r<=2b^2 `True`, odd `False`
- a `125`: cube `True`, n `390625`, r `0`, r<=2b^2 `True`, odd `True`
- a `37840`: cube `False`, n `1613874181767`, r `64339188707111144663`, r<=2b^2 `False`, odd `True`

## Candidate theorems

### Mihailescu / Catalan

- citation: Mihailescu 2004; consecutive perfect powers are 8 and 9
- status: `THEOREM`
- theorem variables: |x^p - y^q| for p,q > 1
- our variables: x=n, p=3, y=b, q=4
- hypotheses: nonzero difference of perfect powers
- resulting lower bound: 2
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

### Liouville on x^3 - b^4

- citation: defining polynomial x^3 - b^4, degree 3
- status: `THEOREM`
- theorem variables: alpha = b^{4/3}, integer n
- our variables: r = |n^3 - b^4|
- hypotheses: b not a cube
- resulting lower bound: 1
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

### Roth / height-dependent irrationality of b^{4/3}

- citation: Roth 1955; height of x^3 - b^4 is b^4
- status: `THEOREM`
- theorem variables: |alpha - p/q| > c(alpha)/q^{2+eps}
- our variables: alpha = b^{4/3} depends on b; q = 1
- hypotheses: alpha algebraic irrational
- resulting lower bound: b^{-O(1)} after height; weaker than r >= 1 at our scale
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

### Hall conjecture (strong)

- citation: Hall 1971; |Y^2 - X^3| > C X^{1/2}
- status: `CONJECTURE`
- theorem variables: X cube-root side, Y square-root side
- our variables: X=n, Y=b^2=a^4; need |X^3-Y^2| > 2Y = 2 X^{3/2}
- hypotheses: Y^2 != X^3; C absolute
- resulting lower bound: C n^{1/2} ~ C b^{2/3}
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

### Weak Hall / ABC

- citation: Stark-Trotter; Masser-Oesterle ABC implies weak Hall
- status: `CONJECTURE`
- theorem variables: |Y^2 - X^3| > c(eps) X^{1/2-eps}
- our variables: same X=n, Y=a^4
- hypotheses: ABC or an eps-Hall statement
- resulting lower bound: n^{1/2-eps}
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

### Danilov optimality of the Hall exponent

- citation: Danilov 1982 Math. Notes 32
- status: `THEOREM`
- theorem variables: |Y^2 - X^3| < C X^{1/2} infinitely often
- our variables: general square-cube pairs, Y not forced to a fourth power
- hypotheses: none on Y being a fourth power
- resulting lower bound: no C, delta with |X^3-Y^2| > C X^{1/2+delta} for all pairs
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

### Bennett differences of perfect powers (fixed bases)

- citation: Bennett CMB 2008
- status: `THEOREM`
- theorem variables: 0 < |A^x - B^y| < (1/4) max(A^{x/2}, B^{y/2})
- our variables: A,B fixed; x,y variable. Ours is opposite
- hypotheses: A,B fixed positive integers
- resulting lower bound: at most one exponent pair; no |n^3-b^4| bound
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

### Bennett |A x^n - B y^n| = 1

- citation: Bennett Crelle / LMS 1997-2001
- status: `THEOREM`
- theorem variables: same exponent n >= 3
- our variables: exponents 3 and 4 differ; not this equation
- hypotheses: equal exponents
- resulting lower bound: does not apply
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

### Bugeaud effective gap depending only on the exponents

- citation: Bugeaud 1996; Waldschmidt survey arXiv:0908.4031
- status: `THEOREM`
- theorem variables: |x^n - y^m| for fixed n,m
- our variables: n=3, m=4; bound independent of x,y
- hypotheses: x^3 != y^4
- resulting lower bound: C(3,4), a constant
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

### Baker linear forms in logarithms for |X^3-Y^2|

- citation: Baker; later Laurent-Mignotte-Nesterenko
- status: `THEOREM`
- theorem variables: linear form log X^3 - log Y^2
- our variables: typically (log n)^C or n^eps with tiny eps
- hypotheses: effective transcendental estimates
- resulting lower bound: (log n)^C or n^eps << 2 n^{3/2}
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

### Superelliptic x^3 - y^8 = k for fixed k

- citation: Bilu-Hanrot; Baker-Davenport reductions; Faltings for each k
- status: `THEOREM`
- theorem variables: k fixed, x,y variable
- our variables: k = r grows up to 2 a^4
- hypotheses: k constant
- resulting lower bound: does not apply uniformly in r
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

### Pillai conjecture

- citation: Pillai 1945; open for |k| > 1
- status: `CONJECTURE`
- theorem variables: x^p - y^q = k, finitely many for each k
- our variables: no explicit |n^3-b^4| rate
- hypotheses: p,q >= 2
- resulting lower bound: gaps -> infinity, no 2b^2 rate
- beats `2b^2`: `False`
- `a=97` remains legal: `True`

## Weakest bound that would suffice

|x^3 - y^8| > 2 y^4 when y is not a cube and x is odd (equivalently |X^3 - Y^2| > 2Y when Y is a fourth power and X is odd). This is stronger than Hall and not a published theorem.

## Formalization cost

Mihailescu is realistic to cite and too weak. Hall is open and still too weak. Baker/Thue proofs of weaker |X^3-Y^2| bounds are not a practical Lean import and still miss 2Y.

## Unresolved statement

0 < n^3 - b^4 <= 2 b^2 with b = a^2 not a cube and n odd.

`a = 97` survives: `True`.

