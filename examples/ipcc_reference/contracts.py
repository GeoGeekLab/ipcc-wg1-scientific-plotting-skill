from __future__ import annotations

REFERENCE_CONTRACTS: dict[str, dict[str, object]] = {
    "ch03_fig3_2b_scatter": {
        "figure": "AR6 WGI Figure 3.2b",
        "size_mm": [90.0, 120.0],
        "panel_count": 1,
        "axes": [
            {
                "xlim": [-11.0, 20.0],
                "ylim": [-15.0, 25.0],
                "xlabel": "Temperature change over sea (°C)",
                "ylabel": "Temperature change over land (°C)",
                "title": "b) Global temperature change over\nland and ocean for a range of climates",
                "bbox": [0.23, 0.12, 0.73, 0.78],
                "bbox_tolerance": 0.005,
                "legend_contains": [
                    "Instrumental",
                    "Reconstruction",
                    "Fit to data",
                    "CMIP6 models",
                    "CMIP5 models",
                    "non-CMIP models",
                    "CMIP6 mean",
                ],
            }
        ],
    },
    "ch06_fig6_18_ch4_emissions": {
        "figure": "AR6 WGI Figure 6.18 source",
        "size_mm": [180.0, 92.0],
        "panel_count": 1,
        "axes": [
            {
                "xlim": [1850.0, 2100.0],
                "ylim_min": 0.0,
                "xlabel": "Year",
                "ylabel": "CH$_4$ emissions (Tg (CH$_4$) yr$^{-1}$)",
                "title": "CH$_4$",
                "legend_contains": [
                    "SSP1-1.9",
                    "SSP1-2.6",
                    "SSP2-4.5",
                    "SSP3-7.0",
                    "SSP5-8.5",
                ],
                "line_colors": {
                    "SSP1-1.9": "#1E9684",
                    "SSP1-2.6": "#1D3354",
                    "SSP2-4.5": "#EADD3D",
                    "SSP3-7.0": "#F21111",
                    "SSP5-8.5": "#840B22",
                },
            }
        ],
    },
    "ch10_fig10_20b_stations": {
        "figure": "AR6 WGI Figure 10.20b",
        "size_mm": [90.0, 72.0],
        "panel_count": 1,
        "axes": [
            {
                "projection": "LambertConformal",
                "extent": [-10.0, 40.0, 25.0, 50.0],
                "extent_tolerance": 0.15,
                "title": "Station locations",
                "legend_labels": ["E-OBS", "Donat et al. 2014"],
            }
        ],
    },
}
