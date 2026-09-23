import matplotlib.pyplot as plt
import pytest

from ipcc_sciplot import add_uncertainty_legend, label_line_ends, map_panel_grid


def test_map_panel_grid_uses_requested_delivery_size():
    fig, axes = map_panel_grid(
        3,
        ncols=3,
        width="double",
        height_mm=72,
    )
    size_mm = fig.get_size_inches() * 25.4
    assert len(axes) == 3
    assert size_mm[0] == pytest.approx(180)
    assert size_mm[1] == pytest.approx(72)
    plt.close(fig)


def test_map_panel_grid_removes_unused_axes():
    fig, axes = map_panel_grid(4, ncols=3, width="double", height_mm=120)
    assert len(axes) == 4
    assert len(fig.axes) == 4
    plt.close(fig)


def test_uncertainty_legend_builds_requested_entries():
    fig, ax = plt.subplots()
    legend = add_uncertainty_legend(
        ax,
        low_agreement="Low agreement",
        insufficient_data="Insufficient data",
        significance="Significant",
    )
    labels = [text.get_text() for text in legend.get_texts()]
    assert labels == ["Low agreement", "Insufficient data", "Significant"]
    assert legend.get_frame().get_facecolor()[-1] == pytest.approx(1)
    assert legend.get_frame().get_linewidth() == pytest.approx(0)
    plt.close(fig)


def test_uncertainty_legend_requires_an_entry():
    fig, ax = plt.subplots()
    with pytest.raises(ValueError):
        add_uncertainty_legend(ax)
    plt.close(fig)



def test_line_end_labels_are_separated():
    fig, ax = plt.subplots(figsize=(6, 3))
    (a,) = ax.plot([0, 1], [0, 1.00], label="A")
    (b,) = ax.plot([0, 1], [0, 1.01], label="B")
    labels = label_line_ends(
        ax,
        {"A": a, "B": b},
        min_gap_points=2,
    )
    fig.canvas.draw()

    renderer = fig.canvas.get_renderer()
    a_box = labels["A"].get_window_extent(renderer=renderer)
    b_box = labels["B"].get_window_extent(renderer=renderer)
    assert not a_box.overlaps(b_box)
    plt.close(fig)


def test_line_end_labels_skip_empty_lines():
    fig, ax = plt.subplots()
    (line,) = ax.plot([], [], label="empty")
    assert label_line_ends(ax, {"empty": line}) == {}
    plt.close(fig)
