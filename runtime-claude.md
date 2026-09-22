# Claude runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md) in
Claude Code or a compatible host.

- Resolve capability tiers from the host's configured models; keep concrete
  identifiers out of the portable core.
- Do not delegate `direct` work.
- In the first reply of a new top-level editing conversation, obtain the
  user-confirmed model choice required by
  [runtime-contract.md](runtime-contract.md), before routing or substantive
  editing. Ask even if the eventual path may be `direct`. Launch only the
  required roles.
- Use read-only and background controls when the host exposes them; otherwise
  state and audit the no-source-edit boundary.
- Record unavailable or hidden model identity as `unknown`.
- When delegation is unavailable or prohibited, inherit in the parent and mark
  verification as `self_only`.

Treat version-1 jobs as closed history and start a fresh version-2 job.
