# Adaptive routing

Choose between two execution paths. The path controls independent verification;
scientific risk and content triggers determine which reviewers the reviewed
path launches. Passage length and model price are not proxies for risk.

## Version-2 state

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
principle_specialists: [P01, P02, ...]
```

Adapters map known models to capability tiers. The portable core never names a
vendor model. Treat `unknown` as `economy`. A user may override the tier or ask
for stronger verification.

## Risk classification

| Risk | Trigger |
|---|---|
| `low` | An exactly bounded grammar, punctuation, formatting, or local-clarity repair that changes no claim, equation, order, definition, term, or symbol |
| `medium` | Any substantive rewrite, terminology audit, new or renamed term or symbol, new or changed object, normalization or factor change, reordered explanation, equation exposition, or approximation language |
| `high` | A changed derivation, hypothesis, quantifier, scientific claim, coupled definition, cross-section consequence, or scientifically ambiguous meaning |

A new symbol, definition, normalization, or moved prefactor is at least medium
risk. Classify risk from the difference between the source-supported meaning
and the proposed output, not from the user's label or the apparent quality of a
candidate draft. Correcting an unsupported candidate assertion is at least
medium risk even when the source fixes the answer.

If the editor discovers a scientific defect in the author's source that the
user did not already authorize this task to repair, pause the entire task with
`needs_user`. State the defect and ask whether to expand the scope or supply the
intended science. Do not continue unrelated edits while that decision is open.
A defect introduced by the editor or a reviewer belongs to the candidate and
must be repaired rather than presented as an author decision.

## Routing matrix

| Condition | Path and profile |
|---|---|
| Exactly bounded low-risk work with no specialist trigger | `direct`; an economy or unknown editor uses the scaffold |
| Medium risk, an explicit language or terminology audit, or any independent-review request | `reviewed`, `standard` |
| High risk or a scientific conflict found during reviewed work | `reviewed`, `high_risk` |

Language coverage is orthogonal to this matrix. It determines which sentences
need current evidence, not which principles apply. Persistence is also
orthogonal: it depends on whether work is resumable, asynchronous, concurrent,
file-based, or exhaustive, not on the execution path.

Select `formal_review_scope` by the first matching row, in this order:

| Condition | Scope |
|---|---|
| No relevant definition, equation, approximation, implication, quantifier, convention, or logical claim | `none` |
| The work is high risk or explicitly requests a full formal audit | `all_in_scope` |
| A changed formal statement may affect in-scope dependent statements | `dependency_closure` |
| A formal statement or its prose exposition changes, and a dependency search establishes no in-scope dependents | `changed` |
| Relevant formal content is present but unchanged by the edit | `all_in_scope` |

The scope governs the formal-validity check whether it is self-checked under
`direct` or assigned to a formal reviewer under `reviewed`. Never use `none`
merely because formulas were left textually unchanged.

## Path contracts

### Direct

- Build a private physics spine and any triggered object ledger.
- Draft and run every required quality axis yourself.
- Check every in-scope sentence against all 15 sentence principles and resolve
  the terminology-and-notation delta for the edited unit.
- Launch no reviewer. An ordinary synchronous edit creates no job state, but a
  resumable or concurrent direct edit still uses the required persistence.
- After the first repair, any additional candidate or authorized in-scope
  principle `FIX`, `USER_DECISION`, or specialist trigger upgrades the task to
  `reviewed`. A defect explicitly named by the user and fully repaired in the
  candidate does not itself force an upgrade when the final direct check
  passes. Preserve an unauthorized, non-scientific observation outside the
  repair scope as an advisory; it neither authorizes a change nor certifies the
  untouched context.
- A newly discovered scientific defect in the author's source pauses the task
  under the rule above rather than causing a silent upgrade or repair.

### Reviewed

1. The editor drafts from the physics spine and object ledger and completes its
   own canon closure.
2. One independent sentence reviewer checks every sentence in the declared
   language coverage against all 15 principles.
3. One independent terminology-and-notation reviewer checks the entire edited
   unit against the source, surrounding manuscript, project vocabulary, and
   established field usage. This review is mandatory even when the sentence
   reviewer reports no terminology problem.
4. Any sentence principle reported as `FIX`, or as a non-scientific
   `USER_DECISION`, launches a whole-unit specialist for that principle or the
   tightly coupled group defined in [review-prompts.md](review-prompts.md). The
   specialist searches beyond the originally flagged sentence. A source-level
   scientific `USER_DECISION` pauses the task before further review.
5. One holistic physics-story reviewer checks the integrated candidate. When
   `formal_review_scope` is not `none`, add one formal reviewer for exactly the
   scope selected by the table above.
6. Under `high_risk`, the holistic and formal reviewers inspect the same frozen
   candidate independently, without seeing the editor's conclusions or one
   another's findings. Use an adjudicator only for incompatible supported
   scientific repairs.
7. Reviewers never write the live manuscript or file. The editor integrates
   exact proposed repairs, reruns every affected check, and reruns terminology
   review whenever a later repair changes terminology or notation.

If delegation is forbidden, perform the same checks in the strongest available
parent, record `self_only`, and do not claim independent verification. If a
required selected model is unavailable, stop before launching that reviewer
and ask the user for a replacement.

## Compatibility mapping

For a new job receiving old options:

- `job_mode: polish` → `edit_intent: copyedit`, unless the requested change is
  scientifically substantive.
- `job_mode: rewrite|mixed` → `edit_intent: substantive`.
- `pace: fast` → adaptive routing.
- `pace: full`, `guided`, or `independent` -> `reviewed`; use `high_risk` only
  when the scientific triggers above apply.

Existing version-1 jobs are closed history. Start a new version-2 job with
fresh routing, coverage, and pending quality state.
