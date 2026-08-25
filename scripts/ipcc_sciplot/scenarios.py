from __future__ import annotations

from collections.abc import Iterable, Sequence


_CANONICAL_SSP_ORDER = (
    "SSP1-1.9",
    "SSP1-2.6",
    "SSP2-4.5",
    "SSP3-7.0",
    "SSP5-8.5",
)

_ALIASES = {
    "ssp119": "SSP1-1.9",
    "ssp126": "SSP1-2.6",
    "ssp245": "SSP2-4.5",
    "ssp370": "SSP3-7.0",
    "ssp585": "SSP5-8.5",
    "historical": "historical",
}


def canonical_scenario_label(label: str) -> str:
    """Normalize common CMIP6 scenario aliases to assessment-facing labels.

    Unknown labels are returned unchanged so idealized experiments and project-
    specific scenarios are not silently reclassified.
    """

    text = str(label).strip()
    return _ALIASES.get(text.lower(), text)


def canonical_scenario_order(labels: Iterable[str]) -> list[str]:
    """Return stable low-to-high forcing order for known SSPs.

    `historical` is placed first; unknown labels retain their first-seen order after
    the known SSPs rather than being assigned a scientific ordering that is not known.
    """

    normalized = [canonical_scenario_label(x) for x in labels]
    unique = list(dict.fromkeys(normalized))
    result: list[str] = []

    if "historical" in unique:
        result.append("historical")
    for scenario in _CANONICAL_SSP_ORDER:
        if scenario in unique:
            result.append(scenario)
    result.extend(x for x in unique if x not in result)
    return result


def validate_scenario_order(labels: Sequence[str]) -> None:
    """Raise when known scenarios are ordered inconsistently with canonical forcing order."""

    normalized = [canonical_scenario_label(x) for x in labels]
    expected = canonical_scenario_order(normalized)
    if list(normalized) != expected:
        raise ValueError(f"scenario order {normalized!r} is inconsistent; expected {expected!r}")


def known_ssp_labels() -> tuple[str, ...]:
    return _CANONICAL_SSP_ORDER
