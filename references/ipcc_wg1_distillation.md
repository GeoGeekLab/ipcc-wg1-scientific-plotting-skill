# IPCC-WG1 方法蒸馏与现代化

## 观察到的可迁移模式

### 1. 图、代码、数据和引用绑定

IPCC-WG1 组织按章节和图号组织大量仓库。多个仓库将最终图、绘图代码、plotted-data、环境文件及 Zenodo/CEDA 引用绑定在一起。这比单独保存图片更接近可审计科研交付。

**蒸馏规则**：每张图是一个可独立运行、可引用的计算产品；至少包含 recipe、plotted-data、figure、provenance 和 citation。

### 2. FAIR 与数据溯源

Atlas 仓库强调 Findable、Accessible、Interoperable、Reusable，并用公开仓库、注释 notebook、聚合数据和 provenance 支撑重用。

**现代化**：

- 计算过程用脚本/工作流，notebook 主要承担解释和探索；
- 输入文件记录 URI、DOI、版本、SHA-256、获取时间和许可证；
- 中间数据使用 CF-compliant NetCDF/Zarr；
- 输出同时写 JSON provenance 与机器可读 plotted-data；
- 发布版本使用不可变 tag 和 DOI。

### 3. 配置驱动的语义样式

Chapter-6_Fig19 用 YAML 将 SSP 颜色和数据类型线型从绘图代码中分离，并用 `pyam` 映射场景语义。

**现代化**：

- 将颜色、线型、统计阈值、基准期、排序和输出规格统一放入 recipe；
- recipe 通过 schema 验证；
- 颜色键是语义标识符，不是 RGB 常量散落在函数中；
- 重要类别同时编码颜色与线型/标记。

### 4. 气候数据栈与大数据

Chapter 11 的环境覆盖 xarray、Dask、Cartopy、regionmask、xESMF、xclim、Zarr、统计和测试工具；部分图需要约 TB 级数据。Chapter-2_Fig31 也明确并行处理和内存约束。

**现代化**：

- xarray 作为统一数据模型；
- Dask 仅在 chunk 设计合理时启用；在绘图前 `.compute()` 小型 plotted-data；
- Zarr 用于云/并行中间数据，NetCDF 用于稳定交换；
- regionmask 管理区域；xESMF 保存重网格权重与守恒方法；
- 先降维再绘图，禁止把 TB 级原始数据直接传给 Matplotlib。

### 5. 不确定性与模型一致性

AR6 多幅地图采用“简单方法”：高模型符号一致性区域不覆盖，低一致性区域用斜线；具体阈值常为 80%，并要求图注解释。某些图使用 5–95% 或 17–83% 范围。

**蒸馏规则**：

- 阈值不是装饰参数，而是科学方法的一部分；
- 计算每个网格点的有效模型数；
- 符号一致性按相对零或明确参考值计算；
- 中心估计、范围、低一致性和样本不足是四个独立图层；
- “显著性”与“模型一致性”不能混为一谈。

### 6. 多语言遗产与可重复环境

组织包含 Python、R、MATLAB、NCL、IDL、Fortran 等。旧仓库经常锁定早期软件版本或依赖 HPC 目录。

**现代化**：

- 保留科学算法，重写 I/O、配置、测试和环境；
- 不把旧版本环境当作最佳实践；
- 用 Python 3.11+、类型标注、Ruff、pytest 和 lockfile；
- 外部程序（CDO/NCO/ESMValTool）通过明确命令和版本调用；
- 所有路径相对项目根目录或由配置注入。

## 不应直接复制的部分

- 硬编码的绝对路径、图号、字体、坐标范围；
- 未解释的手工 y-limit 或 scale factor；
- 依赖 notebook cell 顺序的状态；
- 仅对某台 HPC 主机有效的启动脚本；
- 缺少许可证时的颜色表或代码文件再分发；
- 过时版本约束。

## 本 Skill 的升级架构

```text
Scientific question
  -> figure contract
  -> validated dataset
  -> explicit statistical transform
  -> compact plotted-data
  -> declarative visual mapping
  -> vector/raster outputs
  -> provenance + QA + citation
```

此架构保留 IPCC-WG1 的透明性与气候领域语义，同时用现代软件工程降低复现成本。
