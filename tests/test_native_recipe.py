from pathlib import Path

import pytest
import yaml

from ipcc_sciplot.recipe import IPCCNativeRecipe, load_ipcc_native_recipe


def test_native_recipe_template_loads() -> None:
    recipe = load_ipcc_native_recipe(Path("templates/ipcc_native_recipe.yaml"))
    assert isinstance(recipe, IPCCNativeRecipe)
    assert recipe.figure_id == "figure_01"
    assert recipe.assessment["archetype"] == "assessment-map"
    assert recipe.ensemble["center"] == "median"
    assert recipe.output_stem == "outputs/figure_01"


def test_native_recipe_rejects_bad_two_slope(tmp_path: Path) -> None:
    payload = yaml.safe_load(Path("templates/ipcc_native_recipe.yaml").read_text(encoding="utf-8"))
    payload["visual"]["normalization"].update({"vmin": 1, "vcenter": 0, "vmax": 2})
    path = tmp_path / "bad.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    with pytest.raises(ValueError, match="vmin < vcenter < vmax"):
        load_ipcc_native_recipe(path)


def test_native_recipe_rejects_bad_agreement_threshold(tmp_path: Path) -> None:
    payload = yaml.safe_load(Path("templates/ipcc_native_recipe.yaml").read_text(encoding="utf-8"))
    payload["robustness"]["sign_agreement_threshold"] = 1.2
    path = tmp_path / "bad.yaml"
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    with pytest.raises(ValueError, match="sign_agreement_threshold"):
        load_ipcc_native_recipe(path)
