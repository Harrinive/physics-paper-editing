# Cursor runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md)
in Cursor. Cursor-specific commands belong here, not in the core workflow.

## Session and model profile

- Use `AskQuestion` once at top-level intake for `recommended`, `parent`, or
  `custom`; persist the response using the contract schema.
- Launch each `Task` with the role's resolved `model`. Use `model: inherit` for
  `parent`, unavailable tiers, and unselected custom roles.
- Record the requested tier separately from the model Cursor actually runs. If
  Cursor falls back or hides the final identifier, write `unknown`.

## Worker operations

| Contract capability | Cursor operation | Fallback |
|---|---|---|
| Read-only worker | `Task` with `readonly: true` | Explicit source-edit ban and one shard |
| Background worker | `Task` with `is_background: true` or equivalent | Foreground wave; say verification is blocking |
| Concurrency | Launch to Cursor's active subagent limit, then queue | Independent waves |
| Completion | Returned task/subagent status and shard | Harvest next parent turn |
| Interrupt | Interrupt the task when supported | Finish, then mark obsolete shard stale |
| Resume | Resume recorded task/subagent identifier | Rebuild from `agents.json` and relaunch |

Give every `Task` its snapshot identifier, assigned labels, result path, and
read-only boundary. Background output may aid diagnosis, but the shard is
authoritative.

## Optional hook

If installed, a Cursor hook may notify the parent that a shard is ready. It is
an optimization only: persisted shards and deterministic harvest must work with
no hook installed.
