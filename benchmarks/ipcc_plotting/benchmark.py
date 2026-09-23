from __future__ import annotations

import csv
import io
import json
import platform
from hashlib import sha256
from importlib.metadata import version
from pathlib import Path
from urllib.request import urlopen

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from cartopy import crs as ccrs
from figanos import matplotlib as fg

from ipcc_sciplot import (
    add_uncertainty_legend,
    audit_figure_report,
    label_line_ends,
    map_panel_grid,
    publication_context,
    scenario_style,
)
from ipcc_sciplot.archetypes import add_ipcc_colorbar, plot_scenario_timeseries
from ipcc_sciplot.maps import add_low_agreement_hatching
from ipcc_sciplot.style import axis_label, panel_label

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "benchmarks" / "ipcc_plotting" / "out"
OUT.mkdir(parents=True, exist_ok=True)

FIGANOS_VERSION = "0.7.0"
AR6_REPO = "IPCC-WG1/Chapter-6_Fig18"
AR6_COMMIT = "09d9b43fe935fc81d828147f91b717396a84fca3"
AR6_BLOB = "07162ad5f315cbcfd49bd672f6180c67ad6fc7b3"
AR6_FILE = "ar6-wg1-ch6-emissions-global-data.csv"
AR6_URL = f"https://raw.githubusercontent.com/{AR6_REPO}/{AR6_COMMIT}/{AR6_FILE}"
CORE_SSPS = ("SSP1-1.9", "SSP1-2.6", "SSP2-4.5", "SSP3-7.0", "SSP5-8.5")


def save(fig: mpl.figure.Figure, name: str) -> Path:
    path = OUT / name
    fig.savefig(path, dpi=180, bbox_inches="tight", pad_inches=0.03, facecolor="white")
    plt.close(fig)
    return path


def mm_size(fig: mpl.figure.Figure) -> list[float]:
    return [round(float(v) * 25.4, 2) for v in fig.get_size_inches()]


def line_colors(ax: mpl.axes.Axes) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in ax.lines:
        label = str(line.get_label())
        if label in CORE_SSPS:
            out[label] = mcolors.to_hex(line.get_color()).upper()
    return out


def line_diagnostics(ax: mpl.axes.Axes) -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for line in ax.lines:
        label = str(line.get_label())
        if label not in CORE_SSPS:
            continue
        y = np.asarray(line.get_ydata(), dtype=float)
        finite = np.isfinite(y)
        out[label] = {
            "visible": bool(line.get_visible()),
            "linewidth": float(line.get_linewidth()),
            "linestyle": str(line.get_linestyle()),
            "alpha": line.get_alpha(),
            "points": int(y.size),
            "finite_points": int(finite.sum()),
            "y_min": float(np.nanmin(y)),
            "y_max": float(np.nanmax(y)),
        }
    return out


def load_ar6_ch4() -> tuple[dict[str, xr.DataArray], dict[str, object]]:
    with urlopen(AR6_URL, timeout=60) as response:
        raw = response.read()
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8")))
    rows = [
        row
        for row in reader
        if row["Region"] == "World" and row["Variable"] == "Emissions|CH4"
    ]
    if not rows:
        raise RuntimeError("Pinned AR6 CH4 rows were not found.")

    scenario_rows = {
        scenario: next(
            row for row in rows if row["Scenario"].startswith(scenario)
        )
        for scenario in CORE_SSPS
    }
    fieldnames = reader.fieldnames or []
    years = [
        int(name)
        for name in fieldnames
        if name.isdigit()
        and all(scenario_rows[scenario].get(name, "") for scenario in CORE_SSPS)
    ]
    if len(years) < 2:
        raise RuntimeError("Pinned AR6 scenario rows have insufficient common time points.")

    times = pd.to_datetime([f"{year}-01-01" for year in years])
    arrays: dict[str, xr.DataArray] = {}
    for scenario, row in scenario_rows.items():
        values = [float(row[str(year)]) for year in years]
        arrays[scenario] = xr.DataArray(
            values,
            coords={"time": times},
            dims=("time",),
            name="ch4_emissions",
            attrs={
                "description": "Global methane emissions",
                "long_name": "CH4 emissions",
                "units": "Tg CH4 yr-1",
            },
        )

    return arrays, {
        "repository": AR6_REPO,
        "commit": AR6_COMMIT,
        "blob": AR6_BLOB,
        "file": AR6_FILE,
        "download_sha256": sha256(raw).hexdigest(),
        "common_scenario_years": years,
    }


def render_timeseries(data: dict[str, xr.DataArray]) -> dict[str, object]:
    mpl.rcdefaults()
    fg.set_mpl_style("ouranos", reset=True)
    ax = fg.timeseries(data, show_lat_lon=False, legend="edge")
    ax.set_title("Global methane emissions", loc="left")
    ax.set_ylabel("CH4 emissions (Tg CH4 yr-1)")
    fig = ax.figure
    figanos_size = mm_size(fig)
    figanos_colors = line_colors(ax)
    figanos_lines = line_diagnostics(ax)
    save(fig, "01_timeseries_figanos_native.png")

    mpl.rcdefaults()
    with publication_context(width="double", height_mm=100, strict_font=False):
        fig, ax = plt.subplots()
        x = next(iter(data.values())).time.dt.year.values
        series = {key: value.values for key, value in data.items()}
        report_lines_map = plot_scenario_timeseries(
            ax,
            x,
            series,
            profile="ar6-report",
            legend=False,
        )
        label_line_ends(ax, report_lines_map, min_gap_points=2)
        ax.set_title("Global methane emissions", loc="left")
        ax.set_xlabel("Year")
        ax.set_ylabel(axis_label("CH4 emissions", "Tg CH4 yr-1"))
        ax.spines[["top", "right"]].set_visible(False)
        report_size = mm_size(fig)
        report_colors = line_colors(ax)
        report_lines = line_diagnostics(ax)
        report_audit = audit_figure_report(
            fig, profile="ar6-report", strict_dimensions=True
        ).to_dict()
        save(fig, "01_timeseries_ar6_report.png")

    mpl.rcdefaults()
    with publication_context(width="double", height_mm=100, strict_font=False):
        fig, ax = plt.subplots()
        x = next(iter(data.values())).time.dt.year.values
        series = {key: value.values for key, value in data.items()}
        plot_scenario_timeseries(
            ax, x, series, profile="wgi-guide-2022", legend_loc="upper left"
        )
        ax.set_title("Global methane emissions", loc="left")
        ax.set_xlabel("Year")
        ax.set_ylabel(axis_label("CH4 emissions", "Tg CH4 yr-1"))
        ax.spines[["top", "right"]].set_visible(False)
        guide_size = mm_size(fig)
        guide_colors = line_colors(ax)
        save(fig, "01_timeseries_ar6_wgi2022.png")

    expected_2022 = {
        name: scenario_style(name, profile="wgi-guide-2022").color.upper()
        for name in CORE_SSPS
    }
    expected_report = {
        name: scenario_style(name, profile="ar6-report").color.upper()
        for name in CORE_SSPS
    }
    return {
        "figanos_native_size_mm": figanos_size,
        "ar6_report_size_mm": report_size,
        "ar6_wgi2022_size_mm": guide_size,
        "figanos_colors": figanos_colors,
        "figanos_lines": figanos_lines,
        "ar6_report_colors": report_colors,
        "ar6_report_lines": report_lines,
        "ar6_wgi2022_colors": guide_colors,
        "expected_report_colors": expected_report,
        "expected_2022_colors": expected_2022,
        "figanos_matches_wgi2022": figanos_colors == expected_2022,
        "figanos_matches_ar6_report": figanos_colors == expected_report,
        "ar6_report_audit": report_audit,
    }


def benchmark_field() -> tuple[xr.DataArray, xr.DataArray]:
    lat = np.linspace(-80, 80, 65)
    lon = np.linspace(-177.5, 177.5, 144)
    xx, yy = np.meshgrid(np.deg2rad(lon), np.deg2rad(lat))
    field = (
        2.2 * np.cos(yy) * np.sin(xx * 0.8)
        + 0.9 * np.sin(2.3 * yy)
        + 0.35 * np.cos(2.0 * xx - yy)
    )
    field = np.clip(field, -3.8, 3.8)
    low_agreement = (
        (np.abs(field) < 0.75)
        | ((np.cos(xx * 1.7) + np.sin(yy * 2.1)) > 1.25)
    )
    da = xr.DataArray(
        field,
        coords={"lat": lat, "lon": lon},
        dims=("lat", "lon"),
        name="tas_change",
        attrs={
            "description": "Synthetic temperature change",
            "long_name": "Temperature change",
            "units": "°C",
        },
    )
    mask = xr.DataArray(
        np.where(low_agreement, 1.0, np.nan),
        coords=da.coords,
        dims=da.dims,
        name="low_agreement",
    )
    return da, mask


def render_map() -> dict[str, object]:
    da, mask = benchmark_field()
    levels = np.arange(-4, 4.01, 1.0)
    figsize = (180 / 25.4, 100 / 25.4)
    shared_cmap = mpl.colormaps["temp_div"]

    mpl.rcdefaults()
    fg.set_mpl_style("ouranos", reset=True)
    ax = fg.gridmap(
        da,
        projection=ccrs.Robinson(),
        cmap=shared_cmap,
        levels=levels,
        divergent=0,
        fig_kw={"figsize": figsize},
        plot_kw={"cbar_kwargs": {"orientation": "horizontal", "pad": 0.07}},
        features=None,
        frame=True,
    )
    fg.hatchmap(
        {"Low agreement": mask},
        ax=ax,
        plot_kw={"Low agreement": {"hatches": ["////"]}},
        legend_kw={"loc": "lower left", "fontsize": 8, "frameon": True},
        features=None,
        frame=True,
    )
    ax.set_global()
    ax.set_title("Temperature change and model agreement", loc="left")
    fig = ax.figure
    figanos_size = mm_size(fig)
    figanos_projection = ax.projection.__class__.__name__
    save(fig, "02_map_figanos_controlled.png")

    mpl.rcdefaults()
    with publication_context(width="double", height_mm=100, strict_font=False):
        fig, ax = plt.subplots(subplot_kw={"projection": ccrs.Robinson()})
        norm = mcolors.BoundaryNorm(levels, shared_cmap.N)
        mesh = ax.pcolormesh(
            da.lon,
            da.lat,
            da.values,
            transform=ccrs.PlateCarree(),
            cmap=shared_cmap,
            norm=norm,
            rasterized=True,
        )
        add_low_agreement_hatching(
            ax,
            da.lon.values,
            da.lat.values,
            np.isfinite(mask.values),
            transform=ccrs.PlateCarree(),
            hatch="////",
        )
        add_uncertainty_legend(
            ax,
            low_agreement="Low agreement",
            hatch="////",
            fontsize=8,
        )
        ax.set_global()
        ax.set_title("Temperature change and model agreement", loc="left", pad=4)
        cbar = add_ipcc_colorbar(
            fig,
            mesh,
            ax=ax,
            label="Temperature change",
            unit="°C",
            orientation="horizontal",
            pad=0.07,
            fraction=0.06,
        )
        cbar.set_ticks(levels)
        ar6_size = mm_size(fig)
        ar6_projection = ax.projection.__class__.__name__
        ar6_audit = audit_figure_report(
            fig,
            profile="ar6-report",
            strict_dimensions=True,
            require_ipcc_colormap=False,
            reference_size_mm=(180, 100),
            reference_panel_count=1,
            reference_projection="Robinson",
        ).to_dict()
        save(fig, "02_map_ar6_controlled.png")

    return {
        "data": {
            "shape": list(da.shape),
            "levels": levels.tolist(),
            "shared_cmap_name": shared_cmap.name,
            "low_agreement_fraction": round(float(np.isfinite(mask.values).mean()), 4),
        },
        "figanos_size_mm": figanos_size,
        "ar6_size_mm": ar6_size,
        "figanos_projection": figanos_projection,
        "ar6_projection": ar6_projection,
        "same_projection": figanos_projection == ar6_projection,
        "same_palette_object": True,
        "ar6_contract_diagnostic": ar6_audit,
    }


def render_multipanel() -> dict[str, object]:
    base, _ = benchmark_field()
    warming = np.array([1.5, 2.0, 4.0])
    scales = np.array([0.55, 0.72, 1.0])
    data = xr.concat(
        [base * scale for scale in scales],
        dim=xr.DataArray(warming, dims="warming", name="warming"),
    )
    data.name = "tas_change"
    data.attrs = base.attrs.copy()
    levels = np.arange(-4, 4.01, 1.0)
    figsize = (180 / 25.4, 72 / 25.4)
    shared_cmap = mpl.colormaps["temp_div"]

    mpl.rcdefaults()
    fg.set_mpl_style("ouranos", reset=True)
    facet = fg.gridmap(
        data,
        projection=ccrs.Robinson(),
        cmap=shared_cmap,
        levels=levels,
        divergent=0,
        fig_kw={"figsize": figsize},
        plot_kw={
            "col": "warming",
            "col_wrap": 3,
            "cbar_kwargs": {"orientation": "horizontal", "pad": 0.06},
        },
        features=None,
        frame=True,
        enumerate_subplots=True,
    )
    fig = facet.fig
    figanos_axes = len([ax for ax in fig.axes if hasattr(ax, "projection")])
    figanos_size = mm_size(fig)
    save(fig, "03_multipanel_figanos_facet.png")

    mpl.rcdefaults()
    with publication_context(width="double", height_mm=72, strict_font=False):
        fig, axes = map_panel_grid(
            3,
            projection=ccrs.Robinson(),
            ncols=3,
            width="double",
            height_mm=72,
            wspace=0.03,
        )
        norm = mcolors.BoundaryNorm(levels, shared_cmap.N)
        mesh = None
        for idx, (ax, value) in enumerate(zip(axes, warming, strict=True)):
            panel = data.sel(warming=value)
            mesh = ax.pcolormesh(
                panel.lon,
                panel.lat,
                panel.values,
                transform=ccrs.PlateCarree(),
                cmap=shared_cmap,
                norm=norm,
                rasterized=True,
            )
            ax.set_global()
            panel_label(ax, chr(ord("a") + idx), title=f"{value:g} °C")
        if mesh is None:
            raise RuntimeError("No multipanel mesh rendered.")
        add_ipcc_colorbar(
            fig,
            mesh,
            ax=list(axes),
            label="Temperature change",
            unit="°C",
            orientation="horizontal",
            pad=0.08,
            fraction=0.08,
        )
        ar6_axes = len(axes)
        ar6_size = mm_size(fig)
        ar6_audit = audit_figure_report(
            fig,
            profile="ar6-report",
            strict_dimensions=True,
            reference_size_mm=(180, 72),
            reference_panel_count=3,
            reference_projection="Robinson",
        ).to_dict()
        save(fig, "03_multipanel_ar6_panel_grid.png")

    return {
        "figanos_panel_axes": figanos_axes,
        "ar6_panel_axes": ar6_axes,
        "figanos_size_mm": figanos_size,
        "ar6_size_mm": ar6_size,
        "figanos_native_faceting": True,
        "ar6_native_faceting": False,
        "ar6_panel_grid_helper": True,
        "ar6_contract_diagnostic": ar6_audit,
    }


def write_markdown(results: dict[str, object]) -> None:
    ts = results["timeseries"]
    mp = results["map"]
    multi = results["multipanel"]
    lines = [
        "# Benchmark results",
        "",
        f"Generated with Figanos {results['versions']['figanos']} and "
        f"ar6-sciplot {results['versions']['ar6_sciplot']} on Python "
        f"{results['versions']['python']}.",
        "",
        "## Summary",
        "",
        "Figanos remains the stronger general-purpose climate plotting library: "
        "broader plot coverage, deeper Xarray integration, native faceting, automatic "
        "scenario colours, and bundled IPCC colormaps.",
        "",
        "ar6-sciplot is focused on AR6/WGI profile versioning, print geometry, provenance, "
        "uncertainty semantics, and figure checks. This benchmark iteration also adds a "
        "fixed-size panel-grid helper and uncertainty legends.",
        "",
        "## 1. Scenario time series",
        "",
        f"- Figanos matches the WGI-2022 SSP colour table: {ts['figanos_matches_wgi2022']}.",
        f"- Figanos matches the report-era AR6 SSP table: {ts['figanos_matches_ar6_report']}.",
        f"- Native Figanos figure size: {ts['figanos_native_size_mm']} mm.",
        f"- ar6-report figure size: {ts['ar6_report_size_mm']} mm.",
        "",
        "Figanos uses the updated WGI scenario palette automatically. The ar6-report "
        "profile keeps final-report-era scenario colours for source-faithful reproduction.",
        "",
        "Figanos' edge labels save plotting space, but the SSP1-1.9 and SSP1-2.6 labels "
        "overlap at the 2100 endpoint in this dataset. ar6-sciplot uses the same "
        "line-end approach with vertical collision avoidance.",
        "",
        "## 2. Controlled change map + agreement",
        "",
        f"- Projection: {mp['figanos_projection']} for both renderers.",
        "- Shared registered IPCC colormap: "
        f"{mp['data']['shared_cmap_name']}.",
        f"- Shared level boundaries: {mp['data']['levels']}.",
        "",
        "Figanos still provides the more compact gridmap+hatchmap workflow. ar6-sciplot "
        "now supplies the agreement hatch and its legend through dedicated helpers, while "
        "keeping low agreement, missing data, and significance as separate encodings.",
        "",
        "## 3. Warming-level multipanel",
        "",
        f"- Figanos native Xarray faceting: {multi['figanos_native_faceting']}.",
        f"- ar6-sciplot panel-grid helper: {multi['ar6_panel_grid_helper']}.",
        "",
        "At the same 180 x 72 mm size, the rendered panel layout is now comparable. "
        "Figanos still has the simpler data-to-facet path because it maps the Xarray "
        "dimension directly to panels.",
        "",
        "The PNG outputs in the artifact show the rendered comparison.",
        "",
    ]
    (OUT / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")

def main() -> None:
    if version("figanos") != FIGANOS_VERSION:
        raise RuntimeError(
            f"Benchmark requires figanos=={FIGANOS_VERSION}; found {version('figanos')}"
        )

    data, source = load_ar6_ch4()
    results = {
        "schema": "ar6-sciplot.cross-library-benchmark/v1",
        "versions": {
            "python": platform.python_version(),
            "matplotlib": mpl.__version__,
            "xarray": xr.__version__,
            "figanos": version("figanos"),
            "ar6_sciplot": version("ar6-sciplot"),
        },
        "source": source,
        "timeseries": render_timeseries(data),
        "map": render_map(),
        "multipanel": render_multipanel(),
        "claims": {
            "figanos_general_plotting_breadth_stronger": True,
            "figanos_xarray_faceting_stronger": True,
            "ar6_profile_versioning_more_explicit": True,
            "ar6_machine_fidelity_audit_available": True,
            "ar6_panel_grid_helper_available": True,
            "ar6_uncertainty_legend_available": True,
        },
    }
    (OUT / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_markdown(results)
    print(OUT / "RESULTS.md")


if __name__ == "__main__":
    main()
