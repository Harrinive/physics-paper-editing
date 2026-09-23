# Adaptive routing

Select the editing path from two independent facts: **scientific risk** and the
available editor's **model tier**. Do not use passage length or model price as a
proxy for scientific risk.

## Version-2 state

```yaml
harness_version: 2
edit_intent: copyedit | substantive
model_tier: strong | economy | unknown
tier_source: adapter | user | inherited | fallback
scientific_risk: low | medium | high
language_coverage: selective | exhaustive
execution_path: direct | guided | independent
verification_independence: independent | self_only | unavailable
```

Adapters map known models to capability tiers. The portable core never names a
vendor model. Treat `unknown` as `economy`. A user may override the tier or ask
for stronger verification.

## Risk classification

| Risk | Trigger |
|---|---|
| `low` | Grammar, punctuation, notation formatting, or local clarity without changing claims, equations, order, definitions, or symbols |
| `medium` | Every substantive rewrite; a new/redefined object; changed normalization or factor placement; reordered explanation; equation exposition; approximation language |
| `high` | Changed derivation, hypothesis, quantifier, scientific claim, coupled definition, cross-section consequence, or uncertain physical meaning |

A new symbol, definition, normalization, or moved prefactor makes the task at
least medium risk. When the context cannot resolve an essential scientific
meaning, stop that decision and ask the author; stronger review cannot supply
missing intent.

Classify risk from the scientific difference between the source-supported
meaning and the proposed output, not from the user's label or the quality of a
candidate draft. Removing or correcting an unsupported scientific assertion in
a candidate is at least medium risk even when the source fixes the answer. It
becomes high risk when the repair changes a derivation, hypothesis, quantifier,
cross-section consequence, or scientifically ambiguous claim.

## Routing matrix

| Risk | Strong editor | Economy or unknown editor |
|---|---|---|
| Low | `direct` | scaffolded `direct` |
| Medium | `guided` | scaffolded `guided` with a capable holistic reviewer |
| High | `independent` | capable scientific editor/reviewers; economy models only for bounded preparation or local repair |

User constraints on delegation override worker launch. In that case retain the
required quality checks in the parent and record `self_only`; never claim
independent review.

Language coverage is orthogonal to this matrix. Exhaustive coverage does not
raise scientific risk, but it requires the current-snapshot per-sentence record
defined in [language-coverage.md](language-coverage.md). It uses at most one
language reviewer per chunk, not one worker per sentence.

## Path contracts

### Direct

- Build a private physics spine and any triggered object ledger.
- Draft and run the quality axes yourself.
- Check every changed or newly written sentence against all 15 sentence
  principles, and run every applicable passage, math, and object check.
- Treat “compact self-check” as compact private evidence, not reduced canon
  coverage.
- Launch no workers and create no job state.

### Guided

- Draft from the physics spine and object ledger.
- Complete the editor's canon closure before independent review.
- Launch one holistic reviewer using [review-prompts.md](review-prompts.md).
- Add one math reviewer only if formal content changed.
- Repair `FIX` findings and recheck the affected axis.

### Independent

- Complete the editor's canon closure before independent review.
- Launch a holistic reviewer and, when formal content is present, a math
  reviewer independently.
- Aggregate axis results mechanically using [quality-contract.md](quality-contract.md).
- Launch an adjudicator only when reviewers propose incompatible scientific
  resolutions. Do not use one for stylistic disagreement.

## Compatibility mapping

For a new job receiving old options:

- `job_mode: polish` → `edit_intent: copyedit`, unless the requested change is
  scientifically substantive.
- `job_mode: rewrite|mixed` → `edit_intent: substantive`.
- `pace: fast` → adaptive routing.
- `pace: full` → at least `independent` scientific review; it does not by
  itself imply exhaustive sentence coverage.

Existing version-1 jobs are closed history. Start a new version-2 job with
fresh routing, coverage, and pending quality state.
