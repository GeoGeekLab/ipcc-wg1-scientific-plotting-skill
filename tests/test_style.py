from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ipcc_sciplot.style import publication_context, register_rgb_colormap, save_figure


def test_register_rgb_colormap(tmp_path: Path):
    path = tmp_path / "cmap.txt"
    np.savetxt(path, np.array([[0, 0, 0], [255, 255, 255]]), fmt="%d")
    cmap = register_rgb_colormap(path, name="unit_test_cmap")
    assert cmap.name == "unit_test_cmap"


def test_save_figure(tmp_path: Path):
    with publication_context():
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1])
        paths = save_figure(fig, tmp_path / "figure", close=True)
    assert {p.suffix for p in paths} == {".pdf", ".png"}
    assert all(p.stat().st_size > 0 for p in paths)
