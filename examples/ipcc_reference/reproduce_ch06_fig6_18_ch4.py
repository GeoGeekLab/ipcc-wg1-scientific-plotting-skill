from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ipcc_sciplot import publication_context, scenario_style

from common import clean_axes, finalize
from sources import CH6_REPO, CH6_SHA, raw_url

DATA_FILE = "ar6-wg1-ch6-emissions-global-data.csv"
CORE_SSPS = ["SSP1-1.9", "SSP1-2.6", "SSP2-4.5", "SSP3-7.0", "SSP5-8.5"]
REMOVE = {"SSP4-3.4-SPA4", "SSP4-6.0-SPA4", "SSP5-3.4-OS"}


def canonical_ssp(scenario: str) -> str | None:
    if not isinstance(scenario, str) or not scenario.startswith("SSP"):
        return None
    if scenario.startswith("SSP3-LowNTCF"):
        return "SSP3-LowNTCF"
    parts = scenario.split("-")
    if len(parts) < 2:
        return scenario
    return "-".join(parts[:2])


def row_xy(row: pd.Series, years: list[str]) -> tuple[np.ndarray, np.ndarray]:
    vals = pd.to_numeric(row[years], errors="coerce").to_numpy(dtype=float)
    x = np.asarray([int(y) for y in years], dtype=float)
    keep = np.isfinite(vals)
    return x[keep], vals[keep]


def envelope(rows: pd.DataFrame, years: list[str]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    values = rows[years].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    x = np.asarray([int(y) for y in years], dtype=float)
    with np.errstate(all="ignore"):
        lo = np.nanmin(values, axis=0)
        hi = np.nanmax(values, axis=0)
    keep = np.isfinite(lo) & np.isfinite(hi)
    return x[keep], lo[keep], hi[keep]


def main():
    df = pd.read_csv(raw_url(CH6_REPO, CH6_SHA, DATA_FILE))
    years = [c for c in df.columns if str(c).isdigit()]
    data = df[
        (df["Region"] == "World")
        & (df["Variable"] == "Emissions|CH4")
    ].copy()
    data = data[~data["Scenario"].isin(REMOVE)]

    with publication_context(width="double", height_mm=92, strict_font=False):
        fig, ax = plt.subplots()
        clean_axes(ax)

        history_styles = {
            "CMIP6": "-",
            "CMIP5": "--",
            "EDGAR": ":",
            "ECLIPSE_Ev5a": "-.",
        }
        history = data[data["Model"] == "History"]
        for _, row in history.iterrows():
            x, y = row_xy(row, years)
            if not len(x):
                continue
            label = str(row["Scenario"])
            ax.plot(
                x,
                y,
                color="black",
                linestyle=history_styles.get(label, "-"),
                linewidth=0.8,
                alpha=0.85,
                label=label,
                zorder=4,
            )

        rcps = data[data["Scenario"].astype(str).str.startswith("RCP")]
        if not rcps.empty:
            x, lo, hi = envelope(rcps, years)
            ax.fill_between(x, lo, hi, color="black", alpha=0.10, linewidth=0, label="RCP range")

        ev5a = data[data["Model"] == "Ev5a"]
        if not ev5a.empty:
            x, lo, hi = envelope(ev5a, years)
            ax.fill_between(x, lo, hi, color="purple", alpha=0.12, linewidth=0, label="ECLIPSE Ev5a range")

        data["canonical"] = data["Scenario"].map(canonical_ssp)
        for scenario in CORE_SSPS:
            subset = data[data["canonical"] == scenario]
            if subset.empty:
                continue
            color = scenario_style(scenario, profile="ar6-report").color
            for _, row in subset.iterrows():
                x, y = row_xy(row, years)
                if len(x):
                    ax.plot(x, y, color=color, linewidth=0.55, alpha=0.28, label="_nolegend_")

            values = subset[years].apply(pd.to_numeric, errors="coerce")
            median = values.median(axis=0, skipna=True).to_numpy(dtype=float)
            x = np.asarray([int(y) for y in years], dtype=float)
            keep = np.isfinite(median)
            ax.plot(
                x[keep],
                median[keep],
                color=color,
                linewidth=1.35,
                label=scenario,
                zorder=5,
            )

        ax.set_xlim(1850, 2100)
        ax.set_ylim(bottom=0)
        ax.set_title("CH₄", loc="left", pad=4)
        ax.set_xlabel("Year")
        ax.set_ylabel("CH₄ emissions (Mt CH₄ yr⁻¹)")

        handles, labels = ax.get_legend_handles_labels()
        unique = {}
        for handle, label in zip(handles, labels):
            if label and label != "_nolegend_" and label not in unique:
                unique[label] = handle
        legend = ax.legend(
            unique.values(),
            unique.keys(),
            loc="upper left",
            ncol=2,
            frameon=True,
            fancybox=False,
            framealpha=1,
        )
        legend.get_frame().set_edgecolor("black")
        legend.get_frame().set_linewidth(0.5)

        return finalize(
            fig,
            "ch06_fig6_18_ch4_emissions",
            metadata={
                "Subject": (
                    "Global methane-emissions reference reproduction from pinned "
                    "AR6 WGI Chapter 6 Figure 6.18 source CSV"
                ),
            },
        )


if __name__ == "__main__":
    print(main())
