"""End-to-end synthetic IPCC-native assessment-map example.

Run after installing the climate extras:
    python -m pip install -e ".[climate,qa]"
    python examples/ipcc_native_workflow.py

The data are synthetic and must never be interpreted as a climate projection.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from ipcc_sciplot import (
    add_insufficient_data_mask,
    add_mask_hatching,
    add_panel_label,
    assessment_context,
    build_provenance,
    classify_robustness,
    ensemble_summary,
    load_ipcc_native_recipe,
    make_norm,
    save_figure,
    write_provenance,
)


ROOT = Path(__file__).resolve().parents[1]
RECIPE_PATH = ROOT / "templates" / "ipcc_native_recipe.yaml"


def synthetic_ensemble(seed: int = 20260825) -> xr.DataArray:
    rng = np.random.default_rng(seed)
    models = [f"model_{i:02d}" for i in range(12)]
    lat = np.arange(-87.5, 90.0, 5.0)
    lon = np.arange(-177.5, 180.0, 5.0)
    lon2d, lat2d = np.meshgrid(lon, lat)

    forced_pattern = 2.0 + 1.2 * np.cos(np.deg2rad(lat2d)) + 0.7 * np.sin(np.deg2rad(lon2d))
    values = np.stack(
        [forced_pattern + rng.normal(0.0, 1.2, size=forced_pattern.shape) for _ in models]
    )

    # Demonstrate cell-varying model availability without manufacturing a scientific result.
    values[:8, :4, :10] = np.nan

    da = xr.DataArray(
        values,
        dims=("model", "lat", "lon"),
        coords={"model": models, "lat": lat, "lon": lon},
        name="synthetic_temperature_change",
        attrs={
            "units": "K",
            "long_name": "Synthetic model-level temperature change",
            "warning": "Synthetic example only; not a climate projection.",
        },
    )
    return da


def main() -> None:
    recipe = load_ipcc_native_recipe(RECIPE_PATH)
    seed = int(recipe.provenance.get("random_seed", 20260825))
    ensemble = synthetic_ensemble(seed)

    summary = ensemble_summary(
        ensemble,
        dim=str(recipe.sources.get("model_dimension", "model")),
        center=str(recipe.ensemble.get("center", "median")),
        lower_q=float(recipe.ensemble.get("lower_quantile", 0.17)),
        upper_q=float(recipe.ensemble.get("upper_quantile", 0.83)),
        sign_agreement=float(recipe.robustness.get("sign_agreement_threshold", 0.80)),
        min_count=int(recipe.ensemble.get("min_valid_count", 5)),
        zero_tolerance=float(recipe.robustness.get("zero_tolerance", 0.0)),
    )
    classes = classify_robustness(
        n_valid=summary["n_valid"],
        agreement=summary["sign_agreement"],
        min_count=int(recipe.ensemble.get("min_valid_count", 5)),
        agreement_threshold=float(recipe.robustness.get("sign_agreement_threshold", 0.80)),
    )

    plotted = xr.merge([summary, classes], compat="override")
    plotted.attrs.update(
        {
            "assessment_intent": recipe.assessment["intent"],
            "estimand": recipe.science["estimand"],
            "synthetic_example": "true",
        }
    )

    norm_cfg = recipe.visual["normalization"]
    norm = make_norm(
        str(norm_cfg["type"]),
        vmin=float(norm_cfg["vmin"]),
        vcenter=float(norm_cfg["vcenter"]),
        vmax=float(norm_cfg["vmax"]),
    )

    output_stem = ROOT / recipe.output_stem
    output_stem.parent.mkdir(parents=True, exist_ok=True)

    with assessment_context(width_mm=180, height_mm=92, base_font_pt=8):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
        transform = ccrs.PlateCarree()

        mesh = ax.pcolormesh(
            ensemble.lon,
            ensemble.lat,
            plotted["center"],
            transform=transform,
            cmap=str(recipe.visual["colormap"]),
            norm=norm,
            shading="auto",
            rasterized=True,
            zorder=1,
        )
        add_mask_hatching(
            ax,
            ensemble.lon.values,
            ensemble.lat.values,
            plotted["low_agreement"],
            transform=transform,
            hatch="////",
            zorder=3,
        )
        add_insufficient_data_mask(
            ax,
            ensemble.lon.values,
            ensemble.lat.values,
            plotted["insufficient_data"],
            transform=transform,
            color=str(recipe.visual.get("missing_color", "0.85")),
            zorder=4,
        )
        ax.coastlines(linewidth=0.45, color="0.25", zorder=5)
        ax.set_global()
        add_panel_label(ax, "(a)")

        cbar = fig.colorbar(mesh, ax=ax, orientation="horizontal", pad=0.04, fraction=0.06)
        cbar.set_label("Synthetic temperature change [K]")
        ax.set_title("Synthetic assessment-map workflow — not a climate projection", loc="left")

        save_figure(
            fig,
            output_stem,
            formats=tuple(str(x) for x in recipe.outputs["formats"]),
            dpi=int(recipe.outputs.get("preview_dpi", 300)),
            metadata={
                "Title": "Synthetic IPCC-native assessment-map example",
                "Subject": "Demonstration of estimate, agreement and sample-support semantics",
            },
            close=True,
        )

    plotted_path = ROOT / str(recipe.outputs["plotted_data"])
    plotted_path.parent.mkdir(parents=True, exist_ok=True)
    plotted.to_netcdf(plotted_path)

    recipe_copy = output_stem.with_name(output_stem.name + "_recipe.yaml")
    shutil.copyfile(RECIPE_PATH, recipe_copy)

    provenance = build_provenance(
        inputs=[RECIPE_PATH],
        parameters={
            "figure_id": recipe.figure_id,
            "assessment_intent": recipe.assessment["intent"],
            "ensemble_center": recipe.ensemble["center"],
            "lower_quantile": recipe.ensemble["lower_quantile"],
            "upper_quantile": recipe.ensemble["upper_quantile"],
            "sign_agreement_threshold": recipe.robustness["sign_agreement_threshold"],
            "min_valid_count": recipe.ensemble["min_valid_count"],
            "synthetic_example": True,
        },
        citations=[
            "https://www.ipcc.ch/site/assets/uploads/2022/09/IPCC_AR6_WGI_VisualStyleGuide_2022.pdf",
            "https://github.com/IPCC-WG1/Atlas",
            "https://github.com/IPCC-WG1/colormaps",
        ],
        project_root=ROOT,
        random_seed=seed,
    )
    write_provenance(provenance, ROOT / str(recipe.outputs["provenance"]))

    qa_path = ROOT / str(recipe.outputs["qa_notes"])
    qa_path.write_text(
        "# QA notes\n\n"
        "- Synthetic data only; no scientific conclusion is claimed.\n"
        "- Color shows model-equal median synthetic change.\n"
        "- Hatching marks cells below the configured sign-agreement threshold.\n"
        "- Gray marks cells below the configured minimum valid-model count.\n"
        "- Plotted NetCDF, recipe copy and provenance JSON accompany the figure.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
