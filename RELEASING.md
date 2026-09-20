# Releasing ar6-sciplot

The PyPI distribution is **`ar6-sciplot`**. The Python import package remains
**`ipcc_sciplot`**.

Versions are derived from Git tags with `setuptools-scm`; do not edit a version
string manually.

## One-time PyPI setup

Use PyPI **Trusted Publishing** rather than a long-lived API token.

For the first release, create a pending GitHub Actions publisher on PyPI with:

| Field | Value |
| --- | --- |
| PyPI project name | `ar6-sciplot` |
| GitHub owner | `GeoGeekLab` |
| Repository | `ipcc-wg1-scientific-plotting-skill` |
| Workflow filename | `publish-pypi.yml` |
| Environment | leave blank |

The workflow is stored at:

`.github/workflows/publish-pypi.yml`

A pending publisher does not reserve the project name. Configure it immediately
before the first release and publish without unnecessary delay.

## Release procedure

1. Merge only after CI and the reference-reproduction workflow are green.
2. Choose the next semantic version.
3. Create and publish a GitHub Release from `main` with the matching tag,
   for example `v2.2.0`.
4. The `Publish to PyPI` workflow builds wheel + sdist from that release tag.
5. The publish job requests a short-lived OIDC credential from PyPI and uploads
   the distributions. No PyPI API token is stored in GitHub.
6. Verify the published package in a clean environment:

   ```bash
   python -m venv /tmp/ar6-sciplot-verify
   source /tmp/ar6-sciplot-verify/bin/activate
   python -m pip install ar6-sciplot
   python -c "import ipcc_sciplot; print(ipcc_sciplot.__version__)"
   ```

The printed version must match the release tag without the leading `v`.

## Release safety

- Do not add `workflow_dispatch` to the publishing workflow merely for
  convenience; publishing should stay bound to a reviewed GitHub Release.
- Keep `fetch-depth: 0` in build/release checkouts so `setuptools-scm` can
  resolve the tag correctly.
- Do not publish from a pull-request workflow.
- Review changes to `.github/workflows/publish-pypi.yml` with the same care as
  package credentials.
- If a protected GitHub `pypi` environment is added later, configure the same
  environment name in the PyPI Trusted Publisher settings.
