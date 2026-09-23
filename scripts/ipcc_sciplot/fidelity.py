from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

import matplotlib as mpl
import matplotlib.colors as mcolors

from .style import audit_text_conventions, require_arial
from .tokens import scenario_style

_ALLOWED_WIDTHS_MM = (90.0, 180.0)
_MAX_HEIGHT_MM = 250.0

AuditStatus = Literal["pass", "fail", "skip"]


@dataclass(frozen=True)
class AuditCheck:
    """One machine-checkable item in an AR6 visual-fidelity audit."""

    code: str
    status: AuditStatus
    category: str
    message: str
    actual: str | float | None = None
    expected: str | float | None = None

    def to_dict(self) -> dict[str, str | float | None]:
        return asdict(self)


@dataclass(frozen=True)
class AuditReport:
    """Structured result of a machine-checkable AR6 visual-fidelity audit."""

    profile: str
    checks: tuple[AuditCheck, ...]

    @property
    def passed(self) -> bool:
        return not self.failures

    @property
    def failures(self) -> tuple[AuditCheck, ...]:
        return tuple(check for check in self.checks if check.status == "fail")

    @property
    def passes(self) -> tuple[AuditCheck, ...]:
        return tuple(check for check in self.checks if check.status == "pass")

    @property
    def skipped(self) -> tuple[AuditCheck, ...]:
        return tuple(check for check in self.checks if check.status == "skip")

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": "ar6-sciplot.audit/v1",
            "profile": self.profile,
            "passed": self.passed,
            "summary": {
                "passed": len(self.passes),
                "failed": len(self.failures),
                "skipped": len(self.skipped),
            },
            "checks": [check.to_dict() for check in self.checks],
        }

    def render_text(self) -> str:
        state = "PASS" if self.passed else "FAIL"
        lines = [f"AR6 fidelity audit — {state}", f"Profile: {self.profile}", ""]
        icons = {"pass": "PASS", "fail": "FAIL", "skip": "SKIP"}
        for check in self.checks:
            lines.append(f"{icons[check.status]:4}  {check.code:<28} {check.message}")
            details: list[str] = []
            if check.actual is not None:
                details.append(f"actual={check.actual}")
            if check.expected is not None:
                details.append(f"expected={check.expected}")
            if details:
                lines.append(f"      {'; '.join(details)}")
        lines.extend(
            [
                "",
                (
                    "Summary: "
                    f"{len(self.passes)} passed, "
                    f"{len(self.failures)} failed, "
                    f"{len(self.skipped)} skipped"
                ),
            ]
        )
        return "\n".join(lines)


def audit_figure_report(
    fig: mpl.figure.Figure,
    *,
    profile: str = "ar6-report",
    strict_font: bool = False,
    require_ipcc_colormap: bool = False,
    strict_dimensions: bool = False,
    dimension_tolerance_mm: float = 0.5,
    reference_size_mm: tuple[float, float] | None = None,
    reference_panel_count: int | None = None,
    reference_projection: str | None = None,
) -> AuditReport:
    """Audit requested AR6/WGI delivery, semantic, and reference geometry checks."""

    checks: list[AuditCheck] = []

    text_issues = audit_text_conventions(fig)
    if text_issues:
        checks.extend(
            AuditCheck(
                code="text.unit-convention",
                status="fail",
                category="text",
                message=issue,
                expected="units in parentheses",
            )
            for issue in text_issues
        )
    else:
        checks.append(
            AuditCheck(
                code="text.unit-convention",
                status="pass",
                category="text",
                message="axis and annotation unit syntax passed",
                expected="units in parentheses",
            )
        )

    if strict_font:
        try:
            resolved_font = require_arial()
        except RuntimeError as exc:
            checks.append(
                AuditCheck(
                    code="typography.arial",
                    status="fail",
                    category="typography",
                    message=str(exc),
                    expected="Arial available",
                )
            )
        else:
            checks.append(
                AuditCheck(
                    code="typography.arial",
                    status="pass",
                    category="typography",
                    message="strict font requirement resolved",
                    actual=resolved_font,
                    expected="Arial available",
                )
            )
    else:
        checks.append(
            AuditCheck(
                code="typography.arial",
                status="skip",
                category="typography",
                message="strict font check not requested",
                expected="Arial available for strict fidelity",
            )
        )

    width_mm, height_mm = (float(value) for value in fig.get_size_inches() * 25.4)
    if strict_dimensions:
        width_matches = any(
            abs(width_mm - target) <= dimension_tolerance_mm
            for target in _ALLOWED_WIDTHS_MM
        )
        checks.append(
            AuditCheck(
                code="delivery.width",
                status="pass" if width_matches else "fail",
                category="delivery",
                message=(
                    "figure width matches an IPCC delivery width"
                    if width_matches
                    else "figure width does not match 90 or 180 mm"
                ),
                actual=round(width_mm, 2),
                expected="90 or 180 mm",
            )
        )
        height_ok = height_mm <= _MAX_HEIGHT_MM + dimension_tolerance_mm
        checks.append(
            AuditCheck(
                code="delivery.height",
                status="pass" if height_ok else "fail",
                category="delivery",
                message=(
                    "figure height is within the delivery maximum"
                    if height_ok
                    else "figure height exceeds the 250 mm delivery maximum"
                ),
                actual=round(height_mm, 2),
                expected="<= 250 mm",
            )
        )
    else:
        checks.extend(
            [
                AuditCheck(
                    code="delivery.width",
                    status="skip",
                    category="delivery",
                    message="strict delivery-width check not requested",
                    actual=round(width_mm, 2),
                    expected="90 or 180 mm for strict fidelity",
                ),
                AuditCheck(
                    code="delivery.height",
                    status="skip",
                    category="delivery",
                    message="strict delivery-height check not requested",
                    actual=round(height_mm, 2),
                    expected="<= 250 mm for strict fidelity",
                ),
            ]
        )

    if reference_size_mm is not None:
        if len(reference_size_mm) != 2 or any(value <= 0 for value in reference_size_mm):
            raise ValueError("reference_size_mm must contain positive (width, height) values")
        reference_width, reference_height = (float(value) for value in reference_size_mm)
        width_matches = abs(width_mm - reference_width) <= dimension_tolerance_mm
        height_matches = abs(height_mm - reference_height) <= dimension_tolerance_mm
        checks.extend(
            [
                AuditCheck(
                    code="reference.width",
                    status="pass" if width_matches else "fail",
                    category="reference",
                    message="figure width matches reference" if width_matches else "figure width differs from reference",
                    actual=round(width_mm, 2),
                    expected=round(reference_width, 2),
                ),
                AuditCheck(
                    code="reference.height",
                    status="pass" if height_matches else "fail",
                    category="reference",
                    message="figure height matches reference" if height_matches else "figure height differs from reference",
                    actual=round(height_mm, 2),
                    expected=round(reference_height, 2),
                ),
            ]
        )

    panel_axes = tuple(
        ax
        for ax in fig.axes
        if ax.get_label() != "<colorbar>" and getattr(ax, "_colorbar", None) is None
    )
    if reference_panel_count is not None:
        if reference_panel_count < 1:
            raise ValueError("reference_panel_count must be >= 1")
        panel_count = len(panel_axes)
        panels_match = panel_count == reference_panel_count
        checks.append(
            AuditCheck(
                code="reference.panel-count",
                status="pass" if panels_match else "fail",
                category="reference",
                message="panel count matches reference" if panels_match else "panel count differs from reference",
                actual=float(panel_count),
                expected=float(reference_panel_count),
            )
        )

    if reference_projection is not None:
        projection_names = [
            ax.projection.__class__.__name__
            for ax in panel_axes
            if getattr(ax, "projection", None) is not None
        ]
        projections_match = bool(projection_names) and all(
            name.casefold() == reference_projection.casefold() for name in projection_names
        )
        checks.append(
            AuditCheck(
                code="reference.projection",
                status="pass" if projections_match else "fail",
                category="reference",
                message=(
                    "map projection matches reference"
                    if projections_match
                    else "map projection differs from reference"
                ),
                actual=", ".join(sorted(set(projection_names))) if projection_names else "none",
                expected=reference_projection,
            )
        )

    semantic_lines = 0
    for ax_index, ax in enumerate(fig.axes):
        for line_index, line in enumerate(ax.lines):
            label = line.get_label()
            if not label or label.startswith("_"):
                continue
            normalized = label.lower()
            if not normalized.startswith(("ssp", "rcp")):
                continue
            try:
                expected = scenario_style(label, profile=profile).color
            except KeyError:
                checks.append(
                    AuditCheck(
                        code=f"scenario.unknown.{ax_index}.{line_index}",
                        status="skip",
                        category="semantics",
                        message=f"no registered semantic colour for scenario {label!r}",
                        actual=label,
                    )
                )
                continue

            semantic_lines += 1
            actual = mcolors.to_hex(line.get_color()).upper()
            matches = actual == expected.upper()
            checks.append(
                AuditCheck(
                    code=f"scenario.color.{ax_index}.{line_index}",
                    status="pass" if matches else "fail",
                    category="semantics",
                    message=(
                        f"scenario {label!r} uses the {profile} semantic colour"
                        if matches
                        else f"scenario {label!r} uses the wrong semantic colour"
                    ),
                    actual=actual,
                    expected=expected.upper(),
                )
            )

    if semantic_lines == 0:
        checks.append(
            AuditCheck(
                code="scenario.colors",
                status="skip",
                category="semantics",
                message="no registered SSP/RCP line labels found",
                expected=f"semantic scenario colours for {profile} when applicable",
            )
        )

    if require_ipcc_colormap:
        found_names: list[str] = []
        for ax in fig.axes:
            artists = list(ax.collections) + list(ax.images)
            for artist in artists:
                get_cmap = getattr(artist, "get_cmap", None)
                if get_cmap is None:
                    continue
                cmap = get_cmap()
                if cmap is not None and str(cmap.name).startswith("ipcc_"):
                    found_names.append(str(cmap.name))
        checks.append(
            AuditCheck(
                code="map.official-colormap",
                status="pass" if found_names else "fail",
                category="semantics",
                message=(
                    "official IPCC colormap artist found"
                    if found_names
                    else "strict map audit found no official ipcc_* colormap artist"
                ),
                actual=", ".join(sorted(set(found_names))) if found_names else "none",
                expected="at least one official ipcc_* colormap artist",
            )
        )
    else:
        checks.append(
            AuditCheck(
                code="map.official-colormap",
                status="skip",
                category="semantics",
                message="official map-colormap check not requested",
                expected="official ipcc_* colormap for strict map fidelity",
            )
        )

    return AuditReport(profile=profile, checks=tuple(checks))


def audit_figure(
    fig: mpl.figure.Figure,
    *,
    profile: str = "ar6-report",
    strict_font: bool = False,
    require_ipcc_colormap: bool = False,
    strict_dimensions: bool = False,
    dimension_tolerance_mm: float = 0.5,
    reference_size_mm: tuple[float, float] | None = None,
    reference_panel_count: int | None = None,
    reference_projection: str | None = None,
) -> list[str]:
    """Return failure messages for compatibility with the original API."""

    report = audit_figure_report(
        fig,
        profile=profile,
        strict_font=strict_font,
        require_ipcc_colormap=require_ipcc_colormap,
        strict_dimensions=strict_dimensions,
        dimension_tolerance_mm=dimension_tolerance_mm,
        reference_size_mm=reference_size_mm,
        reference_panel_count=reference_panel_count,
        reference_projection=reference_projection,
    )
    return [check.message for check in report.failures]
