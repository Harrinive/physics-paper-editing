---
name: physics-paper-editing
description: >-
  Edits and proofreads LaTeX from physics papers: sentence clarity, narrative
  flow, and math/logic rigor. Use when the user asks to edit, revise, polish, or
  proofread manuscript text, improve academic writing, or fix wording in a
  scientific paper. Loads checklists by passage length; uses Task subagents for
  multi-sentence sentence-level checks when feasible.
---

# Physics Paper Editing

Expert scientific editor for physics and mathematics at graduate level.

## Agent workflow (every editing round)

Copy and track:

```
[ ] 1. Context — topic, section map, relevant .tex files; read neighbors if needed
[ ] 2. Load checklists — use decision table below; Read tool on each file (no memory)
[ ] 3. Sentence-level — inline OR Task subagents per sentence-check-subagents.md
[ ] 4. Draft — assemble edits; honor [bracket comments] as instructions
[ ] 5. Passage-level — narrative-checks.md and/or math-checks.md on full draft
[ ] 6. Respond — format in § Response; self-check against loaded checklists
[ ] 7. Apply — edit source in agent mode; dual-format output in ask mode
```

## Context (step 1)

If the user has not provided enough context, establish:

| Item | Source |
|------|--------|
| Topic and main claim | User or abstract / introduction |
| Section order | User or `main.tex` (or top-level `.tex`) |
| Files for this passage | User or paths around the selection |

Read surrounding `.tex` when placement, references, or notation are unclear.

## Which checklists to load (step 2)

**Always read files with the Read tool before editing** — do not rely on recall.

| Passage | Read |
|---------|------|
| One sentence or fragment | [sentence-checks.md](sentence-checks.md) |
| Two or more sentences | [sentence-checks.md](sentence-checks.md) + [narrative-checks.md](narrative-checks.md) |
| Any math, equations, or logical argument | Also [math-checks.md](math-checks.md) |

When length is ambiguous, load sentence + narrative. When math might appear, load math too.

## Sentence-level execution (step 3)

| Passage | Method |
|---------|--------|
| One sentence or fragment | Run all 10 objectives in [sentence-checks.md](sentence-checks.md) inline |
| Two or more sentences | Read [sentence-check-subagents.md](sentence-check-subagents.md) first, then subagents or inline per that file |

Narrative and math checklists stay with the **main agent** after sentence-level work (subagents do not run them).

## Response format (step 6)

**1. Passage summary**

- What the text does and how it flows logically.
- Where it sits in the section and relation to neighbors.
- Underlying physics and mathematics.

**2. Check report**

- **Sentence-level:** If subagents ran, silent fixes are in the assembled draft; name all **10 objectives** from `sentence-checks.md` and report only **unresolved** items (or “addressed in draft”). If inline, report all 10. Do not re-list fixes subagents already applied.
- **Narrative / math:** For each loaded file, go through every objective **in file order**; if N/A, say why.
- Include any explicit user editing directions.

**3. Clarify** — one focused question if guidance is ambiguous; do not finalize edits until resolved.

**4. Edited text**

- **Agent mode:** apply edits in the source `.tex` file.
- **Ask mode:** provide
  - **Rendered:** inline `\( … \)`, display `\[ … \]`.
  - **LaTeX source:** inline `\( … \)`, display `\begin{equation} … \end{equation}` in a fenced block for copy-paste.
- Extra variants only if word limit allows.

**5. Self-check** — re-run every loaded checklist against the final draft; fix gaps before sending.

## Checklist files (reference)

| File | Scope |
|------|--------|
| [sentence-checks.md](sentence-checks.md) | 10 sentence-level objectives (canonical list) |
| [sentence-check-subagents.md](sentence-check-subagents.md) | Task splitting, prompts, synthesis for ≥2 sentences |
| [narrative-checks.md](narrative-checks.md) | Paragraph through full paper |
| [math-checks.md](math-checks.md) | Definitions, logic, notation, quantifiers |

## Project-specific context (optional)

When the manuscript is the Ancilla Optimization / QEC error-budgeting paper, also know:

- **Topic:** decomposing logical infidelity into error-mechanism contributions for realistic QEC devices.
- **Typical skeleton:** Introduction → Background → full QEC evolution → logical evolution graph → Markov chain → error-budget analysis → example.
- **Main sources:** `main.tex`, `Sections/*.tex` (read only what the user points to or what surrounds the edit).

For other papers, use only the generic workflow above.
