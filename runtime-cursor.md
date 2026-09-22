# Cursor runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md) in
Cursor.

- Resolve capability tiers through the models available in the active Cursor
  runtime; the portable core contains no model slugs.
- Run `direct` work in the parent.
- Obtain the user-confirmed model profile required by
  [runtime-contract.md](runtime-contract.md) before launching any subagent.
  Launch only the role required by adaptive routing.
- Use read-only/background task controls when available; otherwise give an
  explicit no-source-edit boundary and run foreground.
- Record hidden model resolution as `unknown`, not an inferred identifier.
- Respect user constraints on delegation and report `self_only` honestly.

Existing version-1 jobs use [legacy-v1/runtime-cursor.md](legacy-v1/runtime-cursor.md).
