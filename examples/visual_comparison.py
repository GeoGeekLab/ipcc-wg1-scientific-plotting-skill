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



def _svg_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def write_compact_svg(path: Path) -> None:
    """Write a compact, deterministic SVG version of the comparison asset."""
    years, series = synthetic_series()
    width, height = 1600, 1000
    panel_w, panel_h = 700, 350
    panel_positions = [(70, 115), (830, 115), (70, 545), (830, 545)]
    x_min, x_max = 2015.0, 2100.0
    y_min, y_max = 1.0, 3.55
    x_ticks = [2020, 2040, 2060, 2080, 2100]
    y_ticks = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]

    default_colors = {
        "SSP1-2.6": "#1f77b4",
        "SSP2-4.5": "#ff7f0e",
        "SSP5-8.5": "#2ca02c",
    }
    guessed_colors = {
        "SSP1-2.6": "#2A6FDB",
        "SSP2-4.5": "#F0B429",
        "SSP5-8.5": "#C73E1D",
    }
    adapted_colors = {
        name: scenario_style(name, profile="wgi-guide-2022").color for name in series
    }
    strict_colors = {
        name: scenario_style(name, profile="ar6-report").color for name in series
    }

    panels = [
        (
            "1  Matplotlib default",
            default_colors,
            ["implicit color cycle", "unit grammar: generic", "fidelity claim: none"],
            True,
            "Temperature change [°C]",
        ),
        (
            '2  "IPCC-ish"',
            guessed_colors,
            [
                "colors guessed by appearance",
                "hatching added decoratively",
                "evidence / provenance: absent",
            ],
            False,
            "Temperature change (°C)",
        ),
        (
            "3  Adapted / IPCC-inspired",
            adapted_colors,
            ["profile: wgi-guide-2022", "semantic SSP colors", "substitutions disclosed"],
            False,
            "Temperature change (°C)",
        ),
        (
            "4  Strict contract / fidelity-aware",
            strict_colors,
            [
                "profile: ar6-report",
                "semantic colors + audit gate",
                "strict typography: Arial required locally",
            ],
            False,
            "Temperature change (°C)",
        ),
    ]

    def sx(year: float, plot_x: float, plot_w: float) -> float:
        return plot_x + (year - x_min) / (x_max - x_min) * plot_w

    def sy(value: float, plot_y: float, plot_h: float) -> float:
        return plot_y + plot_h - (value - y_min) / (y_max - y_min) * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        "<defs>",
        '<pattern id="hatch" width="12" height="12" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(25)">',
        '<rect width="12" height="12" fill="#eeeeee" fill-opacity="0.75"/>',
        '<line x1="0" y1="0" x2="0" y2="12" stroke="#cccccc" stroke-width="2"/>',
        "</pattern>",
        "</defs>",
        '<rect width="100%" height="100%" fill="white"/>',
        '<g font-family="Arial, Liberation Sans, DejaVu Sans, sans-serif" fill="#111">',
        '<text x="800" y="48" text-anchor="middle" font-size="30" font-weight="700">'
        "From &quot;IPCC-ish&quot; styling to evidence-backed visual fidelity</text>",
    ]

    for idx, ((px, py), panel) in enumerate(zip(panel_positions, panels, strict=True)):
        title, colors, status, show_grid, ylabel = panel
        plot_x, plot_y = px + 70, py + 48
        plot_w, plot_h = panel_w - 92, panel_h - 105

        parts.append(
            f'<text x="{px}" y="{py + 20}" font-size="22" '
            f'font-weight="{700 if idx < 2 else 400}">{_svg_escape(title)}</text>'
        )

        if show_grid:
            for xt in x_ticks:
                xx = sx(xt, plot_x, plot_w)
                parts.append(
                    f'<line x1="{xx:.1f}" y1="{plot_y:.1f}" x2="{xx:.1f}" '
                    f'y2="{plot_y + plot_h:.1f}" stroke="#dddddd" stroke-width="1"/>'
                )
            for yt in y_ticks:
                yy = sy(yt, plot_y, plot_h)
                parts.append(
                    f'<line x1="{plot_x:.1f}" y1="{yy:.1f}" '
                    f'x2="{plot_x + plot_w:.1f}" y2="{yy:.1f}" '
                    'stroke="#dddddd" stroke-width="1"/>'
                )

        axis_width = 1.0 if idx < 2 else 0.8
        parts.extend(
            [
                f'<rect x="{plot_x}" y="{plot_y}" width="{plot_w}" height="{plot_h}" '
                f'fill="none" stroke="#111" stroke-width="{axis_width}"/>',
                f'<text x="{plot_x + plot_w / 2:.1f}" y="{plot_y + plot_h + 40:.1f}" '
                'font-size="16" text-anchor="middle">Year</text>',
                f'<text x="{plot_x - 50:.1f}" y="{plot_y + plot_h / 2:.1f}" '
                'font-size="16" text-anchor="middle" '
                f'transform="rotate(-90 {plot_x - 50:.1f} {plot_y + plot_h / 2:.1f})">'
                f"{_svg_escape(ylabel)}</text>",
            ]
        )

        for xt in x_ticks:
            xx = sx(xt, plot_x, plot_w)
            parts.append(
                f'<line x1="{xx:.1f}" y1="{plot_y + plot_h:.1f}" x2="{xx:.1f}" '
                f'y2="{plot_y + plot_h + 6:.1f}" stroke="#111" stroke-width="{axis_width}"/>'
            )
            parts.append(
                f'<text x="{xx:.1f}" y="{plot_y + plot_h + 23:.1f}" '
                f'font-size="13" text-anchor="middle">{xt}</text>'
            )
        for yt in y_ticks:
            yy = sy(yt, plot_y, plot_h)
            parts.append(
                f'<line x1="{plot_x - 6:.1f}" y1="{yy:.1f}" x2="{plot_x:.1f}" '
                f'y2="{yy:.1f}" stroke="#111" stroke-width="{axis_width}"/>'
            )
            parts.append(
                f'<text x="{plot_x - 10:.1f}" y="{yy + 5:.1f}" '
                f'font-size="13" text-anchor="end">{yt:.1f}</text>'
            )

        if idx == 1:
            center = series["SSP2-4.5"]
            upper = center + 0.16
            lower = center - 0.16
            upper_pts = [
                f"{sx(float(x), plot_x, plot_w):.1f},{sy(float(y), plot_y, plot_h):.1f}"
                for x, y in zip(years, upper, strict=True)
            ]
            lower_pts = [
                f"{sx(float(x), plot_x, plot_w):.1f},{sy(float(y), plot_y, plot_h):.1f}"
                for x, y in zip(years[::-1], lower[::-1], strict=True)
            ]
            parts.append(
                f'<polygon points="{" ".join(upper_pts + lower_pts)}" fill="url(#hatch)" '
                'stroke="none"/>'
            )

        for name, values in series.items():
            points = " ".join(
                f"{sx(float(x), plot_x, plot_w):.1f},{sy(float(y), plot_y, plot_h):.1f}"
                for x, y in zip(years, values, strict=True)
            )
            line_width = 3.2 if idx < 2 else (2.1 if idx == 2 else 1.8)
            parts.append(
                f'<polyline points="{points}" fill="none" stroke="{colors[name]}" '
                f'stroke-width="{line_width}" stroke-linejoin="round"/>'
            )

        legend_x, legend_y = plot_x + 10, plot_y + 12
        parts.append(
            f'<rect x="{legend_x}" y="{legend_y}" width="110" height="67" '
            'fill="white" fill-opacity="0.94" stroke="#bbbbbb" stroke-width="0.7"/>'
        )
        for j, name in enumerate(series):
            yy = legend_y + 17 + j * 19
            parts.append(
                f'<line x1="{legend_x + 8}" y1="{yy}" x2="{legend_x + 32}" y2="{yy}" '
                f'stroke="{colors[name]}" stroke-width="3"/>'
            )
            parts.append(
                f'<text x="{legend_x + 38}" y="{yy + 4}" font-size="12">'
                f"{_svg_escape(name)}</text>"
            )

        status_x, status_y = plot_x + 10, plot_y + plot_h - 61
        status_w = 215 if idx != 3 else 245
        parts.append(
            f'<rect x="{status_x}" y="{status_y}" width="{status_w}" height="55" '
            'rx="5" fill="white" fill-opacity="0.95" stroke="#bbbbbb" stroke-width="0.8"/>'
        )
        for j, line in enumerate(status):
            parts.append(
                f'<text x="{status_x + 7}" y="{status_y + 15 + j * 16}" font-size="12">'
                f"{_svg_escape(line)}</text>"
            )

    parts.extend(
        [
            '<text x="800" y="962" text-anchor="middle" font-size="14">'
            "Synthetic trajectories for visual comparison only — not IPCC data. "
            "Strict IPCC-faithful output additionally requires satisfying local font "
            "and reference-specific gates.</text>",
            "</g>",
            "</svg>",
        ]
    )
    path.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig = make_comparison()
    png = OUT / "default-to-fidelity.png"
    svg = OUT / "default-to-fidelity.svg"
    fig.savefig(png, dpi=135, bbox_inches="tight", facecolor="white")
    write_compact_svg(svg)
    plt.close(fig)
    print(png)
    print(svg)


if __name__ == "__main__":
    main()
