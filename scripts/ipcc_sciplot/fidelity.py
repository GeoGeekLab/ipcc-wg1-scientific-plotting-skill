from __future__ import annotations

import matplotlib as mpl
import matplotlib.colors as mcolors

from .style import audit_text_conventions, require_arial
from .tokens import scenario_style


def audit_figure(
    fig: mpl.figure.Figure,
    *,
    profile: str = "ar6-report",
    strict_font: bool = False,
    require_ipcc_colormap: bool = False,
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
