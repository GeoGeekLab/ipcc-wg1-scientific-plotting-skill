import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from ipcc_sciplot.fidelity import AuditReport, audit_figure, audit_figure_report
from ipcc_sciplot.style import publication_context
from ipcc_sciplot.tokens import scenario_style


def test_scenario_colour_audit_passes():
    with publication_context():
        fig, ax = plt.subplots()
        token = scenario_style("SSP2-4.5", profile="ar6-report")
        ax.plot([0, 1], [0, 1], label="SSP2-4.5", color=token.color)
        assert audit_figure(fig, profile="ar6-report") == []
        plt.close(fig)


def test_scenario_colour_audit_detects_default_cycle():
    with publication_context():
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1], label="SSP2-4.5")
        issues = audit_figure(fig, profile="ar6-report")
        plt.close(fig)
    assert any("wrong semantic colour" in issue for issue in issues)


def test_strict_dimension_audit_passes_for_single_column():
    with publication_context(width="single"):
        fig, _ = plt.subplots()
        issues = audit_figure(fig, strict_dimensions=True)
        plt.close(fig)
    assert issues == []


def test_strict_dimension_audit_rejects_arbitrary_width():
    fig, _ = plt.subplots(figsize=(4, 3))
    issues = audit_figure(fig, strict_dimensions=True)
    plt.close(fig)
    assert any("does not match 90 or 180 mm" in issue for issue in issues)


def test_structured_report_exposes_schema_and_requested_checks():
    with publication_context(width="double"):
        fig, ax = plt.subplots()
        token = scenario_style("SSP2-4.5", profile="ar6-report")
        ax.plot([0, 1], [0, 1], label="SSP2-4.5", color=token.color)
        report = audit_figure_report(fig, strict_dimensions=True)
        plt.close(fig)

    assert isinstance(report, AuditReport)
    assert report.passed
    assert any(
        check.code == "delivery.width" and check.status == "pass"
        for check in report.checks
    )
    assert not any(check.code == "typography.arial" for check in report.checks)
    payload = report.to_dict()
    assert payload["schema"] == "ar6-sciplot.audit/v1"
    assert payload["passed"] is True


def test_structured_report_records_actual_and_expected_colour():
    with publication_context():
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1], label="SSP2-4.5", color="#000000")
        report = audit_figure_report(fig, profile="ar6-report")
        plt.close(fig)

    failure = next(check for check in report.failures if check.code.startswith("scenario.color."))
    assert failure.actual == "#000000"
    assert failure.expected == scenario_style("SSP2-4.5", profile="ar6-report").color.upper()



def test_reference_geometry_audit_passes():
    fig, _ = plt.subplots(1, 3, figsize=(180 / 25.4, 72 / 25.4))
    report = audit_figure_report(
        fig,
        reference_size_mm=(180, 72),
        reference_panel_count=3,
    )
    plt.close(fig)

    assert report.passed
    assert any(
        check.code == "reference.width" and check.status == "pass"
        for check in report.checks
    )
    assert any(
        check.code == "reference.height" and check.status == "pass"
        for check in report.checks
    )
    assert any(
        check.code == "reference.panel-count" and check.status == "pass"
        for check in report.checks
    )
    assert not any(check.code == "reference.manual-review" for check in report.checks)


def test_reference_geometry_audit_detects_mismatch():
    fig, _ = plt.subplots(1, 2, figsize=(180 / 25.4, 80 / 25.4))
    report = audit_figure_report(
        fig,
        reference_size_mm=(180, 72),
        reference_panel_count=3,
    )
    plt.close(fig)

    codes = {check.code for check in report.failures}
    assert "reference.height" in codes
    assert "reference.panel-count" in codes



def test_official_colormap_audit_rejects_name_only():
    fig, ax = plt.subplots()
    cmap = ListedColormap(["#000000", "#FFFFFF"], name="ipcc_temp_div")
    ax.imshow(np.array([[0.0, 1.0]]), cmap=cmap)
    report = audit_figure_report(fig, require_ipcc_colormap=True)
    plt.close(fig)

    failure = next(
        check for check in report.failures if check.code == "map.official-colormap"
    )
    assert "unverified: ipcc_temp_div" in str(failure.actual)
