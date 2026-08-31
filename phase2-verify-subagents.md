# Phase 2 — output verify

**For agents:** Start with [SKILL.md](SKILL.md) § Agent read order. **Read with the Read tool** before launching Phase 2 ([SKILL.md](SKILL.md) step 6).

Required for **every** micro edit — standalone or macro chunk. **Canonical for:** model selection gate · changed-sentence scope · Phase 2 workflow. Macro verifier inheritance: [cross-skill.md](cross-skill.md) § Verifier model profile (chunk agents only).

Also read: [verification-loop.md](verification-loop.md) · [sentence-check-subagents.md](sentence-check-subagents.md) · [compliance-monitoring.md](compliance-monitoring.md). When `edit_gate: polish` + `pace: fast` + `caller: micro`: also read [fast-polish.md](fast-polish.md) before step 6.

---

## At a glance

| Always run (full passage) | Run only on changed sentences |
|---------------------------|-------------------------------|
| Narrative verifier | Sentence verifiers (all 13 objectives each) |
| Math verifier (when passage has math or logical argument — see footnote) | |
| Verifier synthesizer (after all verifiers complete) | |

Footnote — **fast polish, standalone micro only:** the math verifier Task is not launched when the quote and draft have no equations ([fast-polish.md](fast-polish.md) § 1). Every other combination of pace/`edit_gate`/`caller` launches math whenever math or a logical argument is present, exactly as before.

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

## Model profile gate (hard stop)

**Do not launch any verifier `Task` until model slugs are resolved.**

Resolve the profile in the **single editing intake**, together with job and
pace, after the ≤12-sentence scope check. Do not launch any editing Task before
that intake returns. Do not interrupt again when the draft becomes ready.

| Valid skip | Action |
|------------|--------|
| User already chose a profile for **this draft scope in this chat** | Reuse same three slugs (including FAIL→fix loops) |
| Section `session.md` has `user_confirmed: true` and complete § Verifier model profile | Inherit `{ sentence, deep, synth }`; note `inherited from session.md (Stage A confirmed)` — no re-ask |
| Section brief supplied `verifier_profile` **only** | **Not a valid skip by itself** — must also have `session.md` `user_confirmed: true` from Stage A AskQuestion |

**Not a valid skip:** Phase 1 skipped; major rewrite; polish path; skill "recommended" slugs; your guess at good models; manifest/brief slugs without `session.md` `user_confirmed: true`.

**Forbidden before the single intake:**

- Any `Task(...)` call for sentence, narrative, math, or synthesizer verifiers.
- Announcing a "default model profile" or silently picking recommended slugs.

**Rewrite path:** Phase 1 is skipped, but Phase 2 always runs with the profile
confirmed in intake.

**Pre-launch self-check** (all must be true before the first `Task`):

- [ ] Single editing intake returned job, pace, and model choices, **or** valid skip conditions are documented.
- [ ] Three slugs recorded: sentence (Q1), deep (Q2), synth (Q3).
- [ ] **Task plan** published in response and pasted into every worker prompt ([compliance-monitoring.md](compliance-monitoring.md) § Task plan block).
- [ ] Phase 2: `phase2_sentence_tasks` lists **one label per changed sentence**; no batching when C ≤ 10.
- [ ] No verifier `Task` was launched earlier in this turn.

---

## Workflow

```
1. Confirm the intake already resolved the verifier model profile
2. Write passage summary → paste into every verifier prompt
3. Label S1, S2, … and identify changed labels (§ Changed sentences)
4. Emit Task plan (phase2_sentence_tasks = changed labels only)
5. Launch in parallel when practical (run_in_background: false):
     • narrative verifier — full passage (deep tier)
     • math verifier — full passage when applicable (deep tier; or N/A report if no math);
       on `edit_gate: polish` + `pace: fast` + `caller: micro` with no equations in quote or
       draft, **do not launch this Task** — record `phase2_math_task: skipped (no equations)`
       ([fast-polish.md](fast-polish.md) § 1)
     • sentence verifiers — one Task per changed label (fast tier)
6. Launch synthesizer — deep tier; pass Task plan + all reports + changed/skipped label lists
   (math report is "skipped — no equations per Task plan" when § 5 skipped it)
7. PASS (content + procedural) → step 7 ship  |  FAIL → fix draft and/or relaunch with corrected Task plan
```

**Task count:** narrative + math (if applicable, else 0) + synthesizer + **C** sentence Tasks (C = changed count). Mode line **M** must equal C.

---

## Producer rules

**Allowed:** track changed sentences; apply synthesizer fixes on FAIL; relaunch verifier suite on revised draft.

**Forbidden:**

- Launching verifier Tasks before the single intake resolves model slugs.
- Auto-selecting recommended/default slugs without user input.
- Running [sentence-checks.md](sentence-checks.md), [narrative-checks.md](narrative-checks.md), or [math-checks.md](math-checks.md) inline on the draft.
- Writing or guessing `OVERALL` without synthesizer output.
- Skipping narrative or math because the draft is "already checked" in Phase 1.
- Sentence verifier Tasks for **unchanged** labels.
- Resuming old verifier Tasks after a draft fix.
- Launching one sentence Task for multiple labels (compliance violation).
- Shipping when any worker reports `COMPLIANCE: FAIL` or synthesizer reports `compliance_orchestrator_plan: FAIL`.

---

## Single intake — verifier model profile

Include these three questions in the same form as job and pace. Reuse the same
slugs across every FAIL→fix iteration.

**Title:** *Verifier model profile*

Each model question offers one flagship (or fast tier) per provider, with the
exact slug in each label and a recommended first option. Recommendations are
not permission to skip asking.

1. **Sentence checker** (high volume, fast tier) — recommend **Cursor Composer (fast)** when available.
2. **Narrative & logic checker** (passage-level reasoning) — at `pace: full` or `edit_gate: rewrite`, recommend a **flagship, high-reasoning-effort** model (e.g. Claude thinking-high). At `pace: fast` + `edit_gate: polish`, recommend a **medium-effort** flagship instead — not an "xhigh"/"thinking-high" reasoning variant, not a coding-specialist slug — and note on the form: "a high-reasoning-effort model adds several minutes at fast pace." ([fast-polish.md](fast-polish.md) § 5)
3. **Synthesizer** (sets `OVERALL`; never fast tier) — same pace-conditional recommendation as question 2.

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

## User's original source (only when edit_gate: polish, pace: fast, caller: micro)
<the user's quoted source, exactly as given, before this turn's edit>

## Step 0 — Assignment compliance (run FIRST)
Confirm you received the full passage and a valid Task plan. Audit Phase 1
against `pace`: fast polish requires `phase1_sentence_tasks: INLINE`; full
polish with N≥2 requires N labels. See compliance-monitoring.md.

## Instructions

**If `edit_gate: polish`, `pace: fast`, `caller: micro` (fast polish scope):**
Read and run every group and bullet in narrative-checks.md, but narrow classes
1–5 to what **this edit changed** relative to "User's original source" above —
do not chase a defect that exists unedited in that source against other parts
of the manuscript; report it as `SUGGEST — pre-existing in source` instead.
Also apply the closed word-delta class: a change to *only / all / any /
uniform / iff / equivalent / necessary / sufficient / always* ↔ *may / can /
does* (or the reverse) relative to the source is BLOCKER-eligible on its own.
Do not `Grep` or `Read` beyond what is in this prompt; if a finding needs more
manuscript context than supplied, report `PACKET_GAP: <what's missing>`
instead of searching for it. Full detail: fast-polish.md § 2–3.

**Otherwise (`pace: full`, `edit_gate: rewrite`, or `caller: section-orchestrator`):**
Read and run every group and bullet in narrative-checks.md against the full
manuscript context as usual. Apply its closed BLOCKER list; findings outside
it are SUGGEST.

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

**BLOCKER items:** <class + check + one-line reason; or "none">
**SUGGEST items:** <bulleted list; include "pre-existing in source" items here; or "none">
**PACKET_GAP:** <bulleted list, fast polish only; or "none">
```

### Math verifier

**Skip this Task entirely** when `edit_gate: polish`, `pace: fast`, `caller: micro`, and the quote and draft contain no equations ([fast-polish.md](fast-polish.md) § 1). Record `phase2_math_task: skipped (no equations)` in the Task plan and pass `### Math report: skipped — no equations per Task plan` to the synthesizer in place of a worker report. Do not launch this Task in that case.

Otherwise, launch as follows:

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

## User's original source (only when edit_gate: polish, pace: fast, caller: micro)
<the user's quoted source, exactly as given, before this turn's edit>

## Step 0 — Assignment compliance (run FIRST)
Confirm full passage + Task plan present. See compliance-monitoring.md § Math worker.

## Instructions

**If `edit_gate: polish`, `pace: fast`, `caller: micro` (fast polish scope):**
Read and run Step 0, then type-specific checks in math-checks.md, but narrow
to what **this edit changed** relative to "User's original source" above — a
defect that exists unedited in that source is `SUGGEST — pre-existing in
source`, not a BLOCKER, and is not chased against other parts of the
manuscript. Also apply the closed word-delta class from fast-polish.md § 2. Do
not `Grep` or `Read` beyond what is in this prompt; report `PACKET_GAP:
<what's missing>` instead of searching.

**Otherwise:** read math-checks.md and run the full audit against the
manuscript context as usual. Apply its closed BLOCKER list; findings outside
it are SUGGEST.

If no math or logical argument: state that and mark math checks N/A — still complete the report.

## Output format
### Assignment compliance
COMPLIANCE: PASS | FAIL
Role: math
Reason: <one line>

### Math verification
**Step 0 — Classifications:** <list each statement and type, or "no math statements">

**Per-statement / per-type findings:** <findings in file order>

**BLOCKER items:** <class + check + one-line reason; or "none">
**SUGGEST items:** <bulleted list; include "pre-existing in source" items here; or "none">
**PACKET_GAP:** <bulleted list, fast polish only; or "none">
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

## Closed BLOCKER lists (apply these — do not open narrative-checks.md or math-checks.md)

Narrative (5 classes): (1) contradiction or false relation, incl. an
unsupported transition/causal/contrast connective; (2) unbound essential
object; (3) broken reasoning (non-sequitur, reversed implication, omitted
essential premise); (4) claim-strength mismatch (necessity, sufficiency,
equivalence, generality, novelty, or evidence stronger than supplied);
(5) meaning loss or invention (dropped limitation, or a mechanism/assumption/
conclusion absent from the source). Everything else is SUGGEST.

Math (5 classes): (1) invalid or inconsistent mathematics; (2) undefined
essential object; (3) formula–prose mismatch; (4) unsupported logical
strength (necessity, sufficiency, equivalence, uniqueness, generality, "WLOG"
stronger than supplied); (5) incorrect import (misstated citation or
hypotheses that do not hold here). Everything else is SUGGEST.

Fast polish only (standalone micro — [fast-polish.md](fast-polish.md) § 2):
also treat a change to *only/all/any/uniform/iff/equivalent/necessary/
sufficient/always* ↔ *may/can/does* (or the reverse) relative to the user's
source as BLOCKER-eligible. A defect reported as "pre-existing in source" is
SUGGEST, not BLOCKER, regardless of severity — it was not introduced by this
edit.

## Verifier reports
### Sentence reports (changed only)
<paste sentence verifier outputs, or "none — 0 changed sentences">

### Narrative report
<paste narrative verifier output>

### Math report
<paste math verifier output, or "skipped — no equations per Task plan" when phase2_math_task: skipped>

## Instructions
1. **Procedural compliance first:** Any worker `COMPLIANCE: FAIL` →
   `compliance_worker_reports: FAIL` → OVERALL: FAIL. Audit Phase 1 against
   pace and Phase 2 as M=C sentence Tasks. Audit `phase2_math_task`: `skipped`
   is only valid on `edit_gate: polish` + `pace: fast` + `caller: micro`; a
   "skipped — no equations per Task plan" math report under those conditions
   is **not** a missing report and does not fail procedurally.
2. Adjudicate every reported BLOCKER against the pasted closed lists above.
   Downgrade out-of-list items to SUGGEST and record the downgrade. Never
   upgrade a SUGGEST without naming the matching class. On fast polish, a
   BLOCKER a worker labeled "pre-existing in source" is SUGGEST regardless of
   class.
3. Deduplicate blockers by root defect. Any unresolved BLOCKER → OVERALL: FAIL.
   SUGGEST-only → OVERALL: PASS.
4. Unchanged sentences were not sentence-verified; do not fail for wording
   issues on skipped labels unless narrative or math identifies a BLOCKER.
5. Sum every `PACKET_GAP` line across worker reports into `packet_gap` in
   CHECKS (count, 0 if none). A PACKET_GAP never fails the passage on its own.
6. Emit the CHECKS block. You are the only agent that may set OVERALL.
7. If OVERALL: FAIL, return `FAILED_SET`: the minimal deduplicated set of
   procedural defects and unresolved BLOCKERs. Keep SUGGESTS separate.

## Output format (required — this is the final output of this Task; do not
## add commentary, explanation, or a follow-up message after this block)
Mode: verify-subagents · <N> sentences · <C> changed · <M> Tasks · sentence:<Q1 slug> · deep:<Q2 slug> · synth:<Q3 slug>

<!-- CHECKS
compliance_orchestrator_plan: PASS|FAIL
compliance_worker_reports: PASS|FAIL
sentence_S1: PASS|FAIL|skipped
...
narrative_group1: PASS|FAIL
math_step0: PASS|FAIL|N/A|N/A (skipped)
severity_downgrades: <count>
packet_gap: <count>
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
