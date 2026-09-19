from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pytest

from ipcc_sciplot.style import (
    audit_text_conventions,
    axis_label,
    figure_size_inches,
    figure_width_inches,
    panel_label,
    publication_context,
    save_figure,
)


def test_ipcc_delivery_widths():
    assert figure_width_inches("single") == pytest.approx(90 / 25.4)
    assert figure_width_inches("double") == pytest.approx(180 / 25.4)


def test_ipcc_max_height():
    assert figure_size_inches("double", height_mm=250)[1] == pytest.approx(250 / 25.4)
    with pytest.raises(ValueError):
        figure_size_inches("double", height_mm=251)


def test_context_uses_ipcc_delivery_typography():
    with publication_context(width="single"):
        assert mpl.rcParams["font.size"] == pytest.approx(9)
        assert mpl.rcParams["axes.linewidth"] == pytest.approx(0.5)
        assert mpl.rcParams["savefig.dpi"] == pytest.approx(350)
    with publication_context(width="double"):
        assert mpl.rcParams["font.size"] == pytest.approx(11)


def test_axis_label_uses_parentheses():
    assert axis_label("Temperature change", "°C") == "Temperature change (°C)"


def test_audit_rejects_square_bracket_units():
    with publication_context():
        fig, ax = plt.subplots()
        ax.set_ylabel("Temperature [K]")
        warnings = audit_text_conventions(fig)
        plt.close(fig)
    assert warnings
    assert "square brackets" in warnings[0]


def test_panel_label():
    with publication_context():
        fig, ax = plt.subplots()
        artist = panel_label(ax, "a", title="Global mean")
        assert artist.get_text() == "(a) Global mean"
        assert artist.get_fontweight() == "normal"
        plt.close(fig)


def test_save_figure(tmp_path: Path):
    with publication_context():
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1])
        paths = save_figure(fig, tmp_path / "figure", close=True)
    assert {p.suffix for p in paths} == {".pdf", ".png"}
    assert all(p.stat().st_size > 0 for p in paths)


def test_strict_font_fails_cleanly_when_unavailable(monkeypatch):
    import ipcc_sciplot.style as style

    def _missing(*args, **kwargs):
        raise ValueError("missing")

    monkeypatch.setattr(style.fm, "findfont", _missing)
    with pytest.raises(RuntimeError):
        style.require_arial()
