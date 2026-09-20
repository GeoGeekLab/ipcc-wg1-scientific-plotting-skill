# Visual comparison: source data vs fidelity claim

This communication asset uses **official IPCC AR6 WGI Chapter 6 Figure 6.18 source
data**, pinned to commit `09d9b43fe935fc81d828147f91b717396a84fca3`.

The same CH₄ source rows are rendered under four different contracts:

1. **Raw plotting** — generic plotting with no fidelity claim.
2. **“IPCC-ish”** — guessed colours and decorative hatching; visual resemblance
   without an evidence contract.
3. **Adapted / IPCC-inspired** — explicit `wgi-guide-2022` semantic SSP colours
   with substitutions disclosed.
4. **Reference-grounded AR6** — `ar6-report` scenario semantics, report-style
   history treatment, source-derived RCP/ECLIPSE ranges, and an audit gate.

There are **no synthetic trajectories** in this comparison.

Regenerate:

```bash
python examples/visual_comparison.py
```

Verify the committed asset against the pinned upstream source:

```bash
python examples/visual_comparison.py --check
```

The comparison demonstrates increasingly strong fidelity claims; it does not
replace reference-specific scientific review. Exact reproduction still requires
the full fidelity checklist and local Arial availability where strict typography
is claimed.
