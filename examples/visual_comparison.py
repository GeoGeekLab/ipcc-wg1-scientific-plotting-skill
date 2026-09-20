from __future__ import annotations

import argparse
import csv
import io
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples" / "visual_comparison"
OUTPUT = OUT / "ar6-source-fidelity.svg"

CH6_REPO = "IPCC-WG1/Chapter-6_Fig18"
CH6_SHA = "09d9b43fe935fc81d828147f91b717396a84fca3"
DATA_FILE = "ar6-wg1-ch6-emissions-global-data.csv"
DATA_URL = (
    f"https://raw.githubusercontent.com/{CH6_REPO}/{CH6_SHA}/{DATA_FILE}"
)

CORE_SSPS = ("SSP1-1.9", "SSP1-2.6", "SSP2-4.5", "SSP3-7.0", "SSP5-8.5")
RAW_COLORS = ("#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd")
GUESSED_COLORS = {
    "SSP1-1.9": "#24B9C7",
    "SSP1-2.6": "#2D66B3",
    "SSP2-4.5": "#F0B429",
    "SSP3-7.0": "#E45538",
    "SSP5-8.5": "#A52A2A",
}
ADAPTED_COLORS = {
    "SSP1-1.9": "#00ADCF",
    "SSP1-2.6": "#173C66",
    "SSP2-4.5": "#F79420",
    "SSP3-7.0": "#E71D25",
    "SSP5-8.5": "#951B1E",
}
STRICT_COLORS = {
    "SSP1-1.9": "#1E9684",
    "SSP1-2.6": "#1D3354",
    "SSP2-4.5": "#EADD3D",
    "SSP3-7.0": "#F21111",
    "SSP5-8.5": "#840B22",
}


def load_rows() -> tuple[list[int], list[dict[str, str]]]:
    with urlopen(DATA_URL, timeout=30) as response:
        text = response.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    rows = [
        row
        for row in reader
        if row["Region"] == "World" and row["Variable"] == "Emissions|CH4"
    ]
    if not rows:
        raise RuntimeError("pinned AR6 Chapter 6 CH4 source rows were not found")
    years = [int(name) for name in reader.fieldnames or [] if name.isdigit()]
    return years, rows


def row_series(row: dict[str, str], years: list[int]) -> list[tuple[int, float]]:
    out: list[tuple[int, float]] = []
    for year in years:
        value = row.get(str(year), "")
        if value:
            out.append((year, float(value)))
    return out


def envelope(
    rows: list[dict[str, str]],
    years: list[int],
) -> list[tuple[int, float, float]]:
    out: list[tuple[int, float, float]] = []
    for year in years:
        values = [
            float(row[str(year)])
            for row in rows
            if row.get(str(year), "")
        ]
        if values:
            out.append((year, min(values), max(values)))
    return out


def escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_svg(years: list[int], rows: list[dict[str, str]]) -> str:
    scenario_rows = {
        name: next(row for row in rows if row["Scenario"].startswith(name))
        for name in CORE_SSPS
    }
    scenarios = {
        name: row_series(row, years)
        for name, row in scenario_rows.items()
    }
    histories = [
        (
            row["Scenario"] if row["Model"] == "History" else row["Model"],
            row_series(row, years),
        )
        for row in rows
        if row["Model"] in {"CMIP5", "CMIP6", "History"}
    ]
    rcp_env = envelope([row for row in rows if row["Model"] == "RCP"], years)
    ev_env = envelope([row for row in rows if row["Model"] == "Ev5a"], years)

    width, height = 1800, 1080
    panels = [
        (60, 150, 810, 390, "A  Raw plotting", "No semantic colour contract", "raw"),
        (930, 150, 810, 390, 'B  “IPCC-ish”', "Appearance first; evidence absent", "guess"),
        (60, 590, 810, 390, "C  Adapted / IPCC-inspired", "Explicit WGI 2022 profile", "adapt"),
        (
            930,
            590,
            810,
            390,
            "D  Reference-grounded AR6",
            "Report-era semantics + audit gate",
            "strict",
        ),
    ]

    def path_for(points, sx, sy):
        return " ".join(
            f"{'M' if index == 0 else 'L'} {sx(x):.1f} {sy(y):.1f}"
            for index, (x, y) in enumerate(points)
        )

    def env_path(values, sx, sy):
        upper = [
            f"{'M' if index == 0 else 'L'} {sx(x):.1f} {sy(hi):.1f}"
            for index, (x, _lo, hi) in enumerate(values)
        ]
        lower = [
            f"L {sx(x):.1f} {sy(lo):.1f}"
            for x, lo, _hi in reversed(values)
        ]
        return " ".join([*upper, *lower, "Z"])

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<defs><pattern id="hatch" width="12" height="12" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(28)"><line x1="0" y1="0" x2="0" y2="12" '
        'stroke="#9a9a9a" stroke-width="2"/></pattern></defs>',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<g font-family="Arial, Liberation Sans, DejaVu Sans, sans-serif" fill="#121212">',
        '<text x="900" y="48" text-anchor="middle" font-size="34" font-weight="700">'
        "Same AR6 source data. Four fidelity claims.</text>",
        '<text x="900" y="82" text-anchor="middle" font-size="16" fill="#555">'
        "Official AR6 WGI Chapter 6 Figure 6.18 CH₄ source CSV · pinned commit "
        "09d9b43f…</text>",
        '<text x="900" y="111" text-anchor="middle" font-size="15" fill="#555">'
        "Only the rendering contract changes — the source rows do not.</text>",
    ]

    for panel_x, panel_y, panel_w, panel_h, title, subtitle, mode in panels:
        parts.append(
            f'<rect x="{panel_x}" y="{panel_y}" width="{panel_w}" height="{panel_h}" '
            'rx="12" fill="#fbfbfb" stroke="#d8d8d8" stroke-width="1.5"/>'
        )
        parts.append(
            f'<text x="{panel_x + 24}" y="{panel_y + 36}" font-size="23" '
            f'font-weight="700">{escape(title)}</text>'
        )
        parts.append(
            f'<text x="{panel_x + 24}" y="{panel_y + 61}" font-size="14" '
            f'fill="#666">{escape(subtitle)}</text>'
        )

        plot_x, plot_y = panel_x + 78, panel_y + 92
        plot_w, plot_h = panel_w - 108, 230

        def sx(
            value: float,
            panel_x: float = plot_x,
            panel_width: float = plot_w,
        ) -> float:
            return panel_x + (value - 1850) / 250 * panel_width

        def sy(
            value: float,
            panel_y: float = plot_y,
            panel_height: float = plot_h,
        ) -> float:
            return panel_y + panel_height - value / 950 * panel_height

        for value in (0, 200, 400, 600, 800):
            yy = sy(value)
            parts.append(
                f'<line x1="{plot_x}" y1="{yy:.1f}" x2="{plot_x + plot_w}" '
                f'y2="{yy:.1f}" stroke="#e7e7e7" stroke-width="1"/>'
            )
            parts.append(
                f'<text x="{plot_x - 10}" y="{yy + 5:.1f}" text-anchor="end" '
                f'font-size="12" fill="#666">{value}</text>'
            )
        for value in (1850, 1900, 1950, 2000, 2050, 2100):
            xx = sx(value)
            parts.append(
                f'<line x1="{xx:.1f}" y1="{plot_y}" x2="{xx:.1f}" '
                f'y2="{plot_y + plot_h}" stroke="#eeeeee" stroke-width="1"/>'
            )
            parts.append(
                f'<text x="{xx:.1f}" y="{plot_y + plot_h + 22}" text-anchor="middle" '
                f'font-size="12" fill="#666">{value}</text>'
            )

        axis_width = "1" if mode == "strict" else "1.2"
        parts.extend(
            [
                f'<line x1="{plot_x}" y1="{plot_y + plot_h}" '
                f'x2="{plot_x + plot_w}" y2="{plot_y + plot_h}" '
                f'stroke="#222" stroke-width="{axis_width}"/>',
                f'<line x1="{plot_x}" y1="{plot_y}" x2="{plot_x}" '
                f'y2="{plot_y + plot_h}" stroke="#222" stroke-width="{axis_width}"/>',
                f'<text x="{plot_x + plot_w / 2:g}" y="{plot_y + plot_h + 44}" '
                'text-anchor="middle" font-size="13">Year</text>',
                f'<text x="{plot_x - 54}" y="{plot_y + plot_h / 2:g}" '
                'text-anchor="middle" font-size="13" '
                f'transform="rotate(-90 {plot_x - 54} {plot_y + plot_h / 2:g})">'
                "CH₄ emissions (Tg CH₄ yr⁻¹)</text>",
            ]
        )

        if mode == "guess":
            parts.append(
                f'<path d="{env_path(rcp_env, sx, sy)}" fill="#d0d0d0" fill-opacity="0.22"/>'
            )
            parts.append(
                f'<path d="{env_path(rcp_env, sx, sy)}" fill="url(#hatch)" fill-opacity="0.55"/>'
            )
            parts.append(
                f'<path d="{env_path(ev_env, sx, sy)}" fill="#bdbdbd" fill-opacity="0.12"/>'
            )
        elif mode == "strict":
            parts.append(
                f'<path d="{env_path(rcp_env, sx, sy)}" fill="#111111" fill-opacity="0.10"/>'
            )
            parts.append(
                f'<path d="{env_path(ev_env, sx, sy)}" fill="#7A1E7A" fill-opacity="0.12"/>'
            )
        else:
            rcp_opacity = "0.10" if mode == "raw" else "0.12"
            ev_opacity = "0.07" if mode == "raw" else "0.10"
            parts.append(
                f'<path d="{env_path(rcp_env, sx, sy)}" fill="#777777" '
                f'fill-opacity="{rcp_opacity}"/>'
            )
            parts.append(
                f'<path d="{env_path(ev_env, sx, sy)}" fill="#8d6e8d" '
                f'fill-opacity="{ev_opacity}"/>'
            )

        for index, (_name, points) in enumerate(histories):
            dashes = ("", "8 4", "2 3", "10 3 2 3")
            dash = dashes[index % len(dashes)] if mode == "strict" else ""
            raw_history = ("#7f7f7f", "#555555", "#999999", "#333333")
            color = raw_history[index % len(raw_history)] if mode == "raw" else "#222222"
            dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
            parts.append(
                f'<path d="{path_for(points, sx, sy)}" fill="none" '
                f'stroke="{color}" stroke-width="{"1.5" if mode == "strict" else "1.35"}" '
                f'stroke-opacity="{"0.62" if mode == "guess" else "0.78"}"{dash_attr}/>'
            )

        if mode == "raw":
            colors = dict(zip(CORE_SSPS, RAW_COLORS, strict=True))
        elif mode == "guess":
            colors = GUESSED_COLORS
        elif mode == "adapt":
            colors = ADAPTED_COLORS
        else:
            colors = STRICT_COLORS

        for name in CORE_SSPS:
            parts.append(
                f'<path d="{path_for(scenarios[name], sx, sy)}" fill="none" '
                f'stroke="{colors[name]}" stroke-width="{"2.5" if mode == "strict" else "2.8"}" '
                'stroke-linecap="round" stroke-linejoin="round"/>'
            )

        legend_x, legend_y = plot_x + 6, plot_y + 10
        for index, name in enumerate(CORE_SSPS):
            column = index if index < 3 else index - 3
            row = 0 if index < 3 else 1
            xx = legend_x + column * 150
            yy = legend_y + row * 22
            parts.append(
                f'<line x1="{xx}" y1="{yy}" x2="{xx + 24}" y2="{yy}" '
                f'stroke="{colors[name]}" stroke-width="4"/>'
            )
            parts.append(
                f'<text x="{xx + 31}" y="{yy + 4}" font-size="11.5">{name}</text>'
            )

        if mode == "raw":
            badge, badge_width, badge_fill, badge_color = (
                "NO FIDELITY CLAIM", 160, "#efefef", "#333333"
            )
            note = "default colour cycle + generic styling"
        elif mode == "guess":
            badge, badge_width, badge_fill, badge_color = (
                "VISUAL RESEMBLANCE ONLY", 190, "#efefef", "#333333"
            )
            note = "guessed palette + decorative hatch"
        elif mode == "adapt":
            badge, badge_width, badge_fill, badge_color = (
                "ADAPTED PROFILE", 160, "#e8eef4", "#333333"
            )
            note = "WGI 2022 semantic SSP colours · substitutions disclosed"
        else:
            badge, badge_width, badge_fill, badge_color = (
                "REFERENCE-GROUNDED", 178, "#111111", "#ffffff"
            )
            note = "AR6 report SSP colours · history styles · RCP + ECLIPSE ranges"

        parts.append(
            f'<rect x="{panel_x + 24}" y="{panel_y + panel_h - 38}" '
            f'width="{badge_width}" height="24" rx="12" fill="{badge_fill}"/>'
        )
        parts.append(
            f'<text x="{panel_x + 34}" y="{panel_y + panel_h - 21}" '
            f'font-size="11.5" font-weight="700" fill="{badge_color}">{badge}</text>'
        )
        parts.append(
            f'<text x="{panel_x + panel_w - 24}" y="{panel_y + panel_h - 21}" '
            f'text-anchor="end" font-size="11.5" fill="#666">{escape(note)}</text>'
        )

    parts.extend(
        [
            '<text x="900" y="1030" text-anchor="middle" font-size="14" fill="#444">'
            "Source: IPCC-WG1/Chapter-6_Fig18 · ar6-wg1-ch6-emissions-global-data.csv · "
            "commit 09d9b43fe935fc81d828147f91b717396a84fca3</text>",
            '<text x="900" y="1055" text-anchor="middle" font-size="13" fill="#666">'
            "World · Emissions|CH4 · official AR6 source data; no synthetic trajectories."
            "</text>",
            "</g>",
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if the committed SVG differs from the pinned AR6 source render",
    )
    args = parser.parse_args()

    years, rows = load_rows()
    rendered = render_svg(years, rows)
    if args.check:
        committed = OUTPUT.read_text(encoding="utf-8")
        if committed != rendered:
            committed_lines = committed.splitlines()
            rendered_lines = rendered.splitlines()
            for index in range(max(len(committed_lines), len(rendered_lines))):
                left = committed_lines[index] if index < len(committed_lines) else "<missing>"
                right = rendered_lines[index] if index < len(rendered_lines) else "<missing>"
                if left != right:
                    print(f"first drift at line {index + 1}")
                    print(f"committed: {left}")
                    print(f"rendered:  {right}")
                    break
            raise SystemExit(
                "visual comparison drifted from the pinned AR6 source; "
                "run python examples/visual_comparison.py"
            )
        print(f"verified {OUTPUT}")
        return

    OUT.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(rendered, encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
