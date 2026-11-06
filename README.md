# Hermes Linear

An MIT-licensed Hermes Agent platform plugin for **Linear delegation, mentions and
Agent Sessions**. People keep issue ownership while Hermes acts as the delegate.
Replies, follow-ups, clarification requests and stop signals use Linear's native
Agent Session protocol.

Maintained by ParkesAI, derived from
[infinityrobot/hermes-linear-agent](https://github.com/infinityrobot/hermes-linear-agent).
Original MIT attribution is preserved. See [verification](docs/VERIFICATION.md)
for the reviewed boundary and the compatibility evidence.

## Install

```sh
hermes plugins install ParkesAI/hermes-linear --no-enable
```

Use `--ref` with a reviewed full commit SHA for an immutable installation. The
plugin ID and Python distribution are `hermes-linear`; the module is
`hermes_linear`. The gateway key and existing tool names remain `linear_agent`
and `linear_agent_*` for compatibility. Use one ingress profile per installation
with the qualified Hermes version. Never install independently named copies
of the same package across profiles.

The repository builds a wheel and source distribution but is **not published to
PyPI**. Do not assume a similarly named PyPI package is this project.

## Connect Linear

1. Create a workspace-private OAuth application in Linear. Enable client
   credentials and **Agent session events**; permission-change events are useful
   for diagnosing revoked access. Ordinary Issue/Comment event subscriptions
   are not required for delegation or mentions.
2. Set the app's webhook URL to your public HTTPS endpoint ending in `/linear`.
   Keep its Client Secret and Webhook Signing Secret private.
3. Put the following environment variables in the active Hermes profile's
   protected `.env` file, through Hermes's configuration tools:

   ```dotenv
   LINEAR_AGENT_CLIENT_ID=<OAuth client ID>
   LINEAR_AGENT_CLIENT_SECRET=<OAuth client secret>
   LINEAR_AGENT_WEBHOOK_SECRET=<Webhook signing secret>
   LINEAR_AGENT_OAUTH_SCOPES=read,write,app:assignable,app:mentionable
   LINEAR_AGENT_ALLOWED_USERS=<explicit allowed Linear user IDs>
   LINEAR_AGENT_PERSIST_TOKENS=false
   ```

   Client credentials initially grant access to public teams. In Linear's
   installed-app settings, restrict team access before operating the agent.
   The plugin mints short-lived app tokens and obtains a new one on expiry/401;
   no personal API token is required.
4. Merge this into the private profile configuration, preserving other platforms:

   ```yaml
   linear_agent:
     enabled: true
     webhook_host: 127.0.0.1
     webhook_port: 8651
     webhook_path: /linear
     workspace_id: "<workspace ID>"
     allowed_teams: ["<allowed team ID>"]
     allowed_users: ["<allowed user ID>"]
     allow_all_users: false
     auto_start_on_delegation: false
     auto_self_delegate: false
     dispatch_issue_updates: false
     mutation_policy: {}
   ```

   With this configuration, normal agent replies use Agent Activities. The
   additional Linear write tools remain disabled. Terminal/MCP permissions are
   governed separately by Hermes; configure them for the work you intend to delegate.
5. Enable the plugin, restart the gateway through its existing supervisor, and
   check the loopback receiver:

   ```sh
   hermes plugins enable hermes-linear
   hermes gateway restart
   curl --fail http://127.0.0.1:8651/health
   ```

6. Publish only `/linear` through your HTTPS ingress. Preserve the body and Linear
   signature headers. For a path-stripping proxy, forward `/linear` to
   `http://127.0.0.1:8651/linear`. Keep the health endpoint, dashboard and other
   listeners private. An unsigned public POST must return 401.
7. Delegate a controlled test issue or mention the app through Linear's mention
   picker. Verify an actual Hermes session and a visible response in Linear.
   HTTP 200 means the delivery was handed off, not that analysis is complete.

## Safety and delivery

The receiver binds only to loopback. It verifies the signature over the original
bytes, requires a fresh timestamp inside the signed body, and checks the configured
workspace, team and sender before side effects. Duplicate identity comes from
signed body fields, not mutable caller headers. A handoff exception returns 503
and releases the duplicate claim so Linear can retry. Responses contain no internal
exception text.

Duplicate caching is bounded and in memory. It is not an independent durable
queue or an exactly-once guarantee across process crashes. Hermes owns session
execution and persistence after handoff. Do not delegate irreversible operations
without an appropriate review policy. See [security](SECURITY.md).

## Update and remove

Review the new immutable commit before updating through Hermes's plugin manager.
Disable the app's webhook delivery before removal, drain active sessions, remove
its ingress rule, then disable/remove the plugin and restart the gateway.
Revoke the app in Linear when retiring it; plugin removal does not revoke tokens
or delete Hermes session history. Keep secrets out of configuration exports and Git.

## Development

See [contributing](CONTRIBUTING.md) for the pinned real Hermes SDK setup and tests.
The [configuration reference](docs/REFERENCE.md) covers optional features and the
existing Linear toolset. Every write policy is off by default. See also
[changelog](CHANGELOG.md) and [verification](docs/VERIFICATION.md).
