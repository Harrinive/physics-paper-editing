# Gate routing (Phase 1 only)

**Read with the Read tool** when [SKILL.md](SKILL.md) steps **3 or 4** run.

**Phase 2 has no gate** — see [phase2-verify-subagents.md](phase2-verify-subagents.md). Phase comparison: [verification-loop.md](verification-loop.md) (canonical).

**Do not run sentence-level work until the gate for the current step is done.**

---

## Sentence-count thresholds

| Count | Effect |
|-------|--------|
| **1** (or fragment) | Always **INLINE** |
| **2–10** | Feasible for **SUBAGENTS** — one Task per sentence |
| **11–12** | Feasible; may batch 2 sentences per Task |
| **>12** | **Not feasible** — route to [physics-paper-editing-section](../physics-paper-editing-section/SKILL.md) or **ASK USER** to narrow |

---

## Two gate contexts

Same Q1–Q3 decision tree. **Count sentences in the target text for that context:**

| Context | Step | Count sentences in | Q2 |
|---------|------|-------------------|-----|
| Edit gate | 3 | User's quote / selection | Major rewrite? |
| Source verify gate | 4 (polish only) | User's quote / existing prose | Skipped — always polish |

- **Edit gate** routes production: compose vs polish + Phase 1.
- **Source verify gate** routes Phase 1 machinery: INLINE vs SUBAGENTS.

---

## Decision tree

### Q1: How many sentences?

```
Q1: How many sentences?
    │
    ├─ 1 (or fragment) ──────────────► INLINE
    │
    └─ 2+ ──► Q2 (edit gate) or Q3 (source verify gate)
```

### Q2: Major rewrite? (edit gate only)

**Major rewrite** = substantially new prose, not tightened wording in place.

| Treat as **yes** | Treat as **no** (polish) |
|------------------|--------------------------|
| Recompose / redraft / start over | Grammar, clarity, notation, citations, tone |
| New structure or argument order | Light reordering within same claims |
| Change voice or level so sentences are not tightened originals | Word choice within same sentence roles |

```
Q2: Major rewrite?
    │
    ├─ yes ─► INLINE — skip Phase 1; main agent composes draft (step 5)
    │
    └─ no ───► Q3
```

### Q3: Feasible split for subagent sentence checks?

**Feasible** when roughly all hold:

- ≤12 complete sentences (not a full section or paper).
- Mostly checkable prose (not mostly display equations, tables, or bare lists).
- Splittable without breaking inside math, `\cite{}`, `\ref{}`, or essential cross-references.
- Reasonable Task count ([sentence-check-subagents.md](sentence-check-subagents.md) §3).

```
Q3: Feasible split?
    │
    ├─ yes ─► SUBAGENTS (mandatory) — model AskQuestion → Tasks → merge
    │
    └─ no ───► ASK USER — then INLINE or SUBAGENTS per answer
```

**Not feasible** examples: >12 sentences, full section, mostly equations/tables, inseparable cross-references. Briefly say why.

**>12 sentences or whole-section edit:** route to [physics-paper-editing-section](../physics-paper-editing-section/SKILL.md) (macro skill). Do not proceed with the micro pipeline on the full section in one turn.

---

## Outcomes

| Situation | Edit gate (step 3) | Source verify gate (step 4) |
|-----------|-------------------|----------------------------|
| 1 sentence | INLINE | INLINE |
| 2+ polish, feasible split | SUBAGENTS | SUBAGENTS (mandatory) |
| Major rewrite | INLINE (compose); skip Phase 1 | Skipped — **Phase 2 AskQuestion still required** |
| Q3 not feasible | ASK USER | ASK USER |
| User requests inline / quick / no subagents | INLINE | INLINE |
| User chose skip / proceed / narrow (this quote, this chat) | Honor choice | Honor choice |

**Skip the Q3 AskQuestion** when Q1 → 1 sentence, Q2 → major rewrite, or Q3 → feasible (go straight to SUBAGENTS).

---

## Major rewrite path

When Q2 → major rewrite:

| Step | Runs? | Model AskQuestion? |
|------|-------|-------------------|
| Phase 1 (step 4) | **No** | **No** (no Phase 1 Tasks) |
| Phase 2 (step 6) | **Yes — always** | **Yes** — *Verifier model profile* ([phase2-verify-subagents.md](phase2-verify-subagents.md) § Model selection gate) |

**Common mistake:** treating "Phase 1 skipped" as "skip all model asks." Phase 2 is independent; compose → **AskQuestion** → verifier Tasks.

---

## Strict mode

When any gate yields **SUBAGENTS**, you **must** use subagents. **Never** substitute INLINE because the passage is short, simple, or you believe you can run the 13 checks yourself.

**Forbidden when SUBAGENTS applies:** applying sentence fixes yourself; skipping model AskQuestion; launching zero Tasks; **batching multiple sentences into one Task** when N ≤ 10 ([compliance-monitoring.md](compliance-monitoring.md)).

If you edited without subagents when SUBAGENTS was required, stop, report the violation, and re-run the gate before further edits.

**Compliance:** Publish the Task plan before launching Tasks. Workers grade assignment in Step 0; synthesizer grades procedural compliance. See [compliance-monitoring.md](compliance-monitoring.md) § Anti-patterns.

---

## AskQuestion prompts

### Sentence-level checking (Q3 not feasible)

**Title:** *Sentence-level checking*

| Option | Then |
|--------|------|
| Use section macro skill (Recommended) | Route to [physics-paper-editing-section](../physics-paper-editing-section/SKILL.md) — Stages A–E |
| Skip sentence-level subagents | INLINE — all 13 sentence checks, then passage-level checklists |
| Proceed with subagents anyway | SUBAGENTS — one Task per splittable sentence; note partial coverage |
| Narrow the scope | User gives shorter quote; re-run gate |

### Sentence checker model (SUBAGENTS)

**Always required** before launching Phase 1 sentence Tasks — [sentence-check-subagents.md](sentence-check-subagents.md) §4 (fast tier). Skip only when user already picked a model for **this same quote in this chat**.

Phase 2 uses the three-question *Verifier model profile* — [phase2-verify-subagents.md](phase2-verify-subagents.md) § AskQuestion. **Required on every first Phase 2 iteration**, including major rewrites. Never auto-select defaults.

---

## Mode lines

**Phase 1** (producer emits when reporting gated work):

```
Mode: <inline | subagents | asked-user> · <N> sentences
```

Add `· <M> Tasks · <model slug>` when Phase 1 SUBAGENTS runs.

**Phase 2** (verifier synthesizer only — [phase2-verify-subagents.md](phase2-verify-subagents.md)):

```
Mode: verify-subagents · <N> sentences · <C> changed · <M> Tasks · sentence:<Q1 slug> · deep:<Q2 slug> · synth:<Q3 slug>
```
