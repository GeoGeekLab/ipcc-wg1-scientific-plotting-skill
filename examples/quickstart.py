from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ipcc_sciplot.provenance import build_provenance, write_provenance
from ipcc_sciplot.style import publication_context, save_figure
from ipcc_sciplot.uncertainty import ensemble_summary


def main() -> None:
    seed = 20260804
    rng = np.random.default_rng(seed)
    years = np.arange(1950, 2101)
    models = [f"M{i:02d}" for i in range(12)]
    forced = 0.012 * (years - 1950)
    noise = rng.normal(0, 0.18, size=(len(models), len(years)))
    offsets = rng.normal(0, 0.08, size=(len(models), 1))
    values = forced[None, :] + noise + offsets
    da = xr.DataArray(
        values,
        coords={"model": models, "year": years},
        dims=("model", "year"),
        name="temperature_change",
        attrs={"units": "K", "baseline": "1950"},
    )
    summary = ensemble_summary(da, dim="model", min_count=5)

    output_dir = ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)
    plotted_path = output_dir / "quickstart_plotted_data.nc"
    summary.to_netcdf(plotted_path)

    with publication_context(width="double"):
        fig, ax = plt.subplots()
        ax.fill_between(
            years,
            summary["lower"].values,
            summary["upper"].values,
            alpha=0.25,
            linewidth=0,
            label="17-83% model range",
        )
        ax.plot(years, summary["center"].values, label="Model-equal median")
        ax.axvline(2020, linewidth=0.8, linestyle="--")
        ax.set(xlabel="Year", ylabel="Temperature change [K]", title="Synthetic ensemble example")
        ax.legend(loc="upper left")
        outputs = save_figure(
            fig,
            output_dir / "quickstart",
            metadata={"Title": "Synthetic ensemble example", "Subject": "Skill smoke test"},
            close=True,
        )

    provenance = build_provenance(
        inputs=[plotted_path],
        parameters={
            "center": "median",
            "interval": [0.17, 0.83],
            "sign_agreement": 0.80,
            "minimum_valid_count": 5,
        },
        random_seed=seed,
        project_root=ROOT,
    )
    write_provenance(provenance, output_dir / "quickstart.provenance.json")
    print("Created:")
    for path in [plotted_path, *outputs, output_dir / "quickstart.provenance.json"]:
        print(f"  {path}")


if __name__ == "__main__":
    main()
