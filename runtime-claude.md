# Claude runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md) in
Claude Code or a compatible host.

- Resolve capability tiers from the host's configured models; keep concrete
  identifiers out of the portable core.
- Do not delegate `direct` work.
- For other paths, launch only the required holistic, math, local-polisher, or
  conditional adjudicator roles.
- Use read-only and background controls when the host exposes them; otherwise
  state and audit the no-source-edit boundary.
- Record unavailable or hidden model identity as `unknown`.
- When delegation is unavailable or prohibited, inherit in the parent and mark
  verification as `self_only`.

Existing version-1 jobs use [legacy-v1/runtime-claude.md](legacy-v1/runtime-claude.md).
