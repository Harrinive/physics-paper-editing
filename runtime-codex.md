# Codex runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md)
in Codex. Codex-specific calls belong here, not in the core workflow.

## Session and model profile

- Use `request_user_input` once at top-level intake when available for
  `recommended`, `parent`, or `custom`. Otherwise use the no-interaction
  fallback in the contract.
- Use `spawn_agent` with a model and reasoning effort when the profile or host
  configuration supplies them. Omit overrides for inheritance.
- Record a resolved model only when Codex reports it. A requested tier or
  assumed default is not a resolved identifier.

## Worker operations

| Contract capability | Codex operation | Fallback |
|---|---|---|
| Read-only worker | Result-only assignment; inherited sandbox permissions | Audit that only the shard was written |
| Background worker | `spawn_agent`, then continue the parent workflow | Bounded foreground wave |
| Concurrency | Respect configured agent limit; launch later scopes in waves | One worker at a time |
| Completion | `wait_agent` or completion notification, then read shard | Harvest next parent wake |
| Interrupt | `interrupt_agent` | Finish, then mark obsolete shard stale |
| Follow-up / resume | `followup_task` or `send_message` to a live agent | Rebuild from `workers.json` and relaunch |

Each spawned agent receives role, scope, snapshot identifier, result path, and
a no-source-edit instruction. `agents.json` is authoritative when agent IDs
or live-thread state are unavailable after a resume.
