# Compliance monitoring (orchestrator ↔ workers ↔ synthesizer)

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. **Read with the Read tool** before launching any verifier `Task` or closing a job round.

Applies to **standalone micro** and **macro Stage D** chunk agents. **Writer ≠ grader:** producer never sets `OVERALL`; synthesizer only. **Orchestrator ≠ self-auditor:** section orchestrator does not launch micro verifier Tasks ([cross-skill.md](../physics-paper-editing-section/cross-skill.md)).

Workers grade **orchestrator dispatch** before specialist work. The **synthesizer** grades worker homework **and** merges procedural compliance. The producer **never** self-certifies task counts.

`OVERALL` is a **job-round** status (`PASS` | `CONFLICTS` | `PARTIAL`). It does **not** gate the first `.tex` write.

---

## Accountability chain

```
Orchestrator (producer / section orchestrator)
    │ publishes Task plan; launches background Tasks
    ▼
Workers (sentence · narrative · math)
    │ Step 0: COMPLIANCE on assignment → specialist checks → append findings.jsonl
    ▼
Synthesizer (per round)
    │ procedural COMPLIANCE merge + content → OVERALL
    ▼
Merge (producer applies merge-policy.md; does not set OVERALL)
```

| Tier | Dispatches? | Monitored by | Grades OVERALL? |
|------|-------------|--------------|-----------------|
| Orchestrator / producer | Yes | Workers + synthesizer | **No** |
| Sentence worker S*k* | No | Self (assignment) + synthesizer | No |
| Narrative / math workers | No | Self (assignment) + synthesizer | No |
| Synthesizer | No | — | **Yes (sole)** |

User constraints limit what prose may change; they never waive background checks or synthesizer authority.

---

## Task plan block (hard stop before Tasks)

Emit this block **before** the first verifier `Task`. Paste the **identical** block into **every** worker prompt under `## Orchestrator task plan`.

```markdown
## Orchestrator task plan (workers: verify in Step 0)
scope_id: <chunk_id or passage id>
edit_gate: polish | rewrite
pace: fast | full
N: <total sentences S1…SN>
phase: background
job_id: <j12>
round: <n>
findings_path: <absolute path to findings.jsonl>
phase1_sentence_tasks: 0
phase2_changed_labels: <list or "none">
phase2_sentence_tasks: <C labels or "0">
phase2_math_task: launched | skipped (no equations)
batching: none | "<note if §3.1 batch only>"
caller: micro | section-orchestrator
```

`phase1_sentence_tasks` is always `0` — there is no blocking source-audit wave.

`phase2_math_task` is `launched` except on `edit_gate: polish` + `pace: fast` + `caller: micro`, where it may be `skipped (no equations)` per [fast-polish.md](fast-polish.md) § 1 (no equations **and** no named-object introduction).

**Rules the plan must satisfy:**

| Condition | Required plan |
|-----------|----------------|
| Any job | `phase1_sentence_tasks: 0` |
| Background wave | `phase2_sentence_tasks` = one label per **changed** sentence only |
| N ≤ 10 | `batching: none` |
| `phase2_math_task: skipped (no equations)` | Only when `edit_gate: polish`, `pace: fast`, `caller: micro`, and [fast-polish.md](fast-polish.md) § 1 finds nothing to launch |

**Forbidden launches** (workers must `COMPLIANCE: FAIL`):

- One Task prompt containing multiple sentence labels (e.g. “S1–S3”) when N ≤ 10
- Phase 1 / source-audit sentence Tasks
- Sentence Task for an **unchanged** label
- Missing Task plan or missing `findings_path`
- `phase2_math_task: skipped` when `caller: section-orchestrator`, `pace: full`, or `edit_gate: rewrite`

---

## Worker Step 0 — assignment compliance

Every worker runs **Step 0 first**. If `COMPLIANCE: FAIL`, **stop** — do not run specialist checks; still append a jsonl line recording the FAIL if possible.

### Sentence worker (label S*k*)

**PASS** only if:

- Prompt assigns **exactly one** label S*k* and **one** sentence body
- `Your assignment` names S*k* matching the Task description (`background sentence: S2`)
- Label is listed in `phase2_changed_labels`

**FAIL** examples: batched S1–S3; wrong label; unchanged S*k*.

### Narrative worker

**PASS** only if the prompt has the **full snapshot** (all N sentences) and a Task plan whose N matches.

### Math worker

Same scope as narrative. **FAIL** if launched on a prose-only passage without `phase2_math_task: launched`. When the plan says `skipped (no equations)`, no math Task is launched — not a violation.

### Worker output format

```text
### Assignment compliance
COMPLIANCE: PASS | FAIL
Role: sentence | narrative | math
Label: S<k> | full-passage | N/A
Reason: <one line if FAIL; "assignment matches task plan" if PASS>

### Specialist verification
<role-specific report — omit if COMPLIANCE: FAIL>
```

**Also append** to `findings_path` as soon as each finding (or `done`) is known — [job-state.md](job-state.md). Do not wait for the final report.

After `COMPLIANCE: PASS`, specialist work is **artifact-first** ([sentence-check-subagents.md](sentence-check-subagents.md) · [phase2-verify-subagents.md](phase2-verify-subagents.md)). Names match the Detect / Required-products columns in **`physics-paper-principles`**. An empty or missing **Diagnostics** block is incomplete specialist homework — the synthesizer marks that role `open` and `OVERALL: PARTIAL`. It is not a closed BLOCKER and not `CONFLICTS`. Fast polish does not skip Diagnostics.

Workers **must not** fix orchestrator mistakes — only report `COMPLIANCE: FAIL`.

---

## Synthesizer — procedural + content (per round)

Merge in **order**:

1. **Procedural compliance** — any worker `COMPLIANCE: FAIL` → `compliance_worker_reports: FAIL`. Relaunch that wave with a corrected plan (fresh Tasks). Do **not** block the user or withhold the marked draft.
2. **Task plan audit** — `phase1_sentence_tasks == 0`; `len(phase2_sentence_tasks) == C`; `phase2_math_task` skip only when legal; one sentence report (or jsonl `done`) per launched label; **no** `sentence_S1-S3` ranges.
3. **Diagnostics present** — each launched worker’s specialist report includes the required **Diagnostics** fields (not empty). Missing → that label/role `open`; `OVERALL: PARTIAL`. Not a closed BLOCKER.
4. **Severity adjudication** — closed BLOCKER classes in [severity.md](severity.md). Downgrade out-of-list BLOCKERs to SUGGEST. On fast polish, also apply [fast-polish.md](fast-polish.md) § 2.
5. **Content vs live text** — apply [merge-policy.md](merge-policy.md):
   - unresolved must-fix on **untouched** sentences → producer will auto-apply; not `CONFLICTS`
   - unresolved physical meaning (math class 6, or narrative class 6 if math skipped) → `OVERALL: CONFLICTS`; never invent the missing scientific choice. Thin motivation alone is SUGGEST
   - serious clash with user edits → `OVERALL: CONFLICTS`
   - interrupt / open labels and no serious clash → `OVERALL: PARTIAL`
   - otherwise → `OVERALL: PASS`
6. SUGGESTS do not fail a round. `PACKET_GAP` never fails a round.

Emit in CHECKS:

```text
compliance_orchestrator_plan: PASS | FAIL
compliance_worker_reports: PASS | FAIL
<one line per sentence label: sentence_S1: PASS | …>
...
math_step0: PASS | FAIL | N/A | N/A (skipped)
packet_gap: <count — 0 if none>
OVERALL: PASS | CONFLICTS | PARTIAL
```

---

## CHECKS block rules

| Rule | Example |
|------|---------|
| **One line per sentence label** | `sentence_S2: PASS` |
| **Forbidden range notation** | `sentence_S1-S3: PASS` |
| **Include compliance lines** | `compliance_orchestrator_plan: PASS` |
| **Synthesizer sets OVERALL only** | Producer copies verbatim into the audit drawer |

---

## Anti-patterns

| ❌ Violation | ✅ Correct |
|-------------|-----------|
| Wait to write `.tex` until PASS | Mark + write, then background check |
| Invent a physical criterion or resolve essential scientific ambiguity by guessing | Retain valid definitions; use definition halt only for the unresolved scientific choice |
| `Task(..., run_in_background: false)` and block the turn | `run_in_background: true`; end the turn |
| One Task for S1–S3 when N ≤ 10 | One Task per label |
| Phase 1 source-audit Tasks | `phase1_sentence_tasks: 0` |
| Producer sets `OVERALL` | Synthesizer only |
| Section orchestrator launches verifier Tasks | Chunk agent / micro producer only |
| Drop `findings.jsonl` on interrupt | Harvest; keep stale lines |

---

## Section orchestrator (macro)

- Pass full Task plan seed + `chunk_id` + `edit_gate` + `pace` + `N` into every micro chunk invocation.
- Must **not** launch micro verifier Tasks itself.
- May have **more than one** marked chunk/job at a time; one job per marked region.
- Record synthesizer outcome in `session.md` from CHECKS, not by inventing values.
