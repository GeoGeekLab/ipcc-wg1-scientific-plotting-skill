# Visual comparison: style vs fidelity

This example is a communication asset for the repository. It uses the same
synthetic SSP trajectories in four panels to separate four different claims:

1. **Matplotlib default** — no IPCC fidelity claim.
2. **“IPCC-ish”** — manually guessed colours and decorative hatching; this is
   intentionally an example of appearance without an evidence contract.
3. **Adapted / IPCC-inspired** — explicit `wgi-guide-2022` profile, semantic SSP
   colours, and disclosed substitutions.
4. **Strict contract / fidelity-aware** — `ar6-report` semantic colours and the
   project’s stricter visual grammar, while explicitly retaining the local Arial
   gate required for a truly IPCC-faithful typography claim.

The trajectories are synthetic and are **not IPCC data**.

Regenerate the assets with:

```bash
python examples/visual_comparison.py
```

Outputs:

- `default-to-fidelity.png` — README/social sharing raster.
- `default-to-fidelity.svg` — scalable source for talks, posts, and docs.

The fourth panel should not be interpreted as proof that the composite graphic
itself is an exact reproduction of an IPCC figure. Exact reproduction remains
reference-specific and must satisfy the full fidelity checklist.
