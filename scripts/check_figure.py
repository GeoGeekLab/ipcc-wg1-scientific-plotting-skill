#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Static preflight for a scientific figure artifact.")
    parser.add_argument("figure", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--min-bytes", type=int, default=5_000)
    args = parser.parse_args()

    problems: list[str] = []
    if not args.figure.is_file():
        problems.append(f"missing figure: {args.figure}")
    elif args.figure.stat().st_size < args.min_bytes:
        problems.append(f"figure is suspiciously small: {args.figure.stat().st_size} bytes")
    if args.figure.suffix.lower() not in {".pdf", ".svg", ".png", ".tif", ".tiff"}:
        problems.append("unsupported or non-publication output format")

    if args.metadata:
        if not args.metadata.is_file():
            problems.append(f"missing metadata: {args.metadata}")
        else:
            try:
                record = json.loads(args.metadata.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                problems.append(f"invalid JSON metadata: {exc}")
            else:
                for key in ("schema", "created_utc", "parameters", "inputs", "packages"):
                    if key not in record:
                        problems.append(f"metadata missing required key: {key}")
                if not record.get("inputs"):
                    problems.append("metadata has no input records")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1
    print("PASS: static figure preflight")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
