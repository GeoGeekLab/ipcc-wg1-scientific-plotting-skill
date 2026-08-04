from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any, Iterable, Mapping


def sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str:
    path = Path(path)
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def _git_commit(cwd: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=cwd, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _package_versions(names: Iterable[str]) -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in names:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            pass
    return versions


def build_provenance(
    *,
    inputs: Iterable[str | Path] = (),
    parameters: Mapping[str, Any] | None = None,
    citations: Iterable[str] = (),
    project_root: str | Path = ".",
    random_seed: int | None = None,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    input_records = []
    for item in inputs:
        path = Path(item)
        record: dict[str, Any] = {"path": str(path)}
        if path.is_file():
            record.update({"bytes": path.stat().st_size, "sha256": sha256_file(path)})
        else:
            record["status"] = "missing-or-nonlocal"
        input_records.append(record)

    return {
        "schema": "ipcc-sciplot-provenance/1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": _git_commit(root),
        "python": sys.version,
        "platform": platform.platform(),
        "hostname": platform.node(),
        "working_directory": str(Path.cwd()),
        "environment": {
            key: os.environ[key]
            for key in ("CONDA_DEFAULT_ENV", "VIRTUAL_ENV")
            if key in os.environ
        },
        "packages": _package_versions(
            [
                "numpy",
                "pandas",
                "matplotlib",
                "xarray",
                "scipy",
                "dask",
                "cartopy",
                "regionmask",
                "cf_xarray",
                "pint-xarray",
                "xesmf",
                "xclim",
                "pyam-iamc",
            ]
        ),
        "random_seed": random_seed,
        "parameters": dict(parameters or {}),
        "inputs": input_records,
        "citations": list(citations),
    }


def write_provenance(record: Mapping[str, Any], path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return path
