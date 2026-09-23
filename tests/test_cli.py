from __future__ import annotations

import json
from pathlib import Path

from ipcc_sciplot.cli import main


def _write_factory(path: Path, *, semantic_color: bool) -> None:
    color_line = (
        'token = scenario_style("SSP2-4.5", profile="ar6-report")\n'
        '        color = token.color'
        if semantic_color
        else 'color = "#000000"'
    )
    path.write_text(
        f"""
import matplotlib.pyplot as plt

from ipcc_sciplot import axis_label, publication_context, scenario_style


def make_figure():
    with publication_context(width="double", strict_font=False):
        fig, ax = plt.subplots()
        {color_line}
        ax.plot([2020, 2100], [1.2, 2.4], color=color, label="SSP2-4.5")
        ax.set_ylabel(axis_label("Temperature change", "°C"))
    return fig
""",
        encoding="utf-8",
    )


def test_cli_audit_text_passes(tmp_path, capsys):
    script = tmp_path / "figure.py"
    _write_factory(script, semantic_color=True)

    code = main(["audit", str(script), "--strict-dimensions"])

    output = capsys.readouterr().out
    assert code == 0
    assert "AR6 fidelity audit — PASS" in output
    assert "delivery.width" in output
    assert "scenario.color" in output


def test_cli_audit_failure_returns_one(tmp_path, capsys):
    script = tmp_path / "figure.py"
    _write_factory(script, semantic_color=False)

    code = main(["audit", str(script), "--strict-dimensions"])

    output = capsys.readouterr().out
    assert code == 1
    assert "AR6 fidelity audit — FAIL" in output
    assert "wrong semantic colour" in output


def test_cli_json_report_is_machine_readable(tmp_path, capsys):
    script = tmp_path / "figure.py"
    _write_factory(script, semantic_color=True)

    code = main(["audit", str(script), "--strict-dimensions", "--format", "json"])

    payload = json.loads(capsys.readouterr().out)
    assert code == 0
    assert payload["schema"] == "ar6-sciplot.audit/v1"
    assert payload["passed"] is True
    assert payload["summary"]["failed"] == 0



def test_cli_reference_geometry_checks(tmp_path, capsys):
    script = tmp_path / "figure.py"
    _write_factory(script, semantic_color=True)

    code = main(
        [
            "audit",
            str(script),
            "--reference-size-mm",
            "180",
            str(180 * 0.62),
            "--reference-panel-count",
            "1",
        ]
    )

    output = capsys.readouterr().out
    assert code == 0
    assert "reference.width" in output
    assert "reference.height" in output
    assert "reference.panel-count" in output
