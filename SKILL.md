---
name: ipcc-wg1-scientific-plotting
description: 高保真蒸馏 IPCC AR6 Working Group I 的科学图形语言。基于 WGI Visual Style Guide、官方 colormaps、AR6 章节绘图代码、TSU 审图意见与 Atlas 不确定性框架，生成或审查 IPCC-faithful / IPCC-inspired 科研图。
---

# IPCC AR6 WGI Scientific Plotting Skill

本 Skill 的首要目标是保真复现 IPCC AR6 WGI 的 visual grammar，而不是把一般“出版级科研绘图”包装成 IPCC 风格。

科研统计、FAIR、provenance 和现代 Python 工作流仍然重要，但属于第二层；视觉保真必须有独立证据和独立 QA。

## 何时触发

当用户要求以下任一任务时使用：

- “IPCC 风格”“AR6 WGI 风格”“像 IPCC 报告图”；
- 复刻某张 AR6 WGI figure；
- 气候模式/情景/观测/再分析图，需要使用 IPCC scenario colours；
- WGI 风格地图、时间序列、多面板、不确定性表达；
- 审查科研图是否符合 IPCC visual style。

## 1. 选择 fidelity mode

### Strict / IPCC-faithful

用户明确要求 IPCC/AR6/WGI 风格时默认使用。

必须满足：

- 选定 ar6-report 或 wgi-guide-2022 profile；
- Arial 可用；
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

## 2. 证据层级

规则冲突时按以下优先级：

1. WGI Visual Style Guide（June 2022）；
2. WGI TSU 审图意见中反复执行的规则；
3. 官方 IPCC-WG1/colormaps；
4. 最终 AR6 章节 figure code / helper；
5. Atlas uncertainty guidance；
6. 一般科研可视化最佳实践。

单个章节的偶然实现不能自动升级为 WGI 全局规范。详见 references/SOURCES.md。

## 3. 建立 figure contract

绘图前必须明确：

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
    uncertainty: 17-83% model range
    robustness: sign agreement >= 0.80
    min_valid_count: 5

如果复刻具体 AR6 figure，还必须记录 chapter / figure number，并优先匹配该图的 projection、extent、panel geometry、levels、annotation 和 legend grammar。

## 4. 硬视觉规则

### Typography

- Strict mode 使用 Arial。
- 单位写成 Variable (unit)，不用 Variable [unit]。
- 温度变化面向 WGI 一般读者时优先 °C；有科学理由时才用 K。
- 陌生缩写首次出现尽量展开。
- Panel label 用 (a), (b) 等，位置一致。
- 短标题帮助第一眼理解 panel，不重复长 caption。

示例：

    from ipcc_sciplot import axis_label, panel_label, publication_context

    with publication_context(width="double", strict_font=True):
        ax.set_ylabel(axis_label("Temperature change", "°C"))
        panel_label(ax, "a", title="Global mean")

### Scenario colours

Scenario colour 是语义，不是 decoration。

    from ipcc_sciplot import scenario_style

    scenario_style("SSP2-4.5", profile="ar6-report")
    scenario_style("SSP2-4.5", profile="wgi-guide-2022")

ar6-report 用于匹配 2021 final-report-era figure/code；wgi-guide-2022 使用更新后的 2022 WGI guide palette。禁止静默混合。

### Generic lines

非 scenario 多线图使用 WGI generic line colour order。超过 6 条后复用颜色并增加 linestyle 区分，不要不断引入新的亮色。

### Continuous / discrete fields

Strict map 必须从官方 IPCC-WG1/colormaps 加载：

- temp_seq, temp_div
- prec_seq, prec_div
- cryo_seq, cryo_div
- chem_seq, chem_div
- slev_seq, slev_div
- wind_seq, wind_div
- misc_* 仅在没有物理量专用 family 时使用

设置：

    export IPCC_WG1_COLORMAPS_DIR=/path/to/IPCC-WG1/colormaps

调用：

    from ipcc_sciplot import load_ipcc_colormap
    cmap = load_ipcc_colormap("temp_div")

缺少官方 asset 时 strict mode 必须失败，不能自动换成 RdBu_r / viridis / cmocean 后仍声称 IPCC fidelity。

## 5. Figure archetypes

先选 figure family，再渲染。详见 references/figure_archetypes.md。

核心 archetypes：

- scenario time series；
- ensemble centre + interval；
- global/regional change map；
- map matrix / small multiples；
- non-scenario multi-series line comparison；
- categorical/point comparison（只有 report-wide grammar，没有唯一 layout）。

不要把所有图强行套成一套 “IPCC theme”。

## 6. Maps

没有一个全局默认的 “IPCC projection”。

- 复刻具体图：匹配 reference figure 的 projection/central longitude/extent。
- 新图：根据科学任务选择，并在 recipe 中显式记录。
- geographic context 必须弱于 data layer。
- land/context 常用克制的 grey；边界细。
- colour bar 必须包含单位。
- comparable panels 的 scale 不得悄悄变化。

### Robustness layers

必须分开：

1. high/low ensemble sign agreement；
2. insufficient valid models/samples；
3. statistical significance。

默认语义：

- robust/high agreement：保持主数据层干净；
- low agreement：可用 hatch；
- insufficient data：独立 blank/neutral mask；
- statistical significance：只有真正对应显著性检验时才用 stipple。

禁止同一种 hatch 同时表示 disagreement、missing data 和 significance。

## 7. Legends / colour bars / annotation

- 能直接标注时优先 direct label。
- 使用 legend 时按科学语义排序，不按代码调用顺序。
- legend / colour bar 靠近数据。
- colour bar 给出单位。
- 图上出现但不属于 colour bar 的颜色、shading、hatch、stipple 必须解释。
- 避免不必要 grid、frame 和视觉装饰。

## 8. Uncertainty

- 中心估计和 uncertainty 同时表达。
- interval 必须具体命名：17–83%、5–95%、95% CI 等。
- 不要把 SD、SE、CI、model range 统一叫 “error”。
- model agreement threshold 是科学方法的一部分，不是样式参数。
- 多 realization 不自动等价于独立模型。
- texture 不得淹没最重要的 robust signal。

统计细节见 references/statistical_rules.md。

## 9. Multi-panel

- 排列编码科学逻辑，不按 loop 顺序。
- 同单位同尺度的可比较 panel 才共享 colour bar。
- panel label/title 位置一致。
- 不要为了塞进版面把地图缩到不可读。
- uncertainty overlay 语义在所有 panel 中一致。

## 10. Reproducibility layer

视觉映射确定之后，再应用：

- xarray / CF / unit validation；
- model/member policy；
- plotted-data；
- provenance；
- deterministic seed；
- PDF/SVG + PNG；
- tests。

这些增强可审计性，但不能替代视觉 style distillation。

## 11. Fidelity gate

输出前按 references/fidelity_checklist.md 检查。

至少运行：

    warnings = audit_text_conventions(fig)
    if warnings:
        raise RuntimeError("\n".join(warnings))

严格模式还要人工/视觉核对：

- semantic colours；
- official colormap；
- font；
- panel geometry；
- projection/extent；
- legend/colorbar；
- uncertainty semantics；
- 与 reference figure 的差异（如果有）。

## 禁止

- 把 IPCC-inspired 写成 IPCC-faithful；
- strict mode 用默认 Matplotlib colour cycle 表示 SSP/RCP；
- strict map fallback 到 RdBu_r / viridis / cmocean；
- 所有地图默认 Robinson；
- 单位使用 [ ]；
- 只因为使用 hatch 就声称遵循 IPCC uncertainty method；
- 把某个 chapter helper 的局部规则冒充全报告规范；
- 用 FAIR/provenance/300 dpi 代替视觉保真；
- 复制旧图的错误、硬编码路径或无依据的 scale。

## Resource index

- references/SOURCES.md — evidence hierarchy and primary source corpus
- references/ipcc_visual_grammar.md — canonical distilled visual grammar
- references/figure_archetypes.md — figure-family rules
- references/fidelity_checklist.md — strict fidelity gate
- references/statistical_rules.md — ensemble/statistical rules
- scripts/ipcc_sciplot/tokens.py — semantic visual tokens
- scripts/ipcc_sciplot/colormaps.py — official palette loader
- scripts/ipcc_sciplot/archetypes.py — reusable figure-family helpers
- templates/figure_recipe.yaml — strict figure contract template
