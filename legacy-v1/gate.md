# Gate routing: job × pace

**For agents:** Start with [LEGACY.md](LEGACY.md) § Agent read order. **Read with the Read tool** at intake.

There is **no blocking source-audit phase**. This file routes how the draft is produced and how thorough verification is. The user never waits on pace.

**Do not run sentence-level verifier jobs until the draft is marked and snapshotted** ([coworker-loop.md](coworker-loop.md)).

---

## Sentence-count thresholds

| Count | Effect |
|-------|--------|
| **1** (or fragment) | Micro-eligible |
| **2–10** | Micro-eligible; one verifier assignment per changed sentence |
| **11–12** | Micro-eligible; may batch two sentences per assignment ([sentence-check-subagents.md](sentence-check-subagents.md) §3.1) |
| **>12** | **Not feasible** — route to [physics-paper-editing-section](../../physics-paper-editing-section/legacy-v1/LEGACY.md) or **ASK USER** to narrow |

---

## Independent choices

| Choice | Values | Controls |
|--------|--------|----------|
| **Job** | `polish` \| `rewrite` | Tighten existing prose vs compose substantially new prose |
| **Pace** | `fast` \| `full` | Verification scope only. At `polish` + standalone micro, `fast` narrows the narrative/math question and may skip math verification — [fast-polish.md](fast-polish.md). Never skips the synthesizer or a changed sentence's verifier assignment |

All four combinations are valid. Ask **job** only when unclear. At the start of a top-level editing session, collect one model-profile choice: accept the role-based profile, use the parent model for all roles, or provide custom mappings. Persist it under [runtime-contract.md](runtime-contract.md). Reuse a profile only when it is user-confirmed for this job or explicitly inherited from a confirmed section session. A no-interaction fallback cannot authorize worker launch.

Default pace when unset: `fast`.

---

## Decision tree

### Q1: How many typographic sentences?

```
Q1: How many sentences?
    │
    ├─ ≤12 ──► intake: job if unclear; resolve the confirmed model profile
    └─ >12 or whole section ──► section skill / narrow scope
```

Count by [sentence-check-subagents.md](sentence-check-subagents.md) §2. A source
line containing three typographic sentences counts as three.

### Q2: Job — rewrite or polish?

**Major rewrite** = substantially new prose, not tightened wording in place.

| Treat as **yes** | Treat as **no** (polish) |
|------------------|--------------------------|
| Recompose / redraft / start over | Grammar, clarity, notation, citations, tone |
| New structure or argument order | Light reordering within same claims |
| Change voice or level so sentences are not tightened originals | Word choice within same sentence roles |
| Substantially reframe a definition or its physical argument | Clarify a supported physical role or tighten an equivalent definition in place |

```
Q2: Job?
    │
    ├─ rewrite ─► compose draft; every sentence is “changed” for checkers
    └─ polish ──► tighten in place; checkers run on changed labels only
```

For a named physical object, run [physical-lead.md](../../physics-paper-principles/legacy-v1/physical-lead.md) and consider the definition form. Construction does not force rewrite or a halt. Ask only if an essential scientific choice cannot be resolved from supplied context ([coworker-loop.md](coworker-loop.md) § Definition halt).

### Q3: Pace — verification scope (do not ask every job)

```
Q3: Pace?  (inherit or default fast)
    │
    ├─ fast ─► standalone micro + polish: delta-scoped narrative/math ([fast-polish.md](fast-polish.md))
    └─ full ─► full passage-vs-manuscript narrative + math
```

**Fast does not skip checks** on changed sentences. It never applies to macro chunks (`caller: section-orchestrator`) or to rewrite.

### Full-pace / long-quote feasibility

**Feasible** when roughly all hold:

- ≤12 complete sentences (not a full section or paper).
- Mostly checkable prose (not mostly display equations, tables, or bare lists).
- Splittable without breaking inside math, `\cite{}`, `\ref{}`, or essential cross-references.

**>12 sentences or whole-section edit:** route to [physics-paper-editing-section](../../physics-paper-editing-section/legacy-v1/LEGACY.md). Do not run the micro loop on the full section in one turn.

If a ≤12 split is not feasible: collect one user decision — section skill / proceed with partial coverage / narrow the quote.

---

## Outcomes

| Job | Pace | Draft | Background checks |
|-----|------|-------|-------------------|
| polish | fast | Tighten in place | Changed sentences + fast-polish narrative; math may skip |
| polish | full | Tighten in place | Changed sentences + full narrative/math |
| rewrite | fast | Compose | Every sentence + full narrative/math (no math skip) |
| rewrite | full | Compose | Every sentence + full narrative/math |

There is no pre-draft sentence-verifier wave.

---

## User-decision prompts

### Sentence-level checking (split not feasible)

**Title:** *Sentence-level checking*

| Option | Then |
|--------|------|
| Use section skill (Recommended) | Route to [physics-paper-editing-section](../../physics-paper-editing-section/legacy-v1/LEGACY.md) |
| Proceed with partial coverage | One verifier assignment per splittable sentence; note gaps |
| Narrow the scope | User gives shorter quote; re-count |

### Editing setup

Ask **only** what is unresolved:

1. Job: light polish or substantial rewrite (omit if clear).
2. Model profile: ask once for the top-level session unless a confirmed parent profile is inherited; use the three choices in [runtime-contract.md](runtime-contract.md).

---

## Mode lines

Producer emits on the draft-ready turn ([user-communication.md](user-communication.md) audit drawer):

```
Mode: draft-ready · verify:running · <N> sentences
```

Per-round synthesizer ([phase2-verify-subagents.md](phase2-verify-subagents.md)):

```
Mode: verify-subagents · verify:<running|partial|complete> · <N> sentences · <C> changed · <M> verifier assignments · profile:<accepted_default|custom|inherit|fallback>
```
