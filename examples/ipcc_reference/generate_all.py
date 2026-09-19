from __future__ import annotations

import hashlib
import json
from pathlib import Path

from reproduce_ch02_fig2_3 import main as ch02
from reproduce_ch03_fig3_2b import main as ch03
from reproduce_ch06_fig6_18_ch4 import main as ch06
from reproduce_ch10_fig10_20b import main as ch10
from sources import (
    CH2_REPO,
    CH2_SHA,
    CH3_REPO,
    CH3_SHA,
    CH6_REPO,
    CH6_SHA,
    CH10_REPO,
    CH10_SHA,
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    outputs = [ch03(), ch02(), ch10(), ch06()]
    record = {
        "schema": "ipcc-reference-reproductions/1.0",
        "sources": [
            {"repo": CH3_REPO, "commit": CH3_SHA, "figure": "AR6 WGI Figure 3.2b"},
            {"repo": CH2_REPO, "commit": CH2_SHA, "figure": "AR6 WGI Figure 2.3"},
            {"repo": CH10_REPO, "commit": CH10_SHA, "figure": "AR6 WGI Figure 10.20b"},
            {"repo": CH6_REPO, "commit": CH6_SHA, "figure": "AR6 WGI Figure 6.18 source"},
        ],
        "outputs": [
            {"path": str(path.relative_to(HERE)), "sha256": digest(path)}
            for path in outputs
        ],
        "font_fidelity": (
            "CI uses the repository font fallback when Arial is unavailable. "
            "Geometry, source data, colours and figure-specific visual grammar are still audited."
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "manifest.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
