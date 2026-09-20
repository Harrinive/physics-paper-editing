# Runtime contract

Read this file only when version-2 work needs model selection, delegation,
persistence, or a runtime fallback. The portable core specifies capability
requirements; adapters resolve concrete host operations and model identifiers.

## Session profile

```yaml
harness_version: 2
edit_intent: copyedit | substantive
model_tier: strong | economy | unknown
tier_source: adapter | user | inherited | fallback
scientific_risk: low | medium | high
execution_path: direct | guided | independent | legacy_full
verification_independence: independent | self_only | unavailable
roles:
  editor: {requested_tier: strong | economy | inherit, resolved_model: unknown}
  holistic_reviewer: {requested_tier: capable | inherit, resolved_model: unknown}
  math_reviewer: {requested_tier: capable | inherit, resolved_model: unknown}
  local_polisher: {requested_tier: economy | inherit, resolved_model: unknown}
  adjudicator: {requested_tier: capable | inherit, resolved_model: unknown}
```

Record a resolved model only when the host reports it. The core skill contains
no vendor model names. Unknown editor capability routes as economy.

Do not ask the user to choose a profile when the runtime already supplies a
known capability tier and no preference is material. State the selected path
only when it changes cost, verification independence, or expected latency.

## Worker rules

- `direct` launches no workers.
- `guided` launches at most one holistic reviewer and one conditionally
  triggered math reviewer.
- `independent` launches the same reviewers independently; an adjudicator is
  conditional on an actual scientific conflict.
- A local polisher receives only a diagnosed span and decided repair.
- No version-2 role is assigned one worker per sentence.
- If delegation is unavailable or forbidden, run the checks in the strongest
  available parent and record `verification_independence: self_only` or
  `unavailable`.

## Persistence

Do not create state for ordinary synchronous short edits. For resumable,
asynchronous, concurrent, or file-based work, persist:

```text
.physics-edit/<scope>/<job_id>/
├── session.md
├── snapshot.tex
├── object-ledger.md
├── reviews/
└── result.yaml
```

Each review records the snapshot identifier, role, scope, model metadata when
known, and axis results from [quality-contract.md](quality-contract.md). Reject
review output from an obsolete snapshot. Separate review files avoid concurrent
writes to one log.

## Capability fallbacks

| Missing capability | Behavior |
|---|---|
| Model-tier resolution | Use `unknown` → economy routing |
| Per-role model selection | Inherit; record the limitation |
| Delegation | Parent performs the checks; mark `self_only` |
| Background work | Run reviewers in foreground; do not claim concurrency |
| Interruption | Let obsolete review finish, preserve it as stale, and recheck changed content |
| Resume handle | Resume from persisted snapshot and review files |

Content quality and verification independence are separate. A fallback changes
the latter; it does not fabricate a content `PASS` or `FIX`.

## Version compatibility

Any live job without `harness_version: 2` resumes under
[legacy-v1/LEGACY.md](legacy-v1/LEGACY.md). Do not translate its state or mix v2
roles and quality axes into an active v1 round.
