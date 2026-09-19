"""Pinned upstream sources used by the reference reproductions."""

CH3_REPO = "IPCC-WG1/Chapter-3_Fig02b"
CH3_SHA = "ee22b6221c6535f81a33c1b033a4183621df0b23"

CH2_REPO = "IPCC-WG1/Chapter-2_Fig03"
CH2_SHA = "5078755d5bf97653ae498f204bc55aeaf13b1671"

CH6_REPO = "IPCC-WG1/Chapter-6_Fig18"
CH6_SHA = "09d9b43fe935fc81d828147f91b717396a84fca3"

CH10_REPO = "ipcc-wgi/ESMValTool-AR6-OriginalCode-FinalFigures"
CH10_SHA = "91845e70e46bb5581d5612ac34256b44106bfb3d"
CH10_BRANCH_CONTEXT = "ar6_chapter_10"


def raw_url(repo: str, sha: str, path: str) -> str:
    from urllib.parse import quote

    return f"https://raw.githubusercontent.com/{repo}/{sha}/{quote(path, safe='/')}"
