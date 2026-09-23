---
name: ipcc-wg1-scientific-plotting
description: 高保真蒸馏 IPCC AR6 Working Group I 的科学图形语言。基于 WGI Visual Style Guide、官方 colormaps、AR6 章节绘图代码、TSU 审图意见与 Atlas 不确定性框架，生成或审查 IPCC-faithful / IPCC-inspired 科研图。
---

# IPCC AR6 WGI Scientific Plotting Skill

目标是复现 IPCC AR6 WGI 的 visual grammar，并把常用规则落实为可复用的绘图与检查接口。

## 1. Profile

### Strict / IPCC-faithful

用于明确的 IPCC/AR6/WGI 风格或具体图复刻。

- 选择 `ar6-report` 或 `wgi-guide-2022`
- Arial
- 90 mm / 180 mm print width，最大高度 250 mm
- SSP/RCP 语义颜色
- 地图使用官方 WGI colormap asset
- 地图投影显式指定
- 单位使用圆括号
- agreement / significance / missing-data 分开编码
- 输出前运行 fidelity audit

缺少 strict 所需资产时直接报错，或切换到 adapted profile。

### Adapted / IPCC-inspired

用于保留 IPCC 视觉语法、但允许字体、palette 或布局替代的图。

## 2. Evidence

具体 AR6 figure 的优先顺序：

1. published reference figure
2. 同时期 WGI visual guide 与 TSU review evidence
3. 官方 colour assets 与 chapter plotting code
4. Atlas uncertainty guidance
5. 一般 scientific visualization practice

新图若明确采用 2022 更新规范，使用 `wgi-guide-2022`。2021 final-report figure 使用对应时期的 report-era tokens。

详细来源：

- `references/SOURCES.md`
- `references/evidence_matrix.md`

## 3. Figure contract

绘图前记录核心参数：

```yaml
figure_id: figure_01
question: What should the reader learn?
estimand: Exact scientific quantity/comparison
plot_type: map
archetype: global-change-map
style_profile: ar6-report
fidelity: strict
variable: tas
unit: °C
baseline: 1850-1900
period: 2081-2100
scenario: SSP2-4.5
colormap: temp_div
projection: Robinson
center_value: 0
uncertainty: method-defined
robustness: method-defined
```

具体复刻同时记录 chapter / figure number、projection、extent、panel geometry、levels、annotation、legend 和 scientific method。

## 4. Delivery geometry / typography

AR6 WGI print grammar：

- single column: **9 cm**
- double column: **18 cm**
- maximum height: **25 cm**
- smaller figure text: about **9 pt**
- larger figure text: about **11 pt**
- black axes: **0.5 pt**
- print raster: **350 ppi**
- font: **Arial**
- units: `Variable (unit)`

```python
from ipcc_sciplot import axis_label, panel_label, publication_context

with publication_context(width="double", strict_font=True):
    ax.set_ylabel(axis_label("Temperature change", "°C"))
    panel_label(ax, "a", title="Global mean")
```

避免多余的 bold、italic、grid、frame 和装饰。

## 5. Colour

### Scenario colours

```python
from ipcc_sciplot import scenario_style

scenario_style("SSP2-4.5", profile="ar6-report")
scenario_style("SSP2-4.5", profile="wgi-guide-2022")
```

- `ar6-report`: final-report-era figure/code
- `wgi-guide-2022`: June-2022 updated palette

### Generic lines

非 scenario 多线图使用 WGI generic line colour order。超过 6 条后以 linestyle 形成第二编码。

### Continuous / discrete fields

Strict map 从官方 `IPCC-WG1/colormaps` 加载：

- `temp_seq`, `temp_div`
- `prec_seq`, `prec_div`
- `cryo_seq`, `cryo_div`
- `chem_seq`, `chem_div`
- `slev_seq`, `slev_div`
- `wind_seq`, `wind_div`
- `misc_*` 用于没有专用 variable family 的情况

```bash
git -C /path/to/IPCC-WG1/colormaps checkout b7d3849d4fa521d2583b91360e875e38f191d209
export IPCC_WG1_COLORMAPS_DIR=/path/to/IPCC-WG1/colormaps
```

```python
from ipcc_sciplot import load_ipcc_colormap
cmap = load_ipcc_colormap("temp_div")
```

## 6. Figure archetypes and layout

见 `references/figure_archetypes.md`：

- scenario time series
- ensemble centre + interval
- global/regional change map
- map matrix / small multiples
- non-scenario multi-series line comparison
- categorical/point comparison

地图 projection、central longitude 和 extent 由 reference 或 scientific context 决定。

多面板可用固定物理尺寸 grid：

```python
from ipcc_sciplot import map_panel_grid

fig, axes = map_panel_grid(
    3,
    projection=projection,
    width="double",
    height_mm=72,
)
```

可比较 panel 使用一致 scale；单位和尺度相同时共享 colour bar。

## 7. Legend / colour bar / annotation

- 优先 direct label，必要时使用 legend
- 多条线端点接近时用 `label_line_ends()` 做垂直避让
- legend / colour bar 靠近数据
- colour bar 标注单位
- legend 顺序按科学语义
- hatch、stipple、shading 在图或 caption 中给出含义

地图 uncertainty legend：

```python
from ipcc_sciplot import add_uncertainty_legend

add_uncertainty_legend(
    ax,
    low_agreement="Low agreement",
    insufficient_data="Insufficient data",
    significance="Statistically significant",
)
```

## 8. Uncertainty

三类信息分别处理：

1. ensemble agreement
2. insufficient valid models/samples
3. statistical significance

常用编码：

- high agreement：保留主数据层
- low agreement：hatch
- insufficient data：blank / neutral mask
- significance：stipple

阈值和统计量来自 target method / reference figure。80% sign agreement、17–83% range、median、equal-model weighting 不是通用 style token。

详见 `references/statistical_rules.md`。

## 9. Reproducibility and audit

绘图 workflow 可加入：

- xarray / CF / units validation
- model/member policy
- plotted-data
- provenance
- deterministic seed
- PDF/SVG + 350 ppi raster
- tests

Machine audit：

```python
from ipcc_sciplot import audit_figure

issues = audit_figure(
    fig,
    profile="ar6-report",
    strict_font=True,
    strict_dimensions=True,
    require_ipcc_colormap=True,
    reference_size_mm=(180, 92),
    reference_panel_count=3,
    reference_projection="Robinson",
)
if issues:
    raise RuntimeError("\n".join(issues))
```

## 10. Common failure modes

- SSP/RCP 使用默认 Matplotlib cycle
- strict map 使用 generic colormap fallback
- 把所有地图固定为 Robinson
- 单位写成 `[unit]`
- 把 analysis threshold 当作 style token
- 把 chapter-specific helper 泛化成 report-wide rule
- 复刻旧代码中的无关硬编码路径或 scale

## Resource index

- `references/SOURCES.md` — source corpus and hierarchy
- `references/evidence_matrix.md` — rule-by-rule evidence/scope/confidence
- `references/ipcc_visual_grammar.md` — canonical visual grammar
- `references/figure_archetypes.md` — figure-family rules
- `references/fidelity_checklist.md` — fidelity checklist
- `references/statistical_rules.md` — scientific-method rules
- `scripts/ipcc_sciplot/tokens.py` — semantic visual tokens
- `scripts/ipcc_sciplot/colormaps.py` — official palette loader
- `scripts/ipcc_sciplot/archetypes.py` — figure-family helpers
- `scripts/ipcc_sciplot/fidelity.py` — machine audit
- `templates/figure_recipe.yaml` — figure contract template
