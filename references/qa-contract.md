# IPCC-native QA Contract

Use before final delivery, review packages, public release, or any claim that a figure is IPCC-quality / assessment-grade.

This is an independent QA framework based on public AR6 WGI practices and general reproducible climate-science standards. It is not an official IPCC approval checklist. The public AR6 WGI Visual Style Guide (updated June 2022) is the current public baseline used here; verify newer official guidance during AR7 before claiming current conformance.

## A. Assessment logic

- [ ] Assessment intent is one sentence with a conclusion verb or an explicitly provisional question.
- [ ] Dominant audience is declared.
- [ ] Each panel has a unique evidence role.
- [ ] Removing any panel would weaken a specific part of the argument; otherwise remove/merge it.
- [ ] Figure archetype is declared.
- [ ] Headline evidence has appropriate visual hierarchy.
- [ ] Caption can stand alone without requiring the reader to reverse-engineer encodings.

## B. Estimand and data

- [ ] Variable/index and scientific definition are explicit.
- [ ] Unit and sign convention match code and colorbar/axis.
- [ ] Baseline/reference period is explicit and correct.
- [ ] Target period, season or GWL is explicit.
- [ ] Calendar and seasonal-year convention are handled correctly.
- [ ] Transformation (absolute anomaly, percent, ratio, standardized, exceedance) is explicit.
- [ ] Spatial domain/mask is explicit.
- [ ] Area weighting is valid for regional/global aggregation.
- [ ] Regridding method is documented and appropriate to the variable.
- [ ] No visual interpolation manufactures apparent resolution.
- [ ] Missing data are distinguished from zero/no change.

## C. Ensemble integrity

- [ ] Sampling unit is named: model, realization, observational product, event, etc.
- [ ] Model identities and member identities are not conflated.
- [ ] Multiple realizations are handled according to a declared within-model policy.
- [ ] Model weighting, if any, is recorded and normalized.
- [ ] `n_valid` is computed from actual available samples at each grid cell/region/period when availability varies.
- [ ] Minimum valid sample threshold is declared.
- [ ] Ensemble spread is not mislabeled as a confidence interval.

## D. Uncertainty and robustness

- [ ] Every interval/band/whisker has a precise statistical definition.
- [ ] Observational uncertainty, internal variability, model spread and scenario uncertainty are not collapsed into one undefined band.
- [ ] Robustness classes are pre-declared, mutually exclusive and exhaustive over valid data.
- [ ] Hatching/stippling/opacity has exactly one semantic meaning per figure.
- [ ] Sign agreement is not called statistical significance.
- [ ] Statistical significance is not called confidence in the IPCC assessment-language sense.
- [ ] If pointwise spatial tests are used, multiplicity/dependence has been considered.
- [ ] Zero tolerance, if any, is scientifically motivated and recorded.

## E. Scenario / GWL / region semantics

- [ ] Canonical scenario labels are preserved.
- [ ] Scenarios are not presented as probabilities without a probabilistic framework.
- [ ] Scenario identities/colors/line styles are stable across panels.
- [ ] Historical-to-scenario transition is handled explicitly.
- [ ] GWL definition, crossing/window method and sample composition are recorded.
- [ ] Fixed time slices and GWL windows are not silently mixed.
- [ ] AR6 reference regions use verified geometries and correct land/ocean domain.
- [ ] Custom regions have a source/version/CRS/provenance record.

## F. Color and visual semantics

- [ ] Sequential vs diverging vs categorical palette matches the variable semantics.
- [ ] Diverging neutral point equals the scientific neutral/reference value.
- [ ] Colorbar range/breaks are declared and comparable across panels intended for comparison.
- [ ] No rainbow/jet for continuous fields.
- [ ] Critical distinctions survive common color-vision deficiencies or have redundant encoding.
- [ ] Missing/insufficient data use a neutral state not present in the scientific scale.
- [ ] Texture density remains interpretable at final size.
- [ ] Coastlines/borders/graticules are subordinate to the data.
- [ ] No faux 3D, shadows or decorative gradients.

## G. Layout and typography

- [ ] Figure is reviewed at final intended report/publication size.
- [ ] Tick, legend and annotation text is legible without zooming.
- [ ] Panel labels are consistent and unobtrusive.
- [ ] Comparable panels use aligned axes/scales where scientifically valid.
- [ ] Repeated legends are consolidated where possible.
- [ ] Direct labels reduce eye travel where stable and uncluttered.
- [ ] Colorbar has units and a concise variable label where needed.
- [ ] No clipped titles, labels, legends, colorbars or map content.
- [ ] Dense raster layers are rasterized selectively while text/axes remain vector where possible.

## H. Caption contract

The caption should define, where applicable:

```text
assessment message
variables/indices
baseline and target period/GWL
spatial domain
scenario/experiment set
center statistic
uncertainty interval
robustness/significance texture
sample unit and minimum n
observational/model data sources
special transformations or masks
```

The AR6 WGI Visual Style Guide recommends concise standalone captions and emphasizes explaining lines, symbols, shading and colors. Keep interpretation in the main text when it becomes lengthy, but do not omit decoding information needed to understand the figure.

## I. FAIR / reproducibility bundle

Expected files where applicable:

```text
figure_XX.pdf
figure_XX.svg
figure_XX.png
figure_XX_plotted_data.nc
figure_XX_provenance.json
figure_XX_recipe.yaml
figure_XX_qa.md
```

Checks:

- [ ] Plotted-data artifact contains the exact numerical fields used for drawing.
- [ ] Figure can be regenerated from plotted data without rerunning raw-data analysis.
- [ ] Recipe records scientific and visual parameters.
- [ ] Provenance records input paths or stable identifiers, hashes when feasible, environment and Git revision.
- [ ] Random seed is fixed for bootstrap/resampling/stochastic layout where applicable.
- [ ] Software versions are captured.
- [ ] Regridding weight files or their hashes/method are captured when material.
- [ ] Region geometry source/version is captured.

## J. Automated checks

Run available tests and preflight:

```bash
pytest -q
python scripts/check_figure.py outputs/figure_01.pdf \
  --metadata outputs/figure_01.provenance.json
```

Recommended additional checks in mature projects:

- image-regression tests with renderer tolerance;
- recipe schema validation;
- data-unit tests for baseline/aggregation;
- deterministic plotted-data hashes;
- PDF/SVG text/editability checks;
- color-vision simulation for critical categorical encodings;
- programmatic check that map `n_valid`, robustness mask and caption thresholds agree.

## K. Human adversarial review

Before release, answer:

1. What would a skeptical climate scientist challenge first?
2. Could a policymaker mistake scenario identity for probability?
3. Could a reader mistake missing data for no change?
4. Does the map look more spatially precise than the data are?
5. Does a texture imply significance/agreement/confidence different from the caption?
6. Are ensemble members inflating apparent evidence?
7. Could the headline survive if the color were removed and values were read numerically?
8. Can another analyst reproduce the exact plotted fields?

Any unresolved `yes` is a QA issue, not a styling preference.