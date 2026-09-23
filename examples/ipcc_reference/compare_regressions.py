from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image

STEMS = (
    "ch03_fig3_2b_scatter",
    "ch02_fig2_3_co2_proxy",
    "ch10_fig10_20b_stations",
    "ch06_fig6_18_ch4_emissions",
)


def image_metrics(baseline: Path, candidate: Path) -> dict[str, object]:
    with Image.open(baseline) as base_image, Image.open(candidate) as cand_image:
        base = base_image.convert("RGB")
        cand = cand_image.convert("RGB")
        if base.size != cand.size:
            return {
                "baseline_size": list(base.size),
                "candidate_size": list(cand.size),
                "same_size": False,
            }

        base_arr = np.asarray(base, dtype=np.float32) / 255.0
        cand_arr = np.asarray(cand, dtype=np.float32) / 255.0
        delta = np.abs(base_arr - cand_arr)

        thumb_size = (64, 64)
        base_thumb = np.asarray(
            base.resize(thumb_size, Image.Resampling.BILINEAR),
            dtype=np.float32,
        ) / 255.0
        cand_thumb = np.asarray(
            cand.resize(thumb_size, Image.Resampling.BILINEAR),
            dtype=np.float32,
        ) / 255.0

        return {
            "baseline_size": list(base.size),
            "candidate_size": list(cand.size),
            "same_size": True,
            "mean_absolute_error": round(float(delta.mean()), 8),
            "changed_pixel_fraction_gt_8": round(
                float((delta.max(axis=2) > (8.0 / 255.0)).mean()),
                8,
            ),
            "thumbnail_mean_absolute_error": round(
                float(np.abs(base_thumb - cand_thumb).mean()),
                8,
            ),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    report = {
        "schema": "ipcc-reference-image-regression/1.0",
        "figures": {},
    }
    for stem in STEMS:
        report["figures"][stem] = image_metrics(
            args.baseline / f"{stem}.png",
            args.candidate / f"{stem}.png",
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
