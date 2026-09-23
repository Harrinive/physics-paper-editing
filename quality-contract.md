# Quality contract

Version-2 editing separates prose quality from execution mechanics. Editors,
snapshots, and model identities do not determine whether the passage is good.

## Result schema

```yaml
quality:
  scientific_fidelity: PASS | FIX | USER_DECISION | N/A
  physics_lead: PASS | FIX | USER_DECISION | N/A
  formal_validity: PASS | FIX | USER_DECISION | N/A
  terminology_notation: PASS | FIX | USER_DECISION | N/A
  prose: PASS | FIX | USER_DECISION | N/A
completion: ready | needs_fix | needs_user
```

## Axis meanings

| Axis | Pass criterion |
|---|---|
| `scientific_fidelity` | No supplied mechanism, limitation, scope, or claim strength was lost or invented |
| `physics_lead` | The physically native quantity leads; every story-bearing helper has an earned role, scope, factor choice, and payoff |
| `formal_validity` | Every statement in the declared formal-review scope (`changed`, `dependency_closure`, or `all_in_scope`) is valid and agrees with the prose |
| `terminology_notation` | Every technical term, shortened name, abbreviation, alias, and symbol preserves the source, project vocabulary, and field-standard meaning, or is necessary, defined, and consistently reused |
| `prose` | Every sentence in the declared language coverage satisfies all applicable sentence principles and the passage is clear, economical, coherent, and locally grammatical |

`physics_lead` is not a synonym for style or brevity. A mathematically correct
but narratively unearned definition is `FIX`.

## Canon binding

An axis may be `PASS` only when no applicable canon principle assigned to that
axis fails within the required edit scope. Routing changes who checks the text
and whether review is independent; it does not lower the quality bar. A
favorable holistic judgment cannot override a specific terminology, notation,
logic, object-choice, sentence, or narrative `FIX`.

Inspection coverage and authorized repair scope are distinct. Review may expose
a problem outside the requested edit, but noticing it does not authorize a
silent repair. A newly discovered scientific defect in the author's source,
whether inside or outside the language coverage, pauses the entire task with
`USER_DECISION` unless the user's request already authorized that scientific
repair. Preserve the source, describe the defect, and ask one focused question
about scope or intended meaning. A defect introduced in the candidate must be
repaired and rechecked; it is not an author decision.

An unauthorized, non-scientific observation outside the repair scope is an
advisory, not an axis failure for the authorized span. Record it without
editing that context or claiming that the unreviewed context passed. Within the
declared inspection coverage, every applicable principle remains mandatory.

The prose axis is evaluated under the declared coverage contract. Under
`selective`, it combines chunk-level prose quality with current checks of every
changed, newly written, or diagnosed sentence. Under `exhaustive`, it is `PASS`
only when every sentence has a current-snapshot `PASS` as defined in
[language-coverage.md](language-coverage.md).

## Required axes

- **Substantive edit:** fidelity, physics lead, terminology/notation, and prose
  must pass. Formal validity must pass for the declared formal-review scope.
- **Copyedit:** fidelity, terminology/notation, and prose must pass. Formal
  validity must also pass whenever `formal_review_scope` is not `none`. Any
  newly discovered scientific defect in the author's source pauses the task
  rather than becoming a completion-time limitation.

## Deterministic completion

1. Any required `USER_DECISION` → `completion: needs_user`.
2. Otherwise any required `FIX` → `completion: needs_fix`.
3. Otherwise → `completion: ready`.

When the selected workflow requires current-snapshot evidence—such as a
section-inherited, exhaustive, resumable, or concurrent review—completion also
requires a matching live snapshot and complete evidence for the declared
language coverage. A stale, skipped, or historical result cannot satisfy an
axis. An ordinary synchronous direct edit applies the same canon checks to the
text in hand without manufacturing snapshot state.

`N/A` is allowed only when an axis truly has no object to inspect—for example,
formal validity when the edited unit contains no relevant definition,
equation, approximation, implication, quantifier, convention, or logical
claim. Do not produce principle-by-principle `N/A` lists.

## Applying review findings

- Repair a clear finding supported by the source and recheck the affected axis.
- Do not repair a newly discovered source-level scientific defect outside the
  user's authorized objective; pause and ask first.
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
