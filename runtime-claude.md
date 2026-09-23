# Claude runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md) in
Claude Code or a compatible host.

- Resolve capability tiers from the host's configured models; keep concrete
  identifiers out of the portable core.
- Do not delegate `direct` work.
- In the first reply, announce and use any standing role-to-model policy. If none
  exists, obtain the user's choice required by
  [runtime-contract.md](runtime-contract.md) before substantive editing.
- Under `reviewed`, launch the whole-unit sentence and
  terminology-and-notation reviewers, then the triggered specialists and
  scientific reviewers. Do not launch one reviewer per sentence. Give every
  reviewer exact applicable canon paths.
- Use read-only and background controls when the host exposes them; otherwise
  state and audit the no-source-edit boundary.
- Record unavailable or hidden model identity as `unknown`.
- When delegation is unavailable or prohibited, inherit in the parent and mark
  verification as `self_only`.

Treat version-1 jobs as closed history and start a fresh version-2 job.
