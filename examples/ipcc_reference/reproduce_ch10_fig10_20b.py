from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from common import assert_reference_contract, finalize
from contracts import REFERENCE_CONTRACTS
from sources import CH10_REPO, CH10_SHA, raw_url

from ipcc_sciplot import publication_context

BASE_PATH = (
    "esmvaltool/diag_scripts/ar6_wgi_ch10/CH10_additional_data/"
    "Mediterranean_station_info"
)


def main():
    try:
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
    except ImportError as exc:
        raise RuntimeError("This reference reproduction requires cartopy.") from exc

    eobs_url = raw_url(
        CH10_REPO,
        CH10_SHA,
        f"{BASE_PATH}/stations_info_tg_v21.0e.txt",
    )
    donat_url = raw_url(
        CH10_REPO,
        CH10_SHA,
        f"{BASE_PATH}/Donat_Stations_tas.csv",
    )

    eobs = pd.read_csv(
        eobs_url,
        sep="|",
        comment="#",
        names=[
            "STATION",
            "NAME",
            "COUNTRY",
            "LAT",
            "LON",
            "ELEV",
            "START",
            "STOP",
        ],
        engine="python",
    )
    donat = pd.read_csv(donat_url, sep="|", engine="python")

    for frame in (eobs, donat):
        frame.columns = [str(column).strip() for column in frame.columns]
    for column in ("LAT", "LON"):
        eobs[column] = pd.to_numeric(eobs[column], errors="coerce")
        donat[column] = pd.to_numeric(donat[column], errors="coerce")

    def med(frame):
        return frame[
            frame["LON"].between(-10, 40)
            & frame["LAT"].between(25, 50)
        ].copy()

    eobs = med(eobs)
    donat = med(donat)

    projection = ccrs.LambertConformal(
        central_longitude=15,
        central_latitude=37.5,
        standard_parallels=(30, 45),
    )

    with publication_context(width="single", height_mm=72, strict_font=False):
        fig, ax = plt.subplots(subplot_kw={"projection": projection})
        ax.set_extent([-10, 40, 25, 50], crs=ccrs.PlateCarree())

        ax.add_feature(
            cfeature.LAND,
            facecolor="#F0F0F0",
            edgecolor="none",
            zorder=0,
        )
        ax.add_feature(
            cfeature.OCEAN,
            facecolor="white",
            edgecolor="none",
            zorder=0,
        )
        ax.coastlines(
            resolution="110m",
            linewidth=0.5,
            color="black",
            zorder=2,
        )
        ax.add_feature(
            cfeature.BORDERS,
            facecolor="none",
            edgecolor="#808080",
            linewidth=0.3,
            zorder=2,
        )

        ax.scatter(
            eobs["LON"],
            eobs["LAT"],
            transform=ccrs.PlateCarree(),
            marker="o",
            s=7,
            facecolor="blue",
            edgecolor="black",
            linewidth=0.25,
            label="E-OBS",
            zorder=3,
        )
        ax.scatter(
            donat["LON"],
            donat["LAT"],
            transform=ccrs.PlateCarree(),
            marker="v",
            s=12,
            facecolor="yellow",
            edgecolor="black",
            linewidth=0.3,
            label="Donat et al. 2014",
            zorder=4,
        )

        ax.set_title("Station locations", loc="left", pad=4)
        legend = ax.legend(
            loc="lower left",
            frameon=True,
            fancybox=False,
            framealpha=1,
            borderpad=0.4,
            handletextpad=0.4,
        )
        legend.get_frame().set_linewidth(0.5)
        legend.get_frame().set_edgecolor("black")

        assert_reference_contract(
            fig,
            REFERENCE_CONTRACTS["ch10_fig10_20b_stations"],
        )
        return finalize(
            fig,
            "ch10_fig10_20b_stations",
            metadata={
                "Subject": (
                    "Reproduction of AR6 WGI Chapter 10 Figure 10.20b "
                    "station-location map from pinned official ESMValTool source data"
                ),
            },
        )


if __name__ == "__main__":
    print(main())
