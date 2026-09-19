from __future__ import annotations

import os
from pathlib import Path
from typing import Final

import matplotlib as mpl
import matplotlib.colors as mcolors
import numpy as np

OFFICIAL_COLORMAP_REPOSITORY: Final[str] = "https://github.com/IPCC-WG1/colormaps"

OFFICIAL_CONTINUOUS_FILES: Final[dict[str, str]] = {
    name: f"continuous_colormaps_rgb_0-255/{name}.txt"
    for name in (
        "chem_div", "chem_seq", "cryo_div", "cryo_seq", "misc_div",
        "misc_seq_1", "misc_seq_2", "misc_seq_3", "prec_div", "prec_seq",
        "slev_div", "slev_seq", "temp_div", "temp_seq", "wind_div", "wind_seq",
    )
}
OFFICIAL_DISCRETE_FILES: Final[dict[str, str]] = {
    name: f"discrete_colormaps_rgb_0-255/{name}.txt"
    for name in (
        "chem_div_disc", "chem_seq_disc", "cryo_div_disc", "cryo_seq_disc",
        "misc_div_disc", "misc_seq_1_disc", "misc_seq_2_disc", "misc_seq_3_disc",
        "prec_div_disc", "prec_seq_disc", "slev_div_disc", "slev_seq_disc",
        "temp_div_disc", "temp_seq_disc", "wind_div_disc", "wind_seq_disc",
    )
}
OFFICIAL_CATEGORICAL_FILES: Final[dict[str, str]] = {
    name: f"categorical_colors_rgb_0-255/{name}.txt"
    for name in (
        "bright_cat", "chem_cat", "cmip_cat", "contrast_cat", "dark_cat",
        "gree-blue_cat", "rcp_cat", "red-yellow_cat", "spectrum_cat",
        "ssp_cat_1", "ssp_cat_2",
    )
}


def official_colormap_root(root: str | Path | None = None) -> Path:
    candidate = root or os.environ.get("IPCC_WG1_COLORMAPS_DIR")
    if not candidate:
        raise FileNotFoundError(
            "IPCC colormap assets are required for faithful mode. "
            "Set IPCC_WG1_COLORMAPS_DIR to a local checkout of "
            f"{OFFICIAL_COLORMAP_REPOSITORY}."
        )
    path = Path(candidate).expanduser().resolve()
    if not path.is_dir():
        raise FileNotFoundError(path)
    return path


def _read_rgb(path: Path) -> np.ndarray:
    data = np.loadtxt(path)
    if data.ndim != 2 or data.shape[1] not in (3, 4):
        raise ValueError(f"invalid RGB table: {path}")
    if not np.isfinite(data).all():
        raise ValueError(f"non-finite RGB value in {path}")
    scale = 255.0 if float(data.max()) > 1.0 else 1.0
    data = data / scale
    if (data < 0).any() or (data > 1).any():
        raise ValueError(f"RGB value outside valid range in {path}")
    return data


def load_ipcc_colormap(
    name: str,
    *,
    root: str | Path | None = None,
    reverse: bool = False,
    register: bool = True,
) -> mcolors.Colormap:
    """Load an official AR6 WGI colour asset by semantic filename."""
    table = {
        **OFFICIAL_CONTINUOUS_FILES,
        **OFFICIAL_DISCRETE_FILES,
        **OFFICIAL_CATEGORICAL_FILES,
    }
    try:
        relative = table[name]
    except KeyError as exc:
        raise KeyError(f"unknown official IPCC colormap {name!r}") from exc

    path = official_colormap_root(root) / relative
    if not path.is_file():
        raise FileNotFoundError(
            f"missing official colormap asset: {path}. "
            f"Refresh the checkout from {OFFICIAL_COLORMAP_REPOSITORY}."
        )
    data = _read_rgb(path)
    if reverse:
        data = data[::-1]

    cmap_name = f"ipcc_{name}" + ("_r" if reverse else "")
    categorical = name.endswith("_cat") or name.startswith(("ssp_cat_", "rcp_cat"))
    if "_disc" in name or categorical:
        cmap: mcolors.Colormap = mcolors.ListedColormap(data[:, :3], name=cmap_name)
    else:
        cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, data[:, :3])

    if register:
        try:
            mpl.colormaps.register(cmap, name=cmap_name, force=True)
        except TypeError:
            if cmap_name not in mpl.colormaps:
                mpl.colormaps.register(cmap, name=cmap_name)
    return cmap
