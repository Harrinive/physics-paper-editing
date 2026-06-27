# User communication (plain language)

**Read with the Read tool** on **every turn** when editing for a user — micro ([SKILL.md](SKILL.md)) or macro ([physics-paper-editing-section/SKILL.md](../physics-paper-editing-section/SKILL.md)).

**Audience split:** Skill files, Task prompts, disk state (`session.md`, `manifest.json`), and the **Audit log** block use internal pipeline terms. The **main narrative** of every user response uses plain language from this file.

**Hard rule:** Never drop or rewrite the verbatim `Mode:` line or `<!-- CHECKS -->` / `<!-- SECTION DONE -->` blocks — hooks depend on them. Place them only in **Audit log (for resume)** at the **end** of the response.

---

## Communication rules

1. **Lead with Status** — one plain-English sentence: what step you are on and progress (if macro).
2. **First turn of a job** — add a short **What to expect** (three bullets):
   - **Micro:** pre-edit review → draft changes → independent quality check → apply to `.tex`
   - **Macro:** setup → structure review → plan editable pieces → edit each piece → final read-through
3. **When pausing** — say why and give an exact reply (`continue`, answer the model form, etc.).
4. **Never expose agent architecture** in the user narrative — no Producer, synthesizer, COMPLIANCE, Task plan, Phase 1/2, Stage A–E, END TURN, micro/macro, chunk agent — unless the user asks how the skill works.
5. **Summarize checks in plain language** under **What happened** — e.g. “wording and notation look consistent” not “narrative_group2: PASS”.
6. **Link paths once** — edit workspace (`.physics-edit/<slug>/`), review notes (`findings-ledger.md`).

---

## Glossary — internal → say to user

| Internal (agent-only) | Say to user (examples) |
|-----------------------|-------------------------|
| Micro skill / ≤12 sentences | “This short passage edit” |
| Macro / section skill | “Whole-section edit” |
| Phase 1 / source verify | “Pre-edit review of your original text” |
| Phase 2 / output verify | “Independent quality check on the revised draft” |
| Edit gate: polish | “Light polish — tighten wording, keep your structure” |
| Edit gate: rewrite | “Substantial rewrite from placeholders / draft notes” |
| Ship / step 7 | “Applying verified edits to your `.tex` file” |
| `OVERALL: PASS` | “All checks passed” |
| `OVERALL: FAIL` | “Some checks need fixes — revising the draft” |
| Stage A | “Setup — read the section and confirm check settings” |
| Stage B | “Structure review — order, signposts, placeholders (no new body prose yet)” |
| Stage C | “Planning — split into editable pieces (≤12 sentences each)” |
| Stage D / chunk *k* of *N* | “Editing piece *k* of *N*” |
| Stage E / integration | “Final read-through — transitions between pieces” |
| `findings-ledger.md` | “Review notes” |
| `.physics-edit/` | “Edit workspace” |
| END TURN | “Pausing here — reply **continue** when ready” |
| Manifest / `session.md` | Do not mention unless user asks about resume |

---

## Status templates

### Micro — short passage edit

| Internal step | Status template |
|---------------|-----------------|
| Edit gate (step 3) | “Deciding edit scope: light polish or substantial rewrite.” |
| Phase 1 (step 4) | “Pre-edit review (step 1 of 3): reading your {N}-sentence passage before drafting changes.” |
| Produce draft (step 5) | “Drafting revisions (step 2 of 3).” |
| Phase 2 (step 6) | “Running an independent quality check on the revised draft (step 3 of 3).” |
| Ship (step 7) | “All checks passed — applying edits to `{file}`.” |
| Phase 2 FAIL (fix loop) | “Some checks flagged issues — revising the draft and re-checking.” |

### Macro — whole-section edit

| Internal stage | Status template |
|----------------|-----------------|
| A | “Whole-section edit — setup: reading the section and confirming check settings.” |
| B | “Whole-section edit — structure review (no new body prose yet).” |
| C | “Whole-section edit — planning {N} editable pieces.” |
| D (chunk) | “Whole-section edit — piece {k}/{N} ({id}) revised and checked; {M} pieces left.” |
| E | “Whole-section edit — final read-through at piece boundaries.” |
| Done | “Whole-section edit complete — all pieces checked and transitions reviewed.” |

### Pause templates (macro)

| After | Next step (user-facing) |
|-------|-------------------------|
| Stage A (await continue) | “Setup is ready. Reply **continue** when you want the structure review.” |
| Stage B | “Structure review is done. Skim the [review notes]({path}) if you like. Reply **continue** to split the section into editable pieces.” |
| Stage C | “Planning is done — {N} pieces ready. Reply **continue** to start editing piece 1.” |
| Stage D (each chunk) | “Piece {id} is done. Reply **continue** for piece {next_id}.” |
| Stage E complete | “Section edit complete. Your `.tex` is updated; review notes are in the edit workspace.” |

---

## Scope overflow message

When the passage has **>12 sentences** or the user asked for a whole `\section{...}`:

> This selection is longer than a single short-passage edit (more than 12 sentences). I can either:
> 1. **Edit the whole section** — structure review first, then piece-by-piece edits with checks (recommended for long text), or
> 2. **Narrow the quote** — pick ≤12 sentences and I will edit that passage directly.
>
> Tell me which you prefer, or attach the whole-section editing skill if you want option 1.

Do **not** say “micro scope”, “macro skill”, or “attach physics-paper-editing-section” in the user message.

---

## AskQuestion framing

Explain in chat **before** calling `AskQuestion` (not inside the tool):

| AskQuestion title | Say first |
|-------------------|-----------|
| *Verifier model profile* | “Which models should run the automated quality checks? The recommended defaults are fine for most edits — pick **Recommended** on each question unless you care about model choice.” |
| *Sentence checker model* | “Which fast model should check each sentence during the pre-edit review?” |
| *Sentence-level checking* | “This passage is long or tightly cross-linked — how should I run sentence-level checks?” |
| Edit scope (gate Q2) | “Should I lightly polish your wording or treat this as a substantial rewrite?” |

Keep AskQuestion **titles** unchanged.

---

## Response skeleton

Use this order in **every** editing response to the user:

```markdown
### Status
<plain-language one-liner; add progress for whole-section edits>

### What to expect
<only on first turn of a job — three bullets>

### Context
<passage/section summary: physics, placement, main claim — 2–4 sentences>

### What happened
<2–5 bullets: substance and check outcomes in plain language; [bracket comment] resolutions; deferred edits if any>

### Clarify
<one focused question if needed; omit if none>

### Your text
<edited passage, preview, or “not written yet — checks in progress”>

### Next step
<exact user action, or “Done — `{file}` updated”>

---
### Audit log (for resume)
<verbatim Mode: line — from synthesizer (micro) or orchestrator (macro)>
<verbatim <!-- CHECKS ... --> or <!-- SECTION DONE ... --> when applicable>
```

**Micro Phase 1 only (no Phase 2 yet):** Audit log may contain only `Mode: inline|subagents|asked-user · N sentences` (no CHECKS block until Phase 2 completes).

**Macro Stages A–C:** Audit log contains `Mode: section-edit · stage:<A|B|C> · <slug>` — no CHECKS required.

**Macro Stage D:** Audit log contains `Mode: section-edit · chunk:<id> · <micro Mode line verbatim>` plus micro CHECKS when chunk passes.

---

## What not to put in the user narrative

| Avoid | Use instead |
|-------|-------------|
| “Phase 2 verifier Tasks launched” | “Running an independent quality check on the draft” |
| “Stage E integration PASS” | “Final read-through passed — section edit complete” |
| “Synthesizer reported OVERALL: PASS” | “All checks passed” |
| “END TURN — await continue for Stage C” | “Reply **continue** when ready to plan editable pieces” |
| “findings-ledger open: 3” | “Three open items in the review notes” |
| “chunk c03 pass” | “Piece 3 of 7 complete” |
