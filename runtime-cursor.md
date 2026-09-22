# Cursor runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md) in
Cursor.

- Resolve capability tiers through the models available in the active Cursor
  runtime; the portable core contains no model slugs.
- Run `direct` work in the parent.
- In the first reply of a new top-level editing conversation, obtain the
  user-confirmed model choice required by
  [runtime-contract.md](runtime-contract.md), before routing or substantive
  editing. Ask even if the eventual path may be `direct`. Launch only the role
  required by adaptive routing.
- Use read-only/background task controls when available; otherwise give an
  explicit no-source-edit boundary and run foreground.
- Record hidden model resolution as `unknown`, not an inferred identifier.
- Respect user constraints on delegation and report `self_only` honestly.

Treat version-1 jobs as closed history and start a fresh version-2 job.
