---
name: ipcc-native-plot
description: >-
  IPCC-native climate-assessment visualization workflow for Python/xarray/Matplotlib/Cartopy. Use for climate, Earth-system, CMIP, observation/reanalysis, extremes, scenario, warming-level, regional and uncertainty figures when the target is IPCC-class assessment quality, publication-grade scientific plotting, policy-facing synthesis or FAIR/reproducible figure delivery.
---

# IPCC-native Plot

This is the Claude/Agent discovery entrypoint for the repository.

**Before doing any plotting task, read and follow `../../SKILL.md` as the canonical instruction file.** Do not treat this dispatcher as a shortened alternative to the canonical rules.

Then load only the reference modules required by the task:

- `../../references/assessment-contract.md` — always for a new assessment figure;
- `../../references/ipcc-archetypes.md` — when selecting figure architecture;
- `../../references/climate-data-contract.md` — for climate-model, observational, reanalysis, remote-sensing or gridded data;
- `../../references/uncertainty-robustness.md` — before intervals, hatching, stippling, agreement or significance;
- `../../references/scenarios-regions.md` — for SSP/RCP, Global Warming Levels or AR6/custom regions;
- `../../references/visual-style.md` — for hierarchy, annotation, color, layout and caption design;
- `../../references/qa-contract.md` — before final delivery;
- `../../references/SOURCES.md` — when source provenance or current IPCC baseline needs verification.

Use the reusable Python implementation in `../../scripts/ipcc_sciplot/` and start new figure contracts from `../../templates/ipcc_native_recipe.yaml`.

This is an independent workflow distilled from public IPCC AR6 WGI practices. It is not an official IPCC product and does not imply IPCC endorsement. AR7 is underway; verify newly released official guidance before claiming current IPCC conformance.
