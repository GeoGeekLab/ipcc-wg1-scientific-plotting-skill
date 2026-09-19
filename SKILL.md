---
name: ipcc-wg1-scientific-plotting
description: 高保真蒸馏 IPCC AR6 Working Group I 的科学图形语言。基于 WGI Visual Style Guide、官方 colormaps、AR6 章节绘图代码、TSU 审图意见与 Atlas 不确定性框架，生成或审查 IPCC-faithful / IPCC-inspired 科研图。
---

# IPCC AR6 WGI Scientific Plotting Skill

本 Skill 的首要目标是保真复现 IPCC AR6 WGI 的 visual grammar，而不是把一般“出版级科研绘图”包装成 IPCC 风格。

科研统计、FAIR、provenance 和现代 Python 工作流仍然重要，但属于第二层；视觉保真必须有独立证据和独立 QA。

## 1. 先确定 fidelity mode

### Strict / IPCC-faithful

用户明确要求 IPCC/AR6/WGI 风格时默认使用。

必须满足：

- 选定 `ar6-report` 或 `wgi-guide-2022` profile；
- Arial 可用；
- IPCC print geometry 使用 90 mm / 180 mm 宽度，最大高度 250 mm；
- SSP/RCP 使用语义颜色；
- 地图使用官方 WGI colormap asset；
- 地图投影显式指定；
- 单位使用圆括号；
- uncertainty/agreement/significance/missing-data 语义分离；
- 不允许静默 fallback 到 Matplotlib/cmocean palette；
- 输出前执行 fidelity checklist。

关键项无法满足时，不能把结果称为 IPCC-faithful。

### Adapted / IPCC-inspired

只有在用户接受近似，或缺少必要资产/参考图时使用。允许字体、palette 或布局替代，但必须明确称为 IPCC-inspired/adapted。

## 2. 证据优先，不靠“感觉像”

如果复刻具体 AR6 figure，**published reference figure 本身优先**。其次使用该时期的 WGI visual guide、TSU 审图证据、官方 colour assets、chapter code 和 Atlas uncertainty guidance。

如果创建新图并明确采用更新版规范，使用 `wgi-guide-2022`。

不要用 2022 更新后的 SSP 色值去“纠正”2021 final-report figure。完整 evidence hierarchy 与逐规则强度见：

- `references/SOURCES.md`
- `references/evidence_matrix.md`

## 3. 建立 figure contract

绘图前至少明确：

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

示例里的 interval/agreement 值只是占位，不能因为“IPCC style”就自动采用 17–83% 或 80%。

复刻具体图时还要记录 chapter / figure number，并匹配 projection、extent、panel geometry、levels、annotation、legend 和 scientific method。

## 4. IPCC delivery geometry / typography

AR6 WGI visual guide 的 print delivery grammar：

- single column: **9 cm**
- double column: **18 cm**
- maximum height: **25 cm**
- smaller figure text: about **9 pt**
- larger figure text: about **11 pt**
- black axes: **0.5 pt**
- print raster: **350 ppi**
- strict font: **Arial**
- units: `Variable (unit)`，不用 `Variable [unit]`

避免不必要的 bold/italic/underline、grid、frame 和装饰。

```python
from ipcc_sciplot import axis_label, panel_label, publication_context

with publication_context(width="double", strict_font=True):
    ax.set_ylabel(axis_label("Temperature change", "°C"))
    panel_label(ax, "a", title="Global mean")
```

## 5. Colour 是语义，不是 decoration

### Scenario colours

```python
from ipcc_sciplot import scenario_style

scenario_style("SSP2-4.5", profile="ar6-report")
scenario_style("SSP2-4.5", profile="wgi-guide-2022")
```

- `ar6-report`：匹配 final-report-era figure/code。
- `wgi-guide-2022`：使用 June-2022 updated palette。

禁止静默混合。

### Generic lines

非 scenario 多线图使用 WGI generic line colour order。超过 6 条后复用颜色并用 linestyle 形成第二编码。数据线粗不是全报告统一 token；应匹配 reference/archetype，并保持不低于可读 delivery requirement。

### Continuous / discrete fields

Strict map 从官方 `IPCC-WG1/colormaps` 加载：

- `temp_seq`, `temp_div`
- `prec_seq`, `prec_div`
- `cryo_seq`, `cryo_div`
- `chem_seq`, `chem_div`
- `slev_seq`, `slev_div`
- `wind_seq`, `wind_div`
- `misc_*` 仅在没有物理量专用 family 时使用

```bash
export IPCC_WG1_COLORMAPS_DIR=/path/to/IPCC-WG1/colormaps
```

```python
from ipcc_sciplot import load_ipcc_colormap
cmap = load_ipcc_colormap("temp_div")
```

缺少官方 asset 时 strict mode 必须失败。禁止自动换成 `RdBu_r` / `viridis` / cmocean 后仍声称 IPCC fidelity。

## 6. Figure archetypes，而不是一个“theme”

详见 `references/figure_archetypes.md`：

- scenario time series
- ensemble centre + interval
- global/regional change map
- map matrix / small multiples
- non-scenario multi-series line comparison
- categorical/point comparison

没有一个全局默认的 “IPCC projection”。复刻具体图时，projection/central longitude/extent 以 reference 为准。

## 7. Legend / colour bar / annotation

- 能直接标注时优先 direct label。
- separate legend / colour bar 靠近数据，优先放在 plot 内可用 white space。
- 独立 legend / colour bar 使用克制的 black 0.5 pt boundary。
- colour bar 必须给单位。
- 所有额外颜色、shading、hatch、stipple 都必须解释。
- legend 顺序按科学语义，不按代码调用顺序。

## 8. Uncertainty：视觉语义与统计方法分离

必须分开：

1. high/low ensemble agreement
2. insufficient valid models/samples
3. statistical significance

可用的视觉语法：

- robust/high agreement：主数据层保持干净；
- low agreement：方法允许时用 hatch；
- insufficient data：独立 blank/neutral mask；
- significance：只有真正对应显著性检验时才用 stipple。

**80% sign agreement、17–83% range、median、equal-model weighting 都不是 IPCC-wide visual defaults。** 它们必须来自 target method / reference figure。详见 `references/statistical_rules.md`。

## 9. Multi-panel

- panel 排列编码科学逻辑，不按 loop 顺序；
- 可比较 panel 使用一致 scale；
- 只有单位/尺度真正相同时共享 colour bar；
- panel label/title 位置一致；
- 不要为了塞进版面把 map 缩到不可读。

## 10. Reproducibility 是第二层

视觉映射确定后，再应用：

- xarray / CF / units validation
- model/member policy
- plotted-data
- provenance
- deterministic seed
- PDF/SVG + 350 ppi print raster
- tests

这些增强可审计性，但不能替代 style fidelity。

## 11. Fidelity gate

输出前调用 machine-checkable audit，并执行人工 checklist。

```python
from ipcc_sciplot import audit_figure

issues = audit_figure(
    fig,
    profile="ar6-report",
    strict_font=True,
    strict_dimensions=True,
    require_ipcc_colormap=True,  # map only
)
if issues:
    raise RuntimeError("\n".join(issues))
```

机器 audit 不能判断 reference-specific projection、panel geometry、annotation 和 scientific method。复刻具体 AR6 figure 时仍必须视觉对照。

## 禁止

- 把 IPCC-inspired 写成 IPCC-faithful；
- strict mode 用默认 Matplotlib cycle 表示 SSP/RCP；
- strict map fallback 到 generic colormap；
- 所有 map 默认 Robinson；
- 单位使用 `[ ]`；
- 把 80%、17–83%、median 等 analysis choice 冒充 IPCC style；
- 用 FAIR/provenance/350 dpi 单独证明“IPCC 风格”；
- 把单个 chapter helper 的局部实现冒充 report-wide rule；
- 复制旧图中的错误、硬编码路径或无依据 scale。

## Resource index

- `references/SOURCES.md` — source corpus and hierarchy
- `references/evidence_matrix.md` — rule-by-rule evidence/scope/confidence
- `references/ipcc_visual_grammar.md` — canonical visual grammar
- `references/figure_archetypes.md` — figure-family rules
- `references/fidelity_checklist.md` — strict fidelity gate
- `references/statistical_rules.md` — scientific-method separation
- `scripts/ipcc_sciplot/tokens.py` — semantic visual tokens
- `scripts/ipcc_sciplot/colormaps.py` — official palette loader
- `scripts/ipcc_sciplot/archetypes.py` — figure-family helpers
- `scripts/ipcc_sciplot/fidelity.py` — machine audit
- `templates/figure_recipe.yaml` — figure contract template
