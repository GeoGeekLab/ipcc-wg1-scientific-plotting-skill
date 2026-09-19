from pathlib import Path

import numpy as np
import pytest

from ipcc_sciplot.colormaps import load_ipcc_colormap, official_colormap_root


def test_strict_loader_requires_root(monkeypatch):
    monkeypatch.delenv("IPCC_WG1_COLORMAPS_DIR", raising=False)
    with pytest.raises(FileNotFoundError):
        official_colormap_root()


def test_local_official_layout_loads(tmp_path: Path):
    target = tmp_path / "continuous_colormaps_rgb_0-255"
    target.mkdir()
    np.savetxt(target / "temp_div.txt", np.array([[0, 0, 255], [255, 255, 255], [255, 0, 0]]))
    cmap = load_ipcc_colormap("temp_div", root=tmp_path, register=False)
    assert cmap.name == "ipcc_temp_div"
