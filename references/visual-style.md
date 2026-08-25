# IPCC-native Visual Communication Guidance

Use this reference for layout, hierarchy, annotation, captioning and audience adaptation. It distills principles from the public IPCC AR6 WGI Visual Style Guide and the observed structure of AR6 chapter/Technical Summary figures without copying an official template.

## 1. Start with intent

Before styling, write:

```text
The intent of this figure is to show that ...
```

If the sentence is vague, the figure is not ready for visual design.

The visual hierarchy should let a reader recover that intent before decoding every methodological detail.

## 2. Layer information by reading speed

Design three reading depths:

### First glance: 3–5 seconds

Reader should identify:

- topic/variable;
- direction or dominant pattern;
- comparison frame (scenario, period, GWL, region);
- headline evidence.

### Analytical read: 20–60 seconds

Reader should recover:

- magnitudes;
- regional differences;
- uncertainty/spread;
- scenario identities;
- important exceptions.

### Technical read

Caption/metadata should provide:

- baseline and transformations;
- ensemble sampling unit;
- intervals and robustness rules;
- source datasets;
- methodological details needed to interpret the marks.

Do not force all technical detail into the plotting area.

## 3. Visual hierarchy

Use size, position, contrast and annotation deliberately.

Preferred hierarchy:

1. primary data mark / headline panel;
2. key comparison or central estimate;
3. uncertainty and robustness;
4. axes, coastlines, region boundaries;
5. contextual labels;
6. technical furniture.

Gridlines, political borders and backgrounds should almost never be the darkest marks.

## 4. Direct labels

Prefer direct labeling when it reduces eye travel and remains stable:

- scenario line labels at the right edge;
- region abbreviations next to points where uncluttered;
- named thresholds directly on the threshold line;
- short callouts next to exceptional regions/events.

Use legends when direct labels would collide or when the mapping is reused across many panels.

## 5. Color

Color must carry a defined scientific role.

### Sequential

Use for ordered magnitude with one direction, e.g. precipitation amount, exposure, concentration.

### Diverging

Use for signed departures around a meaningful reference, e.g. change relative to zero or anomaly relative to a baseline.

The neutral midpoint must be meaningful; do not center merely because the palette is symmetric.

### Categorical

Use for discrete identities such as scenarios, methods or evidence categories. Do not imply order with a sequential palette unless order is real.

### General rules

- avoid rainbow/jet for continuous fields;
- critical categories should remain distinguishable for common color-vision deficiencies;
- use redundant line style/marker/position when color failure would change interpretation;
- keep color identities stable across the full report/figure set where possible;
- use official/authorized IPCC/CMIP resources when available locally and provenance is clear.

## 6. Uncertainty presentation

The AR6 WGI visual guidance explicitly recognizes multiple uncertainty representations such as shaded ranges, error bars and patterns. There is no single universally correct graphical representation.

Choose based on task:

- time series: shaded interval/band;
- regional comparison: point + whisker/interval;
- map: texture/mask over primary color field;
- assessed range: interval glyph distinct from raw ensemble spread;
- distribution: raw/model-level points plus density/quantile summaries.

Where uncertainty encodings are unfamiliar, a short in-figure text explanation can reduce misinterpretation.

## 7. Maps

Maps should prioritize the scientific field over geographic decoration.

- Use an explicit projection appropriate to scale/domain.
- Use sparse coastlines and boundaries.
- Use graticules only when coordinate reference is useful.
- Ensure the colorbar is close enough to the map to be interpreted as its scale.
- If several maps share a scale, use one shared colorbar when layout permits.
- For small multiples, preserve extent and projection whenever comparison is intended.
- Treat Antarctica, polar regions and dateline wrapping deliberately rather than accepting defaults blindly.

## 8. Time series

- Separate measured/historical evidence from future scenario information when their status differs.
- Use bands behind lines, not on top of labels.
- Avoid dozens of equal-weight model lines in assessment synthesis.
- Use scenario color only where scenario divergence is meaningful.
- Use vertical reference bands/lines sparingly for assessment periods or major transitions.

## 9. Multi-panel composition

Do not use equal-size panels by default.

Recommended composition for a synthesis figure:

```text
headline / hero panel: 40–60% of visual weight
primary support: 20–30%
regional/robustness/context: remaining space
```

This is a hierarchy heuristic, not a fixed geometry rule.

Align:

- plot edges;
- baselines;
- colorbars;
- region lists;
- panel labels;
- shared legends.

Whitespace is preferable to filling unused space with redundant charts.

## 10. Annotation

Use annotations to explain assessment-relevant information:

Good:

- `Most land regions show an increase`;
- `Low model agreement`;
- `Historical` / `SSP5-8.5`;
- `2 °C GWL`;
- `Reference: 1995–2014`.

Weak:

- `Temperature graph`;
- arrows pointing to obvious maxima;
- decorative labels that duplicate ticks.

Avoid causal language unless the analysis supports causality.

## 11. Captions

A caption should be standalone enough to decode the figure while remaining concise.

Recommended order:

1. one-sentence assessment message;
2. panel-by-panel subject only if needed;
3. data transformation/baseline/period;
4. line/color/symbol/texture definitions;
5. uncertainty/robustness definition;
6. data sources and sampling unit;
7. references to methods/sections if needed.

Do not use the caption to compensate for an incoherent figure design.

## 12. Typography

- Use a consistent sans-serif family with scientific Unicode support.
- Verify the figure at final intended size.
- Keep tick/legend text compact but readable.
- Use sentence case for explanatory labels.
- Use mathematical notation consistently.
- Use Unicode minus sign when supported.
- Do not mix many font weights/styles.

IPCC report production specifications can differ from journal dimensions. Do not import Nature-specific width rules as IPCC requirements.

## 13. Accessibility and grayscale

For critical distinctions:

- check color-vision simulation;
- inspect grayscale;
- add line style, marker shape, position or label redundancy where necessary;
- ensure hatch/stipple is not the only cue at tiny scale;
- avoid red/green as the sole binary encoding.

## 14. Cognitive-load test

A figure is too dense when:

- more than two unrelated color systems are active;
- each panel uses a different legend grammar;
- map texture obscures the primary field;
- the reader must memorize several abbreviations not defined nearby;
- title, annotations and caption repeat the same sentence;
- supporting panels compete visually with the headline.

Simplify the encoding before reducing fonts or shrinking panels.

## 15. Independence disclaimer

This file is an independent distillation for an Agent Skill. It does not reproduce an official IPCC layout template and does not imply IPCC endorsement. For current IPCC production work, verify the newest official guidance.