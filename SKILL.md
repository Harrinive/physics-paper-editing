---
name: physics-paper-editing
description: >-
  Standalone LaTeX prose editor for physics papers (≤12 sentences). Draft-first
  coworker loop: write marked working text, background-verify a snapshot,
  interrupt-safe harvest, three-way merge. Routes >12 sentences to
  physics-paper-editing-section. Loads checklists via Read tool.
---

# Physics Paper Editing (micro)

Expert scientific editor for physics and mathematics at graduate level. **Standalone** for passages **≤12 sentences**; routes longer passages to the macro skill.

## When to use

- Edit LaTeX physics or mathematics prose for a passage of **≤12 sentences**
- Run the coworker loop: draft into the `.tex` immediately, check in the background, merge on each round
- User gives a short quote, paragraph fragment, or caption block within micro scope

**Route elsewhere:** passages **>12 sentences** or whole `\section{...}` → **`physics-paper-editing-section`** ([Scope overflow](#scope-overflow)).

## Agent read order

| Situation | Read |
|-----------|------|
| **Standalone micro job (≤12 sentences)** | This file → [user-communication.md](user-communication.md) → [coworker-loop.md](coworker-loop.md) → step 2 table |
| **Scope overflow (>12 sentences)** | § Scope overflow below — route to macro skill; do **not** read [cross-skill.md](cross-skill.md) |
| **Invoked from macro Stage D** | This file + [Invoked by section macro](#invoked-by-section-macro-optional) + [cross-skill.md](cross-skill.md) § Verifier model profile |
| **Every resume / wake** | [job-state.md](job-state.md) for the live job, then [coworker-loop.md](coworker-loop.md) § Wake |

**Use this skill alone** when the user gives a passage of **≤12 sentences** — run the checklist below. No macro skill, no `cross-skill.md` on that path. Standalone jobs still write `.physics-edit/micro/<job_id>/` ([job-state.md](job-state.md)).

**First reply:** count typographic sentences. If ≤12, ask polish vs rewrite only if unclear; inherit pace and models ([gate.md](gate.md)). Then draft, mark, launch background checks, **end the turn**. User-facing copy: [user-communication.md](user-communication.md).

## Invoked by section macro (optional)

Read this section only when Stage D passes `chunk_text` + `edit_gate` + `pace` +
`session.md` via [chunk-contract.md](../physics-paper-editing-section/chunk-contract.md).

- Run the coworker loop on `chunk_text` only.
- Use supplied `edit_gate` and `pace`; do not re-ask.
- **Verifier models:** inherit from `session.md` when `user_confirmed: true`; else use recommended slugs and note once. Handoff: [cross-skill.md](cross-skill.md) § Verifier model profile.
- Set `caller: section-orchestrator` in the Task plan ([compliance-monitoring.md](compliance-monitoring.md)).
- Wrap that chunk’s `tex_anchor` span; one job per chunk.

## Purpose

Edit LaTeX prose as a **coworker**, not a blocking pipeline:

1. **Draft first** — producer writes using the checklists as principles.
2. **Mark** a construction area and leave the text in the `.tex`.
3. **Background-verify** a frozen snapshot; workers flush findings to disk.
4. **Merge** once per round; interrupt + harvest if the user changed related text.

The producer writes the draft and applies merge actions. It **must not** grade its own draft or set `OVERALL` — only the per-round **verifier synthesizer** may do that. `OVERALL` is a job-round status (`PASS` | `CONFLICTS` | `PARTIAL`), not a gate that blocks the first `.tex` write.

Canonical loop: [coworker-loop.md](coworker-loop.md).

---

## Unit of work

| | |
|--|--|
| **Scope** | One passage, **≤12 sentences** |
| **Input** | Passage + optional context (neighbors, section title, brief) |
| **Output (first turn)** | Marked draft in `.tex`; background job running; first-turn orientation |
| **Output (later wake)** | Receipt and/or one decision; marks updated or removed |

Passages **>12 sentences** are out of scope — see [Scope overflow](#scope-overflow).

---

## Standalone quick start

1. **Scope** — confirm ≤12 sentences ([Scope overflow](#scope-overflow) if not).
2. **Read** — [user-communication.md](user-communication.md), [coworker-loop.md](coworker-loop.md), step 2 table.
3. **Intake** — polish/rewrite only if unclear; inherit pace + models ([gate.md](gate.md)).
4. **Draft** — compose or polish; checklists are principles, not a pre-edit audit gate.
5. **Mark + write** — [job-state.md](job-state.md); snapshot; launch background checkers ([phase2-verify-subagents.md](phase2-verify-subagents.md)).
6. **End the turn** — user keeps editing.
7. **On wake** — interrupt if related; harvest; one merge ([merge-policy.md](merge-policy.md)); relaunch dirty labels or unmark.

---

## Scope overflow

When the target has **>12 sentences** or the user asks for a whole `\section{...}`:

1. Do **not** run the coworker loop on the full text in one turn.
2. Tell the user the passage exceeds a short-passage edit — copy in [user-communication.md](user-communication.md).
3. Offer: attach [physics-paper-editing-section](../physics-paper-editing-section/SKILL.md), **or** narrow to ≤12 sentences.

That is the **only** macro awareness required on a standalone micro job. Do not read [cross-skill.md](cross-skill.md) unless you are routing overflow or were invoked from macro Stage D.

---

## Roles and terms

| Term | Meaning |
|------|---------|
| **Producer** | Main agent — drafts, marks, applies merge; never sets `OVERALL` |
| **Sentence verifier** | Background Task — one sentence; 13 objectives; appends `findings.jsonl` |
| **Narrative verifier** | Background Task — full snapshot; four narrative groups |
| **Math verifier** | Background Task — full snapshot when math or logical argument present |
| **Verifier synthesizer** | Per **round** — sole `OVERALL` authority (`PASS` \| `CONFLICTS` \| `PARTIAL`) |
| **Task plan** | Required before any worker Task ([compliance-monitoring.md](compliance-monitoring.md)) |
| **Construction area** | `% PPE-BEGIN` / `% PPE-END` pair ([job-state.md](job-state.md)) |
| **Round** | Full wave completion **or** interrupt harvest, then one merge write |
| **Edit gate** | `polish` \| `rewrite` — how the draft is produced |
| **Fast / full** | Background-check scope only — never whether the user waits ([fast-polish.md](fast-polish.md)) |
| **BLOCKER** | Must-fix on untouched text (auto-apply) or serious vs user (report) |
| **SUGGEST** | Never auto-applies; never a decision |
| **Changed sentences** | Labels whose text differs from the prior snapshot / source |
| **CHECKS block** | Audit-drawer only; synthesizer is sole authority |
| **PACKET_GAP** | Fast-polish note that a finding needs more manuscript context — not a must-fix |

**Sentence-count thresholds:** [gate.md](gate.md). **Scope:** ≤12 micro; >12 route to macro.

### Agent tiers

| Tier | Who | Writes prose? | Dispatches Tasks? | Grades `OVERALL`? |
|------|-----|---------------|-------------------|-------------------|
| **Main agent** (Producer) | 1 agent | Yes (draft + merge) | Yes | **No** |
| **Verifier subagents** | sentence · narrative · math | No | No | No |
| **Verifier synthesizer** | 1 agent per round | No | No | **Yes (sole authority)** |

**Writer ≠ grader:** [compliance-monitoring.md](compliance-monitoring.md).

---

## Workflow checklist

**Hard rules:**

- Write the marked draft to `.tex` **before** checks finish. Do not wait for `OVERALL`.
- Producer must not grade its own draft or set `OVERALL`.
- Launch checkers `run_in_background: true`. End the turn after launch.
- On wake, harvest `findings.jsonl` before merging. Do not drop stale findings.
- **Publish Task plan** before any worker Task. **Never** batch ≤10 sentences into one sentence Task.
- User-facing turns follow [user-communication.md](user-communication.md) — no fake progress bars, no pipeline narration.

```
[ ] 1. Context — file, neighbors, [bracket comments] as editing instructions
[ ] 2. Read — user-communication.md, coworker-loop.md, checklists (table below)
[ ] 3. Intake — polish/rewrite if unclear; inherit pace + models ([gate.md](gate.md))
[ ] 4. Draft — principles from the checklists; no blocking source-audit phase
[ ] 5. Mark + snapshot — [job-state.md](job-state.md)
[ ] 6. Background verify — [phase2-verify-subagents.md](phase2-verify-subagents.md)
      [ ] Task plan; one Task per changed label; narrative + math when applicable
      [ ] run_in_background: true; workers append findings.jsonl
      [ ] End the turn (Mode: … · verify:running)
[ ] 7. On wake — related hashes → interrupt → harvest → merge ([merge-policy.md](merge-policy.md))
[ ] 8. Relaunch open/dirty labels or unmark; synthesizer CHECKS in the audit drawer
```

### Step 1 — Context

| Item | Source |
|------|--------|
| Topic and main claim | User or abstract / introduction |
| Section order | User or `main.tex` (or top-level `.tex`) |
| Files for this passage | User or paths around the selection |
| `[bracket comments]` | User inline editing instructions — strip from working copy, honor in edits |

### Step 2 — What to Read

| Condition | Read |
|-----------|------|
| Always | [user-communication.md](user-communication.md), [coworker-loop.md](coworker-loop.md), [sentence-checks.md](sentence-checks.md) |
| 2+ sentences | + [narrative-checks.md](narrative-checks.md) |
| Math, equations, or logical argument | + [math-checks.md](math-checks.md) |
| Intake | + [gate.md](gate.md) |
| Mark / snapshot / interrupt | + [job-state.md](job-state.md) |
| Merge round | + [merge-policy.md](merge-policy.md) |
| Launch or wake checkers | + [phase2-verify-subagents.md](phase2-verify-subagents.md), [sentence-check-subagents.md](sentence-check-subagents.md), [compliance-monitoring.md](compliance-monitoring.md) |
| `polish` + `pace: fast` + standalone | + [fast-polish.md](fast-polish.md) |
| Before any verifier Task | + [compliance-monitoring.md](compliance-monitoring.md) § Task plan block |

When length is ambiguous, load sentence + narrative. When math might appear, load math too.

---

## Response format

Follow [user-communication.md](user-communication.md) exactly — named state, receipt, optional decision, audit drawer. Do not use the old seven-section form or progress bars.

---

## Project-specific context (optional)

When the manuscript is the Ancilla Optimization / QEC error-budgeting paper:

- **Topic:** decomposing logical infidelity into error-mechanism contributions for realistic QEC devices.
- **Typical skeleton:** Introduction → Background → full QEC evolution → logical evolution graph → Markov chain → error-budget analysis → example.
- **Main sources:** `main.tex`, `Sections/*.tex` (read only what the user points to or what surrounds the edit).

For other papers, use only the generic workflow above.

---

## File map

**Coworker loop**

| File | Role |
|------|------|
| [coworker-loop.md](coworker-loop.md) | Draft → mark → snapshot → background verify → interrupt → merge |
| [job-state.md](job-state.md) | PPE marks, snapshot, `findings.jsonl`, interrupt prompt |
| [merge-policy.md](merge-policy.md) | Three-way merge rubric |
| [user-communication.md](user-communication.md) | Workbench UX — every user-facing turn |
| [gate.md](gate.md) | Job × pace; inherit models; sentence-count thresholds |
| [phase2-verify-subagents.md](phase2-verify-subagents.md) | Background checkers, prompts, per-round synthesizer |
| [sentence-check-subagents.md](sentence-check-subagents.md) | Sentence split, one Task per label, jsonl flush |
| [compliance-monitoring.md](compliance-monitoring.md) | Task plan, Step 0, synthesizer procedural checks |
| [fast-polish.md](fast-polish.md) | Fast standalone polish: narrower question, possible math skip |

**Checklists**

| File | Role |
|------|------|
| [sentence-checks.md](sentence-checks.md) | 13 sentence objectives (drafting principles + checkers) |
| [narrative-checks.md](narrative-checks.md) | Passage-level narrative groups |
| [math-checks.md](math-checks.md) | Math and logic checks |

## Related skills

| Skill | When |
|-------|------|
| **physics-paper-editing-section** | Passage **>12 sentences** or whole `\section{...}` |
| **sc-qubit-sim** | Scientific prose in simulation docs (`conventions/scientific-prose.md`) |

## Out of scope

- Passages **>12 sentences** or whole `\section{...}` — route to **`physics-paper-editing-section`**
- Waiting to write `.tex` until `OVERALL: PASS`
- Producer self-grading `OVERALL`
- BibTeX, figure files, or non-prose LaTeX (equations-only blocks with no prose claims)
