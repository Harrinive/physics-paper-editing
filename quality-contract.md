# Quality contract

Version-2 editing separates prose quality from execution mechanics. Workers,
snapshots, and model identities do not determine whether the passage is good.

## Result schema

```yaml
quality:
  scientific_fidelity: PASS | FIX | USER_DECISION | N/A
  physics_lead: PASS | FIX | USER_DECISION | N/A
  formal_validity: PASS | FIX | USER_DECISION | N/A
  prose: PASS | FIX | USER_DECISION | N/A
completion: ready | needs_fix | needs_user
```

## Axis meanings

| Axis | Pass criterion |
|---|---|
| `scientific_fidelity` | No supplied mechanism, limitation, scope, or claim strength was lost or invented |
| `physics_lead` | The physically native quantity leads; every story-bearing helper has an earned role, scope, factor choice, and payoff |
| `formal_validity` | Changed definitions, equations, implications, approximations, imports, and conventions are valid |
| `prose` | The edited passage is clear, economical, coherent, and locally grammatical |

`physics_lead` is not a synonym for style or brevity. A mathematically correct
but narratively unearned definition is `FIX`.

The prose axis is evaluated under the declared coverage contract. Under
`selective`, it combines chunk-level prose quality with current checks of every
changed or diagnosed sentence. Under `exhaustive`, it is `PASS` only when every
sentence has a current-snapshot `PASS` as defined in
[language-coverage.md](language-coverage.md).

## Required axes

- **Substantive edit:** fidelity, physics lead, and prose must pass. Formal
  validity must pass whenever mathematical or logical content is present.
- **Copyedit:** fidelity and prose must pass. A pre-existing physics-lead issue
  is advisory unless the edit changes that object, its factors, or its role.

## Deterministic completion

1. Any required `USER_DECISION` → `completion: needs_user`.
2. Otherwise any required `FIX` → `completion: needs_fix`.
3. Otherwise → `completion: ready`.

Completion also requires a matching live snapshot and complete evidence for
the declared language coverage. A stale, skipped, or historical result cannot
satisfy an axis.

`N/A` is allowed only when an axis truly has no object to inspect—for example,
formal validity on equation-free copyediting. Do not produce principle-by-
principle `N/A` lists.

## Applying review findings

- Repair a clear finding supported by the source and recheck the affected axis.
- Do not convert a reviewer's `FIX` to `PASS` merely because the editor prefers
  its draft.
- Conflicting scientific repairs require an adjudicator or the author.
- Stylistic disagreement may be resolved by the editor using the requested
  voice and minimal-change constraint.
- Report missing independent verification separately from content quality; it
  does not fabricate a failed content axis.

## User-facing output

Normally return only the revised text and a concise note about any meaningful
scientific decision. Expose the schema when it helps audit a high-risk edit or
when completion is not `ready`; do not turn it into routine ceremony.
