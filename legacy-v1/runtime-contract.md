# Runtime contract

This is the portable execution contract for the editing harness. It defines
*what* the parent agent must arrange; a host adapter defines concrete commands.
Keep checker prompts in their existing verifier documents.

## Load order

1. Read this contract for every top-level session.
2. Select the adapter for the active host from the runtime reference files.
3. Use the adapter only for host operations. Canon, scope, severity, snapshot,
   and merge rules remain in the editing documents.

## Session profile

At top-level intake, collect one choice and persist it. Do not ask again for
chunks, rounds, or resumes unless the user asks to change it.

| Choice | Meaning |
|---|---|
| `recommended` | `sentence: fast`; `deep: capable`; `synth: capable` |
| `parent` | Every role inherits the parent model and reasoning level |
| `custom` | The user supplies a role-to-model mapping; unspecified roles inherit |

`fast` and `capable` are requirements, not vendor names. Resolve them through
the active adapter. If no suitable model is known, inherit and record the
fallback rather than inventing an identifier.

Persist this shape in `session.md` or its machine-readable companion:

```yaml
runtime: host identifier
model_profile:
  profile_choice: recommended | parent | custom
  profile_source: accepted_default | custom | inherit | fallback
  user_confirmed: true | false
  roles:
    sentence: {requested_tier: fast, resolved_model: unknown, reasoning: unknown, resolution_source: accepted_default}
    deep: {requested_tier: capable, resolved_model: unknown, reasoning: unknown, resolution_source: accepted_default}
    synth: {requested_tier: capable, resolved_model: unknown, reasoning: unknown, resolution_source: accepted_default}
```

Valid `profile_source` and `resolution_source` values are `accepted_default`,
`custom`, `inherit`, and `fallback`. Set `user_confirmed: true` only after the user accepts or supplies
a profile; showing a default is not confirmation.

## Worker lifecycle

Give every worker a frozen snapshot identifier, scope, role, result location,
and a read-only instruction. The parent must:

1. write the draft and snapshot before launch;
2. schedule independent workers up to the runtime concurrency limit, then use
   waves;
3. let the user continue while checks run when asynchronous execution exists;
4. harvest completed results before one synthesizer decides round status;
5. preserve completed artifacts when stopping work; and
6. reject a result whose `snapshot_id` differs from the current snapshot.

Use enforced read-only execution when the host supports it. Otherwise state the
restriction in the assignment and verify that the worker wrote only its result.

## Results and deterministic harvest

Workers never append concurrently to one shared log. Allocate one append-only
shard per worker, immutable after its terminal record:

```text
.physics-edit/<scope>/<job_id>/findings/<worker_id>.jsonl
```

Each line in a shard repeats its worker envelope and has `event: finding` or
`event: completion`. The terminal completion record has this shape:

```json
{
  "schema_version": 1,
  "worker_id": "sentence-s3",
  "role": "sentence",
  "scope": ["s3"],
  "snapshot_id": "sha256:...",
  "runtime": "other",
  "agent_id": "unknown",
  "model": {"requested_tier": "fast", "resolved_model": "unknown", "reasoning": "unknown", "resolution_source": "fallback"},
  "status": "complete",
  "event": "completion",
  "findings": []
}
```

The parent maintains `agents.json` with the same identity and model fields,
plus `result_path`, `started_at`, `completed_at`, and lifecycle `status`:
`queued`, `running`, `complete`, `interrupted`, `failed`, or `stale`.

Harvest in lexical `worker_id` order. Validate schema and snapshot first; mark
invalid, missing, failed, or mismatched shards in `agents.json`, and pass only
valid findings to the synthesizer. A resume reuses valid completed shards, then
relaunches only missing, interrupted, failed, or stale scopes.

## Capability fallbacks

| Capability absent | Required behavior |
|---|---|
| Interactive choice | Do not launch workers; perform self-only checks and report that the model choice remains pending |
| Per-worker model selection | Ask the user to approve parent inheritance or use self-only review; do not silently replace the chosen model |
| Enforced read-only mode | Use a read-only assignment and verify result-only writes |
| Background work | Run foreground waves; do not claim concurrent user editing |
| Completion event | Poll or harvest at the next parent wake |
| Interruption | Allow completion, then label an obsolete shard `stale` |
| Resume handle | Resume from shards and manifest; relaunch unfinished work |

Do not turn a fallback into a prose-verification rule. The invariant is frozen
artifact coverage, not a particular host mechanism.
