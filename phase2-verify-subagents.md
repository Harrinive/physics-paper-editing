# Phase 2 — output verify

**Read with the Read tool** before launching Phase 2 ([SKILL.md](SKILL.md) step 6).

Phase comparison and loop rules: [verification-loop.md](verification-loop.md). Sentence splitting and prompts: [sentence-check-subagents.md](sentence-check-subagents.md).

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

## Workflow

```
1. Write passage summary → paste into every verifier prompt
2. Label S1, S2, … and identify changed labels (§ Changed sentences)
3. AskQuestion — verifier model (unless already chosen for this draft scope)
4. Launch in parallel when practical (run_in_background: false):
     • narrative verifier — full passage
     • math verifier — full passage (or N/A report if no math)
     • sentence verifiers — one Task per changed label
5. Launch synthesizer — pass all reports + changed/skipped label lists
6. PASS → step 7 (ship)  |  FAIL → producer fixes → restart from step 2
```

**Task count:** narrative + math (if applicable) + synthesizer + one Task per changed sentence.

---

## Producer rules

**Allowed:** track changed sentences; apply synthesizer fixes on FAIL; relaunch verifier suite on revised draft.

**Forbidden:**

- Running [sentence-checks.md](sentence-checks.md), [narrative-checks.md](narrative-checks.md), or [math-checks.md](math-checks.md) inline on the draft.
- Writing or guessing `OVERALL` without synthesizer output.
- Skipping narrative or math because the draft is "already checked" in Phase 1.
- Sentence verifier Tasks for **unchanged** labels.
- Resuming old verifier Tasks after a draft fix.

---

## AskQuestion — verifier model

**Before** launching Tasks, call **AskQuestion** unless the user already chose a model for **this same draft scope in this chat**.

**Title:** *Verifier subagent model*

Follow [sentence-check-subagents.md](sentence-check-subagents.md) §4 (one flagship per provider; exact slug in label). Use the chosen slug on **every** Phase 2 Task including the synthesizer.

---

## Verifier prompts

### Sentence verifier

Same template as [sentence-check-subagents.md](sentence-check-subagents.md) §6. Target is the **generated draft**, not the user's original quote.

```text
Task(
  subagent_type: "generalPurpose",
  readonly: true,
  model: <verifier model slug>,
  description: "Phase2 sentence verify: S<k>",
  prompt: <sentence-check-subagents.md §6 template>
)
```

### Narrative verifier

```text
You are a narrative verifier for a physics paper. You did NOT write this draft.

## Passage summary (shared)
<identical block in every Task>

## Draft under review
<full generated passage — LaTeX/text>

## Adjacent context (if helpful)
<1–3 sentences before/after from .tex, or omit>

## Instructions
Read and run every group and bullet in narrative-checks.md (Read tool if needed).
Do not edit the draft. Report each group in file order.

## Output format
### Narrative verification
**Group 1 — Core message and framing:** <findings or PASS>
**Group 2 — Logical arc and motivation:** <findings or PASS>
**Group 3 — Consistency and economy:** <findings or PASS>
**Group 4 — Claims and audience:** <findings or PASS>

**FAIL items:** <bulleted list with check name and one-line reason; or "none">
```

### Math verifier

```text
You are a math/logic verifier for a physics paper. You did NOT write this draft.

## Passage summary (shared)
<identical block in every Task>

## Draft under review
<full generated passage — LaTeX/text>

## Instructions
Read math-checks.md (Read tool if needed). Run Step 0 (classify statements), then type-specific checks.
If no math or logical argument: state that and mark math checks N/A — still complete the report.

## Output format
### Math verification
**Step 0 — Classifications:** <list each statement and type, or "no math statements">

**Per-statement / per-type findings:** <findings in file order>

**FAIL items:** <bulleted list with check name and one-line reason; or "none">
```

### Verifier synthesizer

```text
You are the verifier synthesizer. You did NOT write the draft. You decide whether the draft passes.

## Passage summary (shared)
<identical block>

## Draft under review
<full generated passage>

## Sentence scope
Total sentences: <N>. Changed (sentence-verified): <list>. Skipped (unchanged): <list>.

## Verifier reports
### Sentence reports (changed only)
<paste sentence verifier outputs, or "none — 0 changed sentences">

### Narrative report
<paste narrative verifier output>

### Math report
<paste math verifier output>

## Instructions
1. Merge all FAIL items from narrative, math, and changed-sentence reports. Any unresolved FAIL → OVERALL: FAIL.
2. Unchanged sentences were not sentence-verified; do not FAIL for sentence-level issues on skipped labels unless narrative or math caught them.
3. Emit the CHECKS block. You are the **only** agent that may set OVERALL.
4. If OVERALL: FAIL, list concrete fixes (no vague advice).

## Output format (required)
Mode: verify-subagents · <N> sentences · <C> changed · <M> Tasks · <model slug>

<!-- CHECKS
<one line per check — stable names, e.g. sentence_S2_obj3, narrative_group2_logical_arc>
...
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
