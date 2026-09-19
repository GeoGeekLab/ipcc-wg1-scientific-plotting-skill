import pytest

from ipcc_sciplot.tokens import (
    AR6_REPORT_SSP,
    GENERIC_LINE_COLORS,
    WGI_GUIDE_2022_SSP,
    scenario_style,
)


def test_generic_line_palette_starts_black():
    assert GENERIC_LINE_COLORS[0] == "#000000"


def test_report_and_2022_profiles_are_not_silently_conflated():
    assert AR6_REPORT_SSP["ssp245"].color == "#EADD3D"
    assert WGI_GUIDE_2022_SSP["ssp245"].color == "#F79420"
    assert scenario_style("SSP2-4.5", profile="ar6-report").color == "#EADD3D"
    assert scenario_style("SSP2-4.5", profile="wgi-guide-2022").color == "#F79420"


def test_unknown_scenario_fails():
    with pytest.raises(KeyError):
        scenario_style("made-up")
