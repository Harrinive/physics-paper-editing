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
execution_path: direct | guided | independent | legacy_full
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

## Routing matrix

| Risk | Strong editor | Economy or unknown editor |
|---|---|---|
| Low | `direct` | scaffolded `direct` |
| Medium | `guided` | scaffolded `guided` with a capable holistic reviewer |
| High | `independent` | capable scientific editor/reviewers; economy models only for bounded preparation or local repair |

User constraints on delegation override worker launch. In that case retain the
required quality checks in the parent and record `self_only`; never claim
independent review.

## Path contracts

### Direct

- Build a private physics spine and any triggered object ledger.
- Draft and run the quality axes yourself.
- Launch no workers and create no job state.

### Guided

- Draft from the physics spine and object ledger.
- Launch one holistic reviewer using [review-prompts.md](review-prompts.md).
- Add one math reviewer only if formal content changed.
- Repair `FIX` findings and recheck the affected axis.

### Independent

- Launch a holistic reviewer and, when formal content is present, a math
  reviewer independently.
- Aggregate axis results mechanically using [quality-contract.md](quality-contract.md).
- Launch an adjudicator only when reviewers propose incompatible scientific
  resolutions. Do not use one for stylistic disagreement.

### Legacy full

Use only when the user explicitly requests it or an existing job lacks
`harness_version: 2`. Follow [legacy-v1/LEGACY.md](legacy-v1/LEGACY.md) without
mixing version-2 schemas into that live job.

## Compatibility mapping

For a new job receiving old options:

- `job_mode: polish` → `edit_intent: copyedit`, unless the requested change is
  scientifically substantive.
- `job_mode: rewrite|mixed` → `edit_intent: substantive`.
- `pace: fast` → adaptive routing.
- `pace: full` → at least `independent` review.

Existing version-1 jobs keep their original meanings.
