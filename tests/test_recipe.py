from pathlib import Path

import pytest

from ipcc_sciplot.recipe import FigureRecipe, load_recipe


def test_strict_map_requires_ipcc_colormap_and_projection():
    recipe = FigureRecipe(
        figure_id="x",
        question="q",
        estimand="e",
        plot_type="map",
        variable="tas",
        unit="°C",
    )
    with pytest.raises(ValueError):
        recipe.validate()


def test_adapted_map_can_omit_ipcc_assets():
    recipe = FigureRecipe(
        figure_id="x",
        question="q",
        estimand="e",
        plot_type="map",
        variable="tas",
        unit="°C",
        fidelity="adapted",
    )
    recipe.validate()


def test_template_loads(tmp_path: Path):
    path = tmp_path / "recipe.yaml"
    path.write_text(
        """
figure_id: x
question: q
estimand: e
plot_type: map
variable: tas
unit: "°C"
style_profile: ar6-report
fidelity: strict
colormap: temp_div
projection: Robinson
""".strip(),
        encoding="utf-8",
    )
    recipe = load_recipe(path)
    assert recipe.colormap == "temp_div"
    assert recipe.is_strict
