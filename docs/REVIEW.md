# Review of the inherited plugin

The review covered the request authentication path, authorization before side
effects, dispatch/deduplication behavior, adapter lifecycle, token handling,
profile routing, mutation policy and packaging. It is a maintainer code review,
not an independent audit of every Hermes or Linear dependency.

## Changes made

- Require freshness of the signed body timestamp even when a caller supplies a
  fresh timestamp header. Missing, malformed and non-finite timestamps fail closed.
- Derive duplicate identity from signed fields rather than mutable delivery headers.
- Release a duplicate claim and return a retryable 503 after a failed handoff;
  do not report a failed handoff as successful or expose exception text in replies.
- Restrict binding to loopback and clean up the runner, client and credential lock
  when binding fails. Verify retry after failure.
- Scope the active tool adapter by Hermes profile, preventing tools from selecting
  another profile's connected credential.
- Reject non-boolean/unknown mutation policies. A string such as `"false"` is not
  permission to write. Explicit sender lists narrow broader gateway grants; a
  configured workspace rejects missing as well as mismatched workspace identity.
- Support Python 3.14, use the pinned Hermes 0.23.0 lock contract, and align native
  manifests, wheel discovery, source contents and MIT release metadata.

Existing protections retained: original-byte HMAC checks, a body size cap,
authorization before acknowledgement/auto-start/stop, self-update suppression,
fail-closed write tools, bounded message splitting, and protected OAuth storage.

## Installer scan findings

The initial inherited source was blocked by Hermes's community-plugin scanner.
Findings included a printed cloudflared example, package-install instructions,
CI dependency commands and a comment about credential locking. The tunnel command
was printed guidance, not executed by the receiver. Setup guidance now describes a
restricted HTTPS ingress. CI still installs declared dependencies to test them;
this is expected build behavior and must remain visible for review. Scanning must
not be disabled globally or made green by hiding executable behavior.

## Limits

The receiver has no independent durable inbox. Its in-memory duplicate cache and
Hermes's handoff/session persistence do not establish exactly-once execution across
crashes. The optional broad Linear toolset remains gated by explicit policies;
initial deployment leaves those writes off. Terminal and MCP tools have their own
Hermes policies. See SECURITY.md and the verification record.
