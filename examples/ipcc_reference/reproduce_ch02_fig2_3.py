from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from common import clean_axes, finalize
from sources import CH2_REPO, CH2_SHA, raw_url

from ipcc_sciplot import publication_context

BLUE = "#5492CD"
BLUE_FILL = "#5492CD"
GREY = "#808080"
LIGHT_GREY = "#BFBFBF"
ORANGE = "#C47900"
GREEN = "#004F00"
GREEN_FILL = "#DFEDC3"
DARK_BLUE = "#003466"


def table(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(
        raw_url(CH2_REPO, CH2_SHA, path),
        sep=r"\s+",
        engine="python",
        **kwargs,
    )


def errorbar_abs(ax, x, y, low, high, **kwargs) -> None:
    low = np.asarray(low, dtype=float)
    high = np.asarray(high, dtype=float)
    y = np.asarray(y, dtype=float)
    lo = np.minimum(low, high)
    hi = np.maximum(low, high)
    yerr = np.vstack([np.maximum(0, y - lo), np.maximum(0, hi - y)])
    ax.errorbar(x, y, yerr=yerr, **kwargs)


def fill_study(ax, pp: pd.DataFrame, study: str) -> None:
    data = pp[pp["Study"] == study].sort_values("Age")
    if data.empty:
        return
    ax.fill_between(
        data["Age"],
        data["CO2do"],
        data["CO2up"],
        color=BLUE_FILL,
        alpha=0.32,
        linewidth=0,
    )
    ax.plot(data["Age"], data["CO2"], color=BLUE, linewidth=0.8)


def main():
    ice = table("ice_core.txt")
    sos = table("Sosdian.txt")
    eleni = table("Anagnostou.txt")
    pp = table("Plio_Pleisto_Final.txt", comment="#")
    stoll = table("Stoll.txt")
    wit = table("wit.txt")
    wit.columns = [
        "Ma",
        "Ma_L",
        "Ma_U",
        "pCO2",
        "pCO2_L1",
        "pCO2_U1",
        "pCO2_L2",
        "pCO2_U2",
    ]
    alk = table("Alkenone compilation.txt")
    phan = table("PhanCO2F_feb2021.txt", comment="#")
    smooth = table("PhanCO2sm.exp.txt")

    with publication_context(width="single", height_mm=240, strict_font=False):
        fig, axes = plt.subplots(3, 1, gridspec_kw={"hspace": 0.34})

        ax = axes[0]
        clean_axes(ax)
        ax.set_xlim(450, 0)
        ax.set_ylim(0, 3000)
        ax.set_xticks(np.arange(0, 451, 50))
        ax.set_yticks([0, 1000, 2000, 3000])
        ax.set_xlabel("Age (Myr)")
        ax.set_ylabel("CO₂ (ppm)")
        ax.text(0.01, 0.92, "(a)", transform=ax.transAxes)

        ax.scatter(
            alk["Age"],
            alk["pCO2"],
            s=8,
            facecolor=LIGHT_GREY,
            edgecolor=GREY,
            linewidth=0.4,
        )
        ax.scatter(
            sos["Age"],
            sos["CO2.50"] * 1e6,
            s=10,
            facecolor="none",
            edgecolor=BLUE,
            linewidth=0.6,
        )
        ax.scatter(
            eleni["age"],
            eleni["CO2"],
            s=10,
            facecolor="none",
            edgecolor=BLUE,
            linewidth=0.6,
        )
        stomata = phan["method"] == "Stomata"
        ax.scatter(
            phan.loc[stomata, "Age"],
            phan.loc[stomata, "CO2"],
            s=9,
            marker="s",
            color="#B2B2B2",
            alpha=0.8,
        )
        psols = phan["method"] == "psols"
        ax.scatter(
            phan.loc[psols, "Age"],
            phan.loc[psols, "CO2"],
            s=10,
            marker="x",
            color=DARK_BLUE,
            alpha=0.65,
        )
        ax.scatter(
            wit["Ma"],
            wit["pCO2"],
            s=10,
            facecolor="none",
            edgecolor=ORANGE,
            linewidth=0.6,
        )

        smooth = smooth.sort_values("age")
        ax.fill_between(
            smooth["age"],
            smooth["lw95"],
            smooth["up95"],
            color=GREEN_FILL,
            alpha=0.45,
            linewidth=0,
        )
        ax.fill_between(
            smooth["age"],
            smooth["lw68"],
            smooth["up68"],
            color=GREEN_FILL,
            alpha=0.9,
            linewidth=0,
        )
        ax.plot(smooth["age"], smooth["pmaxCO2"], color=GREEN, linewidth=1.2)
        ax.text(300, 2500, "δ¹³C–paleosols", color=DARK_BLUE, fontsize=7.5)
        ax.text(130, 350, "stomata", color="#7F7F7F", fontsize=7.5)

        ax = axes[1]
        clean_axes(ax)
        ax.set_xlim(58, 0)
        ax.set_ylim(150, 2500)
        ax.set_xticks(np.arange(0, 59, 5))
        ax.set_yticks(np.arange(500, 2501, 500))
        ax.set_xlabel("Age (Myr)")
        ax.set_ylabel("CO₂ (ppm)")
        ax.text(0.01, 0.92, "(b)", transform=ax.transAxes)

        xerr = np.vstack(
            [
                np.abs(wit["Ma"] - wit["Ma_U"]),
                np.abs(wit["Ma_L"] - wit["Ma"]),
            ]
        )
        yerr = np.vstack(
            [
                wit["pCO2"] - wit["pCO2_L1"],
                wit["pCO2_U1"] - wit["pCO2"],
            ]
        )
        ax.errorbar(
            wit["Ma"],
            wit["pCO2"],
            xerr=xerr,
            yerr=yerr,
            fmt="o",
            ms=2.5,
            color=ORANGE,
            ecolor="#DFC27D",
            elinewidth=0.5,
            capsize=0,
        )

        sos_sorted = sos.sort_values("Age")
        ax.fill_between(
            sos_sorted["Age"],
            sos_sorted["CO2.2.5"] * 1e6,
            sos_sorted["CO2.97.5"] * 1e6,
            color=BLUE_FILL,
            alpha=0.32,
            linewidth=0,
        )
        ax.plot(
            sos_sorted["Age"],
            sos_sorted["CO2.50"] * 1e6,
            color=BLUE,
            linewidth=0.8,
        )
        ax.scatter(
            sos_sorted["Age"],
            sos_sorted["CO2.50"] * 1e6,
            s=7,
            color=BLUE,
        )

        eleni_sorted = eleni.sort_values("age")
        ax.fill_between(
            eleni_sorted["age"],
            eleni_sorted["CO2"] - eleni_sorted["CO2do"],
            eleni_sorted["CO2"] + eleni_sorted["CO2up"],
            color=BLUE_FILL,
            alpha=0.32,
            linewidth=0,
        )
        ax.plot(
            eleni_sorted["age"],
            eleni_sorted["CO2"],
            color=BLUE,
            linewidth=0.8,
        )
        ax.scatter(
            eleni_sorted["age"],
            eleni_sorted["CO2"],
            s=7,
            color=BLUE,
        )

        errorbar_abs(
            ax,
            alk["Age"],
            alk["pCO2"],
            alk["pCO2_min"],
            alk["pCO2_max"],
            fmt="o",
            ms=2.5,
            mfc=LIGHT_GREY,
            mec=GREY,
            mew=0.4,
            ecolor=LIGHT_GREY,
            elinewidth=0.5,
            capsize=0,
        )
        ax.text(40, 400, "δ¹³C–alkenone", color=GREY, fontsize=7.5)
        ax.text(30, 2000, "δ¹¹B–foraminifera", color=BLUE, fontsize=7.5)
        ax.text(20, 1000, "δ¹³C–phytane", color=ORANGE, fontsize=7.5)

        ax = axes[2]
        clean_axes(ax)
        ax.set_xlim(3500, 0)
        ax.set_ylim(150, 500)
        ax.set_xticks(np.arange(0, 3501, 500))
        ax.set_yticks([200, 300, 400, 500])
        ax.set_xlabel("Age (kyr bp)")
        ax.set_ylabel("CO₂ (ppm)")
        ax.text(0.01, 0.92, "(c)", transform=ax.transAxes)

        ax.plot(ice["age"], ice["CO2"], color="black", linewidth=0.8)
        errorbar_abs(
            ax,
            stoll["Age"] * 1e3,
            stoll["CO2"],
            stoll["Co2.d"],
            stoll["Co2.up"],
            fmt="o",
            ms=2.3,
            mfc=LIGHT_GREY,
            mec=GREY,
            mew=0.35,
            ecolor=LIGHT_GREY,
            elinewidth=0.45,
            capsize=0,
        )

        for study in [
            "Dyez2018",
            "Chalk2017.LP",
            "Chalk2017.MPT",
            "DelaVega2020",
        ]:
            fill_study(ax, pp, study)

        studies = [
            ("Hoenisch2009", "o"),
            ("Raitzsch2018", "s"),
            ("Bartoli2011", "s"),
        ]
        for study, marker in studies:
            data = pp[pp["Study"] == study]
            if data.empty:
                continue
            errorbar_abs(
                ax,
                data["Age"],
                data["CO2"],
                data["CO2do"],
                data["CO2up"],
                fmt=marker,
                ms=2.5,
                color=BLUE,
                ecolor=BLUE,
                alpha=0.55,
                elinewidth=0.45,
                capsize=0,
            )

        ax.text(700, 300, "Ant. ice core", color="black", fontsize=7.5)
        ax.text(1500, 400, "δ¹¹B–foraminifera", color=BLUE, fontsize=7.5)
        ax.text(2500, 170, "δ¹³C–alkenones", color=GREY, fontsize=7.5)

        for axis in axes:
            axis.tick_params(labelsize=7.5)

        return finalize(
            fig,
            "ch02_fig2_3_co2_proxy",
            metadata={
                "Subject": (
                    "Python reproduction of AR6 WGI Chapter 2 Figure 2.3 "
                    "from pinned official proxy source data"
                ),
            },
        )


if __name__ == "__main__":
    print(main())
