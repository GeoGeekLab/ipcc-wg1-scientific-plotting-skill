from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from common import assert_reference_contract, clean_axes, finalize
from contracts import REFERENCE_CONTRACTS
from sources import CH3_REPO, CH3_SHA, raw_url

from ipcc_sciplot import publication_context

COLORS = {
    "LGM": "blue",
    "LIG": "lightblue",
    "MH": "lightsalmon",
    "mPWP": "red",
    "EECO": "darkred",
    "1pctCO2": "limegreen",
    "abrupt4xCO2": "violet",
}
CMIP6 = ["LGM", "LIG", "MH", "mPWP", "EECO", "1pctCO2", "abrupt4xCO2"]
CMIP5 = ["MH", "LGM", "1pctCO2", "abrupt4xCO2"]
NONCMIP = ["LGM", "LIG", "MH", "mPWP", "EECO"]


def load_xy(filename: str, header: int) -> tuple[np.ndarray, np.ndarray]:
    df = pd.read_csv(raw_url(CH3_REPO, CH3_SHA, filename), header=header)
    x = pd.to_numeric(df["1"], errors="coerce").to_numpy()
    y = pd.to_numeric(df["2"], errors="coerce").to_numpy()
    good = np.isfinite(x) & np.isfinite(y)
    return x[good], y[good]


def plot_points(ax, expts, source, marker, *, mean=False, header=18) -> None:
    for expt in expts:
        suffix = f"_{source}_ensemble_mean.csv" if mean else f"_{source}.csv"
        x, y = load_xy(f"fig3.2b_{expt}{suffix}", header)
        kwargs = {
            "marker": marker,
            "color": COLORS[expt],
            "linewidths": 1,
            "zorder": 3 if mean else 2,
        }
        if marker in {"o", "s"}:
            kwargs["facecolors"] = "none"
            kwargs["edgecolors"] = COLORS[expt]
        ax.scatter(
            x,
            y,
            s=75 if mean else 30,
            label=expt if mean and source == "CMIP6" else None,
            **kwargs,
        )


def main():
    with publication_context(width="single", height_mm=120, strict_font=False):
        fig, ax = plt.subplots()
        fig.subplots_adjust(left=0.23, right=0.96, bottom=0.12, top=0.90)

        ax.set_title(
            "b) Global temperature change over\nland and ocean for a range of climates",
            loc="left",
            pad=5,
        )
        ax.set_xlabel("Temperature change over sea (°C)")
        ax.set_ylabel("Temperature change over land (°C)")
        ax.set_xlim(-11, 20)
        ax.set_ylim(-15, 25)
        ax.axvline(0, color="grey", linestyle=":", linewidth=0.5, zorder=0)
        ax.axhline(0, color="grey", linestyle=":", linewidth=0.5, zorder=0)
        clean_axes(ax)

        plot_points(ax, CMIP6, "CMIP6", "o")
        plot_points(ax, CMIP5, "CMIP5", "x")
        plot_points(ax, NONCMIP, "nonCMIP", "+", header=19)

        plot_points(ax, CMIP6, "CMIP6", "s", mean=True)
        plot_points(ax, CMIP5, "CMIP5", "X", mean=True)
        plot_points(ax, NONCMIP, "nonCMIP", "P", mean=True, header=19)

        x, y = load_xy("fig3.2b_observation_instrumental.csv", 18)
        ax.scatter(
            x,
            y,
            marker="D",
            s=60,
            color="black",
            facecolors="none",
            linewidths=1,
            label="Instrumental",
            zorder=4,
        )

        x, y = load_xy("fig3.2b_observation_reconstruction.csv", 18)
        ax.errorbar(
            x,
            y,
            xerr=0.01,
            yerr=0.01,
            marker="*",
            color="lightsalmon",
            ecolor="black",
            ms=6,
            linestyle="none",
            label="Reconstruction",
            zorder=4,
        )

        xx = np.arange(-11, 20, 0.5)
        yy = -0.019470 * xx**2 + 1.580454 * xx
        ax.plot(xx, yy, color="black", linewidth=1, label="Fit to data", zorder=1)

        ax.scatter(
            [],
            [],
            marker="o",
            s=30,
            edgecolors="black",
            facecolors="none",
            label="CMIP6 models",
        )
        ax.scatter([], [], marker="x", s=30, color="black", label="CMIP5 models")
        ax.scatter([], [], marker="+", s=30, color="black", label="non-CMIP models")
        ax.scatter(
            [],
            [],
            marker="s",
            s=75,
            edgecolors="black",
            facecolors="none",
            label="CMIP6 mean",
        )

        legend = ax.legend(
            frameon=False,
            markerfirst=False,
            fontsize=7.5,
        )
        for text in legend.get_texts():
            text.set_fontsize(7.5)

        assert_reference_contract(
            fig,
            REFERENCE_CONTRACTS["ch03_fig3_2b_scatter"],
        )
        return finalize(
            fig,
            "ch03_fig3_2b_scatter",
            metadata={
                "Subject": (
                    "Reproduction of AR6 WGI Chapter 3 Figure 3.2b "
                    "from pinned official CSV source data"
                ),
            },
        )


if __name__ == "__main__":
    print(main())
