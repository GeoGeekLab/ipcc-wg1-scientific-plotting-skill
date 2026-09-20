# Third-party materials and attribution

The MIT License in [LICENSE](LICENSE) applies to the original source code and
documentation authored for this repository, except where a file states
otherwise.

It does **not** relicense third-party material.

## IPCC and AR6 sources

This project references and, in reproducibility workflows, may fetch material
from IPCC AR6 Working Group I sources, including visual guidance, source data,
chapter repositories, published figures, and the official
`IPCC-WG1/colormaps` repository.

Those upstream materials remain subject to their own copyright, licensing,
attribution, and reuse terms. Users are responsible for checking the relevant
upstream source before redistributing third-party code, data, graphics, or
colour assets.

The project intentionally does not vendor the official WGI RGB tables. Strict
colormap workflows load an authorized local checkout through
`IPCC_WG1_COLORMAPS_DIR`.

## Reference reproductions

Files under `examples/ipcc_reference/outputs/` are regression artifacts
generated from pinned upstream source data. Their presence in this repository
does not grant additional rights over any underlying third-party data,
published figure content, or other upstream material.

See `references/SOURCES.md` and the reference-gallery manifest for provenance.

## Fonts

Arial is not distributed by this repository. Users who require strict
typographic fidelity must provide a legally installed copy in their own
environment.

## Project status

This is an independent project. It is not an official IPCC product and does
not imply IPCC endorsement.
