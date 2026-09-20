# Optional version-2 job state

Ordinary synchronous edits do not create job state. Use this file only when a
file edit is asynchronous, concurrent, resumable, or likely to outlive the
current context.

## Required state

Store the version-2 routing block from [runtime-contract.md](runtime-contract.md),
the source-file span, current snapshot identifier, physics spine, object ledger,
review status, quality axes, and next action.

Use construction sentinels only when concurrent editing makes a stable span
necessary:

```tex
% PPE2-BEGIN id=<job_id> snapshot=<sha256> status=<editing|reviewing|needs_user>
... editable interior ...
% PPE2-END id=<job_id>
```

Do not mark quoted text returned only in chat. Do not create one state directory
per sentence.

## Wake and stale review

On resume, compare the live span with the review snapshot. Preserve obsolete
reviews as stale, apply no finding blindly, and recheck only axes affected by
the changed text. Never convert a version-1 job in place; use the legacy state
contract for jobs without `harness_version: 2`.

## Completion

Remove sentinels when `completion: ready` and no reviewer is running. Leave the
draft intact and ask one focused question when `completion: needs_user`.
