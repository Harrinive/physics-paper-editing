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
| `scientific_fidelity` | Nothing was invented, and no supplied mechanism, limitation, scope, or claim strength that the story needs was lost ([narrative.md](../physics-paper-principles/narrative.md), carefulness carries the argument) |
| `physics_lead` | The physically native quantity leads; every story-bearing helper has an earned role, scope, factor choice, and payoff |
| `formal_validity` | Every statement in the declared formal-review scope (`changed`, `dependency_closure`, or `all_in_scope`) is valid and agrees with the prose |
| `terminology_notation` | Every technical term, shortened name, abbreviation, alias, and symbol preserves the source, project vocabulary, and field-standard meaning, or is allowed by [names-and-symbols.md](../physics-paper-principles/names-and-symbols.md); the banned-name scan of the whole registry has no hit; when symbols are present, each character's type (italic or roman) matches the Symbol typography section of [math.md](../physics-paper-principles/math.md) |
| `prose` | Every sentence in the declared language coverage satisfies all applicable sentence principles; when the unit is a figure or table caption, every applicable [caption.md](../physics-paper-principles/caption.md) principle also passes; and the passage is clear, economical, coherent, and locally grammatical |

`physics_lead` is not a synonym for style or brevity. A mathematically correct
but narratively unearned definition is `FIX`.

## Canon binding

An axis may be `PASS` only when no applicable canon principle assigned to that
axis fails within the required edit scope, apart from a principle set aside with
its reason ([SKILL.md](../physics-paper-principles/SKILL.md), status of the
canon). Routing changes who checks the text and whether review is independent;
it does not lower the quality bar. A general impression that the passage reads
well does not override a specific terminology, notation, logic, object-choice,
sentence, narrative, or caption `FIX`. Record each principle set aside with its
reason: in a section round with `waive --reason`, otherwise in the note of the reply.

Inspection coverage and authorized repair scope are distinct. Review may expose
a problem outside the requested edit, but noticing it does not authorize a
silent repair.

**A scientific defect in the author's source.** This covers a newly discovered
defect inside or outside the language coverage, marked `USER_DECISION`. Do not
repair it silently, unless the request already authorized that repair. Preserve
the source, log the defect with one recommended repair, and hold only the work
that depends on it: the passage itself and anything whose meaning would change
with the answer. Other work continues. If the author is present, ask now;
otherwise report the decision when the run ends. The round closes only after the
author rules. Stop the whole task only when the defect undermines the basis of
the remaining work.

A defect introduced in the candidate must be repaired and rechecked; it is not an
author decision.

An unauthorized, non-scientific observation outside the repair scope is an
advisory, not an axis failure for the authorized span. Record it without
editing that context or claiming that the unreviewed context passed. Within the
declared inspection coverage, every applicable principle is still checked.

The prose axis is evaluated under the declared coverage contract. Under
`selective`, it combines chunk-level prose quality with current checks of every
changed, newly written, or diagnosed sentence. Under `exhaustive`, it is `PASS`
only when every sentence has a current-snapshot `PASS` as defined in
[language-coverage.md](language-coverage.md).

## Required axes

- **Substantive edit:** fidelity, physics lead, terminology/notation, and prose
  must pass. Formal validity must pass for the declared formal-review scope.
- **Copyedit:** fidelity, terminology/notation, and prose must pass. Formal
  validity must also pass whenever `formal_review_scope` is not `none`. A newly
  discovered scientific defect in the author's source never becomes a
  completion-time limitation.

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

- Read the project's rulings file, when there is one, before weighing findings.
  A ruled decision is settled. Do not reopen it on grounds of style or
  preference; a finding against it must show a scientific error or a
  contradiction with another ruling. The agent keeps its own judgment: when it
  thinks a ruling harms the text, it leaves the text as ruled and says so once
  in its report, with its reason. The author decides.
- Repair a clear finding supported by the source and recheck the affected axis.
  The limit on repairs ([review-prompts.md](review-prompts.md)) binds the editor
  as it binds a reviewer.
- A `story_check` finding is decided here: the editor reads the sentence against
  what its paragraph is for and applies the canon's rule for a hard sentence or
  an unneeded clause. Under a copyedit it is reported, not applied.
- A change the request did not ask for that moves or deletes a clause of the
  author's wording, or rewrites an author's sentence, is shown to the author before
  and after. Only a minor language repair that leaves the meaning, the flow, and the
  level of detail as they are may be silent.
- Do not repair a newly discovered source-level scientific defect outside the
  user's authorized objective; follow the rule for such a defect above.
- Do not convert a reviewer's `FIX` to `PASS` merely because the editor prefers
  its own draft.
- Conflicting scientific repairs require an adjudicator or the author.
- Stylistic disagreement may be resolved by the editor using the requested
  voice and minimal-change constraint.
- Reader load (sentence principle 16) is not style. When a scientific repair
  makes a sentence fail it, find a wording that satisfies both. When none
  exists, keep the correct wording and record why.
- Report missing independent verification separately from content quality; it
  does not fabricate a failed content axis.

## User-facing output

Normally return only the revised text and a concise note about any meaningful
scientific decision. Expose the schema when it helps audit a high-risk edit or
when completion is not `ready`; do not turn it into routine ceremony.
