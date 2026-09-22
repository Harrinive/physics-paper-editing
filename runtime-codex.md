# Codex runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md) in
Codex.

- Resolve `strong`, `economy`, and `capable` from the models actually available
  in the current Codex surface; keep identifiers out of the core files.
- Use the parent directly for `direct` work.
- For `guided` or `independent` work, obtain the user-confirmed model profile
  required by [runtime-contract.md](runtime-contract.md) before spawning. Delegate
  only the roles required by the routing matrix; do not spawn sentence workers.
- Pass source, draft, context, physics spine, object ledger, snapshot identifier
  when applicable, and a no-source-edit instruction.
- Respect an explicit user request not to use subagents; record `self_only`.
- Use background execution only when available and useful. Otherwise run a
  bounded foreground review without claiming concurrency.
- Persist returned model identifiers only when Codex exposes them.

Existing version-1 jobs use [legacy-v1/runtime-codex.md](legacy-v1/runtime-codex.md).
