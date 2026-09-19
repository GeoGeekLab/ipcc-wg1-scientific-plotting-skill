from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ipcc_sciplot.archetypes import plot_scenario_timeseries
from ipcc_sciplot.fidelity import audit_figure
from ipcc_sciplot.provenance import build_provenance, write_provenance
from ipcc_sciplot.style import (
    axis_label,
    ipcc_legend,
    panel_label,
    publication_context,
    save_figure,
)
from ipcc_sciplot.tokens import scenario_style

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    seed = 20260919
    rng = np.random.default_rng(seed)
    years = np.arange(2015, 2101)

    base = 1.1 + 0.004 * (years - 2015)
    series = {
        "SSP1-2.6": base + 0.004 * (years - 2015),
        "SSP2-4.5": base + 0.012 * (years - 2015),
        "SSP5-8.5": base + 0.027 * (years - 2015),
    }
    series = {
        name: values + rng.normal(0, 0.015, size=years.size)
        for name, values in series.items()
    }

    output_dir = ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)
    plotted_path = output_dir / "quickstart_plotted_data.csv"
    matrix = np.column_stack([years, *series.values()])
    header = "year," + ",".join(series)
    np.savetxt(plotted_path, matrix, delimiter=",", header=header, comments="")

    with publication_context(width="double", strict_font=False):
        fig, ax = plt.subplots()
        plot_scenario_timeseries(
            ax,
            years,
            series,
            profile="ar6-report",
            legend=False,
        )

        for name, values in series.items():
            style = scenario_style(name, profile="ar6-report")
            spread = 0.05 + 0.0015 * (years - 2015)
            ax.fill_between(
                years,
                values - spread,
                values + spread,
                color=style.color,
                alpha=0.14,
                linewidth=0,
            )

        ax.set_xlabel("Year")
        ax.set_ylabel(axis_label("Global surface temperature change", "°C"))
        panel_label(ax, "a", title="Illustrative SSP trajectories")
        ipcc_legend(ax, loc="upper left")

        issues = audit_figure(fig, profile="ar6-report")
        if issues:
            raise RuntimeError("\n".join(issues))

        outputs = save_figure(
            fig,
            output_dir / "quickstart",
            metadata={
                "Title": "Illustrative SSP trajectories",
                "Subject": "Synthetic WGI-style smoke test; not IPCC data",
            },
            close=True,
        )

    provenance = build_provenance(
        inputs=[plotted_path],
        parameters={
            "style_profile": "ar6-report",
            "fidelity": "adapted",
            "font_note": "strict_font=False in portable synthetic example",
            "scenario_colours": "AR6 final-report-era semantic tokens",
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
