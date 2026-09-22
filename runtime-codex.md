# Codex runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md) in
Codex.

- Resolve `strong`, `economy`, and `capable` from the models actually available
  in the current Codex surface; keep identifiers out of the core files.
- Use the parent directly for `direct` work.
- In the first reply of a new top-level editing conversation, obtain the
  user-confirmed model choice required by
  [runtime-contract.md](runtime-contract.md), before routing or substantive
  editing. Ask even if the eventual path may be `direct`. Delegate only the
  roles required by the routing matrix; do not spawn sentence workers.
- Pass source, draft, context, physics spine, object ledger, snapshot identifier
  when applicable, and a no-source-edit instruction.
- Respect an explicit user request not to use subagents; record `self_only`.
- Use background execution only when available and useful. Otherwise run a
  bounded foreground review without claiming concurrency.
- Persist returned model identifiers only when Codex exposes them.

Treat version-1 jobs as closed history and start a fresh version-2 job.
