from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from ipcc_sciplot import axis_label, publication_context, scenario_style


def make_figure() -> plt.Figure:
    """Return a portable figure that passes the requested machine checks."""
    years = np.arange(2015, 2101)
    trajectories = {
        "SSP1-2.6": 1.1 + 0.006 * (years - 2015),
        "SSP2-4.5": 1.1 + 0.015 * (years - 2015),
        "SSP5-8.5": 1.1 + 0.030 * (years - 2015),
    }

    with publication_context(width="double", strict_font=False):
        fig, ax = plt.subplots()
        for scenario, values in trajectories.items():
            token = scenario_style(scenario, profile="ar6-report")
            ax.plot(years, values, color=token.color, label=scenario)

        ax.set_xlabel("Year")
        ax.set_ylabel(axis_label("Temperature change", "°C"))
        ax.legend()

    return fig


if __name__ == "__main__":
    make_figure().show()
