# Changelog

## 0.1.0 — 2026-11-06 (ParkesAI fork)

- Support Python 3.14 and qualify against the pinned Hermes 0.23.0 SDK.
- Update lock lifecycle tests for the current Hermes contract.
- Require a fresh numeric timestamp in the signed webhook body, regardless of
  unsigned headers, with regression coverage.


All notable changes to this project will be documented here.

## 0.4.2 — 2026-07-29

### Fixed

- Resolve a child `AgentSession.sourceCommentId` to its root comment before replying; Linear rejects child comments as `commentCreate.parentId` with `incorrect parent`.
- Mirror final Agent Session responses to the resolved source thread in adapter-controlled delivery instead of relying on the model to invoke a comment tool.

## 0.4.1 — 2026-07-29

### Fixed

- Preserve Linear's current `agentSession.sourceCommentId` webhook field so replies triggered from an existing issue-comment thread can be routed back to that original thread.
- Accept `agentActivity.sourceCommentId` as a compatible fallback for prompted activity payloads.

## 0.4.0 — 2026-07-29

### Added

- Standalone Hermes platform-plugin distribution for Linear Agent Sessions.
- Git-directory plugin manifest and pip entry point.
- 58 attributed `linear_agent_*` tools with fail-closed mutation policies.
- Linear client-credentials and authorization-code OAuth support.
- Signed webhook handling, replay protection, Agent Activities, plans, session links, clarification, stop signals, and standalone cron delivery.
- Plugin-owned, process-locked, atomic OAuth state storage with POSIX mode `0600`.
- Read-only migration fallback for earlier `providers.linear_agent` state in Hermes `auth.json`.
- Compatibility tests for current Hermes upstream and Python 3.11–3.13.
