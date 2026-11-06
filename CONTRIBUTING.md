# Contributing

This project is derived from infinityrobot/hermes-linear-agent under MIT. Preserve
original attribution. Use public-safe synthetic data in fixtures and documentation.
Do not add deployment addresses, personal credentials, real project identifiers or
private issue payloads. Keep credentials profile-scoped and use the public Hermes
plugin API. Read AGENTS.md before changing code.

## Set up and test

The qualified Hermes SDK lock targets Python 3.14. Install uv and use that Python
version for the integration suite:

```sh
uv sync --locked --extra dev
uv run ruff check hermes_linear tests scripts __init__.py
uv run ruff format --check hermes_linear tests scripts __init__.py
git clone --filter=blob:none https://github.com/NousResearch/hermes-agent.git .hermes-sdk
git -C .hermes-sdk checkout 2bd378ed1b8d6bf2192cb26e0a55ff3091e6bd19
PYTHONPATH="$PWD/.hermes-sdk" HERMES_HOME="$PWD/.hermes-test-home" \
  uv run --project .hermes-sdk --with '.[dev]' pytest
uv build
uv run python scripts/check_distribution.py
```

Tests use generated/synthetic credentials, fake Linear clients and loopback servers.
They do not need a real Linear account, model key or public endpoint. CI runs against
the pinned real Hermes SDK and verifies pip entry-point discovery. Native discovery
must also pass `hermes plugins doctor . --ci` on a matching Hermes installation.

After changing tool schemas, run `uv run python scripts/update_manifest.py`. The
manifest's tool declarations are generated from explicit schema definitions; a
contract test verifies they agree with runtime registration. Commit both the inputs
and regenerated manifest. Do not edit generated distributions or lockfiles by hand.

## Release

Run the checks above on a clean immutable commit. Verify native installation and a
controlled provider-originated delegation and mention through the actual gateway.
Inspect the response in Linear. Record exactly which checks passed in
`docs/VERIFICATION.md`; distinguish HTTP acknowledgement from a completed analysis.
Scan source, history and both distributions for secrets/deployment identifiers.
Publish the wheel, source archive and generated SHA-256 checksums on the GitHub
release after CI passes. This project is not published to PyPI.
