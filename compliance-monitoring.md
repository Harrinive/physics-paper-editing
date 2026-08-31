# Compliance monitoring (orchestrator ↔ workers ↔ synthesizer)

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. **Read with the Read tool** before launching any verifier `Task` (Phase 1 or Phase 2) or grading a chunk PASS.

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

**User constraints** limit what prose may change; they never waive Phase 2 or
synthesizer authority. Phase 1 routing is pace-aware: fast polish is INLINE,
full polish uses sentence Tasks.

---

## Task plan block (orchestrator — hard stop before Tasks)

The producer **must** emit this block in the turn response **before** the first verifier `Task`. Paste the **identical** block into **every** worker prompt under `## Orchestrator task plan`.

```markdown
## Orchestrator task plan (workers: verify in Step 0)
scope_id: <chunk_id or passage id>
edit_gate: polish | rewrite
pace: fast | full
N: <total sentences S1…SN>
phase: Phase 1 | Phase 2  # publish once, at the first Task launch this turn — Phase 2 when Phase 1 ran INLINE with no Tasks to publish for
phase1_sentence_tasks: <N labels | "INLINE" | "0 (rewrite/skipped)">
phase2_changed_labels: <list or "none">
phase2_sentence_tasks: <C labels or "0">
phase2_math_task: launched | skipped (no equations)
batching: none | "<note if §3.1 batch only>"
caller: micro | section-orchestrator
```

`phase2_math_task` is always `launched` except on `edit_gate: polish` + `pace: fast` + `caller: micro`, where it may be `skipped (no equations)` per the mechanical test in [fast-polish.md](fast-polish.md) § 1. On any other combination, `skipped` is a plan defect.

**Rules the plan must satisfy:**

| Condition | Required plan |
|-----------|----------------|
| `edit_gate: polish`, `pace: fast` | `phase1_sentence_tasks: INLINE`; zero Phase 1 sentence Tasks; producer runs all 13 checks on source |
| `edit_gate: polish`, `pace: full`, N ≥ 2 | `phase1_sentence_tasks` lists **N** distinct labels (one Task each) |
| `edit_gate: rewrite` | `phase1_sentence_tasks: 0` |
| Phase 2 | `phase2_sentence_tasks` = one label per **changed** sentence only |
| N ≤ 10 | `batching: none` — **forbidden** to batch multiple sentences per Task |
| `phase2_math_task: skipped (no equations)` | Only valid when `edit_gate: polish`, `pace: fast`, `caller: micro`, and no equations per [fast-polish.md](fast-polish.md) § 1 |

**Forbidden launches** (workers must `COMPLIANCE: FAIL`):

- One Task prompt containing multiple sentence labels (e.g. “S1–S3”, “all sentences in chunk”)
- `phase1_sentence_tasks: 0` when `edit_gate: polish`
- Any Phase 1 sentence Task when `pace: fast`
- Phase 2 sentence Task for an **unchanged** label
- Missing Task plan in worker prompt
- `phase2_math_task: skipped` when `caller: section-orchestrator`, `pace: full`, or `edit_gate: rewrite` — the skip is standalone-fast-polish only
- `phase2_math_task: skipped (no equations)` while the quote or draft contains any trigger from [fast-polish.md](fast-polish.md) § 1

---

## Worker Step 0 — assignment compliance (all workers)

Every worker runs **Step 0 first**. If `COMPLIANCE: FAIL`, **stop** — do not run specialist checks.

### Sentence worker (label S*k*)

**PASS** only if:

- Prompt assigns **exactly one** label S*k* and **one** sentence body (not a range, not “check all sentences”)
- `Your assignment` names S*k* matching the Task description (`Phase1 sentence: S2` / `Phase2 sentence verify: S2`)
- Phase 2: label is listed in `phase2_changed_labels`
- Phase 1 full-pace polish: label appears in `phase1_sentence_tasks`

**FAIL** examples: batched S1–S3; wrong label; Phase 2 on unchanged S*k*.

### Narrative worker

**PASS** only if:

- Receives **full passage** (all N sentences), not a fragment
- Task plan present with N matching passage sentence count
- Phase 1 fast polish: plan shows `phase1_sentence_tasks: INLINE`
- Phase 1 full polish + N ≥ 2: plan shows **N** distinct labels

**FAIL** examples: fragment only; plan says `phase1_sentence_tasks: 1` but N = 3.

### Math worker

Same scope rules as narrative. **FAIL** if math Task on prose-only passage without explicit N/A in plan.

**Fast polish, standalone micro** ([fast-polish.md](fast-polish.md)): when `phase2_math_task: skipped (no equations)`, no math Task is launched — there is nothing for a math worker to grade, and this is **not** a violation. The synthesizer accepts a `skipped` math report in its place (§ Synthesizer below). A math Task launched **despite** `skipped` in the plan, or a plan showing `skipped` while the passage or draft contains a § 1 trigger, is a `COMPLIANCE: FAIL`-worthy plan defect.

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
   - Phase 1 fast polish: `phase1_sentence_tasks == INLINE`
   - Phase 1 full polish: `len(phase1_sentence_tasks) == N`
   - Phase 2: `len(phase2_sentence_tasks) == C` and Mode line `M == C` (sentence Tasks only)
   - `phase2_math_task`: `skipped (no equations)` is valid **only** when `edit_gate: polish`, `pace: fast`, `caller: micro` — otherwise it is a plan defect ([fast-polish.md](fast-polish.md) § 4)
   - Received sentence reports: one per launched label; **no** `sentence_S1-S3` range lines in CHECKS
3. **Severity adjudication** — apply the closed BLOCKER classes in
   [narrative-checks.md](narrative-checks.md) and
   [math-checks.md](math-checks.md). Downgrade any out-of-list BLOCKER to
   SUGGEST and record the downgrade. Never upgrade a SUGGEST without naming the
   matching class. On fast polish (standalone micro), also apply the word-delta
   class and inherited-issue rule in [fast-polish.md](fast-polish.md) § 2.
4. **Content** — unresolved BLOCKERs fail; SUGGESTS do not fail or trigger a
   re-loop. A math report of `skipped — no equations per Task plan` is not a
   missing report and does not fail procedurally.

Emit in CHECKS:

```text
compliance_orchestrator_plan: PASS | FAIL
compliance_worker_reports: PASS | FAIL
<one line per sentence label: sentence_S1: PASS | ...>
...
math_step0: PASS | FAIL | N/A | N/A (skipped)
packet_gap: <count — 0 if none reported>
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
| `phase1_sentence_tasks: 0` on fast polish | `INLINE`; producer runs all 13 source checks |
| Fast polish launches Phase 1 Tasks | INLINE Phase 1; Phase 2 remains unchanged |
| Full polish batches ≤10 sentences | One Task per sentence |
| `phase2_math_task: skipped` on `caller: section-orchestrator` or `pace: full` | Chunks and full pace always launch math when applicable ([fast-polish.md](fast-polish.md)) |
| Math skipped while quote/draft has math | Re-run § 1's test; launch math Task |
| Orchestrator sets `OVERALL` or edits CHECKS | Synthesizer only |
| Section orchestrator launches verifier Tasks | Chunk agent (micro producer) only |

---

## Section orchestrator (macro)

The section orchestrator is monitored indirectly:

- Must pass full **Task plan** + `chunk_id` + `edit_gate` + `pace` + `N` into every micro chunk invocation ([chunk-contract.md](../physics-paper-editing-section/chunk-contract.md)).
- Must **not** launch micro verifier Tasks itself.
- First applicable **sentence worker** and **narrative worker** receive
  `caller: section-orchestrator`; they FAIL if handoff omits `chunk_id`,
  `edit_gate`, `pace`, or `N`.

Record synthesizer outcome in `session.md` § **Last turn compliance** (written from CHECKS, not by orchestrator).
