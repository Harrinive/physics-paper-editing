# Phase 2 — output verify

**Read with the Read tool** before launching Phase 2 ([SKILL.md](SKILL.md) step 6).

Required for **every** micro edit — standalone or macro chunk. **Canonical for:** model selection gate · changed-sentence scope · Phase 2 workflow. Macro verifier inheritance: [cross-skill.md](cross-skill.md) § Verifier model profile (chunk agents only).

Also read: [verification-loop.md](verification-loop.md) · [sentence-check-subagents.md](sentence-check-subagents.md) · [compliance-monitoring.md](compliance-monitoring.md).

---

## At a glance

| Always run (full passage) | Run only on changed sentences |
|---------------------------|-------------------------------|
| Narrative verifier | Sentence verifiers (all 13 objectives each) |
| Math verifier (when passage has math or logical argument) | |
| Verifier synthesizer (after all verifiers complete) | |

- **No gate.** Fresh verifier Tasks every iteration — never resume old Tasks.
- **Producer** must not inline-check the draft or set `OVERALL: PASS|FAIL`.
- **Synthesizer** is the sole authority for CHECKS and OVERALL.

---

## Roles

| Role | Who | May edit draft? | May emit CHECKS / OVERALL? |
|------|-----|-----------------|---------------------------|
| Producer | Main agent | Yes (step 5; fixes on FAIL) | **No** |
| Sentence verifiers | Task subagents (one per changed sentence) | Suggest **Edited** lines only | No |
| Narrative verifier | Task subagent | No | No |
| Math verifier | Task subagent | No | No |
| Verifier synthesizer | Task subagent | No | **Yes** |

Use **`readonly: true`** on every verifier Task.

---

## Changed sentences

Before launching sentence verifier Tasks, the **producer** labels **S1, S2, …** on the draft ([sentence-check-subagents.md](sentence-check-subagents.md) §2) and marks which labels **changed** relative to the immediately prior baseline:

| Iteration | Baseline | Compare to |
|-----------|----------|------------|
| First Phase 2 (after step 5) | User's source prose (after stripping `[bracket comments]`) | Producer's draft from step 5 |
| Major rewrite (Phase 1 skipped) | — | **Every** sentence is changed |
| Re-loop (after `OVERALL: FAIL`) | Draft before producer applied fixes | Revised draft |

**Changed:** label **S*k*** exists in both baseline and draft, but LaTeX/text differs (any edit — wording, inline math, punctuation affecting boundaries).

**Unchanged:** no sentence verifier Task. Narrative and math verifiers still receive the **full** draft.

**Record** changed and skipped labels for prompts and the Mode line (e.g. changed: `S2, S5`; skipped: `S1, S3, S4`).

**Zero changed sentences:** skip sentence Tasks; still run narrative (+ math if applicable) and synthesizer. Note `0 changed` in the Mode line.

---

## Model selection gate (hard stop)

**Do not launch any verifier `Task` until model slugs are resolved.**

```
Draft ready (step 5) ──► AskQuestion (*Verifier model profile*) ──► user answers ──► Tasks
                              ▲
                              │ skip only if valid (see below)
```

| Valid skip | Action |
|------------|--------|
| User already chose a profile for **this draft scope in this chat** | Reuse same three slugs (FAIL→fix loops) |
| Section `session.md` has `user_confirmed: true` and complete § Verifier model profile | Inherit `{ sentence, deep, synth }`; note `inherited from session.md (Stage A confirmed)` — no re-ask |
| Section brief supplied `verifier_profile` **only** | **Not a valid skip by itself** — must also have `session.md` `user_confirmed: true` from Stage A AskQuestion |

**Not a valid skip:** Phase 1 skipped; major rewrite; polish path; skill "recommended" slugs; your guess at good models; manifest/brief slugs without `session.md` `user_confirmed: true`.

**Forbidden before AskQuestion:**

- Any `Task(...)` call for sentence, narrative, math, or synthesizer verifiers.
- Announcing "default model profile" or silently picking slugs from § AskQuestion recommendations.

**Major rewrite path:** Phase 1 is skipped, but step 6 **always** runs. On the **first** Phase 2 iteration you **must** call `AskQuestion` — there is no Phase 1 sentence-model ask to substitute for it.

**Pre-launch self-check** (all must be true before the first `Task`):

- [ ] `AskQuestion` returned user choices, **or** a valid skip condition is documented.
- [ ] Three slugs recorded: sentence (Q1), deep (Q2), synth (Q3).
- [ ] **Task plan** published in response and pasted into every worker prompt ([compliance-monitoring.md](compliance-monitoring.md) § Task plan block).
- [ ] Phase 2: `phase2_sentence_tasks` lists **one label per changed sentence**; no batching when C ≤ 10.
- [ ] No verifier `Task` was launched earlier in this turn.

---

## Workflow

```
1. AskQuestion — verifier model profile (unless valid skip — § Model selection gate)
2. Write passage summary → paste into every verifier prompt
3. Label S1, S2, … and identify changed labels (§ Changed sentences)
4. Emit Task plan (phase2_sentence_tasks = changed labels only)
5. Launch in parallel when practical (run_in_background: false):
     • narrative verifier — full passage (deep tier)
     • math verifier — full passage when applicable (deep tier; or N/A report if no math)
     • sentence verifiers — one Task per changed label (fast tier)
6. Launch synthesizer — deep tier; pass Task plan + all reports + changed/skipped label lists
7. PASS (content + procedural) → step 7 ship  |  FAIL → fix draft and/or relaunch with corrected Task plan
```

**Task count:** narrative + math (if applicable) + synthesizer + **C** sentence Tasks (C = changed count). Mode line **M** must equal C.

---

## Producer rules

**Allowed:** track changed sentences; apply synthesizer fixes on FAIL; relaunch verifier suite on revised draft.

**Forbidden:**

- Launching verifier `Task`s before `AskQuestion` resolves model slugs (§ Model selection gate).
- Auto-selecting recommended/default slugs without user input.
- Running [sentence-checks.md](sentence-checks.md), [narrative-checks.md](narrative-checks.md), or [math-checks.md](math-checks.md) inline on the draft.
- Writing or guessing `OVERALL` without synthesizer output.
- Skipping narrative or math because the draft is "already checked" in Phase 1.
- Sentence verifier Tasks for **unchanged** labels.
- Resuming old verifier Tasks after a draft fix.
- Launching one sentence Task for multiple labels (compliance violation).
- Shipping when any worker reports `COMPLIANCE: FAIL` or synthesizer reports `compliance_orchestrator_plan: FAIL`.

---

## AskQuestion — verifier model profile

**Mandatory on first Phase 2 iteration** unless a valid skip in § Model selection gate applies. Reuse the same three slugs across every FAIL→fix loop iteration — do **not** re-ask on re-loops.

**Title:** *Verifier model profile*

**One form, three questions** — each option = one flagship (or fast tier) per provider, **exact slug in each label**, built from the session's allowed Task model list. Mark the skill's recommended pick with **(Recommended)** in the option label — the user must still confirm via `AskQuestion`; recommendations are **not** permission to skip asking.

1. **Sentence checker** (high volume, fast tier) — recommend **Cursor Composer (fast)** when available.
2. **Narrative & logic checker** (passage-level reasoning) — recommend **Claude flagship**.
3. **Synthesizer** (sets `OVERALL`; never fast tier) — recommend **Claude flagship**.

Narrative and math verifier Tasks share the slug from question 2. Sentence verifier Tasks use question 1. The synthesizer Task uses question 3.

If a recommended slug is unavailable in the session list, omit it and offer valid alternatives — still via `AskQuestion`, never silent substitution.

### Per-Task model assignment

| Task | Tier | Slug source |
|------|------|-------------|
| Sentence verifiers | Fast | Question 1 |
| Narrative verifier | Deep | Question 2 |
| Math verifier | Deep | Question 2 |
| Verifier synthesizer | Deep | Question 3 |

Keep `readonly: true` on every verifier Task.

---

## Verifier prompts

### Sentence verifier

Same template as [sentence-check-subagents.md](sentence-check-subagents.md) §6. Target is the **generated draft**, not the user's original quote.

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  model: <sentence-checker slug — fast tier, profile Q1>,
  description: "Phase2 sentence verify: S<k>",
  prompt: <sentence-check-subagents.md §6 template>
)
```

### Narrative verifier

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  model: <narrative+logic slug — deep tier, profile Q2>,
  description: "Phase2 narrative verify",
  prompt: <template below>
)
```

```text
You are a narrative verifier for a physics paper. You did NOT write this draft.

## Orchestrator task plan (verify in Step 0 — read-only)
<paste identical block from producer — compliance-monitoring.md>

## Passage summary (shared)
<identical block in every Task>

## Draft under review
<full generated passage — LaTeX/text>

## Adjacent context (if helpful)
<1–3 sentences before/after from .tex, or omit>

## Step 0 — Assignment compliance (run FIRST)
Confirm you received the **full passage** (all N sentences) and a valid Task plan. If fragment only, or polish + N≥2 but plan shows fewer Phase 1 labels than N, emit COMPLIANCE: FAIL and stop. See compliance-monitoring.md § Narrative worker.

## Instructions
If COMPLIANCE: PASS — read and run every group and bullet in narrative-checks.md (Read tool if needed).
Do not edit the draft. Report each group in file order.

## Output format
### Assignment compliance
COMPLIANCE: PASS | FAIL
Role: narrative
Reason: <one line>

### Narrative verification
**Group 1 — Core message and framing:** <findings or PASS>
**Group 2 — Logical arc and motivation:** <findings or PASS>
**Group 3 — Consistency and economy:** <findings or PASS>
**Group 4 — Claims and audience:** <findings or PASS>

**FAIL items:** <bulleted list with check name and one-line reason; or "none">
```

### Math verifier

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  model: <narrative+logic slug — deep tier, profile Q2>,
  description: "Phase2 math verify",
  prompt: <template below>
)
```

```text
You are a math/logic verifier for a physics paper. You did NOT write this draft.

## Orchestrator task plan (verify in Step 0 — read-only)
<paste identical block from producer>

## Passage summary (shared)
<identical block in every Task>

## Draft under review
<full generated passage — LaTeX/text>

## Step 0 — Assignment compliance (run FIRST)
Confirm full passage + Task plan present. See compliance-monitoring.md § Math worker.

## Instructions
If COMPLIANCE: PASS — read math-checks.md (Read tool if needed). Run Step 0 (classify statements), then type-specific checks.
If no math or logical argument: state that and mark math checks N/A — still complete the report.

## Output format
### Assignment compliance
COMPLIANCE: PASS | FAIL
Role: math
Reason: <one line>

### Math verification
**Step 0 — Classifications:** <list each statement and type, or "no math statements">

**Per-statement / per-type findings:** <findings in file order>

**FAIL items:** <bulleted list with check name and one-line reason; or "none">
```

### Verifier synthesizer

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  model: <synthesizer slug — deep tier, profile Q3>,
  description: "Phase2 verifier synthesizer",
  prompt: <template below>
)
```

```text
You are the verifier synthesizer. You did NOT write the draft. You decide whether the draft passes.

## Passage summary (shared)
<identical block>

## Draft under review
<full generated passage>

## Orchestrator task plan
<paste Task plan block from producer>

## Sentence scope
Total sentences: <N>. Changed (sentence-verified): <list>. Skipped (unchanged): <list>.
Expected Phase 2 sentence Tasks launched (C): <count>. Mode line M must equal C.

## Verifier reports
### Sentence reports (changed only)
<paste sentence verifier outputs, or "none — 0 changed sentences">

### Narrative report
<paste narrative verifier output>

### Math report
<paste math verifier output>

## Instructions
1. **Procedural compliance first:** Any worker `COMPLIANCE: FAIL` → `compliance_worker_reports: FAIL` → OVERALL: FAIL. Audit Task plan: Phase 2 requires M=C sentence Tasks; forbid `sentence_S1-S3` range lines — one line per label (`sentence_S1`, `sentence_S2`, …).
2. Merge specialist FAIL items from workers that passed Step 0. Any unresolved FAIL → OVERALL: FAIL.
3. Unchanged sentences were not sentence-verified; do not FAIL for sentence-level issues on skipped labels unless narrative or math caught them.
4. Emit the CHECKS block. You are the **only** agent that may set OVERALL.
5. If OVERALL: FAIL, list concrete fixes — distinguish **procedural** (relaunch Tasks with correct plan) vs **content**.

## Output format (required)
Mode: verify-subagents · <N> sentences · <C> changed · <M> Tasks · sentence:<Q1 slug> · deep:<Q2 slug> · synth:<Q3 slug>

<!-- CHECKS
compliance_orchestrator_plan: PASS|FAIL
compliance_worker_reports: PASS|FAIL
sentence_S1: PASS|FAIL|skipped
...
narrative_group1: PASS|FAIL
math_step0: PASS|FAIL|N/A
OVERALL: PASS|FAIL
-->

**Producer actions if FAIL:** <numbered fix list>
```

---

## After synthesizer returns

1. Copy the synthesizer's `Mode:` line and `<!-- CHECKS ... -->` block into the user response **verbatim**.
2. **`OVERALL: PASS`:** step 7 — write `.tex`, ship.
3. **`OVERALL: FAIL`:** producer applies fixes → relaunch workflow (§ Workflow).

On verifier Task timeout or incomplete report: relaunch that Task; producer must not grade inline.
