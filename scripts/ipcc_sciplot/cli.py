from __future__ import annotations

import argparse
import json
import runpy
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import matplotlib as mpl

from .fidelity import AuditReport, audit_figure_report


def _load_figure(script: Path, factory_name: str) -> mpl.figure.Figure:
    if not script.is_file():
        raise ValueError(f"figure script does not exist: {script}")

    mpl.use("Agg")\n    namespace = runpy.run_path(str(script))
    factory: Any = namespace.get(factory_name)
    if factory is None:
        raise ValueError(f"{script} does not define {factory_name}()")
    if not callable(factory):
        raise ValueError(f"{factory_name} in {script} is not callable")

    figure = factory()
    if not isinstance(figure, mpl.figure.Figure):
        raise ValueError(
            f"{factory_name}() must return matplotlib.figure.Figure, "
            f"got {type(figure).__name__}"
        )
    return figure


def _write_report(report: AuditReport, output_format: str, output: Path | None) -> None:
    if output_format == "json":
        rendered = json.dumps(report.to_dict(), indent=2, sort_keys=True)
    else:
        rendered = report.render_text()

    if output is None:
        print(rendered)
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote audit report: {output}")


def _audit_command(args: argparse.Namespace) -> int:
    try:
        figure = _load_figure(args.script, args.factory)
        report = audit_figure_report(
            figure,
            profile=args.profile,
            strict_font=args.strict_font,
            strict_dimensions=args.strict_dimensions,
            require_ipcc_colormap=args.require_ipcc_colormap,
            dimension_tolerance_mm=args.dimension_tolerance_mm,
        )
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 2

    _write_report(report, args.format, args.output)
    return 0 if report.passed else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ar6plot",
        description="Evidence-backed AR6 scientific-figure utilities.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser(
        "audit",
        help="run machine-checkable AR6 fidelity checks on a Matplotlib figure factory",
    )
    audit.add_argument("script", type=Path, help="Python script containing a figure factory")
    audit.add_argument(
        "--factory",
        default="make_figure",
        help="zero-argument function returning matplotlib.figure.Figure (default: make_figure)",
    )
    audit.add_argument(
        "--profile",
        choices=("ar6-report", "wgi-guide-2022"),
        default="ar6-report",
    )
    audit.add_argument("--strict-font", action="store_true")
    audit.add_argument("--strict-dimensions", action="store_true")
    audit.add_argument("--require-ipcc-colormap", action="store_true")
    audit.add_argument("--dimension-tolerance-mm", type=float, default=0.5)
    audit.add_argument("--format", choices=("text", "json"), default="text")
    audit.add_argument("--output", type=Path)
    audit.set_defaults(func=_audit_command)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
