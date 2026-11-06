# Security policy

Report vulnerabilities through this repository's **Report a vulnerability** flow.
Do not put live tokens, signing secrets, private issue content or host configuration
in public issues. Security fixes target the latest published release.

## Trust boundaries

This is in-process Hermes code, not a sandbox. Review and pin the immutable
installation commit. The HTTP receiver binds only to loopback; publish only its
Linear webhook path through an HTTPS ingress. Keep health, dashboard and other
listeners private. Apply request-size and rate limits at ingress.

The receiver verifies signatures before parsing or acting, requires a fresh numeric
`webhookTimestamp` inside the signed body, and derives duplicate identity from
signed fields rather than caller delivery headers. Configured workspace and team
restrictions apply before side effects. An explicit local sender allowlist narrows
broader gateway grants. Missing authorization fails closed.

A handoff exception returns 503 and removes the duplicate claim for retry. Duplicate
caching is bounded and in memory; it resets when the process restarts. The receiver
is not an independent durable queue or an exactly-once execution guarantee. A crash
at the handoff boundary can lose or repeat work. Hermes owns execution/persistence
after handoff. Keep delegated operations safe to retry and use review gates for
irreversible actions. HTTP 200 does not prove a completed agent turn.

## Credentials and permissions

Use a workspace-private Linear application with an app actor. Store client and
webhook secrets in the protected profile environment, never Git, public examples,
command arguments, logs or exported configuration. With client credentials, access
tokens can remain in memory (`LINEAR_AGENT_PERSIST_TOKENS=false`). If persistence is
explicitly enabled, plugin-owned state is protected and atomically written. Rotate
through Linear and update the matching profile credentials together.

Client-credential tokens initially access public teams. Restrict the installed app's
team access in Linear before operating it. Also configure the receiver's workspace,
team and sender allowlists. Agent Activities are necessary protocol messages; the
additional Linear write tools are separately gated by explicit boolean policy
values and default to denied. Host, terminal and MCP permissions remain Hermes's
responsibility. Untrusted issue text is not authorization to reveal credentials or
perform unrelated actions.

Review logging, Hermes session storage and model-provider retention for your own
data requirements. No private deployment configuration belongs in this repository.
The initial qualification targets Hermes 0.23.0 / Python 3.14; see the verification
record for completed checks and limitations.
