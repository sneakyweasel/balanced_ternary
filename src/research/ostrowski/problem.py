"""Descriptor for the order-(m) Ostrowski-adder Phase-0 gate."""

from research.open_problems.definition import ProblemDefinition

PROBLEM = ProblemDefinition(
    id="ostrowski_order_m_adder",
    title="Generalized Ostrowski order-(m) adder",
    status="STRUCTURAL",
    statement=(
        "For the genuine order-3 Gamma=([0;2-bar],[0;1-bar],[0;1-bar]), "
        "the live unread-tail residuals form an explicit 55-element "
        "forward-invariant set B_MIN. The comparison Gamma=([0;2-bar],"
        "[0;1-bar],[0;3-bar]) is an irreducible Perron non-Pisot cubic "
        "with the same digit alphabets; its live union grows in every "
        "scan window, but unbounded live paths are not proved. Reverse "
        "contraction of A^{-1} is certified in a Q-norm and makes the "
        "basin of the origin finite (9164 states); that basin is not "
        "the adder live set. The non-Pisot accepting boundary is "
        "K_0 = {s3=0} and the E_n-slabs K_n, with an explicit unbounded "
        "family on F. Origin-reachable states satisfy s1 ≡ 0 (mod 3), "
        "which excludes t_n except n ≡ 0 or 12 (mod 24); that "
        "obstruction is Lean-verified. Exceptional classes occupy "
        "distinct residues mod 9, both reachable on (Z/9Z)^3; legal "
        "two-step F-returns form a finite ray. Time-augmented "
        "quotients G_m and affine forms on (remaining, s) do not "
        "separate those phases. Exact L_n layers grow along a finite "
        "live path with no symbolic family. The unread-tail energy "
        "satisfies E_{i-1}(T_w s)=E_i(s)-w q_{i-1} and the telescope "
        "E_n(T_w s)=E_{n+k}(s)-sum_j w_j q_{n+k-1-j} (Lean, KNOWN "
        "construction). Defects restate K_n. Short expanding interior "
        "blocks leave K_n. The co-live prefix language at finite N has "
        "22 consecutive Ext-windows in W (max branching 4); all length-2 "
        "and length-3 interior factors occur; occurring blocks of length "
        "4-6 that stay live return to the origin. Live Ext is the "
        "energy-slab interval in w (Lean energy_control_interval, KNOWN); "
        "width <4 through remaining 24 is computational; u=s2+2s3 is E_1 "
        "only. Neighboring energies invert s (det of consecutive adjoints "
        "is 3^{n-2}, Lean adjointDet_eq); homogeneous A^k is energy-neutral "
        "(Lean energy_homogeneous). Origin-live |s_orth| in ker(u_n) grows "
        "with horizon; no symbolic energy-neutral family. From the origin "
        "the residual is the control particular s_k = -sum A^{k-1-j} e3 w_j "
        "(Lean origin_particular, KNOWN). Unnormalized companion modes grow "
        "on remaining-0 live slices from start remaining 12 to 16; "
        "normalized |lambda|^{-k}|z| bounded is not residual boundedness; "
        "maximizer words are not a symbolic family. The origin impulse is "
        "the place-value vector A^r e3 = (3 q_{r-1}, 3 q_{r-2}+q_{r-1}, q_r) "
        "(Lean iterateA_e3, KNOWN). Large |s| does not force unique Ext. "
        "Every small integer "
        "linear form on s grows from start remaining 16 to 20. |L_0| is "
        "not proved infinite. Pisot existence of some adder is known."
    ),
    bt_relevance=(
        "The rewrite-calculus theorem add_not_DLocal isolates the LSD "
        "carry as the missing state for D(x+y). The Ostrowski question "
        "is whether a higher-dimensional unread-tail residual plays "
        "the same role. The systems are not identified."
    ),
    docs=("docs/problems/ostrowski_order_m_adder.md",),
)
