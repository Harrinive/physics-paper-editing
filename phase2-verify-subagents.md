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
- [ ] No verifier `Task` was launched earlier in this turn.

---

## Workflow

```
1. AskQuestion — verifier model profile (unless valid skip — § Model selection gate)
2. Write passage summary → paste into every verifier prompt
3. Label S1, S2, … and identify changed labels (§ Changed sentences)
4. Launch in parallel when practical (run_in_background: false):
     • narrative verifier — full passage (deep tier)
     • math verifier — full passage when applicable (deep tier; or N/A report if no math)
     • sentence verifiers — one Task per changed label (fast tier)
5. Launch synthesizer — deep tier; pass all reports + changed/skipped label lists
6. PASS → step 7 (ship)  |  FAIL → producer fixes → restart from step 3 (reuse slugs; no re-AskQuestion)
```

**Task count:** narrative + math (if applicable) + synthesizer + one Task per changed sentence.

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
Mode: verify-subagents · <N> sentences · <C> changed · <M> Tasks · sentence:<Q1 slug> · deep:<Q2 slug> · synth:<Q3 slug>

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
