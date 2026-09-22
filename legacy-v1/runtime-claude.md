# Claude runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md)
in Claude Code or another Claude host with compatible subagents. Do not assume
every Claude surface supplies every operation.

## Session and model profile

- Ask once with the host's interactive question facility for `recommended`,
  `parent`, or `custom`; otherwise apply the no-interaction fallback.
- Use the host's subagent configuration or launch option to select a model per
  role when available. Inherit the parent only when the user selected `parent`
  or left a custom role unspecified. If the selected model is unavailable, ask
  for a revised choice before launch.
- Persist only an exposed model identifier. Record `unknown` for hidden model
  resolution while retaining the requested tier and source.

## Worker operations

| Contract capability | Claude operation | Fallback |
|---|---|---|
| Read-only worker | Subagent with read-only tools/permissions when configured | Result-only assignment and output audit |
| Background worker | Background subagent when supported | Foreground wave; say verification is blocking |
| Concurrency | Respect configured subagent limit and queue excess scopes | Sequential waves |
| Completion | Host subagent completion state, then read shard | Harvest next parent wake |
| Interrupt | Host stop/interrupt control | Finish, then mark obsolete shard stale |
| Resume | Retained subagent session when offered | Rebuild from `agents.json` and relaunch |

Claude Code installations may expose subagents through the `Task` tool and
custom agent files; other Claude hosts use different controls. In every case,
pass role, scope, snapshot, and result path; make source material read-only
where possible; and treat the shard rather than the chat transcript as
authoritative.
