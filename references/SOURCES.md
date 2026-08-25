# Source map

This independent Skill is distilled from public climate-assessment, visualization and reproducibility sources. It paraphrases methods and provides original helper code; it is not an official IPCC product and does not imply IPCC endorsement.

Last source review for the IPCC-native v1 branch: 2026-08-25.

## Primary IPCC / AR6 sources

- IPCC Working Group I resources page and AR6 WGI materials: https://www.ipcc.ch/working-group/wg1/
- IPCC WGI Visual Style Guide, updated June 2022: https://www.ipcc.ch/site/assets/uploads/2022/09/IPCC_AR6_WGI_VisualStyleGuide_2022.pdf
- Earlier AR6 visual style guide: https://www.ipcc.ch/site/assets/uploads/2019/04/IPCC-visual-style-guide.pdf
- IPCC AR6 WGI Atlas chapter: https://www.ipcc.ch/report/ar6/wg1/chapter/atlas/
- IPCC-WG1 GitHub organization: https://github.com/IPCC-WG1
- AR6 WGI Atlas reproducibility repository: https://github.com/IPCC-WG1/Atlas
- AR6 WGI colormap resources: https://github.com/IPCC-WG1/colormaps
- Chapter 11 analysis and visualization: https://github.com/IPCC-WG1/Chapter-11
- Chapter 9 figure repository: https://github.com/IPCC-WG1/Chapter-9
- Chapter 6 Figure 19 configuration-driven plotting: https://github.com/IPCC-WG1/Chapter-6_Fig19
- Chapter 2 Figure 31 ocean-colour workflow: https://github.com/IPCC-WG1/Chapter-2_Fig31
- ESMValTool recipe example, Chapter 3 Figure 16: https://github.com/IPCC-WG1/Chapter-3_Fig16
- FAIR principles / IPCC AR6 data traceability article: https://doi.org/10.1038/s41597-022-01739-y

## Regional framework

- IPCC AR6 reference regions / Atlas materials: https://github.com/IPCC-WG1/Atlas/tree/main/reference-regions
- Regionmask scientific region implementation: https://regionmask.readthedocs.io/en/stable/defined_scientific.html
- Iturbide et al. (2020), AR6 reference regions: https://doi.org/10.5194/essd-12-2959-2020

## Current assessment-cycle status

- IPCC Seventh Assessment Report: https://www.ipcc.ch/assessment-report/ar7/

AR7 is underway. AR6 WGI remains the public visual/reproducibility baseline used by this branch. Before claiming compliance with a current IPCC production rule, verify newly released AR7 guidance.

## Skill-production method reference

The repository architecture and production discipline were informed by the public `nature-figure-skill` project:

- https://github.com/jing1312/nature-figure-skill

What was adopted conceptually:

- contract-before-plotting workflow;
- modular reference files loaded by task;
- figure archetype classification;
- adversarial QA before delivery;
- code + source/plotted data + export bundle thinking.

No Nature-specific journal dimensions, private templates, or proprietary material are treated as IPCC requirements. IPCC-native scientific semantics are independently derived from the primary sources listed above.

## License and reuse note

Upstream repositories and IPCC assets have heterogeneous copyright/licensing terms. Consult each upstream source before copying code, figures, color data or geographic assets. This Skill intentionally favors original helper implementations and local loading of authorized upstream color resources rather than redistributing them.