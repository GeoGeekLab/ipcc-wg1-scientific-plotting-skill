# Figure archetypes

AR6 WGI does not use one universal plot template. Fidelity is best represented
as a set of recurring figure families plus shared design tokens.

## A. Scenario time series

Use when the primary comparison is historical/projected evolution across SSPs or RCPs.

Required grammar:

- scenario colours are semantic and profile-specific;
- historical/observed series are neutral unless a source figure specifies otherwise;
- uncertainty bands use a related shade of the corresponding series;
- scenario labels/legend are close to the lines;
- interval meaning is explicit;
- unit uses parentheses;
- short title states the quantity or comparison.

Do not use Matplotlib's default colour cycle for scenarios.

## B. Ensemble centre + interval

Use for a central estimate with model/observational spread.

Required grammar:

- central estimate visually dominates the interval;
- interval label states its statistic (e.g. 17–83% model range);
- ensemble members are not all drawn as equally strong lines unless individual
  trajectories are the message;
- neutral black/grey is appropriate when the series is not scenario-semantic.

## C. Global or regional change map

Required grammar:

- choose an official variable-matched WGI colormap;
- use explicit levels and a meaningful centre for diverging data;
- declare projection/central longitude/extent;
- keep geographic context subdued;
- colour bar carries unit;
- low agreement, insufficient data and significance remain separate layers;
- explain every non-colormap texture/colour in the caption or figure.

A reference figure may use a chapter-specific projection. Reproduce it when
doing figure-level fidelity; do not normalize everything to Robinson.

## D. Map matrix / small multiples

Use for period × scenario, variable × warming level or comparable spatial panels.

Required grammar:

- identical comparable panels use identical limits and palette;
- one shared colour bar when units/scales are the same;
- row/column headings carry the comparison logic;
- panel labels stay in fixed positions;
- maps remain large enough to read;
- uncertainty overlays use the same semantics in every panel.

## E. Multi-series line comparison

For non-scenario series:

- use the WGI generic colour order;
- after six colours, reuse colours with line-style variation;
- do not invent extra bright hues simply to make every line unique;
- direct-label lines when practical, otherwise use a semantically ordered legend.

## F. Categorical/point comparison

AR6 WGI uses many chapter-specific categorical figures; there is no single
canonical bar/point template.

Use the report-wide grammar:

- Arial;
- semantic or generic WGI colours;
- minimal decoration;
- direct labels where useful;
- units in parentheses;
- meaningful ordering;
- uncertainty intervals identified explicitly.

Do not claim a categorical layout itself is an exact WGI archetype unless a
specific reference figure is supplied.

## Fidelity modes

### Strict

Use when the user asks for "IPCC AR6 WGI style", "match IPCC", "reproduce this
AR6 figure", or equivalent.

Strict mode requires:

- Arial present;
- correct style profile selected;
- official WGI palette assets for continuous/discrete maps;
- explicit map projection for maps;
- semantic scenario colours;
- no silent generic fallbacks;
- fidelity audit completed.

### Adapted

Use when the user wants an IPCC-inspired publication figure but exact assets or
a matching archetype are unavailable.

Adapted mode may substitute fonts/palettes only if the output is labelled
"IPCC-inspired" rather than "IPCC-faithful".
