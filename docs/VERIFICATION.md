# Verification and compatibility

## Qualification target

Hermes Agent 0.23.0 at commit
`2bd378ed1b8d6bf2192cb26e0a55ff3091e6bd19`, Python 3.14.

Qualification completed on 2026-11-06:

- 217 tests passed against the pinned real SDK on the server and in CI. CI also
  passed lint, formatting, wheel entry-point discovery, build and distribution
  metadata/content checks. Native plugin doctor passed without warnings.
- Native installation completed through Hermes's normal plugin-manager path
  without a scanner override. Dependencies and the installation commit were pinned.
- A provider-originated delegation reached the running gateway and produced a
  completed response visible in Linear. The corresponding Hermes transcript
  contained one user message, one assistant response and zero tool calls.
- A real comment mention through Linear's mention picker produced a separate
  completed response. A subsequent prompt recalled that prior response in the same
  conversation. The transcript contained two user messages, two assistant responses
  and zero tool calls.
- The receiver rejected an unsigned public POST with 401. Public health returned
  404; receiver sockets were bound to loopback. Existing private services and the
  separate Sentry receiver remained available after gateway restart.
- Source and distributions were scanned/reviewed for secrets and private deployment
  identifiers. Scanner findings in synthetic credential fixtures were reviewed
  explicitly; live configuration remains outside the repository.

Live qualification found and corrected an inherited payload mismatch: current
Linear Agent Session events identify the initial human via `agentSession.creator`
/ `creatorId`, and follow-up humans via `agentActivity.user` / `userId`. Regression
coverage verifies that a follow-up cannot inherit its session creator's authority.

Stop behavior is covered by the automated suite, but was not exercised as a live
provider stop signal in this qualification. No production issue was modified by the
agent. These checks are not a load test, independent audit, or proof of exactly-once
execution across crashes. Duplicate caching remains bounded and in memory.

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
