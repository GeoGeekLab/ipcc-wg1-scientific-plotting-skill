from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

from ipcc_sciplot import audit_figure

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


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
