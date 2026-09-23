# Cursor runtime adapter

Use this adapter only to implement [runtime-contract.md](runtime-contract.md) in
Cursor.

- Resolve capability tiers through the models available in the active Cursor
  runtime; the portable core contains no model slugs.
- Run `direct` work in the parent.
- In the first reply, announce and use any standing role-to-model policy. If none
  exists, obtain the user's choice required by
  [runtime-contract.md](runtime-contract.md) before substantive editing.
- Under `reviewed`, launch the whole-unit sentence and
  terminology-and-notation reviewers, then the triggered specialists and
  scientific reviewers. Do not launch one reviewer per sentence. Give every
  reviewer exact applicable canon paths.
- Use read-only/background task controls when available; otherwise give an
  explicit no-source-edit boundary and run foreground.
- Record hidden model resolution as `unknown`, not an inferred identifier.
- Respect user constraints on delegation and report `self_only` honestly.

Treat version-1 jobs as closed history and start a fresh version-2 job.
