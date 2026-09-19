from __future__ import annotations

import matplotlib as mpl
import matplotlib.colors as mcolors

from .style import audit_text_conventions, require_arial
from .tokens import scenario_style

_ALLOWED_WIDTHS_MM = (90.0, 180.0)
_MAX_HEIGHT_MM = 250.0


def audit_figure(
    fig: mpl.figure.Figure,
    *,
    profile: str = "ar6-report",
    strict_font: bool = False,
    require_ipcc_colormap: bool = False,
    strict_dimensions: bool = False,
    dimension_tolerance_mm: float = 0.5,
) -> list[str]:
    """Audit machine-checkable parts of the AR6 WGI visual contract.

    This does not replace visual comparison with a reference figure.
    """
    issues = audit_text_conventions(fig)

    if strict_font:
        try:
            require_arial()
        except RuntimeError as exc:
            issues.append(str(exc))

    if strict_dimensions:
        width_mm, height_mm = fig.get_size_inches() * 25.4
        width_matches = any(
            abs(width_mm - target) <= dimension_tolerance_mm
            for target in _ALLOWED_WIDTHS_MM
        )
        if not width_matches:
            issues.append(
                f"figure width is {width_mm:.1f} mm; strict IPCC delivery expects 90 or 180 mm"
            )
        if height_mm > _MAX_HEIGHT_MM + dimension_tolerance_mm:
            issues.append(
                f"figure height is {height_mm:.1f} mm; strict IPCC delivery maximum is 250 mm"
            )

    for ax in fig.axes:
        for line in ax.lines:
            label = line.get_label()
            if not label or label.startswith("_"):
                continue
            normalized = label.lower()
            if normalized.startswith(("ssp", "rcp")):
                try:
                    expected = scenario_style(label, profile=profile).color
                except KeyError:
                    continue
                actual = mcolors.to_hex(line.get_color()).upper()
                if actual != expected.upper():
                    issues.append(
                        f"scenario {label!r} uses {actual}; expected {expected} for {profile}"
                    )

    if require_ipcc_colormap:
        found = False
        for ax in fig.axes:
            artists = list(ax.collections) + list(ax.images)
            for artist in artists:
                get_cmap = getattr(artist, "get_cmap", None)
                if get_cmap is None:
                    continue
                cmap = get_cmap()
                if cmap is not None and str(cmap.name).startswith("ipcc_"):
                    found = True
                    break
            if found:
                break
        if not found:
            issues.append("strict map audit found no official ipcc_* colormap artist")

    return issues
