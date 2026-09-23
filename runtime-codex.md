# Codex runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md) in
Codex.

- Resolve `strong`, `economy`, and `capable` from the models actually available
  in the current Codex surface; keep identifiers out of the core files.
- Use the parent directly for `direct` work.
- In the first reply, announce and use any standing role-to-model policy. If none
  exists, obtain the user's choice required by
  [runtime-contract.md](runtime-contract.md) before substantive editing.
- Under `reviewed`, launch the whole-unit sentence and
  terminology-and-notation reviewers, then the triggered specialists and
  scientific reviewers. Do not spawn one reviewer per sentence.
- Pass source, candidate, context, physics spine, object ledger, dependency and
  snapshot identifiers when applicable, exact applicable canon paths, and a
  no-source-edit instruction.
- Respect an explicit user request not to use subagents; record `self_only`.
- Use background execution only when available and useful. Otherwise run a
  bounded foreground review without claiming concurrency.
- Persist returned model identifiers only when Codex exposes them.

Treat version-1 jobs as closed history and start a fresh version-2 job.
