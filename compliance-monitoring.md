# Compliance monitoring (orchestrator ↔ workers ↔ synthesizer)

**Read with the Read tool** before launching any verifier `Task` (Phase 1 or Phase 2) or grading a chunk PASS.

Applies to **standalone micro** and **macro Stage D** chunk agents. **Writer ≠ grader:** producer/orchestrator never sets `OVERALL`; synthesizer only. **Orchestrator ≠ self-auditor:** section orchestrator does not launch micro verifier Tasks ([cross-skill.md](cross-skill.md) — macro/maintainer context only).

Workers grade **orchestrator dispatch** before specialist work. The **synthesizer** grades worker homework **and** merges procedural compliance. The producer/orchestrator **never** self-certifies task counts.

---

## Accountability chain

```
Orchestrator (producer / section orchestrator)
    │ publishes Task plan; launches Tasks
    ▼
Workers (sentence · narrative · math)
    │ Step 0: COMPLIANCE on assignment → then specialist checks
    ▼
Synthesizer
    │ procedural COMPLIANCE merge + content CHECKS → OVERALL
    ▼
Ship (only if OVERALL: PASS and procedural PASS)
```

| Tier | Dispatches? | Monitored by | Grades OVERALL? |
|------|-------------|--------------|-----------------|
| Orchestrator / producer | Yes | Workers + synthesizer | **No** |
| Sentence worker S*k* | No | Self (assignment) + synthesizer | No |
| Narrative / math workers | No | Self (assignment) + synthesizer | No |
| Synthesizer | No | — | **Yes (sole)** |

**User constraints** (e.g. “minor edits only”, “log narrative/math”) limit **what prose may change** — they **never** waive one-sentence-per-Task, Phase 1 SUBAGENTS on polish, or synthesizer authority.

---

## Task plan block (orchestrator — hard stop before Tasks)

The producer **must** emit this block in the turn response **before** the first verifier `Task`. Paste the **identical** block into **every** worker prompt under `## Orchestrator task plan`.

```markdown
## Orchestrator task plan (workers: verify in Step 0)
scope_id: <chunk_id or passage id>
edit_gate: polish | rewrite
N: <total sentences S1…SN>
phase: Phase 1 | Phase 2
phase1_sentence_tasks: <N labels or "0 (rewrite/skipped)">
phase2_changed_labels: <list or "none">
phase2_sentence_tasks: <C labels or "0">
batching: none | "<note if §3.1 batch only>"
caller: micro | section-orchestrator
```

**Rules the plan must satisfy:**

| Condition | Required plan |
|-----------|----------------|
| `edit_gate: polish`, N ≥ 2 | `phase1_sentence_tasks` lists **N** distinct labels (one Task each) |
| `edit_gate: rewrite` | `phase1_sentence_tasks: 0` |
| Phase 2 | `phase2_sentence_tasks` = one label per **changed** sentence only |
| N ≤ 10 | `batching: none` — **forbidden** to batch multiple sentences per Task |

**Forbidden launches** (workers must `COMPLIANCE: FAIL`):

- One Task prompt containing multiple sentence labels (e.g. “S1–S3”, “all sentences in chunk”)
- `phase1_sentence_tasks: 0` when `edit_gate: polish` and N ≥ 2
- Phase 2 sentence Task for an **unchanged** label
- Missing Task plan in worker prompt

---

## Worker Step 0 — assignment compliance (all workers)

Every worker runs **Step 0 first**. If `COMPLIANCE: FAIL`, **stop** — do not run specialist checks.

### Sentence worker (label S*k*)

**PASS** only if:

- Prompt assigns **exactly one** label S*k* and **one** sentence body (not a range, not “check all sentences”)
- `Your assignment` names S*k* matching the Task description (`Phase1 sentence: S2` / `Phase2 sentence verify: S2`)
- Phase 2: label is listed in `phase2_changed_labels`
- Phase 1 polish: label appears in `phase1_sentence_tasks`

**FAIL** examples: batched S1–S3; wrong label; Phase 2 on unchanged S*k*.

### Narrative worker

**PASS** only if:

- Receives **full passage** (all N sentences), not a fragment
- Task plan present with N matching passage sentence count
- Phase 1 polish + N ≥ 2: plan shows `phase1_sentence_tasks` with **N** labels (cross-check orchestration)

**FAIL** examples: fragment only; plan says `phase1_sentence_tasks: 1` but N = 3.

### Math worker

Same scope rules as narrative. **FAIL** if math Task on prose-only passage without explicit N/A in plan.

### Worker output format (prepend to every report)

```text
### Assignment compliance
COMPLIANCE: PASS | FAIL
Role: sentence | narrative | math
Label: S<k> | full-passage | N/A
Reason: <one line if FAIL; "assignment matches task plan" if PASS>

### Specialist verification
<role-specific report — omit if COMPLIANCE: FAIL>
```

Workers **must not** fix orchestrator mistakes — only report `COMPLIANCE: FAIL`.

---

## Synthesizer — procedural + content grading

The synthesizer merges in **order**:

1. **Procedural compliance** — any worker `COMPLIANCE: FAIL` → `OVERALL: FAIL` (procedural); do not ship.
2. **Task plan audit** — independent of workers:
   - Phase 1 polish: `len(phase1_sentence_tasks) == N`
   - Phase 2: `len(phase2_sentence_tasks) == C` and Mode line `M == C` (sentence Tasks only)
   - Received sentence reports: one per launched label; **no** `sentence_S1-S3` range lines in CHECKS
3. **Content** — merge specialist FAIL items from workers that passed Step 0.

Emit in CHECKS:

```text
compliance_orchestrator_plan: PASS | FAIL
compliance_worker_reports: PASS | FAIL
<one line per sentence label: sentence_S1: PASS | ...>
...
OVERALL: PASS | FAIL
```

**Procedural FAIL** → producer relaunches with corrected Task plan and **fresh** Tasks (never resume old workers).

---

## CHECKS block rules

| Rule | Example |
|------|---------|
| **One line per sentence label** | `sentence_S2: PASS` |
| **Forbidden range notation** | `sentence_S1-S3: PASS` |
| **Include compliance lines** | `compliance_orchestrator_plan: PASS` |
| **Synthesizer sets OVERALL only** | Producer copies verbatim |

---

## Anti-patterns (orchestrator violations)

| ❌ Violation | ✅ Correct |
|-------------|-----------|
| `Task(description: "sentence verify c11", prompt: "S1, S2, S3…")` | `Task(description: "Phase1 sentence: S1")` × N |
| `sentence_S1-S6: skipped` with 0 Phase 1 Tasks on polish | N Phase 1 Tasks; Phase 2 only on changed |
| Loop / “minor only” / speed | Does **not** reduce Task count |
| Orchestrator sets `OVERALL` or edits CHECKS | Synthesizer only |
| Section orchestrator launches verifier Tasks | Chunk agent (micro producer) only |

---

## Section orchestrator (macro)

The section orchestrator is monitored indirectly:

- Must pass full **Task plan** + `chunk_id` + `edit_gate` + `N` into every micro chunk invocation ([chunk-contract.md](../physics-paper-editing-section/chunk-contract.md)).
- Must **not** launch micro verifier Tasks itself.
- First **sentence worker** (S1) and **narrative worker** receive `caller: section-orchestrator` in the plan; they FAIL if handoff omits `chunk_id`, `edit_gate`, or `N`.

Record synthesizer outcome in `session.md` § **Last turn compliance** (written from CHECKS, not by orchestrator).
