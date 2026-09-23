from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from ipcc_sciplot import audit_figure

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def assert_reference_contract(
    fig,
    contract: dict[str, object],
    *,
    tolerance_mm: float = 0.5,
) -> dict[str, object]:
    """Validate figure geometry and semantic fields used by a reference reproduction."""
    failures: list[str] = []
    actual: dict[str, object] = {}

    expected_size = contract.get("size_mm")
    if expected_size is not None:
        width_mm, height_mm = (float(value) for value in fig.get_size_inches() * 25.4)
        actual["size_mm"] = [round(width_mm, 3), round(height_mm, 3)]
        exp_width, exp_height = (float(value) for value in expected_size)
        if abs(width_mm - exp_width) > tolerance_mm:
            failures.append(f"width: expected {exp_width} mm, got {width_mm:.3f} mm")
        if abs(height_mm - exp_height) > tolerance_mm:
            failures.append(f"height: expected {exp_height} mm, got {height_mm:.3f} mm")

    expected_panels = contract.get("panel_count")
    if expected_panels is not None:
        actual["panel_count"] = len(fig.axes)
        if len(fig.axes) != int(expected_panels):
            failures.append(
                f"panel count: expected {expected_panels}, got {len(fig.axes)}"
            )

    axes_contracts = contract.get("axes", [])
    if len(fig.axes) < len(axes_contracts):
        failures.append(
            f"axes contract count: expected at least {len(axes_contracts)}, got {len(fig.axes)}"
        )

    axes_actual: list[dict[str, object]] = []
    for index, spec in enumerate(axes_contracts):
        if index >= len(fig.axes):
            break
        ax = fig.axes[index]
        observed: dict[str, object] = {}
        axes_actual.append(observed)

        if "xlim" in spec:
            got = [float(value) for value in ax.get_xlim()]
            expected = [float(value) for value in spec["xlim"]]
            observed["xlim"] = [round(value, 6) for value in got]
            if not np.allclose(got, expected, atol=1e-6, rtol=0):
                failures.append(f"axes[{index}].xlim: expected {expected}, got {got}")

        if "ylim" in spec:
            got = [float(value) for value in ax.get_ylim()]
            expected = [float(value) for value in spec["ylim"]]
            observed["ylim"] = [round(value, 6) for value in got]
            if not np.allclose(got, expected, atol=1e-6, rtol=0):
                failures.append(f"axes[{index}].ylim: expected {expected}, got {got}")

        if "ylim_min" in spec:
            got = float(ax.get_ylim()[0])
            expected = float(spec["ylim_min"])
            observed["ylim_min"] = round(got, 6)
            if abs(got - expected) > 1e-6:
                failures.append(
                    f"axes[{index}].ylim_min: expected {expected}, got {got}"
                )

        for field, getter in (
            ("xlabel", ax.get_xlabel),
            ("ylabel", ax.get_ylabel),
        ):
            if field in spec:
                got = getter()
                expected = str(spec[field])
                observed[field] = got
                if got != expected:
                    failures.append(
                        f"axes[{index}].{field}: expected {expected!r}, got {got!r}"
                    )

        if "title" in spec:
            title_loc = str(spec.get("title_loc", "center"))
            got = ax.get_title(loc=title_loc)
            expected = str(spec["title"])
            observed["title"] = got
            observed["title_loc"] = title_loc
            if got != expected:
                failures.append(
                    f"axes[{index}].title[{title_loc}]: "
                    f"expected {expected!r}, got {got!r}"
                )

        if "bbox" in spec:
            got = [float(value) for value in ax.get_position().bounds]
            expected = [float(value) for value in spec["bbox"]]
            tol = float(spec.get("bbox_tolerance", 0.005))
            observed["bbox"] = [round(value, 6) for value in got]
            if not np.allclose(got, expected, atol=tol, rtol=0):
                failures.append(
                    f"axes[{index}].bbox: expected {expected} ± {tol}, got {got}"
                )

        projection = getattr(ax, "projection", None)
        if "projection" in spec:
            got = projection.__class__.__name__ if projection is not None else "none"
            expected = str(spec["projection"])
            observed["projection"] = got
            if got != expected:
                failures.append(
                    f"axes[{index}].projection: expected {expected}, got {got}"
                )

        if "geographic_extent" in spec:
            try:
                import cartopy.crs as ccrs
                from shapely.geometry import box
            except ImportError as exc:
                raise RuntimeError("geographic extent contract requires cartopy") from exc

            west, east, south, north = (
                float(value) for value in spec["geographic_extent"]
            )
            source_crs = ccrs.PlateCarree()
            domain = box(west, south, east, north)
            projected = ax.projection.project_geometry(domain, source_crs)
            xmin, ymin, xmax, ymax = projected.bounds
            expected = [xmin, xmax, ymin, ymax]
            got = [
                float(ax.get_xlim()[0]),
                float(ax.get_xlim()[1]),
                float(ax.get_ylim()[0]),
                float(ax.get_ylim()[1]),
            ]
            tol = float(spec.get("projected_extent_tolerance", 1.0))
            observed["geographic_extent"] = [west, east, south, north]
            observed["projected_view_bounds"] = [round(value, 3) for value in got]
            if not np.allclose(got, expected, atol=tol, rtol=0):
                failures.append(
                    f"axes[{index}].projected extent: "
                    f"expected {[round(value, 3) for value in expected]} ± {tol}, "
                    f"got {[round(value, 3) for value in got]}"
                )

        legend = ax.get_legend()
        legend_labels = (
            [text.get_text() for text in legend.get_texts()]
            if legend is not None
            else []
        )
        if "legend_labels" in spec:
            expected = [str(value) for value in spec["legend_labels"]]
            observed["legend_labels"] = legend_labels
            if legend_labels != expected:
                failures.append(
                    f"axes[{index}].legend_labels: expected {expected}, got {legend_labels}"
                )
        if "legend_contains" in spec:
            expected = [str(value) for value in spec["legend_contains"]]
            missing = [value for value in expected if value not in legend_labels]
            observed["legend_labels"] = legend_labels
            if missing:
                failures.append(
                    f"axes[{index}].legend_contains: missing {missing}"
                )

        if "line_colors" in spec:
            by_label = {
                str(line.get_label()): mcolors.to_hex(line.get_color()).upper()
                for line in ax.lines
                if str(line.get_label()) and str(line.get_label()) != "_nolegend_"
            }
            expected = {
                str(label): str(color).upper()
                for label, color in spec["line_colors"].items()
            }
            observed["line_colors"] = {
                label: by_label.get(label) for label in expected
            }
            for label, color in expected.items():
                if by_label.get(label) != color:
                    failures.append(
                        f"axes[{index}].line_colors[{label!r}]: "
                        f"expected {color}, got {by_label.get(label)}"
                    )

    actual["axes"] = axes_actual
    if failures:
        raise RuntimeError("reference contract regression:\n" + "\n".join(failures))
    return actual


def finalize(
    fig,
    stem: str,
    *,
    profile: str = "ar6-report",
    strict_dimensions: bool = True,
    metadata: dict[str, Any] | None = None,
) -> Path:
    issues = audit_figure(
        fig,
        profile=profile,
        strict_font=False,
        strict_dimensions=strict_dimensions,
        require_ipcc_colormap=False,
    )
    if issues:
        raise RuntimeError("\n".join(issues))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / f"{stem}.png"
    clean_metadata = {
        "Title": stem,
        "Subject": (
            "Reference reproduction from pinned official IPCC AR6 WGI source data"
        ),
        "Creator": "ipcc-wg1-scientific-plotting-skill",
        **(metadata or {}),
    }

    # Do not use bbox_inches="tight" here. These files are physical-size
    # regression references: 90/180 mm canvas dimensions must survive export.
    dpi = 350
    expected = tuple(round(value * dpi) for value in fig.get_size_inches())
    fig.savefig(
        output,
        dpi=dpi,
        bbox_inches=fig.bbox_inches,
        pad_inches=0,
        metadata={str(key): str(value) for key, value in clean_metadata.items()},
    )

    from PIL import Image

    with Image.open(output) as image:
        actual = image.size
    if any(abs(a - e) > 1 for a, e in zip(actual, expected, strict=True)):
        raise RuntimeError(
            f"physical-size regression: expected about {expected} px, got {actual} px"
        )

    plt.close(fig)
    return output


def mm(value: float) -> float:
    return value / 25.4


def clean_axes(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.spines["left"].set_linewidth(0.5)
    ax.tick_params(width=0.5)


def close_all() -> None:
    plt.close("all")
