from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from ipcc_sciplot.style import (
    audit_text_conventions,
    axis_label,
    panel_label,
    publication_context,
    save_figure,
)


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
