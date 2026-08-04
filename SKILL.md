---
name: ipcc-wg1-scientific-plotting
description: 面向气候、地球系统与一般科研数据的可复现绘图工作流。将 IPCC AR6 WGI 的 FAIR、数据溯源、配置驱动样式、集合不确定性与地图稳健性表达方法，升级为现代 Python/xarray 科研绘图规范。
---

# IPCC-WG1 Scientific Plotting Skill

本 Skill 的目标不是“画得像 IPCC”，而是生成**统计含义明确、视觉编码可解释、数据与代码可追溯、可重复运行、可审计**的科研图。

## 触发条件

当任务涉及下列任一内容时使用本 Skill：

- 气候模式、再分析、遥感、观测、情景、集合或区域统计；
- NetCDF/Zarr/GRIB/CSV 数据的时间序列、地图、分布或多面板图；
- 模型一致性、置信区间、显著性、稳健性或不确定性表达；
- 期刊图、报告图、补充材料图及其可复现交付；
- 用户要求“IPCC 风格”“科学绘图”“出版级”“可复现”。

## 核心原则

1. **先定义科学问题与 estimand，再选图形。** 明确比较对象、基准期、空间/时间聚合、权重、统计量和不确定性来源。
2. **分析与渲染分离。** 原始数据 -> 规范化中间数据 -> plotted-data -> figure。绘图函数不得偷偷改变科学结果。
3. **单位、坐标、日历、缺测值显式化。** 不允许依赖文件名或变量名猜测单位；经纬度、时间日历和掩膜必须验证。
4. **集合成员不自动等价于独立样本。** 默认按模型聚合；多个 realization 是否加权必须由研究设计说明。
5. **不确定性与中心估计同时展示。** 优先效果量 + 区间；避免只标 p 值或只画均值。
6. **颜色承担数值语义，纹理承担二级信息。** 连续场用感知均匀色图；零中心变化量用发散色图；类别色不编码顺序。
7. **稳健性分类互斥且穷尽。** 不把未定义区域留给读者猜测；图注给出阈值、样本量与算法。
8. **FAIR 交付。** 每张图输出 plotted-data、参数、软件环境、输入哈希、随机种子、版本和引用信息。

## 标准工作流

### 1. 建立 figure contract

在写代码前记录：

```yaml
question: "区域年最大日降水在 2°C 全球变暖水平下如何变化？"
estimand: "每个模式的 20 年均值相对 1850-1900 的百分比变化"
unit: "%"
baseline: "1850-1900"
aggregation: "one realization per model; model-equal median"
uncertainty: "17-83% model range"
robustness: "valid models >= 5; sign agreement >= 0.80"
output: "map + plotted NetCDF + provenance JSON"
```

若上述字段不完整，先做合理假设并在图注和元数据中公开，不要隐式处理。

### 2. 数据预检

必须检查：

- 维度、坐标名、单调性、经度范围、日历类型；
- `_FillValue`/NaN、无穷值、重复时间、重复模式；
- 单位可转换性和正负号约定；
- 网格、掩膜和面积权重；
- 有效模型数是否随网格点变化；
- 基准期与目标期是否有足够覆盖。

优先使用 `xarray` 数据模型；大数据使用 Dask/Zarr；CF 元数据使用 `cf_xarray`；单位使用 `pint-xarray`；重网格化使用 `xESMF` 并保存权重文件与方法。

### 3. 统计计算

- 时间平均前明确频率、季节边界和日历。
- 全球/区域平均使用网格单元面积；规则经纬网可用 `cos(lat)` 作为近似，但应记录这一近似。
- 集合中心默认中位数或模型等权均值；二者不能混用。
- 区间必须标明分位数或置信水平，例如 17–83%、5–95%、95% CI。
- 多重检验时使用 FDR 或场显著性；考虑时间/空间自相关对有效样本量的影响。
- 稳健性遮罩必须基于实际有效样本数，而不是全局固定成员数。

本 Skill 提供：

```python
from ipcc_sciplot.uncertainty import ensemble_summary, fdr_bh_mask

summary = ensemble_summary(
    da,
    dim="model",
    center="median",
    lower_q=0.17,
    upper_q=0.83,
    sign_agreement=0.80,
    min_count=5,
)
```

### 4. 选择视觉编码

| 科学任务 | 首选图形 | 不确定性 | 禁忌 |
|---|---|---|---|
| 有序时间变化 | 线 + 区间带 | 分位带/CI | 每个成员同等粗线、双 y 轴 |
| 类别或区域比较 | 点区间图/水平条形图 | whisker/区间 | 3D、面积编码 |
| 连续空间场 | 等值填色/栅格地图 | 低一致性斜线、有效样本掩膜 | 彩虹色图、未经说明的插值 |
| 分布比较 | ECDF/violin/box + raw points | bootstrap CI | 仅均值柱形图 |
| 两变量关系 | 散点/hexbin + 模型 | 回归区间 | 暗示因果、过度平滑 |
| 组成关系 | 堆叠或 small multiples | 情景范围 | 过多扇区饼图 |

地图不确定性遵循以下默认语义：

- **无覆盖纹理**：达到预先声明的高一致性条件；
- **斜线**：低模型符号一致性；
- **灰色/空白**：有效样本不足；
- **点状纹理**：仅在确实表示统计显著性时使用。

不要用纹理遮挡最需要阅读的稳健信息；图例与图注必须解释纹理含义。

### 5. 样式与布局

```python
from ipcc_sciplot.style import publication_context, save_figure

with publication_context(width="double", font_scale=1.0):
    fig, ax = plt.subplots()
    ...
    save_figure(
        fig,
        "outputs/figure_01",
        metadata={"title": "...", "units": "K", "baseline": "1850-1900"},
    )
```

默认要求：

- 单栏宽约 89 mm，双栏宽约 183 mm；高度由信息密度决定；
- 正文字号在最终尺寸下通常不小于 7 pt；
- 轴标题写“变量名称 [单位]”或领域标准形式；
- 子图标签 `(a)`, `(b)` 固定位置；共享轴不重复标签；
- 图例按语义排序，不按代码执行顺序；
- 线型、标记、颜色至少双重编码重要类别；
- PDF/SVG 保存矢量对象，超密栅格层可 rasterize；同时输出 300 dpi PNG 预览。

### 6. 配置驱动

把场景颜色、线型、阈值、基准期和输出规格放入 YAML，而不是散落在脚本中。参考 `templates/figure_recipe.yaml`。

```python
from ipcc_sciplot.recipe import load_recipe
recipe = load_recipe("templates/figure_recipe.yaml")
```

### 7. 质量检查

运行：

```bash
python scripts/check_figure.py outputs/figure_01.pdf \
  --metadata outputs/figure_01.provenance.json
pytest -q
```

至少验证：

- 图像无裁切、重叠、不可见文字、错误透明度；
- 色图与变量语义匹配，色条包含单位；
- 图注中的阈值和代码一致；
- plotted-data 可单独重画图；
- 固定随机种子后结果一致；
- 输入哈希与 Git commit 已记录；
- 关键图进行 image-regression 测试，并允许合理的渲染器容差。

## 文件结构约定

```text
project/
  data/raw/                 # 不修改
  data/interim/             # 可重建
  data/processed/           # plotted-data
  src/analysis.py           # 统计计算
  src/figure_01.py          # 仅视觉映射
  recipes/figure_01.yaml
  outputs/figure_01.pdf
  outputs/figure_01.png
  outputs/figure_01.provenance.json
  tests/test_analysis.py
  tests/test_figure_01.py
  CITATION.cff
  environment.lock.yml
```

## 必须拒绝或修正的做法

- 用 rainbow/jet 表示连续数值；
- 截断坐标轴却不显式标记；
- 把标准差、标准误、置信区间混称为“误差”；
- 把多个模式成员当成独立重复以人为缩小不确定性；
- 用插值后的高分辨率外观暗示真实空间分辨率；
- 在地图上同时叠加过密 hatching、stippling、边界和标签；
- 只交付 PNG，不交付数据、参数和环境；
- 从旧 IPCC 脚本复制硬编码路径、版本或样式而不验证。

## 资源索引

- `references/ipcc_wg1_distillation.md`：从 IPCC-WG1 仓库抽象出的模式与升级策略。
- `references/statistical_rules.md`：集合、不确定性、显著性与空间统计规则。
- `references/visual_encoding.md`：颜色、地图、时间序列、多面板和可访问性。
- `scripts/ipcc_sciplot/`：可复用 Python 模块。
- `templates/figure_recipe.yaml`：声明式绘图配方。
- `examples/quickstart.py`：合成数据完整示例。
