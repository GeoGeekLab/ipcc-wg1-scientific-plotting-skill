from pathlib import Path

import numpy as np
import pytest

import ipcc_sciplot.colormaps as colormaps
from ipcc_sciplot.colormaps import (
    load_ipcc_colormap,
    official_colormap_root,
    verify_official_colormap_asset,
)


def test_strict_loader_requires_root(monkeypatch):
    monkeypatch.delenv("IPCC_WG1_COLORMAPS_DIR", raising=False)
    with pytest.raises(FileNotFoundError):
        official_colormap_root()


def test_local_official_layout_loads(tmp_path: Path):
    target = tmp_path / "continuous_colormaps_rgb_0-255"
    target.mkdir()
    np.savetxt(target / "temp_div.txt", np.array([[0, 0, 255], [255, 255, 255], [255, 0, 0]]))
    cmap = load_ipcc_colormap(
        "temp_div",
        root=tmp_path,
        register=False,
        verify=False,
    )
    assert cmap.name == "ipcc_temp_div"



def test_asset_verification_accepts_expected_blob(tmp_path: Path, monkeypatch):
    target = tmp_path / "continuous_colormaps_rgb_0-255"
    target.mkdir()
    path = target / "temp_div.txt"
    path.write_text("0 0 255\n255 255 255\n255 0 0\n", encoding="utf-8")
    expected = colormaps._normalized_git_blob_sha(path)
    monkeypatch.setitem(
        colormaps.OFFICIAL_COLORMAP_BLOBS,
        "continuous_colormaps_rgb_0-255/temp_div.txt",
        expected,
    )

    assert verify_official_colormap_asset("temp_div", root=tmp_path) == path


def test_asset_verification_rejects_drift(tmp_path: Path):
    target = tmp_path / "continuous_colormaps_rgb_0-255"
    target.mkdir()
    path = target / "temp_div.txt"
    path.write_text("0 0 0\n255 255 255\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="differs from"):
        verify_official_colormap_asset("temp_div", root=tmp_path)
