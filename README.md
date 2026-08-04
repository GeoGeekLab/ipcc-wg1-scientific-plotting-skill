# IPCC-WG1 Scientific Plotting Skill

这是一个从 IPCC AR6 Working Group I 公开仓库中提炼并现代化的科研绘图 Skill。它不是 IPCC 官方产品，也不复制或重新分发 IPCC 代码/颜色数据。

## 快速使用

```bash
cd ipcc-wg1-scientific-plotting-skill
python -m venv .venv
source .venv/bin/activate
pip install -e .[qa]
python examples/quickstart.py
pytest
```

气候地图全栈：

```bash
pip install -e .[climate,qa,workflow]
```

主说明见 `SKILL.md`。
