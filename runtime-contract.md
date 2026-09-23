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
language_coverage: selective | exhaustive
execution_path: direct | reviewed
review_profile: standard | high_risk
formal_review_scope: none | changed | dependency_closure | all_in_scope
verification_independence: independent | self_only | unavailable
role_model_policy:
  choice: standing | recommended | parent | custom | pending
  active: true | false
  source: user | inherited_section | standing_instruction | pending
roles:
  editor: {requested_tier: strong | economy | inherit, resolved_model: unknown}
  sentence_reviewer: {requested_tier: economy | inherit, resolved_model: unknown}
  terminology_reviewer: {requested_tier: economy | inherit, resolved_model: unknown}
  principle_specialist: {requested_tier: economy | capable | inherit, resolved_model: unknown}
  holistic_reviewer: {requested_tier: capable | inherit, resolved_model: unknown}
  formal_reviewer: {requested_tier: capable | inherit, resolved_model: unknown}
  local_polisher: {requested_tier: economy | inherit, resolved_model: unknown}
  adjudicator: {requested_tier: capable | inherit, resolved_model: unknown}
```

Record a resolved model only when the host reports it. The core skill contains
no vendor model names. Unknown editor capability routes as economy.

A known capability tier selects the editing path; it does not silently choose
the standing role-to-model policy. At the start of every new top-level editing
conversation:

1. Look for a standing project or conversation instruction that supplies the
   role-to-model mapping.
2. If one exists, state the mapping briefly in the first reply, set
   `choice: standing`, `active: true`, and continue without requesting
   confirmation.
3. If none exists, ask which models to use if reviewers are needed: accept the
   recommended mapping, inherit the parent, or accept a custom mapping. Wait
   for the answer before substantive editing.

Reuse the active mapping throughout the conversation unless the user changes
it. A section chunk inherits the active section mapping and does not ask again.
On resume in a new conversation, re-read current standing instructions:
announce and use them if present; otherwise ask again. A stale saved profile
cannot override a current standing instruction. If the host cannot honor a
selected model or reasoning effort, stop before launching that reviewer,
explain the limitation, and ask for a replacement. Never substitute silently.

## Runtime adapter selection

Read exactly one adapter before resolving capabilities or launching reviewers:

| Host | Adapter |
|---|---|
| Codex | [runtime-codex.md](runtime-codex.md) |
| Cursor | [runtime-cursor.md](runtime-cursor.md) |
| Claude Code or compatible host | [runtime-claude.md](runtime-claude.md) |

For another host, apply this portable contract directly and record unavailable
capabilities as unknown.

## Editor and reviewer rules

- `direct` launches no reviewers.
- `reviewed` always launches one sentence reviewer and one terminology-and-
  notation reviewer for the whole edited unit.
- A sentence-principle hit launches one whole-unit specialist for that
  principle or tightly coupled group; never one reviewer per sentence.
- `reviewed` also launches one holistic reviewer and, when
  `formal_review_scope` is not `none`, one formal reviewer with the scope
  selected in [adaptive-routing.md](adaptive-routing.md).
- A high-risk profile keeps the holistic and formal reviews blind to the
  editor's conclusions and to one another. An adjudicator is conditional on an
  actual scientific conflict.
- A local polisher receives only a diagnosed span and decided repair.
- No version-2 role is assigned one reviewer per sentence.
- If delegation is unavailable or forbidden, run the checks in the strongest
  available parent and record `verification_independence: self_only` or
  `unavailable`.

## Persistence

Do not create state for ordinary synchronous short edits, regardless of path.
For resumable, asynchronous, concurrent, file-based, or exhaustive work,
persist:

```text
.physics-edit/<scope>/<job_id>/
├── session.md
├── source-original.txt
├── candidate-snapshot.txt
├── object-ledger.md
├── reviews/
└── result.yaml
```

Each review records the round/job identifier, candidate snapshot identifier,
role, review scope, formal-review scope when applicable, requested and resolved
model, reasoning effort when known, verification independence, applicable canon
paths and revision, context revision and applicable object-ledger revision, and
axis results from
[quality-contract.md](quality-contract.md). Persist the checked sentence map
required by [language-coverage.md](language-coverage.md) for both coverage modes
when snapshot evidence is required. Reject output from an obsolete candidate or
dependency revision. Separate review files avoid concurrent writes to one log.

## Capability fallbacks

| Missing capability | Behavior |
|---|---|
| Model-tier resolution | Use `unknown` → economy routing |
| Per-role model selection | Ask whether to inherit the parent or use self-only review; do not silently override the user's choice |
| Delegation | Parent performs the checks; mark `self_only` |
| Background work | Run reviewers in foreground; do not claim concurrency |
| Interruption | Let obsolete review finish, preserve it as stale, and recheck changed content |
| Resume handle | Resume from the immutable original, current candidate, dependency revisions, and review files |

`context_revision` identifies the inherited physics spine, neighboring text,
and manuscript conventions supplied to the review. It excludes the object
ledger, whose applicable revision is recorded separately.

Content quality and verification independence are separate. A fallback changes
the latter; it does not fabricate a content `PASS` or `FIX`.

## Legacy closure

Any job without `harness_version: 2` is closed historical evidence. Do not
resume or translate it. Start a fresh version-2 job with new snapshots and all
quality and coverage results pending.
