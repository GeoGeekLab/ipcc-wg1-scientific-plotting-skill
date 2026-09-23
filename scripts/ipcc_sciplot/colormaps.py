from __future__ import annotations

import hashlib
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Final

import matplotlib as mpl
import matplotlib.colors as mcolors
import numpy as np

OFFICIAL_COLORMAP_REPOSITORY: Final[str] = "https://github.com/IPCC-WG1/colormaps"
OFFICIAL_COLORMAP_COMMIT: Final[str] = "b7d3849d4fa521d2583b91360e875e38f191d209"

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

OFFICIAL_COLORMAP_BLOBS: Final[dict[str, str]] = {
    "continuous_colormaps_rgb_0-255/chem_div.txt": "db287d56f1231fe763b73bc73e083395894308e0",
    "continuous_colormaps_rgb_0-255/chem_seq.txt": "ccba3745eb2c6c7138a38c56a4de584841932505",
    "continuous_colormaps_rgb_0-255/cryo_div.txt": "6ae1ac864a854b31b6cabc2eaa8ca83612f87d76",
    "continuous_colormaps_rgb_0-255/cryo_seq.txt": "25effe81e67672cdd61e261b1d91427f3b967f28",
    "continuous_colormaps_rgb_0-255/misc_div.txt": "24fa51f7b13e0dd5840548777769c0a16db66f0e",
    "continuous_colormaps_rgb_0-255/misc_seq_1.txt": "12ebafdd92115dafde2594813074c63bd54edb21",
    "continuous_colormaps_rgb_0-255/misc_seq_2.txt": "4eb216e18647cb2bcf4caf41243410cd91461151",
    "continuous_colormaps_rgb_0-255/misc_seq_3.txt": "7083bee5203e47529aa9fc3034bdb0a2168acc57",
    "continuous_colormaps_rgb_0-255/prec_div.txt": "2469424d9a416ef1ed67ed808f64f433ecea069a",
    "continuous_colormaps_rgb_0-255/prec_seq.txt": "50018d4a2a7745c25336ad58fbbd4397e3f1b5ac",
    "continuous_colormaps_rgb_0-255/slev_div.txt": "eb359bbe6218088e2c67ecdfee4437f8ff4f85e0",
    "continuous_colormaps_rgb_0-255/slev_seq.txt": "83b35c0cea3c36f5bcb50513b31a7306212511f1",
    "continuous_colormaps_rgb_0-255/temp_div.txt": "1469ecd5690d4b057360c8ad031dfbeb3be2f54e",
    "continuous_colormaps_rgb_0-255/temp_seq.txt": "03c3745b663c17f2618900d9eeb4a74e5162c82a",
    "continuous_colormaps_rgb_0-255/wind_div.txt": "05eb8387c24856ab92274e96fa1ccf7463e3fc01",
    "continuous_colormaps_rgb_0-255/wind_seq.txt": "13c53fad450d05ca75baa38780a93d42e6741fc2",
    "discrete_colormaps_rgb_0-255/chem_div_disc.txt": "afdee5329fad30a732ef2dd6af1884528c514462",
    "discrete_colormaps_rgb_0-255/chem_seq_disc.txt": "da1d34f0bcd97664bf26a22e44b1095407d700f0",
    "discrete_colormaps_rgb_0-255/cryo_div_disc.txt": "fecc22416a0e57040323dcb3c72e02d76dcd6ab8",
    "discrete_colormaps_rgb_0-255/cryo_seq_disc.txt": "b47a3ab60a492d689d1196ce724b2890e36f1886",
    "discrete_colormaps_rgb_0-255/misc_div_disc.txt": "b78db7a95bf3ca0239e459cdfe693acb2cc61245",
    "discrete_colormaps_rgb_0-255/misc_seq_1_disc.txt": "9e93a3ee7fa49680f7697ba4c35d5275f1b534d3",
    "discrete_colormaps_rgb_0-255/misc_seq_2_disc.txt": "e1613d68244f680af87ba5069f15c94cd4a7cdc0",
    "discrete_colormaps_rgb_0-255/misc_seq_3_disc.txt": "610e8e1429d69a034bd7debe2b8605aa5df21d51",
    "discrete_colormaps_rgb_0-255/prec_div_disc.txt": "3d7e6e9feb17159434c9fcf56edf3cf544115c3c",
    "discrete_colormaps_rgb_0-255/prec_seq_disc.txt": "2b8d240c4c40b35a9325558dc65f78ee41306f25",
    "discrete_colormaps_rgb_0-255/slev_div_disc.txt": "4f1203517ae95a348f4018c959928e5700244bc2",
    "discrete_colormaps_rgb_0-255/slev_seq_disc.txt": "e2644ce4b5bac6004d019f5f20cfe365cfd38d6c",
    "discrete_colormaps_rgb_0-255/temp_div_disc.txt": "8cddf21bfe395660998e098b5f24421e8a2f54e5",
    "discrete_colormaps_rgb_0-255/temp_seq_disc.txt": "b28bab320eb2fdd3b48228672836b0400001f539",
    "discrete_colormaps_rgb_0-255/wind_div_disc.txt": "e010a5250ae6375a1370742cb80496b1b18285ba",
    "discrete_colormaps_rgb_0-255/wind_seq_disc.txt": "26d49b63b44d5e1d2e8ce4450569acb9554c626d",
    "categorical_colors_rgb_0-255/bright_cat.txt": "c066f983eb1f63b20ca08c5ca1485b2452729f62",
    "categorical_colors_rgb_0-255/chem_cat.txt": "a4ad4a43fcddcaaf3f090e24c5250956b0ce238f",
    "categorical_colors_rgb_0-255/cmip_cat.txt": "0c4596e8718c253b39b5995d189bf37785e98e08",
    "categorical_colors_rgb_0-255/contrast_cat.txt": "246b4166dcae80047afcb630a73fe9d37c59224c",
    "categorical_colors_rgb_0-255/dark_cat.txt": "14ac5925bc86dfd94593bca724ca948d37d14ca1",
    "categorical_colors_rgb_0-255/gree-blue_cat.txt": "208a34d98f00b2f07404266ace6152317c0bbfa2",
    "categorical_colors_rgb_0-255/rcp_cat.txt": "087b9ae9e20a0518c8aef0384ea0215a863a7549",
    "categorical_colors_rgb_0-255/red-yellow_cat.txt": "4557d20542d1923a58d7670e90b11438a6fefc8a",
    "categorical_colors_rgb_0-255/spectrum_cat.txt": "2d8be9c6bf7c69adc08a7c1de94d5950a37e58ba",
    "categorical_colors_rgb_0-255/ssp_cat_1.txt": "5deb1011398cc2a109d8103b6c260c561b401456",
    "categorical_colors_rgb_0-255/ssp_cat_2.txt": "3364240a40d29ad7f58cd622fa18d70ca4d78ee2",
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


def _official_files() -> dict[str, str]:
    return {
        **OFFICIAL_CONTINUOUS_FILES,
        **OFFICIAL_DISCRETE_FILES,
        **OFFICIAL_CATEGORICAL_FILES,
    }


def official_colormap_blob(name: str) -> str:
    """Return the pinned Git blob SHA for one official colour asset."""
    try:
        relative = _official_files()[name]
    except KeyError as exc:
        raise KeyError(f"unknown official IPCC colormap {name!r}") from exc
    return OFFICIAL_COLORMAP_BLOBS[relative]


def _normalized_git_blob_sha(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def verify_official_colormap_asset(
    name: str,
    *,
    root: str | Path | None = None,
) -> Path:
    """Validate one official colour table against the pinned AR6 WGI asset commit."""
    table = _official_files()
    try:
        relative = table[name]
    except KeyError as exc:
        raise KeyError(f"unknown official IPCC colormap {name!r}") from exc

    path = official_colormap_root(root) / relative
    if not path.is_file():
        raise FileNotFoundError(f"missing official colormap asset: {path}")

    expected = OFFICIAL_COLORMAP_BLOBS[relative]
    actual = _normalized_git_blob_sha(path)
    if actual != expected:
        raise RuntimeError(
            f"official colormap asset differs from {OFFICIAL_COLORMAP_COMMIT}: "
            f"{relative} (expected {expected}, got {actual})"
        )
    return path


def verify_official_colormap_checkout(
    *,
    root: str | Path | None = None,
    names: Iterable[str] | None = None,
) -> dict[str, str]:
    """Validate a set of official colour tables and return their blob SHAs."""
    selected = tuple(names) if names is not None else tuple(_official_files())
    verified: dict[str, str] = {}
    for name in selected:
        path = verify_official_colormap_asset(name, root=root)
        verified[name] = _normalized_git_blob_sha(path)
    return verified


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
    verify: bool = True,
) -> mcolors.Colormap:
    """Load an official AR6 WGI colour asset by semantic filename."""
    table = _official_files()
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
    if verify:
        path = verify_official_colormap_asset(name, root=root)
    data = _read_rgb(path)
    if reverse:
        data = data[::-1]

    cmap_name = f"ipcc_{name}" + ("_r" if reverse else "")
    categorical = name.endswith("_cat") or name.startswith(("ssp_cat_", "rcp_cat"))
    if "_disc" in name or categorical:
        cmap: mcolors.Colormap = mcolors.ListedColormap(data[:, :3], name=cmap_name)
    else:
        cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, data[:, :3])

    cmap._ipcc_asset_name = name
    cmap._ipcc_asset_blob = OFFICIAL_COLORMAP_BLOBS[relative] if verify else None
    cmap._ipcc_source_commit = OFFICIAL_COLORMAP_COMMIT if verify else None

    if register:
        try:
            mpl.colormaps.register(cmap, name=cmap_name, force=True)
        except TypeError:
            if cmap_name not in mpl.colormaps:
                mpl.colormaps.register(cmap, name=cmap_name)
    return cmap
