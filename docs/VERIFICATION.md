# Verification and compatibility

## Qualification target

Hermes Agent 0.23.0 at commit
`2bd378ed1b8d6bf2192cb26e0a55ff3091e6bd19`, Python 3.14.

The initial release is under qualification. Unit tests and plugin discovery alone
do not prove a connected Linear app or a completed agent response. Live results
will be recorded here without hostnames, credentials or workspace/issue identities.

## Repeatable release checks

1. Run locked dependency setup, lint, formatting, all tests and distribution checks.
2. Verify native discovery with `hermes plugins doctor . --ci` and installed wheel
   entry-point discovery through the actual Hermes plugin manager.
3. Install a reviewed immutable commit through Hermes's plugin manager. Configure
   a protected app identity, signed webhook receiver and explicit sender/team scope.
4. Verify unsigned, tampered, stale, malformed and oversized requests cannot dispatch.
   Replay a signed body with changed delivery headers and verify one activation.
5. Verify dispatch failure remains retryable and bind failure releases resources.
6. Delegate a controlled issue through Linear and verify a Hermes session plus a
   visible response. Test a comment mention, a follow-up and a stop signal separately.
7. Confirm the dashboard, health endpoint and unrelated listeners remain private.
8. Scan source, history and distributions; publish an immutable release only after
   CI passes. Attach artifacts/checksums and state remaining coverage limitations.

## Benchmarks and provenance

- [Hermes Sentry](https://github.com/ParkesAI/hermes-sentry): package-manager
  installation, loopback ingress, explicit trust boundaries, real-SDK tests,
  release artifacts and evidence distinguishing admission from completed analysis.
- [Official Hermes plugins](https://github.com/NousResearch/hermes-official-plugins):
  native manifests and plugin API contracts.
- [Original Linear Agent plugin](https://github.com/infinityrobot/hermes-linear-agent):
  Agent Sessions, activity replies and fail-closed write tools. Original MIT
  attribution is preserved in this derivative.

These comparisons are implementation/packaging references, not security endorsements.
