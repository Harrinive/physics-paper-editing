# Gate routing: job × pace

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. **Read with the Read tool** when [SKILL.md](SKILL.md) steps **3 or 4** run.

**Phase 2 has no gate** — it always uses independent verifiers. This file routes
only how the draft is produced and how Phase 1 checks the user's source.

**Do not run sentence-level work until the gate for the current step is done.**

---

## Sentence-count thresholds

| Count | Effect |
|-------|--------|
| **1** (or fragment) | Micro-eligible; Phase 1 is INLINE |
| **2–10** | Micro-eligible; full pace may use one Task per sentence |
| **11–12** | Micro-eligible; full pace may batch 2 sentences per Task |
| **>12** | **Not feasible** — route to [physics-paper-editing-section](../physics-paper-editing-section/SKILL.md) or **ASK USER** to narrow |

---

## Independent choices

| Choice | Values | Controls |
|--------|--------|----------|
| **Job** | `polish` \| `rewrite` | Tighten existing prose vs compose substantially new prose |
| **Pace** | `fast` \| `full` | Phase 1 runner; at `polish` + standalone micro, also narrows the Phase 2 question and may skip the math Task — see [fast-polish.md](fast-polish.md). Never skips the synthesizer or a changed sentence's Task |

All four combinations are valid. A rewrite may be fast; a polish may be full.
Ask for both in the single intake after the ≤12-sentence scope check. Skip the
job question when the user's wording or placeholders make it unambiguous.

---

## Decision tree

### Q1: How many typographic sentences?

```
Q1: How many sentences?
    │
    ├─ ≤12 ──► intake: job + pace + models
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

```
Q2: Job?
    │
    ├─ rewrite ─► skip Phase 1; compose draft
    └─ polish ──► Q3 pace
```

### Q3: Pace — fast or full?

```
Q3: Pace?
    │
    ├─ fast ─► Phase 1 INLINE: producer runs all 13 checks on source
    └─ full ─► Phase 1 SUBAGENTS when split is feasible
```

**Fast does not skip checks.** It changes the Phase 1 runner. Phase 2 remains
the full independent sentence + narrative + synthesizer suite at every pace,
and the full narrative + math suite except in the one case below.

**Standalone micro exception:** at `edit_gate: polish` + `pace: fast` +
`caller: micro` (a direct short-quote edit, not a macro chunk), Phase 2
narrative and math ask a narrower question — did **this edit** change what
the source claimed — and math is skipped when there is no equation in the
quote or draft. Macro chunks and full pace never get this exception. Detail:
[fast-polish.md](fast-polish.md).

### Full-pace feasibility

**Feasible** when roughly all hold:

- ≤12 complete sentences (not a full section or paper).
- Mostly checkable prose (not mostly display equations, tables, or bare lists).
- Splittable without breaking inside math, `\cite{}`, `\ref{}`, or essential cross-references.
- Reasonable Task count ([sentence-check-subagents.md](sentence-check-subagents.md) §3).

```
Q3: Feasible split?
    │
    ├─ yes ─► SUBAGENTS (mandatory) — Tasks → merge
    │
    └─ no ───► ASK USER — then INLINE or SUBAGENTS per answer
```

**Not feasible** examples: >12 sentences, full section, mostly equations/tables, inseparable cross-references. Briefly say why.

**>12 sentences or whole-section edit:** route to [physics-paper-editing-section](../physics-paper-editing-section/SKILL.md) (macro skill). Do not proceed with the micro pipeline on the full section in one turn.

---

## Outcomes

| Job | Pace | Phase 1 | Phase 2 |
|-----|------|---------|---------|
| polish | fast | INLINE, all sentences | Full independent suite |
| polish | full | SUBAGENTS when feasible | Full independent suite |
| rewrite | fast | Skipped | Full independent suite |
| rewrite | full | Skipped | Full independent suite |

For one sentence, Phase 1 is INLINE at either pace.

---

## Rewrite path

When job → rewrite:

| Step | Runs? | Model AskQuestion? |
|------|-------|-------------------|
| Phase 1 (step 4) | **No** | **No** (no Phase 1 Tasks) |
| Phase 2 (step 6) | **Yes — always** | Models already confirmed in the single intake |

**Common mistake:** treating "Phase 1 skipped" as "skip Phase 2." Phase 2 is
independent at both paces.

---

## Strict mode

At **full** pace, when the gate yields SUBAGENTS, use them. At **fast** pace,
INLINE is the required Phase 1 route, not a shortcut or compliance violation.

**Forbidden when full-pace SUBAGENTS applies:** replacing it with INLINE;
launching zero Tasks; batching multiple sentences into one Task when N ≤ 10.
Fast INLINE is **not batching**.

If you edited without subagents when SUBAGENTS was required, stop, report the violation, and re-run the gate before further edits.

**Compliance:** Publish the Task plan before launching Tasks. Workers grade assignment in Step 0; synthesizer grades procedural compliance. See [compliance-monitoring.md](compliance-monitoring.md) § Anti-patterns.

---

## AskQuestion prompts

### Sentence-level checking (full-pace split not feasible)

**Title:** *Sentence-level checking*

| Option | Then |
|--------|------|
| Use section macro skill (Recommended) | Route to [physics-paper-editing-section](../physics-paper-editing-section/SKILL.md) — Stages A–E |
| Skip sentence-level subagents | INLINE — all 13 sentence checks, then passage-level checklists |
| Proceed with subagents anyway | SUBAGENTS — one Task per splittable sentence; note partial coverage |
| Narrow the scope | User gives shorter quote; re-run gate |

### Editing setup

Use one intake form after scope:

1. Job: light polish or substantial rewrite (omit if clear).
2. Pace: fast or full.
3. Independent-check model profile.

This replaces separate Phase 1 and Phase 2 model questions.

---

## Mode lines

**Phase 1** (producer emits when reporting gated work):

```
Mode: <inline | subagents | asked-user> · pace:<fast|full> · <N> sentences
```

Add `· <M> Tasks · <model slug>` when Phase 1 SUBAGENTS runs.

**Phase 2** (verifier synthesizer only — [phase2-verify-subagents.md](phase2-verify-subagents.md)):

```
Mode: verify-subagents · <N> sentences · <C> changed · <M> Tasks · sentence:<Q1 slug> · deep:<Q2 slug> · synth:<Q3 slug>
```
