from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# These imports resolve from the repository when the script is run with
# `python -m pip install -e .` (or from the published package).
from ipcc_sciplot.style import axis_label
from ipcc_sciplot.tokens import scenario_style

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "visual_comparison"


def synthetic_series() -> tuple[np.ndarray, dict[str, np.ndarray]]:
    years = np.arange(2015, 2101)
    t = years - 2015
    wiggle = 0.018 * np.sin(t / 4.5)
    series = {
        "SSP1-2.6": 1.08 + 0.010 * t - 0.000055 * t**2 + wiggle,
        "SSP2-4.5": 1.08 + 0.016 * t - 0.000035 * t**2 + wiggle * 0.8,
        "SSP5-8.5": 1.08 + 0.030 * t - 0.000020 * t**2 + wiggle * 0.6,
    }
    return years, series


def finish_axes(ax: plt.Axes) -> None:
    ax.set_xlim(2015, 2100)
    ax.set_xticks([2020, 2040, 2060, 2080, 2100])
    ax.tick_params(axis="both", labelsize=8)


def add_status(ax: plt.Axes, lines: list[str]) -> None:
    ax.text(
        0.02,
        0.03,
        "\n".join(lines),
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=7.2,
        linespacing=1.35,
        bbox={
            "boxstyle": "round,pad=0.35",
            "facecolor": "white",
            "edgecolor": "0.75",
            "alpha": 0.95,
        },
    )


def panel_default(ax: plt.Axes, years: np.ndarray, series: dict[str, np.ndarray]) -> None:
    for name, values in series.items():
        ax.plot(years, values, label=name, linewidth=1.8)
    ax.set_title("1  Matplotlib default", loc="left", fontsize=11, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature change [°C]")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, loc="upper left")
    finish_axes(ax)
    add_status(ax, ["implicit color cycle", "unit grammar: generic", "fidelity claim: none"])


def panel_ipccish(ax: plt.Axes, years: np.ndarray, series: dict[str, np.ndarray]) -> None:
    guessed = {
        "SSP1-2.6": "#2A6FDB",
        "SSP2-4.5": "#F0B429",
        "SSP5-8.5": "#C73E1D",
    }
    for name, values in series.items():
        ax.plot(years, values, label=name, color=guessed[name], linewidth=2.0)
    center = series["SSP2-4.5"]
    ax.fill_between(years, center - 0.16, center + 0.16, color="#999999", alpha=0.22, hatch="///")
    ax.set_title("2  “IPCC-ish”", loc="left", fontsize=11, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature change (°C)")
    ax.legend(fontsize=7, loc="upper left", frameon=False)
    finish_axes(ax)
    add_status(
        ax,
        [
            "colors guessed by appearance",
            "hatching added decoratively",
            "evidence / provenance: absent",
        ],
    )


def panel_adapted(ax: plt.Axes, years: np.ndarray, series: dict[str, np.ndarray]) -> None:
    for name, values in series.items():
        token = scenario_style(name, profile="wgi-guide-2022")
        ax.plot(years, values, label=name, color=token.color, linewidth=1.25)
    ax.set_title("3  Adapted / IPCC-inspired", loc="left", fontsize=11, fontweight="normal")
    ax.set_xlabel("Year")
    ax.set_ylabel(axis_label("Temperature change", "°C"))
    legend = ax.legend(fontsize=7, loc="upper left", frameon=True, fancybox=False)
    legend.get_frame().set_linewidth(0.5)
    for spine in ax.spines.values():
        spine.set_linewidth(0.5)
    ax.tick_params(width=0.5)
    finish_axes(ax)
    add_status(ax, ["profile: wgi-guide-2022", "semantic SSP colors", "substitutions disclosed"])


def panel_strict(ax: plt.Axes, years: np.ndarray, series: dict[str, np.ndarray]) -> None:
    for name, values in series.items():
        token = scenario_style(name, profile="ar6-report")
        ax.plot(years, values, label=name, color=token.color, linewidth=1.0)
    ax.set_title(
        "4  Strict contract / fidelity-aware",
        loc="left",
        fontsize=11,
        fontweight="normal",
    )
    ax.set_xlabel("Year")
    ax.set_ylabel(axis_label("Temperature change", "°C"))
    legend = ax.legend(fontsize=7, loc="upper left", frameon=True, fancybox=False, framealpha=1)
    legend.get_frame().set_edgecolor("black")
    legend.get_frame().set_linewidth(0.5)
    for spine in ax.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color("black")
    ax.tick_params(width=0.5)
    finish_axes(ax)
    add_status(
        ax,
        [
            "profile: ar6-report",
            "semantic colors + audit gate",
            "strict typography: Arial required locally",
        ],
    )


def make_comparison() -> plt.Figure:
    years, series = synthetic_series()
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.8))
    fig.subplots_adjust(left=0.07, right=0.985, top=0.89, bottom=0.12, wspace=0.14, hspace=0.32)
    panel_default(axes[0, 0], years, series)
    panel_ipccish(axes[0, 1], years, series)
    panel_adapted(axes[1, 0], years, series)
    panel_strict(axes[1, 1], years, series)
    fig.suptitle(
        "From “IPCC-ish” styling to evidence-backed visual fidelity",
        fontsize=15,
        fontweight="bold",
    )
    fig.text(
        0.5,
        0.025,
        "Synthetic trajectories for visual comparison only — not IPCC data. "
        "Strict IPCC-faithful output additionally requires satisfying the local font "
        "and reference-specific gates.",
        ha="center",
        va="bottom",
        fontsize=8,
    )
    return fig


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig = make_comparison()
    png = OUT / "default-to-fidelity.png"
    svg = OUT / "default-to-fidelity.svg"
    fig.savefig(png, dpi=135, bbox_inches="tight", facecolor="white")
    fig.savefig(svg, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(png)
    print(svg)


if __name__ == "__main__":
    main()
