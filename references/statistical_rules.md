# 统计与不确定性规则

## 集合统计

设网格点或时间点上的模式变化为 `x_m`。

- 中心：默认 `median_m(x_m)`；采用 mean 时说明原因。
- 分位区间：`Q_lower` 到 `Q_upper`，例如 0.17–0.83 或 0.05–0.95。
- 有效数量：`n_valid = sum(isfinite(x_m))`。
- 符号一致性：

```text
p_pos = count(x_m > reference) / n_valid
p_neg = count(x_m < reference) / n_valid
agreement = max(p_pos, p_neg)
```

- 低一致性：`agreement < threshold`。
- 样本不足：`n_valid < min_count`，优先级高于一致性分类。

零值的处理必须声明。默认零值既不支持正号也不支持负号，但仍进入有效数量；可通过 tolerance 将极小值视为零。

## 模型与成员权重

- 默认一模型一票，避免成员数多的模式获得隐式高权重。
- 若使用多个 realization，先在模型内聚合，再在模型间聚合。
- 性能权重或独立性权重必须预先定义，并做敏感性分析。
- 情景集合不是概率分布，不能把 scenario spread 解释为概率区间。

## 时间序列

- 趋势估计前检查自相关、非平稳性和断点。
- OLS 置信区间在残差自相关明显时通常过窄；考虑 HAC、GLS、block bootstrap 或明确的时间序列模型。
- 平滑线必须公开窗口/带宽；原始信息不应被完全隐藏。
- 多条模式轨迹可用浅色细线作为背景，但主视觉应是中心与范围。

## 空间显著性

逐格 p 值会产生多重检验问题。默认流程：

1. 计算每格效果量与检验统计量；
2. 检查检验假设；
3. 对有效格点使用 Benjamini–Hochberg FDR；
4. 对空间自相关强的数据，补充 field significance、置换或空间 block bootstrap；
5. 将显著性纹理与模型一致性纹理分离。

`fdr_bh_mask` 只实现标准 BH 步骤，不自动解决空间依赖问题。

## 区域与全球平均

规则经纬网近似权重：

```python
weights = np.cos(np.deg2rad(lat))
mean = da.weighted(weights).mean(("lat", "lon"))
```

对于非规则网格、旋转网格、海岸线或网格面积差异明显的情况，使用真实 cell area。区域掩膜应与网格对齐，面积分数掩膜优于中心点二值掩膜。

## 缺测值

- 缺测不是零；
- 每个统计量报告有效数量；
- 对不同变量/情景比较时检查是否使用相同样本集合；
- 完整案例分析会改变估计对象，必须说明；
- 插补值和观测值应可区分，不能只在代码中知道。
